import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

// Create axios instance with auth header
const createAuthConfig = () => {
  const token = getAuthToken();
  return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
};

// Auth APIs
export const authAPI = {
  signup: async (data) => {
    const response = await axios.post(`${API}/auth/signup`, data);
    return response.data;
  },
  
  login: async (data) => {
    const response = await axios.post(`${API}/auth/login`, data);
    return response.data;
  },
  
  getMe: async () => {
    const response = await axios.get(`${API}/auth/me`, createAuthConfig());
    return response.data;
  }
};

// Chat APIs
export const chatAPI = {
  sendMessage: async (message, sessionId = null) => {
    const response = await axios.post(
      `${API}/chat/message`,
      { message, session_id: sessionId },
      createAuthConfig()
    );
    return response.data;
  },
  
  getHistory: async (sessionId = null) => {
    const params = sessionId ? { session_id: sessionId } : {};
    const response = await axios.get(`${API}/chat/history`, {
      ...createAuthConfig(),
      params
    });
    return response.data;
  }
};

// Demo & Contact APIs
export const demoContactAPI = {
  scheduleDemo: async (data) => {
    const response = await axios.post(`${API}/demo/schedule`, data);
    return response.data;
  },
  
  contactSales: async (data) => {
    const response = await axios.post(`${API}/contact/sales`, data);
    return response.data;
  }
};

// Dashboard APIs
export const dashboardAPI = {
  getAnalytics: async () => {
    const response = await axios.get(`${API}/dashboard/analytics`, createAuthConfig());
    return response.data;
  },
  
  getCollections: async () => {
    const response = await axios.get(`${API}/dashboard/collections`, createAuthConfig());
    return response.data;
  },
  
  getAnalyticsTrends: async () => {
    const response = await axios.get(`${API}/dashboard/analytics-trends`, createAuthConfig());
    return response.data;
  },
  
  getReconciliation: async () => {
    const response = await axios.get(`${API}/dashboard/reconciliation`, createAuthConfig());
    return response.data;
  }
};

