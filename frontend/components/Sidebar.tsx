"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageCircle, BarChart3, Zap, Settings } from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Chat", href: "/chat", icon: MessageCircle },
    { name: "Dashboard", href: "/dashboard", icon: BarChart3 },
    { name: "Agents", href: "/agents", icon: Zap },
  ];

  return (
    <aside className="w-64 bg-gradient-to-b from-slate-900 to-slate-800 border-r border-purple-500/20 flex flex-col">
      {/* Logo */}
      <Link href="/" className="p-6 border-b border-purple-500/20 hover:bg-slate-800/50 transition-all duration-200 cursor-pointer">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center">
            <span className="text-white font-bold text-sm">AR</span>
          </div>
          <div>
            <h1 className="font-bold text-lg bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              A.R.E.S.
            </h1>
            <p className="text-xs text-gray-400">Research System</p>
          </div>
        </div>
      </Link>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? "bg-gradient-to-r from-purple-600/50 to-pink-600/50 text-white border border-purple-400/30 shadow-lg shadow-purple-500/20"
                  : "text-gray-400 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Settings */}
      <div className="p-4 border-t border-purple-500/20 space-y-2">
        <button className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-slate-700/50 transition-all duration-200">
          <Settings size={20} />
          <span className="font-medium">Settings</span>
        </button>
      </div>
    </aside>
  );
}
