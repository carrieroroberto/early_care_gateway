from abc import ABC, abstractmethod

class AnalysisStrategy(ABC):
    """
    Interface defining the contract for all analysis strategies.
    Implements the Strategy Design Pattern to interchange AI models dynamically.
    """
    @abstractmethod
    async def analyse(self, payload: dict) -> dict:
        """
        Abstract method to perform analysis.
        Must be implemented by concrete strategies (Text, Image, Numeric, Signal).
        """
        pass