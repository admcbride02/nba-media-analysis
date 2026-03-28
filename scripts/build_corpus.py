import pandas as pd
import os

# Config
INPUT_FILE = "data/cleaned/nexis_articles_cleaned.csv"
OUTPUT_FILE = "data/corpus/nba_corpus.csv"

# Main
def main():
    print("Loading Nexis cleaned data...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} articles.")
    
    before = len(df)
    df = df[df["body"].str.strip().str.len() > 100]
    print(f"Dropped {before -len(df)} rows with invalid dates.")
    
    before = len(df)
    df = df[df["era"].isin(["pre_2009", "post_2009"])]
    print(f"Dropped {before - len(df)} rows with unknown era.")
    
    df["player"] = df["player"].replace("Lebron James", "LeBron James")
    
    df = df.reset_index(drop=True)

# Summarise
    print(f"\nFinal corpus: {len(df)} articles")
    print("\nBreakdown by player and era:")
    print(df.groupby(["player", "era"]).size().to_string())
    print("\nDate ranges per player:")
    for player, group in df.groupby("player"):
        print(f"{player}: {group['date'].min()} to {group['date'].max()}")
        
    os.makedirs("data/corpus", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\nSaved master corpus to '{OUTPUT_FILE}'")
    
if __name__ == "__main__":
    main()