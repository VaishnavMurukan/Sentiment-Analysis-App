import { motion } from 'framer-motion';
import { Lightbulb, ArrowRight } from 'lucide-react';

export default function SuggestionsSection({ suggestions }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-effect rounded-2xl p-8"
    >
      <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
        <Lightbulb className="h-8 w-8 text-yellow-500" />
        Suggestions & Insights
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {suggestions?.map((suggestion, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            className="p-4 bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-xl hover:shadow-lg transition-all cursor-pointer group"
          >
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center text-white font-bold">
                {index + 1}
              </div>
              <div className="flex-1">
                <p className="text-gray-700 group-hover:text-gray-900 transition-colors">
                  {suggestion}
                </p>
              </div>
              <ArrowRight className="h-5 w-5 text-yellow-600 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
