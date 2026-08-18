"use client";

import { useState, useEffect } from "react";
import { Activity, Zap, BarChart3, FileText } from "lucide-react";

interface Agent {
  name: string;
  status: "idle" | "processing" | "complete" | "error";
  progress: number;
  lastActivity: string;
  icon: any;
}

export default function AgentStatus() {
  const [agents, setAgents] = useState<Agent[]>([
    {
      name: "Orchestrator",
      status: "idle",
      progress: 0,
      lastActivity: "Waiting for query",
      icon: Zap,
    },
    {
      name: "Scraper",
      status: "idle",
      progress: 0,
      lastActivity: "Ready to collect data",
      icon: FileText,
    },
    {
      name: "EDA Agent",
      status: "idle",
      progress: 0,
      lastActivity: "Ready to analyze",
      icon: BarChart3,
    },
    {
      name: "Synthesizer",
      status: "idle",
      progress: 0,
      lastActivity: "Ready to compile",
      icon: Activity,
    },
  ]);

  // Simulate agent activity
  useEffect(() => {
    const interval = setInterval(() => {
      setAgents((prev) =>
        prev.map((agent) => ({
          ...agent,
          status: ["idle", "processing", "complete"][Math.floor(Math.random() * 3)] as any,
          progress: Math.random() * 100,
          lastActivity: `Updated ${new Date().toLocaleTimeString()}`,
        }))
      );
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "processing":
        return "bg-blue-500";
      case "complete":
        return "bg-green-500";
      case "error":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  const getStatusBgColor = (status: string) => {
    switch (status) {
      case "processing":
        return "bg-blue-500/10 border-blue-500/30";
      case "complete":
        return "bg-green-500/10 border-green-500/30";
      case "error":
        return "bg-red-500/10 border-red-500/30";
      default:
        return "bg-gray-500/10 border-gray-500/30";
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h3 className="font-bold text-lg flex items-center space-x-2">
        <Activity size={20} className="text-purple-400" />
        <span>Agent Status</span>
      </h3>

      <div className="space-y-3">
        {agents.map((agent) => {
          const Icon = agent.icon;
          return (
            <div
              key={agent.name}
              className={`p-4 rounded-lg border transition-all ${getStatusBgColor(
                agent.status
              )}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <Icon size={18} className="text-purple-400" />
                  <span className="font-semibold text-sm">{agent.name}</span>
                </div>
                <span
                  className={`text-xs px-2 py-1 rounded-full text-white ${getStatusColor(
                    agent.status
                  )}`}
                >
                  {agent.status}
                </span>
              </div>

              {/* Progress Bar */}
              <div className="mb-2">
                <div className="bg-slate-700/50 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${getStatusColor(
                      agent.status
                    )}`}
                    style={{ width: `${agent.progress}%` }}
                  />
                </div>
              </div>

              <p className="text-xs text-gray-400">{agent.lastActivity}</p>
            </div>
          );
        })}
      </div>

      {/* Stats */}
      <div className="pt-4 border-t border-purple-500/20">
        <h4 className="text-sm font-semibold mb-3 text-gray-300">Performance</h4>
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-gray-400">Active Agents</span>
            <span className="text-green-400 font-semibold">
              {agents.filter((a) => a.status !== "idle").length}/
              {agents.length}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Avg. Response Time</span>
            <span className="text-blue-400 font-semibold">~2.4s</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-400">Success Rate</span>
            <span className="text-purple-400 font-semibold">98.5%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
