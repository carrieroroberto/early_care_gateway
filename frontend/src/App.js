//Decides what page to show based on the URL
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Analysis from './pages/Analysis';
import Reports from './pages/Reports';
import Layout from './components/Layout';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('jwt_token');   //Checks if the doctor has the token
  if (!token) {  //If there's no token, goes to login page
    return <Navigate to="/" replace />;
  }
  return children;   //If htere's the token, it lets the doctor see the page he was on
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Login Page*/}
        <Route path="/" element={<Login />} />
        
        {/* Dashboard*/}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          {/* Analysis */}
          <Route index element={<Analysis />} />
          
          {/* Reports */}
          <Route path="reports" element={<Reports />} />
        </Route>

        {/* If the path is something else it goes to dashboard anyways */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;