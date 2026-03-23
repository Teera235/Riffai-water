"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

interface DataPoint {
  datetime: string;
  level_m: number;
  station_name?: string;
}

export default function WaterLevelChart({
  data,
  warningLevel = 3.0,
  criticalLevel = 4.5,
}: {
  data: DataPoint[];
  warningLevel?: number;
  criticalLevel?: number;
}) {
  const formatted = data.map((d) => ({
    ...d,
    time: new Date(d.datetime).toLocaleDateString("en-US", {
      day: "2-digit",
      month: "short",
    }),
  }));

  return (
    <div className="card-mono p-5">
      <h3 className="text-lg font-bold mb-4 text-primary-900 tracking-tight">
        Water Level Trend
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" stroke="#dee2e6" vertical={false} />
          <XAxis 
            dataKey="time" 
            tick={{ fontSize: 11, fill: "#868e96", fontFamily: "monospace" }}
            axisLine={{ stroke: "#dee2e6" }}
          />
          <YAxis 
            tick={{ fontSize: 11, fill: "#868e96", fontFamily: "monospace" }}
            label={{ value: "m", angle: 0, position: "top", offset: 10 }}
            axisLine={{ stroke: "#dee2e6" }}
          />
          <Tooltip
            contentStyle={{ 
              borderRadius: "2px", 
              border: "1px solid #dee2e6",
              fontFamily: "monospace",
              fontSize: "12px"
            }}
            formatter={(value: any) => [`${value.toFixed(2)} m`, "Level"]}
          />
          <ReferenceLine
            y={warningLevel}
            stroke="#868e96"
            strokeDasharray="5 5"
            strokeWidth={1}
            label={{ value: "Warning", fill: "#868e96", fontSize: 10 }}
          />
          <ReferenceLine
            y={criticalLevel}
            stroke="#212529"
            strokeDasharray="5 5"
            strokeWidth={1.5}
            label={{ value: "Critical", fill: "#212529", fontSize: 10, fontWeight: 600 }}
          />
          <Line
            type="monotone"
            dataKey="level_m"
            stroke="#212529"
            strokeWidth={2}
            dot={{ fill: "#212529", r: 3, strokeWidth: 0 }}
            activeDot={{ r: 5, fill: "#212529" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
