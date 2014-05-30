import endpoints
from google.appengine.ext import ndb
from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'myChannelEndpoint'

myChannel = endpoints.api(name='library', version='v1.0')

class chatRoom(ndb.Model):
  """Room class to maintain separate chat rooms"""
  roomID = ndb.StringProperty(required=True)
  participants = ndb.StringProperty(repeated=True)
  participantTokens = ndb.StringProperty(repeated=True)
  histChat = ndb.TextProperty(indexed=False)

class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)

class pktMsg(messages.Message):
    """Greeting that stores a message."""
    token = messages.StringField(1)
    clientID = messages.StringField(2)
    roomID = messages.StringField(3)
    message = messages.StringField(4)

class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)

STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])

@myChannel.api_class(resource_name='chatApi', path='chat')
class chatApi(remote.Service):
	"""Chat API Version 1.0"""

	@endpoints.method(message_types.VoidMessage, pktMsg,
		              path='test', http_method='GET',
		              name='chatApi.test')
	def test(self, unused_request):
		qry = chatRoom.query().get();
		res = pktMsg(token="asd", clientID="asd", roomID=qry.roomID, message="test")
		return res

@myChannel.api_class(resource_name='helloworld', path='greeting')
class HelloWorldApi(remote.Service):
    """Helloworld API v1.0"""

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

APPLICATION = endpoints.api_server([myChannel])