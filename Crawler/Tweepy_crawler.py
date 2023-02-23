import time
import configparser
import pandas as pd
import os
import json
import tweepy

#read config 
config= configparser.ConfigParser()
config.read("config.ini")
Api_Key=config['twitter_api']['API_Key']
Api_Key_Secret=config['twitter_api']['API_Key_Secret']
Access_Token=config['twitter_api']['Access_Token']
Access_Token_Secret=config['twitter_api']['Access_Token_Secret']

auth=tweepy.OAuthHandler(Api_Key,Api_Key_Secret,Access_Token,Access_Token_Secret)
# auth.set_access_tokens(Access_Token,Access_Token_Secret)

api=tweepy.API(auth,wait_on_rate_limit=True)


num_tweets = 5000

# Define the number of requests to make
num_requests = int(num_tweets / 100)

container = []
ListOfKeywords=['Mario Draghi','Angela Merkel','Scott Morrison','Fumio Kishida','Pedro Sanchez','Emmanuel Macron','Jair Bolsonaro','Volodymyr Zelenskyy']
def func(myquery, myword):
    print("DEBUG:func:: myquery ",myquery)
    # Open the file to save the tweets
    filename = "tweets_" + myword.replace(" ", "-")
    try:
        with open(filename, 'w') as f:
            # Collect tweets using tweepy Cursor
            for i in range(num_requests):
                print("DEBUG:func:: request number ",i+1)
                tweets = tweepy.Cursor(api.search_tweets, q=myquery, tweet_mode="extended").items(100)
                for tweet in tweets:
                    # Write each tweet to the file as a separate line
                    f.write(json.dumps(tweet._json) + '\n')
    except Exception as e:
        print("DEBUG:func:: some Exception", e, "\n")
        print("DEBUG:func:: INCOMPLETE EXECUTION QUERY ", myquery)
        print("DEBUG:****Sleeping for 15 mins****")
        time.sleep(910)

for word in ListOfKeywords:
    query = word + " exclude:retweets" + " exclude:replies"
    print(" ******* DEBUG: query ",query, "******* \n")
    func(query, word)
    print(" ******* DEBUG: query complete",query,"*******  \n")