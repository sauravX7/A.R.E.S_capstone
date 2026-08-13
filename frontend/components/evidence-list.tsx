import React from 'react';

interface EvidenceListProps {
  artifacts: string[];
}

export default function EvidenceList({ artifacts }: EvidenceListProps) {
  if (!artifacts || artifacts.length === 0) return null;

  return (
    <div className="mt-6 bg-gray-50 p-4 rounded-md border border-gray-200">
      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3">Supporting Evidence / Artifacts</h3>
      <div className="flex flex-wrap gap-2">
        {artifacts.map((artifactId, index) => (
          <span 
            key={index} 
            className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200 font-mono"
            title={`Artifact ID: ${artifactId}`}
          >
            {artifactId}
          </span>
        ))}
      </div>
    </div>
  );
}
