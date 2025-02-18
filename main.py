# Reddit Sentiment Analysis Bot
# This script is intended to fetch comments from a subreddit post 
# using PRAW and prepares them for sentiment analysis using an LLM.
# Author: Obeida Iqbal

import praw


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
    return 0

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
    print(comments)

if __name__ == "__main__":
    main()