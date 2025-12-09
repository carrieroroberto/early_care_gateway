import os

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ENABLE_GRADCAM = True

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
    MODELS_DIR = os.path.join(PROJECT_ROOT, "ai_models")

    if not os.path.exists(MODELS_DIR):
        print(f"Models directory not found at {MODELS_DIR}")

    CHEXNET_PATH = os.path.join(MODELS_DIR, "chexnet_rx.pth")
    EFFICIENTNET_PATH = os.path.join(MODELS_DIR, "efficientnet_skin.pth")
    XGBOOST_PATH = os.path.join(MODELS_DIR, "xgboost_heart.joblib")
    CLINICALBERT_PATH = os.path.join(MODELS_DIR, "clinicalbert_text")

    XRAY_LABELS = [
        'Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass', 'Nodule',
        'Pneumonia', 'Pneumothorax', 'Consolidation', 'Edema', 'Emphysema',
        'Fibrosis', 'Pleural_Thickening', 'Hernia'
    ]

    SKIN_LABELS = [
        'Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis',
        'Dermatofibroma', 'Melanocytic nevi', 'Melanoma', 'Vascular lesions'
    ]

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