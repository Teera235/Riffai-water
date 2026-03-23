import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

// Auto attach token
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("riffai_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ═══════════ Auth ═══════════
export const authAPI = {
  login: (email: string, password: string) =>
    api.post("/api/auth/login", { email, password }),
  register: (data: { email: string; name: string; password: string; organization?: string }) =>
    api.post("/api/auth/register", data),
  me: () => api.get("/api/auth/me"),
};

// ═══════════ Dashboard ═══════════
export const dashboardAPI = {
  overview: () => api.get("/api/dashboard/overview"),
  basinStats: (basinId: string, days = 30) =>
    api.get(`/api/dashboard/stats/${basinId}`, { params: { days } }),
};

// ═══════════ Map ═══════════
export const mapAPI = {
  basins: () => api.get("/api/map/basins"),
  stations: (basinId?: string) =>
    api.get("/api/map/stations", { params: { basin_id: basinId } }),
  waterLevelMap: (basinId?: string) =>
    api.get("/api/map/water-level-map", { params: { basin_id: basinId } }),
  floodLayer: (basinId: string, date?: string) =>
    api.get(`/api/map/flood-layer/${basinId}`, { params: { date } }),
  satellite: (basinId: string, index = "ndwi") =>
    api.get(`/api/map/satellite/${basinId}`, { params: { index } }),
};

// ═══════════ Prediction ═══════════
export const predictAPI = {
  flood: (basinId: string, daysAhead = 30) =>
    api.post("/api/predict/flood", null, {
      params: { basin_id: basinId, days_ahead: daysAhead },
    }),
  history: (basinId: string, days = 90) =>
    api.get(`/api/predict/history/${basinId}`, { params: { days } }),
  accuracy: () => api.get("/api/predict/accuracy"),
};

// ═══════════ Alerts ═══════════
export const alertsAPI = {
  active: (basinId?: string) =>
    api.get("/api/alerts/active", { params: { basin_id: basinId } }),
  check: () => api.post("/api/alerts/check"),
  acknowledge: (id: number) => api.put(`/api/alerts/${id}/acknowledge`),
  resolve: (id: number) => api.put(`/api/alerts/${id}/resolve`),
  history: (days = 30) => api.get("/api/alerts/history", { params: { days } }),
};

// ═══════════ Data ═══════════
export const dataAPI = {
  waterLevel: (basinId: string, days = 30) =>
    api.get(`/api/data/water-level/${basinId}`, { params: { days } }),
  rainfall: (basinId: string, days = 30, aggregate = "daily") =>
    api.get(`/api/data/rainfall/${basinId}`, { params: { days, aggregate } }),
  satelliteIndices: (basinId: string, days = 365) =>
    api.get(`/api/data/satellite-indices/${basinId}`, { params: { days } }),
  comparison: (basinId: string, year1: number, year2: number) =>
    api.get(`/api/data/comparison/${basinId}`, { params: { year1, year2 } }),
};

// ═══════════ Pipeline ═══════════
export const pipelineAPI = {
  fetchWater: (basinId?: string) =>
    api.post("/api/pipeline/fetch-water", null, {
      params: { basin_id: basinId },
    }),
  fetchSatellite: (basinId?: string) =>
    api.post("/api/pipeline/fetch-satellite", null, {
      params: { basin_id: basinId },
    }),
};

// ═══════════ Reports ═══════════
export const reportsAPI = {
  daily: (date?: string) =>
    api.get("/api/reports/daily", { params: { date } }),
};

export default api;
