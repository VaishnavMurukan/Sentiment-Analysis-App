import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Sparkles } from 'lucide-react';

const sampleTopics = [
  'Artificial Intelligence',
  'Climate Change',
  'Cryptocurrency',
  'Electric Vehicles',
  'Mental Health',
];

export default function SearchForm({ onAnalyze, loading }) {
  const [topic, setTopic] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (topic.trim()) {
      onAnalyze(topic);
    }
  };

  const handleSampleTopic = (sampleTopic) => {
    setTopic(sampleTopic);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-effect rounded-2xl p-8 max-w-3xl mx-auto"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Search className="h-6 w-6 text-gray-400" />
          </div>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a topic to analyze... (e.g., AI, movies, politics)"
            className="w-full pl-14 pr-4 py-4 text-lg border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all"
            disabled={loading}
          />
        </div>

        <motion.button
          type="submit"
          disabled={loading || !topic.trim()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <Sparkles className="h-5 w-5" />
          {loading ? 'Analyzing...' : 'Analyze Sentiment'}
        </motion.button>
      </form>

      {/* Sample Topics */}
      <div className="mt-6">
        <p className="text-sm text-gray-600 mb-3">Try these topics:</p>
        <div className="flex flex-wrap gap-2">
          {sampleTopics.map((sampleTopic) => (
            <motion.button
              key={sampleTopic}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleSampleTopic(sampleTopic)}
              className="px-4 py-2 bg-white border-2 border-gray-200 rounded-full text-sm font-medium text-gray-700 hover:border-blue-400 hover:text-blue-600 transition-all"
              disabled={loading}
            >
              {sampleTopic}
            </motion.button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
