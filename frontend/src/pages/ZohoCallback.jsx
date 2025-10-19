import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ZohoCallback = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('processing'); // processing, success, error
  const [message, setMessage] = useState('Connecting to Zoho Books...');

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const error = searchParams.get('error');

      if (error) {
        setStatus('error');
        setMessage(`Connection failed: ${error}`);
        return;
      }

      if (!code || !state) {
        setStatus('error');
        setMessage('Invalid callback parameters');
        return;
      }

      try {
        const token = localStorage.getItem('authToken');
        
        const response = await axios.post(
          `${API}/integrations/zoho/callback`,
          { code, state },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (response.data.success) {
          setStatus('success');
          setMessage('Zoho Books connected successfully!');
          
          // Redirect to dashboard after 2 seconds
          setTimeout(() => {
            navigate('/dashboard');
          }, 2000);
        }
      } catch (error) {
        setStatus('error');
        setMessage(error.response?.data?.detail || 'Failed to complete connection');
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              {status === 'processing' && (
                <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
              )}
              {status === 'success' && (
                <CheckCircle2 className="w-16 h-16 text-green-600" />
              )}
              {status === 'error' && (
                <AlertCircle className="w-16 h-16 text-red-600" />
              )}
            </div>
            <CardTitle className="text-2xl">
              {status === 'processing' && 'Connecting...'}
              {status === 'success' && 'Connected!'}
              {status === 'error' && 'Connection Failed'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-center text-gray-600 mb-6">{message}</p>
            
            {status === 'success' && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                <p className="text-sm text-green-800">
                  Redirecting you to dashboard...
                </p>
              </div>
            )}

            {status === 'error' && (
              <Button
                onClick={() => navigate('/dashboard')}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                Back to Dashboard
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ZohoCallback;
