import sys
import tweepy
import datetime
import urllib
import signal
import json
import pymongo

class Tweet2Mongo:
   output = False
    
   def start(self,myColl):
      self.myColl = myColl

   def end(self):
      output = True
   
   def write(self,tweetText):
      if not self.myColl is None:
          self.myDoc = {"tweet": tweetText}          
          self.myColl.insert(self.myDoc)
                        


try:
    conn=pymongo.MongoClient()
    print "Connected!"
except pymongo.errors.ConnectionFailure, e:
   print "Connection failed : %s" % e 
conn                        
    
try:
    db = conn['db_tweets']
    db
except:
    print "error connecting with db:", sys.exc_info()[0]
    
    
try:
    mycoll = db.my_tweets
    mycoll
except:
    print "error with collection:", sys.exc_info()[0]
# Don't forget to install tweepy
# pip install tweepy

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

maxid=1
if maxid=="":
    maxid=1
else:
    maxid = int(maxid)

#q = urllib.quote_plus(sys.argv[1])  # URL encoded query
#hardcoding for now.
q="minecraft OR microsoft"
# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"    
try:
    ts = Tweet2Mongo()
    ts.start(mycoll)
    print "start"
    for tweet in tweepy.Cursor(api.search,q=q,
                       since="2015-03-05",
                       until="2015-03-07",
                       lang="en", since_id=maxid-10000).items(10000):
    # FYI: JSON is in tweet._json
        ts.write(str([unicode(tweet.text).encode("utf-8")]))
        #print tweet.text
        if (int(tweet.id)>maxid):
            maxid=tweet.id
            print maxid

    ts.end()
    print "end"
except TweepError, e:
	print 'failed because of %s' % e.reason
    pass 
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise



      
                    
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   if ts is not None:
        if ts.output == False and ts.first == False:
           ts.end()
   exit(1)

signal.signal(signal.SIGINT, interrupt)
