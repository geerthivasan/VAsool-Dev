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
        {dummyAnalyticsData.stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Collection Performance Trends */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-blue-600" />
              Collection Performance Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {dummyAnalyticsData.performanceTrends.map((item, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">{item.period}</span>
                    <span className="text-sm font-bold text-gray-900">{item.rate}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full bg-${item.color}-500`}
                      style={{ width: `${item.rate}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Customer Payment Behavior */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="w-5 h-5 mr-2 text-purple-600" />
              Customer Payment Behavior
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyAnalyticsData.customerBehavior.map((item, index) => {
                const bgColor = index === 0 ? 'bg-green-50 border-green-200' :
                               index === 1 ? 'bg-blue-50 border-blue-200' :
                               'bg-orange-50 border-orange-200';
                const textColor = index === 0 ? 'text-green-700' :
                                 index === 1 ? 'text-blue-700' :
                                 'text-orange-700';
                
                return (
                  <div key={index} className={`p-4 border rounded-lg ${bgColor}`}>
                    <div className="flex items-center justify-between mb-2">
                      <p className={`font-semibold ${textColor}`}>{item.category}</p>
                      <p className={`text-lg font-bold ${textColor}`}>{item.percentage}</p>
                    </div>
                    <p className="text-sm text-gray-600">{item.description} • {item.volume} volume</p>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Predictive Analytics & Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Lightbulb className="w-5 h-5 mr-2 text-yellow-600" />
            Predictive Analytics & Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {dummyAnalyticsData.recommendations.map((rec, index) => {
              const priorityColor = rec.priority === 'high' ? 'bg-red-500' :
                                   rec.priority === 'medium' ? 'bg-orange-500' :
                                   'bg-blue-500';
              
              return (
                <div key={index} className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <p className="font-semibold text-gray-900">{rec.title}</p>
                    <span className={`px-2 py-1 text-xs text-white rounded ${priorityColor}`}>
                      {rec.priority.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">{rec.description}</p>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AnalyticsTab;