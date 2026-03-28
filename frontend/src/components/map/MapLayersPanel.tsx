"use client";

import { X, Layers, Download, AlertTriangle } from "lucide-react";
import type { GeoJSONFeatureCollection } from "@/types";

type LayersState = Record<string, boolean>;

export default function MapLayersPanel(props: {
  open: boolean;
  onClose: () => void;
  layers: LayersState;
  toggle: (k: keyof LayersState) => void;
  selectedBasin: string | null;

  onwrSarEnabled: boolean;
  onwrDates: string[];
  onwrDate: string | null;
  onSetOnwrDate: (d: string | null) => void;
  onExportOnwrCsv: () => void;
  onwrHasFeatures: boolean;

  onwrAlerts: {
    pipeline_basin: string;
    HYBAS_ID?: number;
    name?: string;
    date: string;
    mean_z_score?: number;
  }[];

  tileSummary: any | null;
  waterLevels: GeoJSONFeatureCollection | null;
  lastUpdate: Date;
}) {
  if (!props.open) return null;

  const layerRows: { key: keyof LayersState; label: string; description: string }[] = [
    { key: "heatmap", label: "Flood Risk Heatmap", description: "Grid-based risk visualization" },
    { key: "onwrSar", label: "ONWR SAR sub-basin (Z-score)", description: "Sentinel-1 zonal stats — HydroBASIN Lev09" },
    { key: "tambonFlood", label: "Tambon Flood Prediction", description: "XGBoost AI model (6,363 tambons)" },
    { key: "v3DailyValidation", label: "V3 daily validation (TP/TN/FP/FN)", description: "Static test-set snapshot — 6,363 tambon markers" },
    { key: "timelapse", label: "Time-lapse Animation", description: "Historical playback (7 days)" },
    { key: "basins", label: "Basin Boundaries", description: "Administrative boundaries" },
    { key: "rivers", label: "Rivers", description: "Major river systems" },
    { key: "dams", label: "Dams & Reservoirs", description: "Water management infrastructure" },
    { key: "waterLevels", label: "Water Levels", description: "Current station readings" },
    { key: "floodDepth", label: "Flood Depth", description: "Predicted inundation depth" },
    { key: "rainfall", label: "Rainfall Data", description: "Precipitation measurements" },
    { key: "satellite", label: "Satellite Imagery", description: "Sentinel-1/2 imagery" },
    { key: "onwrNational", label: "ONWR national aggregate", description: "Thailand SAR aggregate from GCS" },
  ];

  return (
    <div className="fixed inset-0 z-[1200]">
      <button
        type="button"
        aria-label="Close layers panel"
        onClick={props.onClose}
        className="absolute inset-0 bg-black/30 backdrop-blur-[1px]"
      />

      <div
        className={[
          "absolute left-0 right-0 bottom-0",
          "md:left-4 md:right-auto md:top-16 md:bottom-auto",
          "w-full md:w-[420px]",
          "bg-white/95 backdrop-blur border border-gray-200",
          "rounded-t-2xl md:rounded-2xl shadow-mono-lg",
          "max-h-[85vh] md:max-h-[calc(100vh-6rem)] overflow-hidden",
          "animate-slide-up",
        ].join(" ")}
        role="dialog"
        aria-modal="true"
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-mono bg-gray-50 border border-gray-200 flex items-center justify-center">
              <Layers className="w-5 h-5 text-gray-900" />
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-900">Layers & tools</div>
              <div className="text-xs text-gray-500 font-mono">
                {props.selectedBasin ? `basin=${props.selectedBasin}` : "all basins"}
              </div>
            </div>
          </div>
          <button type="button" onClick={props.onClose} className="btn-mono-ghost px-2 py-2" aria-label="Close">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="overflow-y-auto p-4 space-y-6">
          <section>
            <div className="text-xs font-semibold text-gray-700 uppercase tracking-wider mb-3">Data layers</div>
            <div className="space-y-2">
              {layerRows.map(({ key, label, description }) => (
                <label
                  key={String(key)}
                  className="flex items-start gap-3 p-3 rounded-mono border border-gray-200 bg-white hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <input
                    type="checkbox"
                    checked={Boolean(props.layers[key as any])}
                    onChange={() => props.toggle(key)}
                    className="mt-0.5 w-4 h-4 rounded-mono border-gray-300 text-black focus:ring-black"
                  />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-900">{label}</div>
                    <div className="text-xs text-gray-500 font-mono mt-0.5">{description}</div>
                  </div>
                </label>
              ))}
            </div>
          </section>

          {props.onwrSarEnabled && props.selectedBasin && (
            <section className="p-3 rounded-mono border border-sky-200 bg-sky-50">
              <div className="text-xs font-semibold text-sky-900 uppercase tracking-wider mb-2">
                ONWR date (≈6-day SAR cadence)
              </div>
              <select
                value={props.onwrDate || ""}
                onChange={(e) => props.onSetOnwrDate(e.target.value || null)}
                className="input-mono text-sm w-full"
                disabled={!props.onwrDates.length}
              >
                {props.onwrDates.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>

              <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={props.onExportOnwrCsv}
                  disabled={!props.onwrHasFeatures}
                  className="btn-mono-outline text-xs py-2 flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  <Download className="w-4 h-4" />
                  Download CSV
                </button>
                <button
                  type="button"
                  onClick={() => props.onSetOnwrDate(props.onwrDates[props.onwrDates.length - 1] || null)}
                  className="btn-mono-ghost text-xs py-2"
                  disabled={!props.onwrDates.length}
                >
                  Jump to latest
                </button>
              </div>
            </section>
          )}

          <section>
            <div className="text-xs font-semibold text-gray-700 uppercase tracking-wider mb-2 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              SAR anomalies (latest)
            </div>
            <div className="max-h-56 overflow-y-auto space-y-1 text-xs border border-gray-200 rounded-mono p-2 bg-gray-50/60">
              {props.onwrAlerts.length === 0 ? (
                <span className="text-gray-500">No sub-basin alerts or data not loaded.</span>
              ) : (
                props.onwrAlerts.slice(0, 60).map((a, i) => (
                  <div
                    key={`${a.HYBAS_ID}-${a.date}-${i}`}
                    className="flex justify-between gap-2 py-1 border-b border-gray-200 last:border-0"
                  >
                    <span className="truncate text-gray-800">
                      {a.name || `HYBAS ${a.HYBAS_ID}`}
                      <span className="text-gray-500 font-mono ml-1">{a.pipeline_basin}</span>
                    </span>
                    <span className="font-mono shrink-0 text-red-700">z={a.mean_z_score?.toFixed(2)}</span>
                  </div>
                ))
              )}
            </div>
          </section>

          <section className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {props.layers.heatmap && props.tileSummary && (
              <div className="p-4 bg-gray-50 border border-gray-200 rounded-mono">
                <div className="text-xs font-semibold text-gray-900 uppercase tracking-wider mb-3">Heatmap summary</div>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-700">Grid tiles</span>
                    <span className="text-lg font-bold text-gray-900 font-mono">{props.tileSummary.totalTiles}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-black rounded" />
                      <span>{props.tileSummary.riskCounts?.critical || 0} Critical</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-gray-700 rounded" />
                      <span>{props.tileSummary.riskCounts?.warning || 0} Warning</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-gray-400 rounded" />
                      <span>{props.tileSummary.riskCounts?.watch || 0} Watch</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-gray-200 rounded" />
                      <span>{props.tileSummary.riskCounts?.safe || 0} Safe</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {props.waterLevels && (
              <div className="p-4 bg-gray-50 border border-gray-200 rounded-mono">
                <div className="text-xs font-semibold text-gray-900 uppercase tracking-wider mb-3">Stations</div>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-700">Total</span>
                    <span className="text-lg font-bold text-gray-900 font-mono">
                      {props.waterLevels.features?.length || 0}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-700">Critical</span>
                    <span className="text-lg font-bold text-gray-900 font-mono">
                      {props.waterLevels.features?.filter((f: any) => f.properties.risk_level === "critical").length || 0}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-700">Warning</span>
                    <span className="text-lg font-bold text-gray-700 font-mono">
                      {props.waterLevels.features?.filter((f: any) => f.properties.risk_level === "warning").length || 0}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-700">Watch</span>
                    <span className="text-lg font-bold text-gray-500 font-mono">
                      {props.waterLevels.features?.filter((f: any) => f.properties.risk_level === "watch").length || 0}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </section>

          <section className="p-3 bg-gray-50 border border-gray-200 rounded-mono text-xs text-gray-700">
            <div className="font-semibold text-gray-900 mb-1">Last update</div>
            <div className="font-mono">
              {props.lastUpdate.toLocaleString("th-TH", { dateStyle: "short", timeStyle: "short" })}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

