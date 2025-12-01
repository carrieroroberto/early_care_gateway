import google.generativeai as genai
from app.config import Config
import json
import numpy as np


class SignalAnalyzer:
    def __init__(self):
        self.model = None
        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            # AGGIORNAMENTO: Usiamo 2.0 Flash
            self.model = genai.GenerativeModel('gemini-2.0-flash')

    def analyze(self, signal_data: list):
        if not self.model: return {"error": "Gemini non disponibile"}
        try:
            stats = {"min": float(np.min(signal_data)), "max": float(np.max(signal_data)),
                     "mean": float(np.mean(signal_data))}
            sample = signal_data[:300]  # Riduciamo i punti per velocità

            prompt = f"""
            Analizza questi dati di segnale ECG (campionati).
            Statistiche: {json.dumps(stats)}
            Dati: {json.dumps(sample)}
            Identifica potenziali anomalie o ritmo.
            """

            response = self.model.generate_content(prompt)
            return {"status": "success", "analysis": response.text}

        except Exception as e:
            return {"error": str(e)}


signal_analyzer = SignalAnalyzer()