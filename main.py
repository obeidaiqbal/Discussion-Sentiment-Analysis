# Reddit Sentiment Analysis Bot
# This script is intended to fetch comments from a subreddit post 
# using PRAW and prepares them for sentiment analysis using an LLM.
# Author: Obeida Iqbal

import praw


def read_file(filename):
    file = open(filename, "r")
    return file.read()

reddit = praw.Reddit(
    client_id = read_file("clientid.txt"), 
    client_secret = read_file("secret.txt"), 
    user_agent = "DiscussionSentimentAnalysis/0.1 by chikachika-boomboom" 
)
print(reddit.read_only)
print("Hello, world!")