from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func
from ..utils.db_connection import Base

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    service: Mapped[str] = mapped_column(String(50), nullable=False)
    event: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    doctor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    patient_hashed_cf: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_id: Mapped[int | None] = mapped_column(Integer, nullable=True)