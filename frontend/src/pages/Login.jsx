//Handle login and registration
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { Activity, Lock, Mail, UserPlus, LogIn, User } from 'lucide-react';

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);   //If this var is true then it shows welcome back
  const [formData, setFormData] = useState({ name: '', surname: '', email: '', password: '' });   //Form to registrate
  const [error, setError] = useState('');  //If login fails then it this will be the error
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();   //Don't refresh
    setError('');   //Cleans previous errors
    
    try {
      if (isLogin) {   //The user wants to login
        const res = await authAPI.login({ email: formData.email, password: formData.password });   //Calls the function in api.js to POST in backend. It sends email and password as payload
        localStorage.setItem('jwt_token', res.data.token);   //It saves the token taken from the JSON response sent by the server
        navigate('/dashboard');   //Login went well, now it goes to /dashboard
      } else {   //The user wants to registrate
        await authAPI.register(formData);  //We give the whole form, including name and surname this time
        alert('Registration successful! Please login.');
        setIsLogin(true);   //After the user is registred it switches back to the login page
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Invalid credentials or server error');
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100 items-center justify-center p-4">
      <div className="flex w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden">
        
        {/* Left Side */}
        <div className="hidden md:flex w-1/2 bg-teal-700 text-white flex-col justify-center items-center p-10">
          <Activity size={64} className="mb-4" />
          <h1 className="text-3xl font-bold mb-2">EarlyCare Gateway</h1>
          <p className="text-center text-teal-100">
            Clinical Decision Support System. <br/>
            Professional Access Only.
          </p>
        </div>

        {/* Right Side (Form) */}
        <div className="w-full md:w-1/2 p-8 md:p-12">
          <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            {isLogin ? <LogIn className="text-teal-600"/> : <UserPlus className="text-teal-600"/>}
            {isLogin ? 'Welcome Back' : 'New Doctor'}
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
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Name</label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 text-gray-400" size={18} />
                    <input
                      type="text"
                      placeholder="John"
                      className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Surname</label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 text-gray-400" size={18} />
                    <input
                      type="text"
                      placeholder="Doe"
                      className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                      onChange={(e) => setFormData({...formData, surname: e.target.value})}
                    />
                  </div>
                </div>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-gray-400" size={18} />
                <input
                  type="email"
                  className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                  placeholder="doctor@hospital.com"
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={18} />
                <input
                  type="password"
                  className="w-full pl-10 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 outline-none"
                  placeholder="••••••••"
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-teal-600 hover:bg-teal-700 text-white font-bold p-3 rounded-lg transition duration-200 shadow-md mt-4"
            >
              {isLogin ? 'Login' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            {isLogin ? "Don't have an account? " : "Already have credentials? "}
            <button 
              onClick={() => { setError(''); setIsLogin(!isLogin); }}
              className="text-teal-600 font-semibold hover:underline"
            >
              {isLogin ? 'Register now' : 'Sign In'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;