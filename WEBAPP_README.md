# Sentiment Analysis Web App - Quick Start Guide

## 🚀 Quick Start

### 1. Start the Backend Server (Terminal 1)

```powershell
# Navigate to backend directory
cd backend

# Install dependencies (first time only)
python -m pip install -r requirements.txt

# Start Flask server
python app.py
```

The backend will run on: `http://localhost:5000`

### 2. Start the Frontend (Terminal 2)

```powershell
# Navigate to frontend directory
cd frontend

# Start development server
npm run dev
```

The frontend will run on: `http://localhost:5173`

### 3. Use the App

1. Open your browser to `http://localhost:5173`
2. Enter a topic (e.g., "Artificial Intelligence", "Climate Change")
3. Click "Analyze Sentiment"
4. View the results with beautiful animations!

## 📦 What's Included

### Backend (Flask)
- `/api/analyze` - Main sentiment analysis endpoint
- `/api/health` - Health check endpoint
- `/api/topics` - Sample topics suggestions

### Frontend (React)
- Modern UI with TailwindCSS
- Smooth animations with Framer Motion
- Interactive charts with Recharts
- Responsive design
- Real-time sentiment analysis

## 🎨 Features

✅ **Beautiful UI** - Modern glassmorphism design
✅ **Smooth Animations** - Framer Motion transitions
✅ **Interactive Charts** - Bar, Pie, and Line charts
✅ **Top Comments** - See top 5 tweets per sentiment
✅ **Smart Suggestions** - Get related topic suggestions
✅ **Responsive** - Works on all devices

## 🛠️ Tech Stack

**Frontend:**
- React + Vite
- TailwindCSS
- Framer Motion
- Recharts
- Lucide Icons
- Axios

**Backend:**
- Flask
- VADER Sentiment
- Pandas
- NLTK

## 📝 API Reference

### POST /api/analyze
Analyzes sentiment for a given topic.

**Request Body:**
```json
{
  "topic": "Artificial Intelligence",
  "max_tweets": 500
}
```

**Response:**
```json
{
  "topic": "Artificial Intelligence",
  "total_tweets": 500,
  "sentiment_summary": {
    "average_score": 0.0619,
    "median_score": 0.0
  },
  "distribution": {
    "positive": 200,
    "negative": 150,
    "neutral": 150
  },
  "percentages": {
    "positive": 40.0,
    "negative": 30.0,
    "neutral": 30.0
  },
  "top_comments": {
    "positive": [...],
    "negative": [...],
    "neutral": [...]
  },
  "suggestions": [...],
  "timeline_data": [...]
}
```

## 🐛 Troubleshooting

**Backend not starting?**
- Make sure Python 3.7+ is installed
- Install dependencies: `python -m pip install -r backend/requirements.txt`

**Frontend not starting?**
- Make sure Node.js is installed
- Run `npm install` in frontend directory

**CORS errors?**
- Make sure backend is running on port 5000
- Check that flask-cors is installed

**Blank page?**
- Check browser console for errors
- Make sure both servers are running

## 🎯 Usage Tips

1. **Try different topics** - The app works with any topic!
2. **Wait for results** - Analysis may take 10-30 seconds
3. **Explore charts** - Hover over elements for more details
4. **Check suggestions** - Get ideas for related topics to explore

## 📸 Screenshots

The app features:
- Clean search interface with sample topics
- Animated sentiment cards with percentages
- Interactive charts and visualizations
- Top comments for each sentiment category
- Smart suggestions based on analysis

Enjoy exploring sentiments! 🎉
