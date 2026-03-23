# RiffAI - AI Engine

AI Engine สำหรับพยากรณ์น้ำท่วมโดยใช้ HydroLSTM (Encoder-Decoder LSTM)

## โมเดล

### HydroLSTM
- **ที่มา**: [UIHILab/HydroLSTM](https://github.com/uihilab/HydroLSTM)
- **สถาปัตยกรรม**: Encoder-Decoder LSTM
- **Input**: 
  - Precipitation (mm)
  - Water level (m)
  - Evapotranspiration (mm/month)
  - Previous discharge (m3/s)
- **Output**: Future water level/discharge predictions
- **Horizon**: 24-120 hours ahead

### Performance
- **R² Score**: > 0.85 (target)
- **RMSE**: < 0.5 m (water level)
- **MAE**: < 0.3 m (water level)

## การติดตั้ง

```bash
cd ai-engine
pip install -r requirements.txt
```

## การฝึกโมเดล

### ฝึกโมเดลสำหรับลุ่มน้ำเดียว

```bash
cd training
python train_model.py --basin mekong_north --epochs 100 --batch-size 32
```

### ฝึกโมเดลทั้ง 3 ลุ่มน้ำ

```bash
python train_model.py
```

## โครงสร้างไฟล์

```
ai-engine/
├── models/
│   ├── __init__.py
│   ├── hydro_lstm.py          # HydroLSTM model class
│   └── trained/               # Trained models
│       ├── mekong_north/
│       │   ├── model.h5
│       │   ├── scalers.pkl
│       │   └── metrics.txt
│       ├── eastern_coast/
│       └── southern_east/
├── training/
│   ├── __init__.py
│   └── train_model.py         # Training script
├── requirements.txt
└── README.md
```

## การใช้งานใน Backend

```python
from app.services.ai_service import AIService

ai_service = AIService()

# Predict flood
result = ai_service.predict(
    basin_id='mekong_north',
    satellite_data=sat_data,
    water_data=water_data,
    rainfall_data=rainfall_data,
    days_ahead=30
)

print(f"Flood probability: {result['flood_probability']}")
print(f"Predicted water level: {result['predicted_water_level']} m")
```

## ข้อมูลที่ใช้ฝึก

### Input Features (24 hours history)
1. **Precipitation** (mm) - ปริมาณฝน
2. **Water Level** (m) - ระดับน้ำ
3. **Evapotranspiration** (mm/month) - การคายน้ำ
4. **Discharge** (m³/s) - อัตราการไหล

### Output (24 hours ahead)
- **Water Level** (m) - ระดับน้ำในอนาคต
- **Flood Probability** - ความน่าจะเป็นของน้ำท่วม

## Model Versions

### v1.0 - Rule-based (Current)
- Simple heuristic-based prediction
- No training required
- Accuracy: ~75%
- Used as fallback

### v2.0 - HydroLSTM (In Development)
- Deep learning LSTM model
- Requires training on historical data
- Target accuracy: >85%
- 24-hour predictions

### v3.0 - HydroLSTM Extended (Future)
- Extended prediction horizon (120 hours)
- Multi-site learning
- Watershed features integration

## References

1. Xiang, Z., Yan, J., & Demir, I. (2020). A rainfall‐runoff model with LSTM‐based sequence‐to‐sequence learning. Water Resources Research, 56(1), e2019WR025326.

2. Xiang, Z., & Demir, I. (2020). Distributed long-term hourly streamflow predictions using deep learning–A case study for State of Iowa. Environmental Modelling & Software, 104761.

3. Xiang, Z., Demir, I., Mantilla, R., & Krajewski, W. F. (2021). A Regional Semi-Distributed Streamflow Model Using Deep Learning.

## TODO

- [ ] Connect training script to production database
- [ ] Implement data preprocessing pipeline
- [ ] Add model versioning and A/B testing
- [ ] Create automated retraining pipeline
- [ ] Add model monitoring and drift detection
- [ ] Implement ensemble methods
- [ ] Add uncertainty quantification
