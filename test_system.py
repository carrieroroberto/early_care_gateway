import sys
import os
import torch
import numpy as np
import json
import base64
from io import BytesIO
from PIL import Image

# --- CONFIGURAZIONE PERCORSI ---
# Aggiunge la cartella ai-service al path per trovare i moduli interni
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "ai_service"))

# Importiamo le strategie dal backend
try:
    from app.strategies.text import text_analyzer
    from app.strategies.image import image_analyzer
    from app.strategies.numeric import numeric_analyzer
    from app.strategies.signal import signal_analyzer
    from app.config import Config
except ImportError as e:
    print(f"❌ ERRORE IMPORT CRITICO: {e}")
    print("   Assicurati di essere nella cartella 'Medical_AI_System' e che la struttura delle cartelle sia corretta.")
    sys.exit(1)


# --- FUNZIONI DI UTILITÀ ---

def save_base64_image(b64_str, filename):
    """Decodifica una stringa Base64 e la salva come file immagine su disco"""
    try:
        if "," in b64_str:
            b64_str = b64_str.split(",")[1]
        img_data = base64.b64decode(b64_str)
        with open(filename, "wb") as f:
            f.write(img_data)
        return True
    except Exception as e:
        print(f"      ❌ Errore salvataggio immagine {filename}: {e}")
        return False


def create_dummy_tensor():
    """Crea un tensore random (3x224x224) per simulare un'immagine processata per i modelli Pytorch"""
    return torch.rand(3, 224, 224).tolist()


def create_dummy_base64_image(color='red'):
    """Crea una stringa base64 di un'immagine colorata per testare Gemini Vision"""
    img = Image.new('RGB', (224, 224), color=color)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


# --- SUITE DI TEST COMPLETA ---

def run_tests():
    print("\n" + "=" * 70)
    print("   🏥 MEDICAL AI HUB - TEST DI VALIDAZIONE SISTEMA COMPLETO 🏥")
    print("   Verifica dei 4 Modelli + Explainable AI (XAI) + Output Visivi")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. TEST TESTO (BERT + Gemini XAI)
    # ---------------------------------------------------------
    print("\n📝 [1] TESTO: Analisi Sintomi (BERT + Gemini)")
    symptom_text = "Patient complains of severe retrosternal chest pain radiating to the left arm, associated with diaphoresis and shortness of breath."
    print(f"   🔹 Input: '{symptom_text[:60]}...'")

    res = text_analyzer.analyze(symptom_text)

    if "error" in res:
        print(f"   ❌ ERRORE: {res['error']}")
    else:
        print(f"   ✅ Status: SUCCESS")
        print(
            f"   🤖 BERT Macro-Categoria: \033[1m{res.get('macro_category')}\033[0m (Confidenza: {res.get('confidence')})")
        print(f"   🧠 Gemini Diagnosi Specifica: {res.get('specific_diagnosis')}")
        print(f"   💡 XAI Spiegazione: \"{res.get('xai_explanation')}\"")

    # ---------------------------------------------------------
    # 2. TEST NUMERICO (XGBoost + Logic XAI)
    # ---------------------------------------------------------
    print("\n📊 [2] NUMERICO: Rischio Cardiaco (XGBoost)")
    # Dati simulati (Paziente ad alto rischio)
    heart_data = {
        'age': 68, 'trestbps': 160, 'chol': 300, 'thalch': 110, 'oldpeak': 3.5, 'ca': 2,
        'sex_Male': 1, 'cp_atypical angina': 0, 'cp_non-anginal': 0, 'cp_typical angina': 1,
        'fbs_True': 1, 'restecg_normal': 0, 'restecg_st-t abnormality': 1, 'exang_True': 1,
        'slope_flat': 1, 'slope_upsloping': 0, 'thal_normal': 0, 'thal_reversable defect': 1
    }

    res = numeric_analyzer.analyze(heart_data)

    if "error" in res:
        print(f"   ❌ ERRORE: {res['error']}")
    else:
        print(f"   ✅ Status: SUCCESS")
        print(f"   🤖 Rischio Stimato: \033[1m{res.get('risk_level')} ({res.get('probability_percent')}%) \033[0m")

        print(f"   🔍 Fattori Critici (XAI):")
        factors = res.get('xai_factors')
        if isinstance(factors, list):
            for f in factors:
                # Gestisce sia il formato SHAP che il formato Regole (che ora sono uniformati)
                feat = f.get('feature', 'N/A')
                eff = f.get('effect', 'N/A')
                imp = f.get('impact_score', 'N/A')
                print(f"      - {feat}: {eff} (Impatto: {imp})")
        else:
            print(f"      {factors}")

    # ---------------------------------------------------------
    # 3. TEST IMMAGINI (Multi-Modale con Grad-CAM)
    # ---------------------------------------------------------
    print("\n🩻 [3] IMMAGINI: Diagnostica Visiva Avanzata")

    # A. DenseNet (X-Ray)
    print("\n   --- A. Chest X-Ray (DenseNet121 + Grad-CAM + Gemini) ---")
    res_xray = image_analyzer.analyze("chest_xray", create_dummy_tensor())

    if "error" in res_xray:
        print(f"   ⚠️  Errore/Warning: {res_xray['error']}")
    else:
        print(f"   ✅ Status: SUCCESS")
        print(f"   🤖 Finding Principale: \033[1m{res_xray.get('primary_finding')}\033[0m")
        print(f"   🧠 Spiegazione Gemini: \"{res_xray.get('xai_explanation_text')}\"")

        # Verifica e Salvataggio Heatmap
        heatmap = res_xray.get('xai_heatmap_base64')
        if heatmap:
            filename = "test_output_xray_heatmap.jpg"
            if save_base64_image(heatmap, filename):
                print(f"   🎨 Heatmap Grad-CAM salvata in: '{filename}'")
        else:
            print("   ⚪ Heatmap: Non generata (Verifica ENABLE_GRADCAM in config)")

    # B. EfficientNet (Skin)
    print("\n   --- B. Skin Lesion (EfficientNet + Grad-CAM + Gemini) ---")
    res_skin = image_analyzer.analyze("skin", create_dummy_tensor())

    if "error" in res_skin:
        print(f"   ⚠️  Errore/Warning: {res_skin['error']}")
    else:
        print(f"   ✅ Status: SUCCESS")
        print(f"   🤖 Diagnosi: \033[1m{res_skin.get('diagnosis')}\033[0m (Conf: {res_skin.get('confidence')})")
        print(f"   🧠 Spiegazione Gemini: \"{res_skin.get('xai_explanation_text')}\"")

        # Verifica e Salvataggio Heatmap
        heatmap = res_skin.get('xai_heatmap_base64')
        if heatmap:
            filename = "test_output_skin_heatmap.jpg"
            if save_base64_image(heatmap, filename):
                print(f"   🎨 Heatmap Grad-CAM salvata in: '{filename}'")
        else:
            print("   ⚪ Heatmap: Non generata")

    # C. Gemini Vision (Generic)
    print("\n   --- C. Generic Image (Gemini Vision) ---")
    res_gemini = image_analyzer.analyze("generic", create_dummy_base64_image(color='green'))

    if "error" in res_gemini:
        print(f"   ⚠️  Errore/Warning: {res_gemini['error']}")
    else:
        print(f"   ✅ Status: SUCCESS")
        print(f"   🤖 Modello: {res_gemini.get('model')}")
        print(f"   📝 Analisi: \"{str(res_gemini.get('analysis'))[:100]}...\"")

    # ---------------------------------------------------------
    # 4. TEST SEGNALI (ECG)
    # ---------------------------------------------------------
    print("\n📈 [4] SEGNALI: ECG (Gemini Analysis)")
    ecg_mock = list(np.random.rand(200))  # 200 punti random
    res_sig = signal_analyzer.analyze(ecg_mock)

    if "error" in res_sig:
        print(f"   ❌ ERRORE: {res_sig['error']}")
    else:
        print(f"   ✅ Status: SUCCESS")
        print(f"   📝 Report ECG: \"{str(res_sig.get('analysis'))[:100]}...\"")

    print("\n" + "=" * 70)
    print("🏁 TEST SUITE COMPLETATA")
    print("=" * 70)


if __name__ == "__main__":
    # Controllo preliminare API Key
    if not Config.GOOGLE_API_KEY:
        print("⚠️  WARNING: GOOGLE_API_KEY non trovata! I test su Gemini falliranno.")
    else:
        print("🔑 API Key rilevata. Avvio test completo...")

    run_tests()