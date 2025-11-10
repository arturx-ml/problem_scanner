"""
Collect Polymarket-related posts from Reddit and Twitter for the last month
Focus on identifying user problems and pain points
"""

import os
import praw
import tweepy
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import time

# Load environment variables
load_dotenv()

class PolymarketDataCollector:
    def __init__(self):
        """Initialize Reddit and Twitter API clients"""
        # Reddit setup
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        # Twitter setup
        self.twitter_client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        
    def collect_reddit_posts(self, query='polymarket', subreddits=None, days_back=30, limit=100):
        """
        Collect Reddit posts about Polymarket from the last month
        
        Args:
            query: Search query (default: 'polymarket')
            subreddits: List of subreddit names to search (default: None for all)
            days_back: Number of days to look back (default: 30)
            limit: Maximum posts per subreddit (default: 100, reduced to avoid rate limits)
            
        Returns:
            DataFrame with Reddit posts
        """
        print(f"\n{'='*60}")
        print(f"Collecting Reddit posts about '{query}'")
        print(f"{'='*60}")
        
        all_posts = []
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        cutoff_timestamp = cutoff_date.timestamp()
        
        print(f"\n[DEBUG] Date filter: Posts after {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"[DEBUG] Looking back {days_back} days")
        
        # Default subreddits if none specified
        if subreddits is None:
            subreddits = ['polymarket', 'cryptocurrency', 'CryptoMarkets', 
                         'defi', 'ethereum', 'polygon', 'betting', 'prediction_markets']
        
        for subreddit_name in subreddits:
            print(f"\nSearching r/{subreddit_name}...")
            
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Count posts retrieved and filtered
                posts_retrieved = 0
                posts_filtered_out = 0
                subreddit_posts_count = 0
                
                # For r/polymarket, get all posts instead of searching
                # (since everything there is about polymarket already)
                if subreddit_name.lower() == 'polymarket':
                    print(f"  [DEBUG] Getting all posts (no search query needed), Limit: {limit}")
                    # Combine hot and new posts for better coverage
                    post_generator = list(subreddit.hot(limit=limit//2)) + list(subreddit.new(limit=limit//2))
                else:
                    print(f"  [DEBUG] Query: '{query}', Limit: {limit}, Time filter: month")
                    post_generator = subreddit.search(query, limit=limit, sort='relevance', time_filter='month')
                
                # Iterate through posts
                for post in post_generator:
                    posts_retrieved += 1
                    post_date = datetime.fromtimestamp(post.created_utc)
                    
                    # Log first few posts for debugging
                    if posts_retrieved <= 3:
                        print(f"  [DEBUG] Post #{posts_retrieved}: '{post.title[:60]}...' | Date: {post_date.strftime('%Y-%m-%d')} | Score: {post.score}")
                    
                    # Only include posts from the last month
                    if post.created_utc >= cutoff_timestamp:
                        post_data = {
                            'platform': 'reddit',
                            'id': post.id,
                            'created_utc': post_date,
                            'title': post.title,
                            'text': post.selftext if post.selftext else '',
                            'full_text': f"{post.title}\n\n{post.selftext}",
                            'score': post.score,
                            'num_comments': post.num_comments,
                            'upvote_ratio': post.upvote_ratio,
                            'subreddit': str(post.subreddit),
                            'url': f"https://reddit.com{post.permalink}",
                            'author': str(post.author) if post.author else '[deleted]'
                        }
                        all_posts.append(post_data)
                        subreddit_posts_count += 1
                    else:
                        posts_filtered_out += 1
                        if posts_filtered_out <= 2:
                            print(f"  [DEBUG] Filtered out (too old): '{post.title[:60]}...' | Date: {post_date.strftime('%Y-%m-%d')}")
                
                print(f"  [DEBUG] Retrieved {posts_retrieved} posts from API")
                print(f"  [DEBUG] Filtered out {posts_filtered_out} posts (too old)")
                print(f"  ✓ Found {subreddit_posts_count} posts matching criteria")
                time.sleep(2)  # Rate limiting - 2 second delay between subreddit requests
                
            except Exception as e:
                print(f"  ✗ Error searching r/{subreddit_name}: {str(e)}")
                continue
        
        print(f"\n{'='*60}")
        print(f"Total Reddit posts collected: {len(all_posts)}")
        print(f"{'='*60}")
        
        return pd.DataFrame(all_posts)
    
    def collect_twitter_posts(self, query='polymarket', days_back=7, max_results=5):
        """
        Collect Twitter posts about Polymarket from the last week
        
        Args:
            query: Search query (default: 'polymarket')
            days_back: Number of days to look back (default: 7, max for standard API)
            max_results: Maximum tweets to collect (default: 10, very conservative to avoid rate limits)
            
        Returns:
            DataFrame with Twitter posts
        """
        print(f"\n{'='*60}")
        print(f"Collecting Twitter posts about '{query}'")
        print(f"{'='*60}")
        
        all_tweets = []
        
        # Twitter API only allows searching last 7 days for standard access
        # If you have Academic Research access, you can go back further
        search_days = min(days_back, 7)  # Limit to 7 days for standard access
        
        # end_time must be at least 10 seconds before request time per Twitter API requirements
        # Add buffer and round to avoid timing issues
        end_time = datetime.utcnow() - timedelta(seconds=60)
        start_time = end_time - timedelta(days=search_days) + timedelta(seconds=60)
        
        # Ensure start_time is not too close to end_time
        if (end_time - start_time).total_seconds() < 60:
            print(f"  [DEBUG] Time range too narrow, adjusting...")
            start_time = end_time - timedelta(hours=24)
        
        print(f"\n[DEBUG] Date range: {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print(f"[DEBUG] Searching last {search_days} days")
        
        try:
            # Paginate through results
            tweets_collected = 0
            next_token = None
            
            batch_num = 0
            max_retries = 3
            
            while tweets_collected < max_results:
                batch_num += 1
                batch_size = min(100, max_results - tweets_collected)  # Max 100 per request, but we default to 20
                
                print(f"\n  [DEBUG] Batch #{batch_num}: Requesting {batch_size} tweets (max_results={max_results})...")
                
                # Format times for API (ISO 8601 with seconds)
                start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                
                print(f"  [DEBUG] API start_time: {start_time_str}")
                print(f"  [DEBUG] API end_time: {end_time_str}")
                
                # Retry logic for rate limits
                retry_count = 0
                response = None
                
                while retry_count < max_retries:
                    try:
                        response = self.twitter_client.search_recent_tweets(
                            query=f"{query} -is:retweet lang:en",  # Exclude retweets, English only
                            max_results=batch_size,
                            start_time=start_time_str,
                            end_time=end_time_str,
                            tweet_fields=['created_at', 'public_metrics', 'lang', 'conversation_id'],
                            expansions=['author_id'],
                            user_fields=['username', 'public_metrics'],
                            next_token=next_token
                        )
                        break  # Success, exit retry loop
                        
                    except tweepy.TooManyRequests as e:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 60 * retry_count  # Exponential backoff: 60s, 120s, 180s
                            print(f"  ⚠️  Rate limit hit! Attempt {retry_count}/{max_retries}")
                            print(f"  ⏳ Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                        else:
                            raise  # Re-raise after max retries
                    
                    except tweepy.TwitterServerError as e:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 10 * retry_count
                            print(f"  ⚠️  Twitter server error! Attempt {retry_count}/{max_retries}")
                            print(f"  ⏳ Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                        else:
                            raise
                
                if not response or not response.data:
                    print(f"  [DEBUG] No more tweets found")
                    break
                
                print(f"  [DEBUG] Received {len(response.data)} tweets in this batch")
                
                # Create user lookup
                users = {}
                if response.includes and 'users' in response.includes:
                    users = {user.id: user for user in response.includes['users']}
                
                tweets_in_batch = 0
                for tweet in response.data:
                    tweets_in_batch += 1
                    user = users.get(tweet.author_id, None)
                    
                    # Log first tweet in batch
                    if tweets_in_batch == 1:
                        print(f"  [DEBUG] Sample tweet: '{tweet.text[:80]}...' | Likes: {tweet.public_metrics['like_count']}")
                    
                    tweet_data = {
                        'platform': 'twitter',
                        'id': tweet.id,
                        'created_utc': tweet.created_at,
                        'title': '',  # Twitter doesn't have titles
                        'text': tweet.text,
                        'full_text': tweet.text,
                        'score': tweet.public_metrics['like_count'],
                        'num_comments': tweet.public_metrics['reply_count'],
                        'retweet_count': tweet.public_metrics['retweet_count'],
                        'quote_count': tweet.public_metrics['quote_count'],
                        'author': user.username if user else 'unknown',
                        'author_followers': user.public_metrics['followers_count'] if user else 0,
                        'url': f"https://twitter.com/i/web/status/{tweet.id}"
                    }
                    all_tweets.append(tweet_data)
                    tweets_collected += 1
                
                # Check if there are more results
                if 'next_token' in response.meta:
                    next_token = response.meta['next_token']
                    print(f"  [DEBUG] More results available, waiting 2 seconds...")
                    time.sleep(2)  # Rate limiting - 2 second delay between Twitter API requests
                else:
                    print(f"  [DEBUG] No more results available")
                    break
                
            print(f"\n  ✓ Collected {len(all_tweets)} tweets total")
            
        except tweepy.TooManyRequests as e:
            print(f"\n  ✗ Rate limit exhausted after {max_retries} retries")
            print(f"  ℹ️  Twitter API rate limits:")
            print(f"     - Standard access: 450 requests per 15 minutes")
            print(f"     - Each search counts as 1 request")
            print(f"     - Current setting: {max_results} tweets per collection (very conservative)")
            print(f"  💡 Solutions:")
            print(f"     1. Wait 15 minutes and try again")
            print(f"     2. Skip Twitter: collector.collect_all_data(skip_twitter=True)")
            print(f"     3. Reduce max_results further (already at {max_results})")
            print(f"     4. Run less frequently")
            if len(all_tweets) > 0:
                print(f"\n  ✓ Partial success: Collected {len(all_tweets)} tweets before rate limit")
            else:
                print(f"\n  💡 TIP: Use skip_twitter=True to continue with Reddit data only")
                
        except tweepy.Unauthorized as e:
            print(f"\n  ✗ Authentication error: {str(e)}")
            print(f"  ℹ️  Check your Twitter API credentials in .env file")
            
        except tweepy.Forbidden as e:
            print(f"\n  ✗ Access forbidden: {str(e)}")
            print(f"  ℹ️  Your API access level may not support this endpoint")
            
        except Exception as e:
            print(f"\n  ✗ Error collecting tweets: {str(e)}")
            print(f"  ℹ️  Error type: {type(e).__name__}")
        
        print(f"\n{'='*60}")
        print(f"Total Twitter posts collected: {len(all_tweets)}")
        print(f"{'='*60}")
        
        return pd.DataFrame(all_tweets)
    
    def collect_all_data(self, days_back=30, skip_twitter=False):
        """
        Collect data from both Reddit and Twitter
        
        Args:
            days_back: Number of days to look back (default: 30)
            skip_twitter: Skip Twitter collection if True (default: False, useful if rate limited)
        
        Returns:
            Combined DataFrame with all posts
        """
        print("\n" + "="*60)
        print("POLYMARKET DATA COLLECTION STARTING")
        print("="*60)
        
        # Collect from Reddit (reduced limit to avoid rate limits)
        reddit_df = self.collect_reddit_posts(days_back=days_back, limit=100)
        
        # Collect from Twitter (reduced to 7 days and 20 tweets to avoid rate limits)
        if skip_twitter:
            print("\n⚠️  Skipping Twitter collection (skip_twitter=True)")
            twitter_df = pd.DataFrame()
        else:
            print("\n💡 Collecting only 20 tweets to minimize API usage")
            twitter_df = self.collect_twitter_posts(days_back=min(days_back, 7), max_results=5)
        
        # Combine datasets
        if not reddit_df.empty and not twitter_df.empty:
            combined_df = pd.concat([reddit_df, twitter_df], ignore_index=True)
        elif not reddit_df.empty:
            combined_df = reddit_df
        elif not twitter_df.empty:
            combined_df = twitter_df
        else:
            combined_df = pd.DataFrame()
        
        # Sort by date
        if not combined_df.empty:
            combined_df = combined_df.sort_values('created_utc', ascending=False)
            
            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"polymarket_data_{timestamp}.csv"
            combined_df.to_csv(filename, index=False)
            
            print(f"\n{'='*60}")
            print(f"DATA COLLECTION COMPLETE")
            print(f"{'='*60}")
            print(f"Total posts collected: {len(combined_df)}")
            print(f"  - Reddit: {len(reddit_df)}")
            print(f"  - Twitter: {len(twitter_df)}")
            print(f"Data saved to: {filename}")
            print(f"{'='*60}\n")
            
        return combined_df

if __name__ == "__main__":
    collector = PolymarketDataCollector()
    df = collector.collect_all_data(days_back=30)
    
    if not df.empty:
        print("\nSample of collected data:")
        print(df[['platform', 'created_utc', 'full_text']].head())
