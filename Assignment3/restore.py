import time
import subprocess
import os
import shutil
import tarfile
import sys
import datetime
import urllib
import signal
import json


#get tar file

from boto.s3.connection import S3Connection
conn = S3Connection('', '')

myBucket = conn.get_bucket('midseric') 
from boto.s3.key import Key
myKey = Key(myBucket)
myKey.get_key(mongodb)
myKey.get_contents_to_filename('/files.tar')

#extract tar file 
tar = tarfile.open("files.tar")
tar.extractall()
tar.close()
print "Extracted in Current Directory"

now=int(time.time())

cmd="mongorestore"
print subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
              
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)

signal.signal(signal.SIGINT, interrupt)
