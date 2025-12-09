import base64
import pickle
from io import BytesIO
from PIL import Image, ImageEnhance
import numpy as np
from skimage import exposure
from ...services.data_processing_handler import DataProcessingHandler

class ImagePreprocessingHandler(DataProcessingHandler):
    async def handle(self, data: str, strategy: str) -> str:
        if strategy not in ("img_rx", "img_skin"):
            return await super().handle(data, strategy)

        image_bytes = base64.b64decode(data)
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img = img.resize((224, 224))

        img_array = np.array(img).astype(np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_array = (img_array - mean) / std

        tensor = np.transpose(img_array, (2, 0, 1))
        tensor = np.expand_dims(tensor, 0)
        tensor = tensor.astype(np.float32)

        serialized = pickle.dumps(tensor)
        tensor_b64 = base64.b64encode(serialized).decode('utf-8')

        return tensor_b64