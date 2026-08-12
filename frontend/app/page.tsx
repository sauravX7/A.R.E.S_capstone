"use client";

import { useState, useEffect } from "react";
import { checkHealth, sendChatMessage } from "@/lib/api";

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<string>("Checking...");
  const [chatResponse, setChatResponse] = useState<string>("");
  const [message, setMessage] = useState<string>("Hello, A.R.E.S!");
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    async function getHealth() {
      const res = await checkHealth();
      setHealthStatus(res ? `Backend is ${res.status}` : "Backend is offline");
    }
    getHealth();
  }, []);

  const handleSend = async () => {
    setLoading(true);
    const res = await sendChatMessage(message);
    setChatResponse(res ? res.response : "Error communicating with backend");
    setLoading(false);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50 text-gray-900">
      <div className="z-10 max-w-2xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">A.R.E.S. Capstone</h1>
        
        <div className="bg-white shadow rounded-lg p-6 mb-8 border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          <div className="flex items-center space-x-2">
            <span className={`h-3 w-3 rounded-full ${healthStatus.includes('ok') ? 'bg-green-500' : 'bg-red-500'}`}></span>
            <span>{healthStatus}</span>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6 border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Test LLM Connection</h2>
          
          <div className="flex flex-col space-y-4">
            <input 
              type="text" 
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="border border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Send a message to Ollama..."
            />
            
            <button 
              onClick={handleSend}
              disabled={loading || !healthStatus.includes('ok')}
              className="bg-blue-600 text-white rounded p-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? "Sending..." : "Send to LangGraph"}
            </button>
            
            {chatResponse && (
              <div className="mt-4 p-4 bg-gray-100 rounded border border-gray-200">
                <p className="font-semibold text-gray-700 mb-1">Response:</p>
                <p className="whitespace-pre-wrap">{chatResponse}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
