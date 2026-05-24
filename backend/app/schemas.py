from pydantic import BaseModel
from typing import List, Optional


class TroubleshootRequest(BaseModel):
    namespace: str
    pod_name: Optional[str] = None
    logs: Optional[str] = None
    events: Optional[str] = None


class TroubleshootResponse(BaseModel):
    id: Optional[int] = None
    issue_summary: str
    possible_causes: List[str]
    recommended_actions: List[str]
    severity: str


class IncidentHistoryResponse(BaseModel):
    id: int
    namespace: str
    pod_name: Optional[str]
    severity: str
    issue_summary: str
    possible_causes: str
    recommended_actions: str

    class Config:
        from_attributes = True