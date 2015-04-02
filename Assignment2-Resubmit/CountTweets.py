import sys
import tweepy
import datetime
import urllib
import signal

import json

class TweetSerializer:
   output = False
   first = True
   text=""
   def start(self,myKey):
      self.text = "[\n"
      self.first = True
      self.myKey = myKey

   def updatemax(self, maxid):
      self.myKey.key = 'twitter/maxid'
      self.myKey.set_contents_from_string(str(maxid+1))

   def end(self):
      self.text = self.text + "\n]\n"
      self.myKey.set_contents_from_string(str(ts.text))
      output = True
   
   def write(self,tjson):
      if not self.first:
         self.text + ",\n"
      self.first = False
      self.text = self.text + tjson
                        
# Don't forget to install tweepy
# pip install tweepy

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

from boto.s3.connection import S3Connection
conn = S3Connection('', '')

myBucket = conn.get_bucket('midseric') 
from boto.s3.key import Key
myKey = Key(myBucket)
myKey.key = 'twitter/maxid'
maxid = myKey.get_contents_as_string()
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
myKey.key = 'twitter/Data/' + str(maxid) + ".json"        
try:
    ts = TweetSerializer()
    ts.start(myKey)
    print "start"
    for tweet in tweepy.Cursor(api.search,q=q,
                       since="2015-03-15",
                       until="2015-04-02",
                       lang="en", since_id=maxid).items(10000):
    # FYI: JSON is in tweet._json
        ts.write(str(json.dumps(tweet._json).encode('utf8')))
        #print tweet.text
        if (int(tweet.id)>maxid):
            maxid=tweet.id
            print maxid

    ts.end()
    ts.updatemax(maxid)
    print ts.text
    print "end"
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise



      
                    
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   if ts is not None:
        if ts.output == False and ts.first == False:
           myKey.set_contents_from_string(ts.text)
        myKey.key = 'twitter/maxid'
        myKey.set_contents_from_string(str(maxid+1))
   exit(1)

signal.signal(signal.SIGINT, interrupt)




