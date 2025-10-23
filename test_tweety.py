"""
Test tweety-ns for real-time Twitter scraping
"""

from tweety import Twitter
import pandas as pd
from datetime import datetime

def test_tweety():
    print("🐦 Testing tweety-ns for Twitter scraping...")
    print("=" * 60)
    
    try:
        app = Twitter()
        print("✓ Twitter client initialized\n")
        
        # Search for tweets
        query = "AI"
        print(f"Searching for: '{query}'")
        print("Fetching tweets...\n")
        
        tweets = app.search(query, pages=1)
        
        tweets_list = []
        count = 0
        
        for tweet in tweets:
            if count >= 10:  # Limit to 10 for testing
                break
            
            tweets_list.append({
                'date': tweet.created_on,
                'id': tweet.id,
                'content': tweet.text,
                'username': tweet.author.username,
                'like_count': tweet.likes,
                'retweet_count': tweet.retweet_counts,
                'reply_count': tweet.reply_counts,
                'views': tweet.views,
                'url': tweet.url
            })
            
            count += 1
            print(f"{count}. @{tweet.author.username}: {tweet.text[:80]}...")
        
        print(f"\n✓ Successfully scraped {len(tweets_list)} tweets!")
        
        # Save to CSV
        if tweets_list:
            df = pd.DataFrame(tweets_list)
            df.to_csv('data/test_tweety.csv', index=False)
            print(f"💾 Saved to: data/test_tweety.csv")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: tweety-ns may require:")
        print("1. Browser cookies for authentication")
        print("2. CAPTCHA solving service")
        print("3. Or may be blocked by Twitter")
        return False

if __name__ == "__main__":
    test_tweety()
