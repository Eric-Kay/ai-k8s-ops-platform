from pydantic import BaseModel
from typing import List, Optional


class TroubleshootRequest(BaseModel):
    issue: str


class TroubleshootResponse(BaseModel):
    diagnosis: str
    recommendation: str


class IncidentHistoryResponse(BaseModel):
    incidents: List[str]


class IncidentCreate(BaseModel):
    issue: str
    diagnosis: str
    recommendation: str


class HealthResponse(BaseModel):
    status: str