import React, { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Building2, Landmark, CheckCircle2, Clock } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import ZohoSetupModal from './ZohoSetupModal';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const IntegrationsModal = ({ open, onOpenChange }) => {
  const [activeIntegration, setActiveIntegration] = useState(null);
  const [zohoSetupOpen, setZohoSetupOpen] = useState(false);
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

  const handleZohoClick = () => {
    setZohoSetupOpen(true);
    onOpenChange(false); // Close main integrations modal
  };

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="sm:max-w-[700px]">
          <DialogHeader>
            <DialogTitle className="text-2xl">Connect Integrations</DialogTitle>
            <DialogDescription>
              Connect your accounting systems and bank accounts to enhance your collections management
            </DialogDescription>
          </DialogHeader>

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
                      onClick={() => system.available && !isConnected && system.id === 'zohobooks' && handleZohoClick()}
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
        </DialogContent>
      </Dialog>

      {/* Zoho Setup Modal */}
      <ZohoSetupModal 
        open={zohoSetupOpen} 
        onOpenChange={setZohoSetupOpen}
        onSuccess={() => {
          toast({
            title: "Connection Successful!",
            description: "Zoho Books has been connected.",
          });
          window.location.reload();
        }}
      />
    </>
  );
};

export default IntegrationsModal;