# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Run Setup Script
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Download required NLTK data
- Create your `.env` file

### Step 2: Configure API Credentials

Edit the `.env` file:
```bash
nano .env
```

Add your credentials:
- **Reddit**: Get from https://www.reddit.com/prefs/apps
- **Twitter**: Get from https://developer.twitter.com/en/portal/dashboard

### Step 3: Test Your Setup
```bash
source venv/bin/activate
python test_setup.py
```

### Step 4: Run Your First Analysis

#### Option A: Python Script
```bash
# Reddit analysis
python reddit_sentiment_analysis.py

# Twitter analysis
python twitter_sentiment_analysis.py
```

#### Option B: Jupyter Notebook
```bash
jupyter notebook
```
Then open:
- `reddit_sentiment_analysis.ipynb` for Reddit
- `twitter_sentiment_analysis.ipynb` for Twitter

## 📝 Customize Your Analysis

### Reddit Analysis
Edit these variables in the script or notebook:
```python
TOPIC = "your topic here"
SUBREDDIT = "all"  # or specific subreddit
LIMIT = 100
TIME_FILTER = "week"
```

### Twitter Analysis
Edit these variables in the script or notebook:
```python
QUERY = "your topic here"
MAX_RESULTS = 100
LANGUAGE = "en"
```

## 📊 What You'll Get

### Output Files
- **CSV files**: Complete data with sentiment scores
- **PNG images**: Visualizations and charts
- **TXT files**: Summary statistics

### Visualizations
- Sentiment distribution pie charts
- Score/engagement histograms
- Word clouds
- Temporal trends
- Top posts/tweets

## 🔧 Troubleshooting

### Virtual Environment Not Activated?
```bash
source venv/bin/activate
```

### Missing Dependencies?
```bash
pip install -r requirements.txt
```

### API Errors?
- Check your `.env` file
- Verify credentials are correct
- Check API rate limits

## 💡 Pro Tips

1. **Start small**: Use `LIMIT=50` for testing
2. **Check rate limits**: Reddit allows 60 req/min
3. **Twitter free tier**: Only last 7 days of tweets
4. **Save your work**: Results are auto-exported to CSV

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the Jupyter notebooks for interactive analysis
- Customize the code for your specific needs
- Combine Reddit and Twitter data for comprehensive insights

---

**Need Help?** Check the troubleshooting section in README.md
