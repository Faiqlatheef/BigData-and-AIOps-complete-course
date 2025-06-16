import re
import tweepy
from tweepy import OAuthHandler, Client
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = "7KUKKdr9pVTdkluuHBZvAiP2I"
        consumer_secret = "LbS4erTpCfMoUcKnOQYl2Z9y0NZsVQANcUHt46TI7giauVWzvW"
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAHy%2FugEAAAAASuKZiULDBj65SEbXkqav6a8Fa7A%3DHjCzCYt5MoMdpUqgwG8cEqwtIqAskGFnWeOY56bUYFQXkiGnyo"

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # create tweepy Client object to fetch tweets
            self.api = Client(bearer_token=bearer_token)
        except tweepy.TweepyException as e:
            print("Error: Authentication Failed - " + str(e))

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_recent_tweets(query=query, max_results=count, tweet_fields=['text'])

            # parsing tweets one by one
            for tweet in fetched_tweets.data:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if 'retweeted_status' in tweet:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepyException as e:
            # print error (if any)
            print("Error : " + str(e))
            return []

def analyze_sentiments(keyword, no_of_tweets):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=keyword, count=no_of_tweets)

    if not tweets:
        print("No tweets found for the given keyword.")
        return

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    positive_percentage = 100 * len(ptweets) / len(tweets)
    print("Positive tweets percentage: {} %".format(positive_percentage))
    
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    negative_percentage = 100 * len(ntweets) / len(tweets)
    print("Negative tweets percentage: {} %".format(negative_percentage))
    
    # percentage of neutral tweets
    neutral_percentage = 100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)
    print("Neutral tweets percentage: {} %".format(neutral_percentage))

    # printing first 10 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 10 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    # Creating PieChart
    labels = [f'Positive [{positive_percentage:.2f}%]', f'Neutral [{neutral_percentage:.2f}%]', f'Negative [{negative_percentage:.2f}%]']
    sizes = [positive_percentage, neutral_percentage, negative_percentage]
    colors = ['yellowgreen', 'blue', 'red']
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=90, autopct='%1.1f%%')
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(10)
    plt.legend(patches, labels, loc="best")
    plt.title(f"Sentiment Analysis Result for keyword= {keyword}")
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    keyword = input("Please enter keyword or hashtag to search: ")
    no_of_tweets = int(input("Please enter how many tweets to analyze: "))
    analyze_sentiments(keyword, no_of_tweets)
