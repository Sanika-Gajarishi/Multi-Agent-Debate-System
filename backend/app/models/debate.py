from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.database import Base


class Debate(Base):
    """
    Database model for a completed debate.
    """

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