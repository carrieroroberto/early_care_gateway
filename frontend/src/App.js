import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Authentication from "./pages/Authentication";
import Analysis from "./pages/Analysis";
import Reports from "./pages/Reports";
import Layout from "./components/Layout";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("jwt_token");
  if (!token) {
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Authentication />} />
        
        <Route path="/dashboard" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<Analysis />} />
          <Route path="reports" element={<Reports />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;