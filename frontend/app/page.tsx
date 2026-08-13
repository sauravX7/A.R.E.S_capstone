"use client";

import { useState, useEffect } from "react";
import { checkHealth, sendChatMessage } from "@/lib/api";
import { ChatResponse } from "@/lib/api/types";
import ChatInput from "@/components/chat-input";
import ResponseView from "@/components/response-view";

export default function Home() {
  const [healthStatus, setHealthStatus] = useState<string>("Checking...");
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [chatResponse, setChatResponse] = useState<ChatResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function getHealth() {
      const res = await checkHealth();
      setHealthStatus(res ? `Backend is Connected` : "Backend is Offline");
    }
    getHealth();
  }, []);

  const handleSend = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    setError(null);
    setChatResponse(null);
    
    const result = await sendChatMessage(message);
    
    if (result.success) {
      setChatResponse(result.data);
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900 font-sans selection:bg-blue-200">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <h1 className="text-xl font-bold tracking-tight text-gray-900">A.R.E.S.</h1>
            <span className="text-sm text-gray-500 hidden sm:inline-block">| Advanced Research & Execution System</span>
          </div>
          <div className="flex items-center space-x-2 text-sm" aria-label="Backend status">
            <span className={`h-2.5 w-2.5 rounded-full ${healthStatus.includes('Connected') ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]' : 'bg-red-500'}`} aria-hidden="true"></span>
            <span className="font-medium text-gray-600">{healthStatus}</span>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="space-y-8">
          <section aria-labelledby="input-heading">
            <h2 id="input-heading" className="sr-only">Research Input</h2>
            <ChatInput 
              message={message} 
              setMessage={setMessage} 
              onSend={handleSend} 
              disabled={loading || healthStatus.includes('Offline')} 
            />
          </section>

          <section aria-labelledby="results-heading">
            <h2 id="results-heading" className="sr-only">Analysis Results</h2>
            <ResponseView 
              response={chatResponse} 
              error={error} 
              isLoading={loading} 
            />
          </section>
        </div>
      </div>
    </main>
  );
}
