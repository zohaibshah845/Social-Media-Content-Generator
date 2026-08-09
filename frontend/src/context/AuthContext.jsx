// src/context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

const API_URL = 'http://localhost:8000';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // ===== LOAD USER ON MOUNT =====
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try {
          const response = await axios.get(`${API_URL}/auth/me`);
          setUser(response.data);
        } catch (error) {
          console.error('Error fetching user:', error);
          localStorage.removeItem('token');
          delete axios.defaults.headers.common['Authorization'];
          setToken(null);
        }
      }
      setLoading(false);
    };

    loadUser();
  }, [token]);

  // ===== REGISTER =====
  const register = async (name, email, password) => {
    try {
      console.log('📤 Registering:', { name, email });
      
      const response = await axios.post(`${API_URL}/auth/register`, {
        name: name.trim(),
        email: email.trim().toLowerCase(),
        password: password
      });
      
      console.log('✅ Registration response:', response.data);
      
      const { access_token, user } = response.data;
      setToken(access_token);
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setUser(user);
      return { success: true };
    } catch (error) {
      console.error('❌ Registration error:', error);
      console.error('❌ Response data:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      };
    }
  };

  // ===== LOGIN =====
  const login = async (email, password) => {
    try {
      console.log('📤 Logging in:', { email });
      
      const response = await axios.post(`${API_URL}/auth/login`, {
        email: email.trim().toLowerCase(),
        password: password
      });
      
      console.log('✅ Login response:', response.data);
      
      const { access_token, user } = response.data;
      setToken(access_token);
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setUser(user);
      return { success: true };
    } catch (error) {
      console.error('❌ Login error:', error);
      console.error('❌ Response data:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Invalid credentials' 
      };
    }
  };

  // ===== LOGOUT =====
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    console.log('👋 Logged out');
  };

  const value = {
    user,
    loading,
    register,
    login,
    logout,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};