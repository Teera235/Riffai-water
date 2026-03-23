from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import os

from app.models.database import Base

# ตรวจสอบว่าใช้ SQLite หรือไม่
USE_SQLITE = "sqlite" in os.getenv("DATABASE_URL", "sqlite")

if not USE_SQLITE:
    from geoalchemy2 import Geometry


class RiskLevel(str, enum.Enum):
    NORMAL = "normal"
    WATCH = "watch"
    WARNING = "warning"
    CRITICAL = "critical"


class Basin(Base):
    __tablename__ = "basins"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    name_en = Column(String(200))
    provinces = Column(JSON)
    area_sqkm = Column(Float)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326)) if not USE_SQLITE else Column(Text)
    bbox = Column(JSON)
    
    stations = relationship("Station", back_populates="basin")
    predictions = relationship("Prediction", back_populates="basin")
    alerts = relationship("Alert", back_populates="basin")


class Station(Base):
    __tablename__ = "stations"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    station_type = Column(String(50))
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    province = Column(String(100))
    basin_id = Column(String(50), ForeignKey("basins.id"))
    source = Column(String(100))
    is_active = Column(Boolean, default=True)
    geometry = Column(Geometry("POINT", srid=4326)) if not USE_SQLITE else Column(Text)
    
    basin = relationship("Basin", back_populates="stations")
    water_levels = relationship("WaterLevel", back_populates="station")
    rainfall_records = relationship("Rainfall", back_populates="station")


class WaterLevel(Base):
    __tablename__ = "water_levels"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String(50), ForeignKey("stations.id"), nullable=False)
    datetime = Column(DateTime, nullable=False, index=True)
    level_m = Column(Float)
    flow_rate = Column(Float)
    
    station = relationship("Station", back_populates="water_levels")


class Rainfall(Base):
    __tablename__ = "rainfall"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String(50), ForeignKey("stations.id"), nullable=False)
    datetime = Column(DateTime, nullable=False, index=True)
    amount_mm = Column(Float)
    accumulated_mm = Column(Float)
    
    station = relationship("Station", back_populates="rainfall_records")


class SatelliteImage(Base):
    __tablename__ = "satellite_images"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    acquisition_date = Column(DateTime, nullable=False, index=True)
    basin_id = Column(String(50), ForeignKey("basins.id"))
    cloud_coverage = Column(Float)
    resolution_m = Column(Float)
    
    raw_path = Column(String(500))
    ndvi_path = Column(String(500))
    ndwi_path = Column(String(500))
    mndwi_path = Column(String(500))
    rgb_path = Column(String(500))
    
    # Optical indices (Sentinel-2)
    avg_ndvi = Column(Float)
    avg_ndwi = Column(Float)
    avg_mndwi = Column(Float)
    avg_lswi = Column(Float)  # Land Surface Water Index
    avg_ndbi = Column(Float)  # Normalized Difference Built-up Index
    
    # SAR features (Sentinel-1)
    sar_vv_db = Column(Float)  # VV polarization (dB)
    sar_vh_db = Column(Float)  # VH polarization (dB)
    sar_ratio = Column(Float)  # VV/VH ratio
    change_detected = Column(Boolean, default=False)  # Change detection flag
    change_area_sqkm = Column(Float)  # Area of detected change
    
    water_area_sqkm = Column(Float)
    
    geometry = Column(Geometry("POLYGON", srid=4326)) if not USE_SQLITE else Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    basin_id = Column(String(50), ForeignKey("basins.id"), nullable=False)
    predict_date = Column(DateTime, nullable=False)
    target_date = Column(DateTime, nullable=False)
    
    flood_probability = Column(Float)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.NORMAL)
    predicted_water_level = Column(Float)
    affected_area_sqkm = Column(Float)
    confidence = Column(Float)
    
    model_version = Column(String(50))
    model_accuracy = Column(Float)
    prediction_map_path = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    basin = relationship("Basin", back_populates="predictions")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    basin_id = Column(String(50), ForeignKey("basins.id"), nullable=False)
    level = Column(Enum(RiskLevel), nullable=False)
    title = Column(String(300), nullable=False)
    message = Column(Text)
    trigger_type = Column(String(50))
    trigger_value = Column(Float)
    threshold_value = Column(Float)
    
    is_active = Column(Boolean, default=True)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    basin = relationship("Basin", back_populates="alerts")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    password_hash = Column(String(500), nullable=False)
    role = Column(String(50), default="viewer")
    organization = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
