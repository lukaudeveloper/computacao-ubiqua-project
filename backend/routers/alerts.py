from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Alert, Sensor, User
from auth import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

@router.get("/alerts")
def get_alerts(sensor_id: int | None = None, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    query = db.query(Alert, Sensor.name.label("sensor_name"), Sensor.type.label("sensor_type"), Sensor.color.label("sensor_color"))
    query = query.join(Sensor).filter(Sensor.user_id == user.id)
    if sensor_id:
        query = query.filter(Alert.sensor_id == sensor_id)
    results = query.order_by(Alert.timestamp.desc()).all()
    alerts = []
    for alert, sensor_name, sensor_type, sensor_color in results:
        alerts.append({
            "id": alert.id,
            "sensor_id": alert.sensor_id,
            "sensor_name": sensor_name,
            "sensor_type": sensor_type,
            "sensor_color": sensor_color,
            "message": alert.message,
            "threshold_value": alert.threshold_value,
            "measurement_value": alert.measurement_value,
            "comparison": alert.comparison,
            "timestamp": alert.timestamp.isoformat(),
            "is_active": alert.is_active,
        })
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
