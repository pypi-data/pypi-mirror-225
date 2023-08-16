from setuptools import setup, find_packages

setup(
    name="Tweets_Analyzer",
    version="0.1",
    description="A Python package for analyzing the sentiment of tweets.",
    author="Aleksandr",
    author_email="novacyan545@gmail.com",
    url="https://github.com/Aleksandr-Chelyshkin/Tweets_Sentiment_Analyzer.git",
    packages=find_packages(),
    install_requires=["tweepy", "textblob"],
)
