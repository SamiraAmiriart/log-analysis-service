from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class LogSource(Enum):
    GRAFANA = "grafana"
    SENTRY = "sentry"
    SYSLOG = "syslog"
    FILE = "file"

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class Action(Enum):
    IGNORE = "ignore"
    NOTIFY = "notify"
    ESCALATE = "escalate"

@dataclass
class NormalizedEvent:
    source: LogSource
    service_component: str
    message: str
    severity: Severity
    timestamp: datetime
    attributes: Dict[str, Any]

@dataclass
class AnalysisResult:
    action: Action
    severity: Severity
    analysis: str
    normalized_event: NormalizedEvent

@dataclass
class Rule:
    name: str
    condition: str
    action: Action
    severity: Severity
    description: str

@dataclass
class Notification:
    id: str
    event_id: str
    channel: str
    message: str
    sent_at: datetime
    status: str