from pydantic import BaseModel, Field
from typing import List, Literal

Severity = Literal["critical", "high", "medium", "low"]

class ErrorAnalysis(BaseModel):
    error_id: str
    error_name: str
    severity: Severity
    probable_root_cause: str
    impact_assesment: str
    urgency: Severity
    confidence: float = Field(ge=0, le=1)
    signals_used: List[str]
    immediate_actions: List[str]
    deeper_investigation: List[str]
    assumptions: List[str] = []