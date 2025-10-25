import React, { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent } from './ui/card';
import { ExternalLink, CheckCircle2, AlertCircle } from 'lucide-react';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ZohoSetupModal = ({ open, onOpenChange, onSuccess }) => {
  const [step, setStep] = useState(1); // 1: Instructions, 2: Input Form
  const [loading, setLoading] = useState(false);
  const [credentials, setCredentials] = useState({
    clientId: '',
    clientSecret: '',
    organizationId: ''
  });

  const handleConnect = async () => {
    // Validate inputs
    if (!credentials.clientId || !credentials.clientSecret) {
      toast({
        title: "Missing Information",
        description: "Please enter both Client ID and Client Secret",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem('authToken');
      
      // Send credentials to backend to initiate OAuth
      const response = await axios.post(
        `${API}/integrations/zoho/user-oauth-setup`,
        {
          client_id: credentials.clientId,
          client_secret: credentials.clientSecret,
          organization_id: credentials.organizationId || null
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.auth_url) {
        // Close modal and redirect to Zoho login
        toast({
          title: "Redirecting to Zoho...",
          description: "Please login with your Zoho credentials",
        });
        
        onOpenChange(false);
        
        // Redirect to Zoho OAuth page - use direct assignment for better compatibility
        window.location.replace(response.data.auth_url);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail 
        ? (typeof error.response.data.detail === 'string' 
            ? error.response.data.detail 
            : JSON.stringify(error.response.data.detail))
        : error.message || "Failed to setup Zoho connection";
        
      toast({
        title: "Connection Failed",
        description: errorMessage,
        variant: "destructive",
      });
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl flex items-center">
            {step === 1 ? '🔐 Setup Zoho Books OAuth' : '📝 Enter Your OAuth Credentials'}
          </DialogTitle>
          <DialogDescription>
            {step === 1 
              ? 'Follow these steps to create your Zoho OAuth application'
              : 'Paste your Client ID and Secret from Zoho API Console'}
          </DialogDescription>
        </DialogHeader>

        {step === 1 ? (
          <div className="space-y-4">
            {/* Instructions */}
            <Card className="border-blue-200 bg-blue-50">
              <CardContent className="pt-6">
                <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  Why do I need to do this?
                </h3>
                <p className="text-sm text-blue-800">
                  To securely access your Zoho Books data, you need to create an OAuth application. 
                  This is a one-time setup that takes about 5 minutes.
                </p>
              </CardContent>
            </Card>

            {/* Step-by-step guide */}
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-green-700 font-bold">1</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold mb-2">Go to Zoho API Console</h4>
                  <a 
                    href="https://api-console.zoho.com/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-blue-600 hover:text-blue-700 text-sm"
                  >
                    Open Zoho API Console
                    <ExternalLink className="w-4 h-4 ml-1" />
                  </a>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-green-700 font-bold">2</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold mb-2">Create Client</h4>
                  <p className="text-sm text-gray-600 mb-2">
                    Click "Add Client" → Select "Server-based Applications"
                  </p>
                  <div className="bg-gray-50 border rounded p-3 text-sm space-y-1">
                    <p><strong>Client Name:</strong> Vasool Collections (or any name)</p>
                    <p><strong>Homepage URL:</strong> {window.location.origin}</p>
                    <p><strong>Authorized Redirect URI:</strong></p>
                    <code className="bg-white px-2 py-1 rounded text-xs block mt-1">
                      {window.location.origin}/zoho/callback
                    </code>
                  </div>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-green-700 font-bold">3</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold mb-2">Copy Credentials</h4>
                  <p className="text-sm text-gray-600">
                    After creating, you'll see your <strong>Client ID</strong> and <strong>Client Secret</strong>. 
                    Copy both - you'll need them in the next step.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-green-700 font-bold">4</span>
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold mb-2">Get Organization ID (Optional)</h4>
                  <p className="text-sm text-gray-600">
                    Login to Zoho Books → Settings → Organization Profile → Copy Organization ID
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-between pt-4">
              <Button variant="outline" onClick={() => onOpenChange(false)}>
                Cancel
              </Button>
              <Button onClick={() => setStep(2)} className="bg-green-600 hover:bg-green-700">
                I've Created the OAuth App →
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Input Form */}
            <Card className="border-green-200 bg-green-50">
              <CardContent className="pt-4">
                <p className="text-sm text-green-800 flex items-start">
                  <CheckCircle2 className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                  Great! Now paste your OAuth credentials below. These will be securely stored and used only to access your Zoho Books data.
                </p>
              </CardContent>
            </Card>

            <div className="space-y-4">
              <div>
                <Label htmlFor="clientId">
                  Client ID <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="clientId"
                  placeholder="1000.XXXXXXXXXXXXXXXXXXXXXXX"
                  value={credentials.clientId}
                  onChange={(e) => setCredentials({ ...credentials, clientId: e.target.value })}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Starts with "1000." - found in Zoho API Console
                </p>
              </div>

              <div>
                <Label htmlFor="clientSecret">
                  Client Secret <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="clientSecret"
                  type="password"
                  placeholder="Enter your Client Secret"
                  value={credentials.clientSecret}
                  onChange={(e) => setCredentials({ ...credentials, clientSecret: e.target.value })}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Keep this secret! Never share it publicly
                </p>
              </div>

              <div>
                <Label htmlFor="organizationId">
                  Organization ID (Optional)
                </Label>
                <Input
                  id="organizationId"
                  placeholder="Enter Organization ID (optional)"
                  value={credentials.organizationId}
                  onChange={(e) => setCredentials({ ...credentials, organizationId: e.target.value })}
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Found in Zoho Books → Settings → Organization Profile
                </p>
              </div>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <p className="text-xs text-yellow-800">
                <strong>Security Note:</strong> Your credentials are encrypted and stored securely. 
                They're used only to authenticate with Zoho on your behalf.
              </p>
            </div>

            <div className="flex justify-between pt-4">
              <Button variant="outline" onClick={() => setStep(1)}>
                ← Back to Instructions
              </Button>
              <Button 
                onClick={handleConnect} 
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {loading ? 'Connecting...' : 'Connect to Zoho Books'}
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default ZohoSetupModal;
