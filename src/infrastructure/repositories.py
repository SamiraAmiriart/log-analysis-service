import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from domain.entities import NormalizedEvent, AnalysisResult, Rule, Notification, LogSource, Severity, Action
from domain.repositories import EventRepository, AnalysisRepository, RuleRepository, NotificationRepository


class SQLiteEventRepository(EventRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    service_component TEXT NOT NULL,
                    message TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    attributes TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    async def save(self, event: NormalizedEvent) -> str:
        import uuid
        event_id = str(uuid.uuid4())

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id,
                    event.source.value,
                    event.service_component,
                    event.message,
                    event.severity.value,
                    event.timestamp.isoformat(),
                    json.dumps(event.attributes),
                    datetime.now().isoformat()
                )
            )

        return event_id

    async def get_by_id(self, event_id: str) -> Optional[NormalizedEvent]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM events WHERE id = ?", (event_id,)
            ).fetchone()

            if row:
                return NormalizedEvent(
                    source=LogSource(row[1]),
                    service_component=row[2],
                    message=row[3],
                    severity=Severity(row[4]),
                    timestamp=datetime.fromisoformat(row[5]),
                    attributes=json.loads(row[6])
                )
        return None

# Similar implementations for other repositories...
# (SQLiteAnalysisRepository, SQLiteRuleRepository, SQLiteNotificationRepository)
