# Reddit Sentiment Analysis Bot
# This script is intended to fetch comments from a subreddit post 
# using PRAW and prepares them for sentiment analysis using an LLM.
# Author: Obeida Iqbal

from transformers import pipeline, AutoConfig
import praw
import json

sentiment_model = pipeline("sentiment-analysis", model = "akshataupadhye/finetuning-sentiment-model-reddit-data")
totalConfidence = 0


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

def get_sentiment(sentiment):
    """Returns what each label is equivalent to"""
    if sentiment == 'LABEL_0':
        return "negative"
    elif sentiment == 'LABEL_1':
        return "neutral"
    elif sentiment == 'LABEL_2':
        return "positive"

def analyze_comments(comments, results):
    """Analyzes the sentiment of each comment"""
    global totalConfidence
    for i, comment in enumerate(comments, 1):
        sentiment, confidence = analyze_sentiment(comment)
        # print(f"Comment {i}: \n{comment}")
        # print(f"Sentiment: {get_sentiment(sentiment)} (Confidence: {confidence})\n")
        totalConfidence += confidence
        results[get_sentiment(sentiment)] += 1

def print_results(results, comment_count):
    """Prints the collected results of the analysis"""
    print("Sentiment")
    for sentiment in results:
        print(f"{sentiment}: {(results[sentiment] / comment_count) * 100}%")
    print(f"Confidence: {(totalConfidence / comment_count) * 100}%")

def get_training_data(count):
    """Gets the top posts from the subreddit to be used for training"""
    reddit = praw.Reddit(
        client_id = read_file("clientid.txt"), 
        client_secret = read_file("secret.txt"), 
        user_agent = "DiscussionSentimentAnalysis/0.1 by u/chikachika-boomboom" 
    )
    subreddit = reddit.subreddit("OnePiece")
    hot_posts = subreddit.hot(limit = count)
    return hot_posts

def save_comments(post, filename = "comments.json"):
    """Saves comments from post to comments.json for training"""
    post.comment_sort = "top"
    post.comments.replace_more(limit = 0)
    data = []
    for comment in post.comments.list():
        data.append({"text": comment.body, "label": None})
    with open(filename, "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 4)
    print(f"Saved {len(data)} comments to `{filename}` for training.")

def main():
    """Main function"""
    instruction = input("Would you like to analyze or train the model(a/t)?: ")
    if instruction == "a":
        current = get_post()
        comment_count = 200
        comments = get_comments(current, comment_count)
        results = {"positive": 0, "neutral": 0, "negative": 0}
        analyze_comments(comments, results)
        print_results(results, comment_count)
    elif instruction == "t":
        count = int(input("How many posts would you like to use: "))
        hot_posts = get_training_data(count)
        for post in hot_posts:
            save_comments(post)
    else:
        print("Unkown input")

if __name__ == "__main__":
    main()