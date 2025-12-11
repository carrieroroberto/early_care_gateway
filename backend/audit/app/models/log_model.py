from datetime import datetime
# Import SQLAlchemy ORM components
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func
# Import the shared Base class
from ..utils.db_connection import Base


class Log(Base):
    """
    Database model representing the 'logs' table.
    Stores audit information about events occurring across microservices.
    """
    __tablename__ = "logs"

    # Primary key, auto-incremented
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Timestamp of when the log was created (server default to NOW)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Name of the microservice that generated the log (e.g., 'authentication', 'data_processing')
    service: Mapped[str] = mapped_column(String(50), nullable=False)

    # Type of event (e.g., 'login_success', 'analysis_completed')
    event: Mapped[str] = mapped_column(String(50), nullable=False)

    # Detailed description of the event
    description: Mapped[str] = mapped_column(String(100), nullable=False)

    # Optional foreign key references to link logs to specific entities
    doctor_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    patient_hashed_cf: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_id: Mapped[int | None] = mapped_column(Integer, nullable=True)