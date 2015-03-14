import sys
import tweepy
import datetime
import urllib
import signal
import json
import pymongo
import collections


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

try:
    dbStream = conn['db_streamT']
    dbStream
except:
    print "error connecting with db:", sys.exc_info()[0]
    
    
try:
    mycollStream = dbStream.my_tweets
    mycollStream
except:
    print "error with collection:", sys.exc_info()[0]

    
pipelines = []
pipelines.append({ '$group': { '_id': '$text','count':{ '$sum': 1 }}})
pipelines.append({ '$sort': { 'count': -1 } })
pipelines.append({ '$limit': 30 })

user = collections.defaultdict(str)
location= collections.defaultdict(str)
followers= collections.defaultdict(int)
retweets= collections.defaultdict(int)


eps = dbStream.my_tweets.aggregate(pipelines)
for item in eps['result']:
    eps2= dbStream.my_tweets.find({'text': item['_id'] })
   
    for q in eps2:
        try:
            k = q['retweeted_status']
            l = k['user']
            #print l['name'] + "," + l['location']
            user[item['_id']]=l['name']
            location[item['_id']]=(l['location'])
            try:
                if followers[item['_id']]< l['followers_count']:
                    followers[item['_id']] = (l['followers_count'])
            except:
                followers[item['_id']] = l['followers_count']
            retweets[item['_id']] = retweets[item['_id']]+1
        except:
            pass
           #print "no retweet info"
            

            
            
try:
    mycollStats = dbStream.retweet_stats
    mycollStats
except:
    print "error with collection:", sys.exc_info()[0]            

class Stats2Mongo:
   output = False
    
   def start(self,myColl):
      self.myColl = myColl

   def end(self):
      output = True
   
   def write(self,tweetText,user,location,followers,retweets):
      if not self.myColl is None:
          self.myDoc = {"tweet": tweetText, "user": user, "location": location, "followers": followers, "retweets": retweets}          
          self.myColl.insert(self.myDoc)     
          
s = Stats2Mongo()
s.start(mycollStats)

for i in retweets:
    s.write(i, user[i], location[i], followers[i], retweets[i])
s.end

   
        
print "Done!"




      
        
