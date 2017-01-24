import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json

consumer_key = 'e0025rM6yZa3H6LT4ZFDv9KgT'
consumer_secret = '1wxtYLZrhwtzACVUSWpx3CpU4vTX5wyjSM51icnBbi7MVRwVbr'
access_token = '767779112-8UcZ3tMIykqXNXxZr4c56Y27HgJa5iN3fZQuEETT'
access_secret = 'NTYgdSq4w3BkwyYjYXSvsKv9a8Uaaus7lIGv2ltDVQ4zm'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            client = MongoClient('localhost',27017)
            db = client['twitter_db']
            collection = db['twitter_collection']
            tweet = json.loads(data)
            collection.insert(tweet)
            return True
            #with open('python.json', 'a') as f:
             #   f.write(data)
                
        except BaseException as e:
            print("Error on_data:",str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#Acura',
'#Audi',
'#BMW',
'#Buick',
'#Cadillac',
'#Chevrolet',
'#Chrysler',
'#Dodge',
'#Fiat',
'#Ford',
'#GMC',
'#Genesis',
'#Honda',
'#Hyundai',
'#Infiniti',
'#Jaguar',
'#Jeep',
'#Kia',
'#LandRover',
'#Lexus',
'#Lincoln',
'#Maserati',
'#Mazda',
'#Mercedes-Benz',
'#MiniCooper',
'#Mitsubishi',
'#Nissan',
'#Porsche',
'#Ram',
'#Scion',
'#Subaru',
'#Tesla',
'#Toyota',
'#Volkswagen',
'#Volvo'])
