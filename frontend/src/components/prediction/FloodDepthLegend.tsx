interface FloodDepthData {
  area_sqm: number;
  volume_m3: number;
  depth_m: number;
  color: string;
}

const SAMPLE_DATA: FloodDepthData[] = [
  { area_sqm: 2526213, volume_m3: 1422707, depth_m: 2.5, color: "bg-primary-900" },
  { area_sqm: 4561560, volume_m3: 3703487, depth_m: 1.5, color: "bg-primary-600" },
  { area_sqm: 6086186, volume_m3: 5738665, depth_m: 0.5, color: "bg-primary-300" },
];

export default function FloodDepthLegend({ data = SAMPLE_DATA }: { data?: FloodDepthData[] }) {
  return (
    <div className="p-4 bg-primary-50 border border-primary-200 rounded-mono">
      <div className="grid grid-cols-3 gap-4 text-xs font-mono">
        <div>
          <div className="font-semibold text-primary-900 mb-2 uppercase tracking-wider">
            Area (m²)
          </div>
          <div className="space-y-1 text-primary-700">
            {data.map((d, i) => (
              <div key={i}>{d.area_sqm.toLocaleString()}</div>
            ))}
          </div>
        </div>
        <div>
          <div className="font-semibold text-primary-900 mb-2 uppercase tracking-wider">
            Volume (m³)
          </div>
          <div className="space-y-1 text-primary-700">
            {data.map((d, i) => (
              <div key={i}>{d.volume_m3.toLocaleString()}</div>
            ))}
          </div>
        </div>
        <div>
          <div className="font-semibold text-primary-900 mb-2 uppercase tracking-wider">
            Depth (m)
          </div>
          <div className="space-y-1">
            {data.map((d, i) => (
              <div key={i} className="flex items-center gap-2">
                <div className={`w-4 h-4 ${d.color}`}></div>
                <span className="text-primary-700">{d.depth_m}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
