from ...services.data_processing_handler import DataProcessingHandler
import re

class TextPreprocessingHandler(DataProcessingHandler):
    """
    Handler responsible for preprocessing text data.
    """
    # Set of common stop words (currently defined but not used in the logic below)
    STOP_WORDS = {"the", "a", "an", "of", "and", "in", "on"}

    async def handle(self, data: str, strategy: str) -> str:
        # Check if the strategy is 'text'. If not, pass to the next handler.
        if strategy != "text":
            return await super().handle(data, strategy)

        # Handle case where data might be None
        if not data:
            text = ""

        # Replace multiple whitespace characters (tabs, newlines, spaces) with a single space
        # and strip leading/trailing whitespace.
        text = re.sub(r'\s+', ' ', data).strip()

        return text