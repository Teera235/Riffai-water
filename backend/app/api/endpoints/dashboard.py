from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import Optional

from app.models.database import get_db
from app.models.models import (
    Basin, WaterLevel, Rainfall, Prediction, Alert,
    SatelliteImage, RiskLevel, Station
)
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/summary")
async def get_dashboard_summary(
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    """Aggregates for analytics: mean water level and total rainfall over the window."""
    now = datetime.utcnow()
    since = now - timedelta(days=days)

    avg_wl = await db.scalar(
        select(func.avg(WaterLevel.level_m)).where(
            and_(
                WaterLevel.datetime >= since,
                WaterLevel.datetime <= now,
                WaterLevel.level_m.isnot(None),
            )
        )
    )
    total_rain = await db.scalar(
        select(func.sum(Rainfall.amount_mm)).where(
            and_(Rainfall.datetime >= since, Rainfall.datetime <= now)
        )
    )

    return {
        "period_days": days,
        "avgWaterLevel": float(avg_wl) if avg_wl is not None else 0.0,
        "totalRainfall": float(total_rain) if total_rain is not None else 0.0,
    }


@router.get("/overview")
async def get_overview(db: AsyncSession = Depends(get_db)):
    """ภาพรวมทั้ง 3 ลุ่มน้ำ"""
    
    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # จำนวนเตือนภัย Active
    active_alerts = await db.scalar(
        select(func.count(Alert.id)).where(Alert.is_active == True)
    )
    
    # ข้อมูลแต่ละลุ่มน้ำ
    basins_data = []
    basins = await db.scalars(select(Basin))
    
    for basin in basins:
        # ระดับน้ำล่าสุด
        latest_water = await db.scalar(
            select(WaterLevel.level_m)
            .join(Station)
            .where(Station.basin_id == basin.id)
            .order_by(WaterLevel.datetime.desc())
            .limit(1)
        )
        
        # ฝนวันนี้
        today_rain = await db.scalar(
            select(func.sum(Rainfall.amount_mm))
            .join(Station)
            .where(
                and_(
                    Station.basin_id == basin.id,
                    Rainfall.datetime >= today
                )
            )
        )
        
        # AI prediction ล่าสุด
        latest_prediction = await db.execute(
            select(Prediction)
            .where(Prediction.basin_id == basin.id)
            .order_by(Prediction.created_at.desc())
            .limit(1)
        )
        pred = latest_prediction.scalar_one_or_none()
        
        # สถานะลุ่มน้ำ
        risk = RiskLevel.NORMAL
        if latest_water and latest_water > settings.ALERT_WATER_LEVEL_CRITICAL:
            risk = RiskLevel.CRITICAL
        elif latest_water and latest_water > settings.ALERT_WATER_LEVEL_WARNING:
            risk = RiskLevel.WARNING
        elif pred and pred.flood_probability > 0.5:
            risk = RiskLevel.WATCH
        
        basins_data.append({
            "id": basin.id,
            "name": basin.name,
            "provinces": basin.provinces,
            "current_water_level": latest_water,
            "today_rainfall_mm": today_rain or 0,
            "risk_level": risk.value,
            "prediction": {
                "flood_probability": pred.flood_probability if pred else None,
                "target_date": pred.target_date.isoformat() if pred else None,
                "affected_area_sqkm": pred.affected_area_sqkm if pred else None,
            } if pred else None,
        })
    
    # AI Model accuracy ล่าสุด
    latest_accuracy = await db.scalar(
        select(Prediction.model_accuracy)
        .order_by(Prediction.created_at.desc())
        .limit(1)
    )
    
    return {
        "timestamp": now.isoformat(),
        "active_alerts": active_alerts,
        "model_accuracy": latest_accuracy,
        "basins": basins_data,
        "summary": {
            "total_basins": len(basins_data),
            "critical_count": sum(1 for b in basins_data if b["risk_level"] == "critical"),
            "warning_count": sum(1 for b in basins_data if b["risk_level"] == "warning"),
        }
    }


@router.get("/stats/{basin_id}")
async def get_basin_stats(
    basin_id: str,
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """สถิติรายละเอียดของลุ่มน้ำ"""
    
    since = datetime.utcnow() - timedelta(days=days)
    
    # ระดับน้ำย้อนหลัง
    water_levels = await db.execute(
        select(WaterLevel.datetime, WaterLevel.level_m)
        .join(Station)
        .where(
            and_(
                Station.basin_id == basin_id,
                WaterLevel.datetime >= since
            )
        )
        .order_by(WaterLevel.datetime)
    )
    
    # ปริมาณฝนย้อนหลัง
    rainfall = await db.execute(
        select(Rainfall.datetime, Rainfall.amount_mm)
        .join(Station)
        .where(
            and_(
                Station.basin_id == basin_id,
                Rainfall.datetime >= since
            )
        )
        .order_by(Rainfall.datetime)
    )
    
    # NDVI/NDWI trend
    satellite = await db.execute(
        select(
            SatelliteImage.acquisition_date,
            SatelliteImage.avg_ndvi,
            SatelliteImage.avg_ndwi,
            SatelliteImage.avg_mndwi,
            SatelliteImage.water_area_sqkm
        )
        .where(
            and_(
                SatelliteImage.basin_id == basin_id,
                SatelliteImage.acquisition_date >= since
            )
        )
        .order_by(SatelliteImage.acquisition_date)
    )
    
    return {
        "basin_id": basin_id,
        "period_days": days,
        "water_levels": [
            {"datetime": r[0].isoformat(), "level_m": r[1]}
            for r in water_levels
        ],
        "rainfall": [
            {"datetime": r[0].isoformat(), "amount_mm": r[1]}
            for r in rainfall
        ],
        "satellite_indices": [
            {
                "date": r[0].isoformat(),
                "ndvi": r[1], "ndwi": r[2], "mndwi": r[3],
                "water_area_sqkm": r[4]
            }
            for r in satellite
        ],
    }
