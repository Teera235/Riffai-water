# 🌊 RIFFAI Platform - AI-Powered Flood Prediction System

ระบบคาดการณ์น้ำท่วมด้วย AI และข้อมูลดาวเทียม สำหรับการบริหารจัดการน้ำในประเทศไทย

[![Status](https://img.shields.io/badge/status-production-success)](https://riffai-frontend-715107904640.asia-southeast1.run.app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Live Demo

- **Frontend:** https://riffai-frontend-715107904640.asia-southeast1.run.app
- **API Docs:** https://riffai-backend-715107904640.asia-southeast1.run.app/docs

## ✨ Features

### 🛰️ Satellite Data Integration
- **Sentinel-2** optical imagery (10m resolution)
  - NDVI (Vegetation Index)
  - NDWI (Water Index)
  - MNDWI (Modified Water Index)
  - LSWI (Land Surface Water Index)
  - NDBI (Built-up Index)
- **Sentinel-1** SAR imagery (10m resolution)
  - VV/VH polarization
  - Change detection
  - All-weather monitoring

### 🤖 AI Prediction
- HydroLSTM deep learning models
- 7-30 day flood forecasts
- Flood probability calculation
- Affected area estimation
- Confidence scoring

### 📊 Real-time Monitoring
- Water level tracking
- Rainfall monitoring
- Multi-basin support (3 basins)
- Interactive maps
- Alert system

### 🗺️ GIS Integration
- PostGIS spatial database
- Basin geometries
- Flood extent mapping
- Interactive visualization

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │  Next.js + TypeScript
│   (Cloud Run)   │  Tailwind CSS + Leaflet
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Backend       │  FastAPI + Python
│   (Cloud Run)   │  SQLAlchemy + Alembic
└────────┬────────┘
         │
         ├──────────────┐
         ▼              ▼
┌─────────────┐  ┌──────────────┐
│  Database   │  │ Earth Engine │
│  Cloud SQL  │  │   Satellite  │
│  PostGIS    │  │     Data     │
└─────────────┘  └──────────────┘
```

## 📦 Tech Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Leaflet (maps)
- Recharts (charts)
- Axios

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL + PostGIS
- Google Earth Engine
- TensorFlow/Keras
- Pandas + NumPy

### Infrastructure
- Google Cloud Run
- Cloud SQL
- Cloud Build
- Secret Manager

### AI/ML
- HydroLSTM models
- TensorFlow 2.19
- Scikit-learn
- Time series forecasting

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ with PostGIS
- Google Cloud account
- Earth Engine account

### Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/Teera235/Riffai-water.git
cd Riffai-water
```

#### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
# Edit .env file with your database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### 3. Setup Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

#### 4. Authenticate Earth Engine
```bash
python authenticate-ee.py
```

### 🌐 Production Deployment

#### Deploy Backend
```bash
cd backend
gcloud builds submit --config cloudbuild.yaml --region asia-southeast1
```

#### Deploy Frontend
```bash
cd frontend
gcloud run deploy riffai-frontend --source . --region asia-southeast1
```

## 📊 Data Sources

### Satellite Data
- **Sentinel-2:** Optical imagery from ESA
- **Sentinel-1:** SAR imagery from ESA
- **Source:** Google Earth Engine

### Hydrological Data
- Water level stations
- Rainfall stations
- Historical flood records

### Basins Covered
1. **Mekong North** (28,000 km²)
2. **Eastern Coast** (13,830 km²)
3. **Southern East** (11,850 km²)

## 🧪 Testing

### Test Satellite Data
```bash
python test-satellite-indices.py
```

### Test AI Models
```bash
python test-ai-models.py
```

### Test API
```bash
# Health check
curl https://riffai-backend-715107904640.asia-southeast1.run.app/

# Get prediction
curl -X POST https://riffai-backend-715107904640.asia-southeast1.run.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"basin_id":"mekong_north","days_ahead":7}'
```

## 📖 Documentation

- [Deployment Guide](DEPLOY-README.md)
- [Satellite Indices](SATELLITE-INDICES.md)
- [Earth Engine Setup](EARTH-ENGINE-AUTH.md)
- [API Documentation](https://riffai-backend-715107904640.asia-southeast1.run.app/docs)
- [Final Status](FINAL-STATUS.md)

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/riffai
GEE_PROJECT_ID=your-project-id
GEE_SERVICE_ACCOUNT=your-sa@project.iam.gserviceaccount.com
GEE_KEY_FILE=/path/to/key.json
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.run.app
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Teera** - *Initial work* - [Teera235](https://github.com/Teera235)

## 🙏 Acknowledgments

- [HydroLSTM](https://github.com/uihilab/HydroLSTM) - LSTM models for hydrological forecasting
- [Google Earth Engine](https://earthengine.google.com/) - Satellite data platform
- [Sentinel Hub](https://www.sentinel-hub.com/) - Sentinel satellite data
- Thai Meteorological Department - Weather and rainfall data

## 📊 Project Status

- ✅ Frontend deployed and operational
- ✅ Backend API deployed and operational
- ✅ Database configured with PostGIS
- ✅ Earth Engine integration complete
- ✅ AI models integrated (3 HydroLSTM models)
- ✅ Real-time satellite data retrieval
- ✅ Prediction system active

## 🎯 Roadmap

- [ ] Train custom models with local data
- [ ] Add more basins (expand coverage)
- [ ] Mobile application
- [ ] Email/SMS notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Historical flood database
- [ ] Community reporting system

## 📞 Support

For support, email teera@example.com or open an issue in this repository.

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Built with ❤️ for flood prevention and water management in Thailand**
