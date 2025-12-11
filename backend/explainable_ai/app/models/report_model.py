# Import SQLAlchemy components for ORM mapping and data types
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Float, Text, func
from datetime import datetime
# Import the shared Base class for database models
from ..utils.db_connection import Base


class Report(Base):
    """
    Database model representing the 'reports' table.
    Stores the final results of the AI analysis.
    """
    __tablename__ = "reports"

    # Primary key: Unique identifier for the report
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # ID of the doctor who requested the analysis
    doctor_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Hashed fiscal code of the patient to ensure privacy
    patient_hashed_cf: Mapped[str] = mapped_column(String(255), nullable=False)

    # Reference ID to the processed data used for this analysis
    processed_data_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Timestamp of report creation, defaults to server time
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # The strategy used (e.g., 'img_rx', 'text', 'numeric')
    strategy: Mapped[str] = mapped_column(String(255), nullable=False)

    # The outcome of the analysis (e.g., "Pneumonia", "High Risk")
    diagnosis: Mapped[str] = mapped_column(String(255), nullable=False)

    # Confidence score of the AI model (0.0 to 1.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    # Textual or visual explanation of the result (e.g., SHAP values, heatmap base64, text reasoning)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)