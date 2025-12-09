from abc import ABC, abstractmethod

class AnalysisStrategy(ABC):
    @abstractmethod
    async def analyse(self, payload: dict) -> dict:
        pass