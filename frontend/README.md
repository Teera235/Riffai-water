# RIFFAI Frontend

Next.js 14 + TypeScript + Tailwind CSS + React Leaflet

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Dashboard (/)
│   ├── map/               # Map page (/map)
│   ├── predict/           # AI Prediction (/predict)
│   ├── alerts/            # Alerts (/alerts)
│   ├── reports/           # Reports (/reports)
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/
│   ├── common/            # Reusable components
│   │   ├── Navbar.tsx
│   │   ├── StatCard.tsx
│   │   └── RiskBadge.tsx
│   ├── dashboard/
│   │   └── BasinCard.tsx
│   ├── charts/
│   │   ├── WaterLevelChart.tsx
│   │   └── RainfallChart.tsx
│   └── map/
│       └── MapView.tsx    # Leaflet map component
├── services/
│   └── api.ts             # API client (axios)
├── types/
│   └── index.ts           # TypeScript types
└── hooks/
    └── useAuth.ts         # Auth hook (future)
```

## 🌐 Pages

- `/` - Dashboard (ภาพรวมสถานการณ์น้ำ)
- `/map` - Interactive Map (แผนที่)
- `/predict` - AI Flood Prediction (AI พยากรณ์น้ำท่วม)
- `/alerts` - Alert System (ระบบเตือนภัย)
- `/reports` - Daily Reports (รายงานสรุป)

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Maps**: React Leaflet + Leaflet
- **Charts**: Recharts
- **HTTP Client**: Axios
- **State**: Zustand (future)
- **Notifications**: React Hot Toast

## 🔧 Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## 📦 Key Dependencies

```json
{
  "react-leaflet": "^4.2.1",
  "leaflet": "^1.9.4",
  "recharts": "^2.12.7",
  "axios": "^1.7.2",
  "react-hot-toast": "^2.4.1"
}
```

## 🐳 Docker

```bash
# Build
docker build -t riffai-frontend .

# Run
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8080 riffai-frontend
```

## 🎨 Features

- ✅ Responsive design (mobile-friendly)
- ✅ Interactive Leaflet map with GeoJSON layers
- ✅ Real-time data visualization (charts)
- ✅ AI prediction interface
- ✅ Alert management system
- ✅ Daily report generation
- ✅ Thai language support
- ✅ Dark mode ready (future)

## 📝 API Integration

All API calls are centralized in `src/services/api.ts`:

```typescript
import { dashboardAPI, mapAPI, predictAPI, alertsAPI } from "@/services/api";

// Example usage
const overview = await dashboardAPI.overview();
const basins = await mapAPI.basins();
const prediction = await predictAPI.flood("mekong_north", 30);
```

## 🗺️ Map Features

- Basin boundaries (GeoJSON polygons)
- Water level stations (markers with risk colors)
- Satellite imagery layers (future)
- Flood prediction overlays (future)

## 🚨 Alert System

- Real-time active alerts
- Alert history (30 days)
- Acknowledge/resolve functionality
- Risk level badges (normal/watch/warning/critical)

## 📊 Charts

- Water level time series (LineChart)
- Rainfall bar chart (BarChart)
- Responsive design with Recharts

## 🎯 Future Enhancements

- [ ] Authentication (login/register)
- [ ] User profile management
- [ ] Dark mode toggle
- [ ] PDF report download
- [ ] Real-time WebSocket updates
- [ ] Mobile app (React Native)
- [ ] Offline mode (PWA)

## 🐛 Known Issues

- Leaflet SSR warning (fixed with dynamic import)
- Map icons require CDN (can be bundled locally)

## 📞 Support

- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs
- Frontend: http://localhost:3000

---

**RIFFAI Platform v1.0** • สนับสนุนโดย NIA
