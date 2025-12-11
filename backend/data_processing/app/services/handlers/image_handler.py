import base64
import pickle
from io import BytesIO
# Import PIL for image manipulation and NumPy for array operations
from PIL import Image, ImageEnhance
import numpy as np
# Import exposure from skimage (though not currently used in the active logic)
from skimage import exposure
from ...services.data_processing_handler import DataProcessingHandler


class ImagePreprocessingHandler(DataProcessingHandler):
    """
    Handler responsible for preprocessing image data.
    Typically used for strategies like 'img_rx' (X-ray) or 'img_skin'.
    """

    async def handle(self, data: str, strategy: str) -> str:
        # Check if the strategy is related to images. If not, pass to the next handler.
        if strategy not in ("img_rx", "img_skin"):
            return await super().handle(data, strategy)

        # Decode the Base64 input string into bytes
        image_bytes = base64.b64decode(data)
        # Open the image using PIL and convert it to RGB mode
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        # Resize the image to 224x224 pixels (standard input size for many CNN models)
        img = img.resize((224, 224))

        # Convert image to a NumPy array and normalize pixel values to range [0, 1]
        img_array = np.array(img).astype(np.float32) / 255.0

        # Define mean and standard deviation for normalization (standard ImageNet values)
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])

        # Apply standardization: (input - mean) / std
        img_array = (img_array - mean) / std

        # Transpose the array dimensions from (Height, Width, Channels) to (Channels, Height, Width)
        # This is the format required by PyTorch models.
        tensor = np.transpose(img_array, (2, 0, 1))

        # Add a batch dimension at index 0 (Result shape: 1, C, H, W)
        tensor = np.expand_dims(tensor, 0)
        tensor = tensor.astype(np.float32)

        # Serialize the processed tensor using pickle
        serialized = pickle.dumps(tensor)
        # Encode the serialized data back to Base64 string for transport
        tensor_b64 = base64.b64encode(serialized).decode('utf-8')

        return tensor_b64