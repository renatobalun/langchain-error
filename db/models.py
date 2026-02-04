from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from db.base import Base

class Error(Base):
    __tablename__ = "errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # osnovno iz payload-a
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)  # "error"|"warning"|"info"
    detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # sve ostalo spremi kao JSON (context, metrics, suggested_checks, itd.)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # one-to-one (po erroru max 1 analysis i 1 solution)
    analysis: Mapped[Optional["ErrorAnalysis"]] = relationship(
        back_populates="error",
        uselist=False,
        cascade="all, delete-orphan",
    )
    solution: Mapped[Optional["ErrorSolution"]] = relationship(
        back_populates="error",
        uselist=False,
        cascade="all, delete-orphan",
    )


class ErrorAnalysis(Base):
    __tablename__ = "error_analyses"
    __table_args__ = (
        UniqueConstraint("error_id", name="uq_error_analyses_error_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    error_id: Mapped[int] = mapped_column(ForeignKey("errors.id", ondelete="CASCADE"), nullable=False, unique=True)

    probable_root_cause: Mapped[str] = mapped_column(Text, nullable=False)
    impact_assesment: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[str] = mapped_column(String(20), nullable=False)  # Severity Literal
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    # liste spremamo kao JSON array
    signals_used: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    immediate_actions: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    deeper_investigation: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    assumptions: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    error: Mapped["Error"] = relationship(back_populates="analysis")


class ErrorSolution(Base):
    __tablename__ = "error_solutions"
    __table_args__ = (
        UniqueConstraint("error_id", name="uq_error_solutions_error_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    error_id: Mapped[int] = mapped_column(ForeignKey("errors.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Ovo su list/object strukture iz Pydantic modela -> najlakše JSONB
    code_fixes: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    configuration_changes: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=False, default=list)
    deployment_steps: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    rollback_plan: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    error: Mapped["Error"] = relationship(back_populates="solution")
