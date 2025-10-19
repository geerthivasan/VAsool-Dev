import React, { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Building2, Landmark, CheckCircle2, Clock } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const IntegrationsModal = ({ open, onOpenChange }) => {
  const [activeIntegration, setActiveIntegration] = useState(null);
  const [loading, setLoading] = useState(false);
  const [connectedIntegrations, setConnectedIntegrations] = useState([]);

  const accountingSystems = [
    {
      id: 'zohobooks',
      name: 'Zoho Books',
      description: 'Connect your Zoho Books account',
      icon: Building2,
      available: true,
      color: 'blue'
    },
    {
      id: 'quickbooks',
      name: 'QuickBooks',
      description: 'Coming soon',
      icon: Building2,
      available: false,
      color: 'green'
    },
    {
      id: 'xerobooks',
      name: 'Xero Books',
      description: 'Coming soon',
      icon: Building2,
      available: false,
      color: 'purple'
    },
    {
      id: 'tally',
      name: 'Tally',
      description: 'Coming soon',
      icon: Building2,
      available: false,
      color: 'orange'
    }
  ];

  const handleZohoConnect = async () => {
    setLoading(true);
    
    try {
      const token = localStorage.getItem('authToken');
      
      // Check if we should use demo mode (when real OAuth credentials aren't configured)
      const useDemoMode = window.confirm(
        "Demo Mode Available\n\n" +
        "Since Zoho OAuth credentials aren't configured yet, would you like to use DEMO MODE?\n\n" +
        "✅ Click OK for Demo Mode (simulates connection)\n" +
        "❌ Click Cancel to try real OAuth (requires Zoho app setup)"
      );
      
      if (useDemoMode) {
        // Use demo mode - simulate successful connection
        const response = await axios.post(
          `${API}/integrations/zoho/demo-connect`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        if (response.data.success) {
          toast({
            title: "Demo Connection Successful!",
            description: "Zoho Books connected in demo mode. Real OAuth setup required for production.",
          });
          setActiveIntegration(null);
          setTimeout(() => {
            window.location.reload();
          }, 1000);
        }
      } else {
        // Close modal before redirect to avoid iframe issues
        onOpenChange(false);
        
        // Get OAuth URL from backend
        const response = await axios.get(
          `${API}/integrations/zoho/auth-url`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (response.data.auth_url) {
          // Small delay to ensure modal closes, then redirect at top level
          setTimeout(() => {
            // Force top-level redirect (not in iframe/modal)
            window.top.location.href = response.data.auth_url;
          }, 100);
        }
      }
    } catch (error) {
      toast({
        title: "Connection Failed",
        description: error.response?.data?.detail || "Failed to initiate Zoho Books connection",
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle className="text-2xl">Connect Integrations</DialogTitle>
          <DialogDescription>
            Connect your accounting systems and bank accounts to enhance your collections management
          </DialogDescription>
        </DialogHeader>

        {activeIntegration === 'zohobooks' ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-3 mb-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setActiveIntegration(null)}
              >
                ← Back
              </Button>
              <h3 className="text-lg font-semibold">Connect Zoho Books</h3>
            </div>
            
            <Card>
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
                    <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Building2 className="w-8 h-8 text-blue-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-1">Secure OAuth 2.0 Connection</h4>
                      <p className="text-sm text-gray-600">
                        You'll be redirected to Zoho Books to securely authorize access to your accounting data.
                      </p>
                    </div>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-lg p-4">
                    <h5 className="font-medium text-gray-900 mb-3">What we'll access:</h5>
                    <ul className="space-y-2 text-sm text-gray-600">
                      <li className="flex items-start">
                        <CheckCircle2 className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                        <span>Read your invoices and outstanding payments</span>
                      </li>
                      <li className="flex items-start">
                        <CheckCircle2 className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                        <span>Access customer payment history</span>
                      </li>
                      <li className="flex items-start">
                        <CheckCircle2 className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                        <span>View financial reports for collections analysis</span>
                      </li>
                    </ul>
                  </div>

                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p className="text-sm text-green-800">
                      <strong className="flex items-center mb-1">
                        <CheckCircle2 className="w-4 h-4 mr-1" />
                        Secure & Safe
                      </strong>
                      We use OAuth 2.0 industry standard. Your Zoho credentials are never shared with us. 
                      You can revoke access anytime from your Zoho account settings.
                    </p>
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-sm text-blue-800">
                      <strong>🔧 Setup Options:</strong>
                      <br />
                      <strong>Demo Mode:</strong> Test the integration with simulated data (no real Zoho account needed)
                      <br />
                      <strong>Production Mode:</strong> Requires Zoho OAuth App setup with client ID and secret
                    </p>
                  </div>

                  <Button
                    onClick={handleZohoConnect}
                    className="w-full bg-blue-600 hover:bg-blue-700"
                    disabled={loading}
                  >
                    {loading ? 'Connecting...' : 'Connect with Zoho Books'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Accounting Systems */}
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Building2 className="w-5 h-5 mr-2" />
                Accounting Systems
              </h3>
              <div className="grid grid-cols-2 gap-4">
                {accountingSystems.map((system) => {
                  const Icon = system.icon;
                  const isConnected = connectedIntegrations.includes(system.id);
                  
                  return (
                    <Card
                      key={system.id}
                      className={`relative ${
                        system.available && !isConnected
                          ? 'cursor-pointer hover:shadow-md transition-shadow'
                          : 'opacity-60'
                      }`}
                      onClick={() => system.available && !isConnected && setActiveIntegration(system.id)}
                    >
                      {isConnected && (
                        <div className="absolute top-2 right-2">
                          <CheckCircle2 className="w-5 h-5 text-green-600" />
                        </div>
                      )}
                      <CardHeader>
                        <div className={`w-12 h-12 bg-${system.color}-100 rounded-lg flex items-center justify-center mb-2`}>
                          <Icon className={`w-6 h-6 text-${system.color}-600`} />
                        </div>
                        <CardTitle className="text-base">{system.name}</CardTitle>
                        <CardDescription className="text-sm">
                          {isConnected ? 'Connected' : system.description}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        {system.available && !isConnected ? (
                          <Button size="sm" className="w-full">
                            Connect
                          </Button>
                        ) : !system.available ? (
                          <Button size="sm" variant="outline" className="w-full" disabled>
                            <Clock className="w-4 h-4 mr-2" />
                            Coming Soon
                          </Button>
                        ) : (
                          <Button size="sm" variant="outline" className="w-full" disabled>
                            Connected
                          </Button>
                        )}
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>

            {/* Bank Account */}
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Landmark className="w-5 h-5 mr-2" />
                Bank Account
              </h3>
              <Card className="opacity-60">
                <CardHeader>
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-2">
                    <Landmark className="w-6 h-6 text-gray-600" />
                  </div>
                  <CardTitle className="text-base">Connect Bank Account</CardTitle>
                  <CardDescription className="text-sm">
                    Connect your bank account to read statements for reconciliation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button size="sm" variant="outline" className="w-full" disabled>
                    <Clock className="w-4 h-4 mr-2" />
                    Coming Soon
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default IntegrationsModal;