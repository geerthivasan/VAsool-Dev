import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { CheckCircle2, AlertTriangle, Target } from 'lucide-react';
import StatCard from '../StatCard';
import { dummyCollectionsData } from '../../dummyDashboardData';

const CollectionsTab = () => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {dummyCollectionsData.stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Collections */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckCircle2 className="w-5 h-5 mr-2 text-green-600" />
              Recent Collections
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyCollectionsData.recentCollections.map((item, index) => (
                <div key={index} className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="font-semibold text-gray-900">{item.company}</p>
                      <p className="text-sm text-gray-600">{item.invoice} • {item.status}</p>
                    </div>
                    <p className="font-bold text-green-700">{item.amount}</p>
                  </div>
                  <p className="text-xs text-gray-500">{item.time}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Priority Collections */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-red-600" />
              Priority Collections
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyCollectionsData.priorityCollections.map((item, index) => {
                const bgColor = item.priority === 'high' ? 'bg-red-50 border-red-200' : 
                               item.priority === 'medium' ? 'bg-orange-50 border-orange-200' : 
                               'bg-yellow-50 border-yellow-200';
                const badge = item.priority === 'high' ? 'bg-red-500' : 
                             item.priority === 'medium' ? 'bg-orange-500' : 
                             'bg-yellow-500';
                
                return (
                  <div key={index} className={`p-4 border rounded-lg ${bgColor}`}>
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <p className="font-semibold text-gray-900">{item.company}</p>
                        <p className="text-sm text-gray-600">{item.dueDate} • {item.status}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-gray-900">{item.amount}</p>
                        <span className={`inline-block px-2 py-1 text-xs text-white rounded mt-1 ${badge}`}>
                          {item.priority.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
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