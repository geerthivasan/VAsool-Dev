import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { CheckCircle2, AlertCircle, Activity } from 'lucide-react';
import StatCard from '../StatCard';
import { dummyReconciliationData } from '../../dummyDashboardData';

const ReconciliationTab = () => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {dummyReconciliationData.stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Reconciliation Timeline */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="w-5 h-5 mr-2 text-blue-600" />
              Reconciliation Timeline
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyReconciliationData.timeline.map((item, index) => {
                const statusColor = item.statusType === 'success' ? 'bg-green-100 text-green-700 border-green-200' :
                                   item.statusType === 'processing' ? 'bg-blue-100 text-blue-700 border-blue-200' :
                                   'bg-gray-100 text-gray-700 border-gray-200';
                const badgeColor = item.statusType === 'success' ? 'bg-green-500' :
                                  item.statusType === 'processing' ? 'bg-blue-500' :
                                  'bg-gray-500';
                
                return (
                  <div key={index} className={`p-4 border rounded-lg ${statusColor}`}>
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <p className="font-semibold">{item.batch}</p>
                        <p className="text-sm opacity-75">{item.time} • Auto-reconciled</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">{item.amount}</p>
                        <span className={`inline-block px-2 py-1 text-xs text-white rounded mt-1 ${badgeColor}`}>
                          {item.status}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Reconciliation Issues */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertCircle className="w-5 h-5 mr-2 text-red-600" />
              Reconciliation Issues
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyReconciliationData.issues.map((issue, index) => {
                const severityColor = issue.severity === 'high' ? 'bg-red-50 border-red-200' :
                                     'bg-orange-50 border-orange-200';
                const badgeColor = issue.severity === 'high' ? 'bg-red-500' : 'bg-orange-500';
                
                return (
                  <div key={index} className={`p-4 border rounded-lg ${severityColor}`}>
                    <div className="flex items-start justify-between mb-2">
                      <p className="font-semibold text-gray-900">{issue.type}</p>
                      <span className={`px-2 py-1 text-xs text-white rounded ${badgeColor}`}>
                        {issue.severity === 'high' ? 'Action Required' : 'Review'}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mb-1">
                      {issue.invoice || issue.transaction}
                    </p>
                    <p className="text-sm text-gray-600">{issue.details}</p>
                    <p className="text-xs text-gray-500 mt-2 italic">{issue.note}</p>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bank Reconciliation Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <CheckCircle2 className="w-5 h-5 mr-2 text-green-600" />
            Bank Reconciliation Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-blue-900 font-medium mb-2">Automated Reconciliation Active</p>
            <p className="text-blue-700">
              Bank statements are automatically synced and reconciled every 4 hours. Last sync: 1 hour ago.
              <span className="block mt-2 text-sm">Next scheduled sync: 3 hours from now</span>
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ReconciliationTab;