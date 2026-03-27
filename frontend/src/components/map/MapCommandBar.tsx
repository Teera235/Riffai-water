"use client";

import { useMemo } from "react";
import { Layers, RefreshCw, Search } from "lucide-react";
import type { GeoJSONFeatureCollection } from "@/types";

type BasinFeature = {
  properties?: { id?: string; name?: string };
};

type SubBasinFeature = {
  properties?: { subbasin_id?: string; id?: string; name?: string };
};

export type MapSearchScope = "basin" | "subbasin";

export default function MapCommandBar(props: {
  basins: GeoJSONFeatureCollection | null;
  subbasins: GeoJSONFeatureCollection | null;
  selectedBasin: string | null;
  selectedSubbasin: string | null;
  onSelectBasin: (id: string | null) => void;
  onSelectSubbasin: (id: string | null) => void;
  onOpenLayers: () => void;
  onRefresh: () => void;
  searchValue: string;
  onSearchValueChange: (v: string) => void;
  searchScope: MapSearchScope;
  onSearchScopeChange: (s: MapSearchScope) => void;
  searchInputRef?: React.RefObject<HTMLInputElement | null>;
}) {
  const basinOptions = useMemo(() => {
    const feats = (props.basins?.features || []) as unknown as BasinFeature[];
    return feats
      .map((f) => ({
        id: String(f.properties?.id || ""),
        label: String(f.properties?.name || f.properties?.id || ""),
      }))
      .filter((o) => o.id);
  }, [props.basins]);

  const subbasinOptions = useMemo(() => {
    const feats = (props.subbasins?.features || []) as unknown as SubBasinFeature[];
    return feats
      .map((f) => {
        const id = f.properties?.subbasin_id || f.properties?.id;
        return {
          id: id != null ? String(id) : "",
          label: String(f.properties?.name || id || ""),
        };
      })
      .filter((o) => o.id);
  }, [props.subbasins]);

  const filtered = useMemo(() => {
    const q = props.searchValue.trim().toLowerCase();
    if (!q) return [];
    const source = props.searchScope === "basin" ? basinOptions : subbasinOptions;
    return source
      .filter((o) => o.label.toLowerCase().includes(q) || o.id.toLowerCase().includes(q))
      .slice(0, 8);
  }, [props.searchScope, props.searchValue, basinOptions, subbasinOptions]);

  const applyFirstMatch = () => {
    const first = filtered[0];
    if (!first) return;
    if (props.searchScope === "basin") {
      props.onSelectBasin(first.id);
      props.onSelectSubbasin(null);
    } else {
      props.onSelectSubbasin(first.id);
    }
  };

  return (
    <div className="pointer-events-none absolute left-3 right-3 top-3 z-[1100] md:left-4 md:right-auto md:top-4">
      <div className="pointer-events-auto w-full md:w-[520px] card-mono shadow-mono-lg border-gray-200/80 bg-white/90 backdrop-blur">
        <div className="flex items-center gap-2 px-3 py-2">
          <div className="flex items-center gap-2 min-w-0 flex-1">
            <div className="hidden md:flex items-center gap-2 text-xs font-semibold tracking-wide text-gray-700 whitespace-nowrap">
              <Search className="w-4 h-4" />
              Find
            </div>
            <div className="flex items-center gap-2 min-w-0 flex-1">
              <select
                value={props.searchScope}
                onChange={(e) => props.onSearchScopeChange(e.target.value as MapSearchScope)}
                className="text-xs rounded-mono border border-gray-300 bg-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-black"
              >
                <option value="basin">Basin</option>
                <option value="subbasin" disabled={!props.selectedBasin}>
                  Sub-basin
                </option>
              </select>
              <div className="relative min-w-0 flex-1">
                <input
                  ref={props.searchInputRef as any}
                  value={props.searchValue}
                  onChange={(e) => props.onSearchValueChange(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      applyFirstMatch();
                    }
                  }}
                  placeholder={
                    props.searchScope === "basin"
                      ? "Type basin name…"
                      : props.selectedBasin
                        ? "Type sub-basin name…"
                        : "Select a basin first…"
                  }
                  disabled={props.searchScope === "subbasin" && !props.selectedBasin}
                  className="w-full text-sm rounded-mono border border-gray-300 bg-white px-3 py-2 pr-3 focus:outline-none focus:ring-2 focus:ring-black disabled:opacity-50"
                />
                {filtered.length > 0 && (
                  <div className="absolute mt-1 w-full rounded-mono border border-gray-200 bg-white shadow-mono-lg overflow-hidden">
                    {filtered.map((o) => (
                      <button
                        type="button"
                        key={o.id}
                        onClick={() => {
                          if (props.searchScope === "basin") {
                            props.onSelectBasin(o.id);
                            props.onSelectSubbasin(null);
                          } else {
                            props.onSelectSubbasin(o.id);
                          }
                        }}
                        className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 transition-colors"
                      >
                        <div className="truncate font-medium text-gray-900">{o.label}</div>
                        <div className="text-xs font-mono text-gray-500 truncate">{o.id}</div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={props.onOpenLayers}
              className="btn-mono-ghost px-3 py-2 text-sm flex items-center gap-2"
              aria-label="Open layers"
            >
              <Layers className="w-4 h-4" />
              <span className="hidden sm:inline">Layers</span>
            </button>
            <button
              type="button"
              onClick={props.onRefresh}
              className="btn-mono px-3 py-2 text-sm flex items-center gap-2"
              aria-label="Refresh"
            >
              <RefreshCw className="w-4 h-4" />
              <span className="hidden sm:inline">Refresh</span>
            </button>
          </div>
        </div>

        <div className="px-3 pb-3">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <select
              value={props.selectedBasin || ""}
              onChange={(e) => {
                const v = e.target.value || null;
                props.onSelectBasin(v);
                props.onSelectSubbasin(null);
              }}
              className="input-mono text-sm"
            >
              <option value="">All basins</option>
              {basinOptions.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.label}
                </option>
              ))}
            </select>

            <select
              value={props.selectedSubbasin || ""}
              onChange={(e) => props.onSelectSubbasin(e.target.value || null)}
              className="input-mono text-sm"
              disabled={!props.selectedBasin || !props.subbasins}
            >
              <option value="">All sub-basins</option>
              {subbasinOptions.map((o) => (
                <option key={o.id} value={o.id}>
                  {o.label}
                </option>
              ))}
            </select>
          </div>

          <div className="mt-2 text-[11px] text-gray-500 flex flex-wrap gap-x-3 gap-y-1">
            <span className="font-mono">/ search</span>
            <span className="font-mono">L layers</span>
            <span className="font-mono">Esc close</span>
          </div>
        </div>
      </div>
    </div>
  );
}

