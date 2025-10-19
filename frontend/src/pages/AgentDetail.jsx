import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { ArrowLeft, TrendingUp, Shield, Users, CheckCircle2, Briefcase, Zap } from 'lucide-react';
import { mockAgents } from '../mockData';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const iconMap = {
  'briefcase': Briefcase,
  'trending-up': TrendingUp,
  'zap': Zap,
  'users': Users,
  'check-circle': CheckCircle2,
  'shield': Shield
};

const AgentDetail = () => {
  const { agentId } = useParams();
  const navigate = useNavigate();
  const agent = mockAgents.find(a => a.id === agentId);

  if (!agent) {
    return <div>Agent not found</div>;
  }

  const IconComponent = iconMap[agent.icon];

  return (
    <div className="min-h-screen bg-white">
      <Navbar />

      <div className="pt-24 pb-20 px-4">
        <div className="max-w-4xl mx-auto">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="mb-8"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>

          <Card className="border-none shadow-lg">
            <CardHeader>
              <div className={`w-16 h-16 bg-${agent.color === 'green' ? 'green' : 'red'}-100 rounded-xl flex items-center justify-center mb-4`}>
                <IconComponent className={`w-8 h-8 text-${agent.color === 'green' ? 'green' : 'red'}-600`} />
              </div>
              <CardTitle className="text-4xl mb-4">{agent.name}</CardTitle>
              <CardDescription className="text-lg">{agent.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="text-2xl font-semibold mb-3">How It Works</h3>
                  <p className="text-gray-600 leading-relaxed">{agent.details}</p>
                </div>

                <div>
                  <h3 className="text-2xl font-semibold mb-3">Key Features</h3>
                  <ul className="space-y-3">
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-600">Real-time data processing and analysis</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-600">Automated decision-making capabilities</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-600">Seamless integration with other agents</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle2 className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-600">Continuous learning and optimization</span>
                    </li>
                  </ul>
                </div>

                <div className="pt-6">
                  <Button
                    size="lg"
                    className="bg-green-600 hover:bg-green-700"
                    onClick={() => navigate('/signup')}
                  >
                    Get Started with {agent.name}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default AgentDetail;