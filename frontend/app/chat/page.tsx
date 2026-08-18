"use client";

import { useState, useEffect, useRef } from "react";
import { checkHealth, sendChatMessage } from "@/lib/api";
import { Send, RotateCcw, Sparkles } from "lucide-react";
import AgentStatus from "@/components/AgentStatus";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  agentInfo?: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [healthStatus, setHealthStatus] = useState<string>("Checking...");
  const [showAgentStatus, setShowAgentStatus] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check backend health on mount
  useEffect(() => {
    async function getHealth() {
      const res = await checkHealth();
      setHealthStatus(res ? "Connected" : "Offline");
    }
    getHealth();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChatMessage(input);
      
      let messageContent = "Error communicating with backend";
      if (res.success) {
        messageContent = res.data.answer;
        // Optionally append warnings or findings to the UI if present
        if (res.data.warnings && res.data.warnings.length > 0) {
           messageContent += "\n\n⚠️ Warnings:\n- " + res.data.warnings.join("\n- ");
        }
      } else {
        messageContent = `Error: ${res.error}`;
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: messageContent,
        timestamp: new Date(),
        agentInfo: "A.R.E.S. Core",
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setInput("");
  };

  return (
    <div className="flex-1 flex overflow-hidden">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-slate-950">
        {/* Header */}
        <header className="px-6 py-4 border-b border-purple-500/20 flex items-center justify-between bg-gradient-to-r from-slate-900/50 to-purple-900/20">
          <div className="flex items-center space-x-3">
            <Sparkles className="text-purple-400" size={24} />
            <div>
              <h2 className="font-bold text-lg">Research Assistant</h2>
              <p className="text-xs text-gray-400">
                Status: <span className={healthStatus === "Connected" ? "text-green-400" : "text-red-400"}>
                  {healthStatus}
                </span>
              </p>
            </div>
          </div>
          <button
            onClick={handleClearChat}
            className="p-2 rounded-lg bg-slate-800/50 hover:bg-slate-700 text-gray-400 hover:text-white transition-colors"
            title="Clear chat"
          >
            <RotateCcw size={20} />
          </button>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-thin scrollbar-thumb-purple-500/20">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center opacity-50">
                <Sparkles size={32} />
              </div>
              <div className="text-center">
                <h3 className="text-xl font-semibold">Welcome to A.R.E.S.</h3>
                <p className="text-gray-400 mt-2">
                  Ask me anything about research, data analysis, or web scraping
                </p>
              </div>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-2xl px-4 py-3 rounded-2xl ${
                    message.role === "user"
                      ? "bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-br-none"
                      : "bg-slate-800/50 text-gray-100 border border-purple-500/20 rounded-bl-none"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  {message.agentInfo && message.role === "assistant" && (
                    <p className="text-xs text-gray-400 mt-2">
                      {message.agentInfo}
                    </p>
                  )}
                  <p className="text-xs text-gray-400 mt-1">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-800/50 text-gray-100 border border-purple-500/20 px-4 py-3 rounded-2xl rounded-bl-none">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                  <div className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="px-6 py-4 border-t border-purple-500/20 bg-gradient-to-t from-slate-950 to-slate-900/50">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask A.R.E.S. anything..."
              disabled={loading}
              className="flex-1 bg-slate-800/50 border border-purple-500/30 rounded-full px-6 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-400/50 focus:ring-2 focus:ring-purple-400/20 transition-all disabled:opacity-50"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-full p-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-purple-500/20"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>

      {/* Agent Status Sidebar */}
      {showAgentStatus && (
        <div className="w-80 border-l border-purple-500/20 overflow-y-auto bg-gradient-to-b from-slate-900 to-slate-800">
          <AgentStatus />
        </div>
      )}
    </div>
  );
}
