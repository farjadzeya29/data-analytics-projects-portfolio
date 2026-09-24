import React, { useState } from 'react';
import { Terminal, Copy, Check, FileCode, CheckCircle2, Cpu, BarChart2 } from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface PythonPipelineViewProps {
  project: ProjectMeta;
}

export const PythonPipelineView: React.FC<PythonPipelineViewProps> = ({ project }) => {
  const [selectedFileIndex, setSelectedFileIndex] = useState(0);
  const [copied, setCopied] = useState(false);

  const currentFile = project.pythonFiles[selectedFileIndex] || project.pythonFiles[0];

  const handleCopy = () => {
    navigator.clipboard.writeText(currentFile.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <Terminal className="w-3.5 h-3.5" />
            <span>Python Pipeline & Analytical Algorithms</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            pandas, NumPy & Matplotlib Analytics Workflow
          </h2>
        </div>

        {/* Script Selector Tabs */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-md text-xs">
          {project.pythonFiles.map((f, idx) => (
            <button
              key={f.name}
              onClick={() => setSelectedFileIndex(idx)}
              className={`px-3 py-1.5 rounded text-xs font-mono font-medium transition-colors ${
                selectedFileIndex === idx
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {f.name}
            </button>
          ))}
        </div>
      </div>

      {/* Methodology & Analytical Logic Explanation */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-2">
          <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-blue-500"></span>
            <span>Step 1: Data Ingestion & Hygiene</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Eliminates duplicate tracking keys, coerces corrupted negative values (e.g. negative age, negative freight weight), and standardizes inconsistent text casing.
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-2">
          <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Step 2: Feature Engineering</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            {project.number === 1 && "Computes Days Since Last Purchase (Recency), Total Transactions (Frequency), and Cumulative Spend (Monetary Value)."}
            {project.number === 2 && "Engineers composite Retention Risk Score combining inactivity penalties, multi-product hazard weights, and high-balance exposure."}
            {project.number === 3 && "Computes dispatch latency (actual_ship - scheduled_ship), transit duration, and delivery delay days."}
            {project.number === 4 && "Evaluates multi-stage transition flags, sales cycle durations (days to close), and unit CAC/ROAS benchmarks."}
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-2">
          <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-purple-500"></span>
            <span>Step 3: Statistical Modeling</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            {project.number === 1 && "Applies pandas qcut quantiles (1 to 5) to categorize customers into Champions, Loyal, At-Risk, and Lost cohorts."}
            {project.number === 2 && "Identifies statistically significant churn disparities across tenure cohorts and account balance quartiles."}
            {project.number === 3 && "Calculates network-wide On-Time Delivery (OTD %) benchmarks and origin hub dispatch efficiency."}
            {project.number === 4 && "Maps 6-stage lead conversion drop-offs and ranks marketing acquisition channels by Net ROI."}
          </p>
        </div>
      </div>

      {/* Code Editor Display */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden text-white shadow-sm">
        <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
            <FileCode className="w-3.5 h-3.5 text-emerald-400" />
            <span className="font-semibold text-white">{currentFile.name}</span>
            <span className="text-slate-500">·</span>
            <span className="text-slate-400">{currentFile.description}</span>
          </div>

          <button
            onClick={handleCopy}
            className="bg-slate-700 hover:bg-slate-600 text-slate-200 px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center gap-1 border border-slate-600"
            title="Copy Python script"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Python'}</span>
          </button>
        </div>

        {/* Code View */}
        <div className="p-4 max-h-96 overflow-y-auto font-mono text-xs text-slate-300 leading-relaxed scrollbar-thin scrollbar-thumb-slate-700">
          <pre className="whitespace-pre-wrap">{currentFile.content}</pre>
        </div>
      </div>
    </div>
  );
};
