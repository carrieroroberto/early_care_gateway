from typing import List, Dict, Any
from ..services.handlers.image_handler import ImagePreprocessingHandler
from ..services.handlers.numeric_handler import NumericPreprocessingHandler
from ..services.handlers.signal_handler import SignalPreprocessingHandler
from ..services.handlers.text_handler import TextPreprocessingHandler
from ..models.data_model import ProcessedData
from ..repositories.I_data_repository import IProcessedDataRepository
from ..schemas.data_schema import DataRequest, DataResponse, GetDataResponse, ProcessedDataItem
from ..utils.http_client import HttpClient
from ..utils.logging.I_observer import IObserver

class DataProcessingService:
    def __init__(self, data_repository: IProcessedDataRepository, http_client: HttpClient):
        self.data_repository = data_repository
        self.http = http_client
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, payload: Dict[str, Any]):
        for observer in self._observers:
            await observer.update(payload)

    def _build_preprocessing_chain(self):
        text = TextPreprocessingHandler()
        image = ImagePreprocessingHandler()
        numeric = NumericPreprocessingHandler()
        signal = SignalPreprocessingHandler()

        text.set_next(image).set_next(numeric).set_next(signal)

        return text

    async def process(self, data_request: DataRequest) -> DataResponse:
        chain = self._build_preprocessing_chain()
        processed = await chain.handle(data_request.raw_data, data_request.strategy)

        processed_data = ProcessedData(
            type=data_request.strategy,
            data=processed
        )

        processed_data_id = await self.data_repository.save(processed_data)

        await self.notify({
            "service": "data_processing",
            "event": "data_processed",
            "description": "Processed data stored in the database",
            "data_id": processed_data_id
        })

        return DataResponse(processed_data_id=processed_data_id)

    async def retrieve(self, id: int) -> GetDataResponse:
        data = await self.data_repository.find_by_id(id)

        await self.notify({
            "service": "data_processing",
            "event": "data_retrieved",
            "description": "Processed data requested for analysis",
            "data_id": data.id
        })

        return GetDataResponse(data=ProcessedDataItem.model_validate(data))