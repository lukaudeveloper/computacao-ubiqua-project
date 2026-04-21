from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Alert, Sensor, User
from auth import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

@router.get("/alerts")
def get_alerts(sensor_id: int | None = None, page: int = 1, limit: int = 20, token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token_data = verify_token(token.credentials)
    user = db.query(User).filter(User.username == token_data.username).first()
    query = db.query(Alert, Sensor.name.label("sensor_name"), Sensor.type.label("sensor_type"), Sensor.color.label("sensor_color"), Sensor.threshold_min.label("sensor_threshold_min"), Sensor.threshold_max.label("sensor_threshold_max"))
    query = query.join(Sensor).filter(Sensor.user_id == user.id)
    if sensor_id:
        query = query.filter(Alert.sensor_id == sensor_id)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    results = query.order_by(Alert.timestamp.desc()).offset(offset).limit(limit).all()

    alerts = []
    for alert, sensor_name, sensor_type, sensor_color, sensor_threshold_min, sensor_threshold_max in results:
        # Fallback para measurement_value null (alertas antigos)
        measurement_value = alert.measurement_value
        if measurement_value is None:
            measurement_value = alert.threshold_value

        alerts.append({
            "id": alert.id,
            "sensor_id": alert.sensor_id,
            "sensor_name": sensor_name,
            "sensor_type": sensor_type,
            "sensor_color": sensor_color,
            "sensor_threshold_min": sensor_threshold_min,
            "sensor_threshold_max": sensor_threshold_max,
            "message": alert.message,
            "threshold_value": alert.threshold_value,
            "measurement_value": measurement_value,
            "comparison": alert.comparison,
            "timestamp": alert.timestamp.isoformat(),
            "is_active": alert.is_active,
        })
    return {
        "alerts": alerts,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit,
        }
    }

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
