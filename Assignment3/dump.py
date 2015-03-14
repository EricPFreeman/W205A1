import time
import subprocess
import os
import shutil
import tarfile
import datetime
import urllib
import signal
import json

now=int(time.time())
cmd="mongodump"
print subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

#Create Tar file
tFile = tarfile.open("files.tar", 'w')

files = os.listdir("./dump")
for f in files:
    print f
   # tFile.add(f)

#List files in tar
for f in tFile.getnames():
    print "Added %s" % f

tFile.close()

#Send to S3
from boto.s3.connection import S3Connection
conn = S3Connection('', '')

myBucket = conn.get_bucket('midseric') 
from boto.s3.key import Key
myKey = Key(myBucket)
myKey.key = 'mongodb'
myKey.set_contents_from_filename('files.tar')
myKey.set_acl('public-read')
           
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)

signal.signal(signal.SIGINT, interrupt)


