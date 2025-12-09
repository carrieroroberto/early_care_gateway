import google.generativeai as genai
from ...services.strategies.I_strategy import AnalysisStrategy
from ...utils.ai_models_config import Config
import json
import numpy as np
import base64
import pickle

class SignalAnalysisStrategy(AnalysisStrategy):
    def __init__(self):
        self.model = None

        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')

    def _decode_signal(self, b64string: str):
        raw_bytes = base64.b64decode(b64string)
        signal_list = pickle.loads(raw_bytes)

        return signal_list

    async def analyse(self, payload: dict) -> dict:
        if not self.model:
            return {"error": "Gemini model not available"}

        try:
            b64_signal = payload.get("data").get("data")

            if not b64_signal:
                return {"error": "Signal data not provided"}

            signal_data = self._decode_signal(b64_signal)

            stats = {
                "min": float(np.min(signal_data)),
                "max": float(np.max(signal_data)),
                "mean": float(np.mean(signal_data))
            }

            sample = signal_data.tolist()

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
                "diagnosis": result.get("diagnosis", "unknown"),
                "confidence": result.get("confidence", 0.0),
                "explanation": result.get("explanation", "")
            }

        except Exception as e:
            return {"error": str(e)}