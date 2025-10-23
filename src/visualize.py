"""
Visualization of Sentiment Analysis Results
Creates various charts and visualizations for tweet sentiment data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import argparse
import os
from datetime import datetime


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def create_sentiment_distribution(df, output_dir='plots'):
    """
    Create bar chart of sentiment distribution
    
    Args:
        df: DataFrame with sentiment analysis results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(10, 6))
    
    # Count sentiments
    sentiment_counts = df['sentiment'].value_counts()
    colors = {'positive': '#2ecc71', 'neutral': '#95a5a6', 'negative': '#e74c3c'}
    bar_colors = [colors.get(sent, '#3498db') for sent in sentiment_counts.index]
    
    # Create bar chart
    ax = sentiment_counts.plot(kind='bar', color=bar_colors, edgecolor='black', linewidth=1.2)
    plt.title('Sentiment Distribution', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Sentiment', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Tweets', fontsize=12, fontweight='bold')
    plt.xticks(rotation=0)
    
    # Add value labels on bars
    for i, v in enumerate(sentiment_counts):
        ax.text(i, v + max(sentiment_counts) * 0.01, str(v), 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'sentiment_distribution.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def create_sentiment_pie_chart(df, output_dir='plots'):
    """
    Create pie chart of sentiment percentages
    
    Args:
        df: DataFrame with sentiment analysis results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(10, 8))
    
    sentiment_counts = df['sentiment'].value_counts()
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']
    explode = (0.05, 0, 0)  # Explode the first slice
    
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
            colors=colors, explode=explode, shadow=True, startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    plt.title('Sentiment Distribution (%)', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'sentiment_pie_chart.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def create_compound_score_distribution(df, output_dir='plots'):
    """
    Create histogram of compound sentiment scores
    
    Args:
        df: DataFrame with sentiment analysis results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(12, 6))
    
    # Create histogram
    plt.hist(df['sentiment_compound'], bins=30, color='#3498db', 
             edgecolor='black', alpha=0.7)
    
    # Add vertical lines for sentiment thresholds
    plt.axvline(x=0.05, color='#2ecc71', linestyle='--', linewidth=2, label='Positive Threshold')
    plt.axvline(x=-0.05, color='#e74c3c', linestyle='--', linewidth=2, label='Negative Threshold')
    plt.axvline(x=df['sentiment_compound'].mean(), color='orange', 
                linestyle='-', linewidth=2, label=f'Mean: {df["sentiment_compound"].mean():.3f}')
    
    plt.title('Distribution of Compound Sentiment Scores', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Compound Score', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'compound_score_distribution.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def create_sentiment_timeline(df, output_dir='plots'):
    """
    Create timeline showing sentiment over time
    
    Args:
        df: DataFrame with sentiment analysis results
        output_dir: Directory to save plots
    """
    if 'date' not in df.columns:
        print("⚠ Warning: 'date' column not found. Skipping timeline visualization.")
        return
    
    try:
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Group by date and sentiment
        daily_sentiment = df.groupby([df['date'].dt.date, 'sentiment']).size().unstack(fill_value=0)
        
        plt.figure(figsize=(14, 6))
        
        # Plot stacked area chart
        colors = {'positive': '#2ecc71', 'neutral': '#95a5a6', 'negative': '#e74c3c'}
        daily_sentiment.plot(kind='area', stacked=True, 
                            color=[colors.get(col, '#3498db') for col in daily_sentiment.columns],
                            alpha=0.7)
        
        plt.title('Sentiment Timeline', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Tweets', fontsize=12, fontweight='bold')
        plt.legend(title='Sentiment', fontsize=10)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, 'sentiment_timeline.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filepath}")
        plt.close()
    
    except Exception as e:
        print(f"⚠ Warning: Could not create timeline visualization. Error: {e}")


def create_wordcloud(df, sentiment=None, output_dir='plots'):
    """
    Create word cloud from tweet text
    
    Args:
        df: DataFrame with sentiment analysis results
        sentiment: Filter by sentiment ('positive', 'negative', 'neutral', or None for all)
        output_dir: Directory to save plots
    """
    if 'cleaned_text' not in df.columns:
        print("⚠ Warning: 'cleaned_text' column not found. Skipping word cloud.")
        return
    
    # Filter by sentiment if specified
    if sentiment:
        df_filtered = df[df['sentiment'] == sentiment]
        title = f'Word Cloud - {sentiment.capitalize()} Tweets'
        filename = f'wordcloud_{sentiment}.png'
    else:
        df_filtered = df
        title = 'Word Cloud - All Tweets'
        filename = 'wordcloud_all.png'
    
    if df_filtered.empty:
        print(f"⚠ Warning: No tweets found for sentiment: {sentiment}")
        return
    
    # Combine all text
    text = ' '.join(df_filtered['cleaned_text'].astype(str))
    
    if not text.strip():
        print(f"⚠ Warning: No text content found for word cloud")
        return
    
    # Create word cloud
    plt.figure(figsize=(14, 8))
    
    wordcloud = WordCloud(width=1200, height=600, 
                         background_color='white',
                         colormap='viridis',
                         max_words=100,
                         relative_scaling=0.5,
                         min_font_size=10).generate(text)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def create_sentiment_score_boxplot(df, output_dir='plots'):
    """
    Create box plot showing distribution of sentiment scores
    
    Args:
        df: DataFrame with sentiment analysis results
        output_dir: Directory to save plots
    """
    plt.figure(figsize=(12, 6))
    
    # Prepare data for boxplot
    data_to_plot = [
        df[df['sentiment'] == 'positive']['sentiment_compound'],
        df[df['sentiment'] == 'neutral']['sentiment_compound'],
        df[df['sentiment'] == 'negative']['sentiment_compound']
    ]
    
    box = plt.boxplot(data_to_plot, labels=['Positive', 'Neutral', 'Negative'],
                      patch_artist=True, showmeans=True)
    
    # Color the boxes
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.title('Sentiment Score Distribution by Category', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Sentiment Category', fontsize=12, fontweight='bold')
    plt.ylabel('Compound Score', fontsize=12, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, 'sentiment_boxplot.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")
    plt.close()


def visualize_all(input_file, output_dir='plots'):
    """
    Create all visualizations
    
    Args:
        input_file: Path to analyzed tweets CSV
        output_dir: Directory to save plots
    """
    print(f"Reading analyzed tweets from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"Total tweets: {len(df)}")
    
    print("\nCreating visualizations...\n")
    
    # Create all visualizations
    create_sentiment_distribution(df, output_dir)
    create_sentiment_pie_chart(df, output_dir)
    create_compound_score_distribution(df, output_dir)
    create_sentiment_timeline(df, output_dir)
    create_sentiment_score_boxplot(df, output_dir)
    
    # Create word clouds
    create_wordcloud(df, sentiment=None, output_dir=output_dir)
    create_wordcloud(df, sentiment='positive', output_dir=output_dir)
    create_wordcloud(df, sentiment='negative', output_dir=output_dir)
    
    print(f"\n{'='*50}")
    print("✓ All visualizations created successfully!")
    print(f"{'='*50}")
    print(f"Output directory: {os.path.abspath(output_dir)}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Visualize sentiment analysis results')
    parser.add_argument('--input', type=str, required=True,
                        help='Input CSV file with analyzed tweets')
    parser.add_argument('--output-dir', type=str, default='plots',
                        help='Output directory for plots (default: plots)')
    
    args = parser.parse_args()
    
    visualize_all(args.input, args.output_dir)


if __name__ == "__main__":
    main()
