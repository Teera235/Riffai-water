# 📊 RIFFAI Platform - Data Status Report

## 🔍 Overview

สรุปสถานะข้อมูลในระบบ แยกเป็น **ข้อมูลจริง** vs **Mock Data**

---

## ✅ ข้อมูลจริง (Real Data)

### 1. Static Geographic Data
**Status:** ✅ Real Data

**Files:**
- `backend/app/data/rivers.py` - ข้อมูลแม่น้ำ 7 สาย
- `backend/app/data/dams.py` - ข้อมูลเขื่อน 8 แห่ง

**Details:**
- แม่น้ำ: เจ้าพระยา, โขง, ชี, มูล, ปิง, น่าน, ยม
- เขื่อน: ภูมิพล, สิริกิติ์, แควน้อยบำรุงแดน, ศรีนครินทร์, ฯลฯ
- มี coordinates, ความยาว, ความจุ, ปีที่สร้าง

**API Endpoints:**
- `GET /api/map/rivers` ✅
- `GET /api/map/dams` ✅

---

## ⚠️ Mock Data (Simulated)

### 1. Grid Tiles (Heatmap)
**Status:** ⚠️ Mock Data

**File:** `backend/app/data/grid_tiles.py`

**Mock Data:**
```python
avg_water_level = random.uniform(2.5, 5.0)
rainfall_24h = random.uniform(0, 180)
station_count = random.randint(0, 5)
population_at_risk = random.randint(0, 50000)
```

**API Endpoints:**
- `GET /api/map/tiles` ⚠️ Mock
- `GET /api/map/tiles/summary` ⚠️ Mock
- `GET /api/map/tiles/{tile_id}` ⚠️ Mock
- `GET /api/map/tiles/{tile_id}/history` ⚠️ Mock

**To Fix:**
- Query real water level data from database
- Calculate actual rainfall from stations
- Count real stations in each tile
- Calculate population from census data

---

### 2. Satellite Data (Earth Engine)
**Status:** ⚠️ Mock Data (Earth Engine authenticated but using mock)

**File:** `backend/app/services/earth_engine_service.py`

**Mock Data:**
```python
# Sentinel-2 (Optical)
ndvi = round(random.uniform(0.25, 0.45), 4)
ndwi = round(random.uniform(0.15, 0.40), 4)
mndwi = round(random.uniform(0.10, 0.35), 4)

# Sentinel-1 (SAR)
vv_mean = round(random.uniform(-18, -12), 2)
vh_mean = round(random.uniform(-24, -18), 2)
```

**API Endpoints:**
- `POST /api/pipeline/fetch-satellite` ⚠️ Mock
- `GET /api/data/satellite-indices/{basin_id}` ⚠️ Mock

**Why Mock:**
- Earth Engine API calls are slow (5-10 seconds)
- Quota limits (1000 requests/day)
- Need proper authentication setup

**To Fix:**
- Use real Earth Engine API calls
- Implement caching (Redis)
- Schedule batch updates (daily)
- Store results in database

---

### 3. Water Level & Rainfall
**Status:** ✅ Real Data (from seed) / ⚠️ Mock (live updates)

**File:** `backend/app/seed.py`

**Seed Data (Historical):**
```python
# Seasonal pattern
base = 2.5 if month in [8, 9, 10, 11] else 1.2
level = base + random.gauss(0, 0.5)
```

**Database Tables:**
- `water_levels` - มีข้อมูล 90 วันย้อนหลัง
- `rainfall` - มีข้อมูล 90 วันย้อนหลัง
- `satellite_images` - มีข้อมูล 90 วันย้อนหลัง

**API Endpoints:**
- `GET /api/map/water-level-map` ✅ Real (from DB)
- `GET /api/data/water-level/{basin_id}` ✅ Real (from DB)
- `GET /api/data/rainfall/{basin_id}` ✅ Real (from DB)

**To Fix:**
- Connect to real data sources:
  - กรมชลประทาน API
  - กรมอุตุนิยมวิทยา API
  - Hydro-Informatics Institute API

---

### 4. AI Predictions
**Status:** ⚠️ Rule-based (not real AI)

**File:** `backend/app/services/ai_service.py`

**Current Implementation:**
```python
# Rule-based prediction
if avg_water_level > 4.0:
    flood_probability = 0.8
elif avg_water_level > 3.5:
    flood_probability = 0.5
else:
    flood_probability = 0.2
```

**AI Models:**
- 3 models copied from HydroLSTM
- TensorFlow version mismatch
- Not actually used (fallback to rules)

**API Endpoints:**
- `POST /api/predict/flood` ⚠️ Rule-based
- `GET /api/predict/history/{basin_id}` ✅ Real (from DB)
- `GET /api/predict/accuracy` ⚠️ Mock

**To Fix:**
- Retrain models with TensorFlow 2.x
- Use real models for predictions
- Implement proper feature engineering
- Add model versioning

---

### 5. Alerts
**Status:** ✅ Real Logic / ⚠️ Mock Thresholds

**File:** `backend/app/services/alert_service.py`

**Thresholds (Hardcoded):**
```python
ALERT_WATER_LEVEL_WARNING = 4.0  # meters
ALERT_WATER_LEVEL_CRITICAL = 4.5  # meters
ALERT_RAINFALL_WARNING = 100  # mm/24h
ALERT_RAINFALL_CRITICAL = 150  # mm/24h
```

**API Endpoints:**
- `GET /api/alerts/active` ✅ Real (from DB)
- `POST /api/alerts/check` ✅ Real logic
- `GET /api/alerts/history` ✅ Real (from DB)

**To Fix:**
- Use dynamic thresholds per station
- Consider historical patterns
- Add AI-based anomaly detection

---

## 📊 Summary Table

| Component | Status | Data Source | Production Ready |
|-----------|--------|-------------|------------------|
| Rivers | ✅ Real | Static file | ✅ Yes |
| Dams | ✅ Real | Static file | ✅ Yes |
| Basins | ✅ Real | Database | ✅ Yes |
| Stations | ✅ Real | Database | ✅ Yes |
| Water Levels | ✅ Real | Database (seeded) | ⚠️ Need live API |
| Rainfall | ✅ Real | Database (seeded) | ⚠️ Need live API |
| Grid Tiles | ⚠️ Mock | Random | ❌ No |
| Satellite (Sentinel-2) | ⚠️ Mock | Random | ❌ No |
| Satellite (Sentinel-1) | ⚠️ Mock | Random | ❌ No |
| AI Predictions | ⚠️ Rules | Rule-based | ⚠️ Basic |
| Alerts | ✅ Real | Database + Logic | ✅ Yes |
| Dashboard Stats | ✅ Real | Database | ✅ Yes |

---

## 🎯 Priority Fixes for Production

### High Priority (ต้องแก้ก่อน deploy)

1. **Grid Tiles** - ใช้ข้อมูลจริงจาก database
   ```python
   # แทนที่ random ด้วย query จริง
   avg_water_level = await get_avg_water_level_in_tile(lat, lon)
   rainfall_24h = await get_rainfall_in_tile(lat, lon)
   ```

2. **Satellite Data** - ใช้ Earth Engine จริง หรือ cache ข้อมูล
   ```python
   # Option 1: Use real EE API (slow)
   # Option 2: Pre-compute and cache daily
   # Option 3: Use mock but label clearly
   ```

### Medium Priority (ปรับปรุงภายหลัง)

3. **Live Data Integration**
   - Connect to กรมชลประทาน API
   - Connect to กรมอุตุนิยมวิทยา API
   - Schedule hourly updates

4. **AI Models**
   - Retrain with TensorFlow 2.x
   - Deploy models properly
   - Add model monitoring

### Low Priority (Nice to have)

5. **Advanced Features**
   - Real-time streaming data
   - WebSocket updates
   - Advanced analytics

---

## 🔧 Quick Fixes

### Fix 1: Grid Tiles - Use Real Data

**File:** `backend/app/data/grid_tiles.py`

```python
async def generate_thailand_tiles_real(db: AsyncSession) -> List[Dict[str, Any]]:
    """Generate tiles with real data from database"""
    tiles = []
    
    for lat in range(...):
        for lon in range(...):
            # Query real data
            water_levels = await db.execute(
                select(WaterLevel)
                .join(Station)
                .where(
                    Station.lat.between(lat, lat + TILE_SIZE),
                    Station.lon.between(lon, lon + TILE_SIZE)
                )
            )
            
            # Calculate real averages
            avg_water_level = calculate_average(water_levels)
            # ... rest of logic
```

### Fix 2: Satellite Data - Add Caching

**File:** `backend/app/services/earth_engine_service.py`

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_satellite_data_cached(basin_id: str, date: str):
    """Cache satellite data for 24 hours"""
    # Check if data is fresh (< 24 hours old)
    # If yes, return cached
    # If no, fetch new from EE
    pass
```

### Fix 3: Label Mock Data Clearly

**All Mock Endpoints:**

```python
@router.get("/tiles")
async def get_tiles():
    """Get tiles (⚠️ MOCK DATA - for demo only)"""
    tiles = generate_thailand_tiles()
    return {
        "type": "FeatureCollection",
        "features": tiles,
        "meta": {
            "data_source": "mock",
            "warning": "This is simulated data for demonstration purposes"
        }
    }
```

---

## 📝 Recommendations

### For Demo/Testing:
- ✅ Current setup is OK
- Mock data looks realistic
- All features work

### For Production:
1. **Must Fix:**
   - Grid tiles → use real data
   - Add "DEMO MODE" banner
   - Document data sources

2. **Should Fix:**
   - Satellite data → use cache
   - AI models → retrain
   - Live data → integrate APIs

3. **Nice to Have:**
   - Real-time updates
   - Historical data archive
   - Advanced analytics

---

## 🚀 Deployment Strategy

### Option 1: Deploy with Mock (Quick)
- ✅ Deploy now
- ⚠️ Add "DEMO MODE" label
- 📝 Document limitations
- 🔄 Update later with real data

### Option 2: Fix Critical Issues First (Recommended)
- 🔧 Fix grid tiles (2-3 hours)
- 🔧 Add data source labels (30 min)
- 🔧 Update documentation (30 min)
- ✅ Then deploy

### Option 3: Full Production Ready (Long-term)
- 🔧 Integrate all real APIs (1-2 weeks)
- 🔧 Retrain AI models (1 week)
- 🔧 Add monitoring (3-5 days)
- 🔧 Load testing (2-3 days)
- ✅ Then deploy

---

## 💡 Recommendation

**สำหรับตอนนี้:** Deploy แบบ Option 1 (with mock) แต่:
1. เพิ่ม banner "DEMO MODE" บนหน้าเว็บ
2. ระบุชัดเจนว่าข้อมูลไหนเป็น mock
3. วางแผนอัพเดทข้อมูลจริงภายหลัง

**ข้อดี:**
- Deploy ได้ทันที
- ทุก feature ทำงาน
- ดูสวยงาม professional

**ข้อเสีย:**
- ข้อมูลบางส่วนไม่ใช่ real-time
- ต้องระบุว่าเป็น demo

---

**สรุป:** ระบบพร้อม deploy แต่ควรระบุว่าบางส่วนเป็น demo data 🚀
