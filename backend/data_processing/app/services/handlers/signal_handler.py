import json
import numpy as np
from ...services.data_processing_handler import DataProcessingHandler

class SignalPreprocessingHandler(DataProcessingHandler):
    async def handle(self, data: str, strategy: str) -> str:
        if strategy != "signal":
            return await super().handle(data, strategy)

        data_list = json.loads(data)
        np_arr = np.array(data_list, dtype=np.float32)

        processed = (np_arr - np_arr.min()) / (np_arr.max() - np_arr.min() + 1e-8)

        return json.dumps(processed.tolist())