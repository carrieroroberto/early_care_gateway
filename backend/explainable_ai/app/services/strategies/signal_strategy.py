import google.generativeai as genai
from ...services.strategies.I_strategy import AnalysisStrategy
from ...utils.ai_models_config import Config
import json
import numpy as np

class SignalAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for Signal Analysis (e.g., ECG).
    Currently relies on Generative AI (Gemini) to analyze signal statistics and samples.
    """
    def __init__(self):
        self.model = None

        # Configure Gemini model if API key is available
        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    async def analyse(self, payload: dict) -> dict:
        """
        Analyzes ECG signal data using GenAI.
        Computes basic stats (min, max, mean) and sends a prompt to the LLM.
        """
        if not self.model:
            return {"error": "Gemini model not available"}

        try:
            signal_list_str = payload.get("data").get("data")
            if not signal_list_str:
                return {"error": "Signal data not provided"}

            # Parse signal data into a NumPy array
            signal_data = json.loads(signal_list_str)
            signal_array = np.array(signal_data, dtype=np.float32)

            # Compute statistical features to help the LLM
            stats = {
                "min": float(np.min(signal_array)),
                "max": float(np.max(signal_array)),
                "mean": float(np.mean(signal_array))
            }

            sample = signal_array.tolist()

            # Construct the prompt for the AI model
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

            # Generate content and parse JSON response
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