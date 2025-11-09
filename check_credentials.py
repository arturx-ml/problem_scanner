"""
Quick script to check Reddit credentials format
"""
import os
from dotenv import load_dotenv

load_dotenv('.env')

print("=" * 60)
print("CREDENTIAL CHECK")
print("=" * 60)

client_id = os.getenv('REDDIT_CLIENT_ID', '')
client_secret = os.getenv('REDDIT_CLIENT_SECRET', '')
user_agent = os.getenv('REDDIT_USER_AGENT', '')

print("\nChecking credentials format...")
print(f"\nClient ID:")
print(f"  Length: {len(client_id)}")
print(f"  First 5 chars: {client_id[:5] if len(client_id) >= 5 else 'TOO SHORT'}")
has_spaces_id = 'Yes - REMOVE THEM!' if ' ' in client_id else 'No'
print(f"  Has spaces: {has_spaces_id}")
has_quotes_id = 'Yes - REMOVE THEM!' if '"' in client_id or "'" in client_id else 'No'
print(f"  Has quotes: {has_quotes_id}")

print(f"\nClient Secret:")
print(f"  Length: {len(client_secret)}")
print(f"  First 5 chars: {client_secret[:5] if len(client_secret) >= 5 else 'TOO SHORT'}")
has_spaces_secret = 'Yes - REMOVE THEM!' if ' ' in client_secret else 'No'
print(f"  Has spaces: {has_spaces_secret}")
has_quotes_secret = 'Yes - REMOVE THEM!' if '"' in client_secret or "'" in client_secret else 'No'
print(f"  Has quotes: {has_quotes_secret}")

print(f"\nUser Agent:")
print(f"  Value: {user_agent if user_agent else 'Not set (will use default)'}")

print("\n" + "=" * 60)
print("COMMON ISSUES:")
print("=" * 60)
print("1. Make sure there are NO spaces around the = sign")
print("2. Make sure there are NO quotes around values")
print("3. Make sure there are NO spaces in the credentials")
print("4. Format should be: REDDIT_CLIENT_ID=abc123xyz")
print("\nCorrect format:")
print("  REDDIT_CLIENT_ID=your_actual_id")
print("  REDDIT_CLIENT_SECRET=your_actual_secret")
print("  REDDIT_USER_AGENT=SentimentAnalysis/1.0")
