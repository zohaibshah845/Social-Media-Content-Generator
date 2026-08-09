// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';

// Make sure root element exists
const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Root element with id "root" not found in index.html');
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);