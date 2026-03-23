"""
Batch prediction endpoint for scheduled jobs
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import List

from app.models.database import get_db
from app.models.models import Prediction, Basin
from app.services.ai_service import AIService
from app.services.alert_service import AlertService
from app.config import get_settings

router = APIRouter()
settings = get_settings()
ai_service = AIService()
alert_service = AlertService()


@router.post("/batch")
async def batch_predictions(
    basins: List[str] = None,
    days_ahead: int = 30,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Run predictions for multiple basins
    Used by Cloud Scheduler for daily automated predictions
    """
    
    # Default to all basins
    if not basins:
        basins = list(settings.BASINS.keys())
    
    # Validate basins
    valid_basins = []
    for basin_id in basins:
        basin = await db.get(Basin, basin_id)
        if basin:
            valid_basins.append(basin_id)
    
    if not valid_basins:
        return {
            "status": "error",
            "message": "No valid basins found"
        }
    
    # Run predictions in background
    if background_tasks:
        background_tasks.add_task(
            _run_batch_predictions,
            valid_basins,
            days_ahead,
            db
        )
        
        return {
            "status": "started",
            "basins": valid_basins,
            "days_ahead": days_ahead,
            "message": f"Batch predictions started for {len(valid_basins)} basins"
        }
    else:
        # Run synchronously
        results = await _run_batch_predictions(valid_basins, days_ahead, db)
        return results


async def _run_batch_predictions(basins: List[str], days_ahead: int, db: AsyncSession):
    """Background task to run predictions"""
    
    results = []
    now = datetime.utcnow()
    lookback = now - timedelta(days=90)
    
    for basin_id in basins:
        try:
            # Get input data
            from app.models.models import SatelliteImage, WaterLevel, Rainfall, Station
            
            sat_data = (await db.execute(
                select(
                    SatelliteImage.acquisition_date,
                    SatelliteImage.avg_ndvi,
                    SatelliteImage.avg_ndwi,
                    SatelliteImage.avg_mndwi,
                    SatelliteImage.water_area_sqkm
                )
                .where(
                    SatelliteImage.basin_id == basin_id,
                    SatelliteImage.acquisition_date >= lookback
                )
                .order_by(SatelliteImage.acquisition_date)
            )).all()
            
            water_data = (await db.execute(
                select(WaterLevel.datetime, WaterLevel.level_m)
                .join(Station, WaterLevel.station_id == Station.id)
                .where(
                    Station.basin_id == basin_id,
                    WaterLevel.datetime >= lookback
                )
                .order_by(WaterLevel.datetime)
            )).all()
            
            rain_data = (await db.execute(
                select(Rainfall.datetime, Rainfall.amount_mm)
                .join(Station, Rainfall.station_id == Station.id)
                .where(
                    Station.basin_id == basin_id,
                    Rainfall.datetime >= lookback
                )
                .order_by(Rainfall.datetime)
            )).all()
            
            # Run prediction
            result = ai_service.predict(
                basin_id=basin_id,
                satellite_data=sat_data,
                water_data=water_data,
                rainfall_data=rain_data,
                days_ahead=days_ahead,
            )
            
            # Evaluate risk
            risk = alert_service.evaluate_risk(
                flood_probability=result["flood_probability"],
                water_level=result.get("predicted_water_level"),
            )
            
            # Save prediction
            target_date = now + timedelta(days=days_ahead)
            pred = Prediction(
                basin_id=basin_id,
                predict_date=now,
                target_date=target_date,
                flood_probability=result["flood_probability"],
                risk_level=risk,
                predicted_water_level=result.get("predicted_water_level"),
                affected_area_sqkm=result.get("affected_area_sqkm"),
                confidence=result.get("confidence", 0),
                model_version=result.get("model_version", "rule-based-v1"),
                model_accuracy=result.get("model_accuracy"),
            )
            db.add(pred)
            
            results.append({
                "basin_id": basin_id,
                "status": "success",
                "flood_probability": result["flood_probability"],
                "risk_level": risk.value
            })
            
        except Exception as e:
            results.append({
                "basin_id": basin_id,
                "status": "error",
                "error": str(e)
            })
    
    await db.commit()
    
    print(f"✅ Batch predictions completed: {len(results)} basins")
    
    return {
        "status": "completed",
        "timestamp": now.isoformat(),
        "basins_processed": len(results),
        "results": results
    }
