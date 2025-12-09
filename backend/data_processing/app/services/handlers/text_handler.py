from ...services.data_processing_handler import DataProcessingHandler
import re

class TextPreprocessingHandler(DataProcessingHandler):
    STOP_WORDS = {"the", "a", "an", "of", "and", "in", "on"}

    async def handle(self, data: str, strategy: str) -> str:
        if strategy != "text":
            return await super().handle(data, strategy)

        if not data:
            text = ""

        text = re.sub(r'\s+', ' ', data).strip()

        return text