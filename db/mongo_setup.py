import urllib
import mongoengine
from dotenv import load_dotenv
import os

def global_init():
    load_dotenv()
    mongoengine.register_connection(alias="core", name="xander-bot")
    username = urllib.parse.quote_plus(os.getenv('MONGODB_USERNAME'))
    password = urllib.parse.quote_plus(os.getenv('MONGODB_PASSWORD'))
    mongoengine.connect(
        host="mongodb+srv://%s:%s@discord-bots.8kzsgnr.mongodb.net/xander-bot?retryWrites=true&w=majority" % (username, password))
    print("MongoDB connection successful")
