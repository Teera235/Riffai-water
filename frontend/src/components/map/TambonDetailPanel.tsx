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
    <div className="fixed right-4 top-20 bottom-4 w-96 bg-white rounded-lg shadow-2xl z-[1001] flex flex-col overflow-hidden">
      {/* Header */}
      <div
        className="p-4 text-white"
        style={{ backgroundColor: riskColor }}
      >
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <h2 className="text-xl font-bold">{riskLabel}</h2>
            <p className="text-sm opacity-90 mt-1">
              {tambon.tb_tn}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-white/20 rounded transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="text-xs opacity-75">
          Tambon ID: {tambon.tb_idn}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Location */}
        <div className="bg-gray-50 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-4 h-4 text-gray-600" />
            <h3 className="font-bold text-sm text-black">Location</h3>
          </div>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Sub-district:</span>
              <span className="font-medium text-black">{tambon.tb_tn}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">District:</span>
              <span className="font-medium text-black">{tambon.ap_tn}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Province:</span>
              <span className="font-medium text-black">{tambon.pv_tn}</span>
            </div>
          </div>
        </div>

        {/* Flood Probability */}
        <div
          className="rounded-lg p-4 text-white"
          style={{ backgroundColor: riskColor }}
        >
          <div className="text-sm opacity-90 mb-2">Annual Flood Probability</div>
          <div className="text-5xl font-bold mb-2">
            {tambon.flood_percent.toFixed(1)}%
          </div>
          <div className="text-sm opacity-90">
            Probability: {tambon.flood_probability.toFixed(4)}
          </div>
        </div>

        {/* Risk Assessment */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-orange-600" />
            <h3 className="font-bold text-sm text-black">Risk Assessment</h3>
          </div>

          <div className="space-y-3">
            {/* Risk Level */}
            <div>
              <div className="text-xs text-gray-600 mb-1">Risk Level</div>
              <div
                className="inline-block px-3 py-1 rounded-full text-sm font-bold text-white"
                style={{ backgroundColor: riskColor }}
              >
                {riskLabel}
              </div>
            </div>

            {/* Interpretation */}
            <div>
              <div className="text-xs text-gray-600 mb-1">Interpretation</div>
              <div className="text-sm text-gray-700">
                {tambon.flood_probability >= 0.8 && (
                  <>
                    This area has a <strong>very high likelihood</strong> of experiencing
                    flooding this year. Immediate preparedness measures are recommended.
                  </>
                )}
                {tambon.flood_probability >= 0.6 && tambon.flood_probability < 0.8 && (
                  <>
                    This area has a <strong>high likelihood</strong> of flooding.
                    Monitor conditions closely and prepare emergency plans.
                  </>
                )}
                {tambon.flood_probability >= 0.4 && tambon.flood_probability < 0.6 && (
                  <>
                    This area has a <strong>moderate risk</strong> of flooding.
                    Stay informed and be prepared.
                  </>
                )}
                {tambon.flood_probability >= 0.2 && tambon.flood_probability < 0.4 && (
                  <>
                    This area has a <strong>low risk</strong> of flooding.
                    Normal monitoring is sufficient.
                  </>
                )}
                {tambon.flood_probability < 0.2 && (
                  <>
                    This area has a <strong>very low risk</strong> of flooding.
                    Minimal concern for this year.
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        {tambon.flood_probability >= 0.6 && (
          <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-4">
            <div className="font-bold text-orange-900 mb-2">Recommendations</div>
            <ul className="text-sm text-orange-700 space-y-1">
              <li>• Monitor weather forecasts and water levels</li>
              <li>• Prepare emergency evacuation plan</li>
              <li>• Move valuables to higher ground</li>
              <li>• Stock emergency supplies (food, water, medicine)</li>
              <li>• Stay informed through official channels</li>
            </ul>
          </div>
        )}

        {/* Model Information */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-sm text-black">Model Information</h3>
          </div>

          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Model:</span>
              <span className="font-medium text-black">XGBoost V2</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Accuracy:</span>
              <span className="font-medium text-black">83%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">AUC-ROC:</span>
              <span className="font-medium text-black">0.9131</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Training Period:</span>
              <span className="font-medium text-black">2011-2024</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Features:</span>
              <span className="font-medium text-black">19 variables</span>
            </div>
          </div>
        </div>

        {/* Data Sources */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-sm text-black mb-2">Data Sources</h3>
          <div className="space-y-1 text-xs text-gray-600">
            <div>• Sentinel-2 Optical Imagery (NDVI, NDWI, NDMI)</div>
            <div>• Sentinel-1 SAR (VV, VH polarization)</div>
            <div>• ERA5-Land Climate Data (rainfall, temperature)</div>
            <div>• SRTM Digital Elevation Model</div>
            <div>• GISTDA Historical Flood Records (2011-2024)</div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="p-3 border-t bg-gray-50">
        <div className="text-xs text-gray-500 text-center">
          Prediction updated daily at 06:00 AM Bangkok time
        </div>
      </div>
    </div>
  );
}
