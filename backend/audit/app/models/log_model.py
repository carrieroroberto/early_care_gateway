from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, DateTime, func

class Base(DeclarativeBase):
    pass

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)

    patient_id: Mapped[int | None] = mapped_column(ForeignKey("patients.id"), nullable=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    doctor = relationship("Doctor", back_populates="logs", lazy="joined")
    patient = relationship("Patient", back_populates="logs", lazy="joined")