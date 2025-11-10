# Polymarket Problem Analysis Guide

## 🎯 Objective
Analyze Reddit and Twitter posts to identify the top 3-5 problems users face with Polymarket, so we can build solutions using Polymarket and Polygon APIs.

## 📋 What This Does

1. **Data Collection**: Fetches posts about Polymarket from:
   - Reddit (multiple subreddits)
   - Twitter (last 7-30 days depending on API access)

2. **Problem Identification**: Uses NLP to detect posts mentioning problems, issues, bugs, or complaints

3. **Categorization**: Groups problems into categories:
   - Withdrawal issues
   - Deposit/funding problems
   - UI/UX confusion
   - High fees
   - Liquidity/slippage
   - Speed/performance
   - KYC/verification
   - Market resolution
   - Polygon network issues
   - Customer support

4. **Sentiment Analysis**: Measures how negative each problem is

5. **Ranking**: Identifies top 3-5 problems by frequency and severity

## 🚀 Quick Start

### Option 1: Run Everything (Recommended)
```bash
python3 run_full_analysis.py
```

This will:
- ✅ Collect data from Reddit and Twitter
- ✅ Analyze problems using NLP
- ✅ Generate visualizations
- ✅ Create a detailed report

### Option 2: Step by Step

#### Step 1: Collect Data
```bash
python3 collect_polymarket_data.py
```

#### Step 2: Analyze Problems
```bash
python3 analyze_polymarket_problems.py
```

### Option 3: Interactive Jupyter Notebook
```bash
jupyter notebook polymarket_problem_analysis.ipynb
```

## 📊 Output Files

After running the analysis, you'll get:

1. **CSV Files**:
   - `polymarket_data_TIMESTAMP.csv` - All collected posts
   - `polymarket_problem_posts_TIMESTAMP.csv` - Filtered problem posts

2. **Report**:
   - `polymarket_problems_report.txt` - Detailed text report with sample complaints

3. **Visualization**:
   - `polymarket_problems_analysis_TIMESTAMP.png` - Charts showing:
     - Top 5 problems by frequency
     - Problem severity by sentiment
     - Platform distribution
     - All problem categories

4. **JSON** (from notebook):
   - `polymarket_top_problems_TIMESTAMP.json` - Top problems for easy integration

## 🔍 Example Output

The analysis will identify problems like:

**#1. WITHDRAWAL (35% of problem posts)**
- Frequency: 87 mentions
- Avg Sentiment: -0.45 (very negative)
- Sample: "I've been trying to withdraw my funds for 3 days but the transaction keeps failing..."

**#2. FEES (28% of problem posts)**
- Frequency: 69 mentions
- Avg Sentiment: -0.32
- Sample: "The fees on Polymarket are insanely high compared to other platforms..."

... and so on for top 5 problems.

## 💡 Next Steps for App Development

Once you have the top problems identified:

1. **Prioritize** based on:
   - Frequency (how many people complain)
   - Sentiment (how frustrated they are)
   - Feasibility (can we solve it with Polymarket/Polygon API?)

2. **Design Solutions**:
   - Withdrawal tool? → Fast withdrawal tracker/helper
   - Fee calculator? → Gas optimization tool
   - UI confusion? → Simplified interface wrapper
   - etc.

3. **Build** using:
   - Polymarket API
   - Polygon API
   - Your preferred framework

4. **Test** with the community

## ⚙️ Configuration

Edit `.env` to change default settings:

```bash
# Analysis Settings
NUM_POSTS=100  # Posts to fetch per platform
SUBREDDIT=polymarket  # Default subreddit
TWITTER_QUERY=polymarket  # Default search query
```

## 📝 Notes

- **Twitter API Limitation**: Standard access only allows searching last 7 days. For 30-day search, you need Academic Research access.
- **Reddit**: No time limitations, we search the last 30 days by default.
- **Rate Limits**: The scripts include delays to respect API rate limits.
- **Data Quality**: More data = better insights. Consider running multiple times or increasing limits.

## 🛠️ Troubleshooting

### "No data collected"
- Check your API credentials in `.env`
- Run `python3 test_twitter.py` to verify Twitter API
- Verify Reddit credentials are correct

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Twitter API error 429"
- You've hit the rate limit
- Wait 15 minutes and try again
- Reduce `max_results` in the collector

### "No problem posts found"
- The data might not contain problem keywords
- Try collecting from more subreddits
- Adjust `problem_keywords` in `analyze_polymarket_problems.py`

## 📚 Scripts Overview

| Script | Purpose |
|--------|---------|
| `collect_polymarket_data.py` | Fetch posts from Reddit & Twitter |
| `analyze_polymarket_problems.py` | Analyze problems using NLP |
| `run_full_analysis.py` | Run complete pipeline |
| `polymarket_problem_analysis.ipynb` | Interactive analysis notebook |
| `test_twitter.py` | Test Twitter API credentials |

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to modify the scripts to fit your needs!

---

**Ready to find those problems and build solutions! 🚀**
