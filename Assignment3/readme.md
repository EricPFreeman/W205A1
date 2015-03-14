1.1 dbstream.py uses tweepyto write to db_streamT
1.2 dbtweets.py uses tweepy to write to mongodb called db_tweets
2.1 analyzeTweets.py uses a pipeline to find the top 30 tweets in db_tweets
Those 30 tweets are used to query dbStream for username, location, number of followers, and number of retweets. The results are stored in a collection called retweet_stats.
2.2 lexDiv.py computes the lexical diversity by pulling all user and texts from dbstreamT and creating a list of words for each user. Lexical diversity is calculated by len(set(w)/len(w). The number of unique words/number of words.
The results are stored in a collection named lex_div.
lexDivGraph.py creates a histogram which was saved to lexDiv.png
2.3 followers.py was run twice. The code was edited to output to different collections - followers and followers_today. A future improvement would be to pass in collection name.
unfollow.py pulls a list of users and followers from the 2 collections and subtracts the second set from the first to see who unfollowed the user. Currently, the code only identifies user by user_id. A future enhancement would be to show user_name of the people who stopped following.
3.1 dump.py runs mongodump, puts the results in a tar file and sends it E3.
restore.py does the reverse.
https://s3.amazonaws.com/midseric/mongodump_20150313182524.tgz
