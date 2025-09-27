from services.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
