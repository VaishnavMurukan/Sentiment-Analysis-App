"""
Flask Backend for Sentiment Analysis Web App
Provides API endpoints for sentiment analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import pandas as pd
import random

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scrape_tweets import scrape_tweets
from clean_and_analyze import clean_text, analyze_sentiment, download_nltk_data

app = Flask(__name__)
# Enable CORS for all origins (change to specific domain in production)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Download NLTK data on startup
download_nltk_data()

# Store the last analysis data in memory
last_analysis_data = None


def get_top_comments(df, sentiment, n=5):
    """Get top N comments for a specific sentiment"""
    filtered = df[df['sentiment'] == sentiment]
    if filtered.empty:
        return []
    
    # Sort by engagement (like + retweet count)
    filtered['engagement'] = filtered['like_count'] + filtered['retweet_count']
    top = filtered.nlargest(n, 'engagement')
    
    return [
        {
            'text': row['content'],
            'username': row['username'],
            'likes': int(row['like_count']),
            'retweets': int(row['retweet_count']),
            'sentiment_score': float(row['sentiment_compound'])
        }
        for _, row in top.iterrows()
    ]


def generate_suggestions(topic, sentiment_data):
    """Generate topic suggestions based on sentiment analysis"""
    suggestions = {
        'positive': [
            f"Explore success stories about {topic}",
            f"Learn best practices in {topic}",
            f"Join communities discussing {topic}",
            f"Discover innovations in {topic}",
            f"Follow thought leaders in {topic}"
        ],
        'negative': [
            f"Understand challenges in {topic}",
            f"Research solutions for {topic} issues",
            f"Read critical analysis of {topic}",
            f"Explore alternative approaches to {topic}",
            f"Stay informed about {topic} controversies"
        ],
        'neutral': [
            f"Get comprehensive overview of {topic}",
            f"Compare different perspectives on {topic}",
            f"Read factual information about {topic}",
            f"Study the evolution of {topic}",
            f"Analyze trends in {topic}"
        ]
    }
    
    # Determine dominant sentiment
    max_sentiment = max(sentiment_data['distribution'], key=sentiment_data['distribution'].get)
    
    # Return mix of suggestions
    all_suggestions = []
    all_suggestions.extend(random.sample(suggestions['positive'], 2))
    all_suggestions.extend(random.sample(suggestions['negative'], 2))
    all_suggestions.extend(random.sample(suggestions['neutral'], 1))
    
    random.shuffle(all_suggestions)
    return all_suggestions[:5]


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Sentiment Analysis API is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_topic():
    """
    Main endpoint for sentiment analysis
    Expects JSON: {"topic": "AI", "max_tweets": 500}
    """
    global last_analysis_data
    
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        max_tweets = data.get('max_tweets', 500)
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        print(f"\n{'='*50}")
        print(f"Analyzing topic: {topic}")
        print(f"Max tweets: {max_tweets}")
        print(f"{'='*50}\n")
        
        # Step 1: Scrape tweets
        print("Step 1: Scraping tweets...")
        df = scrape_tweets(topic, max_tweets=max_tweets)
        
        if df.empty:
            return jsonify({'error': 'No tweets found for this topic'}), 404
        
        # Step 2: Clean and analyze
        print("\nStep 2: Cleaning and analyzing...")
        df['cleaned_text'] = df['content'].apply(clean_text)
        df = df[df['cleaned_text'].str.strip() != '']
        
        sentiment_results = df['cleaned_text'].apply(analyze_sentiment)
        df['sentiment_compound'] = sentiment_results.apply(lambda x: x['compound'])
        df['sentiment_positive'] = sentiment_results.apply(lambda x: x['positive'])
        df['sentiment_negative'] = sentiment_results.apply(lambda x: x['negative'])
        df['sentiment_neutral'] = sentiment_results.apply(lambda x: x['neutral'])
        df['sentiment'] = sentiment_results.apply(lambda x: x['sentiment'])
        
        # Step 3: Prepare response
        print("\nStep 3: Preparing response...")
        
        sentiment_counts = df['sentiment'].value_counts().to_dict()
        total_tweets = len(df)
        
        response = {
            'topic': topic,
            'total_tweets': total_tweets,
            'sentiment_summary': {
                'average_score': float(df['sentiment_compound'].mean()),
                'median_score': float(df['sentiment_compound'].median()),
            },
            'distribution': {
                'positive': sentiment_counts.get('positive', 0),
                'negative': sentiment_counts.get('negative', 0),
                'neutral': sentiment_counts.get('neutral', 0)
            },
            'percentages': {
                'positive': round((sentiment_counts.get('positive', 0) / total_tweets) * 100, 1),
                'negative': round((sentiment_counts.get('negative', 0) / total_tweets) * 100, 1),
                'neutral': round((sentiment_counts.get('neutral', 0) / total_tweets) * 100, 1)
            },
            'timeline_data': []
        }
        
        # Add timeline data if date column exists
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
                daily_sentiment = df.groupby([df['date'].dt.date, 'sentiment']).size().unstack(fill_value=0)
                timeline_data = []
                for date, row in daily_sentiment.iterrows():
                    timeline_data.append({
                        'date': str(date),
                        'positive': int(row.get('positive', 0)),
                        'negative': int(row.get('negative', 0)),
                        'neutral': int(row.get('neutral', 0))
                    })
                response['timeline_data'] = timeline_data
            except Exception as e:
                print(f"Warning: Could not generate timeline data: {e}")
        
        print("\n✓ Analysis complete!")
        
        # Store the DataFrame for later retrieval
        last_analysis_data = {
            'topic': topic,
            'dataframe': df.to_dict('records'),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/data', methods=['GET'])
def get_analysis_data():
    """
    Get the full dataset from the last analysis
    """
    global last_analysis_data
    
    if last_analysis_data is None:
        return jsonify({'error': 'No analysis data available. Please run an analysis first.'}), 404
    
    return jsonify(last_analysis_data)


@app.route('/api/topics', methods=['GET'])
def get_sample_topics():
    """Get sample topics for suggestions"""
    topics = [
        {"name": "Artificial Intelligence", "icon": "🤖"},
        {"name": "Climate Change", "icon": "🌍"},
        {"name": "Cryptocurrency", "icon": "💰"},
        {"name": "Electric Vehicles", "icon": "🚗"},
        {"name": "Space Exploration", "icon": "🚀"},
        {"name": "Mental Health", "icon": "🧠"},
        {"name": "Remote Work", "icon": "💼"},
        {"name": "Education", "icon": "📚"}
    ]
    return jsonify(topics)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Sentiment Analysis API Server")
    print("="*50)
    print("Server running on: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')
