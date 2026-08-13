import React from 'react';

interface FindingsListProps {
  findings: string[];
}

export default function FindingsList({ findings }: FindingsListProps) {
  if (!findings || findings.length === 0) return null;

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-3 border-b border-gray-200 pb-2">Key Findings</h3>
      <ul className="list-disc pl-5 space-y-2 text-gray-700">
        {findings.map((finding, index) => (
          <li key={index} className="leading-relaxed">{finding}</li>
        ))}
      </ul>
    </div>
  );
}
