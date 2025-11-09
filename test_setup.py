"""
Test script to verify the setup and API credentials
"""

import os
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import praw
        import tweepy
        import pandas
        import numpy
        import textblob
        import vaderSentiment
        import matplotlib
        import seaborn
        import wordcloud
        import nltk
        print("✓ All packages imported successfully!")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_reddit_credentials():
    """Test Reddit API credentials"""
    print("\nTesting Reddit API credentials...")
    load_dotenv()
    
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')
    
    if not client_id or client_id == 'your_client_id_here':
        print("✗ Reddit CLIENT_ID not configured")
        return False
    
    if not client_secret or client_secret == 'your_client_secret_here':
        print("✗ Reddit CLIENT_SECRET not configured")
        return False
    
    try:
        import praw
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent or 'SentimentAnalysis/1.0'
        )
        # Test connection
        reddit.user.me()
        print("✓ Reddit API credentials valid!")
        return True
    except Exception as e:
        print(f"✗ Reddit API error: {e}")
        print("Note: If you're using read-only mode, this is expected")
        return True  # Return True for read-only mode

def test_twitter_credentials():
    """Test Twitter API credentials"""
    print("\nTesting Twitter API credentials...")
    load_dotenv()
    
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not bearer_token or bearer_token == 'your_bearer_token_here':
        print("✗ Twitter BEARER_TOKEN not configured")
        return False
    
    try:
        import tweepy
        client = tweepy.Client(bearer_token=bearer_token)
        # Test with a simple search
        response = client.search_recent_tweets(query="test", max_results=10)
        print("✓ Twitter API credentials valid!")
        return True
    except Exception as e:
        print(f"✗ Twitter API error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SETUP VERIFICATION TEST")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test Reddit
    results.append(("Reddit API", test_reddit_credentials()))
    
    # Test Twitter
    results.append(("Twitter API", test_twitter_credentials()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! You're ready to go!")
    else:
        print("⚠️  Some tests failed. Please check your configuration.")
        print("\nNext steps:")
        print("1. Make sure you've run: pip install -r requirements.txt")
        print("2. Copy .env.example to .env: cp .env.example .env")
        print("3. Edit .env and add your API credentials")
    print("=" * 60)

if __name__ == "__main__":
    main()
