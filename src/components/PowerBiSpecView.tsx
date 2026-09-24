import React, { useState } from 'react';
import { BarChart3, Copy, Check, FileSpreadsheet, Layers, CheckCircle2, BookOpen } from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface PowerBiSpecViewProps {
  project: ProjectMeta;
}

export const PowerBiSpecView: React.FC<PowerBiSpecViewProps> = ({ project }) => {
  const [copiedDax, setCopiedDax] = useState(false);
  const [viewMode, setViewMode] = useState<'powerbi' | 'excel'>('powerbi');

  const handleCopyDax = () => {
    navigator.clipboard.writeText(project.daxMeasures);
    setCopiedDax(true);
    setTimeout(() => setCopiedDax(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Power BI Architecture & DAX Calculation Engine</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            Data Modeling, Relationships & Measures Library
          </h2>
        </div>

        {/* View Mode Toggle (for Supply Chain which has Excel MIS) */}
        {project.excelGuide && (
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-md text-xs">
            <button
              onClick={() => setViewMode('powerbi')}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                viewMode === 'powerbi' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Power BI & DAX Spec
            </button>
            <button
              onClick={() => setViewMode('excel')}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center gap-1.5 ${
                viewMode === 'excel' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-600" />
              <span>Excel MIS Model</span>
            </button>
          </div>
        )}
      </div>

      {viewMode === 'powerbi' ? (
        <>
          {/* Data Model & Star Schema Overview */}
          <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-blue-600" />
                <span>Star Schema Data Model Architecture</span>
              </h3>
              <span className="text-[11px] text-slate-500 font-mono">1:Many (*:1) Single Direction Filtering</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-50 border border-slate-200 rounded p-3.5 space-y-2">
                <div className="text-xs font-bold text-slate-900">Central Fact Table</div>
                <div className="text-xs font-mono text-blue-700 bg-white p-1.5 rounded border border-slate-200">
                  {project.number === 1 && "Fact_EcommerceOrders (2,173 rows)"}
                  {project.number === 2 && "Fact_BankCustomers (2,500 rows)"}
                  {project.number === 3 && "Fact_Shipments (2,200 rows)"}
                  {project.number === 4 && "Fact_Leads (3,500 rows)"}
                </div>
                <p className="text-[11px] text-slate-600">
                  Stores transactional events, granular numeric quantities, revenue amounts, and event timestamps.
                </p>
              </div>

              <div className="bg-slate-50 border border-slate-200 rounded p-3.5 space-y-2">
                <div className="text-xs font-bold text-slate-900">Dimension Tables</div>
                <div className="space-y-1 text-xs font-mono text-slate-700">
                  {project.number === 1 && (
                    <>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Customers (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Products (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Geography (1:*)</div>
                    </>
                  )}
                  {project.number === 2 && (
                    <>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Geography (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_TenureCohorts (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_ProductCount (1:*)</div>
                    </>
                  )}
                  {project.number === 3 && (
                    <>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Suppliers (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Warehouses (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Carriers (1:*)</div>
                    </>
                  )}
                  {project.number === 4 && (
                    <>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Campaigns (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Channels (1:*)</div>
                      <div className="bg-white p-1 rounded border border-slate-200">Dim_Segments (1:*)</div>
                    </>
                  )}
                </div>
              </div>

              <div className="bg-slate-50 border border-slate-200 rounded p-3.5 space-y-2">
                <div className="text-xs font-bold text-slate-900">Measure Container Table</div>
                <div className="text-xs font-mono text-emerald-700 bg-white p-1.5 rounded border border-slate-200">
                  _ProjectMeasures
                </div>
                <p className="text-[11px] text-slate-600">
                  Dedicated calculation group isolating dynamic DAX aggregation formulas without data storage overhead.
                </p>
              </div>
            </div>
          </div>

          {/* DAX Measures Library */}
          <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden text-white shadow-sm">
            <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
                <BarChart3 className="w-3.5 h-3.5 text-blue-400" />
                <span className="font-semibold text-white">dax_measures.dax</span>
                <span className="text-slate-500">·</span>
                <span className="text-slate-400">Power BI Calculated Measures</span>
              </div>

              <button
                onClick={handleCopyDax}
                className="bg-slate-700 hover:bg-slate-600 text-slate-200 px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center gap-1 border border-slate-600"
                title="Copy all DAX measures"
              >
                {copiedDax ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedDax ? 'Copied' : 'Copy All DAX'}</span>
              </button>
            </div>

            <div className="p-4 max-h-96 overflow-y-auto font-mono text-xs text-slate-300 leading-relaxed scrollbar-thin scrollbar-thumb-slate-700">
              <pre className="whitespace-pre-wrap">{project.daxMeasures}</pre>
            </div>
          </div>
        </>
      ) : (
        /* Excel Guide View */
        <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide flex items-center gap-1.5">
              <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
              <span>Microsoft Excel MIS Reporting & Pivot Model</span>
            </h3>
            <span className="text-xs text-slate-500 font-medium">MIS Best Practices</span>
          </div>

          <div className="prose prose-sm max-w-none text-xs text-slate-700 leading-relaxed">
            <pre className="p-4 bg-slate-900 text-slate-200 rounded font-mono text-xs whitespace-pre-wrap overflow-x-auto">
              {project.excelGuide}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
