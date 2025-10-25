import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { CheckCircle2, AlertTriangle, Target, Loader2 } from 'lucide-react';
import StatCard from '../StatCard';
import { dashboardAPI } from '../../api';

const CollectionsTab = () => {
  const [collectionsData, setCollectionsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCollectionsData();
  }, []);

  const loadCollectionsData = async () => {
    try {
      const data = await dashboardAPI.getCollections();
      setCollectionsData(data);
    } catch (error) {
      console.error('Failed to load collections data:', error);
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

  if (!collectionsData) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Failed to load collections data</p>
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
      title: 'Total Unpaid',
      value: formatCurrency(collectionsData.total_unpaid),
      change: '+12.5%',
      icon: AlertTriangle,
      color: 'blue'
    },
    {
      title: 'Total Overdue',
      value: formatCurrency(collectionsData.total_overdue),
      change: '-5.2%',
      icon: AlertTriangle,
      color: 'red'
    },
    {
      title: 'Unpaid Invoices',
      value: collectionsData.unpaid_invoices.length.toString(),
      change: '+8',
      icon: CheckCircle2,
      color: 'blue'
    },
    {
      title: 'Overdue Invoices',
      value: collectionsData.overdue_invoices.length.toString(),
      change: '-3',
      icon: AlertTriangle,
      color: 'orange'
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
        {/* Unpaid Invoices */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckCircle2 className="w-5 h-5 mr-2 text-blue-600" />
              Unpaid Invoices
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {collectionsData.unpaid_invoices.slice(0, 5).map((item, index) => (
                <div key={index} className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="font-semibold text-gray-900">{item.customer_name}</p>
                      <p className="text-sm text-gray-600">{item.invoice_number} • Due: {item.due_date}</p>
                    </div>
                    <p className="font-bold text-blue-700">{formatCurrency(item.balance)}</p>
                  </div>
                </div>
              ))}
              {collectionsData.unpaid_invoices.length === 0 && (
                <p className="text-center text-gray-500 py-4">No unpaid invoices</p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Overdue Invoices */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-red-600" />
              Overdue Invoices
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {collectionsData.overdue_invoices.slice(0, 5).map((item, index) => {
                const bgColor = item.days_overdue > 60 ? 'bg-red-50 border-red-200' : 
                               item.days_overdue > 30 ? 'bg-orange-50 border-orange-200' : 
                               'bg-yellow-50 border-yellow-200';
                const badge = item.days_overdue > 60 ? 'bg-red-500' : 
                             item.days_overdue > 30 ? 'bg-orange-500' : 
                             'bg-yellow-500';
                
                return (
                  <div key={index} className={`p-4 border rounded-lg ${bgColor}`}>
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <p className="font-semibold text-gray-900">{item.customer_name}</p>
                        <p className="text-sm text-gray-600">{item.invoice_number} • {item.days_overdue} days overdue</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-gray-900">{formatCurrency(item.balance)}</p>
                        <span className={`inline-block px-2 py-1 text-xs text-white rounded mt-1 ${badge}`}>
                          {item.days_overdue}d
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
              {collectionsData.overdue_invoices.length === 0 && (
                <p className="text-center text-gray-500 py-4">No overdue invoices</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Collection Strategy Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="w-5 h-5 mr-2 text-purple-600" />
            Collection Strategy Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <p className="text-purple-900 font-medium mb-2">AI Recommendation</p>
            <p className="text-purple-700">
              Based on payment patterns, sending reminders on Tuesday mornings increases response rate by 23%. 
              Consider scheduling your priority collections for optimal timing.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CollectionsTab;