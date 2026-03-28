import re
import pandas as pd
import os
from datetime import datetime

# Config
INPUT_FILES = {
    "Michael Jordan": "data/raw/nexis/jordan_nexis.RTF",
    "Kobe Bryant": "data/raw/nexis/kobe_nexis.RTF",
    "Lebron James": "data/raw/nexis/lebron_nexis.RTF",
    "Stephen Curry": "data/raw/nexis/curry_nexis.RTF",
}
OUTPUT_FILE = "data/cleaned/nexis_articles_cleaned.csv"

# RTF Cleaning
def strip_rtf(text):
    text = re.sub(r'\\[a-zA-Z]+\-?[0-9]*', ' ', text)
    text = re.sub(r'\\[\*~]', ' ', text)
    text = re.sub(r'[{}]', '', text)
    text = re.sub(r'[0-9a-f]{4}(?:[0-9a-f]{4})+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_date(date_str):
    match = re.search(
        r'(January|February|March|April|May|June|July|August|'
        r'September|October|November|December)\s+\d{1,2},\s+\d{4}',
        date_str
    )
    if match:
        try:
            return datetime.strptime(match.group(), "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            return ""
    return ""

def assign_era(date_str):
    try:
        year = int(date_str[:4])
        return "pre_2009" if year < 2009 else "post_2009"
    except (ValueError, TypeError):
        return "unknown"
    
def parse_articles(player_name, filepath):
    print(f"\nParsing: {filepath}")
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    
    copyright_matches = list(re.finditer(r'Copyright\s+\d{4}', raw))
    print(f"Found {len(copyright_matches)} articles")
    
    articles = []
    for i, match in enumerate(copyright_matches):
        header_start = max(0, match.start() - 3000)
        header = raw[header_start:match.start()]
        body_start = match.end()
        body_end = copyright_matches[i + 1].start() if i + 1 < len(copyright_matches) else len(raw)
        body_raw = raw[body_start:body_end]
        headline = ""
        headline_match = re.search(
            r'\\fldrslt\{[^}]*?([A-Z][A-Z\s\'\-\:,]{8,})\}',
            header
        )
        if headline_match:
            headline = headline_match.group(1).strip()
    
        outlet = ""
        date = ""
        date_match = re.search(
            r'(January|February|March|April|May|June|July|August|'
            r'September|October|November|December)\s+\d{1,2},\s+\d{4}',
            header
        )
        if date_match:
            date = parse_date(date_match.group())
        if date_match:
            pre_date = header[:date_match.start()]
            outlet_match = re.search(
                r'\\cf1\s+([^\\{}\n\r]+?)\s*\}?\s*$',
                pre_date
            )
            if outlet_match:
                outlet = outlet_match.group(1).strip()
                outlet = re.sub(r'[\\~\*]', '', outlet).strip()
        if not date:
            continue
        try:
            year = int(date[:4])
            if year < 1980 or year > 2026:
                continue
        except ValueError:
            continue
        
        body = strip_rtf(body_raw)
        body = re.sub(
            r'^.{0,300}?(Body Body Body|Body_\d+ Body_\d+ Body)','', body
        ).strip()
        body = re.sub(r'\s+', ' ', body)
        body = body[:5000]
        
        if len(body) < 100:
            continue
        
        articles.append({
            "player": player_name,
            "era": assign_era(date),
            "date": date,
            "outlet": outlet,
            "headline": headline,
            "body": body,
            "url": ""
        })
        
    print(f"Parsed {len(articles)} valid articles.")
    return articles


# Main
def main():
    all_articles = []
    for player, filepath in INPUT_FILES.items():
        if not os.path.exists(filepath):
            print(f"WARNING: File not found - {filepath}")
            continue
        
        articles = parse_articles(player, filepath)
        all_articles.extend(articles)
    
    df = pd.DataFrame(all_articles)
    if df.empty:
        print("\nNo articles parsed. Check your RTF files.")
        return
    
    df = df[["player", "era", "date", "outlet", "headline", "body", "url"]]
    df = df.sort_values(["player", "date"]).reset_index(drop=True)

    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    
    print(f"\nDone! Saved {len(df)} articles to '{OUTPUT_FILE}'")
    print("\nEra breakdown:")
    print(df.groupby(["player", "era"]).size().to_string())
    print("\nSample headlines:")
    print(df[["player", "date", "outlet", "headline"]].head(10).to_string())

if __name__ == "__main__":
    main()