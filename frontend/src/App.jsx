import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import SearchForm from './components/SearchForm';
import SentimentCards from './components/SentimentCards';
import ChartSection from './components/ChartSection';
import LoadingAnimation from './components/LoadingAnimation';
import './index.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (topic) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, max_tweets: 500 }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze sentiment');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Demo Mode Banner */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-300 rounded-xl p-4"
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">ℹ️</span>
            <div>
              <p className="font-semibold text-yellow-800">Demo Mode - Sample Data</p>
              <p className="text-sm text-yellow-700">
                Currently using AI-generated sample tweets for demonstration. 
                To use real Twitter data, authentication is required.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-6xl font-bold gradient-text mb-4">
            Sentiment Analysis
          </h1>
          <p className="text-gray-600 text-lg">
            Discover what people are saying about any topic in real-time
          </p>
        </motion.div>

        {/* Search Form */}
        <SearchForm onAnalyze={handleAnalyze} loading={loading} />

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-effect rounded-xl p-6 text-center text-red-600 mt-8"
          >
            <p className="text-lg font-semibold">⚠️ {error}</p>
          </motion.div>
        )}

        {/* Loading Animation */}
        {loading && <LoadingAnimation />}

        {/* Results */}
        <AnimatePresence mode="wait">
          {results && !loading && (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-8 mt-12"
            >
              {/* Topic Header */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
              >
                <h2 className="text-4xl font-bold text-gray-800 mb-2">
                  Results for: <span className="gradient-text">{results.topic}</span>
                </h2>
                <p className="text-gray-600">
                  Analyzed {results.total_tweets} tweets
                </p>
              </motion.div>

              {/* Sentiment Cards */}
              <SentimentCards data={results} />

              {/* Chart Section */}
              {results.timeline_data && results.timeline_data.length > 0 && (
                <ChartSection data={results} />
              )}

              {/* View Data Button */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center mt-8"
              >
                <button
                  onClick={() => window.location.href = '/data'}
                  className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                  </svg>
                  View Full Analysis Data ({results.total_tweets} tweets)
                </button>
                <p className="text-gray-500 text-sm mt-3">
                  Browse, filter, and download the complete dataset
                </p>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
