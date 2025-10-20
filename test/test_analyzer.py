import pytest
from datetime import datetime
from domain.entities import NormalizedEvent, LogSource, Severity
from application.services import LogAnalyzer


class TestLogAnalyzer:
    @pytest.fixture
    def sample_event(self):
        return NormalizedEvent(
            source=LogSource.GRAFANA,
            service_component="backend-api",
            message="High CPU usage detected",
            severity=Severity.WARNING,
            timestamp=datetime.now(),
            attributes={"cpu_usage": "95%"}
        )

    @pytest.mark.asyncio
    async def test_analyze_event(self, sample_event):
        # Mock repositories would be used here
        analyzer = LogAnalyzer(None, None, None)
        result = await analyzer.analyze(sample_event)

        assert result.action.value in ["ignore", "notify", "escalate"]
        assert result.severity.value in ["info", "warning", "critical"]
        assert isinstance(result.analysis, str)
