// src/pages/Register.jsx
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    // Name validation
    if (!name.trim()) {
      setError('Name is required');
      return false;
    }

    // Email validation
    if (!email.trim()) {
      setError('Email is required');
      return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address');
      return false;
    }

    // Password validations
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return false;
    }

    if (password.length > 72) {
      setError('Password cannot be longer than 72 characters');
      return false;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validate form before submitting
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Call register with the correct order: name, email, password
      const result = await register(name, email, password);
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      
      // Handle different types of errors
      if (error.response) {
        // Server responded with error
        const errorMessage = error.response.data?.detail || 'Registration failed';
        setError(errorMessage);
      } else if (error.request) {
        // No response received
        setError('No response from server. Please check your connection.');
      } else {
        // Something else went wrong
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Create Account</h2>
          <p className="auth-subtitle">Start generating content today</p>
        </div>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name <span className="required">*</span></label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your full name"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Email <span className="required">*</span></label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="test@example.com"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Password <span className="required">*</span></label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="8-72 characters"
              required
              disabled={loading}
              minLength={8}
              maxLength={72}
            />
            <small className="form-hint">Password must be 8-72 characters long</small>
          </div>

          <div className="form-group">
            <label>Confirm Password <span className="required">*</span></label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
              disabled={loading}
            />
          </div>

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                Creating Account...
              </>
            ) : (
              'Sign Up'
            )}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;