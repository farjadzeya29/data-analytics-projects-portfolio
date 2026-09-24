import React, { useState, useMemo } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Filter, 
  Search, 
  ChevronDown, 
  Download, 
  ArrowUpRight, 
  ArrowDownRight, 
  Table, 
  RefreshCw,
  SlidersHorizontal
} from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface ProjectDashboardProps {
  project: ProjectMeta;
}

export const ProjectDashboard: React.FC<ProjectDashboardProps> = ({ project }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('All');
  const [page, setPage] = useState(1);
  const rowsPerPage = 10;

  // Filter options derived from project data
  const filterOptions = useMemo(() => {
    if (project.number === 1) return ['All', 'Technology', 'Office Supplies', 'Furniture'];
    if (project.number === 2) return ['All', 'France', 'Germany', 'Spain'];
    if (project.number === 3) return ['All', 'North Hub (Delhi-NCR)', 'West Port (Mumbai)', 'South Central (Bengaluru)', 'East Gateway (Kolkata)'];
    if (project.number === 4) return ['All', 'LinkedIn Ads', 'Google Ads', 'Email Marketing', 'Organic Search (SEO)', 'Meta (Facebook/IG)', 'Influencer Partnerships'];
    return ['All'];
  }, [project.number]);

  // Filtered sample records
  const filteredRecords = useMemo(() => {
    return project.sampleRecords.filter(row => {
      const matchFilter = selectedFilter === 'All' ? true : Object.values(row).some(v => String(v).includes(selectedFilter));
      const matchSearch = searchTerm === '' ? true : Object.values(row).some(v => 
        String(v).toLowerCase().includes(searchTerm.toLowerCase())
      );
      return matchFilter && matchSearch;
    });
  }, [project.sampleRecords, selectedFilter, searchTerm]);

  const totalPages = Math.ceil(filteredRecords.length / rowsPerPage) || 1;
  const paginatedRecords = filteredRecords.slice((page - 1) * rowsPerPage, page * rowsPerPage);

  const tableHeaders = project.sampleRecords.length > 0 
    ? Object.keys(project.sampleRecords[0]).slice(0, 7)
    : [];

  // Max value for bar scaling
  const maxCategoryVal = Math.max(...(project.categoryData?.map(c => c.value) || [100]));
  const maxTimeVal = Math.max(...(project.timeData?.map(t => t.value) || [100]));

  return (
    <div className="space-y-6">
      {/* Top Bar: Title & Filter Controls */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider">
            Interactive BI Cockpit · Project {project.number}
          </div>
          <h2 className="text-lg font-bold text-slate-900">
            {project.title}
          </h2>
        </div>

        {/* Segmented Filter Control */}
        <div className="flex flex-wrap items-center gap-1.5 bg-slate-100 p-1 rounded-md text-xs">
          <span className="text-slate-500 px-2 flex items-center gap-1 font-medium">
            <Filter className="w-3 h-3" />
            <span>Filter:</span>
          </span>
          {filterOptions.slice(0, 5).map((opt) => (
            <button
              key={opt}
              onClick={() => { setSelectedFilter(opt); setPage(1); }}
              className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
                selectedFilter === opt
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {project.kpis.map((kpi, idx) => (
          <div key={idx} className="bg-white border border-slate-200 rounded-lg p-4 space-y-1">
            <div className="text-[11px] text-slate-500 font-medium truncate">{kpi.label}</div>
            <div className="text-xl font-bold text-slate-900">{kpi.value}</div>
            <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-600">
              <span>{kpi.delta}</span>
            </div>
            <div className="text-[10px] text-slate-400 truncate">{kpi.sub}</div>
          </div>
        ))}
      </div>

      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Visual 1: Primary Category Bar Chart */}
        <div className="lg:col-span-6 bg-white border border-slate-200 rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                {project.number === 1 && "Revenue & Profit by Product Category"}
                {project.number === 2 && "Churn Rate (%) by Number of Bank Products"}
                {project.number === 3 && "On-Time Delivery Rate (%) by Origin Warehouse Hub"}
                {project.number === 4 && "Channel Return on Ad Spend (ROAS Multiplier)"}
              </h3>
              <p className="text-[11px] text-slate-500">
                {project.number === 1 && "Technology generates $412k (49% of sales) with 28.4% margin"}
                {project.number === 2 && "Multi-product paradox: 2 products is optimal; 3-4 products spikes churn"}
                {project.number === 3 && "Kolkata Hub (71.2%) experiences highest dispatch delays"}
                {project.number === 4 && "Email (12.4x) and LinkedIn (7.2x) deliver highest capital efficiency"}
              </p>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            {project.categoryData?.map((item, idx) => {
              const widthPct = Math.max(8, Math.round((item.value / maxCategoryVal) * 100));
              return (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-medium text-slate-700">{item.name}</span>
                    <span className="font-bold text-slate-900">
                      {project.number === 1 ? `$${item.value.toLocaleString()}` : `${item.value}%`}
                    </span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                    <div 
                      className={`h-full rounded-full transition-all ${
                        project.number === 2 && item.value > 50 ? 'bg-rose-500' :
                        project.number === 3 && item.value < 75 ? 'bg-amber-500' :
                        'bg-blue-600'
                      }`}
                      style={{ width: `${widthPct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Visual 2: Time Trend or Funnel Progression */}
        <div className="lg:col-span-6 bg-white border border-slate-200 rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
                {project.number === 1 && "Monthly Sales & Profit Velocity Trend"}
                {project.number === 2 && "Churn Rate (%) by Customer Tenure Cohort"}
                {project.number === 3 && "Quarterly On-Time Delivery % Trend"}
                {project.number === 4 && "Multi-Stage Lead-to-Customer Funnel Volume"}
              </h3>
              <p className="text-[11px] text-slate-500">
                {project.number === 1 && "Strong seasonal peak in Q4 holiday quarters"}
                {project.number === 2 && "First-year onboarding accounts face peak 24.8% attrition"}
                {project.number === 3 && "Consistent 81-83% band with Q4 holiday freight surge"}
                {project.number === 4 && "Key drop-off occurs at MQL to SQL handoff (-42%)"}
              </p>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            {project.timeData?.map((item, idx) => {
              const widthPct = Math.max(8, Math.round((item.value / maxTimeVal) * 100));
              return (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-medium text-slate-700">{item.date}</span>
                    <span className="font-bold text-slate-900">
                      {project.number === 1 ? `$${item.value.toLocaleString()}` :
                       project.number === 4 ? `${item.value.toLocaleString()} leads` :
                       `${item.value}%`}
                    </span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                    <div 
                      className="h-full rounded-full bg-emerald-500 transition-all"
                      style={{ width: `${widthPct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Interactive Data Table Sample */}
      <div className="bg-white border border-slate-200 rounded-lg p-5 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wide">
              Cleaned Dataset Records (Sample Preview)
            </h3>
            <p className="text-[11px] text-slate-500">
              Showing {filteredRecords.length} records matching current filter: <span className="font-medium text-blue-600">{selectedFilter}</span>
            </p>
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            <div className="relative w-full sm:w-64">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search rows..."
                value={searchTerm}
                onChange={(e) => { setSearchTerm(e.target.value); setPage(1); }}
                className="w-full pl-8 pr-3 py-1.5 border border-slate-200 rounded text-xs focus:outline-hidden focus:border-blue-500"
              />
            </div>
            <button
              onClick={() => { setSelectedFilter('All'); setSearchTerm(''); setPage(1); }}
              className="p-1.5 border border-slate-200 rounded text-slate-500 hover:text-slate-800 hover:bg-slate-50"
              title="Reset Filters"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-700">
            <thead className="bg-slate-50 text-slate-900 font-semibold border-b border-slate-200">
              <tr>
                {tableHeaders.map((h, i) => (
                  <th key={i} className="py-2.5 px-3 whitespace-nowrap">
                    {h.replace(/_/g, ' ').toUpperCase()}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {paginatedRecords.map((row, rIdx) => (
                <tr key={rIdx} className="hover:bg-slate-50/70 transition-colors">
                  {tableHeaders.map((h, cIdx) => (
                    <td key={cIdx} className="py-2 px-3 whitespace-nowrap text-slate-600">
                      {String((row as Record<string, any>)[h])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-2">
          <span>
            Page {page} of {totalPages} ({filteredRecords.length} records)
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-2.5 py-1 rounded border border-slate-200 disabled:opacity-50 hover:bg-slate-50 font-medium"
            >
              Previous
            </button>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-2.5 py-1 rounded border border-slate-200 disabled:opacity-50 hover:bg-slate-50 font-medium"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
