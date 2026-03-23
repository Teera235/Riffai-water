import { LucideIcon } from "lucide-react";

interface StatCardProps {
  icon: LucideIcon;
  label: string;
  value: string;
  sub?: string;
  color?: "black" | "gray";
}

export default function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  color = "black",
}: StatCardProps) {
  return (
    <div className="card-mono p-5 hover:shadow-mono-lg transition-all duration-200">
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 bg-primary-900 flex items-center justify-center">
          <Icon className="w-5 h-5 text-white" strokeWidth={2.5} />
        </div>
        {sub && <div className="text-xs text-primary-500 font-mono">{sub}</div>}
      </div>
      <div className="text-xs font-semibold text-primary-600 uppercase tracking-wider mb-2">
        {label}
      </div>
      <div className="text-3xl font-bold text-primary-900 tracking-tight">
        {value}
      </div>
    </div>
  );
}
