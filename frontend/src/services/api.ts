import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

// Auto attach token
api.interceptors.request.use((config) => {
  // #region agent log
  if (typeof window !== "undefined") {
    const dbg = {
      sessionId: "5f3060",
      runId: "cors-debug",
      hypothesisId: "H_browser_request",
      location: "frontend/src/services/api.ts:request-interceptor",
      message: "Axios request config (baseURL/url)",
      data: {
        apiUrlEnv: process.env.NEXT_PUBLIC_API_URL ? "[set]" : "[unset]",
        apiUrlDefault: API_URL,
        baseURL: config.baseURL,
        url: config.url,
        method: config.method,
      },
      timestamp: Date.now(),
    };
    fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "5f3060" },
      body: JSON.stringify(dbg),
    }).catch(() => {});
  }
  // #endregion

  if (typeof window !== "undefined") {
    const token = localStorage.getItem("riffai_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (resp) => resp,
  (error) => {
    // #region agent log
    if (typeof window !== "undefined") {
      const cfg = error?.config;
      const resp = error?.response;
      const dbg = {
        sessionId: "5f3060",
        runId: "cors-debug",
        hypothesisId: "H_axios_error",
        location: "frontend/src/services/api.ts:response-error-interceptor",
        message: "Axios error (CORS often => no response / Network Error)",
        data: {
          message: error?.message,
          code: error?.code,
          name: error?.name,
          networkError: error?.message === "Network Error",
          hasResponse: !!resp,
          baseURL: cfg?.baseURL,
          fullUrl: cfg?.baseURL && cfg?.url ? `${cfg.baseURL}${cfg.url}` : cfg?.url,
          method: cfg?.method,
          status: resp?.status,
          statusText: resp?.statusText,
        },
        timestamp: Date.now(),
      };
      fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "5f3060" },
        body: JSON.stringify(dbg),
      }).catch(() => {});
    }
    // #endregion
    // #region agent log
    if (typeof window !== "undefined") {
      const cfg = error?.config;
      const resp = error?.response;
      const url = String(cfg?.url || "");
      if (resp?.status === 404 && url.includes("alerts")) {
        const base = String(cfg?.baseURL || "").replace(/\/$/, "");
        const path = url.startsWith("/") ? url : `/${url}`;
        fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "c3765a" },
          body: JSON.stringify({
            sessionId: "c3765a",
            runId: "pre-fix",
            hypothesisId: "H1_H2_H3",
            location: "frontend/src/services/api.ts:alerts-404",
            message: "404 on alerts API path",
            data: {
              baseURL: cfg?.baseURL,
              url: cfg?.url,
              params: cfg?.params,
              constructedPath: `${base}${path}`,
              method: cfg?.method,
              status: 404,
              H1_missingRoutes:
                url === "/api/alerts" || url.startsWith("/api/alerts/history"),
              H2_checkBase: cfg?.baseURL,
            },
            timestamp: Date.now(),
          }),
        }).catch(() => {});
      }
    }
    // #endregion
    return Promise.reject(error);
  }
);

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
  summary: (days = 30) => api.get("/api/dashboard/summary", { params: { days } }),
  basinStats: (basinId: string, days = 30) =>
    api.get(`/api/dashboard/stats/${basinId}`, { params: { days } }),
};

// ═══════════ Map ═══════════
export const mapAPI = {
  basins: () => api.get("/api/map/basins"),
  subbasins: (basinId: string) => api.get("/api/map/subbasins", { params: { basin_id: basinId } }),
  rivers: () => api.get("/api/map/rivers"),
  dams: () => api.get("/api/map/dams"),
  stations: (basinId?: string) =>
    api.get("/api/map/stations", { params: { basin_id: basinId } }),
  waterLevelMap: (basinId?: string) =>
    api.get("/api/map/water-level-map", { params: { basin_id: basinId } }),
  floodLayer: (basinId: string, date?: string) =>
    api.get(`/api/map/flood-layer/${basinId}`, { params: { date } }),
  satellite: (basinId: string, index = "ndwi") =>
    api.get(`/api/map/satellite/${basinId}`, { params: { index } }),
  tiles: (params?: { risk_level?: string; basin_id?: string; date?: string }) =>
    api.get("/api/map/tiles", { params }),
  tilesSummary: (params?: { basin_id?: string; date?: string }) =>
    api.get("/api/map/tiles/summary", { params }),
  tile: (tileId: string) => api.get(`/api/map/tiles/${tileId}`),
  tileHistory: (tileId: string, days = 7) =>
    api.get(`/api/map/tiles/${tileId}/history`, { params: { days } }),
  tileSatellite: (tileId: string) =>
    api.get(`/api/map/tiles/${tileId}/satellite`),
};

/** ONWR Sentinel-1 zonal stats (pipeline basin names: UpperMekong, EastCoast, LowerSouthEast) */
export const onwrAPI = {
  dates: (basinEn: string) =>
    api.get(`/api/basins/${encodeURIComponent(basinEn)}/dates`),
  stats: (basinEn: string, date: string) =>
    api.get(`/api/basins/${encodeURIComponent(basinEn)}/${date}/stats`),
  floodAlertsLatest: (limit = 200) =>
    api.get("/api/flood-alerts/latest", { params: { limit } }),
  /** JSON with signed URL to ~26MB national GeoJSON on GCS */
  thailandSubbasinStatsUrl: (expirationHours = 2) =>
    api.get("/api/basins/onwr/thailand-subbasin-stats-url", {
      params: { expiration_hours: expirationHours },
    }),
  /** Signed URL for Model_Output_test Z-Score GeoTIFF (not XYZ tiles — use GeoTIFF-aware map layer) */
  zscoreRasterUrl: (params: {
    basin_en: string;
    date: string;
    band?: string;
    tile?: string;
    expiration_hours?: number;
  }) =>
    api.get("/api/basins/onwr/zscore-raster-url", { params }),
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
  feed: (params?: { days?: number; limit?: number }) =>
    api.get("/api/alerts", { params }),
  /** When GET /api/alerts is missing (older backend), falls back to /api/alerts/active. */
  async feedWithFallback(params?: { days?: number; limit?: number }) {
    try {
      const r = await api.get("/api/alerts", { params });
      // #region agent log
      if (typeof window !== "undefined") {
        fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "c3765a" },
          body: JSON.stringify({
            sessionId: "c3765a",
            runId: "post-fix",
            hypothesisId: "H_verify_feed",
            location: "frontend/src/services/api.ts:feedWithFallback",
            message: "alert feed OK",
            data: { source: "GET /api/alerts" },
            timestamp: Date.now(),
          }),
        }).catch(() => {});
      }
      // #endregion
      return r;
    } catch (e: unknown) {
      const status = (e as { response?: { status?: number } })?.response?.status;
      if (status === 404) {
        const r = await api.get("/api/alerts/active");
        const alerts = r.data?.alerts ?? [];
        const asList = Array.isArray(alerts)
          ? alerts.map((a: Record<string, unknown>) => ({ ...a, is_active: true }))
          : [];
        // #region agent log
        if (typeof window !== "undefined") {
          fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "c3765a" },
            body: JSON.stringify({
              sessionId: "c3765a",
              runId: "post-fix",
              hypothesisId: "H1_confirmed_fallback",
              location: "frontend/src/services/api.ts:feedWithFallback",
              message: "feed 404, using active list",
              data: { count: asList.length },
              timestamp: Date.now(),
            }),
          }).catch(() => {});
        }
        // #endregion
        return { ...r, data: asList };
      }
      throw e;
    }
  },
  active: (basinId?: string) =>
    api.get("/api/alerts/active", { params: { basin_id: basinId } }),
  check: () => api.post("/api/alerts/check"),
  markRead: (id: number) => api.post(`/api/alerts/${id}/read`),
  acknowledge: (id: number) => api.put(`/api/alerts/${id}/acknowledge`),
  resolve: (id: number) => api.put(`/api/alerts/${id}/resolve`),
  dismiss: (id: number) => api.delete(`/api/alerts/${id}`),
  history: (days = 30) => api.get("/api/alerts/history", { params: { days } }),
  /** History endpoint missing on older backends → empty list. */
  async historyWithFallback(days = 30) {
    try {
      const r = await api.get("/api/alerts/history", { params: { days } });
      if (typeof window !== "undefined") {
        fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "c3765a" },
          body: JSON.stringify({
            sessionId: "c3765a",
            runId: "post-fix",
            hypothesisId: "H_verify_history",
            location: "frontend/src/services/api.ts:historyWithFallback",
            message: "alert history OK",
            data: { source: "GET /api/alerts/history" },
            timestamp: Date.now(),
          }),
        }).catch(() => {});
      }
      return r;
    } catch (e: unknown) {
      if ((e as { response?: { status?: number } })?.response?.status === 404) {
        if (typeof window !== "undefined") {
          fetch("http://127.0.0.1:7908/ingest/8ecea870-d1d6-42b5-905e-45e03cf5df70", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-Debug-Session-Id": "c3765a" },
            body: JSON.stringify({
              sessionId: "c3765a",
              runId: "post-fix",
              hypothesisId: "H1_history_missing",
              location: "frontend/src/services/api.ts:historyWithFallback",
              message: "history 404, returning empty",
              data: {},
              timestamp: Date.now(),
            }),
          }).catch(() => {});
        }
        return { data: { alerts: [] } };
      }
      throw e;
    }
  },
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

// ═══════════ Tambon Flood Prediction ═══════════
export const tambonAPI = {
  getTambon: (tbIdn: string) =>
    api.get(`/api/flood/tambon/${tbIdn}`),
  getProvinceTambons: (provinceName: string) =>
    api.get(`/api/flood/tambon/province/${provinceName}`),
  getTopRisk: (limit = 100) =>
    api.get("/api/flood/tambon/top-risk", { params: { limit } }),
  search: (query: string) =>
    api.get("/api/flood/tambon/search", { params: { q: query } }),
  getStats: () =>
    api.get("/api/flood/tambon/stats"),
  getBasinSummary: (basinId: string) =>
    api.get(`/api/flood/tambon/basin/${basinId}/summary`),
  getMapGeoJSON: (params?: { risk_level?: string; min_probability?: number; limit?: number }) =>
    api.get("/api/flood/tambon/map/geojson", { params }),
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
  fetchSar: (basinId?: string) =>
    api.post("/api/pipeline/fetch-sar", null, {
      params: { basin_id: basinId },
    }),
  fetchHistorical: (basinId: string, startYear = 2020, endYear = 2024) =>
    api.post("/api/pipeline/fetch-historical", null, {
      params: { basin_id: basinId, start_year: startYear, end_year: endYear },
    }),
  testEarthEngine: () => api.get("/api/pipeline/test-ee"),
};

// ═══════════ Reports ═══════════
export const reportsAPI = {
  daily: (date?: string) =>
    api.get("/api/reports/daily", { params: { date } }),
};

export default api;
