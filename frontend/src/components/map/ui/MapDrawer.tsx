"use client";

import { ReactNode } from "react";
import { ChevronLeft, PanelLeftClose, PanelLeftOpen } from "lucide-react";

interface MapDrawerProps {
  title: string;
  subtitle?: string;
  open: boolean;
  onToggle: () => void;
  children: ReactNode;
}

export default function MapDrawer({
  title,
  subtitle,
  open,
  onToggle,
  children,
}: MapDrawerProps) {
  return (
    <div className="absolute inset-0 z-[1000] pointer-events-none">
      <button
        type="button"
        onClick={onToggle}
        className="pointer-events-auto absolute left-4 top-4 h-10 min-w-10 px-2 btn-mono-outline bg-white/95 shadow-mono flex items-center gap-1"
        aria-label={open ? "Close map controls" : "Open map controls"}
      >
        {open ? <PanelLeftClose className="h-4 w-4" /> : <PanelLeftOpen className="h-4 w-4" />}
        <span className="hidden sm:inline text-xs">Controls</span>
      </button>

      <aside
        className={`pointer-events-auto absolute left-4 right-4 top-16 bottom-4 sm:right-auto sm:w-[23rem] card-mono shadow-mono-lg overflow-hidden transition-transform duration-200 ${
          open ? "translate-x-0" : "-translate-x-[120%]"
        }`}
        aria-hidden={!open}
      >
        <div className="flex items-center justify-between border-b border-primary-200 px-4 py-3">
          <div>
            <h2 className="text-lg font-bold tracking-tight text-primary-900 text-wrap balance">{title}</h2>
            {subtitle ? <p className="text-xs text-primary-600 font-mono">{subtitle}</p> : null}
          </div>
          <button
            type="button"
            onClick={onToggle}
            className="h-10 w-10 rounded-mono border border-primary-300 bg-white hover:bg-primary-100 transition-colors flex items-center justify-center"
            aria-label="Collapse map controls"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
        </div>
        <div className="h-[calc(100%-4rem)] overflow-y-auto p-4 space-y-6">{children}</div>
      </aside>
    </div>
  );
}
