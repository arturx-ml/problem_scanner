import os
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_twitter_credentials():
    """Test Twitter API credentials"""
    print("=" * 50)
    print("Testing Twitter API Credentials")
    print("=" * 50)
    
    # Get credentials from environment
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Check if credentials are set
    print("\n1. Checking if credentials are loaded...")
    credentials = {
        'API Key': api_key,
        'API Secret': api_secret,
        'Access Token': access_token,
        'Access Token Secret': access_token_secret,
        'Bearer Token': bearer_token
    }
    
    missing = []
    for name, value in credentials.items():
        if value:
            print(f"   ✓ {name}: {'*' * 20} (loaded)")
        else:
            print(f"   ✗ {name}: NOT SET")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing credentials: {', '.join(missing)}")
        return False
    
    # Test API v2 with Bearer Token
    print("\n2. Testing Twitter API v2 (Bearer Token)...")
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        
        # Search for recent tweets about "polymarket"
        query = os.getenv('TWITTER_QUERY', 'polymarket')
        print(f"   Searching for tweets about '{query}'...")
        
        response = client.search_recent_tweets(
            query=query,
            max_results=10,
            tweet_fields=['created_at', 'public_metrics', 'lang']
        )
        
        if response.data:
            print(f"   ✓ Successfully fetched {len(response.data)} tweets!")
            print("\n   Sample tweets:")
            for i, tweet in enumerate(response.data[:3], 1):
                print(f"\n   Tweet {i}:")
                print(f"   Text: {tweet.text[:100]}...")
                print(f"   Likes: {tweet.public_metrics['like_count']}")
                print(f"   Retweets: {tweet.public_metrics['retweet_count']}")
        else:
            print("   ⚠ No tweets found for this query")
            
        print("\n✅ Twitter API v2 test PASSED!")
        return True
        
    except tweepy.TweepyException as e:
        print(f"\n❌ Twitter API v2 test FAILED!")
        print(f"   Error: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_twitter_credentials()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Your Twitter API is working!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Tests failed. Please check your credentials.")
        print("=" * 50)
