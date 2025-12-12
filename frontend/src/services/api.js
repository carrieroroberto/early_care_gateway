import axios from "axios";
import CryptoJS from "crypto-js";

const GATEWAY_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/gateway";

const api = axios.create({
  baseURL: GATEWAY_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("jwt_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const hashPatientCf = (patientCf) => {
  if (!patientCf) return "";
  return CryptoJS.SHA256(patientCf.toUpperCase()).toString(CryptoJS.enc.Hex);
};

export const authAPI = {
  login: (credentials) => api.post("/login", credentials),
  register: (data) => api.post("/register", data),
};

export const aiAPI = {
  analyse: (payload) => api.post("/analyse", payload),
};

export const reportsAPI = {
  getAll: (patientCf = "") => {
    const params = patientCf ? { patient_hashed_cf: hashPatientCf(patientCf) } : {};
    return api.get("/reports", { params });
  },
};

export default api;