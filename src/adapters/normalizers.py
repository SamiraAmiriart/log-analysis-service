import json
from datetime import datetime
from domain.entities import NormalizedEvent, LogSource, Severity

class LogNormalizer:
    @staticmethod
    def normalize_grafana(payload: dict) -> NormalizedEvent:
        return NormalizedEvent(
            source=LogSource.GRAFANA,
            service_component=payload.get("dashboardId", "unknown"),
            message=payload.get("message", ""),
            severity=LogNormalizer._map_grafana_severity(payload.get("state", "")),
            timestamp=datetime.now(),
            attributes=payload
        )

    @staticmethod
    def normalize_sentry(payload: dict) -> NormalizedEvent:
        return NormalizedEvent(
            source=LogSource.SENTRY,
            service_component=payload.get("project", "unknown"),
            message=payload.get("message", ""),
            severity=LogNormalizer._map_sentry_severity(payload.get("level", "error")),
            timestamp=datetime.now(),
            attributes=payload
        )

    @staticmethod
    def normalize_syslog(payload: str) -> NormalizedEvent:
        # Basic syslog parsing
        parts = payload.split()
        return NormalizedEvent(
            source=LogSource.SYSLOG,
            service_component="syslog",
            message=payload,
            severity=Severity.INFO,
            timestamp=datetime.now(),
            attributes={"raw_message": payload}
        )

    @staticmethod
    def _map_grafana_severity(state: str) -> Severity:
        mapping = {
            "alerting": Severity.CRITICAL,
            "pending": Severity.WARNING,
            "ok": Severity.INFO
        }
        return mapping.get(state.lower(), Severity.INFO)

    @staticmethod
    def _map_sentry_severity(level: str) -> Severity:
        mapping = {
            "fatal": Severity.CRITICAL,
            "error": Severity.CRITICAL,
            "warning": Severity.WARNING,
            "info": Severity.INFO,
            "debug": Severity.INFO
        }
        return mapping.get(level.lower(), Severity.INFO)