import { motion } from 'framer-motion';
import { Smile, Frown, Minus } from 'lucide-react';

export default function SentimentCards({ data }) {
  const sentiments = [
    {
      type: 'positive',
      icon: Smile,
      color: 'from-green-400 to-emerald-500',
      bgColor: 'bg-green-50',
      textColor: 'text-green-600',
      count: data.distribution.positive,
      percentage: data.percentages.positive,
    },
    {
      type: 'neutral',
      icon: Minus,
      color: 'from-gray-400 to-slate-500',
      bgColor: 'bg-gray-50',
      textColor: 'text-gray-600',
      count: data.distribution.neutral,
      percentage: data.percentages.neutral,
    },
    {
      type: 'negative',
      icon: Frown,
      color: 'from-red-400 to-rose-500',
      bgColor: 'bg-red-50',
      textColor: 'text-red-600',
      count: data.distribution.negative,
      percentage: data.percentages.negative,
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {sentiments.map((sentiment, index) => (
        <motion.div
          key={sentiment.type}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="sentiment-card"
        >
          <div className="flex items-center justify-between mb-4">
            <div className={`p-3 rounded-xl bg-gradient-to-br ${sentiment.color}`}>
              <sentiment.icon className="h-8 w-8 text-white" />
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-gray-800">{sentiment.count}</p>
              <p className="text-sm text-gray-500">tweets</p>
            </div>
          </div>
          
          <h3 className={`text-xl font-semibold capitalize mb-2 ${sentiment.textColor}`}>
            {sentiment.type}
          </h3>
          
          <div className="flex items-center gap-2">
            <div className="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${sentiment.percentage}%` }}
                transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                className={`h-full bg-gradient-to-r ${sentiment.color}`}
              />
            </div>
            <span className={`text-lg font-bold ${sentiment.textColor}`}>
              {sentiment.percentage}%
            </span>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
