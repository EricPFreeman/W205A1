import sys
import tweepy
import datetime
import urllib
import signal

import json

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

myKey.key = 'twitter/Data/' + str(maxid)
#q = urllib.quote_plus(sys.argv[1])  # URL encoded query
#hardcoding for now.
q="minecraft OR microsoft"
# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"

text=""
for tweet in tweepy.Cursor(api.search,q=q,
                   since="2015-02-08",
                   until="2015-02-15",
                   lang="en", since_id=maxid).items(1000):
# FYI: JSON is in tweet._json
# print tweet.created_at,tweet._json
    text = text + ' ' + str([unicode(tweet.text).encode("utf-8")])
    if (int(tweet.id)>maxid):
        maxid=tweet.id

myKey.set_contents_from_string(text)
myKey.key = 'twitter/maxid'
myKey.set_contents_from_string(str(maxid+1))



class TweetSerializer:
   out = None
   first = True
   count = 0
   def start(self):
      count += 1
      fname = "tweets-"+str(count)+".json"
      self.out = open(fname,"w")
      self.out.write("[\n")
      self.first = True

   def end(self):
      if self.out is not None:
         self.out.write("\n]\n")
         self.out.close()
      self.out = None

   def write(self,tweet):
      if not self.first:
         self.out.write(",\n")
      self.first = False
      self.out.write(json.dumps(tweet._json).encode('utf8'))

def interrupt(signum, frame):
   print "Interrupted, closing ..."
   # magic goes here
   exit(1)

signal.signal(signal.SIGINT, interrupt)