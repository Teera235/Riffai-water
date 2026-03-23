from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import Optional
import io

from app.models.database import get_db
from app.models.models import WaterLevel, Rainfall, Prediction, Alert, Station
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/daily")
async def daily_report(
    date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    target = datetime.fromisoformat(date) if date else datetime.utcnow()
    day_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)

    report = {
        "report_date": day_start.strftime("%Y-%m-%d"),
        "generated_at": datetime.utcnow().isoformat(),
        "basins": [],
    }

    for basin_id, config in settings.BASINS.items():
        # Water stats
        ws = (await db.execute(
            select(func.max(WaterLevel.level_m), func.avg(WaterLevel.level_m), func.min(WaterLevel.level_m))
            .join(Station, WaterLevel.station_id == Station.id)
            .where(and_(Station.basin_id == basin_id, WaterLevel.datetime.between(day_start, day_end)))
        )).first()

        # Rain total
        rain = await db.scalar(
            select(func.sum(Rainfall.amount_mm))
            .join(Station, Rainfall.station_id == Station.id)
            .where(and_(Station.basin_id == basin_id, Rainfall.datetime.between(day_start, day_end)))
        )

        # Latest prediction
        pred_row = (await db.execute(
            select(Prediction)
            .where(and_(Prediction.basin_id == basin_id, Prediction.predict_date.between(day_start, day_end)))
            .order_by(Prediction.predict_date.desc()).limit(1)
        )).scalar_one_or_none()

        # Alerts count
        alert_count = await db.scalar(
            select(func.count(Alert.id))
            .where(and_(Alert.basin_id == basin_id, Alert.created_at.between(day_start, day_end)))
        )

        report["basins"].append({
            "basin_id": basin_id,
            "name": config["name"],
            "provinces": config["provinces"],
            "risk_level": pred_row.risk_level.value if pred_row and pred_row.risk_level else "normal",
            "water_level": {
                "max_m": round(ws[0], 2) if ws and ws[0] else None,
                "avg_m": round(ws[1], 2) if ws and ws[1] else None,
                "min_m": round(ws[2], 2) if ws and ws[2] else None,
            },
            "rainfall_total_mm": round(rain, 1) if rain else 0,
            "prediction": {
                "flood_probability": pred_row.flood_probability if pred_row else None,
                "risk_level": pred_row.risk_level.value if pred_row and pred_row.risk_level else "normal",
                "affected_area_sqkm": pred_row.affected_area_sqkm if pred_row else None,
            },
            "alerts_today": alert_count or 0,
        })

    return report


@router.get("/generate-pdf")
async def generate_pdf(
    start_date: str,
    end_date: str = None,
    db: AsyncSession = Depends(get_db),
):
    report_data = await daily_report(date=start_date, db=db)

    from jinja2 import Template
    html_template = Template("""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: sans-serif; padding: 30px; font-size: 14px; }
        h1 { color: #1a56db; border-bottom: 2px solid #1a56db; padding-bottom: 8px; }
        table { width: 100%; border-collapse: collapse; margin: 16px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #1a56db; color: white; }
        .footer { margin-top: 30px; font-size: 11px; color: #999; text-align: center; }
    </style>
</head>
<body>
    <h1>🌊 RIFFAI - รายงานสถานการณ์น้ำ</h1>
    <p>📅 วันที่: {{ report_date }}</p>
    <p>🕐 สร้างเมื่อ: {{ generated_at }}</p>
    
    <table>
        <thead>
            <tr>
                <th>ลุ่มน้ำ</th>
                <th>ระดับน้ำสูงสุด (ม.)</th>
                <th>ระดับน้ำเฉลี่ย (ม.)</th>
                <th>ฝนรวม (มม.)</th>
                <th>AI ท่วม %</th>
                <th>ระดับเสี่ยง</th>
                <th>เตือนภัย</th>
            </tr>
        </thead>
        <tbody>
            {% for b in basins %}
            <tr>
                <td><strong>{{ b.name }}</strong><br><small>{{ b.provinces | join(', ') }}</small></td>
                <td>{{ b.water_level.max_m if b.water_level.max_m else '—' }}</td>
                <td>{{ b.water_level.avg_m if b.water_level.avg_m else '—' }}</td>
                <td>{{ b.rainfall_total_mm }}</td>
                <td>{{ '%0.1f' % (b.prediction.flood_probability * 100) if b.prediction.flood_probability else '—' }}%</td>
                <td>{{ b.prediction.risk_level }}</td>
                <td>{{ b.alerts_today }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="footer">
        RIFFAI Platform v1.0 • สนับสนุนโดยสำนักงานนวัตกรรมแห่งชาติ (NIA)<br>
        ร่วมมือกับสำนักงานทรัพยากรน้ำแห่งชาติ (สทนช.)
    </div>
</body>
</html>""")

    html = html_template.render(**report_data)

    # ส่งเป็น HTML (PDF ต้อง install weasyprint ซึ่งหนักมาก)
    return StreamingResponse(
        io.BytesIO(html.encode("utf-8")),
        media_type="text/html",
        headers={"Content-Disposition": f"inline; filename=riffai_report_{start_date}.html"},
    )
