"""
Twitter Scraper using ntscraper
Scrapes real-time tweets from Twitter without authentication
"""

import pandas as pd
from datetime import datetime
import argparse
import os
from ntscraper import Nitter

def scrape_tweets_realtime(query, max_tweets=1000, mode='term', language='en'):
    """
    Scrape real-time tweets using ntscraper
    
    Args:
        query: Search query string or username
        max_tweets: Maximum number of tweets to scrape
        mode: 'term' for keyword search, 'user' for user timeline
        language: Language filter (default: 'en')
    
    Returns:
        DataFrame with scraped tweets
    """
    print(f"🐦 Scraping tweets using ntscraper")
    print(f"Query: {query}")
    print(f"Mode: {mode}")
    print(f"Maximum tweets: {max_tweets}\n")
    
    try:
        # Initialize scraper
        scraper = Nitter(log_level=1, skip_instance_check=False)
        
        tweets_list = []
        
        if mode == 'term':
            # Search for tweets by term/keyword
            print(f"Searching for tweets containing: '{query}'")
            tweets = scraper.get_tweets(query, mode=mode, number=max_tweets)
        elif mode == 'user':
            # Get tweets from specific user
            print(f"Getting tweets from user: {query}")
            tweets = scraper.get_tweets(query, mode=mode, number=max_tweets)
        else:
            print(f"Invalid mode: {mode}. Use 'term' or 'user'")
            return pd.DataFrame()
        
        if not tweets or 'tweets' not in tweets:
            print("No tweets found or error occurred")
            return pd.DataFrame()
        
        # Process tweets
        for i, tweet in enumerate(tweets['tweets'], 1):
            tweets_list.append({
                'date': tweet.get('date', datetime.now()),
                'id': i,
                'content': tweet.get('text', ''),
                'username': tweet.get('user', {}).get('username', 'unknown'),
                'like_count': tweet.get('stats', {}).get('likes', 0),
                'retweet_count': tweet.get('stats', {}).get('retweets', 0),
                'reply_count': tweet.get('stats', {}).get('comments', 0),
                'language': tweet.get('language', 'en'),
                'source': 'ntscraper',
                'url': tweet.get('link', '')
            })
            
            # Progress indicator
            if i % 50 == 0:
                print(f"Scraped {i} tweets...")
        
        print(f"\n✓ Successfully scraped {len(tweets_list)} tweets")
        
        # Create DataFrame
        df = pd.DataFrame(tweets_list)
        return df
    
    except Exception as e:
        print(f"❌ Error occurred while scraping: {e}")
        print("This might be due to:")
        print("1. Twitter/Nitter servers being temporarily unavailable")
        print("2. Rate limiting")
        print("3. Network connectivity issues")
        print("\nTry again in a few minutes or use sample data mode.")
        
        if tweets_list:
            print(f"Returning {len(tweets_list)} tweets collected before error")
            return pd.DataFrame(tweets_list)
        return pd.DataFrame()


def save_tweets(df, filename='tweets.csv', output_dir='data'):
    """
    Save tweets DataFrame to CSV
    
    Args:
        df: DataFrame containing tweets
        filename: Name of output file
        output_dir: Directory to save the file
    """
    if df.empty:
        print("No tweets to save!")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"\n💾 Tweets saved to: {filepath}")
    print(f"Total records: {len(df)}")


def main():
    """Main function to run the scraper"""
    parser = argparse.ArgumentParser(description='Scrape real-time tweets using ntscraper')
    parser.add_argument('--query', type=str, required=True, 
                        help='Search query or username')
    parser.add_argument('--max-tweets', type=int, default=100,
                        help='Maximum number of tweets to scrape (default: 100)')
    parser.add_argument('--mode', type=str, default='term', choices=['term', 'user'],
                        help='Scraping mode: "term" for keyword search or "user" for user timeline')
    parser.add_argument('--language', type=str, default='en',
                        help='Language filter (default: en)')
    parser.add_argument('--output', type=str, default='tweets.csv',
                        help='Output filename (default: tweets.csv)')
    parser.add_argument('--output-dir', type=str, default='data',
                        help='Output directory (default: data)')
    
    args = parser.parse_args()
    
    # Scrape tweets
    df = scrape_tweets_realtime(
        query=args.query,
        max_tweets=args.max_tweets,
        mode=args.mode,
        language=args.language
    )
    
    # Save to CSV
    if not df.empty:
        save_tweets(df, filename=args.output, output_dir=args.output_dir)
    else:
        print("❌ No tweets found or error occurred during scraping.")


if __name__ == "__main__":
    main()
