import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card } from '../components/ui/card';
import { MessageSquare, BarChart3, Plus, AlertCircle, Send, Leaf, Link as LinkIcon, ChevronLeft } from 'lucide-react';
import { chatAPI, dashboardAPI } from '../api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const messagesEndRef = useRef(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem('isAuthenticated')) {
      navigate('/login');
      return;
    }
    
    // Load chat history
    loadChatHistory();
    
    // Load dashboard analytics
    if (activeTab === 'dashboard') {
      loadAnalytics();
    }
  }, [navigate, activeTab]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const response = await chatAPI.getHistory(sessionId);
      setMessages(response.messages);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const data = await dashboardAPI.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMessage = {
      id: messages.length + 1,
      sender: 'user',
      message: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages([...messages, newMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await chatAPI.sendMessage(inputMessage, sessionId);
      
      if (!sessionId) {
        setSessionId(response.session_id);
      }

      const aiMessage = {
        id: messages.length + 2,
        sender: 'assistant',
        message: response.response,
        timestamp: response.timestamp
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = {
        id: messages.length + 2,
        sender: 'assistant',
        message: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleNewChat = () => {
    setMessages([{
      id: 1,
      sender: 'assistant',
      message: "Hello! I'm your AI Collections Assistant. I can help you analyze your portfolio, track payments, and optimize your collection strategies. What would you like to know?",
      timestamp: new Date().toISOString()
    }]);
    setSessionId(null);
  };

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Sidebar */}
      <div className={`${sidebarCollapsed ? 'w-16' : 'w-64'} bg-white border-r border-gray-200 flex flex-col transition-all duration-300`}>
        {/* Logo */}
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          {!sidebarCollapsed && (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Vasool</span>
            </div>
          )}
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="p-1 hover:bg-gray-100 rounded"
          >
            <ChevronLeft className={`w-5 h-5 transition-transform ${sidebarCollapsed ? 'rotate-180' : ''}`} />
          </button>
        </div>

        {/* Navigation */}
        <div className="p-3 space-y-2">
          <button
            onClick={() => setActiveTab('chat')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
              activeTab === 'chat' ? 'bg-green-50 text-green-700' : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <MessageSquare className="w-5 h-5 flex-shrink-0" />
            {!sidebarCollapsed && <span>Chat</span>}
          </button>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
              activeTab === 'dashboard' ? 'bg-green-50 text-green-700' : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <BarChart3 className="w-5 h-5 flex-shrink-0" />
            {!sidebarCollapsed && <span>Dashboard</span>}
          </button>
        </div>

        {/* New Chat Button */}
        {!sidebarCollapsed && (
          <div className="p-3">
            <Button
              onClick={handleNewChat}
              className="w-full bg-green-600 hover:bg-green-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              New Chat
            </Button>
          </div>
        )}

        {/* Integrations */}
        {!sidebarCollapsed && (
          <div className="mt-auto p-4 border-t border-gray-200">
            <div className="text-center">
              <AlertCircle className="w-12 h-12 text-gray-300 mx-auto mb-2" />
              <p className="text-sm text-gray-500 mb-3">No integrations connected</p>
              <Button variant="outline" size="sm" className="w-full">
                Connect Now
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
          <h1 className="text-xl font-semibold">
            {activeTab === 'chat' ? 'Vasool AI Assistant' : 'Dashboard Overview'}
          </h1>
          <div className="flex items-center space-x-3">
            <Button variant="outline" size="sm">
              <LinkIcon className="w-4 h-4 mr-2" />
              Connect
            </Button>
            <Button onClick={() => {
              localStorage.removeItem('isAuthenticated');
              navigate('/');
            }}>
              Logout
            </Button>
          </div>
        </div>

        {/* Content Area */}
        {activeTab === 'chat' ? (
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6">
              <div className="max-w-4xl mx-auto space-y-6">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[70%] ${
                        msg.sender === 'user'
                          ? 'bg-green-600 text-white'
                          : 'bg-white border border-gray-200'
                      } rounded-lg p-4 shadow-sm`}
                    >
                      {msg.sender === 'assistant' && (
                        <div className="flex items-center mb-2">
                          <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-2">
                            <MessageSquare className="w-4 h-4 text-green-600" />
                          </div>
                          <span className="text-sm font-medium text-gray-700">AI Assistant</span>
                        </div>
                      )}
                      <p className={msg.sender === 'user' ? 'text-white' : 'text-gray-800'}>
                        {msg.message}
                      </p>
                      <span className={`text-xs mt-2 block ${
                        msg.sender === 'user' ? 'text-green-100' : 'text-gray-400'
                      }`}>
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 bg-white p-4">
              <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto">
                <div className="flex space-x-2">
                  <Input
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Ask me about collections, payments..."
                    className="flex-1"
                  />
                  <Button type="submit" className="bg-green-600 hover:bg-green-700">
                    <Send className="w-4 h-4" />
                  </Button>
                </div>
              </form>
            </div>
          </div>
        ) : (
          <div className="flex-1 p-6 overflow-y-auto">
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <Card className="p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-2">Total Outstanding</h3>
                  <p className="text-3xl font-bold text-gray-900">₹45.2L</p>
                  <p className="text-sm text-green-600 mt-1">↓ 12% from last month</p>
                </Card>
                <Card className="p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-2">Recovery Rate</h3>
                  <p className="text-3xl font-bold text-gray-900">68%</p>
                  <p className="text-sm text-green-600 mt-1">↑ 8% from last month</p>
                </Card>
                <Card className="p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-2">Active Accounts</h3>
                  <p className="text-3xl font-bold text-gray-900">124</p>
                  <p className="text-sm text-gray-500 mt-1">Across all agents</p>
                </Card>
              </div>
              <Card className="p-6">
                <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">Payment received - INV-2024-001</p>
                      <p className="text-sm text-gray-500">2 hours ago</p>
                    </div>
                    <span className="text-green-600 font-semibold">₹25,000</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">New collection strategy activated</p>
                      <p className="text-sm text-gray-500">5 hours ago</p>
                    </div>
                    <span className="text-blue-600 font-semibold">15 accounts</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">Communication sent - Account XYZ</p>
                      <p className="text-sm text-gray-500">1 day ago</p>
                    </div>
                    <span className="text-gray-600 font-semibold">Email</span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;