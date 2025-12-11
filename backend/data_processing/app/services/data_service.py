from typing import List, Dict, Any
# Import specific concrete handlers for the processing chain
from ..services.handlers.image_handler import ImagePreprocessingHandler
from ..services.handlers.numeric_handler import NumericPreprocessingHandler
from ..services.handlers.signal_handler import SignalPreprocessingHandler
from ..services.handlers.text_handler import TextPreprocessingHandler
# Import models and repository interfaces
from ..models.data_model import ProcessedData
from ..repositories.I_data_repository import IProcessedDataRepository
from ..schemas.data_schema import DataRequest, DataResponse, GetDataResponse, ProcessedDataItem
# Import utility for HTTP requests and Observer interface for logging
from ..utils.http_client import HttpClient
from ..utils.logging.I_observer import IObserver

class DataProcessingService:
    """
    Service responsible for handling data processing requests.
    It builds a Chain of Responsibility to process raw data and manages database persistence.
    It also acts as a Subject in the Observer pattern to notify the Audit service.
    """
    def __init__(self, data_repository: IProcessedDataRepository, http_client: HttpClient):
        # Inject dependencies
        self.data_repository = data_repository
        self.http = http_client
        # List to hold attached observers
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver):
        """
        Attaches an observer to the service.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver):
        """
        Detaches an observer from the service.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify(self, payload: Dict[str, Any]):
        """
        Notifies all observers of an event.
        """
        for observer in self._observers:
            await observer.update(payload)

    def _build_preprocessing_chain(self):
        """
        Constructs the Chain of Responsibility for data preprocessing.
        Order: Text -> Image -> Numeric -> Signal
        """
        text = TextPreprocessingHandler()
        image = ImagePreprocessingHandler()
        numeric = NumericPreprocessingHandler()
        signal = SignalPreprocessingHandler()

        # Link the handlers together
        text.set_next(image).set_next(numeric).set_next(signal)

        # Return the first handler in the chain
        return text

    async def process(self, data_request: DataRequest) -> DataResponse:
        """
        Processes the incoming raw data using the handler chain.
        """
        # Build the chain
        chain = self._build_preprocessing_chain()
        # Pass data through the chain (the appropriate handler will process it based on 'strategy')
        processed = await chain.handle(data_request.raw_data, data_request.strategy)

        # Create a data model instance with the result
        processed_data = ProcessedData(
            type=data_request.strategy,
            data=processed
        )

        # Save the processed data to the database via repository
        processed_data_id = await self.data_repository.save(processed_data)

        # Notify observers (Audit service) about the successful processing
        await self.notify({
            "service": "data_processing",
            "event": "data_processed",
            "description": "Processed data stored in the database",
            "data_id": processed_data_id
        })

        return DataResponse(processed_data_id=processed_data_id)

    async def retrieve(self, id: int) -> GetDataResponse:
        """
        Retrieves processed data from the database by ID.
        """
        # Fetch data using repository
        data = await self.data_repository.find_by_id(id)

        # Notify observers that data was accessed
        await self.notify({
            "service": "data_processing",
            "event": "data_retrieved",
            "description": "Processed data requested for analysis",
            "data_id": data.id
        })

        # Return the data mapped to the response schema
        return GetDataResponse(data=ProcessedDataItem.model_validate(data))