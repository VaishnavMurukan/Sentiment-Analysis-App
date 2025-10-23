# 🔐 Setting Up Real Twitter Data (Twikit Authentication)

## Current Status
✅ **Twikit library installed**  
⚠️ **Sample data mode active** (authentication not configured)

## Why Sample Data?
Twitter/X requires authentication to scrape tweets. Without credentials, we use AI-generated sample tweets that are topic-specific and demonstrate the full functionality of the app.

---

## 🚀 How to Get Real Twitter Data

### Prerequisites
- A Twitter/X account
- Python 3.13 with twikit installed (✅ Already done!)

### Step 1: Create Twitter Account Credentials

You need a Twitter/X account. The free account works fine for basic scraping.

### Step 2: Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```env
TWITTER_USERNAME=your_twitter_username
TWITTER_EMAIL=your_twitter_email@example.com
TWITTER_PASSWORD=your_twitter_password
```

### Step 3: Update `scrape_tweets.py`

Replace the `scrape_with_twikit` function with this:

```python
import asyncio
from twikit import Client
import os
from dotenv import load_dotenv

load_dotenv()

async def scrape_with_twikit(query, max_tweets=1000):
    """
    Scrape tweets using Twikit with authentication
    """
    client = Client('en-US')
    
    # Load credentials from environment
    username = os.getenv('TWITTER_USERNAME')
    email = os.getenv('TWITTER_EMAIL')
    password = os.getenv('TWITTER_PASSWORD')
    
    if not all([username, email, password]):
        print("⚠ Twitter credentials not found in .env file")
        print("Using sample data instead")
        return generate_sample_tweets(query, max_tweets)
    
    try:
        # Login
        print("🔐 Logging into Twitter...")
        await client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password
        )
        
        # Search tweets
        print(f"🔍 Searching for: {query}")
        tweets_list = []
        
        tweets = await client.search_tweet(query, 'Latest')
        
        for i, tweet in enumerate(tweets):
            if i >= max_tweets:
                break
                
            tweets_list.append({
                'date': tweet.created_at,
                'id': tweet.id,
                'content': tweet.text,
                'username': tweet.user.screen_name,
                'like_count': tweet.favorite_count,
                'retweet_count': tweet.retweet_count,
                'reply_count': tweet.reply_count,
                'language': tweet.lang,
                'source': 'Twitter',
                'url': f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
            })
            
            if (i + 1) % 100 == 0:
                print(f"Scraped {i + 1} tweets...")
        
        print(f"\n✓ Successfully scraped {len(tweets_list)} real tweets!")
        return pd.DataFrame(tweets_list)
        
    except Exception as e:
        print(f"❌ Error scraping with Twikit: {e}")
        print("Falling back to sample data")
        return generate_sample_tweets(query, max_tweets)


def scrape_tweets(query, max_tweets=1000, since_date=None, until_date=None):
    """
    Scrape tweets using twikit or sample data
    """
    if SCRAPER_TYPE == 'twikit':
        # Run async function
        try:
            return asyncio.run(scrape_with_twikit(query, max_tweets))
        except Exception as e:
            print(f"Error: {e}")
            return generate_sample_tweets(query, max_tweets)
    
    return generate_sample_tweets(query, max_tweets)
```

### Step 4: Install python-dotenv

```bash
cd backend
pip install python-dotenv
```

### Step 5: Restart Backend

```bash
cd backend
python app.py
```

---

## 🎯 Alternative: Twitter API v2

If you prefer using official Twitter API:

### Pros:
- ✅ Official and stable
- ✅ Better rate limits with paid plans
- ✅ More reliable

### Cons:
- ❌ Requires Twitter Developer account
- ❌ Free tier is very limited (10,000 tweets/month)
- ❌ Approval process needed

### Setup:
1. Go to https://developer.twitter.com
2. Create a developer account
3. Create a new app
4. Get API keys and tokens
5. Use `tweepy` library instead of twikit

---

## 📊 Current Sample Data Features

While using sample data, you still get:
- ✅ **Topic-specific tweets** (AI generates relevant content)
- ✅ **Realistic sentiment distribution**
- ✅ **Proper metadata** (likes, retweets, dates)
- ✅ **All analysis features** work identically
- ✅ **Full UI/UX demonstration**

### Sample Data Templates:
- **10 positive templates** per topic
- **10 negative templates** per topic  
- **10 neutral templates** per topic
- **All dynamically include the search topic**

---

## 🔒 Security Notes

**NEVER commit your .env file to Git!**

Add to `.gitignore`:
```
.env
cookies.json
*.log
```

The `.env` file contains sensitive credentials.

---

## 💡 Recommendations

For this **internship/learning project**, I recommend:

1. **Keep using sample data** - It's perfect for demonstration
2. **Add the disclaimer banner** - So viewers know it's demo mode
3. **Focus on the ML/Analysis** - The sentiment analysis is the key feature
4. **Later**: Set up real data if you deploy this for production use

### Why Sample Data is OK for Learning:
- ✅ No API rate limits
- ✅ No authentication hassles  
- ✅ Consistent results for testing
- ✅ All features work identically
- ✅ Shows your technical skills regardless

---

## 🚀 Quick Setup for Real Data (Summary)

```bash
# 1. Install python-dotenv
pip install python-dotenv

# 2. Create .env in backend/
echo "TWITTER_USERNAME=your_username" > backend/.env
echo "TWITTER_EMAIL=your_email@example.com" >> backend/.env
echo "TWITTER_PASSWORD=your_password" >> backend/.env

# 3. Update scrape_tweets.py (copy code from above)

# 4. Restart backend
python backend/app.py
```

---

## ✅ What's Already Working

Your app is **production-ready** with sample data:
- ✨ Modern UI with animations
- 📊 Real sentiment analysis (VADER)
- 📈 Beautiful visualizations
- 💾 Data export functionality
- 🔍 Search and filter features
- 📱 Fully responsive design

**The only difference with real data would be the tweet content source!**

---

Need help setting up authentication? Let me know! 🚀
