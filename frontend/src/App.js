// Import routing components from React Router
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

// Import application pages
import Authentication from "./pages/Authentication";
import Analysis from "./pages/Analysis";
import Reports from "./pages/Reports";

// Import layout component used for protected routes
import Layout from "./components/Layout";

// Component that protects routes requiring authentication
const ProtectedRoute = ({ children }) => {
  // Retrieve JWT token from local storage
  const token = localStorage.getItem("jwt_token");

  // If no token is found, redirect the user to the authentication page
  if (!token) {
    return <Navigate to="/" replace />;
  }

  // If the user is authenticated, render the protected content
  return children;
};

// Main application component
function App() {
  return (
    // Wrap the application with the router
    <Router>
      <Routes>
        {/* Public route: authentication page */}
        <Route path="/" element={<Authentication />} />
        
        {/* Protected dashboard route with shared layout */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          {/* Default dashboard page */}
          <Route index element={<Analysis />} />

          {/* Reports page inside the dashboard */}
          <Route path="reports" element={<Reports />} />
        </Route>

        {/* Fallback route: redirect unknown paths to the home page */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

// Export the App component as default
export default App;