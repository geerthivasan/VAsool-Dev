import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { TrendingUp, Target, AlertCircle } from 'lucide-react';
import StatCard from '../StatCard';
import { dummyOverviewData } from '../../dummyDashboardData';

const OverviewTab = () => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {dummyOverviewData.stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Cash Flow Forecast */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
              Cash Flow Forecast
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {dummyOverviewData.cashFlowForecast.map((item, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{item.period}</p>
                    <p className="text-sm text-gray-500">{item.label}</p>
                  </div>
                  <p className="text-lg font-bold text-gray-900">{item.amount}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Risk Assessment */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertCircle className="w-5 h-5 mr-2 text-orange-600" />
              Risk Assessment
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {dummyOverviewData.riskAssessment.map((item, index) => {
                const bgColor = item.color === 'red' ? 'bg-red-50 border-red-200' : 
                               item.color === 'orange' ? 'bg-orange-50 border-orange-200' : 
                               'bg-green-50 border-green-200';
                const textColor = item.color === 'red' ? 'text-red-700' : 
                                 item.color === 'orange' ? 'text-orange-700' : 
                                 'text-green-700';
                const badgeColor = item.color === 'red' ? 'bg-red-500' : 
                                  item.color === 'orange' ? 'bg-orange-500' : 
                                  'bg-green-500';
                
                return (
                  <div key={index} className={`p-4 border rounded-lg ${bgColor}`}>
                    <div className="flex items-center justify-between mb-2">
                      <p className={`font-semibold ${textColor}`}>{item.risk}</p>
                      <span className={`px-2 py-1 text-xs text-white rounded ${badgeColor}`}>
                        {item.status}
                      </span>
                    </div>
                    <p className={`text-lg font-bold ${textColor}`}>{item.amount} • {item.accounts} accounts</p>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent AI Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Target className="w-5 h-5 mr-2 text-blue-600" />
            Recent AI Actions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {dummyOverviewData.recentActions.map((action, index) => (
              <div key={index} className="flex items-start p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{action.action}</p>
                  <p className="text-sm text-gray-600">To: {action.company} • {action.details}</p>
                </div>
                <span className="text-xs text-gray-500">{action.time}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default OverviewTab;