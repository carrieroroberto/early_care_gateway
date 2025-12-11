import React, { useState, useEffect } from "react";
import { Search, Calendar, User, ChevronRight } from "lucide-react";
import { reportsAPI, hashPatientCf } from "../services/api";

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedReport, setSelectedReport] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const response = await reportsAPI.getAll();
        setReports(response.data.reports);
      } catch (error) {
        console.error("Error fetching reports:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  const filteredReports = reports.filter(r => r.patient_hashed_cf === hashPatientCf(searchTerm));

  const openModal = (report) => {
    setSelectedReport(report);
    setShowModal(true);
  };

  const closeModal = () => {
    setSelectedReport(null);
    setShowModal(false);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 p-2 animate-fade-in">
      <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports History</h1>
          <p className="text-gray-500 mt-1">Complete archive of performed analysis.</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input 
            type="text" 
            placeholder="Search by patient tax ID code..." 
            className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none transition"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-gray-400">Loading history...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                  <th className="p-6">Report ID</th>
                  <th className="p-6">Patient Hashed Tax ID Code (CF)</th>
                  <th className="p-6">Created At</th>
                  <th className="p-6">Strategy</th>
                  <th className="p-6 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filteredReports.map((report) => (
                  <tr key={report.id} className="hover:bg-teal-50/50 transition duration-150 group">
                    <td className="p-6 font-mono text-sm text-gray-500 font-medium">{report.id}</td>
                    <td className="p-6 flex items-center gap-3">
                      <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-gray-500">
                        <User size={16} />
                      </div>
                      <span className="font-bold text-gray-700">{report.patient_hashed_cf}</span>
                    </td>
                    <td className="p-6 text-gray-600 text-sm flex items-center gap-2">
                      <Calendar size={16} className="text-gray-400" />
                      {report.created_at}
                    </td>
                    <td className="p-6">
                      <span className={"px-3 py-1 rounded-full text-xs font-bold border bg-gray-100 text-gray-600 border-gray-200"}>
                        {report.strategy}
                      </span>
                    </td>
                    <td className="p-6 text-right">
                      <button 
                        className="text-teal-600 hover:text-teal-800 font-semibold text-sm flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => openModal(report)}
                      >
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

      {showModal && selectedReport && (
        <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-full relative shadow-lg">
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-lg"
              onClick={closeModal}
            >
            ✕
            </button>
            <h2 className="text-lg font-bold mb-2">Report Details</h2>
            <p><strong>Diagnosis:</strong> {selectedReport.diagnosis}</p>
            <p><strong>Confidence:</strong> {(selectedReport.confidence * 100).toFixed(2)}%</p>
            <div className="mt-4">
              <strong>Explanation:</strong>
              {selectedReport.explanation ? (
                ["image_rx", "image_skin"].includes(selectedReport.strategy) ? (
                  <img 
                    src={selectedReport.explanation} 
                    alt="Explanation" 
                    className="mt-2 w-full rounded border" 
                  />
                ) : (
                  <p className="mt-2 whitespace-pre-wrap">{selectedReport.explanation}</p>
                )
              ) : (
                <p className="mt-2 text-gray-500">No explanation available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;