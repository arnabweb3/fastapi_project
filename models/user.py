from database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer, String

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True

    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True
    )