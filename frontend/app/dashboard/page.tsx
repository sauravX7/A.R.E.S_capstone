"use client";

import { useState } from "react";
import { BarChart3, TrendingUp, FileText, Database, Download } from "lucide-react";

export default function DashboardPage() {
  const [selectedAnalysis, setSelectedAnalysis] = useState<string | null>(null);

  const analysisResults = [
    {
      id: 1,
      title: "E-commerce Market Trends",
      date: "2024-08-18",
      dataPoints: 1250,
      confidence: 92,
      summary: "Analysis of top 100 e-commerce platforms",
    },
    {
      id: 2,
      title: "AI Industry Growth",
      date: "2024-08-17",
      dataPoints: 845,
      confidence: 88,
      summary: "Quarterly growth metrics in AI sector",
    },
    {
      id: 3,
      title: "Social Media Analytics",
      date: "2024-08-16",
      dataPoints: 2104,
      confidence: 95,
      summary: "Cross-platform engagement patterns",
    },
  ];

  const stats = [
    { label: "Total Analyses", value: "24", icon: BarChart3, color: "from-purple-600 to-pink-600" },
    { label: "Data Points", value: "4,199", icon: Database, color: "from-blue-600 to-purple-600" },
    { label: "Avg Confidence", value: "91.7%", icon: TrendingUp, color: "from-pink-600 to-orange-600" },
    { label: "Reports", value: "12", icon: FileText, color: "from-green-600 to-teal-600" },
  ];

  return (
    <div className="flex-1 h-full min-h-0 flex flex-col overflow-hidden bg-slate-950">
      {/* Header */}
      <header className="flex-shrink-0 px-6 py-4 border-b border-purple-500/20 bg-gradient-to-r from-slate-900/50 to-purple-900/20">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <p className="text-sm text-gray-400 mt-1">View your analyses and research insights</p>
      </header>

      {/* Content */}
      <div className="flex-1 min-h-0 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-purple-500/20">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div
                key={index}
                className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-purple-500/20 rounded-lg p-6 hover:border-purple-400/40 transition-all duration-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color}`}>
                    <Icon size={20} className="text-white" />
                  </div>
                </div>
                <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                <p className="text-3xl font-bold">{stat.value}</p>
              </div>
            );
          })}
        </div>

        {/* Analysis Results */}
        <div>
          <h3 className="text-xl font-bold mb-4 flex items-center space-x-2">
            <BarChart3 size={24} className="text-purple-400" />
            <span>Recent Analyses</span>
          </h3>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {analysisResults.map((analysis) => (
              <div
                key={analysis.id}
                onClick={() => setSelectedAnalysis(analysis.id.toString())}
                className={`p-6 rounded-lg border cursor-pointer transition-all duration-200 ${
                  selectedAnalysis === analysis.id.toString()
                    ? "bg-gradient-to-br from-purple-600/20 to-pink-600/20 border-purple-400/50 shadow-lg shadow-purple-500/20"
                    : "bg-slate-800/30 border-purple-500/20 hover:border-purple-400/30"
                }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-semibold text-white">{analysis.title}</h4>
                  <span className="text-xs px-2 py-1 rounded-full bg-green-500/20 text-green-400">
                    Complete
                  </span>
                </div>
                <p className="text-sm text-gray-400 mb-4">{analysis.summary}</p>
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-500">Data Points</span>
                    <span className="text-sm font-semibold text-blue-400">{analysis.dataPoints}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-500">Confidence</span>
                    <span className="text-sm font-semibold text-green-400">{analysis.confidence}%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between pt-3 border-t border-purple-500/20">
                  <span className="text-xs text-gray-400">{analysis.date}</span>
                  <Download size={16} className="text-purple-400 cursor-pointer hover:text-purple-300" />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Detailed View */}
        {selectedAnalysis && (
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-purple-500/20 rounded-lg p-6">
            <h3 className="text-lg font-bold mb-4">Analysis Details</h3>
            
            {/* Chart Placeholder */}
            <div className="h-72 bg-slate-700/30 rounded-lg flex items-center justify-center border border-purple-500/10 mb-6">
              <div className="text-center">
                <BarChart3 size={48} className="text-purple-400/30 mx-auto mb-2" />
                <p className="text-gray-400">Chart visualization would appear here</p>
              </div>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-3 gap-4">
              <div className="p-4 bg-slate-800/50 rounded-lg border border-purple-500/10">
                <p className="text-sm text-gray-400">Total Records</p>
                <p className="text-2xl font-bold text-blue-400 mt-1">1,250</p>
              </div>
              <div className="p-4 bg-slate-800/50 rounded-lg border border-purple-500/10">
                <p className="text-sm text-gray-400">Processing Time</p>
                <p className="text-2xl font-bold text-purple-400 mt-1">2.4s</p>
              </div>
              <div className="p-4 bg-slate-800/50 rounded-lg border border-purple-500/10">
                <p className="text-sm text-gray-400">Quality Score</p>
                <p className="text-2xl font-bold text-green-400 mt-1">94%</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
