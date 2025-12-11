import React, { useState } from 'react';
import {aiAPI} from '../services/api';
import { runDiagnosticWorkflow } from '../services/api';
import { 
  Activity, FileText, Image, Upload, Brain,
  ArrowRight, AlertTriangle, CheckCircle, BarChart2, Scan, User 
} from 'lucide-react';

const Analysis = () => {
  // --- States ---
  const [activeTab, setActiveTab] = useState('text'); 
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  //Input States
  const [textInput, setTextInput] = useState('');
  const [signalInput, setSignalInput] = useState(''); 
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [imageType, setImageType] = useState('chest_xray');


  //Numeric Data State including all the features used for evaluation
  const [cardioData, setCardioData] = useState({
    age: '', sex: '1', cp: '0', trestbps: '', chol: '',
    fbs: '0', restecg: '0', thalach: '', exang: '0',
    oldpeak: '', slope: '1', ca: '0', thal: '1'
  });


  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const convertBase64 = (file) => {   //Used to convert images according to Base64
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => resolve(fileReader.result.split(',')[1]);
      fileReader.onerror = (error) => reject(error);
    });
  };

  // --- Analysis handling ---
  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);

    try {
      let rawDataString = ""; 
      let strategy = "";

      // Text -> Backend key: "text"
      if (activeTab === 'text') {
        if (!textInput) throw new Error("Please enter clinical notes.");
        rawDataString = textInput;
        strategy = "text"; 
      } 
      
      // Image -> Backend keys: "img_rx" o "img_skin"
      else if (activeTab === 'image') {
        if (!selectedFile) throw new Error("Please upload an image.");
        rawDataString = await convertBase64(selectedFile);
        
        if (imageType === 'chest_xray') {
            strategy = "img_rx";
        } else {
            strategy = "img_skin";
        }
      } 
      
      // Numeric -> Backend key: "numeric"
      else if (activeTab === 'numeric') {
         const numericArray = [
          parseInt(cardioData.age) || 0,        // 1. age
          parseInt(cardioData.sex),             // 2. sex
          parseInt(cardioData.cp),              // 3. cp
          parseInt(cardioData.trestbps) || 0,   // 4. trestbps
          parseInt(cardioData.chol) || 0,       // 5. chol
          parseInt(cardioData.fbs),             // 6. fbs
          parseInt(cardioData.restecg),         // 7. restecg
          parseInt(cardioData.thalach) || 0,    // 8. thalach
          parseInt(cardioData.exang),           // 9. exang
          parseFloat(cardioData.oldpeak) || 0.0,// 10. oldpeak (Float!)
          parseInt(cardioData.slope),           // 11. slope
          parseInt(cardioData.ca),              // 12. ca
          parseInt(cardioData.thal)             // 13. thal
        ];
        rawDataString = JSON.stringify(numericArray); 
        strategy = "numeric";
      }
      
      // Signal -> Backend key: "signal"
      else if (activeTab === 'signal') {
        if (!signalInput) throw new Error("Please enter signal data.");
        
        const arr = signalInput.split(',')
          .map(val => parseFloat(val.trim()))
          .filter(val => !isNaN(val)); 
        
        if (arr.length === 0) throw new Error("Invalid signal format.");
        
        rawDataString = JSON.stringify(arr); 
        strategy = "signal";
      }


      const payload = {
        patient_hashed_cf: "TEST_PATIENT_CF_123", 
        strategy: strategy, 
        raw_data: rawDataString 
      };

      console.log("Sending to gateway:", payload);
      
      const response = await aiAPI.analyse(payload);
      
      setResult(response.data.report);

    } catch (error) {
      console.error(error);
      alert("Analysis Failed: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-8 animate-fade-in">
      
      <div>
        <h1 className="text-3xl font-bold text-gray-800">Diagnostic Hub</h1>
        <p className="text-gray-500">Multimodal Clinical Decision Support System</p>
      </div>

      {/* --- TAB MENU --- */}
      <div className="flex gap-2 border-b border-gray-200 pb-1 overflow-x-auto">
        {[
          { id: 'text', label: 'Symptoms (NLP)', icon: FileText },
          { id: 'image', label: 'Imaging (X-Ray/Skin)', icon: Image },
          { id: 'numeric', label: 'Cardio Risk (Tabular)', icon: Activity },
          { id: 'signal', label: 'ECG Signal', icon: BarChart2 },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => { setActiveTab(tab.id); setResult(null); }}
            className={`flex items-center gap-2 px-6 py-3 font-semibold transition-all rounded-t-lg border-b-2 ${
              activeTab === tab.id
                ? 'border-teal-600 text-teal-700 bg-teal-50'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <tab.icon size={18} /> {tab.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* --- INPUT AREA --- */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          
          {/* TEXT INPUT */}
          {activeTab === 'text' && (
            <div className="space-y-4">
              <label className="font-bold text-gray-700">Patient Symptoms</label>
              <textarea 
                className="w-full h-64 p-4 border rounded-lg focus:ring-2 focus:ring-teal-500 font-mono text-sm"
                placeholder="Ex: The patient complains of severe tachycardia and sweating..."
                value={textInput}
                onChange={e => setTextInput(e.target.value)}
              />
            </div>
          )}

          {/* IMAGE INPUT */}
          {activeTab === 'image' && (
            <div className="space-y-6">
              
              {/* Image type selector */}
              <div>
                <label className="block font-bold text-gray-700 mb-3">Select Image Type</label>
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setImageType('chest_xray')}
                    className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 transition-all ${
                      imageType === 'chest_xray' 
                        ? 'border-teal-600 bg-teal-50 text-teal-800 ring-1 ring-teal-600' 
                        : 'border-gray-200 hover:border-gray-300 text-gray-500'
                    }`}
                  >
                    <Scan size={24} />
                    <span className="font-semibold">Chest X-Ray</span>
                  </button>

                  <button
                    onClick={() => setImageType('skin')}
                    className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 transition-all ${
                      imageType === 'skin' 
                        ? 'border-teal-600 bg-teal-50 text-teal-800 ring-1 ring-teal-600' 
                        : 'border-gray-200 hover:border-gray-300 text-gray-500'
                    }`}
                  >
                    <User size={24} />
                    <span className="font-semibold">Skin Lesion</span>
                  </button>
                </div>
              </div>

              {/* Upload area */}
              <div>
                <label className="block font-bold text-gray-700 mb-2">
                  Upload {imageType === 'chest_xray' ? 'X-Ray' : 'Dermatoscopy'} Image
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center bg-gray-50 hover:bg-gray-100 transition">
                  <input type="file" onChange={handleFileChange} className="hidden" id="file-upload" accept="image/*" />
                  <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                    {previewUrl ? (
                      <img src={previewUrl} alt="Preview" className="h-64 object-contain rounded shadow-sm" />
                    ) : (
                      <>
                        <Upload size={48} className="text-gray-400 mb-3" />
                        <span className="text-teal-600 font-bold">Click to upload</span>
                        <span className="text-xs text-gray-400 mt-1">Supports JPG, PNG</span>
                      </>
                    )}
                  </label>
                </div>
              </div>
            </div>
          )}

          {/* NUMERIC INPUT */}
          {activeTab === 'numeric' && (
            <div className="space-y-4">
              <h3 className="font-bold text-gray-700 border-b pb-2">Clinical Parameters</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InputGroup label="Age" type="number" val={cardioData.age} setter={v => setCardioData({...cardioData, age: v})} />
                <SelectGroup label="Sex" val={cardioData.sex} setter={v => setCardioData({...cardioData, sex: v})}>
                  <option value="1">Male (1)</option>
                  <option value="0">Female (0)</option>
                </SelectGroup>
                <SelectGroup label="Chest Pain (cp)" val={cardioData.cp} setter={v => setCardioData({...cardioData, cp: v})}>
                  <option value="0">Asymptomatic (0)</option>
                  <option value="1">Typical Angina (1)</option>
                  <option value="2">Atypical Angina (2)</option>
                  <option value="3">Non-anginal (3)</option>
                </SelectGroup>
                <InputGroup label="Resting BP (mm Hg)" type="number" val={cardioData.trestbps} setter={v => setCardioData({...cardioData, trestbps: v})} />
                <InputGroup label="Cholesterol (mg/dl)" type="number" val={cardioData.chol} setter={v => setCardioData({...cardioData, chol: v})} />
                <SelectGroup label="Fasting Blood Sugar > 120" val={cardioData.fbs} setter={v => setCardioData({...cardioData, fbs: v})}>
                  <option value="0">False (0)</option>
                  <option value="1">True (1)</option>
                </SelectGroup>
                <SelectGroup label="Resting ECG Results" val={cardioData.restecg} setter={v => setCardioData({...cardioData, restecg: v})}>
                  <option value="0">Normal</option>
                  <option value="1">ST-T Abnormality</option>
                  <option value="2">Hypertrophy</option>
                </SelectGroup>
                <InputGroup label="Max Heart Rate (thalach)" type="number" val={cardioData.thalach} setter={v => setCardioData({...cardioData, thalach: v})} />
                <SelectGroup label="Exercise Induced Angina" val={cardioData.exang} setter={v => setCardioData({...cardioData, exang: v})}>
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </SelectGroup>
                <InputGroup label="ST Depression (oldpeak)" type="number" step="0.1" val={cardioData.oldpeak} setter={v => setCardioData({...cardioData, oldpeak: v})} />
                <SelectGroup label="Slope of Peak ST" val={cardioData.slope} setter={v => setCardioData({...cardioData, slope: v})}>
                  <option value="2">Flat (2)</option>
                  <option value="1">Upsloping (1)</option>
                  <option value="0">Downsloping (0)</option>
                </SelectGroup>
                <InputGroup label="Major Vessels (ca) 0-3" type="number" val={cardioData.ca} setter={v => setCardioData({...cardioData, ca: v})} />
                <SelectGroup label="Thalassemia" val={cardioData.thal} setter={v => setCardioData({...cardioData, thal: v})}>
                  <option value="1">Normal</option>
                  <option value="2">Fixed Defect</option>
                  <option value="3">Reversable Defect</option>
                </SelectGroup>
              </div>
            </div>
          )}

          {/* Input signal */}
          {activeTab === 'signal' && (
            <div className="space-y-4">
              <label className="font-bold text-gray-700">ECG Signal Data (CSV Format)</label>
              <p className="text-xs text-gray-500">Paste comma-separated voltage values</p>
              <textarea 
                className="w-full h-64 p-4 border rounded-lg focus:ring-2 focus:ring-teal-500 font-mono text-xs"
                placeholder="0.05, 0.12, 0.85, -0.20, 0.05..."
                value={signalInput}
                onChange={e => setSignalInput(e.target.value)}
              />
            </div>
          )}

          <div className="mt-6 flex justify-end">
            <button onClick={handleAnalyze} disabled={loading} className={`flex items-center gap-2 px-8 py-3 rounded-lg font-bold text-white shadow-md transition-all ${loading ? 'bg-gray-400' : 'bg-teal-600 hover:bg-teal-700'}`}>
              {loading ? 'Processing...' : <>Run Analysis <ArrowRight size={20}/></>}
            </button>
          </div>
        </div>

        {/* --- OUTPUT AREA --- */}
        <div className="lg:col-span-1">
          {result ? (
            <div className="bg-white rounded-xl shadow-lg border-t-4 border-teal-500 overflow-hidden animate-slide-up">
              
              <div className="bg-teal-50 p-4 border-b border-teal-100 flex items-center gap-2">
                <CheckCircle className="text-teal-600" size={20}/>
                <h3 className="font-bold text-teal-900">Analysis Result</h3>
              </div>

              <div className="p-6 space-y-6">
                
                {/* 1. TESTO */}
                {result.macro_category && (
                  <div>
                    <span className="text-xs font-bold text-gray-400 uppercase">Classification</span>
                    <p className="text-lg font-bold text-teal-800">{result.macro_category}</p>
                    {result.specific_diagnosis && <p className="text-xl font-bold text-gray-900 mt-2">{result.specific_diagnosis}</p>}
                  </div>
                )}

                {/* 2. IMMAGINE (RX o Pelle) */}
                {(result.primary_finding || result.diagnosis) && (
                  <div>
                    <span className="text-xs font-bold text-gray-400 uppercase">Finding</span>
                    <p className="text-2xl font-bold text-gray-900">{result.primary_finding || result.diagnosis}</p>
                    
                    {result.findings_detail && (
                      <ul className="mt-2 space-y-1 bg-gray-50 p-2 rounded">
                        {result.findings_detail.map((f, i) => (
                          <li key={i} className="text-sm flex justify-between">
                            <span>{f.pathology}</span>
                            <span className="font-bold">{(f.probability * 100).toFixed(1)}%</span>
                          </li>
                        ))}
                      </ul>
                    )}

                    {result.xai_heatmap_base64 && (
                      <div className="mt-4">
                        <span className="text-xs font-bold text-orange-500 uppercase mb-1 block">Grad-CAM Heatmap</span>
                        <img src={`data:image/jpeg;base64,${result.xai_heatmap_base64}`} alt="Heatmap" className="rounded-lg border border-orange-200 w-full" />
                      </div>
                    )}
                  </div>
                )}

                {/* Cardiology */}
                {result.risk_level && (
                  <div>
                    <span className="text-xs font-bold text-gray-400 uppercase">Risk Level</span>
                    <p className={`text-3xl font-bold ${result.risk_level === 'ALTO' ? 'text-red-600' : 'text-green-600'}`}>
                      {result.risk_level}
                    </p>
                    <p className="text-sm font-bold text-gray-600 mt-1">Probability: {result.probability_percent}%</p>
                  </div>
                )}

                {/* Signal */}
                {result.analysis && !result.risk_level && !result.macro_category && (
                  <div>
                    <span className="text-xs font-bold text-gray-400 uppercase">Analysis</span>
                    <p className="text-gray-800 text-sm leading-relaxed mt-1">{result.analysis}</p>
                  </div>
                )}

                {/* XAI */}
                {(result.xai_explanation || result.xai_explanation_text) && (
                  <div className="bg-amber-50 p-4 rounded-lg border border-amber-100 mt-4">
                    <div className="flex items-center gap-2 mb-2 text-amber-700">
                      <AlertTriangle size={16} />
                      <span className="font-bold text-xs uppercase">AI Explanation</span>
                    </div>
                    <p className="text-sm text-gray-700 italic">
                      "{result.xai_explanation || result.xai_explanation_text}"
                    </p>
                  </div>
                )}

              </div>
            </div>
          ) : (
            <div className="h-full bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 flex flex-col items-center justify-center text-gray-400 p-6 text-center min-h-[300px]">
              <Brain size={40} className="mb-3 opacity-20" />
              <p>Waiting for data...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};


const InputGroup = ({ label, type = "text", val, setter, step }) => (
  <div>
    <label className="text-xs font-bold text-gray-500 uppercase">{label}</label>
    <input type={type} step={step} className="w-full p-2 border rounded focus:ring-teal-500" value={val} onChange={e => setter(e.target.value)} />
  </div>
);

const SelectGroup = ({ label, val, setter, children }) => (
  <div>
    <label className="text-xs font-bold text-gray-500 uppercase">{label}</label>
    <select className="w-full p-2 border rounded focus:ring-teal-500" value={val} onChange={e => setter(e.target.value)}>
      {children}
    </select>
  </div>
);

export default Analysis;