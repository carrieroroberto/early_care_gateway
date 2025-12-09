from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import os
from ..strategies.I_strategy import AnalysisStrategy
from ...utils.ai_models_config import Config
import google.generativeai as genai
import json

class TextAnalysisStrategy(AnalysisStrategy):
    def __init__(self):
        self.pipeline = None
        self.gemini = None
        self._load_resources()

    def _load_resources(self):
        if os.path.exists(Config.CLINICALBERT_PATH):
            try:
                tokenizer = AutoTokenizer.from_pretrained(Config.CLINICALBERT_PATH)
                model = AutoModelForSequenceClassification.from_pretrained(Config.CLINICALBERT_PATH)
                self.pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1)
            except Exception as e:
                raise Exception(e)

        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.gemini = genai.GenerativeModel('gemini-2.5-flash-lite')

    async def analyse(self, payload: dict) -> dict:
        if not self.pipeline:
            raise Exception("No pipeline available")

        try:
            text = payload.get("data").get("data")
            if not text:
                return {"error": "No processed text provided"}

            output = self.pipeline(text)
            top_result = output[0] if isinstance(output, list) else output

            macro_category = top_result['label']

            if macro_category.startswith("LABEL_"):
                idx = int(macro_category.split("_")[1])
                if idx < len(Config.TEXT_LABELS):
                    macro_category = Config.TEXT_LABELS[idx]

            confidence = round(top_result['score'], 4)

            specific_diagnosis = ""
            explanation = ""
            if self.gemini:
                try:
                    prompt = f"""
                    Act as an expert doctor.
                    Patient Symptoms: "{text}"
                    AI Classification (BERT): {macro_category} (Confidence {confidence:.2%})

                    Task:
                    1. Provide a SPECIFIC DIAGNOSIS based on the symptoms.
                    2. Explain WHY (XAI) in 2 sentences.

                    Respond ONLY in valid JSON format:
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
                    raise Exception(e)

            result = {
                "diagnosis": f"{macro_category}: {specific_diagnosis}",
                "confidence": confidence,
                "explanation": explanation
            }

            return result

        except Exception as e:
            return {"error": str(e)}