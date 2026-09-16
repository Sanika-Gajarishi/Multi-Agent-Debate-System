from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.database import Base

DATABASE_URL = "sqlite:///./debates.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class Debate(Base):

    __tablename__ = "debates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    rounds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    debate_history: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    research_analysis: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    critique: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    judge_result: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )