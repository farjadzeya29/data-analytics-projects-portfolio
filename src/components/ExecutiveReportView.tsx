import React, { useState } from 'react';
import { FileText, Copy, Check, TrendingUp, Lightbulb, Target } from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface ExecutiveReportViewProps {
  project: ProjectMeta;
}

export const ExecutiveReportView: React.FC<ExecutiveReportViewProps> = ({ project }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(project.insightsMd);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <FileText className="w-3.5 h-3.5" />
            <span>Executive Briefing & Strategic Advisory</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            Stakeholder Insights & Commercial Recommendations
          </h2>
        </div>

        <button
          onClick={handleCopy}
          className="bg-slate-900 hover:bg-slate-800 text-white px-3 py-1.5 rounded text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-xs"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied to Clipboard' : 'Copy Full Report'}</span>
        </button>
      </div>

      {/* Structured Report View */}
      <div className="bg-white border border-slate-200 rounded-lg p-6 sm:p-8 space-y-6 text-slate-800 leading-relaxed">
        {/* Author Byline */}
        <div className="border-b border-slate-200 pb-4 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500">
          <div>
            <span className="font-semibold text-slate-800">Author:</span> Farjad Zeya (Data Analyst)
          </div>
          <div>
            <span className="font-semibold text-slate-800">Scope:</span> Analytical Insights & Executive Action Plan
          </div>
        </div>

        {/* Content Render */}
        <div className="prose prose-sm max-w-none text-xs text-slate-700 space-y-4">
          <pre className="font-sans text-xs text-slate-800 whitespace-pre-wrap leading-relaxed bg-slate-50/80 p-6 rounded-lg border border-slate-200">
            {project.insightsMd}
          </pre>
        </div>
      </div>
    </div>
  );
};
