import { useState, useEffect } from "react";
import { Search, Calendar, User } from "lucide-react";
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

  const filteredReports = searchTerm
    ? reports.filter((r) => r.patient_hashed_cf === hashPatientCf(searchTerm))
    : reports;

  const openModal = (report) => {
    setSelectedReport(report);
    setShowModal(true);
  };

  const closeModal = () => {
    setSelectedReport(null);
    setShowModal(false);
  };

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    return `${day}/${month}/${year} ${hours}:${minutes}`;
  };

  const base64ToUrl = (base64, mimeType = "image/jpeg") => {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: mimeType });

    return URL.createObjectURL(blob);
  };

  const getStrategyLabel = (strategy) => {
    switch (strategy) {
      case "text":
        return "Textual";
      case "img_rx":
        return "Imaging (X-Ray)";
      case "img_skin":
        return "Imaging (Skin)";
      case "numeric":
        return "Cardio Risk";
      case "signal":
        return "ECG Signal";
      default:
        return strategy;
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports History</h1>
          <p className="text-gray-500 mt-2">Complete Archive of Performed Analysis</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search by patient fiscal code..."
            className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:outline-none transition"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-x-auto">
        {loading ? (
          <div className="p-12 text-center text-gray-400">Loading history...</div>
        ) : filteredReports.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            {searchTerm ? `No reports found for "${searchTerm}"` : "No reports found"}
          </div>
        ) : (
          <table className="w-full table-fixed text-left border-collapse">
            <thead className="bg-gray-50 border-b border-gray-200 text-xs uppercase text-gray-500 font-semibold">
              <tr>
                <th className="p-4 w-1/4 text-center">Report ID</th>
                <th className="p-4 w-1/4 text-center">Patient Fiscal Code (Hashed)</th>
                <th className="p-4 w-1/4 text-center">Date</th>
                <th className="p-4 w-1/4 text-center">Strategy</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredReports.map((report) => (
                <tr
                  key={report.id}
                  className="hover:bg-teal-50 cursor-pointer transition duration-150 text-center"
                  onClick={() => openModal(report)}
                >
                <td className="p-4 font-mono text-gray-500">{report.id}</td>
                <td className="p-4">
                  <div className="flex items-center justify-center gap-3">
                    <div className="w-8 h-8 bg-teal-50 rounded-full flex items-center justify-center text-teal-600 border border-teal-600">
                      <User size={16} />
                    </div>
                    <span className="font-medium text-gray-700 text-center">{report.patient_hashed_cf}</span>
                  </div>
                </td>
                <td className="p-4">
                  <div className="flex items-center justify-center gap-3">
                    <div className="w-8 h-8 flex items-center justify-center text-gray-500">
                      <Calendar size={20} className="text-teal-600" />
                    </div>
                    <span className="font-medium text-gray-700 text-center">{formatDate(report.created_at)}</span>
                  </div>
                </td>
                <td className="p-4">
                  <span
                    className="px-4 py-2 rounded-full text-xs font-bold text-white text-center"
                    style={{ backgroundColor: "#0d9488" }}
                  >
                    {getStrategyLabel(report.strategy)}
                  </span>
                </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {showModal && selectedReport && (
        <div className="fixed inset-0 z-50 bg-black/70 flex justify-center items-center overflow-auto" style={{ marginTop: "unset" }}>
          <div className="bg-white rounded-lg p-6 w-96 max-w-full max-h-full relative shadow-lg">
            <button
              className="absolute top-1 right-3 text-gray-500 hover:text-gray-700 text-lg"
              onClick={closeModal}
            >
              ✕
            </button>
            <h2 className="text-lg font-bold mb-2">Report Details</h2>
            <p>
              <strong>Diagnosis:</strong> {selectedReport.diagnosis}
            </p>
            <p>
              <strong>Confidence:</strong> {(selectedReport.confidence * 100).toFixed(2)}%
            </p>
            <div className="mt-4">
              <strong>Explanation:</strong>
              {selectedReport.explanation ? (
                ["img_rx", "img_skin"].includes(selectedReport.strategy) ? (
                  <img
                    src={base64ToUrl(selectedReport.explanation)}
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