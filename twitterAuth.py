import tweepy
import json
import os

def twitterAuth():
    with open("twitter_reg.json", "r") as t:
        tweeters = json.load(t)
    t.close()

    with open("twitterGuildID.txt", "r") as g:
        IDs = g.readlines()
    g.close()

    gid = str(IDs[-1].strip('\n'))

    with open("tempCreds.json", "w") as c:
        c.write("{}")

    with open("tempCreds.json", "r") as c:
        keys = json.load(c)
    c.close()

    keys[gid] = [
        tweeters[gid][2],
        tweeters[gid][3],                 
        tweeters[gid][4],                   
        tweeters[gid][5]    
    ]

    with open("tempCreds.json", "w") as c:
        json.dump(keys, c, indent=4)
    c.close()

    auth = tweepy.OAuthHandler(keys[gid][0], keys[gid][1])
    auth.set_access_token(keys[gid][2], keys[gid][3])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    twitter_client_id = api.me().id
    
    if os.path.exists("tempCreds.json"):
        os.remove("tempCreds.json")

    auth = tweepy.OAuthHandler('', '')
    auth.set_access_token('', '')

    return [api, twitter_client_id]
