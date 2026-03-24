"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Map, TrendingUp, AlertTriangle, FileText, Droplets, BarChart3 } from "lucide-react";

const navItems = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/map", label: "Map", icon: Map },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/predict", label: "Predict", icon: TrendingUp },
  { href: "/alerts", label: "Alerts", icon: AlertTriangle },
  { href: "/reports", label: "Reports", icon: FileText },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-white border-b-2 border-primary-900 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary-900 flex items-center justify-center">
              <Droplets className="w-6 h-6 text-white" strokeWidth={2.5} />
            </div>
            <div>
              <div className="text-xl font-bold text-primary-900 tracking-tight">
                RIFFAI
              </div>
              <div className="text-[9px] text-primary-600 -mt-1 font-mono tracking-widest">
                PLATFORM
              </div>
            </div>
          </div>

          {/* Nav */}
          <div className="flex items-center space-x-1">
            {navItems.map((item) => {
              const active = pathname === item.href;
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 px-4 py-2 rounded-mono text-sm font-medium transition-all ${
                    active
                      ? "bg-primary-900 text-white"
                      : "text-primary-700 hover:bg-primary-100 hover:text-primary-900"
                  }`}
                >
                  <Icon className="w-4 h-4" strokeWidth={2} />
                  {item.label}
                </Link>
              );
            })}
          </div>

          {/* Right */}
          <div className="flex items-center space-x-3">
            <div className="text-xs text-primary-600 text-right font-mono">
              NIA
            </div>
            <div className="w-8 h-8 bg-primary-900 text-white flex items-center justify-center font-bold text-sm">
              R
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
