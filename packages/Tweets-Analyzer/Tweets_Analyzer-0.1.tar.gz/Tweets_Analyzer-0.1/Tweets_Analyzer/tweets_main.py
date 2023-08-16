import argparse
import os
import tweepy
from textblob import TextBlob

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Analyze Twitter sentiments")

# Add arguments for the API keys and tokens
parser.add_argument("--api_key", required=True, help="Twitter API key")
parser.add_argument("--api_secret", required=True, help="Twitter API secret key")
parser.add_argument("--access_token", required=True, help="Twitter access token")
parser.add_argument("--access_token_secret", required=True, help="Twitter access token secret")

# Parse the command-line arguments
args = parser.parse_args()

# Get the values from the arguments
api_key = args.api_key
api_secret = args.api_secret
access_token = args.access_token
access_token_secret = args.access_token_secret

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

    # Create a dictionary with the results
    results_dict = {
        "Number of positive tweets": results["positive"],
        "Number of negative tweets": results["negative"],
        "Number of neutral tweets": results["neutral"]
    }

    # Return the dictionary
    return results_dict

if __name__ == "__main__":
    main()
