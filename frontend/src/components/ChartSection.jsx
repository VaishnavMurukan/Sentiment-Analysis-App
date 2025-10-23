import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { TrendingUp } from 'lucide-react';

const COLORS = {
  positive: '#10b981',
  negative: '#ef4444',
  neutral: '#6b7280',
};

export default function ChartSection({ data }) {
  const pieData = [
    { name: 'Positive', value: data.distribution.positive },
    { name: 'Neutral', value: data.distribution.neutral },
    { name: 'Negative', value: data.distribution.negative },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-effect rounded-2xl p-8"
    >
      <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-3">
        <TrendingUp className="h-8 w-8 text-purple-600" />
        Data Visualization
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Bar Chart */}
        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-4">
            Sentiment Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[data.distribution]}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="positive" fill={COLORS.positive} radius={[8, 8, 0, 0]} />
              <Bar dataKey="neutral" fill={COLORS.neutral} radius={[8, 8, 0, 0]} />
              <Bar dataKey="negative" fill={COLORS.negative} radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pie Chart */}
        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-4">
            Sentiment Breakdown
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name.toLowerCase()]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Timeline Chart */}
        {data.timeline_data && data.timeline_data.length > 0 && (
          <div className="lg:col-span-2">
            <h3 className="text-xl font-semibold text-gray-700 mb-4">
              Sentiment Timeline
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.timeline_data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="positive" stroke={COLORS.positive} strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="neutral" stroke={COLORS.neutral} strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="negative" stroke={COLORS.negative} strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </motion.div>
  );
}
