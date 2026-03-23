"use client";

import { useEffect, useState } from "react";
import { AlertTriangle, CheckCircle, Search, RefreshCw, MapPin, Clock, Activity } from "lucide-react";
import Navbar from "@/components/common/Navbar";
import RiskBadge from "@/components/common/RiskBadge";
import { alertsAPI } from "@/services/api";
import { Alert } from "@/types";
import toast from "react-hot-toast";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [historyAlerts, setHistoryAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadAlerts = async () => {
    try {
      const [active, history] = await Promise.all([
        alertsAPI.active(),
        alertsAPI.history(30),
      ]);
      setAlerts(active.data.alerts || []);
      setHistoryAlerts(history.data.alerts || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const checkNow = async () => {
    toast.loading("กำลังตรวจสอบ...", { id: "check" });
    try {
      const res = await alertsAPI.check();
      toast.success(
        `ตรวจสอบเสร็จ สร้าง ${res.data.alerts_created} รายการ`,
        { id: "check" }
      );
      await loadAlerts();
    } catch {
      toast.error("ล้มเหลว", { id: "check" });
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  const basinName: Record<string, string> = {
    mekong_north: "ลุ่มน้ำโขงเหนือ",
    eastern_coast: "ชายฝั่งตะวันออก",
    southern_east: "ภาคใต้ฝั่งตะวันออก",
  };

  return (
    <>
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-between mb-8 pb-6 border-b-2 border-primary-900">
          <h1 className="text-4xl font-bold text-primary-900 tracking-tight flex items-center gap-3">
            <AlertTriangle className="w-9 h-9" strokeWidth={2.5} />
            Alert System
          </h1>
          <button
            onClick={checkNow}
            className="btn-mono text-sm flex items-center gap-2"
          >
            <Search className="w-4 h-4" />
            Check Now
          </button>
        </div>

        {/* Active Alerts */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-6 text-primary-900 tracking-tight flex items-center gap-2">
            <Activity className="w-6 h-6" />
            Active Alerts ({alerts.length})
          </h2>

          {alerts.length === 0 ? (
            <div className="card-mono p-12 text-center">
              <CheckCircle className="w-16 h-16 mx-auto mb-4 text-primary-400" strokeWidth={1.5} />
              <div className="text-xl font-bold text-primary-900 mb-2">
                No Active Alerts
              </div>
              <div className="text-sm text-primary-600">
                All systems operating normally
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {alerts.map((a) => (
                <div
                  key={a.id}
                  className="card-mono p-6 border-l-4 border-primary-900"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <RiskBadge level={a.level} />
                        <h3 className="font-bold text-lg text-primary-900">{a.title}</h3>
                      </div>
                      <p className="text-primary-700 mb-3">{a.message}</p>
                      <div className="flex items-center gap-4 text-xs text-primary-600 font-mono">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3.5 h-3.5" />
                          {basinName[a.basin_id] || a.basin_id}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5" />
                          {new Date(a.created_at).toLocaleString("en-US")}
                        </span>
                        <span className="flex items-center gap-1">
                          <Activity className="w-3.5 h-3.5" />
                          {a.trigger_type}: {a.trigger_value?.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    {!a.acknowledged && (
                      <button
                        onClick={async () => {
                          await alertsAPI.acknowledge(a.id);
                          toast.success("Acknowledged");
                          loadAlerts();
                        }}
                        className="btn-mono-outline text-xs px-3 py-1.5"
                      >
                        Acknowledge
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* History */}
        <div>
          <h2 className="text-2xl font-bold mb-6 text-primary-900 tracking-tight flex items-center gap-2">
            <Clock className="w-6 h-6" />
            History (30 Days) — {historyAlerts.length}
          </h2>
          <div className="card-mono overflow-hidden">
            <table className="table-mono">
              <thead>
                <tr>
                  <th>Status</th>
                  <th>Basin</th>
                  <th>Type</th>
                  <th>Date</th>
                  <th>Active</th>
                </tr>
              </thead>
              <tbody>
                {historyAlerts.slice(0, 20).map((a: any) => (
                  <tr key={a.id}>
                    <td>
                      <RiskBadge level={a.level} size="sm" />
                    </td>
                    <td className="font-mono">
                      {basinName[a.basin_id] || a.basin_id}
                    </td>
                    <td className="font-mono text-primary-600">
                      {a.trigger_type}
                    </td>
                    <td className="font-mono text-primary-600">
                      {new Date(a.created_at).toLocaleString("en-US", {
                        month: "short",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </td>
                    <td>
                      {a.is_active ? (
                        <span className="badge-mono bg-primary-900 text-white text-xs">
                          ACTIVE
                        </span>
                      ) : (
                        <span className="badge-mono bg-primary-200 text-primary-600 text-xs">
                          RESOLVED
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}
