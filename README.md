# Social Media Sentiment Analysis
https://sentiment-analysis-app-ten.vercel.app/

A complete pipeline for scraping tweets, performing sentiment analysis, and visualizing results using Python.

## 🎯 Project Overview

This project demonstrates a full data science workflow for social media sentiment analysis:

1. **Data Collection**: Scrape tweets using `snscrape`
2. **Data Cleaning**: Clean and preprocess tweet text
3. **Sentiment Analysis**: Analyze sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
4. **Visualization**: Create comprehensive visualizations of sentiment patterns

## 📋 Features

- ✅ Scrape tweets by keyword, hashtag, or username
- ✅ Filter tweets by date range
- ✅ Clean text (remove URLs, mentions, special characters)
- ✅ Sentiment classification (positive, negative, neutral)
- ✅ Multiple visualizations:
  - Sentiment distribution bar chart and pie chart
  - Compound score histogram and box plots
  - Sentiment timeline
  - Word clouds (overall and by sentiment)

## 🚀 Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone or navigate to the project directory:
```bash
cd c:\Users\vaish\internship\day1
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (will be done automatically on first run):
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

## 📖 Usage

### Step 1: Scrape Tweets

Scrape tweets using a search query:

```bash
python src/scrape_tweets.py --query "climate change" --max-tweets 1000 --output tweets.csv
```

**Options:**
- `--query`: Search term (required) - can be keywords, hashtags, or usernames
- `--max-tweets`: Maximum number of tweets to scrape (default: 1000)
- `--since`: Start date in YYYY-MM-DD format
- `--until`: End date in YYYY-MM-DD format
- `--output`: Output filename (default: tweets.csv)
- `--output-dir`: Output directory (default: data)

**Examples:**
```bash
# Scrape tweets about AI
python src/scrape_tweets.py --query "artificial intelligence" --max-tweets 500

# Scrape tweets with hashtag for a date range
python src/scrape_tweets.py --query "#Python" --since 2024-01-01 --until 2024-12-31 --max-tweets 2000

# Scrape tweets from a user
python src/scrape_tweets.py --query "from:elonmusk" --max-tweets 100
```

### Step 2: Clean and Analyze

Clean tweet text and perform sentiment analysis:

```bash
python src/clean_and_analyze.py --input data/tweets.csv --output data/tweets_analyzed.csv
```

**Options:**
- `--input`: Input CSV file (required)
- `--output`: Output CSV file (default: input_analyzed.csv)
- `--remove-stopwords`: Remove common stopwords

**Example:**
```bash
python src/clean_and_analyze.py --input data/tweets.csv --output data/tweets_analyzed.csv --remove-stopwords
```

### Step 3: Visualize Results

Create visualizations from analyzed data:

```bash
python src/visualize.py --input data/tweets_analyzed.csv --output-dir plots
```

**Options:**
- `--input`: Input CSV with analyzed tweets (required)
- `--output-dir`: Directory for saving plots (default: plots)

## 📊 Output Files

### CSV Files (in `data/` directory)

1. **tweets.csv**: Raw scraped tweets with columns:
   - date, id, content, username
   - like_count, retweet_count, reply_count
   - language, source, url

2. **tweets_analyzed.csv**: Processed tweets with additional columns:
   - cleaned_text
   - sentiment_compound (score from -1 to +1)
   - sentiment_positive, sentiment_negative, sentiment_neutral
   - sentiment (classification: positive/negative/neutral)

### Visualizations (in `plots/` directory)

1. **sentiment_distribution.png**: Bar chart of sentiment counts
2. **sentiment_pie_chart.png**: Percentage breakdown of sentiments
3. **compound_score_distribution.png**: Histogram of sentiment scores
4. **sentiment_timeline.png**: Sentiment trends over time
5. **sentiment_boxplot.png**: Box plots by sentiment category
6. **wordcloud_all.png**: Word cloud from all tweets
7. **wordcloud_positive.png**: Word cloud from positive tweets
8. **wordcloud_negative.png**: Word cloud from negative tweets

## 🧪 Testing

Run the smoke test to verify the installation:

```bash
python tests/smoke_test.py
```

## 🔧 Project Structure

```
day1/
│
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
│
├── src/
│   ├── scrape_tweets.py        # Tweet scraping module
│   ├── clean_and_analyze.py    # Text cleaning and sentiment analysis
│   └── visualize.py            # Visualization generation
│
├── tests/
│   └── smoke_test.py           # Basic functionality tests
│
├── data/                        # Output directory for CSV files
└── plots/                       # Output directory for visualizations
```

## 📚 Libraries Used

- **snscrape**: Twitter scraping without API limits
- **pandas**: Data manipulation and analysis
- **nltk**: Natural language processing
- **vaderSentiment**: Sentiment analysis specifically tuned for social media
- **matplotlib & seaborn**: Data visualization
- **wordcloud**: Word cloud generation

## 💡 VADER Sentiment Scoring

VADER provides a compound score from -1 (most negative) to +1 (most positive):

- **Positive**: compound score >= 0.05
- **Neutral**: -0.05 < compound score < 0.05
- **Negative**: compound score <= -0.05

## 🤝 Tips

1. **Start small**: Test with 100-500 tweets first
2. **Be specific**: Use specific keywords or hashtags for better results
3. **Date ranges**: Narrow date ranges for focused analysis
4. **Stopwords**: Use `--remove-stopwords` for cleaner word clouds
5. **Rate limiting**: snscrape has no rate limits, but be reasonable

## 📝 Example Workflow

Complete analysis in three commands:

```bash
# 1. Scrape tweets about Python programming
python src/scrape_tweets.py --query "#Python OR #Programming" --max-tweets 1000

# 2. Clean and analyze
python src/clean_and_analyze.py --input data/tweets.csv --remove-stopwords

# 3. Create visualizations
python src/visualize.py --input data/tweets_analyzed.csv
```

## ⚠️ Notes

- Twitter/X content is subject to their Terms of Service
- Scraped data is for educational/research purposes
- VADER works best with social media text (emojis, slang, etc.)
- Large datasets may take time to process

## 🐛 Troubleshooting

**Issue**: snscrape not finding tweets
- **Solution**: Try more recent dates or popular keywords

**Issue**: NLTK data not found
- **Solution**: Manually download: `python -m nltk.downloader stopwords punkt`

**Issue**: Empty word clouds
- **Solution**: Check if cleaned_text column has content; avoid aggressive filtering

## 📄 License

This project is for educational purposes.

## 🌐 Web Application

A modern React-based web application with Flask backend is now available!

### Quick Start

**Option 1: Use the startup script (Windows)**
```bash
# Double-click start.bat or run:
start.bat
```

**Option 2: Manual start**

Terminal 1 - Backend:
```bash
cd backend
python app.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Then open: `http://localhost:5173`

### Web App Features

✨ **Modern UI** with TailwindCSS and glassmorphism design
🎬 **Smooth Animations** using Framer Motion
📊 **Interactive Charts** (Bar, Pie, Line charts)
💬 **Top Comments** display for each sentiment
💡 **Smart Suggestions** based on sentiment analysis
📱 **Fully Responsive** design

For detailed web app documentation, see [WEBAPP_README.md](WEBAPP_README.md)

## 👨‍💻 Author

Created as part of data science internship - Day 1 project

---

**Happy Analyzing! 📊✨**
