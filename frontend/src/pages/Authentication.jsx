// Import React hooks
import { useState } from "react";

// Import navigation hook from React Router
import { useNavigate } from "react-router-dom";

// Import authentication API functions
import { authAPI } from "../services/api";

// Import icons from lucide-react for form and UI elements
import { Activity, Lock, Mail, UserPlus, LogIn, User } from "lucide-react";

// Authentication component for login and registration
const Authentication = () => {
  // State to toggle between login and registration forms
  const [isLogin, setIsLogin] = useState(true);

  // State to store form input values
  const [formData, setFormData] = useState({
    name: "",
    surname: "",
    email: "",
    password: ""
  });

  // State to handle error messages
  const [error, setError] = useState("");

  // Hook to navigate programmatically
  const navigate = useNavigate();

  // Validate form inputs before submission
  const validateForm = () => {
    const name = formData.name.trim();
    const surname = formData.surname.trim();
    const email = formData.email.trim();
    const password = formData.password.trim();

    const emailRegex = /^\S+@\S+\.\S+$/;

    // Additional validation for registration
    if (!isLogin) {
      if (name.length < 2) return "Name must have at least 2 characters.";
      if (surname.length < 2) return "Surname must have at least 2 characters.";
    }

    if (!email) return "Email is required.";
    if (!emailRegex.test(email)) return "Invalid email format.";

    if (!password) return "Password is required.";

    if (!isLogin && password.length < 8)
      return "Password must have at least 8 characters.";

    if (!isLogin && password.length > 100)
      return "Password cannot exceed 100 characters.";

    return null;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      if (isLogin) {
        // Perform login
        await authAPI.login({ email: formData.email, password: formData.password });
        // Navigate to dashboard on successful login
        navigate("/dashboard");
      } else {
        // Perform registration
        await authAPI.register(formData);
        alert("Account created successfully. Please, sign in.");
        setIsLogin(true);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Invalid credentials or server error");
    }
  };

  return (
    // Main container for authentication page
    <div className="flex min-h-screen bg-gray-100 items-center justify-center p-4">
      <div className="flex w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden">

        {/* Left side branding (hidden on small screens) */}
        <div className="hidden md:flex w-1/2 bg-teal-700 text-white flex-col justify-center items-center p-10">
          <Activity size={64} className="mb-4" />
          <h1 className="text-3xl font-bold mb-2">EarlyCare Gateway</h1>
          <p className="text-center text-teal-100">
            AI Clinical Decision Support <br />
            {"(Authorized Access Only)"}
          </p>
        </div>

        {/* Right side form */}
        <div className="w-full md:w-1/2 p-8 md:p-12">
          {/* Form title with icon */}
          <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            {isLogin ? <LogIn className="text-teal-600" /> : <UserPlus className="text-teal-600" />}
            {isLogin ? "Welcome Back" : "New Doctor"}
          </h2>

          {/* Display validation or server errors */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 mb-4 rounded text-sm">
              {error}
            </div>
          )}

          {/* Authentication form */}
          <form onSubmit={handleSubmit} className="space-y-4">

            {/* Registration-specific fields */}
            {!isLogin && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-1">
                    Name <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 text-gray-400" size={18} />
                    <input
                      type="text"
                      placeholder="John"
                      className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-1">
                    Surname <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 text-gray-400" size={18} />
                    <input
                      type="text"
                      placeholder="Doe"
                      className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                      onChange={(e) => setFormData({ ...formData, surname: e.target.value })}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Email input */}
            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">
                Email <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-gray-400" size={18} />
                <input
                  type="email"
                  className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                  placeholder="doctor@hospital.com"
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
              </div>
            </div>

            {/* Password input */}
            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">
                Password <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={18} />
                <input
                  type="password"
                  className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                  placeholder="••••••••"
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
              </div>
            </div>

            {/* Submit button */}
            <button
              type="submit"
              className="w-full bg-teal-600 hover:bg-teal-700 text-white font-bold p-3 rounded-lg transition duration-200 shadow-md mt-4"
            >
              {isLogin ? "Sign In" : "Create Account"}
            </button>
          </form>

          {/* Toggle between login and registration */}
          <div className="mt-6 text-center text-sm text-gray-600">
            {isLogin ? "Don't have an account? " : "Already registered? "}
            <button
              onClick={() => { setError(""); setIsLogin(!isLogin); }}
              className="text-teal-600 font-semibold hover:underline"
            >
              {isLogin ? "Create Account" : "Sign In"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Export the Authentication component
export default Authentication;