from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Measurement, Sensor, Alert
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

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

# Configuração do scheduler
jobstores = {
    'default': MemoryJobStore()
}
executors = {
    'default': AsyncIOExecutor()
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='UTC')

async def simulate_single_sensor(sensor_id: int):
    """Simula dados para um sensor específico"""
    db = next(get_db())
    try:
        sensor = db.query(Sensor).filter(Sensor.id == sensor_id, Sensor.is_active == True).first()
        if not sensor:
            # Sensor não existe ou não está ativo, remover job
            scheduler.remove_job(f"sensor_{sensor_id}")
            return

        # Usar a mesma lógica de simulação do endpoint /simulate
        from routers.sensors import simulate_value
        value = simulate_value(sensor)
        measurement = Measurement(sensor_id=sensor.id, value=value)
        db.add(measurement)
        db.commit()
        db.refresh(measurement)

        # Verificar alertas usando a função existente
        from routers.measurements import check_alerts
        check_alerts(sensor, value, db)

        # Broadcast para WebSocket
        data = {
            "type": "measurement",
            "data": {
                "sensor_id": sensor.id,
                "sensor_name": sensor.name,
                "sensor_type": sensor.type,
                "sensor_color": sensor.color,
                "value": value,
                "timestamp": measurement.timestamp.isoformat(),
            }
        }
        await manager.broadcast(json.dumps(data))

        # Verificar se há alertas recentes para broadcast
        recent_alerts = db.query(Alert).filter(
            Alert.sensor_id == sensor.id,
            Alert.is_active == True
        ).order_by(Alert.timestamp.desc()).limit(1).all()

        for alert in recent_alerts:
            alert_data = {
                "type": "alert",
                "data": {
                    "id": alert.id,
                    "sensor_id": alert.sensor_id,
                    "sensor_name": sensor.name,
                    "sensor_type": sensor.type,
                    "sensor_color": sensor.color,
                    "message": alert.message,
                    "threshold_value": alert.threshold_value,
                    "measurement_value": alert.measurement_value,
                    "comparison": alert.comparison,
                    "timestamp": alert.timestamp.isoformat(),
                    "is_active": alert.is_active,
                }
            }
            await manager.broadcast(json.dumps(alert_data))

    finally:
        db.close()

def update_sensor_jobs():
    """Atualiza os jobs do scheduler baseado nos sensores ativos"""
    db = next(get_db())
    try:
        # Remover jobs de sensores que não existem mais ou não estão ativos
        active_sensors = db.query(Sensor).filter(Sensor.is_active == True).all()
        active_sensor_ids = {sensor.id for sensor in active_sensors}

        # Remover jobs de sensores inativos
        for job in scheduler.get_jobs():
            if job.id.startswith("sensor_"):
                sensor_id = int(job.id.split("_")[1])
                if sensor_id not in active_sensor_ids:
                    scheduler.remove_job(job.id)

        # Adicionar ou atualizar jobs para sensores ativos
        for sensor in active_sensors:
            job_id = f"sensor_{sensor.id}"
            if not scheduler.get_job(job_id):
                # Adicionar novo job
                scheduler.add_job(
                    simulate_single_sensor,
                    IntervalTrigger(seconds=sensor.simulation_interval),
                    args=[sensor.id],
                    id=job_id,
                    name=f"Simulação sensor {sensor.name}"
                )
            else:
                # Atualizar intervalo se mudou
                job = scheduler.get_job(job_id)
                if job.trigger.interval.seconds != sensor.simulation_interval:
                    scheduler.reschedule_job(
                        job_id,
                        trigger=IntervalTrigger(seconds=sensor.simulation_interval)
                    )
    finally:
        db.close()

# Função antiga mantida para compatibilidade, mas não usada
async def simulate_sensor_data(db: Session):
    pass

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

# Iniciar scheduler
scheduler.start()
