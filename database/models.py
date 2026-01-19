from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from typing import 


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Dictionary(Base):
    __tablename__ = "dictionary"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(30), nullable=False)
    translation: Mapped[str] = mapped_column(String(60), nullable=False)