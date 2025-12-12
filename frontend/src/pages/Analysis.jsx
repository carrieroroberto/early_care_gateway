import { useState } from "react";
import { aiAPI } from "../services/api";
import { Activity, FileText, Image, Upload, Brain, ArrowRight, AlertTriangle, CheckCircle, BarChart2, Scan, User } from "lucide-react";

const HEART_FEATURES = [
  "age", "trestbps", "chol", "thalch", "oldpeak", "ca", "sex_Male",
  "cp_atypical angina", "cp_non-anginal", "cp_typical angina", "fbs_True",
  "restecg_normal", "restecg_st-t abnormality", "exang_True", "slope_flat", "slope_upsloping",
  "thal_normal", "thal_reversable defect"
];

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
  const [activeTab, setActiveTab] = useState("text"); 
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const [textInput, setTextInput] = useState("");
  const [signalInput, setSignalInput] = useState(""); 
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [imageType, setImageType] = useState("x-ray");

  const initialCardioState = Object.fromEntries(HEART_FEATURES.map(key => [key, ""]));
  const [cardioData, setCardioData] = useState(initialCardioState);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => resolve(fileReader.result.split(",")[1]);
      fileReader.onerror = (error) => reject(error);
    });
  };

  function buildHeartFeatureVector(data) {
    const out = [];
    HEART_FEATURES.forEach(feature => {
      if (!feature.includes("_") && feature !== "sex_Male") {
        out.push(parseFloat(data[feature]) || 0);
        return;
      }

      if (feature === "sex_Male") {
        out.push(data.sex === "1" ? 1 : 0);
        return;
      }

      if (feature.startsWith("cp_")) {
        const label = feature.replace("cp_", "");
        out.push(data.cp === label ? 1 : 0);
        return;
      }

      if (feature === "fbs_True") {
        out.push(data.fbs === "1" ? 1 : 0);
        return;
      }

      if (feature.startsWith("restecg_")) {
        const label = feature.replace("restecg_", "");
        out.push(data.restecg === label ? 1 : 0);
        return;
      }

      if (feature === "exang_True") {
        out.push(data.exang === "1" ? 1 : 0);
        return;
      }

      if (feature.startsWith("slope_")) {
        const label = feature.replace("slope_", "");
        out.push(data.slope === label ? 1 : 0);
        return;
      }

      if (feature.startsWith("thal_")) {
        const label = feature.replace("thal_", "");
        out.push(data.thal === label ? 1 : 0);
        return;
      }

      out.push(0);
    });

    return out;
  }

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

  const handleAnalyse = async () => {
    setLoading(true);
    setResult(null);

    try {
      let rawDataString = ""; 
      let strategy = "";

      if (activeTab === "text") {
        if (!textInput) throw new Error("Please enter clinical notes.");
        rawDataString = textInput;
        strategy = "text"; 
      } 
      
      else if (activeTab === "image") {
        if (!selectedFile) throw new Error("Please upload an image.");
        rawDataString = await convertBase64(selectedFile);
        strategy = imageType === "x-ray" ? "img_rx" : "img_skin";
      } 
      
      else if (activeTab === "numeric") {
        validateCardioData(cardioData);
        const vector = buildHeartFeatureVector(cardioData);
        rawDataString = JSON.stringify(vector);
        strategy = "numeric";
      }
      
      else if (activeTab === "signal") {
        if (!signalInput) throw new Error("Please enter signal data.");
        const arr = signalInput.split(",")
          .map(val => parseFloat(val.trim()))
          .filter(val => !isNaN(val)); 
        if (arr.length === 0) throw new Error("Invalid signal format.");
        rawDataString = JSON.stringify(arr); 
        strategy = "signal";
      }

      const payload = {
        patient_hashed_cf: "TEST_PATIENT_CF_123",
        strategy,
        raw_data: rawDataString
      };

      console.log("Sending to gateway:", payload);

      const response = await aiAPI.analyse(payload);
      setResult(response.data.report);
      resetAllInputs();

    } catch (error) {
      console.error(error);
      alert("Analysis Failed: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const resetAllInputs = () => {
    setTextInput("");
    setSignalInput("");
    setSelectedFile(null);
    setPreviewUrl(null);
    setCardioData(initialCardioState);
  };

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-8 animate-fade-in">
      
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Diagnostic Hub</h1>
        <p className="text-gray-500 mt-2">Execute AI Multimodal Analysis</p>
      </div>

      <div className="flex gap-2 border-b border-gray-200 pb-1 overflow-x-auto">
        {[
          { id: "text", label: "Textual", icon: FileText },
          { id: "image", label: "Imaging (X-Ray/Skin)", icon: Image },
          { id: "numeric", label: "Cardio Risk", icon: Activity },
          { id: "signal", label: "ECG Signal", icon: BarChart2 },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => { setActiveTab(tab.id); setResult(null); }}
            className={`flex items-center gap-2 px-6 py-3 font-semibold transition-all rounded-t-lg border-b-2 ${
              activeTab === tab.id
                ? "border-teal-600 text-teal-700 bg-teal-50"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50"
            }`}
          >
            <tab.icon size={18} /> {tab.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          
          {activeTab === "text" && (
            <div className="space-y-4">
              <label className="font-bold text-gray-700">Symptoms Description</label>
              <textarea 
                className="w-full h-64 p-4 border-2 border-gray-300 rounded-lg focus:border-teal-600 outline-none font-mono text-sm"
                placeholder="Ex: The patient complains of severe tachycardia and sweating..."
                value={textInput}
                onChange={e => setTextInput(e.target.value)}
              />
            </div>
          )}

          {activeTab === "image" && (
            <div className="space-y-6">
            
              <div>
                <label className="block font-bold text-gray-700 mb-3">Select Image Type</label>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setImageType("x-ray")}
                    className={`p-4 rounded-lg border flex flex-col items-center gap-2 transition-all ${
                      imageType === "x-ray" 
                        ? "border-teal-600 bg-teal-50 text-teal-800 ring-1 ring-teal-600"
                        : "border-gray-200 hover:border-gray-300 text-gray-500"
                    }`}
                  >
                    <Scan size={24} />
                    <span className="font-semibold">X-Ray</span>
                  </button>

                  <button
                    onClick={() => setImageType("skin")}
                    className={`p-4 rounded-lg border flex flex-col items-center gap-2 transition-all ${
                      imageType === "skin"
                        ? "border-teal-600 bg-teal-50 text-teal-800 ring-1 ring-teal-600"
                        : "border-gray-200 hover:border-gray-300 text-gray-500"
                    }`}
                  >
                    <User size={24} />
                    <span className="font-semibold">Skin Lesion</span>
                  </button>
                </div>
              </div>

              <div>
                <label className="block font-bold text-gray-700 mb-2">
                  Upload {imageType === "x-ray" ? "X-Ray" : "Skin Lesion"} Image
                </label>
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

          {activeTab === "numeric" && (
            <div className="space-y-2">
              <h3 className="font-bold text-gray-700 border-b pb-2">Clinical Parameters</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                {["age", "trestbps", "chol", "thalch", "oldpeak", "ca"].map(key => (
                  <InputGroup
                    key={key}
                    label={CARDIO_LABELS[key]}
                    type="number"
                    val={cardioData[key]}
                    setter={v => setCardioData({ ...cardioData, [key]: v })}
                  />
                ))}

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

          {activeTab === "signal" && (
            <div className="space-y-2">
              <label className="font-bold text-gray-700">ECG Signal Data</label>
              <p className="text-s text-gray-500">Paste comma-separated voltage values</p>
              <textarea 
                className="w-full h-64 p-4 border-2 border-gray-300 rounded-lg focus:border-teal-600 outline-none font-mono text-sm"
                placeholder="0.05, 0.12, 0.85, -0.20, 0.05..."
                value={signalInput}
                onChange={e => setSignalInput(e.target.value)}
              />
            </div>
          )}

          <div className="mt-6 flex justify-end">
            <button onClick={handleAnalyse} disabled={loading} className={`flex items-center gap-2 px-8 py-3 rounded-lg font-bold text-white shadow-md transition-all ${loading ? "bg-gray-400" : "bg-teal-600 hover:bg-teal-700"}`}>
              {loading ? "Processing..." : <>Run Analysis <ArrowRight size={20}/></>}
            </button>
          </div>
        </div>
        <div className="lg:col-span-1">
        {result ? (
          <div className="bg-white rounded-xl shadow-lg border-t-4 border-teal-500 overflow-hidden animate-slide-up">
            
            <div className="bg-teal-50 p-4 border-b border-teal-100 flex items-center gap-2">
              <CheckCircle className="text-teal-600" size={20}/>
              <h3 className="font-bold text-teal-900">Analysis Result</h3>
            </div>

            <div className="p-6 space-y-6">

              {result.diagnosis && (
                <div className="space-y-4">
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
                        <div className="space-y-2">
                          <span className="text-xs font-bold text-teal-600 uppercase">Heatmap (Grad-CAM)</span>
                          <img
                            src={`data:image/jpeg;base64,${result.explanation}`}
                            alt="Heatmap"
                            className="rounded-lg border border-orange-200 w-full"
                          />
                        </div>
                      ) : (
                        <div className="space-y-2">
                          <span className="text-xs font-bold text-teal-600 uppercase">Explanation</span>
                          <p className="text-sm text-gray-700 italic">{result.explanation}</p>
                        </div>
                      )
                  )}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="h-full bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400 p-6 text-center min-h-[300px]">
            <Brain size={40} className="mb-3 opacity-20" />
            <p>Waiting for Data...</p>
          </div>
        )}
        </div>
    </div>
</div>
)};

const InputGroup = ({ label, type = "text", val, setter, step }) => (
  <div>
    <label className="text-xs font-bold text-gray-500 uppercase">{label}</label>
    <input
      type={type}
      step={step}
      placeholder="Insert numeric value"
      className="w-full p-2 border rounded focus:ring-teal-500"
      value={val}
      onChange={e => setter(e.target.value)}
    />
  </div>
);

const SelectGroup = ({ label, val, setter, options }) => (
  <div className="flex flex-col">
    <label className="text-xs font-bold text-gray-500 uppercase mb-1">{label}</label>
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