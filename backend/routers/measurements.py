from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Measurement, Sensor, User, Alert
from auth import verify_token
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

class MeasurementCreate(BaseModel):
    sensor_id: int
    value: float

@router.post("/measurements")
def create_measurement(measurement: MeasurementCreate, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    sensor = db.query(Sensor).filter(Sensor.id == measurement.sensor_id, Sensor.user_id == user.id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    new_measurement = Measurement(sensor_id=measurement.sensor_id, value=measurement.value)
    db.add(new_measurement)
    db.commit()
    db.refresh(new_measurement)
    # Verificar alertas
    check_alerts(sensor, measurement.value, db)
    return new_measurement

@router.get("/measurements")
def get_measurements(sensor_id: int | None = None, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    query = db.query(Measurement).join(Sensor).filter(Sensor.user_id == user.id)
    if sensor_id:
        query = query.filter(Measurement.sensor_id == sensor_id)
    measurements = query.all()
    return measurements

def check_alerts(sensor: Sensor, value: float, db: Session):
    if sensor.threshold_min and value < sensor.threshold_min:
        alert = Alert(sensor_id=sensor.id, message=f"Valor abaixo do mínimo: {value} < {sensor.threshold_min}")
        db.add(alert)
        db.commit()
    elif sensor.threshold_max and value > sensor.threshold_max:
        alert = Alert(sensor_id=sensor.id, message=f"Valor acima do máximo: {value} > {sensor.threshold_max}")
        db.add(alert)
        db.commit()
