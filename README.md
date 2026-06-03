# Nexus IT Assistant

An intelligent IT operations assistant combining LangChain + Ollama with threat intelligence and device management.

## Features

- **AI Assistant** - Chat interface with LangChain + Ollama for IT tasks
- **Threat Intelligence** - CISA KEV, NVD CVE, and AlienVault OTX integration
- **Device Management** - Hardware inventory tracking and scanning
- **Notes & Tickets** - Quick note capture and ticket management
- **Infrastructure Monitoring** - Track and manage IT infrastructure
- **Proactive Nudges** - AI-driven insights and recommendations

## Project Structure

```
nexus/
├── backend/          # FastAPI REST API
│   ├── models/       # SQLModel table definitions
│   ├── routers/      # API route handlers
│   ├── agent/        # LangChain + Ollama integration
│   ├── feeds/        # Threat intelligence fetchers
│   ├── scripts/      # Utility scripts
│   └── main.py       # FastAPI app entry point
└── frontend/         # React + Tailwind UI
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── hooks/
    │   └── api/
    └── package.json
```

## Getting Started

### Backend Setup

1. Navigate to `nexus/backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` with your API keys
6. Start the API: `python main.py`

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to `nexus/frontend/`
2. Install dependencies: `npm install`
3. Start dev server: `npm run dev`

The frontend will be available at `http://localhost:5173`

## Requirements

- Python 3.9+
- Node.js 18+
- Ollama (for local LLM)
- SQLite3

## Configuration

Create `nexus/backend/.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
CISA_API_KEY=your_key
NVD_API_KEY=your_key
OTX_API_KEY=your_key
```

## License

MIT
