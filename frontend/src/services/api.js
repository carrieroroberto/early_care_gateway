// Import Axios for HTTP requests
import axios from "axios";

// Import CryptoJS for hashing sensitive data
import CryptoJS from "crypto-js";

// Import utility to decode JSON Web Tokens
import jwt_decode from "jwt-decode";

// Base URL of the API Gateway, configurable via environment variables
const GATEWAY_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000/gateway";

// Create a pre-configured Axios instance
const api = axios.create({
  baseURL: GATEWAY_URL,
  headers: { "Content-Type": "application/json" }
});

// Add a request interceptor to automatically attach the JWT token
api.interceptors.request.use((config) => {
  // Retrieve the JWT token from local storage
  const token = localStorage.getItem("jwt_token");

  // If a token exists, add it to the Authorization header
  if (token) config.headers.Authorization = `Bearer ${token}`;

  return config;
});

// Utility function to hash the patient's fiscal code (CF) using SHA-256
// The value is converted to uppercase to ensure consistency
export const hashPatientCf = (patientCf) => {
  if (!patientCf) return "";
  return CryptoJS.SHA256(patientCf.toUpperCase()).toString(CryptoJS.enc.Hex);
};

// Authentication-related API calls
export const authAPI = {
  // Login function that authenticates the user and stores the JWT
  login: async (credentials) => {
    // Send login request to the backend
    const res = await api.post("/login", credentials);

    // Extract JWT token from the response
    const token = res.data.jwt_token;

    // Store the JWT token in local storage
    localStorage.setItem("jwt_token", token);

    // Decode the token to extract user information
    const decoded = jwt_decode(token);

    // Store basic doctor information for frontend usage
    localStorage.setItem(
      "doctor_info",
      JSON.stringify({ name: decoded.name, surname: decoded.surname })
    );

    return res;
  },

  // Register a new user
  register: (data) => api.post("/register", data),
};

// AI-related API calls
export const aiAPI = {
  // Send analysis request to the backend
  analyse: (payload) => {
    // Hash the patient's fiscal code before sending it
    payload.patient_hashed_cf = hashPatientCf(payload.patient_hashed_cf);

    return api.post("/analyse", payload);
  },
};

// Reports-related API calls
export const reportsAPI = {
  // Retrieve all reports, optionally filtered by patient fiscal code
  getAll: (patientCf = "") => {
    const params = patientCf
      ? { patient_hashed_cf: hashPatientCf(patientCf) }
      : {};

    return api.get("/reports", { params });
  }
};

// Export the Axios instance for generic API usage
export default api;