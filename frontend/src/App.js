import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Analysis from './pages/Analysis';
import Layout from './components/Layout';

// Questo componente serve a proteggere le pagine.
// Se non hai il token, ti rispedisce al Login.
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('jwt_token');
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Pagina Pubblica: Login */}
        <Route path="/" element={<Login />} />
        
        {/* Pagine Protette (Dashboard) */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          {/* Quando vai su /dashboard, carica Analysis al centro */}
          <Route index element={<Analysis />} />
        </Route>

      </Routes>
    </Router>
  );
}

export default App;