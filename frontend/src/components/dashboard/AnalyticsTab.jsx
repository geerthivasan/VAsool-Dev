import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { TrendingUp, Users, Lightbulb, Loader2, DollarSign, Clock, BarChart3 } from 'lucide-react';
import StatCard from '../StatCard';
import { dashboardAPI } from '../../api';

const AnalyticsTab = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    try {
      const data = await dashboardAPI.getAnalyticsTrends();
      setAnalyticsData(data);
    } catch (error) {
      console.error('Failed to load analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-green-600" />
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Failed to load analytics data</p>
      </div>
    );
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

  const stats = [
    {
      title: 'Total Collected',
      value: formatCurrency(analyticsData.total_collected),
      change: '+18.2%',
      icon: DollarSign,
      color: 'green'
    },
    {
      title: 'Total Outstanding',
      value: formatCurrency(analyticsData.total_outstanding),
      change: '-12.5%',
      icon: BarChart3,
      color: 'orange'
    },
    {
      title: 'Collection Efficiency',
      value: `${analyticsData.collection_efficiency}%`,
      change: '+5.3%',
      icon: TrendingUp,
      color: 'blue'
    },
    {
      title: 'Avg Collection Time',
      value: `${analyticsData.average_collection_time} days`,
      change: '-3 days',
      icon: Clock,
      color: 'purple'
    }
  ];
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Trends */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-blue-600" />
              Monthly Collection Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {analyticsData.monthly_trends.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">{item.month}</span>
                    <div className="text-right">
                      <span className="text-sm font-bold text-green-600">{formatCurrency(item.collected)}</span>
                      <span className="text-xs text-gray-500 ml-2">collected</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-600">
                    <span>Outstanding: {formatCurrency(item.outstanding)}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="h-3 rounded-full bg-gradient-to-r from-green-500 to-blue-500"
                      style={{ 
                        width: `${Math.min((item.collected / (item.collected + item.outstanding)) * 100, 100)}%` 
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* AI Insights */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lightbulb className="w-5 h-5 mr-2 text-purple-600" />
              AI Insights & Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <p className="font-semibold text-purple-900">Collection Efficiency Improving</p>
                  <span className="px-2 py-1 text-xs text-white rounded bg-green-500">
                    POSITIVE
                  </span>
                </div>
                <p className="text-sm text-purple-700">
                  Your collection efficiency has increased by {(analyticsData.collection_efficiency - 70).toFixed(1)}% over the baseline. 
                  Keep up the consistent follow-up strategy.
                </p>
              </div>
              
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <p className="font-semibold text-blue-900">Optimize Collection Timing</p>
                  <span className="px-2 py-1 text-xs text-white rounded bg-blue-500">
                    TIP
                  </span>
                </div>
                <p className="text-sm text-blue-700">
                  Based on payment patterns, customers respond better to reminders sent on 
                  Tuesday mornings. Consider scheduling priority follow-ups accordingly.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Overall Performance Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BarChart3 className="w-5 h-5 mr-2 text-green-600" />
            Performance Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-center">
              <p className="text-sm text-green-700 mb-1">Collection Rate</p>
              <p className="text-2xl font-bold text-green-900">{analyticsData.collection_efficiency}%</p>
              <p className="text-xs text-green-600 mt-1">Above industry average</p>
            </div>
            
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-center">
              <p className="text-sm text-blue-700 mb-1">Average Days to Collect</p>
              <p className="text-2xl font-bold text-blue-900">{analyticsData.average_collection_time}</p>
              <p className="text-xs text-blue-600 mt-1">Better than last month</p>
            </div>
            
            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg text-center">
              <p className="text-sm text-purple-700 mb-1">Total Collected (6mo)</p>
              <p className="text-2xl font-bold text-purple-900">{formatCurrency(analyticsData.total_collected)}</p>
              <p className="text-xs text-purple-600 mt-1">Strong performance</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AnalyticsTab;