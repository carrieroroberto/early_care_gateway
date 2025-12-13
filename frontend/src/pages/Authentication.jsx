import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authAPI } from "../services/api";
import { Activity, Lock, Mail, UserPlus, LogIn, User } from "lucide-react";

const Authentication = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ name: "", surname: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const validateForm = () => {
    const name = formData.name.trim();
    const surname = formData.surname.trim();
    const email = formData.email.trim();
    const password = formData.password.trim();

    const emailRegex = /^\S+@\S+\.\S+$/;

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
        const res = await authAPI.login({ email: formData.email, password: formData.password });
        localStorage.setItem("jwt_token", res.data.jwt_token);
        navigate("/dashboard");
      } else {
        await authAPI.register(formData);
        localStorage.setItem("user_info", JSON.stringify({ name: formData.name, surname: formData.surname }));
        alert("Account created successfully. Please, sign in.");
        setIsLogin(true);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Invalid credentials or server error");
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100 items-center justify-center p-4">
      <div className="flex w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden">

        <div className="hidden md:flex w-1/2 bg-teal-700 text-white flex-col justify-center items-center p-10">
          <Activity size={64} className="mb-4" />
          <h1 className="text-3xl font-bold mb-2">EarlyCare Gateway</h1>
          <p className="text-center text-teal-100">
            AI Clinical Decision Support <br />
            {"(Authorized Access Only)"}
          </p>
        </div>

        <div className="w-full md:w-1/2 p-8 md:p-12">
          <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            {isLogin ? <LogIn className="text-teal-600" /> : <UserPlus className="text-teal-600" />}
            {isLogin ? "Welcome Back" : "New Doctor"}
          </h2>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 mb-4 rounded text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">

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

            <button
              type="submit"
              className="w-full bg-teal-600 hover:bg-teal-700 text-white font-bold p-3 rounded-lg transition duration-200 shadow-md mt-4"
            >
              {isLogin ? "Sign In" : "Create Account"}
            </button>
          </form>

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

export default Authentication;