from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from luis_sdk import LUISClient
import urllib.request
import urllib.parse
import http.client
import json
# Simple WebSocket for single-user chat bot

class ChatServer(WebSocket):

    def handleMessage(self):
        # Echo message back to client
        message = self.data
        
        try:
            #Create a LUIS Client by passing in the APP ID and APP Key
            #Then uses the LUIS Client methods provided in the LUIS SDK
            CLIENT = LUISClient(APPID,APPKEY, True)
            response = CLIENT.predict(message)
            #The response received from LUIS predict would be passed in to process_res
        
            resp = process_res(response)
            self.sendMessage(resp)

        except Exception as exc:
            print(exc)
            self.sendMessage('I\'m sorry I do not understand you.')
           


    def handleConnected(self):
        print(self.address, 'connected')
        

    def handleClose(self):

        print(self.address, 'closed')


def process_res(res):
    '''
    A function that processes the luis_response object and prints info from it.
    :param res: A LUISResponse object containing the response data.
    
    '''

    #These data would be printed in the server 
    print('LUIS Response: ')
    print('Query: ' + res.get_query())
    print('Top Scoring Intent: ' + res.get_top_intent().get_name())

    print('Entities:')
    for entity in res.get_entities():
        print('"%s":' % entity.get_name())
        print('Type: %s, Score: %s' % (entity.get_type(), entity.get_score()))
        #The entity which is the location would be passed into the get_weather method
        #The method would call the API to retrieve the current weather data
        #weather_data would be where all the data will be stored from the API response
        weather_data = get_weather(entity.get_name())
        try:
            #Formatting the reply to the user
            #The weather data returned is in JSON
            #It would have lists and dict in the decoded JSON
            reply = 'Weather at ' + entity.get_name() + '<br/>' 
            reply += 'Weather condition : ' + str(weather_data['weather'][0]['description']) + '<br/>'
            reply += 'Temperature : ' + str(weather_data['main']['temp']) + 'C <br/>'
            reply += 'Humidity : ' + str(weather_data['main']['humidity']) + '%'
            return reply
        except Exception as exc:
            print(exc)

def get_weather(location):
    #Get weather is to retrieve the current weather data through the OpenWeatherAPI
    try:
        #Insert the app ID from OpenWeather
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&units=metric&appid=bed208a703f86ae1f7afc93f73e254b9'
        response = urllib.request.urlopen(api)
        data = response.read()
        #The response from the API call is read and decoded from the JSON replied
        
        weather = json.loads(data.decode('UTF-8'))
        #return the json object of weather
        return weather
    except Exception as exc:
        print(exc)
        
        
        #bed208a703f86ae1f7afc93f73e254b9

try:
    #Insert the APP ID and APP Key from LUIS
    APPID = 'b81195cb-904c-48ef-adaf-7b12c664dc42'
    APPKEY = '5a3dd24659a240b9b1721444fee819d3'

    server = SimpleWebSocketServer('', 8000, ChatServer)
    server.serveforever()
    

except Exception as exc:
    print(exc)

