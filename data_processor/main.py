import uvicorn
import hashlib
import base64
import io
import re
import numpy as np
import pandas as pd  # <--- NUOVO IMPORT
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from PIL import Image
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataProcessor")

app = FastAPI(title="Data Processing Service", version="1.0.0")

# --- DEFINIZIONE FEATURE MODELLO CUORE ---
# Queste sono le colonne ESATTE che il modello XGBoost si aspetta
HEART_MODEL_COLUMNS = [
    'age', 'trestbps', 'chol', 'thalch', 'oldpeak', 'ca',
    'sex_Male', 'cp_atypical angina', 'cp_non-anginal', 'cp_typical angina',
    'fbs_True', 'restecg_normal', 'restecg_st-t abnormality', 'exang_True',
    'slope_flat', 'slope_upsloping', 'thal_normal', 'thal_reversable defect'
]


class ProcessingRequest(BaseModel):
    data_type: str
    raw_data: Any
    patient_id: Optional[str] = None
    target_model: Optional[str] = "local"


class Anonymizer:
    @staticmethod
    def hash_patient_id(pid: str) -> str:
        if not pid: return "anonymous"
        return hashlib.sha256(pid.encode()).hexdigest()[:12]


class DataCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text: return ""
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def process_image(b64_string: str, for_gemini: bool = False) -> Any:
        try:
            if "," in b64_string: b64_string = b64_string.split(",")[1]
            image_bytes = base64.b64decode(b64_string)

            if for_gemini: return base64.b64encode(image_bytes).decode('utf-8')

            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            image = image.resize((224, 224))
            img_array = np.array(image) / 255.0
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            img_array = (img_array - mean) / std
            return img_array.transpose((2, 0, 1)).tolist()
        except Exception as e:
            logger.error(f"Image Error: {e}")
            raise ValueError("Immagine non valida")

    @staticmethod
    def process_heart_data(data: dict) -> dict:
        """
        Trasforma i dati grezzi (es. sex=1) nel formato One-Hot (sex_Male=1)
        """
        try:
            # 1. Crea un DataFrame vuoto con le colonne finali a 0
            df = pd.DataFrame(0, index=[0], columns=HEART_MODEL_COLUMNS)

            # 2. Mappatura Valori Numerici
            # Nota: mappiamo 'thalach' (input) su 'thalch' (modello)
            df['age'] = data.get('age', 0)
            df['trestbps'] = data.get('trestbps', 0)
            df['chol'] = data.get('chol', 0)
            df['thalch'] = data.get('thalach', 0)
            df['oldpeak'] = data.get('oldpeak', 0.0)
            df['ca'] = data.get('ca', 0)

            # 3. Mappatura Categoriale (One-Hot Manuale)
            if data.get('sex') == 1: df['sex_Male'] = 1

            cp = data.get('cp')
            if cp == 1:
                df['cp_atypical angina'] = 1
            elif cp == 2:
                df['cp_non-anginal'] = 1
            elif cp == 3:
                df['cp_typical angina'] = 1

            if data.get('fbs') == 1: df['fbs_True'] = 1

            recg = data.get('restecg')
            if recg == 0:
                df['restecg_normal'] = 1
            elif recg == 1:
                df['restecg_st-t abnormality'] = 1

            if data.get('exang') == 1: df['exang_True'] = 1

            slope = data.get('slope')
            if slope == 1:
                df['slope_upsloping'] = 1
            elif slope == 2:
                df['slope_flat'] = 1

            thal = data.get('thal')
            if thal == 1:
                df['thal_normal'] = 1
            elif thal == 2:
                df['thal_reversable defect'] = 1

            # Restituisce il dizionario pulito pronto per il modello
            return df.iloc[0].to_dict()

        except Exception as e:
            raise ValueError(f"Errore preprocessing dati numerici: {e}")


@app.post("/process")
async def process_data(request: ProcessingRequest):
    try:
        hashed_id = Anonymizer.hash_patient_id(request.patient_id)
        processed_payload = None

        if request.data_type == "text":
            processed_payload = DataCleaner.clean_text(str(request.raw_data))

        elif request.data_type == "image":
            is_gemini = request.target_model == "gemini"
            processed_payload = DataCleaner.process_image(str(request.raw_data), for_gemini=is_gemini)

        elif request.data_type == "numeric":
            if not isinstance(request.raw_data, dict):
                raise ValueError("Dati numerici devono essere un JSON")
            # QUI CHIAMIAMO LA NUOVA LOGICA
            processed_payload = DataCleaner.process_heart_data(request.raw_data)

        elif request.data_type == "signal":
            if not isinstance(request.raw_data, list):
                raise ValueError("Segnale deve essere una lista")
            processed_payload = request.raw_data

        return {
            "status": "success",
            "processed_id": hashed_id,
            "data_type": request.data_type,
            "payload": processed_payload
        }

    except Exception as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
