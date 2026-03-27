"use client";

import { useEffect, useMemo, useRef, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import dynamic from "next/dynamic";
import { Loader2 } from "lucide-react";
import Navbar from "@/components/common/Navbar";
import { mapAPI, onwrAPI, pipelineAPI } from "@/services/api";
import { GeoJSONFeatureCollection } from "@/types";
import toast from "react-hot-toast";
import TambonFloodLayer from "@/components/map/TambonFloodLayer";
import MapInspector from "@/components/map/MapInspector";
import { useRouter } from "next/navigation";
import { APP_TO_ONWR_BASIN } from "@/constants/onwrBasins";
import { useFloodLayer } from "@/hooks/useFloodLayer";
import FloodLayerPanel, { SAR_FLOOD_LEGEND_STEPS } from "@/components/map/FloodLayerPanel";
import FloodV3ValidationLegend from "@/components/map/FloodV3ValidationLegend";
import { zscoreToColor } from "@/constants/onwrSarZscore";
import MapCommandBar from "@/components/map/MapCommandBar";
import MapLayersPanel from "@/components/map/MapLayersPanel";

const MapView = dynamic(() => import("@/components/map/MapViewSimple"), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full bg-primary-50 rounded-mono">
      <Loader2 className="w-12 h-12 text-primary-400 animate-spin" />
    </div>
  ),
});

function MapContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const searchRef = useRef<HTMLInputElement | null>(null);
  const [basins, setBasins] = useState<GeoJSONFeatureCollection | null>(null);
  const [waterLevels, setWaterLevels] = useState<GeoJSONFeatureCollection | null>(null);
  const [rivers, setRivers] = useState<GeoJSONFeatureCollection | null>(null);
  const [dams, setDams] = useState<GeoJSONFeatureCollection | null>(null);
  const [tileSummary, setTileSummary] = useState<any>(null);
  const [selectedBasin, setSelectedBasin] = useState<string | null>(
    searchParams?.get("basin") || null
  );
  const [subbasins, setSubbasins] = useState<GeoJSONFeatureCollection | null>(null);
  const [selectedSubbasin, setSelectedSubbasin] = useState<string | null>(
    searchParams?.get("subbasin") || null
  );
  const [layers, setLayers] = useState({
    basins: true,
    waterLevels: true,
    rivers: true,
    dams: true,
    satellite: false,
    floodDepth: false,
    rainfall: true,
    heatmap: true,
    timelapse: false,
    tambonFlood: false,
    onwrSar: false,
    onwrNational: false,
    v3DailyValidation: false,
  });
  const {
    geojson: onwrFc,
    dates: onwrDates,
    selectedDate: onwrDate,
    setSelectedDate: setOnwrDate,
    loading: sarLoading,
    loadingDates: sarLoadingDates,
    error: sarError,
  } = useFloodLayer(layers.onwrSar ? selectedBasin : null, layers.onwrSar);
  const [onwrNationalFc, setOnwrNationalFc] = useState<GeoJSONFeatureCollection | null>(null);
  const [v3DailyFc, setV3DailyFc] = useState<GeoJSONFeatureCollection | null>(null);
  const [v3DailyLoading, setV3DailyLoading] = useState(false);
  const [v3DailyError, setV3DailyError] = useState<string | null>(null);
  const [onwrAlerts, setOnwrAlerts] = useState<
    {
      pipeline_basin: string;
      app_basin_id?: string;
      HYBAS_ID?: number;
      name?: string;
      date: string;
      mean_z_score?: number;
    }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [selectedTambon, setSelectedTambon] = useState<any>(null);
  const [layersOpen, setLayersOpen] = useState(false);
  const [searchScope, setSearchScope] = useState<"basin" | "subbasin">("basin");
  const [searchValue, setSearchValue] = useState("");

  const loadMapData = async () => {
    try {
      const [b, w, r, d, ts] = await Promise.all([
        mapAPI.basins(),
        mapAPI.waterLevelMap(selectedBasin || undefined),
        mapAPI.rivers(),
        mapAPI.dams(),
        mapAPI.tilesSummary({ basin_id: selectedBasin || undefined }),
      ]);
      setBasins(b.data);
      setWaterLevels(w.data);
      setRivers(r.data);
      setDams(d.data);
      setTileSummary(ts.data);
      console.log("Map data loaded:", { basins: b.data, rivers: r.data, dams: d.data });
    } catch (err) {
      console.error("Failed to load map data:", err);
      toast.error("โหลดข้อมูลแผนที่ล้มเหลว");
    } finally {
      setLoading(false);
    }
  };

  // Load persisted layer preferences
  useEffect(() => {
    try {
      const raw = localStorage.getItem("riffai.map.layers.v1");
      if (!raw) return;
      const parsed = JSON.parse(raw) as Record<string, unknown>;
      setLayers((prev) => {
        const next = { ...prev };
        for (const k of Object.keys(prev)) {
          if (typeof parsed[k] === "boolean") (next as any)[k] = parsed[k];
        }
        return next;
      });
    } catch {
      // ignore
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Persist layer preferences
  useEffect(() => {
    try {
      localStorage.setItem("riffai.map.layers.v1", JSON.stringify(layers));
    } catch {
      // ignore
    }
  }, [layers]);

  useEffect(() => {
    loadMapData();
  }, [selectedBasin]);

  useEffect(() => {
    const syncUrl = () => {
      const params = new URLSearchParams(Array.from(searchParams?.entries?.() || []));
      if (selectedBasin) params.set("basin", selectedBasin);
      else params.delete("basin");
      if (selectedSubbasin) params.set("subbasin", selectedSubbasin);
      else params.delete("subbasin");
      router.replace(`?${params.toString()}`);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    syncUrl();
  }, [selectedBasin, selectedSubbasin]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const { data } = await onwrAPI.floodAlertsLatest(120);
        if (!cancelled)
          setOnwrAlerts(
            [...(data.alerts || [])].sort(
              (a: { mean_z_score?: number }, b: { mean_z_score?: number }) =>
                (a.mean_z_score ?? 0) - (b.mean_z_score ?? 0)
            )
          );
      } catch {
        if (!cancelled) setOnwrAlerts([]);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [lastUpdate, layers.onwrSar]);

  useEffect(() => {
    if (!layers.onwrNational) {
      setOnwrNationalFc(null);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const { data } = await onwrAPI.thailandSubbasinStatsUrl();
        const res = await fetch(data.url as string);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = (await res.json()) as GeoJSONFeatureCollection;
        if (!cancelled) setOnwrNationalFc(json);
      } catch {
        if (!cancelled) {
          setOnwrNationalFc(null);
          toast.error("ไม่สามารถโหลดชั้น Thailand SAR aggregate (GCS) ได้");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [layers.onwrNational]);

  useEffect(() => {
    if (!layers.v3DailyValidation) {
      setV3DailyFc(null);
      setV3DailyError(null);
      return;
    }
    let cancelled = false;
    setV3DailyLoading(true);
    setV3DailyError(null);
    (async () => {
      try {
        const res = await fetch("/geojson/flood_v3_daily_validation.geojson");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = (await res.json()) as GeoJSONFeatureCollection;
        if (!cancelled) setV3DailyFc(json);
      } catch {
        if (!cancelled) {
          setV3DailyFc(null);
          setV3DailyError("Could not load V3 validation GeoJSON");
          toast.error("โหลดชั้น V3 daily validation ไม่สำเร็จ");
        }
      } finally {
        if (!cancelled) setV3DailyLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [layers.v3DailyValidation]);

  const onwrNationalFiltered = useMemo(() => {
    if (!onwrNationalFc?.features?.length) return null;
    if (!selectedBasin) return onwrNationalFc;
    const pipe = APP_TO_ONWR_BASIN[selectedBasin];
    const feats = onwrNationalFc.features.filter((f) => {
      const p = (f.properties || {}) as Record<string, unknown>;
      if (p.basin_app_id === selectedBasin) return true;
      if (pipe && p.basin_en === pipe) return true;
      return false;
    });
    return feats.length
      ? { ...onwrNationalFc, type: "FeatureCollection" as const, features: feats }
      : onwrNationalFc;
  }, [onwrNationalFc, selectedBasin]);

  useEffect(() => {
    const loadSub = async () => {
      if (!selectedBasin) {
        setSubbasins(null);
        setSelectedSubbasin(null);
        return;
      }
      try {
        const res = await mapAPI.subbasins(selectedBasin);
        setSubbasins(res.data);
      } catch (e) {
        setSubbasins(null);
      }
    };
    loadSub();
  }, [selectedBasin]);

  const refreshData = async () => {
    toast.loading("กำลังดึงข้อมูลใหม่...", { id: "refresh" });
    try {
      await pipelineAPI.fetchWater(selectedBasin || undefined);
      await loadMapData();
      setLastUpdate(new Date());
      toast.success("อัพเดทสำเร็จ!", { id: "refresh" });
    } catch {
      toast.error("ล้มเหลว", { id: "refresh" });
    }
  };

  const toggle = (key: keyof typeof layers) => {
    if (key === "onwrSar" && !selectedBasin) {
      toast.error("เลือกลุ่มน้ำก่อนเปิดชั้นข้อมูล SAR");
      return;
    }
    setLayers((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const exportOnwrCsv = () => {
    if (!onwrFc?.features?.length) return;
    const rows = onwrFc.features.map((f) => {
      const p = f.properties || {};
      return {
        HYBAS_ID: p.HYBAS_ID,
        name: p.NAME || p.name,
        date: p.date,
        mean_z_score: p.mean_z_score,
        flood_detected: p.flood_detected,
      };
    });
    const header = Object.keys(rows[0]);
    const esc = (v: unknown) =>
      `"${String(v ?? "").replace(/"/g, '""')}"`;
    const csv = [header.join(","), ...rows.map((r) => header.map((h) => esc(r[h as keyof typeof r])).join(","))].join(
      "\n"
    );
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `onwr_subbasin_${selectedBasin}_${onwrDate || "export"}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  // Keyboard shortcuts: / focuses search, L toggles layers, Esc closes panels
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      const isTyping =
        target?.tagName === "INPUT" ||
        target?.tagName === "TEXTAREA" ||
        target?.tagName === "SELECT" ||
        (target as any)?.isContentEditable;

      if (!isTyping && e.key === "/") {
        e.preventDefault();
        setLayersOpen(false);
        searchRef.current?.focus();
        return;
      }
      if (!isTyping && (e.key === "l" || e.key === "L")) {
        e.preventDefault();
        setLayersOpen((v) => !v);
        return;
      }
      if (e.key === "Escape") {
        setLayersOpen(false);
        setSelectedTambon(null);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  return (
    <div className="relative h-[calc(100vh-4rem)] bg-gray-50">
      <div className="absolute inset-0">
        <MapView
          basins={basins}
          waterLevels={waterLevels}
          rivers={rivers}
          dams={dams}
          selectedBasin={selectedBasin}
          onwrSarGeoJSON={onwrFc}
          onwrSarDate={onwrDate}
          onwrNationalGeoJSON={onwrNationalFiltered}
          v3DailyGeoJSON={v3DailyFc}
          layers={layers}
        />

        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white/85 backdrop-blur rounded-mono z-[1050] m-3 md:m-4">
            <div className="text-center">
              <Loader2 className="w-12 h-12 text-gray-700 animate-spin mx-auto mb-3" />
              <div className="text-sm text-gray-700 font-medium">Loading map data…</div>
            </div>
          </div>
        )}

        <MapCommandBar
          basins={basins}
          subbasins={subbasins}
          selectedBasin={selectedBasin}
          selectedSubbasin={selectedSubbasin}
          onSelectBasin={setSelectedBasin}
          onSelectSubbasin={setSelectedSubbasin}
          onOpenLayers={() => setLayersOpen(true)}
          onRefresh={refreshData}
          searchValue={searchValue}
          onSearchValueChange={setSearchValue}
          searchScope={searchScope}
          onSearchScopeChange={(s) => {
            setSearchScope(s);
            setSearchValue("");
          }}
          searchInputRef={searchRef}
        />

        <MapLayersPanel
          open={layersOpen}
          onClose={() => setLayersOpen(false)}
          layers={layers as any}
          toggle={toggle as any}
          selectedBasin={selectedBasin}
          onwrSarEnabled={layers.onwrSar}
          onwrDates={onwrDates}
          onwrDate={onwrDate}
          onSetOnwrDate={setOnwrDate}
          onExportOnwrCsv={exportOnwrCsv}
          onwrHasFeatures={Boolean(onwrFc?.features?.length)}
          onwrAlerts={onwrAlerts}
          tileSummary={tileSummary}
          waterLevels={waterLevels}
          lastUpdate={lastUpdate}
        />

        {layers.v3DailyValidation && (
          <FloodV3ValidationLegend
            featureCount={v3DailyFc?.features?.length}
            loading={v3DailyLoading}
            error={v3DailyError}
          />
        )}

        {layers.onwrSar && selectedBasin && (
          <FloodLayerPanel
            dates={onwrDates}
            selectedDate={onwrDate}
            onDateChange={setOnwrDate}
            loading={sarLoading}
            loadingDates={sarLoadingDates}
            error={sarError}
            featureCount={onwrFc?.features?.length}
            floodedCount={
              onwrFc?.features?.filter((f) => f.properties?.flood_detected).length
            }
            pipelineBasinLabel={
              APP_TO_ONWR_BASIN[selectedBasin] ?? selectedBasin
            }
          />
        )}

        {/* Tambon Flood Layer */}
        {layers.tambonFlood && (
          <TambonFloodLayer
            visible={layers.tambonFlood}
            onTambonClick={(tambon) => setSelectedTambon(tambon)}
          />
        )}
        
        <MapInspector tambon={selectedTambon} onClose={() => setSelectedTambon(null)} />
      </div>
    </div>
  );
}

export default function MapPage() {
  return (
    <>
      <Navbar />
      <Suspense
        fallback={
          <div className="flex items-center justify-center h-screen">
            <div className="text-6xl animate-pulse font-bold">MAP</div>
          </div>
        }
      >
        <MapContent />
      </Suspense>
    </>
  );
}
