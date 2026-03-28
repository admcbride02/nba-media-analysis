import pandas as pd
import re
import os

# Config
INPUT_FILE  = "data/raw/newsapi/nba_articles.csv"
OUTPUT_FILE = "data/cleaned/nba_articles_cleaned.csv"

# Cleaning F-n
def clean_body_text(text):
    """
    Cleans up the article body text.
    NewsAPI truncates content and leaves artifacts we want to remove.
    """
    if not isinstance(text, str):
        return ""

    # Remove NewsAPI truncation "... [+1234 chars]"
    text = re.sub(r'\[\+\d+ chars\]', '', text)

    # Remove HTML tags <p>, <strong>
    text = re.sub(r'<[^>]+>', '', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def clean_headline(text):
    if not isinstance(text, str):
        return ""
    # Remove HTML entities
    text = re.sub(r'&\w+;', '', text)
    # Remove whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Era labels
def assign_era(date_str):
    try:
        year = int(date_str[:4])
        return "pre_2009" if year < 2009 else "post_2009"
    except (ValueError, TypeError):
        return "unknown"

# Outlet names
def standardize_outlet(outlet):
    if not isinstance(outlet, str):
        return "Unknown"

    outlet = outlet.strip()

    # Map variations to a standard name
    outlet_map = {
        "ESPN.com":         "ESPN",
        "BBC News":         "BBC",
        "BBC Sport":        "BBC",
        "Al Jazeera":       "Al Jazeera",
        "Al Jazeera English": "Al Jazeera",
    }

    return outlet_map.get(outlet, outlet)

# Main f-n
def main():
    # Load CSV
    print(f"Loading raw data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    print(f"  Loaded {len(df)} articles.")

    # Apply cleaning f-n
    print("Cleaning data...")
    df["headline"] = df["headline"].apply(clean_headline)
    df["body"]     = df["body"].apply(clean_body_text)
    df["outlet"]   = df["outlet"].apply(standardize_outlet)

    # Add era column
    df["era"] = df["date"].apply(assign_era)

    # Drop rows w/ no headline
    before = len(df)
    df = df[df["headline"].str.len() > 0]
    print(f"  Dropped {before - len(df)} rows with empty headlines.")

    # Reorder cols
    df = df[["player", "era", "date", "outlet", "headline", "body", "url"]]

    # Sort by player and date
    df = df.sort_values(["player", "date"]).reset_index(drop=True)

    # Save to cleaned folder
    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"\nDone! Saved {len(df)} cleaned articles to '{OUTPUT_FILE}'")
    print("\nEra breakdown:")
    print(df.groupby(["player", "era"]).size().to_string())
    print("\nOutlet breakdown:")
    print(df.groupby("outlet").size().sort_values(ascending=False).head(10).to_string())

if __name__ == "__main__":
    main()