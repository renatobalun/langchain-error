from pydantic import BaseModel, Field
from typing import List, Literal

Severity = Literal["error", "warning", "info"]

#tablica Error
#tablica ErrorAnalysis
#tablica ErrorSolution

class ErrorAnalysis(BaseModel):
    error_name: str
    probable_root_cause: str
    impact_assesment: str
    urgency: Severity
    confidence: float = Field(ge=0, le=1)
    signals_used: List[str]
    immediate_actions: List[str]
    deeper_investigation: List[str]
    assumptions: List[str] = []

class CodeFix(BaseModel):
    file: str
    description: str
    code: str
    
class ConfigurationChange(BaseModel):
    key: str
    value: str
    reason: str
    
class RollbackPlan(BaseModel):
    signals_to_monitor: List[str]
    steps: List[str]

class ErrorSolution(BaseModel):
    code_fixes: List[CodeFix]
    configuration_changes: List[ConfigurationChange]
    deployment_steps: List[str]
    rollback_plan: RollbackPlan
    