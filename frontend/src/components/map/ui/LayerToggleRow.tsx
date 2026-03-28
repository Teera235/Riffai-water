"use client";

interface LayerToggleRowProps {
  checked: boolean;
  onToggle: () => void;
  label: string;
  description: string;
  disabled?: boolean;
  disabledReason?: string;
}

export default function LayerToggleRow({
  checked,
  onToggle,
  label,
  description,
  disabled,
  disabledReason,
}: LayerToggleRowProps) {
  return (
    <label
      className={`block rounded-mono border p-3 transition-colors ${
        disabled
          ? "border-primary-200 bg-primary-50/60 cursor-not-allowed opacity-70"
          : "border-transparent hover:border-primary-200 hover:bg-primary-50 cursor-pointer"
      }`}
    >
      <div className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={checked}
          onChange={onToggle}
          disabled={disabled}
          className="mt-0.5 h-4 w-4 rounded-mono border-primary-300 text-primary-900 focus:ring-primary-900"
        />
        <div className="min-w-0">
          <div className="text-sm font-medium text-primary-900">{label}</div>
          <div className="mt-0.5 text-xs font-mono text-primary-500">{description}</div>
          {disabledReason ? (
            <div className="mt-1 text-[11px] font-medium text-primary-700">{disabledReason}</div>
          ) : null}
        </div>
      </div>
    </label>
  );
}
