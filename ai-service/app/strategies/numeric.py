import joblib
import pandas as pd
import os
import shap
import numpy as np
from app.config import Config
import logging

logger = logging.getLogger(__name__)


class NumericAnalyzer:
    def __init__(self):
        self.model = None
        self.explainer = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(Config.HEART_MODEL_PATH):
            try:
                self.model = joblib.load(Config.HEART_MODEL_PATH)
                # Tentativo caricamento SHAP
                try:
                    self.explainer = shap.TreeExplainer(self.model)
                    logger.info("✅ XGBoost + SHAP caricati.")
                except Exception as e:
                    # Questo warning è normale con i file .joblib
                    logger.warning(f"⚠️ SHAP init fallito ({e}). Userò fallback logico.")
                    self.explainer = None
            except Exception as e:
                logger.error(f"❌ Errore caricamento XGBoost: {e}")
        else:
            logger.warning(f"⚠️ File {Config.HEART_MODEL_PATH} non trovato.")

    def _explain_with_rules(self, data):
        """Fallback: Spiegazione basata su regole cliniche se SHAP fallisce"""
        factors = []
        # --- CORREZIONE QUI: Uso 'impact_score' invece di 'impact' per coerenza ---
        if data.get('chol', 0) > 240:
            factors.append({"feature": "Colesterolo", "effect": "Alto (>240)", "impact_score": "Critico"})
        if data.get('trestbps', 0) > 140:
            factors.append({"feature": "Pressione", "effect": "Alta (>140)", "impact_score": "Alto"})
        if data.get('cp', 0) > 0:
            factors.append({"feature": "Dolore Toracico", "effect": "Presente", "impact_score": "Alto"})
        if data.get('oldpeak', 0) > 2.0:
            factors.append({"feature": "ECG ST", "effect": "Depressione", "impact_score": "Alto"})
        if data.get('thalach', 0) > 180:
            factors.append({"feature": "Battito", "effect": "Tachicardia", "impact_score": "Medio"})

        if not factors:
            # Restituiamo un oggetto vuoto coerente per evitare crash
            return []

        return factors

    def analyze(self, data: dict):
        if not self.model: return {"error": "Modello cuore non disponibile"}

        try:
            input_df = pd.DataFrame([data], columns=Config.HEART_FEATURES)
            probs = self.model.predict_proba(input_df)[0]
            risk_prob = probs[1]

            explanation = []

            # Logica XAI: Prova SHAP, altrimenti Regole
            if self.explainer:
                try:
                    shap_values = self.explainer.shap_values(input_df)
                    if isinstance(shap_values, list):
                        vals = shap_values[1][0]
                    else:
                        vals = shap_values[0]

                    for feat, impact, val in zip(Config.HEART_FEATURES, vals, input_df.iloc[0]):
                        if abs(impact) > 0.1:
                            explanation.append({
                                "feature": feat,
                                "value": float(val),
                                # Coerenza chiave
                                "impact_score": round(float(impact), 4),
                                "effect": "Aumenta Rischio" if impact > 0 else "Riduce Rischio"
                            })
                    explanation.sort(key=lambda x: abs(x['impact_score']), reverse=True)
                    explanation = explanation[:5]
                except Exception as e:
                    logger.warning(f"Errore calcolo SHAP: {e}. Passo al fallback.")
                    explanation = self._explain_with_rules(data)
            else:
                explanation = self._explain_with_rules(data)

            return {
                "status": "success",
                "risk_level": "ALTO" if risk_prob > 0.5 else "BASSO",
                "probability_percent": round(risk_prob * 100, 2),
                "xai_factors": explanation
            }

        except Exception as e:
            return {"error": str(e)}


numeric_analyzer = NumericAnalyzer()