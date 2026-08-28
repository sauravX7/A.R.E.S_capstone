"use client";

import { useState } from "react";
import { Zap, BarChart3, FileText, Activity, Play, Pause, RotateCcw } from "lucide-react";

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState("orchestrator");

  const agents = [
    {
      id: "orchestrator",
      name: "Orchestrator",
      icon: Zap,
      description: "Routes queries to appropriate agents based on analysis",
      status: "active",
      tasks: 127,
      successRate: 98.5,
      avgTime: 0.8,
      role: "Main Coordinator",
    },
    {
      id: "scraper",
      name: "Scraper Agent",
      icon: FileText,
      description: "Fetches and extracts data from web sources",
      status: "active",
      tasks: 254,
      successRate: 96.2,
      avgTime: 2.4,
      role: "Data Collection",
    },
    {
      id: "eda",
      name: "EDA Agent",
      icon: BarChart3,
      description: "Performs exploratory data analysis and statistical computations",
      status: "idle",
      tasks: 89,
      successRate: 99.1,
      avgTime: 1.2,
      role: "Analysis",
    },
    {
      id: "synthesizer",
      name: "Synthesizer",
      icon: Activity,
      description: "Compiles findings into comprehensive reports",
      status: "active",
      tasks: 42,
      successRate: 97.6,
      avgTime: 3.1,
      role: "Report Generation",
    },
  ];

  const selectedAgentData = agents.find((a) => a.id === selectedAgent)!;
  const Icon = selectedAgentData.icon;

  const recentTasks = [
    { id: 1, name: "Query: Market Analysis", status: "completed", duration: 2.3 },
    { id: 2, name: "Data Collection: AI Trends", status: "completed", duration: 4.1 },
    { id: 3, name: "Statistical Analysis", status: "processing", duration: 1.5 },
    { id: 4, name: "Report Compilation", status: "pending", duration: 0 },
  ];

  return (
    <div className="flex-1 h-full min-h-0 flex overflow-hidden bg-slate-950">
      {/* Agents List */}
      <div className="w-80 h-full min-h-0 border-r border-purple-500/20 bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col">
        <div className="flex-shrink-0 px-6 py-4 border-b border-purple-500/20">
          <h2 className="text-xl font-bold">Agents</h2>
          <p className="text-sm text-gray-400 mt-1">Manage and monitor agents</p>
        </div>

        <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-2 scrollbar-thin scrollbar-thumb-purple-500/20">
          {agents.map((agent) => {
            const AgentIcon = agent.icon;
            const isSelected = agent.id === selectedAgent;
            return (
              <div
                key={agent.id}
                onClick={() => setSelectedAgent(agent.id)}
                className={`p-4 rounded-lg border cursor-pointer transition-all ${
                  isSelected
                    ? "bg-gradient-to-r from-purple-600/50 to-pink-600/50 border-purple-400/50"
                    : "bg-slate-800/30 border-purple-500/20 hover:border-purple-400/30"
                }`}
              >
                <div className="flex items-start space-x-3">
                  <div className="p-2 rounded-lg bg-slate-700/50">
                    <AgentIcon size={18} className="text-purple-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold">{agent.name}</h3>
                    <p className="text-xs text-gray-400 mt-1">{agent.role}</p>
                    <div className="flex items-center space-x-2 mt-2">
                      <span
                        className={`w-2 h-2 rounded-full ${
                          agent.status === "active" ? "bg-green-500" : "bg-gray-500"
                        }`}
                      ></span>
                      <span className="text-xs capitalize text-gray-400">
                        {agent.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Agent Details */}
      <div className="flex-1 h-full min-h-0 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex-shrink-0 px-6 py-4 border-b border-purple-500/20 bg-gradient-to-r from-slate-900/50 to-purple-900/20">
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-4">
              <div className="p-3 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600">
                <Icon size={24} className="text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">{selectedAgentData.name}</h2>
                <p className="text-sm text-gray-400 mt-1">
                  {selectedAgentData.description}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button className="p-2 rounded-lg bg-slate-800/50 hover:bg-slate-700 text-gray-400 hover:text-white transition-colors">
                <Play size={18} />
              </button>
              <button className="p-2 rounded-lg bg-slate-800/50 hover:bg-slate-700 text-gray-400 hover:text-white transition-colors">
                <Pause size={18} />
              </button>
              <button className="p-2 rounded-lg bg-slate-800/50 hover:bg-slate-700 text-gray-400 hover:text-white transition-colors">
                <RotateCcw size={18} />
              </button>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 min-h-0 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-purple-500/20">
          {/* Metrics */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-purple-500/20 rounded-lg p-6">
              <p className="text-gray-400 text-sm mb-2">Total Tasks</p>
              <p className="text-4xl font-bold text-blue-400">
                {selectedAgentData.tasks}
              </p>
              <p className="text-xs text-gray-500 mt-2">processed successfully</p>
            </div>
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-purple-500/20 rounded-lg p-6">
              <p className="text-gray-400 text-sm mb-2">Success Rate</p>
              <p className="text-4xl font-bold text-green-400">
                {selectedAgentData.successRate}%
              </p>
              <p className="text-xs text-gray-500 mt-2">task completion rate</p>
            </div>
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-purple-500/20 rounded-lg p-6">
              <p className="text-gray-400 text-sm mb-2">Avg Response</p>
              <p className="text-4xl font-bold text-purple-400">
                {selectedAgentData.avgTime}s
              </p>
              <p className="text-xs text-gray-500 mt-2">average execution time</p>
            </div>
          </div>

          {/* Recent Tasks */}
          <div>
            <h3 className="text-lg font-bold mb-4">Recent Tasks</h3>
            <div className="space-y-3">
              {recentTasks.map((task) => (
                <div
                  key={task.id}
                  className="p-4 bg-slate-800/30 border border-purple-500/20 rounded-lg flex items-center justify-between hover:border-purple-400/30 transition-colors"
                >
                  <div className="flex-1">
                    <p className="font-medium">{task.name}</p>
                    {task.duration > 0 && (
                      <p className="text-sm text-gray-400 mt-1">
                        Duration: {task.duration}s
                      </p>
                    )}
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      task.status === "completed"
                        ? "bg-green-500/20 text-green-400"
                        : task.status === "processing"
                        ? "bg-blue-500/20 text-blue-400"
                        : "bg-gray-500/20 text-gray-400"
                    }`}
                  >
                    {task.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Configuration */}
          <div>
            <h3 className="text-lg font-bold mb-4">Configuration</h3>
            <div className="bg-slate-800/30 border border-purple-500/20 rounded-lg p-6 space-y-4">
              <div>
                <label className="text-sm text-gray-400">Timeout (seconds)</label>
                <input
                  type="number"
                  defaultValue="30"
                  className="w-full mt-2 bg-slate-700 border border-purple-500/20 rounded px-3 py-2 text-white focus:outline-none focus:border-purple-400/50"
                />
              </div>
              <div>
                <label className="text-sm text-gray-400">Max Retries</label>
                <input
                  type="number"
                  defaultValue="3"
                  className="w-full mt-2 bg-slate-700 border border-purple-500/20 rounded px-3 py-2 text-white focus:outline-none focus:border-purple-400/50"
                />
              </div>
              <button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-lg py-2 font-semibold transition-all">
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
