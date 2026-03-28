import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Config
INPUT_FILE  = "data/corpus/nba_corpus.csv"
OUTPUT_FILE = "outputs/sentiment_analysis.csv"

# Main
def main():
    df = pd.read_csv(INPUT_FILE)
    print(f"  Loaded {len(df)} articles.")

    analyzer = SentimentIntensityAnalyzer()

    df["full_text"] = df["headline"].fillna("") + " " + df["body"].fillna("")
    df["sentiment_compound"] = df["full_text"].apply(lambda text: analyzer.polarity_scores(text)["compound"])
    df["sentiment_positive"] = df["full_text"].apply(lambda text: analyzer.polarity_scores(text)["pos"])
    df["sentiment_negative"] = df["full_text"].apply(lambda text: analyzer.polarity_scores(text)["neg"])
    df["sentiment_neutral"] = df["full_text"].apply(lambda text: analyzer.polarity_scores(text)["neu"])
    
    def classify_sentiment(compound):
        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"
        
    df["sentiment_label"] = df["sentiment_compound"].apply(classify_sentiment)
    print("\nMean compound sentiment score by player and era:")
    summary = df.groupby(["player", "era"])["sentiment_compound"].mean().round(3)
    print(summary.to_string())

    print("\nSentiment label breakdown by player:")
    breakdown = df.groupby(["player", "sentiment_label"]).size().unstack(fill_value=0)
    print(breakdown.to_string())
    
    os.makedirs("outputs", exist_ok=True)
    df.drop(columns=["full_text"]).to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\nSaved sentiment results to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()