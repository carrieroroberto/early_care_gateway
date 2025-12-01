import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ENABLE_GRADCAM = True

    # --- PERCORSI ---
    CURRENT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = CURRENT_DIR.parent.parent
    MODELS_DIR = PROJECT_ROOT / "models"

    # Controlliamo se i file esistono
    if not MODELS_DIR.exists():
        print(f"⚠️ ATTENZIONE: Cartella {MODELS_DIR} non trovata!")

    CHEXNET_PATH = str(MODELS_DIR / "densenet_epoch_3.pth")
    SKIN_PATH = str(MODELS_DIR / "efficientnet_skin_best.pth")
    HEART_MODEL_PATH = str(MODELS_DIR / "xgboost_heart_model.joblib")
    BERT_PATH = str(MODELS_DIR / "modello_medico_finale")

    # --- LABELS ---
    XRAY_LABELS = [
        'Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass', 'Nodule',
        'Pneumonia', 'Pneumothorax', 'Consolidation', 'Edema', 'Emphysema',
        'Fibrosis', 'Pleural_Thickening', 'Hernia'
    ]

    SKIN_LABELS = [
        'Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis',
        'Dermatofibroma', 'Melanocytic nevi', 'Melanoma', 'Vascular lesions'
    ]

    # Feature per XGBoost (Ordine corretto dopo One-Hot Encoding)
    HEART_FEATURES = [
        'age', 'trestbps', 'chol', 'thalch', 'oldpeak', 'ca',
        'sex_Male', 'cp_atypical angina', 'cp_non-anginal', 'cp_typical angina',
        'fbs_True', 'restecg_normal', 'restecg_st-t abnormality', 'exang_True',
        'slope_flat', 'slope_upsloping', 'thal_normal', 'thal_reversable defect'
    ]

    TEXT_LABELS = [
        'Cardiovascular / Pulmonary', 'Orthopedic', 'Gastroenterology', 'Neurology',
        'Obstetrics / Gynecology', 'Urology', 'ENT - Otolaryngology', 'Hematology - Oncology'
    ]
