"""
Twitter Scraper using snscrape
Scrapes tweets based on search query and saves to CSV
NOTE: snscrape has compatibility issues with Python 3.13+
For demo purposes, this script can generate sample data
"""

import pandas as pd
from datetime import datetime, timedelta
import argparse
import os
import random

# Try to import scraping libraries
SCRAPER_TYPE = None

# Prioritize snscrape for real-time data
try:
    import snscrape.modules.twitter as sntwitter
    SCRAPER_TYPE = 'snscrape'
    print("✓ Using snscrape for real-time Twitter data")
except (ImportError, AttributeError) as e:
    try:
        from twikit import Client
        SCRAPER_TYPE = 'twikit'
        print("✓ Twikit library loaded (requires authentication)")
    except ImportError:
        SCRAPER_TYPE = 'sample'
        print(f"⚠ Warning: No Twitter scraping library available")
        print("Using sample data generation mode instead.")


def generate_sample_tweets(query, max_tweets=1000):
    """
    Generate sample tweets for demo purposes
    
    Args:
        query: Search query string
        max_tweets: Number of sample tweets to generate
    
    Returns:
        DataFrame with sample tweets
    """
    print("⚠ Generating sample tweets (snscrape not available)")
    print(f"Query: {query}")
    print(f"Generating {max_tweets} sample tweets...\n")
    
    # Generate topic-specific tweets
    positive_templates = [
        f"Great news about {query}! This is exactly what we needed 🎉",
        f"Love seeing the progress with {query}! Very exciting times ahead �",
        f"Inspiring developments in {query} - feeling hopeful about the future!",
        f"The innovation in {query} is breaking records this year! Amazing! 🚀",
        f"Really impressed with the latest {query} updates. This is game-changing!",
        f"{query} is becoming more accessible. Great step forward! ⚡",
        f"The positive impact of {query} is showing real results globally �",
        f"Communities embracing {query} - truly inspiring to see! 💪",
        f"Fantastic to see {query} getting the attention it deserves! 👏",
        f"The future of {query} looks incredibly bright! Excited! ✨",
    ]
    
    negative_templates = [
        f"Another setback for {query}. When will we see real progress? 😔",
        f"Disappointed by the lack of action on {query}. We need change now!",
        f"Frustrated by the slow progress with {query}. Time is running out! ⏰",
        f"The problems with {query} keep getting worse. This is concerning.",
        f"Disappointed in the lack of commitment from leaders on {query} 😠",
        f"Still seeing major issues with {query}. This is terrifying honestly.",
        f"Companies prioritizing profits over {query}. So infuriating! �",
        f"The misinformation about {query} is spreading. Very frustrating!",
        f"Another controversy surrounding {query}. When will this end? 😤",
        f"The challenges with {query} are overwhelming. Need solutions ASAP!",
    ]
    
    neutral_templates = [
        f"New {query} report released. Data shows mixed results and trends.",
        f"Conference on {query} scheduled for next month. Key discussions planned.",
        f"{query} affects multiple sectors including economy and infrastructure.",
        f"Researchers studying the long-term impact of {query} on society.",
        f"New policies regarding {query} being discussed at various levels.",
        f"Latest technology for monitoring {query} has been introduced recently.",
        f"Educational program about {query} launched in institutions nationwide.",
        f"Study examines the relationship between {query} and market trends.",
        f"Experts analyzing {query} data. Results expected in coming months.",
        f"Report on {query} published. Contains comprehensive analysis and stats.",
    ]
    
    tweets_list = []
    templates = positive_templates + negative_templates + neutral_templates
    
    for i in range(max_tweets):
        # Random template selection
        content = random.choice(templates)
        
        # Random date in the past 30 days
        days_ago = random.randint(0, 30)
        tweet_date = datetime.now() - timedelta(days=days_ago)
        
        tweets_list.append({
            'date': tweet_date,
            'id': 1000000000000000000 + i,
            'content': content,
            'username': f'user{random.randint(100, 9999)}',
            'like_count': random.randint(0, 1000),
            'retweet_count': random.randint(0, 500),
            'reply_count': random.randint(0, 100),
            'language': 'en',
            'source': 'Twitter Web App',
            'url': f'https://twitter.com/user/status/{1000000000000000000 + i}'
        })
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1} sample tweets...")
    
    print(f"\nTotal sample tweets generated: {len(tweets_list)}")
    df = pd.DataFrame(tweets_list)
    return df


async def scrape_with_twikit(query, max_tweets=1000):
    """
    Scrape tweets using Twikit (requires authentication)
    
    Note: This requires Twitter credentials. For demo purposes,
    we'll use sample data. To use real data, you need to:
    1. Create a Twitter/X account
    2. Set up credentials in a .env file
    3. Authenticate with twikit
    """
    print("⚠ Twikit requires Twitter authentication")
    print("For demo purposes, generating sample data instead")
    print("To use real Twitter data, please set up authentication")
    return generate_sample_tweets(query, max_tweets)


def scrape_tweets(query, max_tweets=1000, since_date=None, until_date=None):
    """
    Scrape tweets using available method (twikit, snscrape, or samples)
    
    Args:
        query: Search query string (e.g., "climate change", "#AI", "@username")
        max_tweets: Maximum number of tweets to scrape
        since_date: Start date (YYYY-MM-DD format)
        until_date: End date (YYYY-MM-DD format)
    
    Returns:
        DataFrame with scraped tweets
    """
    if SCRAPER_TYPE == 'sample':
        return generate_sample_tweets(query, max_tweets)
    
    if SCRAPER_TYPE == 'twikit':
        # Twikit requires async and authentication
        # For now, use sample data
        return generate_sample_tweets(query, max_tweets)
    
    tweets_list = []
    
    # Build the search query
    search_query = query
    if since_date:
        search_query += f" since:{since_date}"
    if until_date:
        search_query += f" until:{until_date}"
    
    print(f"Scraping tweets for query: {search_query}")
    print(f"Maximum tweets: {max_tweets}")
    
    try:
        # Scrape tweets
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
            if i >= max_tweets:
                break
            
            tweets_list.append({
                'date': tweet.date,
                'id': tweet.id,
                'content': tweet.rawContent,
                'username': tweet.user.username,
                'like_count': tweet.likeCount,
                'retweet_count': tweet.retweetCount,
                'reply_count': tweet.replyCount,
                'language': tweet.lang,
                'source': tweet.sourceLabel,
                'url': tweet.url
            })
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"Scraped {i + 1} tweets...")
        
        print(f"\nTotal tweets scraped: {len(tweets_list)}")
        
        # Create DataFrame
        df = pd.DataFrame(tweets_list)
        return df
    
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
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
    print(f"\nTweets saved to: {filepath}")
    print(f"Total records: {len(df)}")


def main():
    """Main function to run the scraper"""
    parser = argparse.ArgumentParser(description='Scrape tweets using snscrape')
    parser.add_argument('--query', type=str, required=True, 
                        help='Search query (e.g., "climate change", "#AI")')
    parser.add_argument('--max-tweets', type=int, default=1000,
                        help='Maximum number of tweets to scrape (default: 1000)')
    parser.add_argument('--since', type=str, default=None,
                        help='Start date in YYYY-MM-DD format')
    parser.add_argument('--until', type=str, default=None,
                        help='End date in YYYY-MM-DD format')
    parser.add_argument('--output', type=str, default='tweets.csv',
                        help='Output filename (default: tweets.csv)')
    parser.add_argument('--output-dir', type=str, default='data',
                        help='Output directory (default: data)')
    
    args = parser.parse_args()
    
    # Scrape tweets
    df = scrape_tweets(
        query=args.query,
        max_tweets=args.max_tweets,
        since_date=args.since,
        until_date=args.until
    )
    
    # Save to CSV
    if not df.empty:
        save_tweets(df, filename=args.output, output_dir=args.output_dir)
    else:
        print("No tweets found or error occurred during scraping.")


if __name__ == "__main__":
    main()
