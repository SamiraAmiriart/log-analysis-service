from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import NormalizedEvent, AnalysisResult, Rule, Notification


class EventRepository(ABC):
    @abstractmethod
    async def save(self, event: NormalizedEvent) -> str:
        pass

    @abstractmethod
    async def get_by_id(self, event_id: str) -> Optional[NormalizedEvent]:
        pass


class AnalysisRepository(ABC):
    @abstractmethod
    async def save_result(self, result: AnalysisResult) -> str:
        pass

    @abstractmethod
    async def get_by_event_id(self, event_id: str) -> Optional[AnalysisResult]:
        pass


class RuleRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Rule]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Rule]:
        pass


class NotificationRepository(ABC):
    @abstractmethod
    async def save(self, notification: Notification) -> str:
        pass

    @abstractmethod
    async def get_by_event_id(self, event_id: str) -> List[Notification]:
        pass