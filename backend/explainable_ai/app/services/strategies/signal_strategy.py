import google.generativeai as genai
from ...services.strategies.I_strategy import AnalysisStrategy
from ...utils.ai_models_config import Config
import json
import numpy as np

class SignalAnalysisStrategy(AnalysisStrategy):
    def __init__(self):
        self.model = None

        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    async def analyse(self, payload: dict) -> dict:
        if not self.model:
            return {"error": "Gemini model not available"}

        try:
            signal_list_str = payload.get("data").get("data")
            if not signal_list_str:
                return {"error": "Signal data not provided"}

            signal_data = json.loads(signal_list_str)
            signal_array = np.array(signal_data, dtype=np.float32)

            stats = {
                "min": float(np.min(signal_array)),
                "max": float(np.max(signal_array)),
                "mean": float(np.mean(signal_array))
            }

            sample = signal_array.tolist()

            prompt = f"""
            Analyze this ECG signal.
            Statistics: {json.dumps(stats)}
            Data: {json.dumps(sample)}

            Identify anomalies, arrhythmias, or irregularities.

            Respond ONLY in JSON:
            {{
              "diagnosis": "...",
              "confidence": 0.0,
              "explanation": "..."
            }}
            """

            response = self.model.generate_content(prompt)
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_text)

            return {
                "diagnosis": result.get("diagnosis", "N/A"),
                "confidence": result.get("confidence", 0.0),
                "explanation": result.get("explanation", "N/A")
            }

        except Exception as e:
            return {"error": str(e)}