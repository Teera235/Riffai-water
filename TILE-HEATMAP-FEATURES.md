# 🗺️ Interactive Tile-based Flood Risk Heatmap

## ✨ Features Implemented

### 1. Grid-based Tile System
- แบ่งประเทศไทยเป็น **Grid Tiles** ขนาด 0.5° x 0.5° (~50km x 50km)
- ครอบคลุมพื้นที่ทั้งหมดของประเทศไทย
- แต่ละ tile มี unique ID และ coordinates

### 2. Risk Level Visualization (Heatmap)
สีของ tile แสดงระดับความเสี่ยง:
- 🟢 **เขียว (Safe)**: ปลอดภัย - ไม่มีความเสี่ยง
- 🟡 **เหลือง (Normal)**: ปกติ - สภาวะปกติ
- 🟠 **ส้ม (Watch)**: เฝ้าระวัง - ควรติดตามอย่างใกล้ชิด
- 🔴 **แดง (Warning)**: เตือนภัย - ความเสี่ยงสูง
- 🔴 **แดงเข้ม (Critical)**: วิกฤต - อันตรายทันที

### 3. Interactive Features

#### Hover (เมื่อเลื่อนเมาส์ผ่าน)
- แสดง tooltip พร้อมข้อมูลสรุป:
  - ระดับความเสี่ยง
  - ระดับน้ำเฉลี่ย
  - ปริมาณฝน 24 ชม.
  - จังหวัดในพื้นที่

#### Click (เมื่อคลิก)
- แสดง popup รายละเอียดเต็ม:
  - สถิติหลัก (ระดับน้ำ, ฝน, แนวโน้ม)
  - ประชากรที่เสี่ยง
  - จำนวนสถานีตรวจวัด
  - AI Prediction (โอกาสน้ำท่วม)
- Zoom เข้าไปที่ tile นั้นอัตโนมัติ

### 4. Tile Detail Panel (แผงรายละเอียด)

#### Tab 1: ภาพรวม (Overview)
- 💧 ระดับน้ำเฉลี่ย (เมตร)
- 🌧️ ปริมาณฝน 24 ชม. (มม.)
- 📈 แนวโน้ม (เพิ่มขึ้น/ลดลง/คงที่) พร้อม %
- 🏘️ ประชากรเสี่ยง (คน)
- 📡 จำนวนสถานีตรวจวัด

#### Tab 2: ประวัติ (History)
- แสดงข้อมูลย้อนหลัง 7 วัน
- กราฟแสดงการเปลี่ยนแปลงของ:
  - ระดับน้ำ
  - ปริมาณฝน
  - ระดับความเสี่ยง

#### Tab 3: คาดการณ์ (Prediction)
- 🤖 AI Prediction:
  - โอกาสน้ำท่วม (%)
  - จำนวนวันข้างหน้า
  - Progress bar แสดงความน่าจะเป็น
- ⚠️ การประเมินความเสี่ยง
- 💡 คำแนะนำ

### 5. Summary Statistics (สถิติสรุป)
แสดงใน sidebar:
- จำนวน tiles ทั้งหมด
- จำนวน tiles แยกตามระดับความเสี่ยง:
  - วิกฤต (Critical)
  - เตือนภัย (Warning)
  - เฝ้าระวัง (Watch)
  - ปลอดภัย (Safe)
- ประชากรเสี่ยงรวมทั้งหมด

### 6. Layer Control
- Toggle เปิด/ปิด Heatmap layer
- ใช้งานร่วมกับ layers อื่นได้:
  - Basin boundaries
  - Rivers
  - Dams
  - Water level stations

## 🎯 Technical Implementation

### Backend APIs

#### 1. GET `/api/map/tiles`
ดึงข้อมูล tiles ทั้งหมด (GeoJSON format)
```
Query params:
- risk_level: filter by risk level (optional)
```

#### 2. GET `/api/map/tiles/summary`
ดึงสถิติสรุปของ tiles ทั้งหมด

#### 3. GET `/api/map/tiles/{tile_id}`
ดึงข้อมูลรายละเอียดของ tile เฉพาะ

#### 4. GET `/api/map/tiles/{tile_id}/history`
ดึงข้อมูลประวัติของ tile
```
Query params:
- days: จำนวนวันย้อนหลัง (default: 7, max: 30)
```

### Frontend Components

#### 1. `TileHeatmap.tsx`
- Render grid tiles บนแผนที่
- จัดการ hover/click interactions
- แสดง tooltips และ popups

#### 2. `TileDetailPanel.tsx`
- แผงรายละเอียดด้านขวา
- 3 tabs: Overview, History, Prediction
- แสดงกราฟและสถิติ

#### 3. `MapViewSimple.tsx` (Updated)
- รองรับ heatmap layer
- จัดการ tile selection

#### 4. `map/page.tsx` (Updated)
- เพิ่ม heatmap toggle
- แสดง tile summary stats

## 📊 Data Structure

### Tile Properties
```typescript
interface TileProperties {
  id: string;                    // Unique ID (e.g., "13.5_100.5")
  center: [lat, lon];            // Center coordinates
  riskLevel: string;             // safe|normal|watch|warning|critical
  stats: {
    avgWaterLevel: number;       // Average water level (m)
    rainfall24h: number;         // 24h rainfall (mm)
    stationCount: number;        // Number of stations
    populationAtRisk: number;    // Population at risk
    trend: "up"|"down"|"stable"; // Trend direction
    trendPercent: number;        // Trend percentage
  };
  provinces: string[];           // Provinces in tile
  rivers: string[];              // Rivers in tile
  dams: any[];                   // Dams in tile
  aiPrediction: {
    floodProbability: number;    // Flood probability (%)
    daysAhead: number;           // Days ahead
  };
  lastUpdate: string;            // ISO datetime
}
```

## 🎨 UI/UX Features

### Visual Design
- ✅ Color-coded risk levels
- ✅ Smooth hover effects
- ✅ Animated transitions
- ✅ Responsive tooltips
- ✅ Clean, modern interface

### Interactions
- ✅ Hover to preview
- ✅ Click to see details
- ✅ Auto-zoom to selected tile
- ✅ Tab navigation
- ✅ Close panel button

### Performance
- ✅ Efficient GeoJSON rendering
- ✅ Lazy loading of history data
- ✅ Optimized tile generation
- ✅ Smooth map interactions

## 🚀 Usage

### 1. เปิด Map Page
```
http://localhost:3000/map
```

### 2. เปิด Heatmap Layer
- ใน sidebar ด้านซ้าย
- เลือก "Flood Risk Heatmap"
- Tiles จะปรากฏบนแผนที่

### 3. สำรวจ Tiles
- **Hover**: ดูข้อมูลสรุปแบบเร็ว
- **Click**: ดูรายละเอียดเต็ม + zoom in
- **Panel**: สลับ tabs เพื่อดูข้อมูลต่างๆ

### 4. ดู Summary
- ดูสถิติรวมใน sidebar
- เช็คจำนวน tiles แต่ละระดับความเสี่ยง
- ดูประชากรเสี่ยงทั้งหมด

## 🎯 Future Enhancements (ที่วางแผนไว้)

### 1. Time-lapse Animation 🎬
- เล่นย้อนหลัง 7-30 วัน
- ดูการเปลี่ยนแปลงของสี tiles
- แสดงการเคลื่อนตัวของมวลน้ำ

### 2. Comparison Mode ⚖️
- เปรียบเทียบ 2 ช่วงเวลา
- Split screen before/after
- Highlight differences

### 3. Advanced Filtering 🔍
- กรองตาม risk level
- กรองตามจังหวัด
- กรองตามลุ่มน้ำ

### 4. Export Features 📥
- ดาวน์โหลดรายงาน PDF
- Export ข้อมูล CSV
- บันทึกภาพแผนที่

### 5. Real-time Updates 🔄
- WebSocket สำหรับ live data
- Auto-refresh tiles
- Push notifications

### 6. Smart Clustering 🧩
- Zoom out: รวม tiles เป็นพื้นที่ใหญ่
- Zoom in: แยกเป็น tiles เล็กลง
- Dynamic tile size

## 📝 Notes

- ข้อมูลปัจจุบันเป็น **simulated data** สำหรับ demo
- ใน production จะต้องเชื่อมต่อกับ real-time data sources
- AI predictions ใช้ rule-based fallback (ยังไม่มี trained models)
- Tile size (0.5°) สามารถปรับได้ตามความต้องการ

## 🎉 Summary

ระบบ Interactive Tile-based Heatmap พร้อมใช้งานแล้ว! 

Features หลัก:
✅ Grid-based visualization
✅ 5 risk levels with colors
✅ Interactive hover/click
✅ Detailed tile panel (3 tabs)
✅ Summary statistics
✅ History tracking
✅ AI predictions
✅ Smooth UX/UI

ลองเปิดแผนที่แล้วคลิกดู tiles ต่างๆ ได้เลย! 🚀
