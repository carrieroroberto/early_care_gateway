import torch
import os
import io
import base64
import pickle
import numpy as np
from torchvision import models
import torch.nn.functional as F
from ...utils.ai_models_config import Config
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
from ...services.strategies.I_strategy import AnalysisStrategy
from PIL import Image

class ImageAnalysisStrategy(AnalysisStrategy):
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.chexnet = None
        self.skinnet = None
        self.target_layers_chexnet = None
        self.target_layers_skinnet = None
        self._load_models()

    def _load_models(self):
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
        except Exception as e:
            raise Exception(f"Error loading CheXNet: {e}")

        try:
            model = models.efficientnet_b0(pretrained=False)
            model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(Config.SKIN_LABELS))
            if os.path.exists(Config.EFFICIENTNET_PATH):
                model.load_state_dict(torch.load(Config.EFFICIENTNET_PATH, map_location=self.device))
                model.to(self.device).eval()
                self.skinnet = model
                self.target_layers_skinnet = [self.skinnet.features[-1]]
        except Exception as e:
            raise Exception(f"Error loading SkinNet: {e}")

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
        except Exception:
            return None

    def _base64_to_tensor(self, tensor_b64):
        try:
            raw = base64.b64decode(tensor_b64)
            np_tensor = pickle.loads(raw)

            return torch.from_numpy(np_tensor).float().to(self.device)

        except Exception as e:
            raise Exception(f"Failed to decode base64 tensor: {str(e)}")

    async def analyse(self, payload: dict) -> dict:
        try:
            img_type = payload.get("data").get("type")
            b64tensor = payload.get("data").get("data")

            if not b64tensor:
                return {"error": "No base64 tensor provided"}

            tensor = self._base64_to_tensor(b64tensor)

            if img_type == "img_rx" and self.chexnet:
                with torch.no_grad():
                    out = self.chexnet(tensor)
                    probs = torch.sigmoid(out)[0]

                top_prob, top_idx = torch.topk(probs, 1)
                top_pathology = Config.XRAY_LABELS[top_idx.item()]
                heatmap = self._generate_heatmap_b64(self.chexnet, self.target_layers_chexnet, tensor, top_idx.item())

                return {
                    "diagnosis": top_pathology,
                    "confidence": round(top_prob.item(), 4),
                    "explanation": heatmap
                }

            elif img_type == "img_skin" and self.skinnet:
                with torch.no_grad():
                    out = self.skinnet(tensor)
                    probs = F.softmax(out[0], dim=0)

                conf, idx = torch.topk(probs, 1)
                diagnosis = Config.SKIN_LABELS[idx.item()]
                heatmap = self._generate_heatmap_b64(self.skinnet, self.target_layers_skinnet, tensor, idx.item())

                return {
                    "diagnosis": diagnosis,
                    "confidence": round(conf.item(), 4),
                    "explanation": heatmap
                }

            return {"error": f"No model found for type '{img_type}'"}

        except Exception as e:
            return {"error": str(e)}