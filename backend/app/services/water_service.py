import httpx
import random
from datetime import datetime
from typing import List, Dict

from app.config import get_settings

settings = get_settings()

# ข้อมูลสถานีจริงในแต่ละลุ่มน้ำ
MOCK_STATIONS = {
    "mekong_north": [
        ("WL001", "สถานีเชียงแสน", "เชียงราย", 20.274, 100.083),
        ("WL002", "สถานีเชียงของ", "เชียงราย", 20.261, 100.403),
        ("WL003", "สถานีแม่สาย", "เชียงราย", 20.433, 99.886),
        ("WL004", "สถานีพะเยา", "พะเยา", 19.163, 99.902),
    ],
    "eastern_coast": [
        ("WL010", "สถานีบางปะกง", "ชลบุรี", 13.596, 100.993),
        ("WL011", "สถานีระยอง", "ระยอง", 12.681, 101.272),
        ("WL012", "สถานีจันทบุรี", "จันทบุรี", 12.611, 102.118),
        ("WL013", "สถานีตราด", "ตราด", 12.243, 102.515),
    ],
    "southern_east": [
        ("WL020", "สถานีหาดใหญ่", "สงขลา", 7.003, 100.474),
        ("WL021", "สถานีปัตตานี", "ปัตตานี", 6.869, 101.252),
        ("WL022", "สถานียะลา", "ยะลา", 6.541, 101.281),
        ("WL023", "สถานีนราธิวาส", "นราธิวาส", 6.432, 101.824),
    ],
}

MOCK_RAIN_STATIONS = {
    "mekong_north": [
        ("RF001", "สถานีฝนเชียงใหม่", "เชียงใหม่", 18.796, 98.984),
        ("RF002", "สถานีฝนเชียงราย", "เชียงราย", 19.912, 99.831),
    ],
    "eastern_coast": [
        ("RF010", "สถานีฝนชลบุรี", "ชลบุรี", 13.362, 100.984),
        ("RF011", "สถานีฝนระยอง", "ระยอง", 12.681, 101.272),
    ],
    "southern_east": [
        ("RF020", "สถานีฝนสงขลา", "สงขลา", 7.190, 100.595),
        ("RF021", "สถานีฝนปัตตานี", "ปัตตานี", 6.869, 101.252),
    ],
}


class WaterService:

    async def fetch_water_levels(self, basin_id: str) -> List[Dict]:
        """ลองดึง API จริงก่อน ไม่ได้ใช้ mock"""
        try:
            return await self._real_water_levels(basin_id)
        except Exception as e:
            print(f"⚠️ Real API failed ({e}), using mock")
            return self._mock_water_levels(basin_id)

    async def fetch_rainfall(self, basin_id: str) -> List[Dict]:
        try:
            return await self._real_rainfall(basin_id)
        except Exception as e:
            print(f"⚠️ Real API failed ({e}), using mock")
            return self._mock_rainfall(basin_id)

    # ─── Real API ───

    async def _real_water_levels(self, basin_id: str) -> List[Dict]:
        provinces = settings.BASINS[basin_id]["provinces"]
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{settings.THAIWATER_API_URL}/thaiwater/waterlevel",
                params={"province": ",".join(provinces)},
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for s in (data.get("data") or data if isinstance(data, list) else []):
                results.append({
                    "station_id": str(s.get("station_id", "")),
                    "station_name": s.get("station_name", ""),
                    "lat": s.get("lat", 0),
                    "lon": s.get("lon", 0),
                    "province": s.get("province", ""),
                    "water_level_m": s.get("water_level"),
                    "datetime": s.get("datetime", datetime.utcnow().isoformat()),
                    "source": "thaiwater",
                })
            return results

    async def _real_rainfall(self, basin_id: str) -> List[Dict]:
        if not settings.TMD_API_KEY:
            raise Exception("No TMD API key")
        bbox = settings.BASINS[basin_id]["bbox"]
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{settings.TMD_API_URL}/observation/rain/latest",
                headers={"Authorization": f"Bearer {settings.TMD_API_KEY}"},
                params={"min_lat": bbox[1], "max_lat": bbox[3], "min_lon": bbox[0], "max_lon": bbox[2]},
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for o in (data.get("observations") or data if isinstance(data, list) else []):
                results.append({
                    "station_id": str(o.get("station_id", "")),
                    "station_name": o.get("station_name", ""),
                    "lat": o.get("lat", 0),
                    "lon": o.get("lon", 0),
                    "province": o.get("province", ""),
                    "rainfall_mm": o.get("rain_24h", 0),
                    "datetime": o.get("datetime", datetime.utcnow().isoformat()),
                    "source": "tmd",
                })
            return results

    # ─── Mock Data ───

    def _mock_water_levels(self, basin_id: str) -> List[Dict]:
        month = datetime.utcnow().month
        is_wet = month in [6, 7, 8, 9, 10, 11]
        return [
            {
                "station_id": sid,
                "station_name": name,
                "lat": lat,
                "lon": lon,
                "province": prov,
                "water_level_m": round(
                    (2.8 if is_wet else 1.3) + random.gauss(0, 0.4), 2
                ),
                "datetime": datetime.utcnow().isoformat(),
                "source": "mock",
            }
            for sid, name, prov, lat, lon in MOCK_STATIONS.get(basin_id, [])
        ]

    def _mock_rainfall(self, basin_id: str) -> List[Dict]:
        month = datetime.utcnow().month
        is_wet = month in [6, 7, 8, 9, 10, 11]
        return [
            {
                "station_id": sid,
                "station_name": name,
                "lat": lat,
                "lon": lon,
                "province": prov,
                "rainfall_mm": round(max(0, (12 if is_wet else 3) + random.gauss(0, 8)), 1),
                "datetime": datetime.utcnow().isoformat(),
                "source": "mock",
            }
            for sid, name, prov, lat, lon in MOCK_RAIN_STATIONS.get(basin_id, [])
        ]
