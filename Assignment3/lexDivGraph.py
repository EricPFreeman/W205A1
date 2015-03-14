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
import numpy as np
import matplotlib.pyplot as plt

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
    mycoll = db.lex_div
    mycoll
except:
    print "error with collection:", sys.exc_info()[0]

   
lex_div = []

eps = mycoll.find({},{'lex_div':1})
for item in eps:
   lex_div.append(item['lex_div'])  

plt.hist(lex_div, bins=10)
plt.show()

print "Done!"
 
