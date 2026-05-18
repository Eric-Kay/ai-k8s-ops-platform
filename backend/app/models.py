from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class IncidentAnalysis(Base):
    __tablename__ = "incident_analyses"

    id = Column(Integer, primary_key=True, index=True)
    namespace = Column(String(255), nullable=False)
    pod_name = Column(String(255), nullable=True)
    severity = Column(String(50), nullable=False)
    issue_summary = Column(Text, nullable=False)
    possible_causes = Column(Text, nullable=False)
    recommended_actions = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())