# NBA Media Coverage Analysis

_A computational linguistics study of sports media narratives across the social media divide._

## Overview

This project investigates how sports media coverage of NBA stars has evolved across the social media era. Using a corpus of nearly 1800 articles sourced from Nexis Uni spanning four decades of professional basketball, I apply NLP techniques to measure shifts in the language used to describe elite NBA players during their active careers.

## Research Question

Has the narrative focus of sports media coverage of NBA stars shifted from gameplay and on-court performance toward financial, branding, and personal storytelling in the social media era (post-2009)?

To investigate this, I compare coverage of four players whose active careers fall cleanly on either side of, or across, the social media divide:
| **Player** | **Career** | **Era** |
| --- | --- | --- |
| Michael Jordan | 1984-2003 | Pre-social media |
| Kobe Bryant | 1996-2016 | Spans both eras |
| LeBron James | 2003-2024 | Spans both era |
| Stephen Curry | 2009-2024 | Post-social media |

Jordan and Curry serve as clean single-era controls, while Kobe and Lebron, whose careers span the 2009 divide, allow for a comparison of how coverage of the same athelete shifted as social media became more dominant. Analysis is restricted to each player's active playing career to isolate sports media narratives from retirement-era legacy coverage (Jordan, Kobe) and pre-career hype (LeBron).

## Methods

**Data Collection:** ~600 newspaper articles per player sourced from Nexis Uni, stratified across each player's active career in three time periods.

**Lexical Field Analysis:** Three custom lexical dictionaries measure the frequency of gameplay, financial/branding, and personal/drama terminology per article, normalized per 1,000 words to account for article length variation.

**Sentiment Analysis:** VADER (Valence Aware Dictionary and sEntiment Reasoner) applied to each article to measure the tone of coverage across players and eras.

**LLM Classification:** Claude API used to semantically classify each article's primary narrative focus, providing a validation layer on top of keyword-based lexical analysis.

**Statistical Testing:** Chi-square significance testing applied to lexical category distributions to determine whether observed shifts are statistically significant rather than incidental.

## Tools & Technologies

- **Python** - pandas, re, VADER, scikit-learn
- **Anthropic Claude API** - LLM-based article classification
- **Nexis Uni** - newspaper archive data source
- **NewsAPI** - modern article collection (pipeline built, excluded from final analysis to maintain sample size balance across eras)
- **Git/GitHub** - version control + reproducibility

## Project Status

Data collection in progress, expanding corpus to ~600 articles per player stratified across active career periods. Analysis pipeline complete and validated on initial 776-article corpus.

## Repository Structure

```
nba_media_analysis/
├── data/
│   ├── raw/nexis/          # Raw RTF exports from Nexis Uni
│   ├── cleaned/            # Parsed and normalized article data
│   └── corpus/             # Master analysis dataset
├── scripts/
│   ├── parse_nexis.py      # RTF parser for Nexis exports
│   ├── build_corpus.py     # Corpus assembly and quality checks
│   ├── analyze.py          # Lexical field frequency analysis
│   ├── sentiment.py        # VADER sentiment scoring
│   ├── classify_llm.py     # Claude API article classification
│   ├── stats_test.py       # Chi-square significance testing
│   └── visualize.py        # Charts and visualizations
├── outputs/                # Analysis results and figures
├── notebooks/              # Exploratory analysis
└── README.md/
```
