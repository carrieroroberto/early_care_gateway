import json
import numpy as np
import pickle
import base64
from ...services.data_processing_handler import DataProcessingHandler

class NumericPreprocessingHandler(DataProcessingHandler):

    HEART_FEATURES = [
        'age', 'trestbps', 'chol', 'thalch', 'oldpeak', 'ca',
        'sex_Male', 'cp_atypical angina', 'cp_non-anginal', 'cp_typical angina',
        'fbs_True', 'restecg_normal', 'restecg_st-t abnormality', 'exang_True',
        'slope_flat', 'slope_upsloping', 'thal_normal', 'thal_reversable defect'
    ]

    async def handle(self, data: str, strategy: str) -> str:
        if strategy != "numeric":
            return await super().handle(data, strategy)

        values = json.loads(data)

        np_arr = np.array(values, dtype=np.float32)

        serialized = pickle.dumps(np_arr)
        b64_encoded = base64.b64encode(serialized).decode('utf-8')

        return b64_encoded