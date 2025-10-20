from abc import ABC, abstractmethod
from domain.entities import AnalysisResult


class Notifier(ABC):
    @abstractmethod
    async def send(self, result: AnalysisResult) -> bool:
        pass


class TelegramNotifier(Notifier):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def send(self, result: AnalysisResult) -> bool:
        # Implementation for Telegram bot
        message = f"""
🚨 Log Alert
Severity: {result.severity.value}
Action: {result.action.value}
Service: {result.normalized_event.service_component}
Message: {result.normalized_event.message}
Analysis: {result.analysis}
        """

        # Here you would implement actual Telegram API call
        print(f"Telegram notification sent: {message}")
        return True


class SMSNotifier(Notifier):
    async def send(self, result: AnalysisResult) -> bool:
        # Stub implementation
        print(f"SMS notification would be sent for: {result.normalized_event.message}")
        return True


class NotificationService:
    def __init__(self):
        self.notifiers: dict[str, Notifier] = {}

    def register_notifier(self, channel: str, notifier: Notifier):
        self.notifiers[channel] = notifier

    async def notify(self, result: AnalysisResult) -> dict[str, bool]:
        outcomes = {}

        if result.action.value == "notify":
            for channel, notifier in self.notifiers.items():
                outcomes[channel] = await notifier.send(result)

        return outcomes