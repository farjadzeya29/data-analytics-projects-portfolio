import React, { useState } from 'react';
import { Database, Play, Copy, Check, Terminal, FileCode, CheckCircle2 } from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface SqlQueryStudioProps {
  project: ProjectMeta;
}

export const SqlQueryStudio: React.FC<SqlQueryStudioProps> = ({ project }) => {
  const [selectedSqlIndex, setSelectedSqlIndex] = useState(1); // Default to data_analysis.sql
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<{
    status: string;
    rowsExamined: number;
    rowsReturned: number;
    durationMs: number;
    columns: string[];
    rows: any[];
  } | null>(null);
  const [copied, setCopied] = useState(false);

  const currentFile = project.sqlFiles[selectedSqlIndex] || project.sqlFiles[0];

  const handleCopy = () => {
    navigator.clipboard.writeText(currentFile.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExecute = () => {
    setIsExecuting(true);
    setExecutionResult(null);

    setTimeout(() => {
      setIsExecuting(false);
      // Simulated realistic results based on project and query
      if (project.number === 1) {
        setExecutionResult({
          status: "SUCCESS (MySQL 8.0 Engine)",
          rowsExamined: 2173,
          rowsReturned: 3,
          durationMs: 14,
          columns: ["category", "total_orders", "total_sales_usd", "total_profit_usd", "profit_margin_pct"],
          rows: [
            ["Technology", 685, "$412,500.00", "$117,150.00", "28.40%"],
            ["Office Supplies", 942, "$248,900.00", "$60,000.00", "24.10%"],
            ["Furniture", 546, "$181,100.00", "$14,850.00", "8.20%"]
          ]
        });
      } else if (project.number === 2) {
        setExecutionResult({
          status: "SUCCESS (MySQL 8.0 Engine)",
          rowsExamined: 2500,
          rowsReturned: 4,
          durationMs: 18,
          columns: ["num_of_products", "total_accounts", "churned_accounts", "churn_rate_pct", "total_balance_churned"],
          rows: [
            ["1 Product", 1250, 345, "27.60%", "$18,450,200.00"],
            ["2 Products", 1100, 89, "8.10%", "$4,210,500.00"],
            ["3 Products", 125, 98, "78.40%", "$21,120,400.00"],
            ["4 Products", 25, 23, "92.00%", "$4,420,000.00"]
          ]
        });
      } else if (project.number === 3) {
        setExecutionResult({
          status: "SUCCESS (MySQL 8.0 Engine)",
          rowsExamined: 2200,
          rowsReturned: 4,
          durationMs: 16,
          columns: ["warehouse_code", "origin_warehouse", "total_shipments", "ontime_delivery_pct", "avg_delay_days"],
          rows: [
            ["WH-MUM-02", "West Port (Mumbai)", 680, "86.40%", "0.80"],
            ["WH-DEL-01", "North Hub (Delhi-NCR)", 610, "84.80%", "1.10"],
            ["WH-BLR-03", "South Central (Bengaluru)", 520, "82.20%", "1.30"],
            ["WH-KOL-04", "East Gateway (Kolkata)", 390, "71.20%", "2.40"]
          ]
        });
      } else {
        setExecutionResult({
          status: "SUCCESS (MySQL 8.0 Engine)",
          rowsExamined: 3500,
          rowsReturned: 6,
          durationMs: 22,
          columns: ["channel", "channel_spend", "inbound_leads", "closed_won", "cac_usd", "roas_multiplier", "net_roi_pct"],
          rows: [
            ["Email Marketing", "$10,500.00", 350, 98, "$107.14", "13.40x", "1240.00%"],
            ["LinkedIn Ads", "$73,000.00", 850, 204, "$357.84", "8.20x", "720.00%"],
            ["Organic Search (SEO)", "$12,000.00", 620, 136, "$88.24", "6.80x", "580.00%"],
            ["Google Ads", "$63,000.00", 940, 150, "$420.00", "5.10x", "410.00%"],
            ["Meta (Facebook/IG)", "$28,000.00", 740, 82, "$341.46", "3.90x", "290.00%"],
            ["Influencer Partnerships", "$22,000.00", 310, 14, "$1,571.43", "0.82x", "-18.00%"]
          ]
        });
      }
    }, 450);
  };

  return (
    <div className="space-y-6">
      {/* Studio Header & File Selector */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <Database className="w-3.5 h-3.5" />
            <span>SQL Query Studio · MySQL 8.0+ Compatible</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            Relational Schemas & Analytical SQL Scripts
          </h2>
        </div>

        {/* Script Selector Tabs */}
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-md text-xs">
          {project.sqlFiles.map((f, idx) => (
            <button
              key={f.name}
              onClick={() => {
                setSelectedSqlIndex(idx);
                setExecutionResult(null);
              }}
              className={`px-3 py-1.5 rounded text-xs font-mono font-medium transition-colors ${
                selectedSqlIndex === idx
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {f.name}
            </button>
          ))}
        </div>
      </div>

      {/* Code Editor & Execution Controls */}
      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden text-white shadow-sm">
        <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
            <FileCode className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-semibold text-white">{currentFile.name}</span>
            <span className="text-slate-500">·</span>
            <span className="text-slate-400">{currentFile.description}</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="bg-slate-700 hover:bg-slate-600 text-slate-200 px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center gap-1 border border-slate-600"
              title="Copy SQL content"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy SQL'}</span>
            </button>
            <button
              onClick={handleExecute}
              disabled={isExecuting}
              className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white px-3 py-1 rounded text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-sm"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>{isExecuting ? 'Running Query...' : 'Run Query'}</span>
            </button>
          </div>
        </div>

        {/* Code Content */}
        <div className="p-4 max-h-96 overflow-y-auto font-mono text-xs text-slate-300 leading-relaxed scrollbar-thin scrollbar-thumb-slate-700">
          <pre className="whitespace-pre-wrap">{currentFile.content}</pre>
        </div>
      </div>

      {/* Query Execution Output Table */}
      {executionResult && (
        <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-4 shadow-xs">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span className="text-xs font-bold text-slate-900">Query Executed Successfully</span>
              <span className="text-xs text-slate-500">({executionResult.status})</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono text-slate-600">
              <span>Duration: <strong className="text-slate-900">{executionResult.durationMs} ms</strong></span>
              <span>·</span>
              <span>Rows Examined: <strong className="text-slate-900">{executionResult.rowsExamined}</strong></span>
              <span>·</span>
              <span>Rows Returned: <strong className="text-slate-900">{executionResult.rowsReturned}</strong></span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left text-slate-700">
              <thead className="bg-slate-50 text-slate-900 font-semibold border-b border-slate-200">
                <tr>
                  {executionResult.columns.map((col, idx) => (
                    <th key={idx} className="py-2.5 px-3 font-mono">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {executionResult.rows.map((row, rIdx) => (
                  <tr key={rIdx} className="hover:bg-slate-50/70 transition-colors font-mono">
                    {row.map((cell: any, cIdx: number) => (
                      <td key={cIdx} className="py-2 px-3 font-medium text-slate-800">
                        {String(cell)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
