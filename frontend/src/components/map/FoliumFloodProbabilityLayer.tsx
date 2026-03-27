"use client";

import { useEffect, useMemo, useState } from "react";
import { GeoJSON } from "react-leaflet";
import L from "leaflet";
import type { GeoJSONFeatureCollection } from "@/types";

type FeatureProps = Record<string, unknown>;

function num(v: unknown): number | null {
  if (v == null || v === "") return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function pct(p: FeatureProps): number | null {
  const pp = num(p.prob_pct);
  if (pp != null) return pp;
  const fp = num(p.flood_percent);
  if (fp != null) return fp;
  const pr = num(p.flood_probability);
  if (pr == null) return null;
  return pr <= 1 ? pr * 100 : pr;
}

function colorForPct(pctValue: number | null): string {
  if (pctValue == null) return "#94a3b8";
  if (pctValue >= 80) return "#d73027";
  if (pctValue >= 60) return "#fc8d59";
  if (pctValue >= 40) return "#fee08b";
  if (pctValue >= 20) return "#91cf60";
  return "#1a9850";
}

interface Props {
  visible: boolean;
  onLoaded?: (count: number) => void;
}

export default function FoliumFloodProbabilityLayer({ visible, onLoaded }: Props) {
  const [geojson, setGeojson] = useState<GeoJSONFeatureCollection | null>(null);
  const [hasFetched, setHasFetched] = useState(false);

  useEffect(() => {
    if (!visible || hasFetched) return;
    let cancelled = false;

    (async () => {
      try {
        const res = await fetch("/geojson/tambon_flood_probability_polygons.geojson");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as GeoJSONFeatureCollection;
        if (!cancelled) {
          setGeojson(data);
          onLoaded?.(data.features?.length || 0);
          setHasFetched(true);
        }
      } catch {
        if (!cancelled) {
          setGeojson(null);
          onLoaded?.(0);
          setHasFetched(true);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [visible, hasFetched, onLoaded]);

  const layerData = useMemo(() => {
    if (!visible || !geojson?.features?.length) return null;
    return geojson;
  }, [visible, geojson]);

  if (!layerData) return null;

  return (
    <GeoJSON
      key={`folium-flood-layer-${layerData.features.length}`}
      data={layerData}
      style={(feature) => {
        const p = ((feature?.properties || {}) as FeatureProps);
        const prob = pct(p);
        return {
          color: "#1f2937",
          weight: 1.2,
          opacity: 0.95,
          fillColor: colorForPct(prob),
          fillOpacity: 0.72,
        } as L.PathOptions;
      }}
      onEachFeature={(feature, layer) => {
        const p = ((feature.properties || {}) as FeatureProps);
        const prob = pct(p);
        const probText = prob == null ? "—" : `${prob.toFixed(1)}%`;
        const rank = p.rank != null ? String(p.rank) : "—";
        const freq = p.freq != null ? String(p.freq) : "—";
        const actual = p.actual != null ? String(p.actual) : "—";

        layer.bindPopup(`
          <div class="text-sm min-w-[240px]">
            <div class="font-bold text-slate-900 border-b pb-1 mb-2">${String(p.tb_tn ?? "—")}</div>
            <div class="text-xs text-slate-600">${String(p.ap_tn ?? "")} · ${String(p.pv_tn ?? "")}</div>
            <div class="mt-2 font-mono text-xs">Flood Prob (%): <strong>${probText}</strong></div>
            <div class="font-mono text-xs">Risk Rank: ${rank}</div>
            <div class="font-mono text-xs">Avg Freq: ${freq}</div>
            <div class="font-mono text-xs">Actual 2024: ${actual}</div>
            <div class="font-mono text-xs text-slate-500 mt-1">tb_idn: ${String(p.tb_idn ?? "—")}</div>
          </div>
        `);

        layer.on({
          mouseover: (e: any) => {
            const target = e.target as L.Path;
            target.setStyle({
              weight: 2.2,
              fillOpacity: 0.82,
            });
          },
          mouseout: (e: any) => {
            const target = e.target as L.Path;
            target.setStyle({
              weight: 1.2,
              fillOpacity: 0.72,
            });
          },
        });
      }}
    />
  );
}

