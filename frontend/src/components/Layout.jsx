import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { Activity, FileText, LogOut, User } from "lucide-react";

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("jwt_token");
    navigate("/");
  };

  const navItems = [
    { path: "/dashboard", label: "New Analysis", icon: <Activity size={20} /> },
    { path: "/dashboard/reports", label: "Reports History", icon: <FileText size={20} /> },
  ];

  const storedUser = localStorage.getItem("user_info");
  const userInfo = storedUser ? JSON.parse(storedUser) : null;
  const displayName = userInfo ? `Dr. ${userInfo.name} ${userInfo.surname}` : "Dr. User";

  return (
    <div className="flex h-screen bg-gray-100 font-sans"> 
      <aside className="w-64 bg-white shadow-xl flex flex-col z-10">

        <div className="p-6 border-b flex flex-col items-center gap-3">
          <div className="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center text-white font-bold shadow-sm">
            <Activity size={18} />
          </div>
          <div className="flex flex-col justify-center items-center">
            <span className="text-lg font-bold text-gray-800 tracking-tight">EarlyCare Gateway</span>
            <p className="text-gray-500 mt-1">AI Clinical Decision Support</p>
          </div>
        </div>
        
        <nav className="flex-1 p-4 space-y-2 mt-2">
          {navItems.map((item) => (   
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all duration-200 ${
                location.pathname === item.path 
                  ? "bg-teal-50 text-teal-700 font-semibold border-r-4 border-teal-600 shadow-sm" 
                  : "text-gray-600 hover:bg-gray-50 hover:text-teal-600"
              }`}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t bg-gray-50">
          <div className="flex items-center gap-3 mb-4 px-2">
            <div className="w-10 h-10 bg-teal-50 rounded-full flex items-center justify-center border border-teal-600">
              <User size={20} className="text-teal-600"/>
            </div>
            <div>

              <p className="text-sm font-bold text-gray-800">{displayName}</p>
              <p className="text-xs text-gray-500">Authorized Doctor</p>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 text-red-600 hover:bg-red-50 p-2 rounded-lg transition text-sm font-medium"
          >
            <LogOut size={16} /> Logout
          </button>
        </div>
      </aside>

      <main className="w-full h-full flex-1 overflow-y-auto p-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;