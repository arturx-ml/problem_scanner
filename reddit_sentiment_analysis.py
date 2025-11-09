"""
Reddit Sentiment Analysis Script
Analyzes sentiment and insights from Reddit posts and comments on a given topic
"""

import os
import praw
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class RedditSentimentAnalyzer:
    """Analyze sentiment and insights from Reddit posts"""
    
    def __init__(self):
        """Initialize Reddit API connection"""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'SentimentAnalysis/1.0')
        )
        self.vader = SentimentIntensityAnalyzer()
        self.data = None
        
    def collect_posts(self, topic, subreddit='all', limit=100, time_filter='week'):
        """
        Collect Reddit posts on a given topic
        
        Args:
            topic: Search query/topic
            subreddit: Subreddit to search (default: 'all')
            limit: Number of posts to collect
            time_filter: Time filter ('hour', 'day', 'week', 'month', 'year', 'all')
        """
        print(f"Collecting {limit} posts about '{topic}' from r/{subreddit}...")
        
        posts_data = []
        subreddit_obj = self.reddit.subreddit(subreddit)
        
        for post in subreddit_obj.search(topic, limit=limit, time_filter=time_filter):
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'text': post.selftext,
                'score': post.score,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'created_utc': datetime.fromtimestamp(post.created_utc),
                'subreddit': post.subreddit.display_name,
                'author': str(post.author),
                'url': post.url,
                'permalink': f"https://reddit.com{post.permalink}"
            })
        
        self.data = pd.DataFrame(posts_data)
        print(f"Collected {len(self.data)} posts")
        return self.data
    
    def analyze_sentiment(self):
        """Analyze sentiment using TextBlob and VADER"""
        if self.data is None or len(self.data) == 0:
            print("No data to analyze. Please collect posts first.")
            return None
        
        print("Analyzing sentiment...")
        
        # Combine title and text for analysis
        self.data['full_text'] = self.data['title'] + ' ' + self.data['text']
        
        # TextBlob sentiment
        self.data['textblob_polarity'] = self.data['full_text'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        self.data['textblob_subjectivity'] = self.data['full_text'].apply(
            lambda x: TextBlob(str(x)).sentiment.subjectivity
        )
        
        # VADER sentiment
        vader_scores = self.data['full_text'].apply(
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
        
        print("Sentiment analysis complete!")
        return self.data
    
    def get_summary_statistics(self):
        """Get summary statistics of the analysis"""
        if self.data is None:
            return None
        
        summary = {
            'total_posts': len(self.data),
            'avg_score': self.data['score'].mean(),
            'avg_comments': self.data['num_comments'].mean(),
            'avg_upvote_ratio': self.data['upvote_ratio'].mean(),
            'sentiment_distribution': self.data['sentiment_label'].value_counts().to_dict(),
            'avg_vader_compound': self.data['vader_compound'].mean(),
            'avg_textblob_polarity': self.data['textblob_polarity'].mean(),
            'most_active_subreddits': self.data['subreddit'].value_counts().head(5).to_dict(),
            'date_range': f"{self.data['created_utc'].min()} to {self.data['created_utc'].max()}"
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
                       autopct='%1.1f%%', startangle=90, colors=['#2ecc71', '#95a5a6', '#e74c3c'])
        axes[0, 0].set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
        
        # VADER compound score distribution
        axes[0, 1].hist(self.data['vader_compound'], bins=30, color='#3498db', alpha=0.7, edgecolor='black')
        axes[0, 1].axvline(self.data['vader_compound'].mean(), color='red', 
                          linestyle='--', label=f"Mean: {self.data['vader_compound'].mean():.3f}")
        axes[0, 1].set_xlabel('VADER Compound Score')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('VADER Sentiment Score Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].legend()
        
        # Sentiment over time
        time_sentiment = self.data.groupby([self.data['created_utc'].dt.date, 'sentiment_label']).size().unstack(fill_value=0)
        time_sentiment.plot(kind='area', stacked=True, ax=axes[1, 0], 
                           color=['#2ecc71', '#95a5a6', '#e74c3c'], alpha=0.7)
        axes[1, 0].set_xlabel('Date')
        axes[1, 0].set_ylabel('Number of Posts')
        axes[1, 0].set_title('Sentiment Trends Over Time', fontsize=14, fontweight='bold')
        axes[1, 0].legend(title='Sentiment')
        
        # Score vs Sentiment
        sentiment_colors = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
        for sentiment in self.data['sentiment_label'].unique():
            data_subset = self.data[self.data['sentiment_label'] == sentiment]
            axes[1, 1].scatter(data_subset['vader_compound'], data_subset['score'], 
                             alpha=0.5, label=sentiment, color=sentiment_colors[sentiment])
        axes[1, 1].set_xlabel('VADER Compound Score')
        axes[1, 1].set_ylabel('Post Score')
        axes[1, 1].set_title('Post Score vs Sentiment', fontsize=14, fontweight='bold')
        axes[1, 1].legend()
        
        plt.tight_layout()
        plt.savefig('reddit_sentiment_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'reddit_sentiment_analysis.png'")
        plt.show()
    
    def generate_wordcloud(self, sentiment_filter=None):
        """Generate word cloud from posts"""
        if self.data is None:
            return
        
        data_filtered = self.data if sentiment_filter is None else self.data[self.data['sentiment_label'] == sentiment_filter]
        text = ' '.join(data_filtered['full_text'].astype(str))
        
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                             colormap='viridis', max_words=100).generate(text)
        
        plt.figure(figsize=(15, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        title = f'Word Cloud - {sentiment_filter if sentiment_filter else "All"} Posts'
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        filename = f'reddit_wordcloud_{sentiment_filter if sentiment_filter else "all"}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Word cloud saved as '{filename}'")
        plt.show()
    
    def get_top_posts(self, n=10, sort_by='score'):
        """Get top N posts"""
        if self.data is None:
            return None
        
        return self.data.nlargest(n, sort_by)[['title', 'score', 'num_comments', 
                                                'sentiment_label', 'vader_compound', 'permalink']]
    
    def export_results(self, filename='reddit_analysis_results.csv'):
        """Export results to CSV"""
        if self.data is None:
            return
        
        self.data.to_csv(filename, index=False)
        print(f"Results exported to '{filename}'")


def main():
    """Main execution function"""
    # Initialize analyzer
    analyzer = RedditSentimentAnalyzer()
    
    # Configuration
    TOPIC = "artificial intelligence"  # Change this to your topic
    SUBREDDIT = "all"  # Change to specific subreddit or keep 'all'
    LIMIT = 100  # Number of posts to analyze
    TIME_FILTER = "week"  # 'hour', 'day', 'week', 'month', 'year', 'all'
    
    print("=" * 60)
    print("REDDIT SENTIMENT ANALYSIS")
    print("=" * 60)
    
    # Collect posts
    analyzer.collect_posts(topic=TOPIC, subreddit=SUBREDDIT, limit=LIMIT, time_filter=TIME_FILTER)
    
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
    analyzer.generate_wordcloud()
    
    # Get top posts
    print("\n" + "=" * 60)
    print("TOP 10 POSTS BY SCORE")
    print("=" * 60)
    top_posts = analyzer.get_top_posts(n=10, sort_by='score')
    print(top_posts.to_string())
    
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
