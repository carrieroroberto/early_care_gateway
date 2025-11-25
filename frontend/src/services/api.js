import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  login: (credentials) => api.post('/login', credentials),
  register: (data) => api.post('/register', data)
};

export const aiAPI = {
  analyse: (payload) => api.post('/analyse', payload)
};

export const reportsAPI = {
  getAll: (patientId = null) => {
    const params = patientId ? { patient_id: patientId } : {};
    return api.get('/reports', { params });
  }
};

export default api;