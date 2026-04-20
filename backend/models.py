from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))  # e.g., temperature, humidity, air_quality, noise
    location = Column(String(100))
    threshold_min = Column(Float, nullable=True)
    threshold_max = Column(Float, nullable=True)
    color = Column(String(20), default="#007bff")
    is_active = Column(Boolean, default=False)
    simulation_interval = Column(Integer, default=30)  # Intervalo em segundos (padrão 30s)
    user_id = Column(Integer, ForeignKey("users.id"))

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sensor = relationship("Sensor")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    message = Column(String(255))
    threshold_value = Column(Float, nullable=True)
    measurement_value = Column(Float, nullable=True)
    comparison = Column(String(1), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    sensor = relationship("Sensor")
