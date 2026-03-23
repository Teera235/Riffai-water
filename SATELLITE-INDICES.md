# 🛰️ Satellite Indices & SAR Features

ระบบ RIFFAI ใช้ดาวเทียม Sentinel-2 และ Sentinel-1 เพื่อวิเคราะห์พื้นที่น้ำและคาดการณ์น้ำท่วม

## 📡 Sentinel-2 (Optical Indices)

### NDVI - Normalized Difference Vegetation Index
**สูตร:** `(NIR - Red) / (NIR + Red)`
- **ช่วงค่า:** -1 ถึง +1
- **ความหมาย:**
  - > 0.6: พืชพรรณหนาแน่น
  - 0.3-0.6: พืชพรรณปานกลาง
  - < 0.3: ดินเปล่า/น้ำ
- **ใช้สำหรับ:** ตรวจสอบสุขภาพพืชพรรณ, แยกแยะพื้นที่เกษตร

### NDWI - Normalized Difference Water Index
**สูตร:** `(Green - NIR) / (Green + NIR)`
- **ช่วงค่า:** -1 ถึง +1
- **ความหมาย:**
  - > 0.3: แหล่งน้ำ
  - 0.0-0.3: พื้นที่เปียกชื้น
  - < 0.0: พื้นที่แห้ง
- **ใช้สำหรับ:** ตรวจจับแหล่งน้ำ, ติดตามการเปลี่ยนแปลงพื้นที่น้ำ

### MNDWI - Modified Normalized Difference Water Index
**สูตร:** `(Green - SWIR) / (Green + SWIR)`
- **ช่วงค่า:** -1 ถึง +1
- **ความหมาย:**
  - > 0.3: น้ำชัดเจน
  - 0.0-0.3: พื้นที่เปียก
  - < 0.0: พื้นที่แห้ง
- **ใช้สำหรับ:** แยกน้ำออกจากดิน, แม่นยำกว่า NDWI
- **ข้อดี:** ลดสัญญาณรบกวนจากดินและอาคาร

### LSWI - Land Surface Water Index
**สูตร:** `(NIR - SWIR) / (NIR + SWIR)`
- **ช่วงค่า:** -1 ถึง +1
- **ความหมาย:**
  - > 0.2: พื้นที่น้ำ/พื้นที่เปียกมาก
  - 0.0-0.2: ความชื้นปานกลาง
  - < 0.0: พื้นที่แห้ง
- **ใช้สำหรับ:** ตรวจจับความชื้นผิวดิน, พื้นที่ชุ่มน้ำ, นาข้าว

### NDBI - Normalized Difference Built-up Index
**สูตร:** `(SWIR - NIR) / (SWIR + NIR)`
- **ช่วงค่า:** -1 ถึง +1
- **ความหมาย:**
  - > 0.0: พื้นที่สิ่งปลูกสร้าง
  - < 0.0: พื้นที่ธรรมชาติ
- **ใช้สำหรับ:** แยกพื้นที่เมือง, ประเมินความเสี่ยงน้ำท่วมในเมือง

## 📡 Sentinel-1 (SAR Features)

### VV Polarization
- **หน่วย:** dB (decibels)
- **ช่วงค่า:** -25 ถึง 0 dB
- **ความหมาย:**
  - < -15 dB: พื้นผิวเรียบ (น้ำ)
  - -15 ถึง -10 dB: พื้นผิวเปียก
  - > -10 dB: พื้นผิวขรุขรา (ดิน/พืช)
- **ใช้สำหรับ:** ตรวจจับน้ำ, ทำงานได้ทั้งกลางวันและกลางคืน

### VH Polarization
- **หน่วย:** dB (decibels)
- **ช่วงค่า:** -30 ถึง -10 dB
- **ความหมาย:**
  - ต่ำกว่า VV ประมาณ 5-10 dB
  - ไวต่อโครงสร้างพืชพรรณ
- **ใช้สำหรับ:** แยกแยะประเภทพืชพรรณ, ตรวจจับน้ำท่วมในป่า

### VV/VH Ratio
- **ช่วงค่า:** 0.5 ถึง 2.0
- **ความหมาย:**
  - > 1.5: พื้นผิวเรียบ (น้ำ)
  - 1.0-1.5: พื้นผิวปานกลาง
  - < 1.0: พื้นผิวขรุขรา (พืช)
- **ใช้สำหรับ:** เพิ่มความแม่นยำในการตรวจจับน้ำ

### Change Detection
- **วิธีการ:** เปรียบเทียบ VV ระหว่าง 2 ช่วงเวลา
- **Threshold:** การเปลี่ยนแปลง > 3 dB
- **ใช้สำหรับ:** 
  - ตรวจจับน้ำท่วมฉับพลัน
  - ติดตามการเปลี่ยนแปลงระดับน้ำ
  - เตือนภัยล่วงหน้า

## 🔄 Data Flow

```
1. Sentinel-2 (ทุก 5 วัน)
   ↓
   คำนวณ NDVI, NDWI, MNDWI, LSWI, NDBI
   ↓
   ตรวจจับพื้นที่น้ำ (MNDWI > 0)
   ↓
   บันทึกลง Database

2. Sentinel-1 (ทุก 6-12 วัน)
   ↓
   วิเคราะห์ VV, VH backscatter
   ↓
   คำนวณ ratio และ change detection
   ↓
   ตรวจจับน้ำ (VV < -15 dB)
   ↓
   บันทึกลง Database

3. AI Model
   ↓
   รวมข้อมูล Optical + SAR + Water Level + Rainfall
   ↓
   คาดการณ์น้ำท่วม
```

## 📊 API Endpoints

### ดึงข้อมูล Sentinel-2
```bash
POST /api/pipeline/fetch-satellite
{
  "basin_id": "mekong_north"
}
```

**Response:**
```json
{
  "status": "success",
  "source": "sentinel-2",
  "avg_ndvi": 0.4523,
  "avg_ndwi": 0.2341,
  "avg_mndwi": 0.1876,
  "avg_lswi": 0.1234,
  "avg_ndbi": -0.2145,
  "water_area_sqkm": 145.67
}
```

### ดึงข้อมูล Sentinel-1 SAR
```bash
POST /api/pipeline/fetch-sar
{
  "basin_id": "mekong_north"
}
```

**Response:**
```json
{
  "status": "success",
  "source": "sentinel-1-sar",
  "vv_mean_db": -14.5,
  "vh_mean_db": -20.3,
  "vv_vh_ratio": 1.4,
  "water_area_sqkm": 152.34,
  "change_detected": true,
  "change_area_sqkm": 8.5
}
```

## 🧪 Testing

รันไฟล์ทดสอบ:
```bash
cd riffai-platform
python test-satellite-indices.py
```

จะทดสอบ:
- ✓ Optical indices (NDVI, NDWI, MNDWI, LSWI, NDBI)
- ✓ SAR features (VV, VH, ratio, change detection)
- ✓ Time series analysis

## 🔐 Authentication

### Earth Engine Authentication
```bash
# Install
pip install earthengine-api

# Authenticate
earthengine authenticate

# หรือใช้ Service Account
export GEE_SERVICE_ACCOUNT="your-account@project.iam.gserviceaccount.com"
export GEE_KEY_FILE="/path/to/key.json"
```

## 📚 References

- [Sentinel-2 Bands](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/resolutions/radiometric)
- [Sentinel-1 SAR](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar)
- [Google Earth Engine](https://earthengine.google.com/)
- [Water Indices Comparison](https://www.mdpi.com/2072-4292/8/4/285)

## 💡 Best Practices

1. **ใช้ MNDWI สำหรับตรวจจับน้ำ** - แม่นยำที่สุด
2. **ใช้ SAR ในฤดูฝน** - ทะลุผ่านเมฆได้
3. **รวม Optical + SAR** - เพิ่มความแม่นยำ
4. **ตรวจสอบ cloud coverage** - ควร < 30%
5. **ใช้ change detection** - เตือนภัยล่วงหน้า

## 🎯 Use Cases

### 1. ตรวจจับน้ำท่วม
- MNDWI > 0.3 + VV < -15 dB = น้ำท่วมแน่นอน
- Change detection = น้ำท่วมฉับพลัน

### 2. ติดตามฤดูกาล
- LSWI + NDVI = ติดตามนาข้าว
- Time series = วิเคราะห์แนวโน้ม

### 3. ประเมินความเสี่ยง
- NDBI = พื้นที่เมือง
- MNDWI + NDBI = เมืองเสี่ยงน้ำท่วม

### 4. คาดการณ์ล่วงหน้า
- LSWI เพิ่มขึ้น = ดินอิ่มตัว
- SAR change = ระดับน้ำเปลี่ยน
- → คาดการณ์น้ำท่วม 7-30 วัน
