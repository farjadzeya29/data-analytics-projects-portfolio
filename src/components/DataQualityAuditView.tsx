import React from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle2, ArrowRight, Database, FileText } from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface DataQualityAuditViewProps {
  project: ProjectMeta;
}

export const DataQualityAuditView: React.FC<DataQualityAuditViewProps> = ({ project }) => {
  const summary = project.cleaningSummary;

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Data Hygiene, Validation & Audit Trail</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            Raw vs Cleaned Data Audit Summary
          </h2>
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded border border-emerald-200">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Production Validation Passed</span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-1">
          <div className="text-[11px] text-slate-500 font-medium">Raw Records Ingested</div>
          <div className="text-xl font-bold text-slate-900">{summary.rawRows.toLocaleString()}</div>
          <div className="text-[10px] text-slate-400">Unfiltered ERP/CRM extract</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-1">
          <div className="text-[11px] text-slate-500 font-medium">Cleaned Records Loaded</div>
          <div className="text-xl font-bold text-emerald-600">{summary.cleanedRows.toLocaleString()}</div>
          <div className="text-[10px] text-slate-400">Ready for SQL & Power BI</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-1">
          <div className="text-[11px] text-slate-500 font-medium">Duplicate Rows Pruned</div>
          <div className="text-xl font-bold text-slate-900">{summary.rawRows - summary.cleanedRows}</div>
          <div className="text-[10px] text-slate-400">Exact primary key collisions</div>
        </div>

        <div className="bg-white border border-slate-200 rounded-lg p-4 space-y-1">
          <div className="text-[11px] text-slate-500 font-medium">Anomalies Rectified</div>
          <div className="text-xl font-bold text-blue-600">100%</div>
          <div className="text-[10px] text-slate-400">Zero nulls or invalid datatypes</div>
        </div>
      </div>

      {/* Issues Found vs Actions Taken */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Issues Found */}
        <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold text-rose-600 uppercase tracking-wide border-b border-slate-100 pb-2">
            <AlertTriangle className="w-4 h-4" />
            <span>Data Quality Defects Identified in Raw Files</span>
          </div>

          <ul className="space-y-2 text-xs text-slate-700">
            {summary.issuesFound.map((issue, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-rose-50/50 p-2.5 rounded border border-rose-100">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mt-1.5 shrink-0"></span>
                <span>{issue}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Actions Taken */}
        <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-3">
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 uppercase tracking-wide border-b border-slate-100 pb-2">
            <CheckCircle2 className="w-4 h-4" />
            <span>Pipeline Transformations & Remediation</span>
          </div>

          <ul className="space-y-2 text-xs text-slate-700">
            {summary.actionsTaken.map((action, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-emerald-50/50 p-2.5 rounded border border-emerald-100">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0"></span>
                <span>{action}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Code Snippet for Cleaning */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg p-4 text-white space-y-2">
        <div className="text-xs font-mono font-semibold text-slate-300">
          Source: src/data_cleaning.py execution
        </div>
        <p className="text-xs text-slate-400">
          The automated cleaning pipeline runs idempotently before database ingestion or Power BI semantic model refreshes, generating audit logs and verifying schema constraints.
        </p>
      </div>
    </div>
  );
};
