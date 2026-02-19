"""
RIFT 2026 — Autonomous CI/CD Healing Agent
Main FastAPI Application Entry Point
"""

import os
import json
import asyncio
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from api.routes import router as agent_router

app = FastAPI(
    title="RIFT 2026 — CI/CD Healing Agent API",
    description="Autonomous agent that detects, fixes, and verifies CI/CD pipeline failures",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://*.vercel.app",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api")

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[run_id] = websocket

    def disconnect(self, run_id: str):
        self.active_connections.pop(run_id, None)

    async def send_update(self, run_id: str, data: dict):
        ws = self.active_connections.get(run_id)
        if ws:
            try:
                await ws.send_json(data)
            except Exception:
                self.disconnect(run_id)

manager = ConnectionManager()

@app.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await manager.connect(run_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(run_id)

app.state.ws_manager = manager

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True,
    )