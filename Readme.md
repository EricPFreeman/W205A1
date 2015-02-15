CountTweets.py is my python script to pull tweets. It looks for a file called maxid in my S3 repository to determine the id of the last tweet it pulled when it last ran and uses that to continue pulling tweets.The text of the tweets is stored in S3. I only stored the text because that was what was going to be used for the histogram.

Twitter Histogram.png is a histogram of word frequency. Most words occurred less than 16 times. Interestingly, 10 words appeared between 750 and 779 times.

I used three S3 repositories. midseric/twitter holds the maxid file. midseric/twitter/Data holds the raw tweets. midseric/twitter2 hold the results of my wordcount script.

