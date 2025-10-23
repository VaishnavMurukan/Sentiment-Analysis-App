"""
Text Cleaning and Sentiment Analysis
Cleans tweet text and performs sentiment analysis using VADER
"""

import pandas as pd
import re
import string
import argparse
import os
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Download required NLTK data
def download_nltk_data():
    """Download required NLTK packages"""
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)


def clean_text(text):
    """
    Clean tweet text by removing URLs, mentions, hashtags, special characters
    
    Args:
        text: Raw tweet text
    
    Returns:
        Cleaned text string
    """
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtag symbol but keep the word
    text = re.sub(r'#', '', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def remove_stopwords(text):
    """
    Remove common stopwords from text
    
    Args:
        text: Cleaned text string
    
    Returns:
        Text with stopwords removed
    """
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    
    return ' '.join(filtered_words)


def analyze_sentiment(text):
    """
    Analyze sentiment using VADER
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with sentiment scores
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    
    # Classify sentiment based on compound score
    if scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'compound': scores['compound'],
        'positive': scores['pos'],
        'negative': scores['neg'],
        'neutral': scores['neu'],
        'sentiment': sentiment
    }


def process_tweets(input_file, output_file=None, remove_stops=False):
    """
    Process tweets: clean text and perform sentiment analysis
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (optional)
        remove_stops: Whether to remove stopwords
    
    Returns:
        Processed DataFrame
    """
    # Download NLTK data if needed
    download_nltk_data()
    
    # Read the data
    print(f"Reading tweets from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"Total tweets loaded: {len(df)}")
    
    if 'content' not in df.columns:
        print("Error: 'content' column not found in the CSV file")
        return None
    
    # Clean the text
    print("\nCleaning text...")
    df['cleaned_text'] = df['content'].apply(clean_text)
    
    # Optionally remove stopwords
    if remove_stops:
        print("Removing stopwords...")
        df['cleaned_text'] = df['cleaned_text'].apply(remove_stopwords)
    
    # Remove empty tweets after cleaning
    df = df[df['cleaned_text'].str.strip() != '']
    print(f"Tweets after cleaning: {len(df)}")
    
    # Perform sentiment analysis
    print("\nPerforming sentiment analysis...")
    sentiment_results = df['cleaned_text'].apply(analyze_sentiment)
    
    # Extract sentiment scores into separate columns
    df['sentiment_compound'] = sentiment_results.apply(lambda x: x['compound'])
    df['sentiment_positive'] = sentiment_results.apply(lambda x: x['positive'])
    df['sentiment_negative'] = sentiment_results.apply(lambda x: x['negative'])
    df['sentiment_neutral'] = sentiment_results.apply(lambda x: x['neutral'])
    df['sentiment'] = sentiment_results.apply(lambda x: x['sentiment'])
    
    # Print summary statistics
    print("\n" + "="*50)
    print("SENTIMENT ANALYSIS SUMMARY")
    print("="*50)
    print(f"\nSentiment Distribution:")
    print(df['sentiment'].value_counts())
    print(f"\nPercentages:")
    print(df['sentiment'].value_counts(normalize=True) * 100)
    print(f"\nAverage Compound Score: {df['sentiment_compound'].mean():.4f}")
    print(f"Median Compound Score: {df['sentiment_compound'].median():.4f}")
    print("="*50)
    
    # Save processed data
    if output_file:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nProcessed tweets saved to: {output_file}")
    
    return df


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Clean tweets and perform sentiment analysis')
    parser.add_argument('--input', type=str, required=True,
                        help='Input CSV file with tweets')
    parser.add_argument('--output', type=str, default=None,
                        help='Output CSV file (default: input_analyzed.csv)')
    parser.add_argument('--remove-stopwords', action='store_true',
                        help='Remove stopwords from text')
    
    args = parser.parse_args()
    
    # Set default output filename if not provided
    if args.output is None:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}_analyzed.csv"
    
    # Process tweets
    df = process_tweets(
        input_file=args.input,
        output_file=args.output,
        remove_stops=args.remove_stopwords
    )
    
    if df is not None:
        print("\n✓ Processing complete!")


if __name__ == "__main__":
    main()
