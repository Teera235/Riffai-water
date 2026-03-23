"use client";

import { useEffect, useState } from "react";
import { FileText, Calendar, Download, Droplets, CloudRain, AlertTriangle, TrendingUp, Loader2 } from "lucide-react";
import Navbar from "@/components/common/Navbar";
import RiskBadge from "@/components/common/RiskBadge";
import { reportsAPI } from "@/services/api";

export default function ReportsPage() {
  const [report, setReport] = useState<any>(null);
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [loading, setLoading] = useState(true);

  const loadReport = async () => {
    setLoading(true);
    try {
      const res = await reportsAPI.daily(date);
      setReport(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, [date]);

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between mb-8 pb-6 border-b-2 border-primary-900">
            <div>
              <h1 className="text-4xl font-bold text-primary-900 tracking-tight flex items-center gap-3">
                <FileText className="w-9 h-9" strokeWidth={2.5} />
                Reports
              </h1>
              <p className="text-sm text-primary-600 mt-2 font-mono">
                Daily water situation summary
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-primary-600" />
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="input-mono text-sm"
              />
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <Loader2 className="w-12 h-12 text-primary-400 animate-spin mx-auto mb-3" />
                <div className="text-sm text-primary-600 font-medium">Loading report...</div>
              </div>
            </div>
          ) : report ? (
            <div className="space-y-6">
              <div className="card-mono p-6">
                <h2 className="text-2xl font-bold mb-6 text-primary-900 tracking-tight">
                  Water Situation Report —{" "}
                  {new Date(report.report_date).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })}
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  {report.basins?.map((b: any) => (
                    <div
                      key={b.id}
                      className="border border-primary-200 rounded-mono p-4 hover:shadow-mono-lg transition-all"
                    >
                      <div className="flex items-center justify-between mb-3 pb-3 border-b border-primary-200">
                        <h3 className="font-bold text-primary-900">{b.name}</h3>
                        <RiskBadge level={b.risk_level} size="sm" />
                      </div>
                      <div className="text-xs text-primary-500 mb-3 font-mono">
                        {b.provinces?.join(" · ")}
                      </div>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between items-center">
                          <span className="text-primary-600 flex items-center gap-1.5">
                            <Droplets className="w-3.5 h-3.5" />
                            Max Level
                          </span>
                          <span className="font-mono font-medium text-primary-900">
                            {b.water_level?.max_m?.toFixed(2) ?? "—"} m
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-primary-600 flex items-center gap-1.5">
                            <CloudRain className="w-3.5 h-3.5" />
                            Rainfall
                          </span>
                          <span className="font-mono font-medium text-primary-900">
                            {b.rainfall_total_mm?.toFixed(1) ?? "—"} mm
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-primary-600 flex items-center gap-1.5">
                            <AlertTriangle className="w-3.5 h-3.5" />
                            Alerts
                          </span>
                          <span className="font-mono font-medium text-primary-900">
                            {b.alerts_today}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="overflow-x-auto">
                  <table className="table-mono">
                    <thead>
                      <tr>
                        <th>Basin</th>
                        <th>Max Level (m)</th>
                        <th>Avg Level (m)</th>
                        <th>Rainfall (mm)</th>
                        <th>AI Probability</th>
                        <th>Status</th>
                        <th>Alerts</th>
                      </tr>
                    </thead>
                    <tbody>
                      {report.basins?.map((b: any) => (
                        <tr key={b.id}>
                          <td>
                            <div className="font-medium text-primary-900">{b.name}</div>
                            <div className="text-xs text-primary-500 font-mono">
                              {b.provinces?.join(" · ")}
                            </div>
                          </td>
                          <td className="font-mono">
                            {b.water_level?.max_m?.toFixed(2) ?? "—"}
                          </td>
                          <td className="font-mono">
                            {b.water_level?.avg_m?.toFixed(2) ?? "—"}
                          </td>
                          <td className="font-mono">
                            {b.rainfall_total_mm?.toFixed(1) ?? "—"}
                          </td>
                          <td className="font-mono">
                            {b.prediction?.flood_probability != null
                              ? `${(b.prediction.flood_probability * 100).toFixed(0)}%`
                              : "—"}
                          </td>
                          <td>
                            <RiskBadge level={b.risk_level} size="sm" />
                          </td>
                          <td className="font-mono">
                            {b.alerts_today}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="mt-6 flex justify-end">
                  <button className="btn-mono text-sm flex items-center gap-2">
                    <Download className="w-4 h-4" />
                    Download PDF
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="card-mono p-12 text-center">
              <FileText className="w-16 h-16 mx-auto mb-4 text-primary-400" strokeWidth={1.5} />
              <div className="text-primary-600 font-medium">No data available</div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
