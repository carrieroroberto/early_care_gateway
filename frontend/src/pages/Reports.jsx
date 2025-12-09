import React, { useState, useEffect } from 'react';
import { Search, FileText, Calendar, User, Filter, ChevronRight, Download } from 'lucide-react';

const Reports = () => {
  const [reports, setReports] = useState([]);   //Data archive
  const [loading, setLoading] = useState(true);  //Loading state
  const [searchTerm, setSearchTerm] = useState('');   //Search bar

  // MOCK DATA
  useEffect(() => {
    setTimeout(() => {
      setReports([
        { id: "REP-001", patient: "John Smith", date: "2025-11-28", type: "Multimodal", diagnosis: "Suspected Pneumonia", status: "high" },
        { id: "REP-002", patient: "Emily Johnson", date: "2025-11-27", type: "Classic", diagnosis: "Hypertension", status: "medium" },
        { id: "REP-003", patient: "Michael Brown", date: "2025-11-26", type: "Multimodal", diagnosis: "Negative", status: "low" },
        { id: "REP-004", patient: "Sarah Davis", date: "2025-11-25", type: "Classic", diagnosis: "Arrhythmia", status: "high" },
        { id: "REP-005", patient: "David Wilson", date: "2025-11-24", type: "Classic", diagnosis: "Type 2 Diabetes", status: "medium" },
      ]);
      setLoading(false);
    }, 800);
  }, []);

  // Filter Logic
  const filteredReports = reports.filter(r =>   //Creates an array that contains the matching elements
    r.patient.toLowerCase().includes(searchTerm.toLowerCase()) ||   //It checks if what the doctor wrote matches a name or an ID
    r.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  //Status Badge Colors
  const getStatusColor = (status) => {
    if (status === 'high') return 'bg-red-100 text-red-700 border-red-200';
    if (status === 'medium') return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    return 'bg-teal-100 text-teal-700 border-teal-200';
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 p-2 animate-fade-in">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports History</h1>
          <p className="text-gray-500 mt-1">Complete archive of performed diagnoses.</p>
        </div>
        <button className="flex items-center gap-2 bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 font-medium shadow-sm transition">
          <Download size={18} /> Export CSV
        </button>
      </div>

      {/* Search & Filters */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input 
            type="text" 
            placeholder="Search by patient name or ID..." 
            className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none transition"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition font-medium">
          <Filter size={18} /> Filters
        </button>
      </div>

      {/* Reports Table */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-gray-400">Loading archive...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                  <th className="p-6">Report ID</th>
                  <th className="p-6">Patient</th>
                  <th className="p-6">Date</th>
                  <th className="p-6">AI Mode</th>
                  <th className="p-6">Urgency</th>
                  <th className="p-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filteredReports.map((report) => (
                  <tr key={report.id} className="hover:bg-teal-50/50 transition duration-150 group">
                    <td className="p-6 font-mono text-sm text-gray-500 font-medium">
                      {report.id}
                    </td>
                    <td className="p-6">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-gray-500">
                          <User size={16} />
                        </div>
                        <span className="font-bold text-gray-700">{report.patient}</span>
                      </div>
                    </td>
                    <td className="p-6 text-gray-600 text-sm">
                      <div className="flex items-center gap-2">
                        <Calendar size={16} className="text-gray-400" />
                        {report.date}
                      </div>
                    </td>
                    <td className="p-6">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold border ${
                        report.type === 'Multimodale' ? 'bg-indigo-50 text-indigo-700 border-indigo-100' : 'bg-gray-100 text-gray-600 border-gray-200'
                      }`}>
                        {report.type === 'Multimodale' ? 'Advanced' : 'Classic'}
                      </span>
                    </td>
                    <td className="p-6">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getStatusColor(report.status)}`}>
                        {report.status === 'high' ? 'High' : report.status === 'medium' ? 'Medium' : 'Low'}
                      </span>
                    </td>
                    <td className="p-6 text-right">
                      <button className="text-teal-600 hover:text-teal-800 font-semibold text-sm flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        Details <ChevronRight size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        
        {!loading && filteredReports.length === 0 && (
          <div className="p-12 text-center text-gray-500">
            No reports found for "{searchTerm}"
          </div>
        )}
      </div>
    </div>
  );
};

export default Reports;