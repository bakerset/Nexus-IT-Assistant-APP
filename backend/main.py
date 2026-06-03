from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db
from routers import notes, tickets, devices, infrastructure, threats, agent

# Initialize database
init_db()

app = FastAPI(title="Nexus IT Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["Tickets"])
app.include_router(devices.router, prefix="/api/devices", tags=["Devices"])
app.include_router(infrastructure.router, prefix="/api/infrastructure", tags=["Infrastructure"])
app.include_router(threats.router, prefix="/api/threats", tags=["Threats"])
app.include_router(agent.router, prefix="/api/agent", tags=["Agent"])

@app.get("/")
def read_root():
    return {"message": "Nexus IT Assistant API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
