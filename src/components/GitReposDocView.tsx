import React, { useState } from 'react';
import { FileText, Copy, Check, Terminal, Folder, ExternalLink, Code } from 'lucide-react';
import { ROOT_PORTFOLIO_README, PROJECTS_DATA } from '../data/portfolioData';

export const GitReposDocView: React.FC = () => {
  const [copied, setCopied] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<'readme' | 'setup'>('readme');

  const handleCopyReadme = () => {
    navigator.clipboard.writeText(ROOT_PORTFOLIO_README);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <FileText className="w-3.5 h-3.5" />
            <span>Root Documentation & Git Repositories</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            Production Portfolio Architecture & Execution Guide
          </h2>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-md text-xs">
            <button
              onClick={() => setSelectedDoc('readme')}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                selectedDoc === 'readme' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              PORTFOLIO_README.md
            </button>
            <button
              onClick={() => setSelectedDoc('setup')}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                selectedDoc === 'setup' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Local Setup Guide
            </button>
          </div>

          <button
            onClick={handleCopyReadme}
            className="bg-slate-900 hover:bg-slate-800 text-white px-3 py-1.5 rounded text-xs font-semibold transition-colors flex items-center gap-1.5"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy README'}</span>
          </button>
        </div>
      </div>

      {selectedDoc === 'readme' ? (
        <div className="bg-white border border-slate-200 rounded-lg p-6 sm:p-8 space-y-4 shadow-xs">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 text-xs text-slate-500 font-mono">
            <span>/PORTFOLIO_README.md</span>
            <span>Markdown Format</span>
          </div>

          <pre className="font-sans text-xs text-slate-800 whitespace-pre-wrap leading-relaxed bg-slate-50/80 p-6 rounded-lg border border-slate-200">
            {ROOT_PORTFOLIO_README}
          </pre>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-3">
            <h3 className="text-sm font-bold text-slate-900">
              How to Run Any Project's Streamlit Dashboard
            </h3>
            <p className="text-xs text-slate-600">
              Each project in the portfolio is completely independent with its own Python virtual environment requirements, scripts, and Streamlit app.
            </p>

            <div className="bg-slate-900 text-slate-200 p-4 rounded-lg font-mono text-xs space-y-2">
              <div className="text-slate-500"># 1. Clone repository and choose project directory</div>
              <div className="text-emerald-400">git clone https://github.com/farjadzeya/data-analyst-portfolio.git</div>
              <div className="text-emerald-400">cd projects/01-ecommerce-customer-sales-analytics</div>
              <div className="text-slate-500 pt-2"># 2. Create isolated virtual environment</div>
              <div className="text-blue-300">python -m venv .venv && source .venv/bin/activate</div>
              <div className="text-slate-500 pt-2"># 3. Install dependencies and run pipeline</div>
              <div className="text-blue-300">pip install -r requirements.txt</div>
              <div className="text-blue-300">python src/data_cleaning.py</div>
              <div className="text-blue-300">python src/analysis.py</div>
              <div className="text-slate-500 pt-2"># 4. Launch interactive browser dashboard</div>
              <div className="text-amber-400 font-bold">streamlit run streamlit_app.py</div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {PROJECTS_DATA.map((p) => (
              <div key={p.id} className="bg-white border border-slate-200 rounded-lg p-4 space-y-2">
                <div className="text-xs font-bold text-slate-900">
                  Project {p.number}: {p.shortTitle}
                </div>
                <div className="text-xs font-mono text-slate-500 bg-slate-50 p-2 rounded border border-slate-200">
                  cd projects/{p.id} && streamlit run streamlit_app.py
                </div>
                <div className="text-[11px] text-slate-600">
                  Tech: {p.tech.join(' · ')}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
