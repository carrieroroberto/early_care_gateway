import torch
import logging
import os
import io
import base64
import numpy as np
import cv2
from torchvision import models
from PIL import Image
import torch.nn.functional as F
import google.generativeai as genai
from app.config import Config

# Librerie XAI
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.chexnet = None
        self.skinnet = None
        self.gemini = None
        self.target_layers_chexnet = None
        self.target_layers_skinnet = None

        self._load_models()
        self._init_gemini()

    def _init_gemini(self):
        if Config.GOOGLE_API_KEY:
            try:
                genai.configure(api_key=Config.GOOGLE_API_KEY)
                self.gemini = genai.GenerativeModel('gemini-2.0-flash')
            except Exception as e:
                logger.warning(f"Gemini non inizializzato: {e}")

    def _load_models(self):
        # 1. CheXNet
        try:
            model = models.densenet121(pretrained=False)
            model.classifier = torch.nn.Linear(model.classifier.in_features, len(Config.XRAY_LABELS))
            if os.path.exists(Config.CHEXNET_PATH):
                state = torch.load(Config.CHEXNET_PATH, map_location=self.device)
                new_state = {k.replace("module.", ""): v for k, v in state.items()}
                model.load_state_dict(new_state)
                model.to(self.device).eval()
                self.chexnet = model
                self.target_layers_chexnet = [self.chexnet.features[-1]]
                logger.info("✅ CheXNet caricato.")
        except Exception as e:
            logger.error(f"❌ Errore CheXNet: {e}")

        # 2. SkinNet
        try:
            model = models.efficientnet_b0(pretrained=False)
            model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(Config.SKIN_LABELS))
            if os.path.exists(Config.SKIN_PATH):
                model.load_state_dict(torch.load(Config.SKIN_PATH, map_location=self.device))
                model.to(self.device).eval()
                self.skinnet = model
                self.target_layers_skinnet = [self.skinnet.features[-1]]
                logger.info("✅ SkinNet caricato.")
        except Exception as e:
            logger.error(f"❌ Errore SkinNet: {e}")

    # --- XAI VISIVA ---
    def _generate_heatmap_b64(self, model, target_layers, tensor, target_class_idx):
        if not Config.ENABLE_GRADCAM or not target_layers:
            return None

        try:
            cam = GradCAM(model=model, target_layers=target_layers)
            targets = [ClassifierOutputTarget(target_class_idx)]
            grayscale_cam = cam(input_tensor=tensor, targets=targets)[0, :]

            img_tensor = tensor.squeeze(0).cpu()
            mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
            std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
            img_denorm = img_tensor * std + mean
            img_denorm = torch.clamp(img_denorm, 0, 1)
            img_np = img_denorm.permute(1, 2, 0).numpy()

            visualization = show_cam_on_image(img_np, grayscale_cam, use_rgb=True)

            img_pil = Image.fromarray(visualization)
            buffered = io.BytesIO()
            img_pil.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')

        except Exception as e:
            logger.error(f"Errore Grad-CAM: {e}")
            return None

    def _get_llm_explanation(self, diagnosis, context_type):
        if not self.gemini: return "Spiegazione LLM non disponibile."

        # Prompt rigido per forzare la sintesi
        prompt = f"""
        Sei un radiologo esperto che deve scrivere una nota sintetica per un report.
        Contesto: {context_type}.
        Diagnosi rilevata: '{diagnosis}'.

        Compito: Genera una spiegazione di massimo 3 punti elenco, molto concisa.

        Struttura obbligatoria della risposta:
        1. [Cos'è]: Una frase semplice su cosa sia la patologia '{diagnosis}'.
        2. [Segni Visivi]: Cosa tipicamente si vede nell'immagine per questa diagnosi (es. opacità, macchie irregolari).
        3. [Cause Potenziali]: Elenca 2 o 3 cause principali.

        Regole:
        - NON salutare, NON presentarti.
        - NON dare consigli generici (es. "consulta un medico").
        - Massimo 40 parole totali.
        - Usa un linguaggio diretto e professionale.
        """

        try:
            # Limitiamo anche i token in output per sicurezza
            response = self.gemini.generate_content(
                prompt,
                generation_config={"max_output_tokens": 150, "temperature": 0.4}
            )
            return response.text.strip()
        except Exception as e:
            return f"Errore spiegazione: {e}"

    # --- METODO PRINCIPALE ---
    def analyze(self, img_type: str, data: any):
        try:
            # A. RAGGI X
            if img_type == "chest_xray" and self.chexnet:
                if not isinstance(data, list): return {"error": "Serve tensore lista"}
                tensor = torch.tensor(data).float().to(self.device)
                if len(tensor.shape) == 3: tensor = tensor.unsqueeze(0)

                with torch.no_grad():
                    out = self.chexnet(tensor)
                    probs = torch.sigmoid(out)[0]

                top_prob, top_idx = torch.topk(probs, 1)
                top_pathology = Config.XRAY_LABELS[top_idx.item()]

                # Generazione XAI
                heatmap = self._generate_heatmap_b64(self.chexnet, self.target_layers_chexnet, tensor, top_idx.item())
                explanation = self._get_llm_explanation(top_pathology, "Radiografia Torace")

                results = [{"pathology": Config.XRAY_LABELS[i], "probability": round(p.item(), 4)}
                           for i, p in enumerate(probs) if p > 0.05]
                results.sort(key=lambda x: x['probability'], reverse=True)

                return {
                    "status": "success",
                    "primary_finding": top_pathology,
                    "findings_detail": results[:3],
                    "xai_heatmap_base64": heatmap,
                    "xai_explanation_text": explanation
                }

            # B. PELLE
            elif img_type == "skin" and self.skinnet:
                if not isinstance(data, list): return {"error": "Serve tensore lista"}
                tensor = torch.tensor(data).float().to(self.device)
                if len(tensor.shape) == 3: tensor = tensor.unsqueeze(0)

                with torch.no_grad():
                    out = self.skinnet(tensor)
                    probs = F.softmax(out[0], dim=0)

                conf, idx = torch.topk(probs, 1)
                diagnosis = Config.SKIN_LABELS[idx.item()]

                # Generazione XAI
                heatmap = self._generate_heatmap_b64(self.skinnet, self.target_layers_skinnet, tensor, idx.item())
                explanation = self._get_llm_explanation(diagnosis, "Dermatoscopia")

                return {
                    "status": "success",
                    "diagnosis": diagnosis,
                    "confidence": round(conf.item(), 4),
                    "xai_heatmap_base64": heatmap,
                    "xai_explanation_text": explanation
                }

            # C. GENERICO
            elif Config.GOOGLE_API_KEY and self.gemini:
                image_bytes = base64.b64decode(data)
                image = Image.open(io.BytesIO(image_bytes))
                prompt = "Analizza questa immagine medica. Descrivi anomalie visibili."
                response = self.gemini.generate_content([prompt, image])
                return {
                    "status": "success",
                    "analysis": response.text
                }

            return {"error": f"Modello non trovato per: {img_type}"}

        except Exception as e:
            return {"error": str(e)}


image_analyzer = ImageAnalyzer()