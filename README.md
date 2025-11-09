# Social Media Sentiment Analysis

A comprehensive Python application for analyzing sentiment and insights from Reddit and Twitter/X posts on any given topic.

## 📋 Features

### Reddit Analysis
- Collect posts from any subreddit or search across all of Reddit
- Sentiment analysis using TextBlob and VADER
- Engagement metrics (score, comments, upvote ratio)
- Temporal trend analysis
- Word clouds and visualizations
- Export results to CSV

### Twitter/X Analysis
- Collect recent tweets (last 7 days)
- Sentiment analysis using TextBlob and VADER
- Hashtag and mention extraction
- Engagement metrics (likes, retweets, replies, quotes)
- Hourly sentiment distribution
- Word clouds and visualizations
- Export results to CSV

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Reddit API credentials
- Twitter API v2 credentials

### 2. Installation

```bash
# Clone or navigate to the project directory
cd windsurf-project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (if needed)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 3. API Setup

#### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Fill in the required fields
5. Note your `client_id` and `client_secret`

#### Twitter API
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new project and app
3. Generate API keys and tokens
4. Note your bearer token and API credentials

### 4. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API credentials
nano .env  # or use your preferred editor
```

Add your credentials to `.env`:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=SentimentAnalysis/1.0

TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

## 📊 Usage

### Option 1: Python Scripts

#### Reddit Analysis
```bash
python reddit_sentiment_analysis.py
```

Edit the configuration in the script:
```python
TOPIC = "artificial intelligence"  # Your topic
SUBREDDIT = "all"  # Specific subreddit or 'all'
LIMIT = 100  # Number of posts
TIME_FILTER = "week"  # 'hour', 'day', 'week', 'month', 'year', 'all'
```

#### Twitter Analysis
```bash
python twitter_sentiment_analysis.py
```

Edit the configuration in the script:
```python
QUERY = "artificial intelligence"  # Your topic
MAX_RESULTS = 100  # Number of tweets (10-100)
LANGUAGE = "en"  # Language code
```

### Option 2: Jupyter Notebooks

```bash
# Start Jupyter Notebook
jupyter notebook

# Open either:
# - reddit_sentiment_analysis.ipynb
# - twitter_sentiment_analysis.ipynb
```

The notebooks provide an interactive environment with:
- Step-by-step execution
- Inline visualizations
- Easy parameter modification
- Detailed explanations

## 📁 Project Structure

```
windsurf-project/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .env.example                        # Example environment variables
├── .gitignore                          # Git ignore rules
│
├── reddit_sentiment_analysis.py        # Reddit analysis script
├── reddit_sentiment_analysis.ipynb     # Reddit analysis notebook
│
├── twitter_sentiment_analysis.py       # Twitter analysis script
└── twitter_sentiment_analysis.ipynb    # Twitter analysis notebook
```

## 📈 Output Files

Both analyzers generate:
- **CSV files**: Complete dataset with sentiment scores
- **PNG visualizations**: 
  - Sentiment distribution charts
  - Word clouds
  - Engagement analysis
  - Temporal trends
- **Summary text files**: Key statistics and insights

## 🔍 Analysis Features

### Sentiment Metrics
- **VADER Compound Score**: -1 (most negative) to +1 (most positive)
- **TextBlob Polarity**: -1 (most negative) to +1 (most positive)
- **Sentiment Labels**: Positive, Neutral, Negative

### Visualizations
- Sentiment distribution pie charts
- VADER score histograms
- Temporal trend analysis
- Word clouds (overall and by sentiment)
- Engagement vs sentiment scatter plots
- Top hashtags (Twitter only)

## 🛠️ Customization

### Reddit Analyzer Class
```python
from reddit_sentiment_analysis import RedditSentimentAnalyzer

analyzer = RedditSentimentAnalyzer()
analyzer.collect_posts(topic="your topic", limit=200)
analyzer.analyze_sentiment()
summary = analyzer.get_summary_statistics()
analyzer.visualize_sentiment_distribution()
```

### Twitter Analyzer Class
```python
from twitter_sentiment_analysis import TwitterSentimentAnalyzer

analyzer = TwitterSentimentAnalyzer()
analyzer.collect_tweets(query="your topic", max_results=100)
analyzer.analyze_sentiment()
summary = analyzer.get_summary_statistics()
analyzer.visualize_sentiment_distribution()
```

## 📝 API Limits

### Reddit API
- Free tier: 60 requests per minute
- Search results: Up to 1000 posts per query
- Historical data: All available posts

### Twitter API v2 (Free Tier)
- Recent search: Last 7 days only
- 10-100 tweets per request
- Rate limits apply (check Twitter documentation)

## 🐛 Troubleshooting

### Common Issues

1. **API Authentication Errors**
   - Verify credentials in `.env` file
   - Ensure no extra spaces in credentials
   - Check API key permissions

2. **No Data Collected**
   - Verify your search query/topic
   - Check API rate limits
   - Ensure internet connection

3. **Import Errors**
   - Activate virtual environment
   - Reinstall requirements: `pip install -r requirements.txt`

4. **Visualization Issues**
   - Install matplotlib backend: `pip install matplotlib`
   - For Jupyter: `%matplotlib inline`

## 📚 Dependencies

Key libraries:
- **praw**: Reddit API wrapper
- **tweepy**: Twitter API wrapper
- **pandas**: Data manipulation
- **textblob**: Sentiment analysis
- **vaderSentiment**: Sentiment analysis
- **matplotlib/seaborn**: Visualizations
- **wordcloud**: Word cloud generation
- **jupyter**: Interactive notebooks

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available for educational and research purposes.

## 🔗 Resources

- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [TextBlob Documentation](https://textblob.readthedocs.io/)

## 💡 Tips

1. **Start Small**: Begin with smaller datasets (50-100 posts) to test
2. **Time Filters**: Use appropriate time filters for trending topics
3. **Multiple Runs**: Run analysis at different times for temporal insights
4. **Combine Data**: Analyze both Reddit and Twitter for comprehensive insights
5. **Custom Queries**: Use advanced search operators for better results

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check your API credentials and limits

---

**Happy Analyzing! 📊✨**
