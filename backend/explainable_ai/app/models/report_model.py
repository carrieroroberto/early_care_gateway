from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Float, Text, func
from datetime import datetime
from ..utils.db_connection import Base

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doctor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    patient_hashed_cf: Mapped[str] = mapped_column(String(255), nullable=False)
    processed_data_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    strategy: Mapped[str] = mapped_column(String(255), nullable=False)
    diagnosis: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)