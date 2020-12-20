import tweepy
from tweepy.error import *
import sys, os, json, webbrowser

CONFIG_FILE = "twitter_bot.config"
def version():
    res = "simple_twit, version: 0.5"
    print(res)
    return res

#creates api with my developer twitter account
def create_api():
    consumer_key = "A0iWBnhbKksbczd4F4N2Ehxkt"
    consumer_secret = "VT9UMUdHvYTctufRntPgTH64KwqZllMf4jAdy7qRHvBMiLp0Dq"
    
    access_token = None
    access_token_secret = None
    verify_access = True
    
    if os.path.exists(CONFIG_FILE):
        print("READING AUTHORIZATION FROM CONFIG FILE")
        f = open(CONFIG_FILE, "r")
        config = json.load(f)
        access_token = config["access_token"]
        access_token_secret = config["access_secret"]
        f.close()
        verify_access = False
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    if verify_access:
        print("AUTHORIZING THROUGH WEB INTERFACE") 
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError as e:
            print("REQUEST VERIFIER URL", e)
        
        print(redirect_url)
        print()
        webbrowser.open(redirect_url)
        
        verifier = input("Enter Verifier: ")
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError as e:
            print("REQUEST ACCESS TOKEN", e)

        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        config = {"access_token" : access_token, 
                  "access_secret" : access_token_secret}
        f = open(CONFIG_FILE, "w")
        json.dump(config, f)
        f.close()
        
    if access_token != None:
        auth.set_access_token(access_token, access_token_secret)
    else:
        print("AUTHENTICATION FAILED: EXITING PROGRAM!")
        sys.exit()

    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
    return api

def post_tweet(api = None, text = ""):
    usage = "USAGE: post_tweet(api <a tweepy api object>, text <a string>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if text == "":
        print("ERROR: You must pass a string to this function.")
        print(usage)
        return
    try:
        result = api.update_status(status = text)
    except TweepError as e:
        print(e)
        return
    return result

def send_reply_tweet(api = None, text = "", id = None):
    usage = "USAGE: send_tweet(api <a tweepy api object>, text <a string>, id <an int>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if text == "" or "@" not in text:
        print("ERROR: You must pass a string to this function.")
        print("ERROR: The text must include @username for the author of the" +
              " tweet to which this is a reply.")
        print(usage)
        return
    if id == None:
        print("ERROR: You must pass a status id in order to send a reply.")
    try:
        result = api.update_status(status = text, in_reply_to_status_id = id)
    except TweepError as e:
        print(e)
        return
    return result

def send_media_tweet(api = None, text = "", filename = ""):
    usage = "USAGE: send_media_tweet(api <a tweepy api object>, text <a string>, filename <a string>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if filename == "":
        print("ERROR: you must pass a filename as a string to this function.")
        print(usage)
        return
    try:
        mo = api.media_upload(filename)
        result = api.update_status(status = text, media_ids = [mo.media_id])
    except TweepError as e:
        print(e)
        return
    return result

def retweet(api = None, id = None):
    usage = "USAGE: retweet(api <a tweepy api object>, id <numerical id of tweet>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if id == None:
        print("ERROR: You must pass an numerical status id to this function.")
        print(usage)
        return
    try:
        result = api.retweet(id = id, tweet_mode = "extended")
    except TweepError as e:
        print(e)
        return
    return result

def get_tweet(api = None, id = None):
    usage = "USAGE: get_tweet(api <a tweepy api object>, id <numerical id of tweet>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if id == None:
        print("ERROR: You must pass an numerical status id to this function.")
        print(usage)
        return
    try:
        result = api.get_status(id = id, tweet_mode = "extended")
    except TweepError as e:
        print(e)
        return
    return result

def get_retweets(api, id, count = 20):
    usage = "USAGE: get_retweets(api <a tweepy api object>, id <numerical id of tweet>, "
    usage += "count <number of tweets to retrieve>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if id == None:
        print("ERROR: You must pass an numerical status id to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.retweets, id = id, tweet_mode = "extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets

def get_retweeters(api, id, count = 20):
    usage = "USAGE: get_retweeters(api <a tweepy api object>, id <numerical id of tweet>, "
    usage += "count <number of user ids to retrieve>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage) 
        return
    if id == None:
        print("ERROR: You must pass an numerical status id to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for user_id in tweepy.Cursor(api.retweeters, id = id, tweet_mode = "extended").items(count):
            tweets.append(user_id)
    except TweepError as e:
        print(e)
        return
    return tweets

def get_home_timeline(api = None, count = 20):
    usage = "USAGE: get_home_timeline(api <a tweepy api object>, "
    usage += "count <number of tweets to retrieve>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.home_timeline, tweet_mode = "extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return []
    return tweets
    
def get_user_timeline(api = None, user = "", count = 20):
    usage = ("USAGE: get_user_timeline(api <a tweepy api object>, " +
             "user <name of user>, count <number of tweets to retrieve>)")
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass an user identifier string to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id = user, tweet_mode = "extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets

def get_retweets_of_me(api = None, count = 20):
    usage = "USAGE: get_retweets(api <a tweepy api object>, "
    usage += "count <number of tweets to retrieve>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.get_retweets_of_me, tweet_mode = "extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets

def get_mentions(api = None, count = 20):
    usage = "USAGE: get_mentions(api <a tweepy api object>, "
    usage += "count <number of tweets to retrieve>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.mentions_timeline, tweet_mode = "extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets

def get_user(api = None, user = None):
    usage = "USAGE: get_user(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    try:
        result = api.get_user(id = user, tweet_mode = "extended")
    except TweepError as e:
        print(e)
        return
    return result

def get_user_friends(api = None, user = "", count = 100):
    usage = "USAGE: get_user_friends(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.friends, id = user, tweet_mode = "extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users

def get_my_friends(api = None, count = 100):
    usage = "USAGE: get_my_friends(api <a tweepy api object>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.friends, tweet_mode = "extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users

def get_user_followers(api = None, user = "", count = 100):
    usage = "USAGE: get_user_followers(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.followers, id = user, tweet_mode = "extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users

def get_my_followers(api = None, count = 100):
    usage = "USAGE: get_my_followers(api <a tweepy api object>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.followers, tweet_mode = "extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users

def follow_user(api = None, user = ""):
    usage = "(USAGE: follow_user(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    try:
        result = api.create_friendship(id = user)
    except TweepError as e:
        print(e)
        return
    return result

def unfollow_user(api = None, user = ""):
    usage = "(USAGE: unfollow_user(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    try:
        result = api.destroy_friendship(id = user)
    except TweepError as e:
        print(e)
        return
    return result

def search(api = None, query = "", count = 20):
    usage = "USAGE: search_users(api <a tweepy api object>, query <a string query>, "
    usage += "count <number of users to return>"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if query == "":
        print("ERROR: You must pass a string as a query to search on.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.search, q = query, tweet_mode = "extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets

def search_users(api = None, query = "", count = 20):
    usage = "USAGE: search_users(api <a tweepy api object>, query <a string query>, "
    usage += "count <number of users to return>"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if query == "":
        print("ERROR: You must pass a string as a query to search on.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    users = []
    try:
        for user in tweepy.Cursor(api.search_users, q = query, tweet_mode = "extended").items(count):
            users.append(user)
    except TweepError as e:
        print(e)
        return
    return users
