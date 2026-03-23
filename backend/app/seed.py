"""
Seed database ด้วยข้อมูลตัวอย่าง สำหรับ dev/demo
รัน: docker exec -it riffai-backend python -m app.seed
"""

import asyncio
import random
from datetime import datetime, timedelta

from app.models.database import engine, Base, async_session
from app.models.models import (
    Basin, Station, WaterLevel, Rainfall,
    SatelliteImage, Prediction, Alert, User, RiskLevel
)
from app.core.security import hash_password


async def seed():
    # สร้าง tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # ═══════════════════════════════
        # 1. Basins (3 ลุ่มน้ำ)
        # ═══════════════════════════════
        from sqlalchemy import select
        existing = await db.scalar(select(Basin).limit(1))
        if existing:
            print("⚠️  Data already seeded, skipping...")
            return

        basins = [
            Basin(
                id="mekong_north",
                name="ลุ่มน้ำโขงเหนือ",
                name_en="Mekong North Basin",
                provinces=["เชียงใหม่", "เชียงราย", "พะเยา"],
                area_sqkm=28000,
                bbox=[98.0, 18.5, 101.5, 20.5],
            ),
            Basin(
                id="eastern_coast",
                name="ลุ่มน้ำชายฝั่งทะเลตะวันออก",
                name_en="Eastern Coastal Basin",
                provinces=["ชลบุรี", "ระยอง", "จันทบุรี", "ตราด"],
                area_sqkm=13830,
                bbox=[100.5, 11.5, 103.0, 13.5],
            ),
            Basin(
                id="southern_east",
                name="ลุ่มน้ำภาคใต้ฝั่งตะวันออกตอนล่าง",
                name_en="Southern East Lower Basin",
                provinces=["สงขลา", "ปัตตานี", "ยะลา", "นราธิวาส"],
                area_sqkm=11850,
                bbox=[100.0, 5.5, 102.0, 7.5],
            ),
        ]
        for b in basins:
            db.add(b)
        print("✅ 3 basins")

        # ═══════════════════════════════
        # 2. Stations (สถานีตรวจวัด)
        # ═══════════════════════════════
        stations_data = [
            # Mekong North
            ("WL001", "สถานีเชียงแสน", "water_level", 20.274, 100.083, "เชียงราย", "mekong_north"),
            ("WL002", "สถานีเชียงของ", "water_level", 20.261, 100.403, "เชียงราย", "mekong_north"),
            ("WL003", "สถานีแม่สาย", "water_level", 20.433, 99.886, "เชียงราย", "mekong_north"),
            ("WL004", "สถานีพะเยา", "water_level", 19.163, 99.902, "พะเยา", "mekong_north"),
            ("RF001", "สถานีฝนเชียงใหม่", "rainfall", 18.796, 98.984, "เชียงใหม่", "mekong_north"),
            ("RF002", "สถานีฝนเชียงราย", "rainfall", 19.912, 99.831, "เชียงราย", "mekong_north"),
            # Eastern Coast
            ("WL010", "สถานีบางปะกง", "water_level", 13.596, 100.993, "ชลบุรี", "eastern_coast"),
            ("WL011", "สถานีระยอง", "water_level", 12.681, 101.272, "ระยอง", "eastern_coast"),
            ("WL012", "สถานีจันทบุรี", "water_level", 12.611, 102.118, "จันทบุรี", "eastern_coast"),
            ("WL013", "สถานีตราด", "water_level", 12.243, 102.515, "ตราด", "eastern_coast"),
            ("RF010", "สถานีฝนชลบุรี", "rainfall", 13.362, 100.984, "ชลบุรี", "eastern_coast"),
            ("RF011", "สถานีฝนระยอง", "rainfall", 12.681, 101.272, "ระยอง", "eastern_coast"),
            # Southern East
            ("WL020", "สถานีหาดใหญ่", "water_level", 7.003, 100.474, "สงขลา", "southern_east"),
            ("WL021", "สถานีปัตตานี", "water_level", 6.869, 101.252, "ปัตตานี", "southern_east"),
            ("WL022", "สถานียะลา", "water_level", 6.541, 101.281, "ยะลา", "southern_east"),
            ("WL023", "สถานีนราธิวาส", "water_level", 6.432, 101.824, "นราธิวาส", "southern_east"),
            ("RF020", "สถานีฝนสงขลา", "rainfall", 7.190, 100.595, "สงขลา", "southern_east"),
            ("RF021", "สถานีฝนปัตตานี", "rainfall", 6.869, 101.252, "ปัตตานี", "southern_east"),
        ]

        for sid, name, stype, lat, lon, prov, bid in stations_data:
            db.add(Station(
                id=sid, name=name, station_type=stype,
                lat=lat, lon=lon, province=prov,
                basin_id=bid, source="mock", is_active=True,
            ))
        print(f"✅ {len(stations_data)} stations")

        # ═══════════════════════════════
        # 3. Historical Water Levels (90 วัน)
        # ═══════════════════════════════
        now = datetime.utcnow()
        wl_count = 0
        for sid, _, stype, *_ in stations_data:
            if stype != "water_level":
                continue
            for hours_ago in range(0, 90 * 24, 6):  # ทุก 6 ชม. 90 วัน
                dt = now - timedelta(hours=hours_ago)
                month = dt.month
                # Seasonal pattern: น้ำสูงช่วง ส.ค.-พ.ย.
                base = 2.5 if month in [8, 9, 10, 11] else 1.2
                level = base + random.gauss(0, 0.5)
                level = max(0.3, min(level, 5.5))

                db.add(WaterLevel(
                    station_id=sid,
                    datetime=dt,
                    level_m=round(level, 2),
                    flow_rate=round(level * 15 + random.uniform(-5, 5), 1),
                ))
                wl_count += 1
        print(f"✅ {wl_count} water level records")

        # ═══════════════════════════════
        # 4. Historical Rainfall (90 วัน)
        # ═══════════════════════════════
        rf_count = 0
        for sid, _, stype, *_ in stations_data:
            if stype != "rainfall":
                continue
            for hours_ago in range(0, 90 * 24, 3):  # ทุก 3 ชม.
                dt = now - timedelta(hours=hours_ago)
                month = dt.month
                base = 8.0 if month in [8, 9, 10, 11] else 2.0
                rain = max(0, base + random.gauss(0, 5))

                db.add(Rainfall(
                    station_id=sid,
                    datetime=dt,
                    amount_mm=round(rain, 1),
                ))
                rf_count += 1
        print(f"✅ {rf_count} rainfall records")

        # ═══════════════════════════════
        # 5. Satellite Images (ทุก 10 วัน 1 ปี)
        # ═══════════════════════════════
        sat_count = 0
        for basin in basins:
            for days_ago in range(0, 365, 10):
                dt = now - timedelta(days=days_ago)
                month = dt.month
                is_wet = month in [8, 9, 10, 11]

                ndvi = round(random.uniform(0.25, 0.45) if is_wet else random.uniform(0.4, 0.7), 4)
                ndwi = round(random.uniform(0.15, 0.45) if is_wet else random.uniform(-0.1, 0.15), 4)
                mndwi = round(ndwi - random.uniform(0.02, 0.08), 4)
                water_frac = 0.15 if is_wet else 0.05
                water_area = round((water_frac + random.uniform(-0.02, 0.03)) * basin.area_sqkm, 2)

                db.add(SatelliteImage(
                    source="sentinel-2",
                    acquisition_date=dt,
                    basin_id=basin.id,
                    cloud_coverage=round(random.uniform(5, 40), 1),
                    resolution_m=10,
                    avg_ndvi=ndvi,
                    avg_ndwi=ndwi,
                    avg_mndwi=mndwi,
                    water_area_sqkm=max(0, water_area),
                    rgb_path=f"mock://satellite/{basin.id}/rgb/{dt.strftime('%Y%m%d')}.tif",
                    ndvi_path=f"mock://satellite/{basin.id}/ndvi/{dt.strftime('%Y%m%d')}.tif",
                    ndwi_path=f"mock://satellite/{basin.id}/ndwi/{dt.strftime('%Y%m%d')}.tif",
                    mndwi_path=f"mock://satellite/{basin.id}/mndwi/{dt.strftime('%Y%m%d')}.tif",
                ))
                sat_count += 1
        print(f"✅ {sat_count} satellite images")

        # ═══════════════════════════════
        # 6. Predictions (30 วัน)
        # ═══════════════════════════════
        pred_count = 0
        for basin in basins:
            for days_ago in range(0, 30):
                dt = now - timedelta(days=days_ago)
                target = dt + timedelta(days=30)
                prob = round(random.uniform(0.1, 0.6), 4)

                risk = RiskLevel.NORMAL
                if prob > 0.7:
                    risk = RiskLevel.CRITICAL
                elif prob > 0.5:
                    risk = RiskLevel.WARNING
                elif prob > 0.3:
                    risk = RiskLevel.WATCH

                db.add(Prediction(
                    basin_id=basin.id,
                    predict_date=dt,
                    target_date=target,
                    flood_probability=prob,
                    risk_level=risk,
                    predicted_water_level=round(1.5 + prob * 3, 2),
                    affected_area_sqkm=round(prob * basin.area_sqkm * 0.05, 2),
                    confidence=round(random.uniform(0.6, 0.9), 4),
                    model_version="rule-based-v1",
                    model_accuracy=round(random.uniform(0.85, 0.97), 4),
                ))
                pred_count += 1
        print(f"✅ {pred_count} predictions")

        # ═══════════════════════════════
        # 7. Alerts (ตัวอย่าง)
        # ═══════════════════════════════
        sample_alerts = [
            Alert(
                basin_id="mekong_north",
                level=RiskLevel.WARNING,
                title="ระดับน้ำสูง - ลุ่มน้ำโขงเหนือ",
                message="สถานีเชียงแสน วัดระดับน้ำ 3.45 ม. เกินเกณฑ์เตือนภัย",
                trigger_type="water_level",
                trigger_value=3.45,
                threshold_value=3.0,
                is_active=True,
            ),
            Alert(
                basin_id="southern_east",
                level=RiskLevel.WATCH,
                title="ฝนตกหนัก - ลุ่มน้ำภาคใต้",
                message="สถานีฝนสงขลา วัดปริมาณฝน 85 มม. ใกล้เกณฑ์เตือน",
                trigger_type="rainfall",
                trigger_value=85.0,
                threshold_value=100.0,
                is_active=True,
            ),
            Alert(
                basin_id="eastern_coast",
                level=RiskLevel.NORMAL,
                title="AI พยากรณ์ - ชายฝั่งตะวันออก",
                message="ความน่าจะเป็นท่วมต่ำ 15% สถานการณ์ปกติ",
                trigger_type="ai_prediction",
                trigger_value=0.15,
                threshold_value=0.5,
                is_active=False,
                acknowledged=True,
            ),
        ]
        for a in sample_alerts:
            db.add(a)
        print(f"✅ {len(sample_alerts)} alerts")

        # ═══════════════════════════════
        # 8. Admin User
        # ═══════════════════════════════
        db.add(User(
            email="admin@riffai.org",
            name="RIFFAI Admin",
            password_hash=hash_password("admin123"),
            role="admin",
            organization="RIFFAI",
        ))
        db.add(User(
            email="onwr@riffai.org",
            name="เจ้าหน้าที่ สทนช.",
            password_hash=hash_password("onwr123"),
            role="editor",
            organization="สทนช.",
        ))
        print("✅ 2 users (admin@riffai.org / onwr@riffai.org)")

        await db.commit()
        print("\n🎉 Seed completed!")
        print("=" * 50)
        print(f"  Basins:           3")
        print(f"  Stations:         {len(stations_data)}")
        print(f"  Water Levels:     {wl_count}")
        print(f"  Rainfall:         {rf_count}")
        print(f"  Satellite Images: {sat_count}")
        print(f"  Predictions:      {pred_count}")
        print(f"  Alerts:           {len(sample_alerts)}")
        print(f"  Users:            2")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(seed())
