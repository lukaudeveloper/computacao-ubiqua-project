from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
from routers import users, sensors, measurements, alerts
from auth import verify_token
from websocket import manager, update_sensor_jobs
import uvicorn

# Criar tabelas e garantir coluna de ativação
Base.metadata.create_all(bind=engine)
with engine.begin() as conn:
    inspector = inspect(conn)
    if "sensors" in inspector.get_table_names():
        columns = [column["name"] for column in inspector.get_columns("sensors")]
        if "is_active" not in columns:
            conn.execute(text("ALTER TABLE sensors ADD COLUMN is_active BOOLEAN DEFAULT FALSE"))
        if "color" not in columns:
            conn.execute(text("ALTER TABLE sensors ADD COLUMN color VARCHAR(20) DEFAULT '#007bff'"))
        if "simulation_interval" not in columns:
            conn.execute(text("ALTER TABLE sensors ADD COLUMN simulation_interval INT DEFAULT 30"))
    if "alerts" in inspector.get_table_names():
        columns = [column["name"] for column in inspector.get_columns("alerts")]
        if "threshold_value" not in columns:
            conn.execute(text("ALTER TABLE alerts ADD COLUMN threshold_value FLOAT NULL"))
        if "measurement_value" not in columns:
            conn.execute(text("ALTER TABLE alerts ADD COLUMN measurement_value FLOAT NULL"))
        if "comparison" not in columns:
            conn.execute(text("ALTER TABLE alerts ADD COLUMN comparison VARCHAR(1) NULL"))

app = FastAPI(title="Sistema de Monitorização Ambiental", version="1.0.0")

# Evento de startup para configurar jobs do scheduler
@app.on_event("startup")
def startup_event():
    from websocket import scheduler
    if not scheduler.running:
        scheduler.start()
    update_sensor_jobs()

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, prefix="/api/auth")
app.include_router(sensors.router, prefix="/api")
app.include_router(measurements.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Pode processar mensagens do cliente se necessário
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
def read_root():
    return {"message": "Sistema de Monitorização Ambiental Inteligente"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
