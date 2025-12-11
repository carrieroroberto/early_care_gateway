# Import SQLAlchemy components for defining ORM mappings
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
# Import the shared Base class for database models
from ..utils.db_connection import Base


class Doctor(Base):
    """
    Database model representing the 'doctors' table.
    """
    __tablename__ = "doctors"

    # Primary key: Unique identifier for the doctor, auto-incremented
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Doctor's first name, required field, max length 50
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Doctor's last name, required field, max length 50
    surname: Mapped[str] = mapped_column(String(50), nullable=False)

    # Doctor's email, must be unique across the table, required
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Encrypted password, required
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)