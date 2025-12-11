# Import SQLAlchemy components for ORM mapping
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text, func
from datetime import datetime
# Import the shared Base class
from ..utils.db_connection import Base


class ProcessedData(Base):
    """
    Database model representing the 'processed_data' table.
    Stores the result of the data processing handlers.
    """
    __tablename__ = "processed_data"

    # Primary key, auto-incremented integer
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # The type/strategy used for processing (e.g., 'numeric', 'img_rx', 'text')
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    # The actual processed data stored as a text string (often JSON or Base64)
    data: Mapped[str] = mapped_column(Text, nullable=False)

    # Timestamp of creation, defaults to current server time
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)