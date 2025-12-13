# Import Hugging Face Transformers for NLP tasks
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import os
# Import the strategy interface and configuration
from ..strategies.I_strategy import AnalysisStrategy
from ...utils.ai_models_config import Config
import google.generativeai as genai
import json


class TextAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for Text Analysis (NLP).
    Uses a local BERT model for classification and Google Gemini for explanation.
    """

    def __init__(self):
        self.pipeline = None
        self.gemini = None
        self._load_resources()

    def _load_resources(self):
        """
        Loads the ClinicalBERT model and configures the Gemini API.
        """
        # Load local BERT model if path exists
        if os.path.exists(Config.CLINICALBERT_PATH):
            try:
                tokenizer = AutoTokenizer.from_pretrained(Config.CLINICALBERT_PATH)
                model = AutoModelForSequenceClassification.from_pretrained(Config.CLINICALBERT_PATH)
                # Initialize pipeline on CPU (device=-1)
                self.pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1)
            except Exception as e:
                raise Exception(e)

        # Configure Google Gemini if API key is present
        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.gemini = genai.GenerativeModel('gemini-2.5-flash-lite')

    async def analyse(self, payload: dict) -> dict:
        """
        Analyzes the input text to provide a diagnosis and an explanation.
        """
        if not self.pipeline:
            raise Exception("No pipeline available")

        try:
            # Extract text data from payload
            text = payload.get("data").get("data")
            if not text:
                return {"error": "No processed text provided"}

            # Perform classification using BERT
            output = self.pipeline(text)
            top_result = output[0] if isinstance(output, list) else output

            macro_category = top_result['label']

            # Map generic label IDs (LABEL_0, etc.) to human-readable categories defined in Config
            if macro_category.startswith("LABEL_"):
                idx = int(macro_category.split("_")[1])
                if idx < len(Config.TEXT_LABELS):
                    macro_category = Config.TEXT_LABELS[idx]

            confidence = round(top_result['score'], 4)

            specific_diagnosis = ""
            explanation = ""

            # Use Gemini to generate a specific diagnosis and natural language explanation
            if self.gemini:
                try:
                    prompt = f"""
                    Act as an expert doctor.
                    If the request is not in english, translate it to English first. Also, ensure the final response is in English.
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
                    # Clean the response to ensure valid JSON
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