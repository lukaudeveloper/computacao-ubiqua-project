from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Measurement, Sensor, Alert
import json
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def simulate_sensor_data(db: Session):
    sensors = db.query(Sensor).all()
    for sensor in sensors:
        value = generate_random_value(sensor.type)
        measurement = Measurement(sensor_id=sensor.id, value=value)
        db.add(measurement)
        db.commit()
        # Verificar alertas
        if sensor.threshold_min and value < sensor.threshold_min:
            alert = Alert(sensor_id=sensor.id, message=f"Valor abaixo do mínimo: {value} < {sensor.threshold_min}")
            db.add(alert)
            db.commit()
        elif sensor.threshold_max and value > sensor.threshold_max:
            alert = Alert(sensor_id=sensor.id, message=f"Valor acima do máximo: {value} > {sensor.threshold_max}")
            db.add(alert)
            db.commit()
        # Broadcast para WebSocket
        data = {
            "sensor_id": sensor.id,
            "value": value,
            "timestamp": measurement.timestamp.isoformat(),
            "type": sensor.type
        }
        await manager.broadcast(json.dumps(data))

def generate_random_value(sensor_type: str) -> float:
    if sensor_type == "temperature":
        return round(random.uniform(15, 35), 2)
    elif sensor_type == "humidity":
        return round(random.uniform(30, 80), 2)
    elif sensor_type == "air_quality":
        return round(random.uniform(0, 500), 2)  # AQI
    elif sensor_type == "noise":
        return round(random.uniform(30, 90), 2)  # dB
    return round(random.uniform(0, 100), 2)

scheduler = AsyncIOScheduler()
scheduler.add_job(simulate_sensor_data, IntervalTrigger(seconds=10), args=[next(get_db())])  # Simular a cada 10s
scheduler.start()
