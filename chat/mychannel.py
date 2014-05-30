import datetime
import logging
import os
import random
import re
import webapp2
import json

from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import hashlib

receiverid = "receiverappid" 
senderid = "senderappid"

def randomString(length):
  s = hashlib.sha256()
  ret = "a"
  while len(ret) < length:
    s.update(str(random.random()))
    ret += s.hexdigest()
  return ret[0:length]


class chatRoom(ndb.Model):
  """Room class to maintain separate chat rooms"""
  roomID = ndb.StringProperty(required=True)
  participants = ndb.StringProperty(repeated=True)
  participantTokens = ndb.StringProperty(repeated=True)
  histChat = ndb.TextProperty(indexed=False)
    

class MainPage(webapp2.RequestHandler):
  """The main UI page, renders the 'index.html' template."""

  def get(self):
    """Renders the main page. When this page is shown, we create a new
    channel to push asynchronous updates to the client."""
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    template_values = {'senderid': senderid, 'receiverid': receiverid}
    self.response.out.write(template.render(path, template_values))

class CreateChannel(webapp2.RequestHandler):
  def get(self):
    clientID = randomString(5)
    tempRmID = randomString(5)
    token = channel.create_channel(clientID)
    msg = clientID + " has joined the chat"

    newRoom = chatRoom(roomID=tempRmID,
                        participants=[clientID],
                        participantTokens=[token],
                        histChat=msg)
    newRoom.put()

    template_values = {'token': token,
                      'appid': clientID,
                      'message': msg,
                      'roomID': tempRmID}

    path = os.path.join(os.path.dirname(__file__), 'mychat.html')
    self.response.out.write(template.render(path, template_values))

class PostMessage(webapp2.RequestHandler):
  def post(self):
    req = json.loads(self.request.body)
    self.response.out.write("message sent to Room "+ req['roomID'])

    qry = chatRoom.query(chatRoom.roomID == req['roomID']).get()

    tempmsg = req['clientID'] + " says: " + req['msg']
    qry.histChat += "\n"+tempmsg
    qry.put()

    for participantToken in qry.participantTokens:
      if(participantToken != req['token']):
        channel.send_message(participantToken, tempmsg)

class JoinChannel(webapp2.RequestHandler):
  def get(self):
    req =self.request.get('id')
    if(req != ''):

      qry = chatRoom.query(chatRoom.roomID == req)

      if(qry):
        clientID = randomString(5)
        token = channel.create_channel(clientID)
        msg = clientID + " has joined the chat"

        res = qry.get()
        res.participants.append(clientID)
        res.participantTokens.append(token)
        res.histChat+="\n"+msg
        for participantToken in res.participantTokens:
          channel.send_message(participantToken, msg)
        template_values = {'token': token,
                      'appid': clientID,
                      'message': res.histChat,
                      'roomID': req}
        res.put()

        path = os.path.join(os.path.dirname(__file__), 'mychat.html')
        self.response.out.write(template.render(path, template_values))

class MobileChannel(webapp2.RequestHandler):
  def get(self):
    req =self.request.get('id')
    if(req != ''):

      qry = chatRoom.query(chatRoom.roomID == req)

      if(qry):
        clientID = self.request.get('clientID')
        token = channel.create_channel(clientID)
        msg = clientID + " has joined the chat"

        res = qry.get()
        res.participants.append(clientID)
        res.participantTokens.append(token)
        res.histChat+="\n"+msg
        for participantToken in res.participantTokens:
          channel.send_message(participantToken, msg)
        template_values = {'token': token,
                      'appid': clientID,
                      'message': res.histChat,
                      'roomID': req}
        res.put()

        path = os.path.join(os.path.dirname(__file__), 'mobileClient.html')
        self.response.out.write(template.render(path, template_values))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createchannel', CreateChannel),
    ('/api/postmessage', PostMessage),
    ('/mobile', MobileChannel),
    ('/joinchat', JoinChannel)], debug=True)
