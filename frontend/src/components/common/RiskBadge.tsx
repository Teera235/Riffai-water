import { RiskLevel } from "@/types";
import { CheckCircle, Eye, AlertTriangle, AlertOctagon } from "lucide-react";

const config: Record<
  string,
  { label: string; icon: any }
> = {
  normal: { label: "NORMAL", icon: CheckCircle },
  watch: { label: "WATCH", icon: Eye },
  warning: { label: "WARNING", icon: AlertTriangle },
  critical: { label: "CRITICAL", icon: AlertOctagon },
};

export default function RiskBadge({
  level,
  size = "md",
}: {
  level: RiskLevel;
  size?: "sm" | "md" | "lg";
}) {
  const c = config[level] || config.normal;
  const Icon = c.icon;
  
  const sizeClass = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-2.5 py-1",
    lg: "text-base px-3 py-1.5",
  }[size];

  const iconSize = {
    sm: "w-3 h-3",
    md: "w-3.5 h-3.5",
    lg: "w-4 h-4",
  }[size];

  const styleClass = level === "critical" || level === "warning"
    ? "badge-critical"
    : level === "watch"
    ? "badge-warning"
    : "badge-normal";

  return (
    <span className={`${styleClass} ${sizeClass} font-mono flex items-center gap-1.5`}>
      <Icon className={iconSize} strokeWidth={2.5} />
      {c.label}
    </span>
  );
}
