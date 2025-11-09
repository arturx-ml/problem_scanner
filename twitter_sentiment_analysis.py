"""
Twitter Sentiment Analysis Script
Analyzes sentiment and insights from Twitter/X posts on a given topic
"""

import os
import tweepy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class TwitterSentimentAnalyzer:
    """Analyze sentiment and insights from Twitter posts"""
    
    def __init__(self):
        """Initialize Twitter API connection"""
        # Twitter API v2 authentication
        self.client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        self.vader = SentimentIntensityAnalyzer()
        self.data = None
        
    def clean_tweet(self, text):
        """Clean tweet text by removing URLs, mentions, and special characters"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags (keep the text)
        text = re.sub(r'#', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def collect_tweets(self, query, max_results=100, language='en'):
        """
        Collect tweets on a given topic
        
        Args:
            query: Search query/topic
            max_results: Number of tweets to collect (10-100 per request)
            language: Language code (default: 'en')
        """
        print(f"Collecting tweets about '{query}'...")
        
        tweets_data = []
        
        try:
            # Search recent tweets (last 7 days for free tier)
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),  # API limit per request
                tweet_fields=['created_at', 'public_metrics', 'lang', 'author_id'],
                expansions=['author_id'],
                user_fields=['username', 'name', 'verified']
            )
            
            if tweets.data:
                # Create user lookup dictionary
                users = {user.id: user for user in tweets.includes['users']} if tweets.includes and 'users' in tweets.includes else {}
                
                for tweet in tweets.data:
                    user = users.get(tweet.author_id)
                    tweets_data.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'cleaned_text': self.clean_tweet(tweet.text),
                        'created_at': tweet.created_at,
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count'],
                        'replies': tweet.public_metrics['reply_count'],
                        'quotes': tweet.public_metrics['quote_count'],
                        'language': tweet.lang,
                        'author_id': tweet.author_id,
                        'author_username': user.username if user else 'unknown',
                        'author_name': user.name if user else 'unknown',
                        'author_verified': user.verified if user else False
                    })
            
            self.data = pd.DataFrame(tweets_data)
            print(f"Collected {len(self.data)} tweets")
            return self.data
            
        except Exception as e:
            print(f"Error collecting tweets: {e}")
            return pd.DataFrame()
    
    def analyze_sentiment(self):
        """Analyze sentiment using TextBlob and VADER"""
        if self.data is None or len(self.data) == 0:
            print("No data to analyze. Please collect tweets first.")
            return None
        
        print("Analyzing sentiment...")
        
        # TextBlob sentiment
        self.data['textblob_polarity'] = self.data['cleaned_text'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        self.data['textblob_subjectivity'] = self.data['cleaned_text'].apply(
            lambda x: TextBlob(str(x)).sentiment.subjectivity
        )
        
        # VADER sentiment
        vader_scores = self.data['cleaned_text'].apply(
            lambda x: self.vader.polarity_scores(str(x))
        )
        self.data['vader_compound'] = vader_scores.apply(lambda x: x['compound'])
        self.data['vader_pos'] = vader_scores.apply(lambda x: x['pos'])
        self.data['vader_neu'] = vader_scores.apply(lambda x: x['neu'])
        self.data['vader_neg'] = vader_scores.apply(lambda x: x['neg'])
        
        # Classify sentiment
        self.data['sentiment_label'] = self.data['vader_compound'].apply(
            lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral')
        )
        
        # Calculate engagement score
        self.data['engagement_score'] = (
            self.data['likes'] + 
            self.data['retweets'] * 2 + 
            self.data['replies'] * 1.5 + 
            self.data['quotes'] * 2
        )
        
        print("Sentiment analysis complete!")
        return self.data
    
    def extract_hashtags(self):
        """Extract hashtags from tweets"""
        if self.data is None:
            return None
        
        all_hashtags = []
        for text in self.data['text']:
            hashtags = re.findall(r'#(\w+)', text)
            all_hashtags.extend(hashtags)
        
        return Counter(all_hashtags)
    
    def extract_mentions(self):
        """Extract mentions from tweets"""
        if self.data is None:
            return None
        
        all_mentions = []
        for text in self.data['text']:
            mentions = re.findall(r'@(\w+)', text)
            all_mentions.extend(mentions)
        
        return Counter(all_mentions)
    
    def get_summary_statistics(self):
        """Get summary statistics of the analysis"""
        if self.data is None:
            return None
        
        hashtags = self.extract_hashtags()
        mentions = self.extract_mentions()
        
        summary = {
            'total_tweets': len(self.data),
            'avg_likes': self.data['likes'].mean(),
            'avg_retweets': self.data['retweets'].mean(),
            'avg_replies': self.data['replies'].mean(),
            'avg_engagement': self.data['engagement_score'].mean(),
            'sentiment_distribution': self.data['sentiment_label'].value_counts().to_dict(),
            'avg_vader_compound': self.data['vader_compound'].mean(),
            'avg_textblob_polarity': self.data['textblob_polarity'].mean(),
            'verified_users': self.data['author_verified'].sum(),
            'top_hashtags': dict(hashtags.most_common(10)),
            'top_mentions': dict(mentions.most_common(10)),
            'date_range': f"{self.data['created_at'].min()} to {self.data['created_at'].max()}"
        }
        
        return summary
    
    def visualize_sentiment_distribution(self):
        """Visualize sentiment distribution"""
        if self.data is None:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Sentiment label distribution
        sentiment_counts = self.data['sentiment_label'].value_counts()
        axes[0, 0].pie(sentiment_counts.values, labels=sentiment_counts.index, 
                       autopct='%1.1f%%', startangle=90, colors=['#1DA1F2', '#657786', '#E1E8ED'])
        axes[0, 0].set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
        
        # VADER compound score distribution
        axes[0, 1].hist(self.data['vader_compound'], bins=30, color='#1DA1F2', alpha=0.7, edgecolor='black')
        axes[0, 1].axvline(self.data['vader_compound'].mean(), color='red', 
                          linestyle='--', label=f"Mean: {self.data['vader_compound'].mean():.3f}")
        axes[0, 1].set_xlabel('VADER Compound Score')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('VADER Sentiment Score Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].legend()
        
        # Sentiment over time
        self.data['hour'] = self.data['created_at'].dt.hour
        time_sentiment = self.data.groupby(['hour', 'sentiment_label']).size().unstack(fill_value=0)
        time_sentiment.plot(kind='bar', stacked=True, ax=axes[1, 0], 
                           color=['#1DA1F2', '#657786', '#E1E8ED'], alpha=0.7)
        axes[1, 0].set_xlabel('Hour of Day')
        axes[1, 0].set_ylabel('Number of Tweets')
        axes[1, 0].set_title('Sentiment Distribution by Hour', fontsize=14, fontweight='bold')
        axes[1, 0].legend(title='Sentiment')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Engagement vs Sentiment
        sentiment_colors = {'Positive': '#1DA1F2', 'Neutral': '#657786', 'Negative': '#E1E8ED'}
        for sentiment in self.data['sentiment_label'].unique():
            data_subset = self.data[self.data['sentiment_label'] == sentiment]
            axes[1, 1].scatter(data_subset['vader_compound'], data_subset['engagement_score'], 
                             alpha=0.5, label=sentiment, color=sentiment_colors[sentiment])
        axes[1, 1].set_xlabel('VADER Compound Score')
        axes[1, 1].set_ylabel('Engagement Score')
        axes[1, 1].set_title('Engagement vs Sentiment', fontsize=14, fontweight='bold')
        axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig('twitter_sentiment_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'twitter_sentiment_analysis.png'")
        plt.show()
    
    def visualize_hashtags(self, top_n=15):
        """Visualize top hashtags"""
        if self.data is None:
            return
        
        hashtags = self.extract_hashtags()
        if not hashtags:
            print("No hashtags found")
            return
        
        top_hashtags = dict(hashtags.most_common(top_n))
        
        plt.figure(figsize=(12, 6))
        plt.barh(list(top_hashtags.keys()), list(top_hashtags.values()), color='#1DA1F2')
        plt.xlabel('Frequency')
        plt.ylabel('Hashtag')
        plt.title(f'Top {top_n} Hashtags', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('twitter_top_hashtags.png', dpi=300, bbox_inches='tight')
        print("Hashtag visualization saved as 'twitter_top_hashtags.png'")
        plt.show()
    
    def generate_wordcloud(self, sentiment_filter=None):
        """Generate word cloud from tweets"""
        if self.data is None:
            return
        
        data_filtered = self.data if sentiment_filter is None else self.data[self.data['sentiment_label'] == sentiment_filter]
        text = ' '.join(data_filtered['cleaned_text'].astype(str))
        
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                             colormap='Blues', max_words=100).generate(text)
        
        plt.figure(figsize=(15, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        title = f'Word Cloud - {sentiment_filter if sentiment_filter else "All"} Tweets'
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        filename = f'twitter_wordcloud_{sentiment_filter if sentiment_filter else "all"}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Word cloud saved as '{filename}'")
        plt.show()
    
    def get_top_tweets(self, n=10, sort_by='engagement_score'):
        """Get top N tweets"""
        if self.data is None:
            return None
        
        return self.data.nlargest(n, sort_by)[['text', 'likes', 'retweets', 
                                                'sentiment_label', 'vader_compound', 
                                                'author_username', 'engagement_score']]
    
    def export_results(self, filename='twitter_analysis_results.csv'):
        """Export results to CSV"""
        if self.data is None:
            return
        
        self.data.to_csv(filename, index=False)
        print(f"Results exported to '{filename}'")


def main():
    """Main execution function"""
    # Initialize analyzer
    analyzer = TwitterSentimentAnalyzer()
    
    # Configuration
    QUERY = "artificial intelligence"  # Change this to your topic
    MAX_RESULTS = 100  # Number of tweets to analyze (10-100)
    LANGUAGE = "en"  # Language code
    
    print("=" * 60)
    print("TWITTER SENTIMENT ANALYSIS")
    print("=" * 60)
    
    # Collect tweets
    analyzer.collect_tweets(query=QUERY, max_results=MAX_RESULTS, language=LANGUAGE)
    
    if analyzer.data is None or len(analyzer.data) == 0:
        print("No tweets collected. Please check your API credentials and query.")
        return
    
    # Analyze sentiment
    analyzer.analyze_sentiment()
    
    # Get summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    summary = analyzer.get_summary_statistics()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Visualize results
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    analyzer.visualize_sentiment_distribution()
    analyzer.visualize_hashtags()
    analyzer.generate_wordcloud()
    
    # Get top tweets
    print("\n" + "=" * 60)
    print("TOP 10 TWEETS BY ENGAGEMENT")
    print("=" * 60)
    top_tweets = analyzer.get_top_tweets(n=10, sort_by='engagement_score')
    print(top_tweets.to_string())
    
    # Export results
    print("\n" + "=" * 60)
    print("EXPORTING RESULTS")
    print("=" * 60)
    analyzer.export_results()
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
