import React from 'react';
import { Card } from './ui/card';
import { TrendingDown, CheckCircle2, BarChart3, AlertCircle, TrendingUp, Clock, Zap, Sparkles, Target } from 'lucide-react';

const iconMap = {
  'trending-down': TrendingDown,
  'check-circle': CheckCircle2,
  'bar-chart': BarChart3,
  'alert-circle': AlertCircle,
  'trending-up': TrendingUp,
  'clock': Clock,
  'zap': Zap,
  'sparkles': Sparkles,
  'robot': Target,
  'mail': CheckCircle2
};

const StatCard = ({ stat }) => {
  const Icon = iconMap[stat.icon] || BarChart3;
  const isNegative = stat.changeType === 'negative';
  
  return (
    <Card className="p-6">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-600 mb-2">{stat.label}</p>
          <p className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</p>
          <p className={`text-sm ${isNegative ? 'text-red-600' : 'text-gray-500'}`}>
            {stat.change}
          </p>
        </div>
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
          isNegative ? 'bg-red-100' : 'bg-green-100'
        }`}>
          <Icon className={`w-6 h-6 ${isNegative ? 'text-red-600' : 'text-green-600'}`} />
        </div>
      </div>
    </Card>
  );
};

export default StatCard;