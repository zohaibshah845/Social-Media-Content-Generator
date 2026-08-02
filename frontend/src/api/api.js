import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('firebase_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const generateContent = (data) => api.post('/generate', data);
export const createGraphic = (postId) => api.post(`/graphics/${postId}`);
export const schedulePost = (data) => api.post('/schedule', data);
export const listPosts = () => api.get('/posts');

export default api;