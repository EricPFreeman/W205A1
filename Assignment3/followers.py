#!/usr/bin/env python
# this script finds the followers
import json
import nltk
import cPickle
import getopt
import sys
import urllib
import signal
import pymongo
import collections
import sys
import tweepy
import datetime
import time

print "start"

try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
   print "Connection failed : %s" % e 
conn                        
    
try:
    db = conn['db_streamT']
    db
except:
    print "error connecting with db:", sys.exc_info()[0]
    
    
try:
    mycoll = db.retweet_stats
    mycoll
except:
    print "error with collection:", sys.exc_info()[0]

   
follow_list = collections.defaultdict(list)
# Don't forget to install tweepy
# pip install tweepy

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
print "api"
eps = mycoll.find({},{'user':1,'followers':1}).sort('followers',1).limit(10)
print "for item"
for item in eps:
    u = item['user']
    print u
    try:
       for item in tweepy.Cursor(api.followers_ids,screen_name=u).pages(3): 
            follow_list[u].append(item)
            time.sleep(15)
    except tweepy.TweepError as e:
        print e
        pass
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
#users = api.lookup_users(user_ids=follow_list) 
            
try:
    mycollStats = db.followers
    mycollStats
except:
    print "error with collection:", sys.exc_info()[0] 
   
original_list = collections.defaultdict(list)
eps = mycoll.find({},{'user':1,'followers':1}).sort('followers',1).limit(10)
print "for item"
for item in eps:
    u = item['user']
    
s = Stats2Mongo()
s.start(mycollStats)

for i in follow_list:
    s.write(i, follow_list[i])
    print i
s.end
 
        
print "Done!"
   
  
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   if s is not None:
        if s.output == False and s.first == False:
           s.end()
   exit(1)

signal.signal(signal.SIGINT, interrupt)
