#!/usr/bin/env python
# this loads a list of followers from
# two tables and finds who has unfollowed
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
    mycoll = db.followers
    mycoll
except:
    print "error with collection:", sys.exc_info()[0]

try:
    mycoll2 = db.followers_today
    mycoll2
except:
    print "error with collection:", sys.exc_info()[0]   
   
follow_list = collections.defaultdict(list)
follow_list2 = collections.defaultdict(list)
follow_lost = collections.defaultdict(list)

eps = mycoll.find({},{'user':1,'followers':1})
for item in eps:
    u = item['user']
    for f in item['followers']:
        follow_list[u].append(f)
       
eps = mycoll2.find({},{'user':1,'followers':1})
for item in eps:
    u = item['user']
    for f in item['followers']:
        follow_list2[u].append(f)  
    
    
for f in follow_list:
    s1 = follow_list[f]
    s2 = follow_list2[f]
    follow_lost[f] = list(set(s1[0]) -set(s2[0]))


            
try:
    mycollStats = db.followers_lost
    mycollStats
except:
    print "error with collection:", sys.exc_info()[0] 

class Stats2Mongo:
   output = False
    
   def start(self,myColl):
      self.myColl = myColl

   def end(self):
      output = True
   
   def write(self,user,followers):
      if not self.myColl is None:
          self.myDoc = {"user": user, "followers": followers}        
          self.myColl.insert(self.myDoc)     
          
s = Stats2Mongo()
s.start(mycollStats)

for i in follow_lost:
    s.write(i, follow_lost[i])
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
