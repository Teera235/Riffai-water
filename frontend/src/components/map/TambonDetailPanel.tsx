"use client";

import { X, AlertTriangle, TrendingUp, MapPin } from "lucide-react";

interface TambonData {
  tb_idn: string;
  tb_tn: string;
  ap_tn: string;
  pv_tn: string;
  flood_probability: number;
  flood_percent: number;
  risk_level: string;
}

interface Props {
  tambon: TambonData | null;
  onClose: () => void;
}

const RISK_COLORS: Record<string, string> = {
  VERY_HIGH: "#d73027",
  HIGH: "#fc8d59",
  MEDIUM: "#fee08b",
  LOW: "#91cf60",
  VERY_LOW: "#1a9850",
};

const RISK_LABELS: Record<string, string> = {
  VERY_HIGH: "Very High Risk",
  HIGH: "High Risk",
  MEDIUM: "Medium Risk",
  LOW: "Low Risk",
  VERY_LOW: "Very Low Risk",
};

export default function TambonDetailPanel({ tambon, onClose }: Props) {
  if (!tambon) return null;

  const riskColor = RISK_COLORS[tambon.risk_level] || "#666";
  const riskLabel = RISK_LABELS[tambon.risk_level] || tambon.risk_level;

  return (
    <div className="fixed inset-x-3 top-20 bottom-3 md:inset-x-auto md:right-4 md:top-20 md:bottom-4 md:w-96 bg-white rounded-mono border border-primary-200 shadow-mono-lg z-[1001] flex flex-col overflow-hidden">
      <div className="p-4 border-b border-primary-200 border-l-4" style={{ borderLeftColor: riskColor }}>
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h2 className="text-lg font-bold text-primary-900">{tambon.tb_tn}</h2>
            <p className="text-xs text-primary-600 font-mono mt-1">Tambon ID: {tambon.tb_idn}</p>
            <span
              className="inline-flex mt-2 px-2 py-0.5 rounded-mono text-xs font-semibold text-white"
              style={{ backgroundColor: riskColor }}
            >
              {riskLabel}
            </span>
          </div>
          <button
            onClick={onClose}
            className="h-10 w-10 rounded-mono border border-primary-200 hover:bg-primary-100 transition-colors"
          >
            <X className="w-5 h-5 mx-auto" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <div className="bg-primary-50 rounded-mono p-3 border border-primary-200">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-4 h-4 text-primary-600" />
            <h3 className="font-bold text-sm text-primary-900">Location</h3>
          </div>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-primary-600">Sub-district:</span>
              <span className="font-medium text-primary-900">{tambon.tb_tn}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-primary-600">District:</span>
              <span className="font-medium text-primary-900">{tambon.ap_tn}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-primary-600">Province:</span>
              <span className="font-medium text-primary-900">{tambon.pv_tn}</span>
            </div>
          </div>
        </div>

        <div className="rounded-mono p-4 bg-primary-900 text-white">
          <div className="text-sm opacity-90 mb-2">Annual Flood Probability</div>
          <div className="text-5xl font-bold mb-2 font-mono tabular-nums">{tambon.flood_percent.toFixed(1)}%</div>
          <div className="text-sm opacity-90 font-mono tabular-nums">
            Probability: {tambon.flood_probability.toFixed(4)}
          </div>
        </div>

        <div className="bg-primary-50 rounded-mono p-4 border border-primary-200">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-primary-700" />
            <h3 className="font-bold text-sm text-primary-900">Risk Assessment</h3>
          </div>
          <div className="space-y-3">
            <div>
              <div className="text-xs text-primary-600 mb-1">Risk Level</div>
              <div
                className="inline-block px-3 py-1 rounded-mono text-sm font-bold text-white"
                style={{ backgroundColor: riskColor }}
              >
                {riskLabel}
              </div>
            </div>
            <div>
              <div className="text-xs text-primary-600 mb-1">Interpretation</div>
              <div className="text-sm text-primary-700">
                {tambon.flood_probability >= 0.8 && (
                  <>
                    This area has a <strong>very high likelihood</strong> of experiencing flooding this year. Immediate
                    preparedness measures are recommended.
                  </>
                )}
                {tambon.flood_probability >= 0.6 && tambon.flood_probability < 0.8 && (
                  <>
                    This area has a <strong>high likelihood</strong> of flooding. Monitor conditions closely and prepare
                    emergency plans.
                  </>
                )}
                {tambon.flood_probability >= 0.4 && tambon.flood_probability < 0.6 && (
                  <>
                    This area has a <strong>moderate risk</strong> of flooding. Stay informed and be prepared.
                  </>
                )}
                {tambon.flood_probability >= 0.2 && tambon.flood_probability < 0.4 && (
                  <>
                    This area has a <strong>low risk</strong> of flooding. Normal monitoring is sufficient.
                  </>
                )}
                {tambon.flood_probability < 0.2 && (
                  <>
                    This area has a <strong>very low risk</strong> of flooding. Minimal concern for this year.
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {tambon.flood_probability >= 0.6 && (
          <div className="bg-primary-50 border border-primary-200 rounded-mono p-4">
            <div className="font-bold text-primary-900 mb-2">Recommendations</div>
            <ul className="text-sm text-primary-700 space-y-1">
              <li>• Monitor weather forecasts and water levels</li>
              <li>• Prepare emergency evacuation plan</li>
              <li>• Move valuables to higher ground</li>
              <li>• Stock emergency supplies (food, water, medicine)</li>
              <li>• Stay informed through official channels</li>
            </ul>
          </div>
        )}

        <div className="bg-primary-50 rounded-mono p-4 border border-primary-200">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-primary-700" />
            <h3 className="font-bold text-sm text-primary-900">Model Information</h3>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-primary-600">Model:</span>
              <span className="font-medium text-primary-900">XGBoost V2</span>
            </div>
            <div className="flex justify-between">
              <span className="text-primary-600">Accuracy:</span>
              <span className="font-medium text-primary-900 font-mono tabular-nums">83%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-primary-600">AUC-ROC:</span>
              <span className="font-medium text-primary-900 font-mono tabular-nums">0.9131</span>
            </div>
            <div className="flex justify-between">
              <span className="text-primary-600">Training Period:</span>
              <span className="font-medium text-primary-900">2011-2024</span>
            </div>
            <div className="flex justify-between">
              <span className="text-primary-600">Features:</span>
              <span className="font-medium text-primary-900">19 variables</span>
            </div>
          </div>
        </div>

        <div className="bg-primary-50 rounded-mono p-4 border border-primary-200">
          <h3 className="font-bold text-sm text-primary-900 mb-2">Data Sources</h3>
          <div className="space-y-1 text-xs text-primary-600">
            <div>• Sentinel-2 Optical Imagery (NDVI, NDWI, NDMI)</div>
            <div>• Sentinel-1 SAR (VV, VH polarization)</div>
            <div>• ERA5-Land Climate Data (rainfall, temperature)</div>
            <div>• SRTM Digital Elevation Model</div>
            <div>• GISTDA Historical Flood Records (2011-2024)</div>
          </div>
        </div>
      </div>

      <div className="p-3 border-t border-primary-200 bg-primary-50">
        <div className="text-xs text-primary-600 text-center">Prediction updated daily at 06:00 AM Bangkok time</div>
      </div>
    </div>
  );
}
