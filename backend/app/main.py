from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.schemas import TroubleshootRequest, TroubleshootResponse, IncidentHistoryResponse
from app.ai_engine import analyse_with_ai
from app.k8s_client import get_pod_logs, get_namespace_events, list_pods
from app.database import Base, engine, get_db
from app.models import IncidentAnalysis

app = FastAPI(
    title="AI Kubernetes Operations Platform",
    description="AI-assisted Kubernetes troubleshooting with PostgreSQL incident history",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    print("Application startup complete")


@app.get("/")
def root():
    return {"message": "AI Kubernetes Operations Platform API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/pods/{namespace}")
def get_pods(namespace: str):
    return {
        "namespace": namespace,
        "pods": list_pods(namespace)
    }


@app.post("/troubleshoot", response_model=TroubleshootResponse)
def troubleshoot(request: TroubleshootRequest, db: Session = Depends(get_db)):
    logs = request.logs
    events = request.events

    if request.pod_name and not logs:
        logs = get_pod_logs(request.namespace, request.pod_name)

    if not events:
        events = get_namespace_events(request.namespace)

    result = analyse_with_ai(logs or "", events or "")

    record = IncidentAnalysis(
        namespace=request.namespace,
        pod_name=request.pod_name,
        severity=result["severity"],
        issue_summary=result["issue_summary"],
        possible_causes="\n".join(result["possible_causes"]),
        recommended_actions="\n".join(result["recommended_actions"]),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return TroubleshootResponse(
        id=record.id,
        issue_summary=result["issue_summary"],
        possible_causes=result["possible_causes"],
        recommended_actions=result["recommended_actions"],
        severity=result["severity"],
    )


@app.get("/history", response_model=list[IncidentHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(IncidentAnalysis).order_by(IncidentAnalysis.id.desc()).limit(20).all()