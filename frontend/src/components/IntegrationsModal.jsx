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
  const [zohoCredentials, setZohoCredentials] = useState({ email: '', password: '' });
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

  const handleZohoConnect = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.post(
        `${API}/integrations/zoho/connect`,
        zohoCredentials,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.success) {
        toast({
          title: "Connected!",
          description: "Zoho Books has been connected successfully.",
        });
        setConnectedIntegrations([...connectedIntegrations, 'zohobooks']);
        setActiveIntegration(null);
        setZohoCredentials({ email: '', password: '' });
        
        // Refresh page to update integration status
        window.location.reload();
      }
    } catch (error) {
      toast({
        title: "Connection Failed",
        description: error.response?.data?.detail || "Failed to connect to Zoho Books",
        variant: "destructive",
      });
    } finally {
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
                <form onSubmit={handleZohoConnect} className="space-y-4">
                  <div>
                    <Label htmlFor="zoho-email">Zoho Email</Label>
                    <Input
                      id="zoho-email"
                      type="email"
                      placeholder="your.email@example.com"
                      value={zohoCredentials.email}
                      onChange={(e) => setZohoCredentials({ ...zohoCredentials, email: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="zoho-password">Zoho Password</Label>
                    <Input
                      id="zoho-password"
                      type="password"
                      placeholder="Enter your Zoho password"
                      value={zohoCredentials.password}
                      onChange={(e) => setZohoCredentials({ ...zohoCredentials, password: e.target.value })}
                      required
                    />
                  </div>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-sm text-blue-800">
                      <strong>Note:</strong> Your credentials are securely encrypted and used only to establish OAuth 2.0 connection with Zoho Books.
                    </p>
                  </div>
                  <Button
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700"
                    disabled={loading}
                  >
                    {loading ? 'Connecting...' : 'Connect to Zoho Books'}
                  </Button>
                </form>
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