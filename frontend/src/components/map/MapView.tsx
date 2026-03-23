"use client";

import { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { GeoJSONFeatureCollection, RiskLevel } from "@/types";

// Fix default icon
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

const RISK_COLORS: Record<string, string> = {
  normal: "#22c55e",
  watch: "#eab308",
  warning: "#f97316",
  critical: "#ef4444",
};

function stationIcon(risk?: string) {
  const color = RISK_COLORS[risk || ""] || "#3b82f6";
  const size = risk === "critical" ? 16 : 12;
  return L.divIcon({
    html: `<div style="background:${color};width:${size}px;height:${size}px;border-radius:50%;border:2px solid white;box-shadow:0 2px 4px rgba(0,0,0,0.3)"></div>`,
    iconSize: [size, size],
    className: "",
  });
}

// Fly to basin when selected
function FlyTo({ center, zoom }: { center?: [number, number]; zoom?: number }) {
  const map = useMap();
  useEffect(() => {
    if (center) map.flyTo(center, zoom || 8, { duration: 1.5 });
  }, [center, zoom, map]);
  return null;
}

interface MapViewProps {
  basins?: GeoJSONFeatureCollection | null;
  waterLevels?: GeoJSONFeatureCollection | null;
  selectedBasin?: string | null;
  layers: {
    basins: boolean;
    waterLevels: boolean;
    satellite: boolean;
  };
}

const BASIN_CENTERS: Record<string, [number, number]> = {
  mekong_north: [19.5, 100.0],
  eastern_coast: [12.5, 101.8],
  southern_east: [6.5, 101.0],
};

export default function MapView({
  basins,
  waterLevels,
  selectedBasin,
  layers,
}: MapViewProps) {
  const flyCenter = selectedBasin
    ? BASIN_CENTERS[selectedBasin]
    : undefined;

  return (
    <MapContainer
      center={[13.7, 100.5]}
      zoom={6}
      style={{ height: "100%", width: "100%" }}
      className="rounded-lg"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {flyCenter && <FlyTo center={flyCenter} />}

      {/* Basin boundaries */}
      {layers.basins && basins && (
        <GeoJSON
          data={basins}
          style={() => ({
            color: "#1e40af",
            weight: 2,
            fillColor: "#3b82f6",
            fillOpacity: 0.08,
            dashArray: "5 5",
          })}
          onEachFeature={(feature, layer) => {
            const p = feature.properties;
            layer.bindPopup(`
              <div class="text-sm">
                <div class="font-bold text-base mb-2">${p.name}</div>
                <div class="space-y-1">
                  <div>📍 ${p.provinces?.join(", ")}</div>
                  <div>📐 ${p.area_sqkm?.toLocaleString()} ตร.กม.</div>
                </div>
              </div>
            `);
          }}
        />
      )}

      {/* Water level markers */}
      {layers.waterLevels &&
        waterLevels?.features?.map((f, i) => {
          const [lon, lat] = f.geometry.coordinates;
          const p = f.properties;
          if (
            selectedBasin &&
            p.basin_id !== selectedBasin
          )
            return null;
          return (
            <Marker
              key={i}
              position={[lat, lon]}
              icon={stationIcon(p.risk_level)}
            >
              <Popup>
                <div className="text-sm min-w-[200px]">
                  <div className="font-bold text-base mb-2">{p.name}</div>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">💧 ระดับน้ำ</span>
                      <span className="font-semibold">
                        {p.water_level_m?.toFixed(2)} ม.
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">📍 จังหวัด</span>
                      <span>{p.province}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">⏰ เวลา</span>
                      <span className="text-xs">
                        {p.datetime
                          ? new Date(p.datetime).toLocaleString("th-TH")
                          : "-"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">สถานะ</span>
                      <span>
                        {p.risk_level === "critical"
                          ? "🔴 วิกฤต"
                          : p.risk_level === "warning"
                          ? "🟠 เตือนภัย"
                          : p.risk_level === "watch"
                          ? "🟡 เฝ้าระวัง"
                          : "🟢 ปกติ"}
                      </span>
                    </div>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}
    </MapContainer>
  );
}
