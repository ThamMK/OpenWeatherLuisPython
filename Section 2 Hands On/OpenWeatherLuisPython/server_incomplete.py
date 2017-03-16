from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


# Simple WebSocket for single-user chat bot
class ChatServer(WebSocket):

    def handleMessage(self):
        # echo message back to client
        message = self.data
        
        self.sendMessage(response)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

try:
    #Insert the APP ID and APP Key from LUIS
    APPID = 'LUIS_APP_ID'
    APPKEY = 'LUIS_APP_KEY'
    
    server = SimpleWebSocketServer('', 8000, ChatServer)
    server.serveforever()
    

except Exception as exc:
    print(exc)
