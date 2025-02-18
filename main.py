# Reddit Sentiment Analysis Bot
# This script is intended to fetch comments from a subreddit post 
# using PRAW and prepares them for sentiment analysis using an LLM.
# Author: Obeida Iqbal

from transformers import pipeline
import praw

sentiment_model = pipeline("sentiment-analysis")


def analyze_sentiment(comment):
    """Uses a Hugging Face model to analyze sentiment of a comment"""
    result = sentiment_model(comment)[0] 
    return result["label"], round(result["score"], 2)

def read_file(filename):
    """Returns the contents of filename"""
    file = open(filename, "r")
    return file.read()

def get_post():
    """Returns the discussion post to be analyzed or 0"""
    reddit = praw.Reddit(
        client_id = read_file("clientid.txt"), 
        client_secret = read_file("secret.txt"), 
        user_agent = "DiscussionSentimentAnalysis/0.1 by u/chikachika-boomboom" 
    )
    subreddit = reddit.subreddit("OnePiece")
    hot_posts = subreddit.hot(limit = 5)
    for post in hot_posts:
        if "Discussion" in post.title:
            return post
    return None

def get_comments(post, num = 10):
    """Prints comments from the given post"""
    post.comment_sort = "top"
    post.comments.replace_more(limit = 0)
    comments = []
    for comment in post.comments.list()[:num]: 
        comments.append(comment.body)
    return comments

def main():
    """Main function"""
    current = get_post()
    comments = get_comments(current, 3)
    for i, comment in enumerate(comments, 1):
        sentiment, confidence = analyze_sentiment(comment)
        print(f"Comment {i}: \n{comment}")
        print(f"Sentiment: {sentiment} (Confidence: {confidence})\n")

if __name__ == "__main__":
    main()