from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from app.models.database import get_db
from app.models.models import Alert, RiskLevel, User, WaterLevel, Station
from app.services.alert_service import AlertService
from app.core.security import get_optional_current_user
from app.config import get_settings

router = APIRouter()
alert_service = AlertService()
settings = get_settings()


def _alert_dict(a: Alert, *, include_active: bool = False) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "id": a.id,
        "basin_id": a.basin_id,
        "level": a.level.value,
        "title": a.title,
        "message": a.message,
        "trigger_type": a.trigger_type,
        "trigger_value": a.trigger_value,
        "threshold_value": a.threshold_value,
        "created_at": a.created_at.isoformat(),
        "acknowledged": a.acknowledged,
    }
    if include_active:
        d["is_active"] = a.is_active
    return d


@router.get("")
async def list_alerts_feed(
    days: int = Query(default=14, ge=1, le=365),
    limit: int = Query(default=100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    """Recent alerts for notification UI (e.g. navbar bell)."""
    since = datetime.utcnow() - timedelta(days=days)
    result = await db.scalars(
        select(Alert)
        .where(Alert.created_at >= since)
        .order_by(Alert.created_at.desc())
        .limit(limit)
    )
    return [_alert_dict(a, include_active=True) for a in result.all()]


@router.get("/active")
async def get_active_alerts(
    basin_id: Optional[str] = None,
    level: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Alert).where(Alert.is_active == True)

    if basin_id:
        query = query.where(Alert.basin_id == basin_id)
    if level:
        query = query.where(Alert.level == RiskLevel(level))

    query = query.order_by(Alert.created_at.desc())
    result = await db.scalars(query)

    alerts = []
    for a in result.all():
        alerts.append(_alert_dict(a))

    return {"count": len(alerts), "alerts": alerts}


@router.get("/history")
async def get_alerts_history(
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    result = await db.scalars(
        select(Alert)
        .where(Alert.created_at >= since)
        .order_by(Alert.created_at.desc())
    )
    alerts = [_alert_dict(a, include_active=True) for a in result.all()]
    return {"alerts": alerts}


@router.post("/check")
async def check_and_create_alerts(db: AsyncSession = Depends(get_db)):
    """ตรวจสอบเงื่อนไขแล้วสร้าง alert อัตโนมัติ"""

    created = []

    for basin_id, config in settings.BASINS.items():
        latest_water = await db.execute(
            select(WaterLevel.level_m, WaterLevel.datetime, Station.name)
            .join(Station, WaterLevel.station_id == Station.id)
            .where(Station.basin_id == basin_id)
            .order_by(WaterLevel.datetime.desc())
            .limit(1)
        )
        water_row = latest_water.first()

        if water_row and water_row[0]:
            level = water_row[0]
            risk = alert_service.evaluate_risk(water_level=level)

            if risk in (RiskLevel.WARNING, RiskLevel.CRITICAL):
                existing = await db.scalar(
                    select(Alert).where(and_(
                        Alert.basin_id == basin_id,
                        Alert.is_active == True,
                        Alert.trigger_type == "water_level",
                    ))
                )

                if not existing:
                    alert = Alert(
                        basin_id=basin_id,
                        level=risk,
                        title=f"ระดับน้ำสูง - {config['name']}",
                        message=f"สถานี {water_row[2]} วัดระดับน้ำ {level:.2f} ม. เกินเกณฑ์เตือนภัย",
                        trigger_type="water_level",
                        trigger_value=level,
                        threshold_value=settings.ALERT_WATER_LEVEL_WARNING,
                    )
                    db.add(alert)
                    created.append({
                        "basin": basin_id,
                        "type": "water_level",
                        "level": risk.value,
                        "value": level,
                    })

                    await alert_service.publish_alert({
                        "basin_id": basin_id,
                        "basin_name": config["name"],
                        "level": risk.value,
                        "type": "water_level",
                        "value": level,
                        "station": water_row[2],
                        "timestamp": datetime.utcnow().isoformat(),
                    })

    await db.commit()

    return {"alerts_created": len(created), "details": created}


async def _mark_acknowledged(
    alert_id: int,
    user: Optional[User],
    db: AsyncSession,
) -> Alert:
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.acknowledged = True
    alert.acknowledged_at = datetime.utcnow()
    alert.acknowledged_by = user.id if user else None
    await db.commit()
    await db.refresh(alert)
    return alert


@router.post("/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _mark_acknowledged(alert_id, user, db)
    return {"status": "read", "alert_id": alert_id}


@router.put("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _mark_acknowledged(alert_id, user, db)
    return {"status": "acknowledged", "alert_id": alert_id}


@router.put("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
):
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.is_active = False
    await db.commit()
    return {"status": "resolved", "alert_id": alert_id}


@router.delete("/{alert_id}")
async def dismiss_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
):
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.is_active = False
    await db.commit()
    return {"status": "dismissed", "alert_id": alert_id}
