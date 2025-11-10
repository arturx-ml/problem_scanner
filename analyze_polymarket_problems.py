"""
Analyze Polymarket-related posts to identify top user problems and pain points
Uses NLP, sentiment analysis, and keyword extraction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# NLP and Sentiment Analysis
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class PolymarketProblemAnalyzer:
    def __init__(self, data_file=None):
        """Initialize the analyzer with data"""
        self.vader = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Problem-related keywords
        self.problem_keywords = [
            'problem', 'issue', 'error', 'bug', 'broken', 'not working', 'failed', 'failure',
            'cant', 'cannot', 'won\'t', 'doesn\'t work', 'stuck', 'help', 'fix', 'trouble',
            'difficult', 'hard', 'complicated', 'confusing', 'frustrated', 'annoying',
            'slow', 'laggy', 'crash', 'frozen', 'glitch', 'wrong', 'incorrect', 'missing',
            'lost', 'scam', 'fraud', 'withdraw', 'withdrawal', 'locked', 'banned', 'suspended'
        ]
        
        # Specific Polymarket problem categories
        self.problem_categories = {
            'withdrawal': ['withdraw', 'withdrawal', 'cash out', 'payout', 'transfer out', 'cant withdraw'],
            'deposit': ['deposit', 'fund', 'add money', 'cant deposit', 'payment failed'],
            'ui_ux': ['confusing', 'hard to use', 'interface', 'ui', 'ux', 'design', 'navigation', 'find'],
            'fees': ['fee', 'fees', 'expensive', 'cost', 'charge', 'high fee'],
            'liquidity': ['liquidity', 'spread', 'slippage', 'no orders', 'volume', 'cant sell', 'cant buy'],
            'speed': ['slow', 'laggy', 'loading', 'pending', 'delay', 'wait', 'taking forever'],
            'kyc_verification': ['kyc', 'verify', 'verification', 'identity', 'id', 'rejected'],
            'market_resolution': ['resolution', 'resolve', 'outcome', 'result', 'payout', 'settled'],
            'polygon_network': ['polygon', 'matic', 'network', 'gas', 'transaction failed', 'metamask'],
            'customer_support': ['support', 'customer service', 'no response', 'help', 'contact', 'ticket']
        }
        
        if data_file:
            self.df = pd.read_csv(data_file)
            self.df['created_utc'] = pd.to_datetime(self.df['created_utc'])
        else:
            self.df = None
    
    def load_latest_data(self):
        """Load the most recent data file"""
        import glob
        files = glob.glob('polymarket_data_*.csv')
        if files:
            latest_file = max(files)
            print(f"Loading data from: {latest_file}")
            self.df = pd.read_csv(latest_file)
            self.df['created_utc'] = pd.to_datetime(self.df['created_utc'])
            return True
        else:
            print("No data files found. Please run collect_polymarket_data.py first.")
            return False
    
    def identify_problem_posts(self):
        """Identify posts that mention problems"""
        if self.df is None:
            return pd.DataFrame()
        
        print("\n" + "="*60)
        print("IDENTIFYING PROBLEM POSTS")
        print("="*60)
        
        def contains_problem(text):
            """Check if text contains problem-related keywords"""
            if pd.isna(text):
                return False
            text_lower = text.lower()
            return any(keyword in text_lower for keyword in self.problem_keywords)
        
        # Filter for problem posts
        self.df['is_problem'] = self.df['full_text'].apply(contains_problem)
        problem_df = self.df[self.df['is_problem']].copy()
        
        print(f"Total posts: {len(self.df)}")
        print(f"Problem posts: {len(problem_df)} ({len(problem_df)/len(self.df)*100:.1f}%)")
        
        return problem_df
    
    def analyze_sentiment(self, df):
        """Analyze sentiment of posts using VADER"""
        print("\n" + "="*60)
        print("ANALYZING SENTIMENT")
        print("="*60)
        
        def get_vader_sentiment(text):
            if pd.isna(text):
                return {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}
            return self.vader.polarity_scores(text)
        
        sentiments = df['full_text'].apply(get_vader_sentiment)
        df['sentiment_neg'] = sentiments.apply(lambda x: x['neg'])
        df['sentiment_neu'] = sentiments.apply(lambda x: x['neu'])
        df['sentiment_pos'] = sentiments.apply(lambda x: x['pos'])
        df['sentiment_compound'] = sentiments.apply(lambda x: x['compound'])
        
        # Classify sentiment
        def classify_sentiment(compound):
            if compound >= 0.05:
                return 'positive'
            elif compound <= -0.05:
                return 'negative'
            else:
                return 'neutral'
        
        df['sentiment'] = df['sentiment_compound'].apply(classify_sentiment)
        
        print("\nSentiment distribution:")
        print(df['sentiment'].value_counts())
        
        return df
    
    def categorize_problems(self, df):
        """Categorize problems into specific areas"""
        print("\n" + "="*60)
        print("CATEGORIZING PROBLEMS")
        print("="*60)
        
        def find_categories(text):
            if pd.isna(text):
                return []
            text_lower = text.lower()
            categories = []
            for category, keywords in self.problem_categories.items():
                if any(keyword in text_lower for keyword in keywords):
                    categories.append(category)
            return categories
        
        df['problem_categories'] = df['full_text'].apply(find_categories)
        
        # Count category occurrences
        all_categories = []
        for categories in df['problem_categories']:
            all_categories.extend(categories)
        
        category_counts = Counter(all_categories)
        
        print("\nProblem categories found:")
        for category, count in category_counts.most_common():
            print(f"  {category}: {count} posts")
        
        return df, category_counts
    
    def extract_top_problems(self, problem_df, category_counts, top_n=5):
        """Extract and rank the top N problems"""
        print("\n" + "="*60)
        print(f"TOP {top_n} PROBLEMS")
        print("="*60)
        
        top_problems = []
        
        for i, (category, count) in enumerate(category_counts.most_common(top_n), 1):
            # Get posts in this category
            category_posts = problem_df[
                problem_df['problem_categories'].apply(lambda x: category in x)
            ]
            
            # Calculate average sentiment
            avg_sentiment = category_posts['sentiment_compound'].mean()
            
            # Get sample complaints
            negative_posts = category_posts[
                category_posts['sentiment'] == 'negative'
            ].nsmallest(3, 'sentiment_compound')
            
            samples = negative_posts['full_text'].tolist()
            
            problem = {
                'rank': i,
                'category': category,
                'count': count,
                'percentage': (count / len(problem_df)) * 100,
                'avg_sentiment': avg_sentiment,
                'sample_complaints': samples,
                'platforms': category_posts['platform'].value_counts().to_dict()
            }
            
            top_problems.append(problem)
            
            # Print summary
            print(f"\n#{i}. {category.upper().replace('_', ' ')}")
            print(f"   Mentions: {count} posts ({problem['percentage']:.1f}% of problem posts)")
            print(f"   Avg Sentiment: {avg_sentiment:.3f}")
            print(f"   Platforms: {problem['platforms']}")
            if samples:
                print(f"   Sample complaint:")
                print(f"   \"{samples[0][:150]}...\"")
        
        return top_problems
    
    def generate_report(self, top_problems, output_file='polymarket_problems_report.txt'):
        """Generate a detailed text report"""
        print("\n" + "="*60)
        print("GENERATING DETAILED REPORT")
        print("="*60)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("POLYMARKET USER PROBLEMS ANALYSIS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for problem in top_problems:
                f.write(f"\n{'-'*80}\n")
                f.write(f"RANK #{problem['rank']}: {problem['category'].upper().replace('_', ' ')}\n")
                f.write(f"{'-'*80}\n\n")
                
                f.write(f"FREQUENCY: {problem['count']} mentions ({problem['percentage']:.1f}% of problem posts)\n")
                f.write(f"AVG SENTIMENT: {problem['avg_sentiment']:.3f} (more negative = bigger problem)\n")
                f.write(f"PLATFORMS: {problem['platforms']}\n\n")
                
                f.write("SAMPLE COMPLAINTS:\n")
                for i, complaint in enumerate(problem['sample_complaints'], 1):
                    f.write(f"\n{i}. {complaint}\n")
                
                f.write("\n" + "="*80 + "\n")
        
        print(f"Report saved to: {output_file}")
        return output_file
    
    def visualize_results(self, top_problems, category_counts):
        """Create visualizations of the analysis"""
        print("\n" + "="*60)
        print("CREATING VISUALIZATIONS")
        print("="*60)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Polymarket User Problems Analysis', fontsize=16, fontweight='bold')
        
        # 1. Top Problems Bar Chart
        ax1 = axes[0, 0]
        categories = [p['category'].replace('_', ' ').title() for p in top_problems]
        counts = [p['count'] for p in top_problems]
        colors = sns.color_palette("Reds_r", len(categories))
        ax1.barh(categories, counts, color=colors)
        ax1.set_xlabel('Number of Mentions')
        ax1.set_title('Top 5 Problems by Frequency')
        ax1.invert_yaxis()
        
        # 2. Sentiment Distribution
        ax2 = axes[0, 1]
        categories = [p['category'].replace('_', ' ').title() for p in top_problems]
        sentiments = [p['avg_sentiment'] for p in top_problems]
        colors = ['red' if s < -0.1 else 'orange' if s < 0.1 else 'green' for s in sentiments]
        ax2.barh(categories, sentiments, color=colors)
        ax2.set_xlabel('Average Sentiment Score')
        ax2.set_title('Problem Severity by Sentiment')
        ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.5)
        ax2.invert_yaxis()
        
        # 3. Platform Distribution
        ax3 = axes[1, 0]
        platform_data = {'reddit': 0, 'twitter': 0}
        for problem in top_problems:
            for platform, count in problem['platforms'].items():
                platform_data[platform] = platform_data.get(platform, 0) + count
        ax3.pie(platform_data.values(), labels=platform_data.keys(), autopct='%1.1f%%',
                colors=['#FF4500', '#1DA1F2'])
        ax3.set_title('Problems by Platform')
        
        # 4. All Categories Distribution
        ax4 = axes[1, 1]
        top_categories = dict(category_counts.most_common(10))
        ax4.bar(range(len(top_categories)), list(top_categories.values()),
                color=sns.color_palette("viridis", len(top_categories)))
        ax4.set_xticks(range(len(top_categories)))
        ax4.set_xticklabels([k.replace('_', ' ').title() for k in top_categories.keys()],
                            rotation=45, ha='right')
        ax4.set_ylabel('Mentions')
        ax4.set_title('All Problem Categories')
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'polymarket_problems_analysis_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to: {filename}")
        
        return filename
    
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("\n" + "="*80)
        print(" "*20 + "POLYMARKET PROBLEM ANALYSIS")
        print("="*80)
        
        # Load data if not already loaded
        if self.df is None:
            if not self.load_latest_data():
                return
        
        # Identify problem posts
        problem_df = self.identify_problem_posts()
        
        if len(problem_df) == 0:
            print("\nNo problem posts found!")
            return
        
        # Analyze sentiment
        problem_df = self.analyze_sentiment(problem_df)
        
        # Categorize problems
        problem_df, category_counts = self.categorize_problems(problem_df)
        
        # Extract top problems
        top_problems = self.extract_top_problems(problem_df, category_counts, top_n=5)
        
        # Generate report
        report_file = self.generate_report(top_problems)
        
        # Create visualizations
        viz_file = self.visualize_results(top_problems, category_counts)
        
        # Save processed data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        problem_file = f'polymarket_problem_posts_{timestamp}.csv'
        problem_df.to_csv(problem_file, index=False)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE!")
        print("="*80)
        print(f"\nFiles generated:")
        print(f"  1. Problem posts CSV: {problem_file}")
        print(f"  2. Text report: {report_file}")
        print(f"  3. Visualization: {viz_file}")
        print("\n" + "="*80 + "\n")
        
        return {
            'top_problems': top_problems,
            'problem_df': problem_df,
            'report_file': report_file,
            'viz_file': viz_file
        }

if __name__ == "__main__":
    analyzer = PolymarketProblemAnalyzer()
    results = analyzer.run_full_analysis()
