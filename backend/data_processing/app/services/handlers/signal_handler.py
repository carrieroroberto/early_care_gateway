import json
import numpy as np
from ...services.data_processing_handler import DataProcessingHandler

class SignalPreprocessingHandler(DataProcessingHandler):
    """
    Handler responsible for preprocessing signal data (time-series).
    """
    async def handle(self, data: str, strategy: str) -> str:
        # Check if the strategy is 'signal'. If not, pass to the next handler.
        if strategy != "signal":
            return await super().handle(data, strategy)

        # Parse the JSON input into a list
        data_list = json.loads(data)
        # Convert to a NumPy float32 array
        np_arr = np.array(data_list, dtype=np.float32)

        # Apply Min-Max Normalization to scale values between 0 and 1.
        # A small epsilon (1e-8) is added to the denominator to prevent division by zero.
        processed = (np_arr - np_arr.min()) / (np_arr.max() - np_arr.min() + 1e-8)

        # Return the normalized data as a JSON string
        return json.dumps(processed.tolist())