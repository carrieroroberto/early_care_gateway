import json
import numpy as np
from ...services.data_processing_handler import DataProcessingHandler

class NumericPreprocessingHandler(DataProcessingHandler):
    """
    Handler responsible for preprocessing structured numeric data.
    """

    # List of expected features for heart disease analysis
    HEART_FEATURES = [
        'age', 'trestbps', 'chol', 'thalch', 'oldpeak', 'ca',
        'sex_Male', 'cp_atypical angina', 'cp_non-anginal', 'cp_typical angina',
        'fbs_True', 'restecg_normal', 'restecg_st-t abnormality', 'exang_True',
        'slope_flat', 'slope_upsloping', 'thal_normal', 'thal_reversable defect'
    ]

    async def handle(self, data: str, strategy: str) -> str:
        # Check if the strategy is 'numeric'. If not, pass to the next handler.
        if strategy != "numeric":
            return await super().handle(data, strategy)

        # Parse the JSON string input into a Python list
        values = json.loads(data)

        # Convert the list to a NumPy array with float32 precision
        np_arr = np.array(values, dtype=np.float32)

        # Convert back to a list and then to a JSON string
        return json.dumps(np_arr.tolist())