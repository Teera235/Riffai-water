import L from "leaflet";

const RISK_COLORS: Record<string, string> = {
  normal: "#22c55e",
  watch: "#eab308",
  warning: "#f97316",
  critical: "#ef4444",
};

export function stationIcon(risk?: string, type?: string) {
  const color = RISK_COLORS[risk || ""] || "#3b82f6";
  const size = risk === "critical" ? 18 : risk === "warning" ? 15 : 12;
  
  return L.divIcon({
    html: `
      <div style="
        background:${color};
        width:${size}px;
        height:${size}px;
        border-radius:50%;
        border:3px solid white;
        box-shadow:0 2px 8px rgba(0,0,0,0.3);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:${size - 4}px;
        position:relative;
      ">
        ${risk === "critical" ? '<div style="position:absolute;width:100%;height:100%;border-radius:50%;border:2px solid ' + color + ';animation:pulse 2s infinite;"></div>' : ''}
      </div>
    `,
    iconSize: [size, size],
    className: "",
  });
}

export function satelliteIcon() {
  return L.divIcon({
    html: `
      <div style="
        background:linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        width:24px;
        height:24px;
        border-radius:4px;
        border:2px solid white;
        box-shadow:0 2px 8px rgba(0,0,0,0.3);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:14px;
      ">🛰️</div>
    `,
    iconSize: [24, 24],
    className: "",
  });
}

export const FLOOD_DEPTH_COLORS: Record<number, string> = {
  0: "#dbeafe",
  0.5: "#93c5fd",
  1.0: "#3b82f6",
  1.5: "#1e40af",
  2.0: "#1e3a8a",
  2.5: "#172554",
};

export const BASIN_CENTERS: Record<string, [number, number]> = {
  mekong_north: [19.5, 100.0],
  eastern_coast: [12.5, 101.8],
  southern_east: [6.5, 101.0],
};
