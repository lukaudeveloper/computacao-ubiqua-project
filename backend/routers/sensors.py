from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Sensor, User
from auth import verify_token
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

class SensorCreate(BaseModel):
    name: str
    type: str
    location: str
    threshold_min: float | None = None
    threshold_max: float | None = None

@router.post("/sensors")
def create_sensor(sensor: SensorCreate, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    new_sensor = Sensor(**sensor.dict(), user_id=user.id)
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
