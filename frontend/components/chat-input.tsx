import React, { KeyboardEvent } from 'react';

interface ChatInputProps {
  message: string;
  setMessage: (msg: string) => void;
  onSend: () => void;
  disabled: boolean;
}

export default function ChatInput({ message, setMessage, onSend, disabled }: ChatInputProps) {
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Ctrl+Enter or Cmd+Enter to allow regular multiline with Enter
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (!disabled && message.trim()) {
        onSend();
      }
    }
  };

  return (
    <div className="flex flex-col space-y-3 w-full bg-white p-4 rounded-lg shadow-sm border border-gray-200">
      <label htmlFor="chat-input" className="sr-only">
        Research Request
      </label>
      <textarea
        id="chat-input"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        className="w-full min-h-[100px] border border-gray-300 rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y text-gray-800"
        placeholder="Enter your research or analysis request..."
        disabled={disabled}
        aria-label="Research request input"
      />
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span>Press <kbd className="bg-gray-100 rounded px-1">Ctrl</kbd> + <kbd className="bg-gray-100 rounded px-1">Enter</kbd> to submit</span>
        <button
          onClick={onSend}
          disabled={disabled || !message.trim()}
          className="bg-blue-600 text-white font-medium rounded-md px-6 py-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-label="Submit request"
        >
          {disabled ? "Processing..." : "Submit"}
        </button>
      </div>
    </div>
  );
}
