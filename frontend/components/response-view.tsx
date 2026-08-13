import React from 'react';
import { ChatResponse } from '../lib/api/types';
import FindingsList from './findings-list';
import EvidenceList from './evidence-list';
import WarningList from './warning-list';

interface ResponseViewProps {
  response: ChatResponse | null;
  error: string | null;
  isLoading: boolean;
}

export default function ResponseView({ response, error, isLoading }: ResponseViewProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4" aria-live="polite">
        <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        <p className="text-gray-600 font-medium">A.R.E.S. is processing your request...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-md my-6" role="alert" aria-live="assertive">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!response) {
    return (
      <div className="text-center py-12 text-gray-400">
        <p>Submit a request above to begin analysis.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 my-6 transition-opacity duration-300">
      <div className="prose prose-blue max-w-none">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Synthesis & Answer</h2>
        <div className="text-gray-800 whitespace-pre-wrap leading-relaxed text-lg">
          {response.answer}
        </div>
      </div>

      <FindingsList findings={response.key_findings} />
      <EvidenceList artifacts={response.supporting_artifacts} />
      <WarningList warnings={response.warnings} />
    </div>
  );
}
