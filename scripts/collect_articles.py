import requests
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# ----------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------

# Load your API key securely from the .env file
load_dotenv()
API_KEY = os.getenv("NEWSAPI_KEY")

# The players you want to search for
PLAYERS = ["LeBron James", "Stephen Curry"]

# NewsAPI free tier only reliably goes back ~30 days,
# but we set this anyway for when you upgrade to a paid plan
FROM_DATE = "2026-03-01"
TO_DATE = datetime.today().strftime("%Y-%m-%d")  # today's date automatically

# How many articles to fetch per player (max 100 per request on free tier)
PAGE_SIZE = 100

# Where to save your data
OUTPUT_FILE = "data/raw/newsapi/nba_articles.csv"

# ----------------------------------------------------------------
# COLLECTOR FUNCTION
# ----------------------------------------------------------------

def fetch_articles(player_name):
    """
    Fetches articles mentioning a player from NewsAPI.
    Returns a list of article dictionaries.
    """

    print(f"\nFetching articles for: {player_name}...")

    # Build the API request URL
    url = "https://newsapi.org/v2/everything"

    # These are the parameters we send to the API
    params = {
        "q": f'"{player_name}"',       # exact phrase search (quotes matter)
        "from": FROM_DATE,
        "to": TO_DATE,
        "language": "en",              # English articles only
        "sortBy": "relevancy",         # most relevant first
        "pageSize": PAGE_SIZE,
        "apiKey": API_KEY
    }

    # Make the request
    response = requests.get(url, params=params)

    # Check if the request succeeded
    if response.status_code != 200:
        print(f"  ERROR: {response.status_code} - {response.json().get('message')}")
        return []

    data = response.json()
    articles = data.get("articles", [])
    print(f"  Found {len(articles)} articles.")

    # Parse each article into a clean dictionary
    parsed = []
    for article in articles:
        parsed.append({
            "player":    player_name,
            "date":      article.get("publishedAt", "")[:10],  # keep only YYYY-MM-DD
            "outlet":    article.get("source", {}).get("name", "Unknown"),
            "headline":  article.get("title", ""),
            "body":      article.get("content", ""),            # NOTE: truncated to ~200 chars on free tier
            "url":       article.get("url", "")
        })

    return parsed

# ----------------------------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------------------------

def main():

    all_articles = []

    for player in PLAYERS:
        articles = fetch_articles(player)
        all_articles.extend(articles)

        # Wait 1 second between requests to be polite to the API
        time.sleep(1)

    # Convert to a pandas DataFrame
    df = pd.DataFrame(all_articles)

    # If nothing came back, exit gracefully
    if df.empty:
        print("\nNo articles were returned. Check your API key or date range.")
        return

    # Drop any rows where both headline and body are empty
    df = df.dropna(subset=["headline", "body"], how="all")

    # Remove duplicate articles (same URL appearing twice)
    df = df.drop_duplicates(subset=["url"])

    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"\nDone! Saved {len(df)} articles to '{OUTPUT_FILE}'")
    print(df[["player", "date", "outlet", "headline"]].head(10))
if __name__ == "__main__":
    main()