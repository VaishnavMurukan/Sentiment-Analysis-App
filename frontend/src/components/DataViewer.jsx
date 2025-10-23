import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Database, Download, ArrowLeft, Filter, Search } from 'lucide-react';
import API_URL from '../config';

export default function DataViewer() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSentiment, setFilterSentiment] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch(`${API_URL}/api/data`);
      if (!response.ok) {
        throw new Error('No data available. Please run an analysis first.');
      }
      const result = await response.json();
      setData(result);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!data) return;

    const headers = Object.keys(data.dataframe[0]);
    const csv = [
      headers.join(','),
      ...data.dataframe.map(row => 
        headers.map(header => `"${row[header] || ''}"`).join(',')
      )
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.topic.replace(/\s+/g, '_')}_analysis_data.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const getFilteredData = () => {
    if (!data) return [];

    let filtered = [...data.dataframe];

    // Filter by sentiment
    if (filterSentiment !== 'all') {
      filtered = filtered.filter(item => item.sentiment === filterSentiment);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.content?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.cleaned_text?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.username?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Sort data
    filtered.sort((a, b) => {
      if (sortBy === 'date') {
        return new Date(b.date) - new Date(a.date);
      } else if (sortBy === 'sentiment_score') {
        return b.sentiment_compound - a.sentiment_compound;
      } else if (sortBy === 'likes') {
        return b.like_count - a.like_count;
      }
      return 0;
    });

    return filtered;
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'negative':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'neutral':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-effect rounded-2xl p-8 max-w-md text-center">
          <p className="text-red-600 text-lg mb-4">⚠️ {error}</p>
          <button
            onClick={() => window.location.href = '/'}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
          >
            Go Back to Analysis
          </button>
        </div>
      </div>
    );
  }

  const filteredData = getFilteredData();

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <button
                onClick={() => window.history.back()}
                className="p-3 glass-effect rounded-xl hover:bg-white/90 transition-all"
              >
                <ArrowLeft className="h-6 w-6 text-gray-700" />
              </button>
              <div>
                <h1 className="text-4xl font-bold gradient-text mb-2">
                  Analysis Data Viewer
                </h1>
                <p className="text-gray-600">
                  Topic: <span className="font-semibold">{data.topic}</span> | 
                  Total Records: <span className="font-semibold">{data.dataframe.length}</span> | 
                  Analyzed: <span className="font-semibold">{new Date(data.timestamp).toLocaleString()}</span>
                </p>
              </div>
            </div>

            <button
              onClick={downloadCSV}
              className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors shadow-lg"
            >
              <Download className="h-5 w-5" />
              Download CSV
            </button>
          </div>

          {/* Filters */}
          <div className="glass-effect rounded-xl p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Search */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Search className="inline h-4 w-4 mr-1" />
                  Search
                </label>
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search tweets..."
                  className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                />
              </div>

              {/* Filter by Sentiment */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <Filter className="inline h-4 w-4 mr-1" />
                  Filter by Sentiment
                </label>
                <select
                  value={filterSentiment}
                  onChange={(e) => setFilterSentiment(e.target.value)}
                  className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                >
                  <option value="all">All Sentiments</option>
                  <option value="positive">Positive</option>
                  <option value="neutral">Neutral</option>
                  <option value="negative">Negative</option>
                </select>
              </div>

              {/* Sort By */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By
                </label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-4 py-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-blue-500"
                >
                  <option value="date">Date (Newest First)</option>
                  <option value="sentiment_score">Sentiment Score</option>
                  <option value="likes">Most Liked</option>
                </select>
              </div>
            </div>

            <div className="mt-4 text-sm text-gray-600">
              Showing {filteredData.length} of {data.dataframe.length} records
            </div>
          </div>
        </motion.div>

        {/* Data Table */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-effect rounded-xl p-6 overflow-x-auto"
        >
          <div className="space-y-4">
            {filteredData.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.03 }}
                className="bg-white rounded-lg p-4 border-2 border-gray-200 hover:border-blue-300 transition-all"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-semibold text-gray-900">@{item.username}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold border-2 ${getSentimentColor(item.sentiment)}`}>
                        {item.sentiment?.toUpperCase()}
                      </span>
                      <span className="text-xs text-gray-500">
                        {new Date(item.date).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="text-gray-700 mb-2">{item.content}</p>
                    {item.cleaned_text && (
                      <p className="text-sm text-gray-500 italic">
                        Cleaned: {item.cleaned_text}
                      </p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-600">Score:</span>
                    <span className={`font-bold ${item.sentiment_compound >= 0.05 ? 'text-green-600' : item.sentiment_compound <= -0.05 ? 'text-red-600' : 'text-gray-600'}`}>
                      {item.sentiment_compound?.toFixed(3)}
                    </span>
                  </div>
                  <div className="text-gray-500">❤️ {item.like_count}</div>
                  <div className="text-gray-500">🔁 {item.retweet_count}</div>
                  <div className="text-gray-500">💬 {item.reply_count}</div>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredData.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No data matches your filters</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
