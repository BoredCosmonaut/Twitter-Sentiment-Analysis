import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


# Generic Twitter Class for sentiment analysis.
class TwitterClient(object):

    # Using the API and constructing a class
    def __init__(self):

        # consumer keys and acces tokens
        consumer_key = ""
        consumer_secret = ""
        acces_token = ""
        acces_token_secret = ""

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(acces_token, acces_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error!! Authencitaction Failed")

    # Cleans the tweets (links,special characters etc.) using a regex
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())

    # function to classify sentiment of passed tweet using textblob's sentiment method
    def get_tweet_sentiment(self, tweet):
        # creates TextBlob object of passed tweet text
        analysis = TextBlob(self.cleanTweet(tweet))
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity == 0:
            return "Neutral"
        else:
            return "Negative"

    # function to fetch tweets and parse them.
    def get_tweets(self, query, count=10):
        # empty list to store parsed tweets
        tweets = []
        try:
            # calls the twiteer apı to get tweets
            fetched_tweets = self.api.search_tweets(q = query, count=count)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dic to store params of a tweet
                parsed_tweet = {}

                # saving text of a tweet
                parsed_tweet["text"] = tweet.text
                # saving sentiment of a tweet
                parsed_tweet["sentiment"] = self.get_tweet_sentiment(tweet.text)
                # adding parsed tweet to the tweets list
                if tweet.retweet_count > 0:
                    # if a tweet has any retweets it only appends once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            # returns tweets
            return tweets
        # returns error if any
        except tweepy.TweepyException as e:
            print("Error: ", str(e))


def main():
    # creating an object of TwitterClient Class
    api = TwitterClient()
    # fetching tweets
    tweets = api.get_tweets(query="funny", count=100)

    # picking positive tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'Negative']
    # percentage of negative tweets
    print('Negative tweets percentage: {} %'.format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))

    # printing first 10 positive tweets
    print("\nPositive Tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    # printing first 10 negative tweets
    print("\nNegative Tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    # calling main function
    main()
