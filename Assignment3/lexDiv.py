#!/usr/bin/env python
# this script calculates the lexical diversity of tweets in a mongoDB
 
import json
import nltk
import cPickle
import getopt
import sys
import urllib
import signal
import pymongo
import collections


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
    mycoll = db.my_tweets
    mycoll
except:
    print "error with collection:", sys.exc_info()[0]

   
words = collections.defaultdict(list)
lex_div = collections.defaultdict(float)

eps = db.my_tweets.find({},{'user':1,'text':1})
for item in eps:
   u = item['user'] 
   words[u['name']].append(item['text'].split())

for w in words:
    for y in words[w]:
        lex_div[w] = 1.0 * len(set(y)) / len(y)
            
try:
    mycollStats = db.lex_div
    mycollStats
except:
    print "error with collection:", sys.exc_info()[0] 

class Stats2Mongo:
   output = False
    
   def start(self,myColl):
      self.myColl = myColl

   def end(self):
      output = True
   
   def write(self,user,lex_div):
      if not self.myColl is None:
          self.myDoc = {"user": user, "lex_div": lex_div }        
          self.myColl.insert(self.myDoc)     
          
s = Stats2Mongo()
s.start(mycollStats)

for i in lex_div:
    s.write(i, lex_div[i])
s.end
 
        
print "Done!"
 
