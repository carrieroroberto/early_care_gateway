// Import React hooks for state and lifecycle management
import { useState, useEffect } from "react";

// Import icons from lucide-react
import { Search, Calendar, User, CheckCircle } from "lucide-react";

// Import API functions and utility to hash patient fiscal codes
import { reportsAPI, hashPatientCf } from "../services/api";

// Reports component to display and manage the history of analyses
const Reports = () => {
  // State to store fetched reports
  const [reports, setReports] = useState([]);

  // State to manage loading status
  const [loading, setLoading] = useState(true);

  // State to manage search input for filtering reports
  const [searchTerm, setSearchTerm] = useState("");

  // State to hold the report selected for modal display
  const [selectedReport, setSelectedReport] = useState(null);

  // State to control modal visibility
  const [showModal, setShowModal] = useState(false);

  // Fetch all reports on component mount
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

  // Filter reports based on hashed patient fiscal code
  const filteredReports = searchTerm
    ? reports.filter((r) => r.patient_hashed_cf === hashPatientCf(searchTerm))
    : reports;

  // Open modal for a selected report
  const openModal = (report) => {
    setSelectedReport(report);
    setShowModal(true);
  };

  // Close modal
  const closeModal = () => {
    setSelectedReport(null);
    setShowModal(false);
  };

  // Format ISO date string into human-readable date and time
  const formatDateParts = (isoString) => {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");

    return {
      date: `${day}/${month}/${year}`,
      time: `${hours}:${minutes}:${seconds}`
    };
  };

  // Convert base64 image to URL for display
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

  // Map strategy codes to human-readable labels
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

  // Truncate long hashes for display
  const truncateHash = (hash, chars = 10) => {
    if (!hash) return "";
    return hash.length > chars ? `${hash.slice(0, chars)}...` : hash;
  };

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      {/* Page header */}
      <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports History</h1>
          <p className="text-gray-500 mt-2">Complete Archive of Performed Analysis</p>
        </div>
      </div>

      {/* Search bar */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search by patient fiscal code..."
            className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:border-teal-600 focus:ring-1 focus:ring-teal-600 outline-none transition"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value.toUpperCase())}
          />
        </div>
      </div>

      {/* Reports table */}
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
                <th className="p-4 w-1/5 text-center">Report ID</th>
                <th className="p-4 w-2/5 text-center">Patient Fiscal Code (Hashed)</th>
                <th className="p-4 w-2/5 text-center"><div className="flex flex-col">Date<span className="lowercase"> (dd/mm/yyyy hh:mm:ss)</span></div></th>
                <th className="p-4 w-1/5 text-center">Strategy</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredReports.map((report) => (
                <tr
                  key={report.id}
                  className="hover:bg-teal-50 cursor-pointer transition duration-150 text-center"
                  onClick={() => openModal(report)}
                >
                  {/* Report ID */}
                  <td className="p-4 font-mono text-gray-500">{report.id}</td>

                  {/* Hashed patient fiscal code */}
                  <td className="p-4">
                    <div className="flex items-center justify-center gap-3">
                      <div className="w-8 h-8 bg-teal-50 rounded-full flex items-center justify-center text-teal-600 border border-teal-600">
                        <User size={16} />
                      </div>
                      <span
                        className="font-medium text-gray-700 text-center"
                        title={report.patient_hashed_cf}
                      >
                        {truncateHash(report.patient_hashed_cf, 32)}
                      </span>
                    </div>
                  </td>

                  {/* Creation date */}
                  <td className="p-4">
                    <div className="flex items-center justify-center gap-3">
                      <div className="w-8 h-8 flex items-center justify-center text-gray-500">
                        <Calendar size={16} className="text-teal-600" />
                      </div>
                      {(() => {
                        const { date, time } = formatDateParts(report.created_at);
                        return (
                          <span className="text-gray-700 text-center">
                            <span className="font-medium">{date}</span> <span>{time}</span>
                          </span>
                        );
                      })()}
                    </div>
                  </td>

                  {/* Strategy label */}
                  <td className="p-4">
                    <span
                      className="px-4 py-2 rounded-full text-xs font-bold text-center bg-teal-50 border border-teal-600 text-teal-600"
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

      {/* Modal for selected report details */}
      {showModal && selectedReport && (
        <div style={{ margin: "unset" }} className="fixed inset-0 z-50 bg-black/70 flex justify-center items-center overflow-auto">
          {/* Close button */}
          <button
            className="absolute top-3 right-5 text-gray-300 hover:text-white text-xl"
            onClick={closeModal}
          >
            ✕
          </button>

          {/* Modal content */}
          <div className="
            bg-white rounded-xl shadow-xl border-t-4 border-teal-500
            overflow-hidden animate-slide-up
            mx-3
            inline-flex flex-col
            w-auto
            max-w-[90vw]
          ">
            {/* Header */}
            <div className="bg-teal-50 p-4 border-b border-teal-100 flex items-center gap-2">
              <CheckCircle className="text-teal-600" size={20} />
              <h3 className="font-bold text-teal-900">Analysis Result</h3>
            </div>

            {/* Body: diagnosis, confidence, explanation */}
            <div className="flex flex-row items-start gap-14 p-6 flex-wrap">
              {/* Diagnosis and confidence */}
              <div className="flex flex-col space-y-4 shrink-0 max-w-[300px] break-words">
                <div>
                  <span className="text-xs font-bold text-gray-400 uppercase">Diagnosis</span>
                  <p className="text-2xl font-bold text-gray-900 whitespace-normal">
                    {selectedReport.diagnosis}
                  </p>
                </div>

                <div>
                  <span className="text-xs font-bold text-gray-400 uppercase">Confidence</span>
                  <p className="text-xl font-bold text-gray-900 whitespace-normal">
                    {(selectedReport.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              {/* Explanation */}
              <div className="flex flex-col shrink-0 max-w-[450px] break-words">
                {selectedReport.explanation && (
                  selectedReport.strategy.startsWith("img") ? (
                    <div className="space-y-2 w-[350px]">
                      <span className="text-xs font-bold text-teal-600 uppercase">Heatmap (Grad-CAM)</span>
                      <img
                        src={base64ToUrl(selectedReport.explanation)}
                        alt="Heatmap"
                        className="rounded-lg object-cover w-full h-full"
                      />
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <span className="text-xs font-bold text-teal-600 uppercase">Explanation</span>

                      {/* Explanation table or raw text */}
                      {(() => {
                        try {
                          const parsed = JSON.parse(selectedReport.explanation);
                          if (Array.isArray(parsed)) {
                            return (
                              <div className="overflow-auto max-h-[420px] w-full rounded-lg border pr-4">
                                <table className="text-sm border-collapse whitespace-nowrap w-full">
                                  <thead className="bg-gray-100 sticky top-0">
                                    <tr>
                                      <th className="border p-2 w-24 h-10 text-center">Feature</th>
                                      <th className="border p-2 w-20 h-10 text-center">Value</th>
                                      <th className="border p-2 w-20 h-10 text-center">Impact</th>
                                      <th className="border p-2 w-28 h-10 text-center">Effect</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {parsed.map((item, idx) => (
                                      <tr key={idx} className="even:bg-gray-50">
                                        <td className="border p-2 w-24 h-10 text-center">{item.Feature}</td>
                                        <td className="border p-2 w-20 h-10 text-center">{item.Value.toFixed(2)}</td>
                                        <td className="border p-2 text-center">{item.Impact_score.toFixed(2)}</td>
                                        <td className="border p-2 w-28 h-10 text-center">{item.Effect}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            );
                          } else {
                            return (
                              <p className="text-sm text-gray-700 italic whitespace-pre-wrap break-words text-justify">
                                {selectedReport.explanation}
                              </p>
                            );
                          }
                        } catch {
                          return (
                            <p className="text-sm text-gray-700 italic whitespace-pre-wrap break-words text-justify">
                              {selectedReport.explanation}
                            </p>
                          );
                        }
                      })()}
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Export the Reports component
export default Reports;