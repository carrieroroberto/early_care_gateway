import json
import joblib
import pandas as pd
import os
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

    async def analyse(self, payload: dict) -> dict:
        if not self.model:
            return {"error": "Heart model not available"}

        try:
            features = payload.get("data").get("data")

            if not features:
                return {"error": "No data provided"}

            features = json.loads(features)
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