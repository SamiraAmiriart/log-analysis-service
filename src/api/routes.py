from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from domain.entities import NormalizedEvent, AnalysisResult
from application.services import LogAnalyzer
from application.notification_service import NotificationService
from adapters.normalizers import LogNormalizer

app = FastAPI(title="Log Analysis Hub")

# Dependency injection would be handled properly in a real implementation
analyzer: LogAnalyzer = None
notification_service: NotificationService = None


class WebhookPayload(BaseModel):
    source: str
    payload: Dict[str, Any]


class AnalysisResponse(BaseModel):
    action: str
    severity: str
    analysis: str
    normalized_event: Dict[str, Any]


@app.post("/webhook/{source}")
async def ingest_webhook(source: str, payload: dict, background_tasks: BackgroundTasks):
    try:
        # Normalize based on source
        if source == "grafana":
            normalized_event = LogNormalizer.normalize_grafana(payload)
        elif source == "sentry":
            normalized_event = LogNormalizer.normalize_sentry(payload)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported source: {source}")

        # Analyze
        result = await analyzer.analyze(normalized_event)

        # Trigger notifications in background
        background_tasks.add_task(notification_service.notify, result)

        return AnalysisResponse(
            action=result.action.value,
            severity=result.severity.value,
            analysis=result.analysis,
            normalized_event={
                "source": normalized_event.source.value,
                "service_component": normalized_event.service_component,
                "message": normalized_event.message,
                "severity": normalized_event.severity.value,
                "timestamp": normalized_event.timestamp.isoformat(),
                "attributes": normalized_event.attributes
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}