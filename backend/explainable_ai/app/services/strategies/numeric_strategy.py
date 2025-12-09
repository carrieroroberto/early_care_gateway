import json
import joblib
import pandas as pd
import os
import base64
import pickle
from ...services.strategies.I_strategy import AnalysisStrategy
from ...utils.ai_models_config import Config

class NumericAnalysisStrategy(AnalysisStrategy):
    def __init__(self):
        self.model = None
        self.explainer = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(Config.XGBOOST_PATH):
            try:
                self.model = joblib.load(Config.XGBOOST_PATH)
                try:
                    import shap
                    self.explainer = shap.TreeExplainer(self.model)
                except Exception:
                    self.explainer = None
            except Exception:
                self.model = None
        else:
            self.model = None

    def _explain_with_rules(self, data: dict):
        factors = []
        if data.get('chol', 0) > 240:
            factors.append({"feature": "Cholesterol", "effect": "High (>240)", "impact_score": "Critical"})
        if data.get('trestbps', 0) > 140:
            factors.append({"feature": "Blood Pressure", "effect": "High (>140)", "impact_score": "High"})
        if data.get('cp', 0) > 0:
            factors.append({"feature": "Chest Pain", "effect": "Present", "impact_score": "High"})
        if data.get('oldpeak', 0) > 2.0:
            factors.append({"feature": "ECG ST", "effect": "Depression", "impact_score": "High"})
        if data.get('thalach', 0) > 180:
            factors.append({"feature": "Heart Rate", "effect": "Tachycardia", "impact_score": "Medium"})
        return factors

    def _decode_features(self, b64string: str):
        raw_bytes = base64.b64decode(b64string)
        features_list = pickle.loads(raw_bytes)

        return features_list

    async def analyse(self, payload: dict) -> dict:
        if not self.model:
            return {"error": "Heart model not available"}

        try:
            b64_features = payload.get("data").get("data")

            if not b64_features:
                return {"error": "No data provided"}

            features = self._decode_features(b64_features)
            input_df = pd.DataFrame([features], columns=Config.HEART_FEATURES)

            probs = self.model.predict_proba(input_df)[0]
            risk_prob = probs[1]

            explanation = []
            if self.explainer:
                try:
                    shap_values = self.explainer.shap_values(input_df)

                    if isinstance(shap_values, list):
                        vals = shap_values[1][0]
                    else:
                        vals = shap_values[0]

                    for feature, impact, value in zip(Config.HEART_FEATURES, vals, input_df.iloc[0]):
                            explanation.append({
                                "Feature": feature,
                                "Value": float(value),
                                "Impact_score": round(float(impact), 4),
                                "Effect": "Increases Risk" if impact > 0 else "Decreases Risk"
                            })
                    explanation.sort(key=lambda x: abs(x['impact_score']), reverse=True)
                except Exception:
                    pass
            else:
                raise Exception("SHAP explanation not available")

            return {
                "diagnosis": "High" if risk_prob > 0.5 else "Low",
                "confidence": risk_prob,
                "explanation": json.dumps(explanation)
            }

        except Exception as e:
            return {"error": str(e)}