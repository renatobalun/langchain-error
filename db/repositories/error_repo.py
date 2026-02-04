from __future__ import annotations

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from db.models import Error, ErrorAnalysis, ErrorSolution


def save_error(db: Session, error_payload: Dict[str, Any]) -> Error:
    err = Error(
        name=error_payload.get("error_name", "UnknownError"),
        status_code=error_payload.get("status_code"),
        severity=error_payload.get("severity", "error"),
        detail=error_payload.get("detail"),
        payload=error_payload,
    )
    db.add(err)
    db.flush()
    return err


def save_error_analysis(db: Session, error_id: int, analysis_dict: Dict[str, Any]) -> ErrorAnalysis:
    a = ErrorAnalysis(
        error_id=error_id,
        probable_root_cause=analysis_dict["probable_root_cause"],
        impact_assesment=analysis_dict["impact_assesment"],
        urgency=analysis_dict["urgency"],
        confidence=analysis_dict["confidence"],
        signals_used=analysis_dict.get("signals_used", []),
        immediate_actions=analysis_dict.get("immediate_actions", []),
        deeper_investigation=analysis_dict.get("deeper_investigation", []),
        assumptions=analysis_dict.get("assumptions", []),
    )
    db.add(a)
    return a


def save_error_solution(db: Session, error_id: int, solution_dict: Dict[str, Any]) -> ErrorSolution:
    s = ErrorSolution(
        error_id=error_id,
        code_fixes=solution_dict.get("code_fixes", []),
        configuration_changes=solution_dict.get("configuration_changes", []),
        deployment_steps=solution_dict.get("deployment_steps", []),
        rollback_plan=solution_dict.get("rollback_plan", {"signals_to_monitor": [], "steps": []}),
    )
    db.add(s)
    return s