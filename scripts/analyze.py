import pandas as pd
import re
import os

# Config
INPUT_FILE = "data/corpus/nba_corpus.csv"
OUTPUT_FILE = "outputs/lexical_analysis.csv"

# Define Lexical Fields for Sentiment Analysis
LEXICAL_FIELDS = {
    "gameplay": [
        "points", "rebounds", "assists", "defense", "offense", "clutch",
        "triple-double", "shot", "dunk", "layup", "block", "steal",
        "turnover", "foul", "quarter", "halftime", "overtime", "playoff",
        "championship", "finals", "mvp", "scoring", "basket", "dribble",
        "pass", "court", "win", "loss", "season", "stats", "performance",
        "highlight", "teammate", "coach", "game"
    ],
    "money_brand": [
        "contract", "extension", "deal", "salary", "max", "endorsement",
        "brand", "sponsorship", "money", "million", "billion", "agent",
        "negotiate", "free agency", "market", "revenue", "invest",
        "business", "owner", "franchise", "nike", "adidas", "commercial",
        "partner", "wealth", "net worth", "shoe", "apparel",
        "media rights", "trade"
    ],
    "personal_drama": [
        "family", "charity", "feud", "controversy", "scandal", "tweet",
        "instagram", "social media", "wife", "child", "father", "mother",
        "foundation", "community", "arrest", "legal", "retirement",
        "interview", "podcast", "political", "activism", "protest",
        "vacation", "lifestyle", "celebrity", "fame", "image", "persona"
    ]
}

def count_lexical_hits(text, word_list):
    if not isinstance(text, str):
        return 0
    
    text = text.lower()
    count = 0
    
    for word in word_list:
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = re.findall(pattern, text)
        count += len(matches)
    return count

def count_words(text):
    if not isinstance(text, str):
        return 1
    words = text.split()
    return max(len(words), 1)

# Main
def main():
    print("Loading corpus...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} articles.")
    df["full_text"] = df["headline"].fillna("") + " " + df["body"].fillna("")
    
    for field, word_list in LEXICAL_FIELDS.items():
        df[f"{field}_hits"] = df["full_text"].apply(
            lambda text: count_lexical_hits(text, word_list)
        )
    
    df["word_count"] = df["full_text"].apply(count_words)
    
    for field in LEXICAL_FIELDS.keys():
        df[f"{field}_per1000"] = (
            df[f"{field}_hits"] / df["word_count"] * 1000
        ).round(4)
        
    print("\nMean lexical field scores per 1000 words by player and era:")
    summary = df.groupby(["player", "era"])[[
        "gameplay_per1000",
        "money_brand_per1000",
        "personal_drama_per1000"
    ]].mean().round(3)
    print(summary.to_string())
    os.makedirs("outputs", exist_ok=True)
    df.drop(columns=["full_text"]).to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\nSaved full results to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()