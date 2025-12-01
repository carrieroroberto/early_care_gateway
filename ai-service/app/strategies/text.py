from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import os
from app.config import Config
import logging
import google.generativeai as genai
import json  # Aggiunto import json che mancava

logger = logging.getLogger(__name__)


class TextAnalyzer:
    def __init__(self):
        self.pipeline = None
        self.gemini = None
        self._load_resources()

    def _load_resources(self):
        # 1. Carica BERT
        if os.path.exists(Config.BERT_PATH):
            try:
                tokenizer = AutoTokenizer.from_pretrained(Config.BERT_PATH)
                model = AutoModelForSequenceClassification.from_pretrained(Config.BERT_PATH)
                self.pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1)
                logger.info("✅ BERT Medico caricato.")
            except Exception as e:
                logger.error(f"❌ Errore BERT: {e}")

        # 2. Carica Gemini
        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            # AGGIORNAMENTO: Usiamo il modello 2.0 Flash che hai nella lista
            self.gemini = genai.GenerativeModel('gemini-2.0-flash')

    def analyze(self, text: str):
        if not self.pipeline: return {"error": "BERT non disponibile"}

        try:
            # --- FASE 1: BERT ---
            output = self.pipeline(text)
            top_result = output[0] if isinstance(output, list) else output

            macro_category = top_result['label']
            if macro_category.startswith("LABEL_"):
                idx = int(macro_category.split("_")[1])
                if idx < len(Config.TEXT_LABELS):
                    macro_category = Config.TEXT_LABELS[idx]

            confidence = round(top_result['score'], 4)

            # --- FASE 2: GEMINI ---
            specific_diagnosis = "N/A"
            explanation = "N/A"

            if self.gemini:
                try:
                    prompt = f"""
                    Agisci come un dottore esperto.
                    Sintomi Paziente: "{text}"
                    Classificazione AI (BERT): {macro_category} (Confidenza {confidence:.2%})

                    Compito:
                    1. Fornisci una DIAGNOSI SPECIFICA basata sui sintomi.
                    2. Spiega PERCHÉ (XAI) in 2 frasi.

                    Rispondi SOLO in formato JSON valido:
                    {{
                        "specific_diagnosis": "...",
                        "explanation": "..."
                    }}
                    """
                    response = self.gemini.generate_content(prompt)
                    cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
                    ai_data = json.loads(cleaned_text)

                    specific_diagnosis = ai_data.get("specific_diagnosis", "N/A")
                    explanation = ai_data.get("explanation", "N/A")

                except Exception as e:
                    explanation = f"Analisi base (Gemini offline o errore): {str(e)}"

            return {
                "status": "success",
                "macro_category": macro_category,
                "confidence": confidence,
                "specific_diagnosis": specific_diagnosis,
                "xai_explanation": explanation
            }

        except Exception as e:
            return {"error": str(e)}


text_analyzer = TextAnalyzer()