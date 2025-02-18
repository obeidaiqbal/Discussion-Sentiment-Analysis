## Subreddit Discussion Sentiment Analysis
This program analyzes the sentiment of discussions on Reddit, specifically targeting new chapter discussion posts in the One Piece subreddit. It uses PRAW (Python Reddit API Wrapper) to fetch comments from discussion threads and processes them for sentiment analysis using an LLM (Large Language Model). The goal is to determine the overall sentiment of reactions to new chapters by leveraging AI-powered text analysis.

Pushing: 
  ```sh
  git add .
  git commit -m "comment"
  git push origin main
  ```
Pulling:
  ```sh
  git pull origin main
  ```
To Run the main.py flask instance locally:
1. Activate the virtual enviornment & run main.py
  ```sh
  source venv/bin/Activate
  cd backend
  python3 main.py
  ```