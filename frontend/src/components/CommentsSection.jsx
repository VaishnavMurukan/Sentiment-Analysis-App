import { motion } from 'framer-motion';
import { MessageSquare, Heart, Repeat2 } from 'lucide-react';

export default function CommentsSection({ comments }) {
  const sentimentTypes = ['positive', 'negative', 'neutral'];
  
  const sentimentColors = {
    positive: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      text: 'text-green-600',
      icon: 'bg-green-100',
    },
    negative: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-600',
      icon: 'bg-red-100',
    },
    neutral: {
      bg: 'bg-gray-50',
      border: 'border-gray-200',
      text: 'text-gray-600',
      icon: 'bg-gray-100',
    },
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-effect rounded-2xl p-8"
    >
      <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
        <MessageSquare className="h-8 w-8 text-blue-600" />
        Top Comments by Sentiment
      </h2>

      <div className="space-y-8">
        {sentimentTypes.map((type, sectionIndex) => (
          <div key={type}>
            <h3 className={`text-xl font-semibold capitalize mb-4 ${sentimentColors[type].text}`}>
              {type} Tweets
            </h3>
            
            <div className="space-y-3">
              {comments[type]?.slice(0, 5).map((comment, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: sectionIndex * 0.1 + index * 0.05 }}
                  className={`p-4 rounded-xl border-2 ${sentimentColors[type].bg} ${sentimentColors[type].border} hover:shadow-md transition-shadow`}
                >
                  <p className="text-gray-700 mb-3">{comment.text}</p>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium text-gray-600">
                      @{comment.username}
                    </span>
                    
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-1 text-gray-500">
                        <Heart className="h-4 w-4" />
                        <span>{comment.likes}</span>
                      </div>
                      <div className="flex items-center gap-1 text-gray-500">
                        <Repeat2 className="h-4 w-4" />
                        <span>{comment.retweets}</span>
                      </div>
                      <div className={`px-2 py-1 rounded-full text-xs font-semibold ${sentimentColors[type].icon} ${sentimentColors[type].text}`}>
                        Score: {comment.sentiment_score.toFixed(2)}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
              
              {(!comments[type] || comments[type].length === 0) && (
                <p className="text-gray-400 italic text-center py-4">
                  No {type} tweets found
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
