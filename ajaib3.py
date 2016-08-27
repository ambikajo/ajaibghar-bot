import sys
import time
import json    
import telepot
import requests
import googlemaps
import random
from pprint import pprint

# Getting the token from command-line is better than embedding it in code,
# because tokens are supposed to be kept secret.
TELEGRAM_API_TOKEN = sys.argv[1]
GOOGLE_MAPS_API_TOKEN = sys.argv[2]
GOOGLE_MAPS_PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=' + GOOGLE_MAPS_API_TOKEN
RIJKS_API_TOKEN = sys.argv[3]
RIJKS_COLLECTION_URL = 'https://www.rijksmuseum.nl/api/en/collection?format=json&key=' + RIJKS_API_TOKEN
COOPER_ACCESS_TOKEN = sys.argv[4]
COOPER_COLLECTION_URL = 'https://api.collection.cooperhewitt.org/rest/?method=cooperhewitt.search.objects&access_token=' + COOPER_ACCESS_TOKEN
BROOKLYN_API_TOKEN = sys.argv[5]
BROOKLYN_COLLECTION_URL = 'https://www.brooklynmuseum.org/opencollection/api/?method=&format=json&key=' + BROOKLYN_API_TOKEN


def handle(msg):
     content_type, chat_type, chat_id = telepot.glance(msg)
     #print (content_type, chat_type, chat_id)
     chat_id = msg['from']['id']
     
     if content_type == 'text':
        #for text query will send a link from Rijksmuseum 
        SEARCH_TEXT = msg['text'] 
        bot.sendChatAction(chat_id, 'typing')
        #requests for Rijksmuseum
        results = requests.get(RIJKS_COLLECTION_URL +'&imgonly=true'+ '&q=' + SEARCH_TEXT)
        objects_rijks = results.json()['artObjects']
        
        #requests for Cooper Hewitt Museum
        results_cooper = requests.get(COOPER_COLLECTION_URL + '&query='+ SEARCH_TEXT + '&page=1&per_page=100')
        objects_cooper = results_cooper.json()['objects']
        
        #requests for Brooklyn Museum
        #results_brooklyn = requests.get(BROOKLYN_COLLECTION_URL + '&query='+ SEARCH_TEXT)
       # objects_brooklyn = results_brooklyn.json()[....]
        
        #pprint (cooper_link)
         #if the list is empty, i.e., there is nothing in the search 
        if len(objects_rijks) == 0:
            reply =  bot.sendMessage (chat_id, 'Sorry, I couldnt find anything try another search.') 
        
        elif len(objects_cooper) == 0:    
            reply =  bot.sendMessage (chat_id, 'Sorry, I couldnt find anything try another search.') 
            
        #elif len(objects_brooklyn) == 0:
           # reply =  bot.sendMessage (chat_id, 'Sorry, I couldnt find anything try another search.')     
      
         #randomly selected link from the search
        else:
            #pick random link from RijksMuseum
            rijks_link = random.choice(objects_rijks)['links']['web']  
            
            #pick random link from Cooper Hewitt Museum
            cooper_link = random.choice (objects_cooper)['url']
            
            #pick random link from Brooklyn Museum
            #brooklyn_link = random.choice(objects_brookly)[....]
            
            #place random link in array can add more museums to this
            array_link = [rijks_link , cooper_link]
            #pick one random link from array 
            any_link = random.choice(array_link)
            pprint (any_link)
            
            reply = bot.sendMessage(chat_id, any_link)
            
         
     elif content_type == 'location':
        #Collect latitude and longitude based on the location sent by user
        DROP_PIN_LAT = msg['location']['latitude']
        DROP_PIN_LONG = msg['location']['longitude']
       
        #initiate the Google Maps json file
        results = requests.get(GOOGLE_MAPS_PLACES_URL + '&location=' + str(DROP_PIN_LAT) + ',' + str(DROP_PIN_LONG) + '&radius=3000&types=museum&art_gallery')
        objects = results.json()['results']
        
        #choose one search results randomally
        museum_nearby = random.choice(objects)
        
        #pick the name and vicinity of the randomly chosen museum
        museum_name = museum_nearby['name']
        museum_vicinity = museum_nearby['vicinity']
       
        bot.sendChatAction(chat_id, 'typing')
        
        #reply with museum name and nearby address
        reply = bot.sendMessage(chat_id, (museum_name) + ', ' + 'near' + ' ' + (museum_vicinity))
        
        
     else:
         #if not location or text query
         reply = bot.sendMessage(chat_id, 'I can only manage text and location at the moment!')
         
          
         
bot = telepot.Bot(TELEGRAM_API_TOKEN)
#bot.notifyOnMessage(handle)
print ('Listening ...')
bot.message_loop(handle)
# Keep the program running.
while 1:
    time.sleep(100)

#trying to send a json link to through the bot