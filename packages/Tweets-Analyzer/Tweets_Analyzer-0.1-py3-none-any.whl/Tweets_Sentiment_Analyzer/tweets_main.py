import os
import tweepy
from dotenv import load_dotenv
from textblob import TextBlob

# Load the stored environment variables
load_dotenv()

# Get the values
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

class TwitterSentimentAnalyzer:
    def __init__(self):
        # Authenticate with the Tweepy API
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def analyze(self, query):
        # Search for tweets about any product
        tweets = tweepy.Cursor(
            self.api.search_tweets,
            q=query,
            count=100,
        ).items()

        # Count the number of positive, negative, and neutral tweets
        sentiments = map(lambda tweet: TextBlob(tweet.text).sentiment.polarity, tweets)
        positive_count = sum(map(lambda sentiment: sentiment > 0, sentiments))
        negative_count = sum(map(lambda sentiment: sentiment < 0, sentiments))
        neutral_count = sum(map(lambda sentiment: sentiment == 0, sentiments))

        # Return the results
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        }

def main():
    analyzer = TwitterSentimentAnalyzer()
    results = analyzer.analyze("product name")

    # Print the results
    print("Number of positive tweets:", results["positive"])
    print("Number of negative tweets:", results["negative"])
    print("Number of neutral tweets:", results["neutral"])

if __name__ == "__main__":
    main()
