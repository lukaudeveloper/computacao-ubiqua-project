from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Sensor, User, Measurement
from auth import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers.measurements import check_alerts
from random import uniform

router = APIRouter()
security = HTTPBearer()

class SensorCreate(BaseModel):
    name: str
    type: str
    location: str
    threshold_min: float | None = None
    threshold_max: float | None = None
    color: str = "#007bff"

class SensorActivate(BaseModel):
    is_active: bool

@router.post("/sensors")
def create_sensor(sensor: SensorCreate, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    data = sensor.dict()
    new_sensor = Sensor(**data, user_id=user.id, is_active=False)
    db.add(new_sensor)
    db.commit()
    db.refresh(new_sensor)
    return new_sensor

@router.get("/sensors")
def get_sensors(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    sensors = db.query(Sensor).filter(Sensor.user_id == user.id).all()
    return sensors

@router.put("/sensors/{sensor_id}")
def update_sensor(sensor_id: int, sensor: SensorCreate, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id, Sensor.user_id == user.id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    for key, value in sensor.dict().items():
        setattr(db_sensor, key, value)
    db.commit()
    return db_sensor

@router.post("/sensors/{sensor_id}/activate")
def activate_sensor(sensor_id: int, payload: SensorActivate, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id, Sensor.user_id == user.id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    db_sensor.is_active = payload.is_active
    db.commit()
    return {"id": db_sensor.id, "is_active": db_sensor.is_active}

@router.post("/sensors/{sensor_id}/simulate")
def simulate_sensor(sensor_id: int, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id, Sensor.user_id == user.id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    if not sensor.is_active:
        raise HTTPException(status_code=400, detail="Sensor must be active to collect data")

    value = simulate_value(sensor)
    new_measurement = Measurement(sensor_id=sensor.id, value=value)
    db.add(new_measurement)
    db.commit()
    db.refresh(new_measurement)
    check_alerts(sensor, value, db)
    return {
        "sensor_id": sensor.id,
        "value": value,
        "timestamp": new_measurement.timestamp,
    }

@router.delete("/sensors/{sensor_id}")
def delete_sensor(sensor_id: int, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id, Sensor.user_id == user.id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    db.delete(db_sensor)
    db.commit()
    return {"message": "Sensor deleted"}


def simulate_value(sensor: Sensor) -> float:
    if sensor.threshold_min is not None and sensor.threshold_max is not None and sensor.threshold_min < sensor.threshold_max:
        return round(uniform(sensor.threshold_min, sensor.threshold_max), 2)

    sensor_type = sensor.type.lower()
    if "temperature" in sensor_type:
        return round(uniform(15.0, 30.0), 2)
    if "humidity" in sensor_type:
        return round(uniform(30.0, 80.0), 2)
    if "air" in sensor_type or "quality" in sensor_type:
        return round(uniform(0.0, 150.0), 2)
    if "noise" in sensor_type:
        return round(uniform(20.0, 90.0), 2)
    return round(uniform(10.0, 100.0), 2)
