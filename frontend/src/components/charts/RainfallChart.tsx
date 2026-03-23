"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface DataPoint {
  date: string;
  total_mm: number;
}

export default function RainfallChart({ data }: { data: DataPoint[] }) {
  const formatted = data.map((d) => ({
    ...d,
    day: new Date(d.date).toLocaleDateString("en-US", {
      day: "2-digit",
      month: "short",
    }),
  }));

  return (
    <div className="card-mono p-5">
      <h3 className="text-lg font-bold mb-4 text-primary-900 tracking-tight">
        Daily Rainfall
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" stroke="#dee2e6" vertical={false} />
          <XAxis 
            dataKey="day" 
            tick={{ fontSize: 11, fill: "#868e96", fontFamily: "monospace" }}
            axisLine={{ stroke: "#dee2e6" }}
          />
          <YAxis 
            tick={{ fontSize: 11, fill: "#868e96", fontFamily: "monospace" }}
            label={{ value: "mm", angle: 0, position: "top", offset: 10 }}
            axisLine={{ stroke: "#dee2e6" }}
          />
          <Tooltip
            contentStyle={{ 
              borderRadius: "2px", 
              border: "1px solid #dee2e6",
              fontFamily: "monospace",
              fontSize: "12px"
            }}
            formatter={(value: any) => [`${value.toFixed(1)} mm`, "Rainfall"]}
          />
          <Bar 
            dataKey="total_mm" 
            fill="#212529" 
            radius={[0, 0, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
