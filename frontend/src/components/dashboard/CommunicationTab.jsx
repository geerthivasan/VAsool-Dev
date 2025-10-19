import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Mail, MessageSquare, AlertCircle, Activity } from 'lucide-react';
import StatCard from '../StatCard';
import { dummyCommunicationData } from '../../dummyDashboardData';

const CommunicationTab = () => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {dummyCommunicationData.stats.map((stat, index) => (
          <StatCard key={index} stat={stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Communications */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <MessageSquare className="w-5 h-5 mr-2 text-blue-600" />
              Recent Communications
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyCommunicationData.recentCommunications.map((item, index) => {
                const iconColor = item.type.includes('AI') ? 'bg-blue-100' :
                                 item.type.includes('Response') ? 'bg-green-100' :
                                 'bg-red-100';
                const textColor = item.type.includes('AI') ? 'text-blue-700' :
                                 item.type.includes('Response') ? 'text-green-700' :
                                 'text-red-700';
                const Icon = item.icon === 'mail' ? Mail :
                            item.icon === 'message-square' ? MessageSquare :
                            AlertCircle;
                
                return (
                  <div key={index} className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
                    <div className="flex items-start space-x-3">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${iconColor}`}>
                        <Icon className={`w-5 h-5 ${textColor}`} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-1">
                          <p className="font-semibold text-gray-900">{item.type}</p>
                          <span className="text-xs text-gray-500">{item.time}</span>
                        </div>
                        <p className="text-sm text-gray-700 mb-1">To: {item.company}</p>
                        {item.invoice && <p className="text-xs text-gray-500">{item.invoice}</p>}
                        <p className="text-sm text-gray-600 mt-2 italic">"{item.message}"</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Communication Channels */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="w-5 h-5 mr-2 text-purple-600" />
              Communication Channels
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {dummyCommunicationData.channels.map((channel, index) => {
                const IconComponent = channel.icon === 'mail' ? Mail : MessageSquare;
                const successRate = parseInt(channel.successRate);
                const rateColor = successRate >= 85 ? 'text-green-600' :
                                 successRate >= 75 ? 'text-blue-600' :
                                 'text-orange-600';
                
                return (
                  <div key={index} className="p-4 bg-white border border-gray-200 rounded-lg">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <IconComponent className="w-5 h-5 text-blue-600" />
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold text-gray-900">{channel.name}</p>
                        <p className="text-sm text-gray-500">{channel.description}</p>
                      </div>
                      <p className={`text-lg font-bold ${rateColor}`}>{channel.successRate}</p>
                    </div>
                    <p className="text-xs text-gray-500">Success rate</p>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Communication Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Mail className="w-5 h-5 mr-2 text-green-600" />
            AI Communication Insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-green-900 font-medium mb-2">Best Practice Detected</p>
            <p className="text-green-700">
              Your AI-generated messages have a 78% response rate, which is 23% higher than industry average. 
              Personalized payment reminders with direct payment links show the highest engagement.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CommunicationTab;