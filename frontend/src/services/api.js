import axios from 'axios';

const MAIN_URL = 'http://localhost:8000';  //Port for authentication and analysis
const PROCESSOR_URL = 'http://localhost:8001';    //Port for preprocessing

const api = axios.create({
  baseURL: MAIN_URL,
  headers: { 'Content-Type': 'application/json' },
});

const processorApi = axios.create({
  baseURL: PROCESSOR_URL,
  headers: { 'Content-Type': 'application/json' },
});

// --- Token handling ---
const addToken = (config) => {
  const token = localStorage.getItem('jwt_token');  //Searches the jwt token in local memory
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
};

api.interceptors.request.use(addToken);
processorApi.interceptors.request.use(addToken);

// --- API functions ---

export const authAPI = {
  login: (credentials) => api.post('/authentication/login', credentials),  //Sends credentials to login 
  register: (data) => api.post('/authentication/register', data),   //Sends whole data to register
};

export const runDiagnosticWorkflow = async (dataType, rawData, targetModel = 'local') => {
  try {
    console.log("🚀 STEP 1: Preprocessing the data, sending them to the Processor...", { dataType, targetModel });   
    
    const processRes = await processorApi.post('/process', {   //This blocks send raw data to the processor
      data_type: dataType,        
      patient_id: "User-Session", 
      raw_data: rawData,         
      target_model: targetModel  
    });

    const cleanPayload = processRes.data.payload;   //We received the cleaned data
    console.log("✅ STEP 1 Completed. Processed payload has been received.");

    console.log("🚀 STEP 2: Sending to AI Brain...");   //After processing we need to analyze
    
    const aiRes = await api.post('/predict', {   //Sending cleaned data to AI
      type: dataType, 
      data: cleanPayload   ///cleaned
    });

    console.log("✅ STEP 2 Completed. Diagnosis received.");
    return aiRes.data;

  } catch (error) {
    console.error("❌ An error occured during AI Workflow:", error);
    throw error;
  }
};

export const reportsAPI = {   //Used for reports
  getAll: (patientId) => {  //List of reports saved in the db
    const params = patientId ? { patient_id: patientId } : {};
    return api.get('/reports', { params });
  }
};

export default api;