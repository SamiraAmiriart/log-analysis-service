# Log Analysis Service

A production-ready log analysis service built with FastAPI, following Clean Architecture principles.

##  Features

- **Multi-source Ingestion**: Grafana, Sentry, Syslog webhooks
- **Smart Normalization**: Unified event format
- **Rule-based Analysis**: YAML-configurable rules
- **Multiple Notifications**: Telegram, SMS, etc.
- **Caching**: Intelligent result caching
- **Docker Ready**: One-command deployment

##  Architecture

┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Webhooks │───▶│ Normalization │───▶│ Rule Engine │
│ (Grafana, │ │ │ │ │
│ Sentry, ...) │ └──────────────────┘ └─────────────────┘
└─────────────────┘ │ │
│ │
▼ ▼
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Notifications │◀───│ Analysis │ │ Persistence │
│ (Telegram, │ │ Results │ │ (SQLite/PostgreSQL)
│ SMS, ...) │ └──────────────────┘ └─────────────────┘
└─────────────────┘


##  Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local development)

### Run with Docker
```bash
git clone https://github.com/SamiraAmiriart/log-analysis-service.git
cd log-analysis-service

# Set optional environment variables
export TELEGRAM_BOT_TOKEN=your_bot_token
export TELEGRAM_CHAT_ID=your_chat_id

docker-compose up -d
