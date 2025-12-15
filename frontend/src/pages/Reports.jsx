import { useState } from "react";
import { aiAPI } from "../services/api";
import { Activity, FileText, Image, Upload, Brain, ArrowRight, CheckCircle, BarChart2, Scan, User } from "lucide-react";

// List of features used for the heart disease model
const HEART_FEATURES = [
  "age", "trestbps", "chol", "thalch", "oldpeak", "ca", "sex_Male",
  "cp_atypical angina", "cp_non-anginal", "cp_typical angina", "fbs_True",
  "restecg_normal", "restecg_st-t abnormality", "exang_True", "slope_flat", "slope_upsloping",
  "thal_normal", "thal_reversable defect"
];

// Labels for the heart features to display in the UI
const CARDIO_LABELS = {
  age: "Age",
  trestbps: "Resting Blood Pressure (mmHg)",
  chol: "Cholesterol (mg/dL)",
  thalch: "Max Heart Rate Achieved",
  oldpeak: "ST Depression Induced by Exercise",
  ca: "Number of Major Vessels Colored by Fluoroscopy",
  sex: "Sex",
  cp: "Chest Pain Type",
  fbs: "Fasting Blood Sugar > 120 mg/dL",
  restecg: "Resting ECG",
  exang: "Exercise Induced Angina",
  slope: "ST Segment Slope",
  thal: "Thalassemia"
};

const Analysis = () => {
  // State for the currently active tab
  const [activeTab, setActiveTab] = useState("text");
  // Loading state while waiting for analysis results
  const [loading, setLoading] = useState(false);
  // Holds the analysis result from the API
  const [result, setResult] = useState(null);

  // Input states for different types of analysis
  const [textInput, setTextInput] = useState(""); // clinical notes
  const [signalInput, setSignalInput] = useState(""); // ECG signal
  const [selectedFile, setSelectedFile] = useState(null); // uploaded image file
  const [previewUrl, setPreviewUrl] = useState(null); // preview URL for uploaded image
  const [imageType, setImageType] = useState("x-ray"); // type of image (x-ray or skin)

  // Initial state for cardio features, all set to empty string
  const initialCardioState = Object.fromEntries(HEART_FEATURES.map(key => [key, ""]));
  const [cardioData, setCardioData] = useState(initialCardioState);

  // State for patient's fiscal code
  const [patientCf, setPatientCf] = useState("");

  // Validates the fiscal code length
  const validateCf = (cf) => {
    if (cf.length !== 16) throw new Error("Fiscal code must have 16 characters.");
    return cf;
  };

  // Handles file selection and creates a preview URL
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  // Converts a file to a Base64 string (without the prefix)
  const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => resolve(fileReader.result.split(",")[1]);
      fileReader.onerror = (error) => reject(error);
    });
  };

  // Builds a numeric vector from cardio input suitable for the model
  function buildHeartFeatureVector(data) {
    const out = [];
    HEART_FEATURES.forEach(feature => {
      if (!feature.includes("_") && feature !== "sex_Male") {
        out.push(parseFloat(data[feature]) || 0); // numeric features
        return;
      }

      if (feature === "sex_Male") {
        out.push(data.sex === "1" ? 1 : 0); // binary encoding for sex
        return;
      }

      if (feature.startsWith("cp_")) {
        const label = feature.replace("cp_", "");
        out.push(data.cp === label ? 1 : 0); // one-hot encoding for chest pain
        return;
      }

      if (feature === "fbs_True") {
        out.push(data.fbs === "1" ? 1 : 0); // binary encoding for fasting blood sugar
        return;
      }

      if (feature.startsWith("restecg_")) {
        const label = feature.replace("restecg_", "");
        out.push(data.restecg === label ? 1 : 0); // one-hot encoding for resting ECG
        return;
      }

      if (feature === "exang_True") {
        out.push(data.exang === "1" ? 1 : 0); // binary encoding for exercise-induced angina
        return;
      }

      if (feature.startsWith("slope_")) {
        const label = feature.replace("slope_", "");
        out.push(data.slope === label ? 1 : 0); // one-hot encoding for ST slope
        return;
      }

      if (feature.startsWith("thal_")) {
        const label = feature.replace("thal_", "");
        out.push(data.thal === label ? 1 : 0); // one-hot encoding for thalassemia
        return;
      }

      out.push(0); // fallback
    });

    return out;
  }

  // Validates that all required cardio fields are filled
  function validateCardioData(data) {
    HEART_FEATURES.forEach(feature => {
      if (!feature.includes("_") && feature !== "sex_Male") {
        if (data[feature] === "" || data[feature] === null) {
          throw new Error(`Field "${feature}" is required.`);
        }
      }
    });

    const requiredCategorical = ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal"];
    requiredCategorical.forEach(key => {
      if (!data[key]) {
        throw new Error(`Field "${key}" is required.`);
      }
    });
  }

  // Main function to handle analysis request
  const handleAnalyse = async () => {
    setLoading(true);
    setResult(null);

    try {
      let rawDataString = "";
      let strategy = "";
      const hashedCf = validateCf(patientCf); // validate fiscal code

      // Prepare input based on active tab
      if (activeTab === "text") {
        if (!textInput) throw new Error("Please enter clinical notes.");
        rawDataString = textInput;
        strategy = "text";
      } else if (activeTab === "image") {
        if (!selectedFile) throw new Error("Please upload an image.");
        rawDataString = await convertBase64(selectedFile);
        strategy = imageType === "x-ray" ? "img_rx" : "img_skin";
      } else if (activeTab === "numeric") {
        validateCardioData(cardioData);
        const vector = buildHeartFeatureVector(cardioData);
        rawDataString = JSON.stringify(vector);
        strategy = "numeric";
      } else if (activeTab === "signal") {
        if (!signalInput) throw new Error("Please enter signal data.");
        const arr = signalInput.split(",")
          .map(val => parseFloat(val.trim()))
          .filter(val => !isNaN(val));
        if (arr.length === 0) throw new Error("Invalid signal format.");
        rawDataString = JSON.stringify(arr);
        strategy = "signal";
      }

      const payload = {
        patient_hashed_cf: patientCf, // hashed fiscal code
        strategy,
        raw_data: rawDataString
      };

      console.log("Sending to gateway:", payload);
      resetAllInputs(); // clear inputs after sending
      setPatientCf("");

      const response = await aiAPI.analyse(payload); // call AI API
      setResult(response.data.report);

    } catch (error) {
      console.error(error);
      alert("Analysis Failed: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Reset all input fields
  const resetAllInputs = () => {
    setTextInput("");
    setSignalInput("");
    setPreviewUrl(null);
    setSelectedFile(null);
    setCardioData(initialCardioState);
  };

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-8 animate-fade-in">

      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Diagnostic Hub</h1>
        <p className="text-gray-500 mt-2">Execute AI Multimodal Analysis</p>
      </div>

      {/* Fiscal code input and tab navigation */}
      <div className="flex gap-8 w-max">
        <div className="flex flex-col">
          <label className="text-xs font-bold text-gray-500 uppercase mb-1">Fiscal Code <span className="text-red-500">*</span></label>
          <input
            type="text"
            value={patientCf}
            onChange={e => setPatientCf(e.target.value.toUpperCase())}
            placeholder="Insert text value"
            maxLength={16}
            className="w-full pl-4 pr-4 py-2.5 border border-gray-300 rounded-lg focus:border-teal-600 focus:ring-1 focus:ring-teal-600 outline-none transition"
          />
        </div>

        {/* Tab buttons for different analysis types */}
        <div className="flex border-b border-gray-200 overflow-x-hidden w-max">
          {[
            { id: "text", label: "Textual", icon: FileText },
            { id: "image", label: "Imaging (X-Ray/Skin)", icon: Image },
            { id: "numeric", label: "Cardio Risk", icon: Activity },
            { id: "signal", label: "ECG Signal", icon: BarChart2 },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => { setActiveTab(tab.id); setResult(null); resetAllInputs(); }}
              className={`flex items-center gap-2 px-6 py-2.5 font-semibold transition-all rounded-t-lg border-b-2 ${activeTab === tab.id
                ? "border-teal-600 text-teal-700 bg-teal-50"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50"
              }`}
            >
              <tab.icon size={18} /> {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main content area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-200">

          {/* Text input tab */}
          {activeTab === "text" && (
            <div className="space-y-4">
              <label className="font-bold text-gray-700">Symptoms Description</label> <span className="text-red-500">*</span>
              <textarea
                className="w-full h-64 p-4 border-2 border-gray-300 rounded-lg focus:border-teal-600 outline-none font-mono text-sm"
                placeholder="Ex: The patient complains of severe tachycardia and sweating..."
                value={textInput}
                onChange={e => setTextInput(e.target.value)}
              />
            </div>
          )}

          {/* Image input tab */}
          {activeTab === "image" && (
            <div className="space-y-6">
              {/* Image type selection */}
              <div>
                <label className="block font-bold text-gray-700 mb-3">Select Image Type</label>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => { setImageType("x-ray"); resetAllInputs(); }}
                    className={`p-4 rounded-lg border flex flex-col items-center gap-2 transition-all ${imageType === "x-ray"
                      ? "border-teal-600 bg-teal-50 text-teal-800 ring-1 ring-teal-600"
                      : "border-gray-200 hover:border-gray-300 text-gray-500"
                    }`}
                  >
                    <Scan size={24} />
                    <span className="font-semibold">X-Ray</span>
                  </button>

                  <button
                    onClick={() => { setImageType("skin"); resetAllInputs(); }}
                    className={`p-4 rounded-lg border flex flex-col items-center gap-2 transition-all ${imageType === "skin"
                      ? "border-teal-600 bg-teal-50 text-teal-800 ring-1 ring-teal-600"
                      : "border-gray-200 hover:border-gray-300 text-gray-500"
                    }`}
                  >
                    <User size={24} />
                    <span className="font-semibold">Skin Lesion</span>
                  </button>
                </div>
              </div>

              {/* File upload section */}
              <div>
                <div className="flex gap-1">
                  <label className="block font-bold text-gray-700 mb-3">
                    Upload {imageType === "x-ray" ? "X-Ray" : "Skin Lesion"} Image
                  </label>
                  <span className="text-red-500">*</span>
                </div>
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center bg-gray-50 hover:bg-gray-100 transition">
                  <input type="file" onChange={handleFileChange} className="hidden" id="file-upload" accept="image/*" />
                  <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                    {previewUrl ? (
                      <img src={previewUrl} alt="Preview" className="h-64 object-contain rounded shadow-sm" />
                    ) : (
                      <>
                        <Upload size={48} className="text-gray-400 mb-3" />
                        <span className="text-gray-600 font-bold">Click to Upload</span>
                        <span className="text-xs text-gray-400 mt-1">JPEG Recommended</span>
                      </>
                    )}
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* Numeric input tab */}
          {activeTab === "numeric" && (
            <div className="space-y-2">
              <h3 className="font-bold text-gray-700 border-b pb-2">Clinical Parameters</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-2">

                {/* Numeric inputs */}
                {["age", "trestbps", "chol", "thalch", "oldpeak", "ca"].map(key => (
                  <InputGroup
                    key={key}
                    label={CARDIO_LABELS[key]}
                    type="number"
                    val={cardioData[key]}
                    setter={v => setCardioData({ ...cardioData, [key]: v })}
                  />
                ))}

                {/* Select dropdowns for categorical features */}
                <SelectGroup
                  label={CARDIO_LABELS.sex}
                  val={cardioData.sex}
                  setter={v => setCardioData({ ...cardioData, sex: v })}
                  options={[
                    { value: "1", label: "Male" },
                    { value: "0", label: "Female" }
                  ]}
                />

                <SelectGroup
                  label={CARDIO_LABELS.cp}
                  val={cardioData.cp}
                  setter={v => setCardioData({ ...cardioData, cp: v })}
                  options={[
                    { value: "typical angina", label: "Typical Angina" },
                    { value: "atypical angina", label: "Atypical Angina" },
                    { value: "non-anginal", label: "Non-anginal" },
                    { value: "asymptomatic", label: "Asymptomatic" }
                  ]}
                />

                <SelectGroup
                  label={CARDIO_LABELS.fbs}
                  val={cardioData.fbs}
                  setter={v => setCardioData({ ...cardioData, fbs: v })}
                  options={[
                    { value: "1", label: "True" },
                    { value: "0", label: "False" }
                  ]}
                />

                <SelectGroup
                  label={CARDIO_LABELS.restecg}
                  val={cardioData.restecg}
                  setter={v => setCardioData({ ...cardioData, restecg: v })}
                  options={[
                    { value: "normal", label: "Normal" },
                    { value: "st-t abnormality", label: "ST-T Abnormality" },
                    { value: "hypertrophy", label: "Hypertrophy" }
                  ]}
                />

                <SelectGroup
                  label={CARDIO_LABELS.exang}
                  val={cardioData.exang}
                  setter={v => setCardioData({ ...cardioData, exang: v })}
                  options={[
                    { value: "1", label: "Yes" },
                    { value: "0", label: "No" }
                  ]}
                />

                <SelectGroup
                  label={CARDIO_LABELS.slope}
                  val={cardioData.slope}
                  setter={v => setCardioData({ ...cardioData, slope: v })}
                  options={[
                    { value: "flat", label: "Flat" },
                    { value: "upsloping", label: "Upsloping" },
                    { value: "downsloping", label: "Downsloping" }
                  ]}
                />

                <SelectGroup
                  label={CARDIO_LABELS.thal}
                  val={cardioData.thal}
                  setter={v => setCardioData({ ...cardioData, thal: v })}
                  options={[
                    { value: "normal", label: "Normal" },
                    { value: "fixed defect", label: "Fixed Defect" },
                    { value: "reversable defect", label: "Reversable Defect" }
                  ]}
                />
              </div>
            </div>
          )}

          {/* Signal input tab */}
          {activeTab === "signal" && (
            <div className="space-y-2">
              <label className="font-bold text-gray-700">ECG Signal Samples</label> <span className="text-red-500">*</span>
              <p className="text-s text-gray-500">Paste comma-separated voltage values</p>
              <textarea
                className="w-full h-64 p-4 border-2 border-gray-300 rounded-lg focus:border-teal-600 outline-none font-mono text-sm"
                placeholder="0.05, 0.12, 0.85, -0.20, 0.05..."
                value={signalInput}
                onChange={e => setSignalInput(e.target.value)}
              />
            </div>
          )}

          {/* Analysis button */}
          <div className="mt-6 flex justify-end">
            <button onClick={handleAnalyse} disabled={loading} className={`flex items-center gap-2 px-8 py-3 rounded-lg font-bold text-white shadow-md transition-transform duration-100 ease-out transform hover:scale-105 ${loading ? "bg-gray-400" : "bg-teal-600 hover:bg-teal-700"}`}>
              {loading ? "Processing..." : <>Run Analysis <ArrowRight size={20} /></>}
            </button>
          </div>
        </div>

        {/* Result panel */}
        <div className="w-auto h-full">
          {result ? (
            <div className={`bg-white rounded-xl shadow-lg border-t-4 border-teal-500 w-max min-w-[400px] ${result.strategy === "numeric" ? "max-w-[500px]" : "max-w-[400px]"
              }`}>

              {/* Result header */}
              <div className="bg-teal-50 p-4 border-b border-teal-100 flex items-center gap-2">
                <CheckCircle className="text-teal-600" size={20} />
                <h3 className="font-bold text-teal-900">Analysis Result</h3>
              </div>

              {/* Result content */}
              <div className="p-6" style={{ paddingTop: "12px" }}>

                {result.diagnosis && (
                  <div className="space-y-2">
                    <div>
                      <span className="text-xs font-bold text-gray-400 uppercase">Diagnosis</span>
                      <p className="text-2xl font-bold text-gray-900">{result.diagnosis}</p>
                    </div>

                    {result.confidence && (
                      <div>
                        <span className="text-xs font-bold text-gray-400 uppercase">Confidence</span>
                        <p className="text-xl font-bold text-gray-900">
                          {(result.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                    )}

                    {result.explanation && (
                      result.strategy?.startsWith("img") ? (
                        // Image-based explanation (Grad-CAM heatmap)
                        <div className="space-y-2">
                          <span className="text-xs font-bold text-teal-600 uppercase">Heatmap (Grad-CAM)</span>
                          <img
                            src={`data:image/jpeg;base64,${result.explanation}`}
                            alt="Heatmap"
                            className="rounded-lg border border-orange-200 w-full"
                          />
                        </div>
                      ) : result.strategy === "numeric" ? (
                        // Numeric explanation (table)
                        <div className="space-y-2">
                          <span className="text-xs font-bold text-teal-600 uppercase">Explanation</span>
                          <div className="overflow-auto max-h-[420px] w-full rounded-lg border pr-4">
                            <table className="text-sm border-collapse whitespace-nowrap">
                              <thead className="bg-gray-100 sticky top-0">
                                <tr>
                                  <th className="border p-2 text-center">Feature</th>
                                  <th className="border p-2 text-center">Value</th>
                                  <th className="border p-2 text-center">Impact</th>
                                  <th className="border p-2 text-center">Effect</th>
                                </tr>
                              </thead>
                              <tbody>
                                {JSON.parse(result.explanation).map((item, idx) => (
                                  <tr key={idx} className="even:bg-gray-50">
                                    <td className="border p-2 text-center">{item.Feature}</td>
                                    <td className="border p-2 text-center">{item.Value.toFixed(2)}</td>
                                    <td className="border p-2 text-center">{item.Impact_score.toFixed(2)}</td>
                                    <td className="border p-2 text-center">{item.Effect}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>

                          </div>
                        </div>
                      ) : (
                        // Textual explanation
                        <div className="space-y-2">
                          <span className="text-xs font-bold text-teal-600 uppercase">Explanation</span>
                          <p className="text-sm text-gray-700 italic text-justify">{result.explanation}</p>
                        </div>
                      )
                    )}
                  </div>
                )}
              </div>
            </div>
          ) : (
            // Placeholder when no results are available
            <div className="h-full bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400 p-6 text-center">
              <Brain size={40} className="mb-3 opacity-20 animate-bounce" />
              {!loading ? (<p>Waiting for Data...</p>) : (<p>Running Analysis. Please, wait...</p>)}
            </div>
          )}
        </div>
      </div>
    </div>
  )
};

// Component for numeric inputs
const InputGroup = ({ label, type = "text", val, setter, step }) => (
  <div>
    <label className="text-xs font-bold text-gray-500 uppercase">{label}</label> <span className="text-red-500">*</span>
    <input
      type={type}
      step={step}
      placeholder="Insert numeric value"
      className="w-full p-2 border rounded-lg focus:border-teal-600 focus:ring-1 focus:ring-teal-600 outline-none transition"
      value={val}
      onChange={e => setter(e.target.value)}
    />
  </div>
);

// Component for dropdown selections
const SelectGroup = ({ label, val, setter, options }) => (
  <div className="flex flex-col">
    <div>
      <label className="text-xs font-bold text-gray-500 uppercase">{label}</label> <span className="text-red-500">*</span>
    </div>
    <select
      className="w-full p-2 border border-gray-300 rounded-lg focus:border-teal-600 focus:ring-1 focus:ring-teal-600 outline-none transition"
      value={val}
      onChange={e => setter(e.target.value)}
    >
      <option value="" selected disabled>Select...</option>
      {options.map(opt => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  </div>
);

export default Analysis;