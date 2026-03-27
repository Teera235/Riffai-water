"use client";

import { zscoreToColor } from "@/constants/onwrSarZscore";

interface Props {
  dates: string[];
  selectedDate: string | null;
  onDateChange: (d: string) => void;
  loading: boolean;
  loadingDates: boolean;
  error: string | null;
  featureCount?: number;
  floodedCount?: number;
  /** e.g. "EastCoast" for subtitle */
  pipelineBasinLabel?: string;
}

export const SAR_FLOOD_LEGEND_STEPS: {
  range: string;
  label: string;
  z: number | null;
}[] = [
  { range: "Z < −5", label: "Extreme Flood", z: -6 },
  { range: "−5 ≤ Z < −3", label: "Flood Detected", z: -4 },
  { range: "−3 ≤ Z < −1.5", label: "Watch", z: -2 },
  { range: "−1.5 ≤ Z < 0", label: "Below Normal", z: -0.8 },
  { range: "0 ≤ Z < 1.5", label: "Normal", z: 0.7 },
  { range: "Z ≥ 1.5", label: "Above Normal / Dry", z: 2 },
  { range: "—", label: "No Data", z: null },
];

export default function FloodLayerPanel({
  dates,
  selectedDate,
  onDateChange,
  loading,
  loadingDates,
  error,
  featureCount,
  floodedCount,
  pipelineBasinLabel = "EastCoast",
}: Props) {
  return (
    <div className="absolute top-3 right-3 md:top-4 md:right-4 z-[1000] pointer-events-auto">
      <div className="w-[min(92vw,320px)] rounded-2xl border border-white/10 bg-slate-950/80 text-slate-100 shadow-mono-lg backdrop-blur p-4 select-none">
      <div className="flex items-center gap-3 mb-4">
        <span style={{ fontSize: 22, lineHeight: 1 }} aria-hidden>
          🛰️
        </span>
        <div>
          <div className="font-semibold text-sm leading-tight text-slate-100">
            SAR Flood Detection
          </div>
          <div className="text-[11px] text-slate-400 mt-0.5">
            {pipelineBasinLabel} · Sentinel-1 VV Z-score
          </div>
        </div>
      </div>

      <div className="mb-4">
        <div className="text-[10px] font-semibold tracking-[0.14em] uppercase text-slate-400 mb-1">
          Date
        </div>
        {loadingDates ? (
          <div className="text-xs text-indigo-300 py-1.5">
            Loading available dates…
          </div>
        ) : dates.length === 0 ? (
          <div className="text-xs text-red-300">No dates available</div>
        ) : (
          <select
            value={selectedDate ?? ""}
            onChange={(e) => onDateChange(e.target.value)}
            className="w-full text-sm rounded-mono border border-indigo-400/40 bg-slate-900/70 text-slate-100 px-3 py-2 outline-none focus:ring-2 focus:ring-white/20"
          >
            {[...dates].reverse().map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        )}
      </div>

      {loading && (
        <div className="flex items-center gap-2 px-3 py-2 rounded-mono mb-3 bg-indigo-500/10 border border-indigo-400/20">
          <span className="text-indigo-300 text-base" aria-hidden>
            ⟳
          </span>
          <span className="text-xs text-indigo-200">Fetching layer…</span>
        </div>
      )}
      {error && !loading && (
        <div className="px-3 py-2 rounded-mono mb-3 bg-red-500/10 border border-red-400/25 text-xs text-red-200">
          {error}
        </div>
      )}

      {!loading && featureCount != null && (
        <div className="flex gap-2 mb-4">
          <div className="flex-1 px-3 py-2 rounded-mono text-center bg-slate-900/60 border border-indigo-400/15">
            <div className="text-[10px] uppercase tracking-wider text-slate-400">
              Sub-basins
            </div>
            <div className="text-lg font-semibold text-slate-100 mt-0.5 font-mono tabular-nums">
              {featureCount}
            </div>
          </div>
          <div className="flex-1 px-3 py-2 rounded-mono text-center bg-amber-400/10 border border-amber-300/25">
            <div className="text-[10px] uppercase tracking-wider text-amber-200">
              Flooded
            </div>
            <div
              className={[
                "text-lg font-semibold mt-0.5 font-mono tabular-nums",
                floodedCount && floodedCount > 0 ? "text-amber-200" : "text-emerald-300",
              ].join(" ")}
            >
              {floodedCount ?? 0}
            </div>
          </div>
        </div>
      )}

      <div>
        <div className="text-[10px] font-semibold tracking-[0.14em] uppercase text-slate-400 mb-2">
          Z-score Legend
        </div>
        <div className="flex flex-col gap-1.5">
          {SAR_FLOOD_LEGEND_STEPS.map(({ range, label, z }) => (
            <div key={label} className="flex items-center gap-2.5">
              <div
                className="w-[18px] h-[18px] rounded-mono shrink-0 border border-white/15"
                style={{
                  background: zscoreToColor(z),
                  boxShadow: z !== null && z < -3 ? `0 0 6px ${zscoreToColor(z)}88` : undefined,
                }}
              />
              <div className="flex-1 min-w-0">
                <span className="text-xs font-medium text-slate-200">
                  {label}
                </span>
                <span className="text-[10px] text-slate-500 ml-1.5 font-mono">
                  {range}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-indigo-400/15 text-[10px] text-slate-500 leading-relaxed">
        Source: ONWR pipeline · GCS bucket{" "}
        <code className="text-indigo-200">onwr-data</code>
        <br />
        Flood threshold: mean Z-score &lt; −3.0
      </div>
      </div>
    </div>
  );
}
