import json
import pickle
import numpy as np
from ...services.data_processing_handler import DataProcessingHandler
import base64

class SignalPreprocessingHandler(DataProcessingHandler):
    async def handle(self, data: str, strategy: str) -> str:
        if strategy != "signal":
            return await super().handle(data, strategy)

        data_list = json.loads(data)
        np_arr = np.array(data_list, dtype=np.float32)

        processed = (np_arr - np_arr.min()) / (np_arr.max() - np_arr.min() + 1e-8)

        serialized = pickle.dumps(processed)
        b64_encoded = base64.b64encode(serialized).decode('utf-8')
        return b64_encoded