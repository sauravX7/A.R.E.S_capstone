"use client";

import { useRouter } from "next/navigation";
import { ArrowRight, Sparkles, Zap } from "lucide-react";

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen w-full bg-gradient-to-b from-slate-950 via-purple-950 to-slate-900 flex items-center justify-center overflow-hidden relative">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Gradient Orb 1 */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-float"></div>
        {/* Gradient Orb 2 */}
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl animate-float" style={{ animationDelay: "1s" }}></div>
      </div>

      {/* Content */}
      <div className="relative z-10 text-center px-6 max-w-4xl mx-auto">
        {/* Logo/Icon */}
        <div className="mb-8 inline-block">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-2xl shadow-purple-500/50 animate-fadeInUp">
            <Sparkles size={40} className="text-white" />
          </div>
        </div>

        {/* Main Headline */}
        <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-slideInUp">
          <span className="bg-gradient-to-r from-purple-300 via-pink-300 to-purple-300 bg-clip-text text-transparent">
            A.R.E.S.
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-gray-300 mb-4 animate-slideInUp" style={{ animationDelay: "0.1s" }}>
          Autonomous Research & Analysis System
        </p>

        {/* Tagline */}
        <p className="text-sm md:text-base text-purple-300 mb-6 font-semibold animate-slideInUp" style={{ animationDelay: "0.15s" }}>
          A YAML-driven Hierarchical Orchestrator-Worker Architecture for Deep Research & EDA
        </p>

        {/* Description */}
        <p className="text-base md:text-lg text-gray-400 mb-6 max-w-3xl mx-auto animate-slideInUp" style={{ animationDelay: "0.2s" }}>
          Automating complex research and exploratory data analysis tasks through a scalable multi-agent system. 
          From web scraping to statistical analysis and synthesized reports—all orchestrated seamlessly.
        </p>

        {/* Problem & Solution */}
        <div className="max-w-3xl mx-auto mb-8 p-6 bg-gradient-to-r from-purple-900/20 to-pink-900/20 border border-purple-500/30 rounded-xl animate-slideInUp" style={{ animationDelay: "0.25s" }}>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-bold text-purple-300 mb-2">🎯 The Problem</h3>
              <p className="text-sm text-gray-300">Manual research and EDA are highly repetitive, time-consuming tasks. Current singular LLMs struggle with multi-step workflows.</p>
            </div>
            <div>
              <h3 className="text-sm font-bold text-pink-300 mb-2">💡 The Solution</h3>
              <p className="text-sm text-gray-300">A robust multi-agent system that automates the pipeline from web scraping to statistical analysis and report synthesis.</p>
            </div>
          </div>
        </div>

        {/* CTA Button */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slideInUp" style={{ animationDelay: "0.3s" }}>
          <button
            onClick={() => router.push("/chat")}
            className="group relative px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white font-semibold rounded-xl transition-all duration-300 shadow-xl shadow-purple-500/30 hover:shadow-2xl hover:shadow-purple-400/50 flex items-center space-x-2"
          >
            <span>Start Research</span>
            <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
          </button>

          <a
            href="#features"
            className="px-8 py-4 bg-slate-800/50 hover:bg-slate-700 text-gray-300 hover:text-white font-semibold rounded-xl border border-purple-500/30 transition-all duration-300 flex items-center space-x-2"
          >
            <span>Learn More</span>
            <Zap size={20} />
          </a>
        </div>

        {/* Agent Architecture Section */}
        <div className="mt-12 max-w-4xl mx-auto animate-slideInUp" style={{ animationDelay: "0.35s" }}>
          <h3 className="text-center text-lg font-bold text-white mb-6">🏗️ Multi-Agent Architecture</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 bg-gradient-to-br from-blue-900/30 to-slate-900/30 border border-blue-500/30 rounded-lg">
              <div className="text-2xl mb-2">🎯</div>
              <h4 className="font-semibold text-blue-300 mb-2">Orchestrator</h4>
              <p className="text-xs text-gray-400">Routes queries to appropriate agents based on analysis requirements</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-green-900/30 to-slate-900/30 border border-green-500/30 rounded-lg">
              <div className="text-2xl mb-2">🕷️</div>
              <h4 className="font-semibold text-green-300 mb-2">Scraper Agent</h4>
              <p className="text-xs text-gray-400">Fetches and extracts data from web sources with precision</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-purple-900/30 to-slate-900/30 border border-purple-500/30 rounded-lg">
              <div className="text-2xl mb-2">📊</div>
              <h4 className="font-semibold text-purple-300 mb-2">EDA Agent</h4>
              <p className="text-xs text-gray-400">Performs exploratory data analysis and statistical computations</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-orange-900/30 to-slate-900/30 border border-orange-500/30 rounded-lg">
              <div className="text-2xl mb-2">📝</div>
              <h4 className="font-semibold text-orange-300 mb-2">Synthesizer</h4>
              <p className="text-xs text-gray-400">Compiles findings into comprehensive data-backed reports</p>
            </div>
          </div>
        </div>

        {/* Feature Pills */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 animate-slideInUp" style={{ animationDelay: "0.4s" }}>
          <div className="p-6 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-purple-500/20 rounded-xl backdrop-blur-sm hover:border-purple-400/40 transition-all">
            <div className="text-2xl mb-3">�️</div>
            <h3 className="font-semibold text-white mb-2">Web Scraping</h3>
            <p className="text-sm text-gray-400">Automated data collection from web sources with intelligent extraction and normalization</p>
          </div>

          <div className="p-6 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-purple-500/20 rounded-xl backdrop-blur-sm hover:border-purple-400/40 transition-all">
            <div className="text-2xl mb-3">📈</div>
            <h3 className="font-semibold text-white mb-2">Statistical Analysis</h3>
            <p className="text-sm text-gray-400">Exploratory data analysis with comprehensive statistical insights and anomaly detection</p>
          </div>

          <div className="p-6 bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-purple-500/20 rounded-xl backdrop-blur-sm hover:border-purple-400/40 transition-all">
            <div className="text-2xl mb-3">🔒</div>
            <h3 className="font-semibold text-white mb-2">Private & Secure</h3>
            <p className="text-sm text-gray-400">Local LLM inference ensures sensitive data stays on your infrastructure</p>
          </div>
        </div>

        {/* Use Cases Section */}
        <div className="mt-16 max-w-4xl mx-auto animate-slideInUp" style={{ animationDelay: "0.45s" }}>
          <h3 className="text-center text-lg font-bold text-white mb-6">🚀 Real-World Applications</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-800/30 border border-purple-500/20 rounded-lg">
              <p className="font-semibold text-purple-300 mb-2">💼 Market Intelligence</p>
              <p className="text-xs text-gray-400">Automate competitive analysis by scraping competitor websites and generating comprehensive market trend reports</p>
            </div>
            <div className="p-4 bg-slate-800/30 border border-purple-500/20 rounded-lg">
              <p className="font-semibold text-pink-300 mb-2">📚 Academic Research</p>
              <p className="text-xs text-gray-400">Accelerate literature reviews by finding, summarizing, and cross-referencing academic papers on specific topics</p>
            </div>
            <div className="p-4 bg-slate-800/30 border border-purple-500/20 rounded-lg">
              <p className="font-semibold text-blue-300 mb-2">💰 Financial Analysis</p>
              <p className="text-xs text-gray-400">Extract data from quarterly reports, identify anomalies, and synthesize findings into investment summaries</p>
            </div>
            <div className="p-4 bg-slate-800/30 border border-purple-500/20 rounded-lg">
              <p className="font-semibold text-green-300 mb-2">🔐 Private Data Exploration</p>
              <p className="text-xs text-gray-400">Safely perform EDA on sensitive internal data without risking exposure to cloud APIs</p>
            </div>
          </div>
        </div>

        {/* Trust Badge */}
        <div className="mt-16 pt-8 border-t border-purple-500/20 animate-slideInUp" style={{ animationDelay: "0.5s" }}>
          <p className="text-gray-500 text-sm mb-4">Powered by Advanced AI Architecture</p>
          <div className="flex justify-center items-center space-x-8">
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-400">4</p>
              <p className="text-xs text-gray-400">Specialized Agents</p>
            </div>
            <div className="w-px h-8 bg-purple-500/20"></div>
            <div className="text-center">
              <p className="text-2xl font-bold text-pink-400">YAML</p>
              <p className="text-xs text-gray-400">Driven Config</p>
            </div>
            <div className="w-px h-8 bg-purple-500/20"></div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-400">Local</p>
              <p className="text-xs text-gray-400">LLM Inference</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
