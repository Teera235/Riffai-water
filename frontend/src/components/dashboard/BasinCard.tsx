import Link from "next/link";
import { Droplets, CloudRain, Map, TrendingUp } from "lucide-react";
import { Basin, RiskLevel } from "@/types";
import RiskBadge from "@/components/common/RiskBadge";

const borderColors: Record<RiskLevel, string> = {
  normal: "border-primary-300",
  watch: "border-primary-500",
  warning: "border-primary-700",
  critical: "border-primary-900 shadow-mono-lg",
};

export default function BasinCard({ basin }: { basin: Basin }) {
  return (
    <div
      className={`card-mono border-2 ${borderColors[basin.risk_level]} p-5 hover:shadow-mono-xl transition-all duration-200 animate-slide-up`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4 pb-3 border-b border-primary-200">
        <div>
          <h3 className="text-lg font-bold text-primary-900 tracking-tight">
            {basin.name}
          </h3>
          <p className="text-xs text-primary-600 mt-1 font-mono">
            {basin.provinces?.join(" · ")}
          </p>
        </div>
        <RiskBadge level={basin.risk_level} />
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-primary-50 border border-primary-200 rounded-mono p-3">
          <div className="flex items-center gap-1.5 mb-2">
            <Droplets className="w-3.5 h-3.5 text-primary-600" strokeWidth={2.5} />
            <div className="text-xs text-primary-600 font-semibold uppercase tracking-wider">
              Water Level
            </div>
          </div>
          <div className="text-xl font-bold text-primary-900 font-mono">
            {basin.current_water_level?.toFixed(2) ?? "—"}
            <span className="text-sm font-normal text-primary-600 ml-1">m</span>
          </div>
        </div>
        <div className="bg-primary-50 border border-primary-200 rounded-mono p-3">
          <div className="flex items-center gap-1.5 mb-2">
            <CloudRain className="w-3.5 h-3.5 text-primary-600" strokeWidth={2.5} />
            <div className="text-xs text-primary-600 font-semibold uppercase tracking-wider">
              Rainfall
            </div>
          </div>
          <div className="text-xl font-bold text-primary-900 font-mono">
            {basin.today_rainfall_mm?.toFixed(1) ?? 0}
            <span className="text-sm font-normal text-primary-600 ml-1">mm</span>
          </div>
        </div>
      </div>

      {/* AI Prediction */}
      {basin.prediction && basin.prediction.flood_probability !== null && (
        <div className="bg-primary-900 text-white rounded-mono p-4 mb-4">
          <div className="text-xs font-semibold uppercase tracking-wider mb-2 opacity-80">
            AI Prediction
          </div>
          <div className="flex items-end justify-between">
            <div>
              <div className="text-3xl font-bold font-mono">
                {(basin.prediction.flood_probability * 100).toFixed(0)}%
              </div>
              <div className="text-xs opacity-80 mt-1">
                Flood Probability
              </div>
            </div>
            {basin.prediction.affected_area_sqkm && (
              <div className="text-xs opacity-80 font-mono">
                {basin.prediction.affected_area_sqkm.toFixed(0)} km²
              </div>
            )}
          </div>

          {/* Probability bar */}
          <div className="mt-3 h-1.5 bg-white/20 rounded-mono overflow-hidden">
            <div
              className="h-full bg-white transition-all duration-500"
              style={{
                width: `${Math.min(basin.prediction.flood_probability * 100, 100)}%`,
              }}
            />
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2">
        <Link
          href={`/map?basin=${basin.id}`}
          className="flex-1 btn-mono-outline text-center py-2.5 text-sm flex items-center justify-center gap-2"
        >
          <Map className="w-4 h-4" strokeWidth={2} />
          View Map
        </Link>
        <Link
          href={`/predict?basin=${basin.id}`}
          className="flex-1 btn-mono text-center py-2.5 text-sm flex items-center justify-center gap-2"
        >
          <TrendingUp className="w-4 h-4" strokeWidth={2} />
          Predict
        </Link>
      </div>
    </div>
  );
}
