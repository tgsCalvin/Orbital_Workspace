      // Path to post message
      var _PATH = 'api/postmessage';

      // Current state of client
      var state = {
        app_key: '{{appid}}',
        token: '{{token}}',
        msg: '{{message}}'
      };

      // Packet structure to send message
      var pkt = {
        clientID: '{{appid}}',
        token: '{{token}}',
        roomID: '{{roomID}}',
        msg: '{{message}}'
      };

      sendMessage = function( {
        var tempMsg = document.getElementById('sendMsg').value;
        document.getElementById('msg').value+= "I say: " + tempMsg+"\n";
        pkt.msg= tempMsg;
        var req=JSON.stringify(pkt);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', _PATH, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader("Content-length", req.length);
        xhr.setRequestHeader("Connection", "close");

        xhr.onreadystatechange = function() {//Call a function when the state changes.
            if(xhr.readyState == 4 && xhr.status == 200) {
                //alert(xhr.responseText);
            }
        }

        xhr.send(req);
      };
      onOpened = function() {
        document.getElementById('msg').value += {{message}}
      };
      
      onMessage = function(m) {
        document.getElementById('msg').value += m.data
      };
      
      openChannel = function() {
        var token = '{{ token }}';
        var channel = new goog.appengine.Channel(token);
        var handler = {
          'onopen': onOpened,
          'onmessage': onMessage,
          'onerror': function() {},
          'onclose': function() {}
        };
        var socket = channel.open(handler);
        socket.onopen = onOpened;
        socket.onmessage = onMessage;
      };
      
      initialize = function() {
        openChannel();
      };

      setTimeout(initialize, 100);
