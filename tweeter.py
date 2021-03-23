import twitterAuth
returns = twitterAuth.twitterAuth()

api = returns[0]

def status_update(text):
    api.update_status(status = text)

def tweet_s():
    tweets = api.user_timeline(id = returns[1], count = 1)[0]
    return tweets
