from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Alert, Sensor, User
from auth import verify_token
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/alerts")
def get_alerts(sensor_id: int | None = None, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    query = db.query(Alert).join(Sensor).filter(Sensor.user_id == user.id)
    if sensor_id:
        query = query.filter(Alert.sensor_id == sensor_id)
    alerts = query.all()
    return alerts

@router.put("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    alert = db.query(Alert).join(Sensor).filter(Alert.id == alert_id, Sensor.user_id == user.id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_active = False
    db.commit()
    return {"message": "Alert resolved"}
