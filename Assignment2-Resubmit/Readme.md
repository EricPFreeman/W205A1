I fixed these two items:
A. No set of tweets organization on S3-tweets texts not extracted properly  (texts are overwritten and no tweet’s text chunking ) 
B. No partition of raw tweets (Jsons)  

CountTweets.py is my python script to pull tweets. It looks for a file called maxid in my S3 repository to determine the id of the last tweet it pulled when it last ran and uses that to continue pulling tweets.The JSON file is stored in S3. The script should be run multiple times to collect all the tweets for that period. I could have written another script that called this script until the max_id does not change. Instead I just ran the script manually a number of times.
