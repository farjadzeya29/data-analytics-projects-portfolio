import React from 'react';
import { 
  BarChart3, 
  Database, 
  FileSpreadsheet, 
  Terminal, 
  ArrowRight, 
  CheckCircle2, 
  Briefcase, 
  GraduationCap, 
  Cpu, 
  Sparkles,
  ShoppingBag,
  ShieldCheck,
  Truck,
  Target,
  Code,
  Download,
  Copy,
  Check
} from 'lucide-react';
import { FARJAD_PROFILE, PROJECTS_DATA, ProjectMeta } from '../data/portfolioData';

interface PortfolioOverviewProps {
  onSelectProject: (projectId: string) => void;
  onOpenResume: () => void;
}

export const PortfolioOverview: React.FC<PortfolioOverviewProps> = ({ onSelectProject, onOpenResume }) => {
  const [copiedCmd, setCopiedCmd] = React.useState(false);

  const getProjectIcon = (num: number) => {
    switch (num) {
      case 1: return <ShoppingBag className="w-5 h-5 text-emerald-400" />;
      case 2: return <ShieldCheck className="w-5 h-5 text-blue-400" />;
      case 3: return <Truck className="w-5 h-5 text-amber-400" />;
      case 4: return <Target className="w-5 h-5 text-purple-400" />;
      default: return <BarChart3 className="w-5 h-5 text-blue-400" />;
    }
  };

  const handleCopyClone = () => {
    navigator.clipboard.writeText("git clone https://github.com/farjadzeya/data-analyst-portfolio.git");
    setCopiedCmd(true);
    setTimeout(() => setCopiedCmd(false), 2000);
  };

  return (
    <div className="space-y-10 pb-16">
      {/* Hero / Executive Profile */}
      <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 sm:p-8 text-white relative overflow-hidden">
        <div className="max-w-4xl relative z-10 space-y-4">
          <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium tracking-wider uppercase">
            <span>Verified Portfolio</span>
            <span aria-hidden="true">·</span>
            <span>Based on Farjad Zeya's Resume</span>
            <span aria-hidden="true">·</span>
            <span>4 End-to-End Production Projects</span>
          </div>

          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white">
            Farjad Zeya <span className="text-slate-400 font-normal">| Data Analyst Portfolio</span>
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed max-w-3xl">
            {FARJAD_PROFILE.summary}
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4 text-xs text-slate-400 border-t border-slate-800/80">
            <div className="flex items-center gap-1.5">
              <GraduationCap className="w-4 h-4 text-blue-400" />
              <span>{FARJAD_PROFILE.education}</span>
            </div>
            <span className="text-slate-700">·</span>
            <div className="flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-emerald-400" />
              <span>Current: Maintenance Data Analyst at CK Infrastructure Ltd</span>
            </div>
            <span className="text-slate-700">·</span>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-blue-400"></span>
              <span>Location: {FARJAD_PROFILE.location}</span>
            </div>
          </div>

          <div className="pt-3 flex flex-wrap items-center gap-3">
            <button
              onClick={() => onSelectProject(PROJECTS_DATA[0].id)}
              className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded text-xs font-semibold transition-colors flex items-center gap-2 shadow-sm"
            >
              <span>Explore Featured Project 1</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onOpenResume}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-4 py-2 rounded text-xs font-medium transition-colors border border-slate-700"
            >
              View Full Resume & Credentials
            </button>
            <button
              onClick={handleCopyClone}
              className="bg-slate-800/60 hover:bg-slate-800 text-slate-300 hover:text-white px-3 py-2 rounded text-xs font-mono transition-colors border border-slate-700/80 flex items-center gap-2"
              title="Copy git clone command"
            >
              <Terminal className="w-3.5 h-3.5 text-slate-400" />
              <span>git clone portfolio.git</span>
              {copiedCmd ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
            </button>
          </div>
        </div>
      </section>

      {/* 4 Projects Grid */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Four Core Resume Projects</h2>
            <p className="text-xs text-slate-600">
              Complete, production-grade repositories with SQL schemas, Python pipelines, Power BI specs, datasets, and executive findings.
            </p>
          </div>
          <span className="text-xs text-slate-500 font-medium">All 4 Implemented</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
          {PROJECTS_DATA.map((proj) => (
            <div
              key={proj.id}
              className="bg-white border border-slate-200 rounded-lg p-5 hover:border-blue-300 transition-all shadow-xs flex flex-col justify-between group"
            >
              <div className="space-y-3">
                {/* Header */}
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-9 h-9 rounded bg-slate-50 border border-slate-200 flex items-center justify-center">
                      {getProjectIcon(proj.number)}
                    </div>
                    <div>
                      <div className="text-[11px] font-semibold text-blue-600 uppercase tracking-wider">
                        Project {proj.number}
                      </div>
                      <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                        {proj.title}
                      </h3>
                    </div>
                  </div>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed">
                  {proj.tagline}
                </p>

                {/* Resume Bullets Quote */}
                <div className="bg-slate-50 border-l-2 border-blue-500 p-3 text-xs text-slate-700 space-y-1.5 rounded-r">
                  <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
                    Resume Objective & Scope:
                  </div>
                  <p className="italic">"{proj.resumeBullet1}"</p>
                  <p className="italic">"{proj.resumeBullet2}"</p>
                </div>

                {/* Key KPIs Preview */}
                <div className="grid grid-cols-3 gap-2 pt-1">
                  {proj.kpis.slice(0, 3).map((kpi, idx) => (
                    <div key={idx} className="bg-slate-50/70 border border-slate-100 rounded p-2 text-center">
                      <div className="text-[10px] text-slate-500 truncate">{kpi.label}</div>
                      <div className="text-sm font-bold text-slate-900 mt-0.5">{kpi.value}</div>
                      <div className="text-[10px] text-emerald-600 font-medium truncate">{kpi.delta}</div>
                    </div>
                  ))}
                </div>

                {/* Tech Stack List (Zero-Pill: Clean unboxed text with separators) */}
                <div className="flex items-center gap-2 text-xs text-slate-500 pt-1">
                  <span className="font-semibold text-slate-700">Tech:</span>
                  {proj.tech.map((t, idx) => (
                    <React.Fragment key={idx}>
                      <span>{t}</span>
                      {idx < proj.tech.length - 1 && <span aria-hidden="true">·</span>}
                    </React.Fragment>
                  ))}
                </div>
              </div>

              {/* Action Bar */}
              <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[11px] text-slate-500">
                  {proj.sampleRecords.length}+ Clean Rows · SQL + Python + Power BI
                </span>
                <button
                  onClick={() => onSelectProject(proj.id)}
                  className="bg-slate-900 hover:bg-blue-600 text-white px-3 py-1.5 rounded text-xs font-semibold transition-colors flex items-center gap-1.5"
                >
                  <span>Open Deep Dive</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Cross-Project Comparison Matrix */}
      <section className="bg-white border border-slate-200 rounded-lg p-5 space-y-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">Project Architectural & Analytical Matrix</h2>
          <p className="text-xs text-slate-600">
            Side-by-side comparison of business domain, technical stack, core dataset, and analytical methodology.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left text-slate-700">
            <thead className="bg-slate-50 text-slate-900 border-b border-slate-200 font-semibold">
              <tr>
                <th className="py-2.5 px-3"># Project</th>
                <th className="py-2.5 px-3">Business Domain</th>
                <th className="py-2.5 px-3">Primary Tech</th>
                <th className="py-2.5 px-3">Dataset & Records</th>
                <th className="py-2.5 px-3">Core Analytics / Models</th>
                <th className="py-2.5 px-3">Key Strategic Finding</th>
                <th className="py-2.5 px-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {PROJECTS_DATA.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50/70 transition-colors">
                  <td className="py-3 px-3 font-bold text-slate-900 whitespace-nowrap">
                    P{p.number}: {p.shortTitle}
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    {p.number === 1 ? 'E-Commerce Retail' : p.number === 2 ? 'Retail Banking' : p.number === 3 ? 'Supply Chain Logistics' : 'B2B Marketing & Growth'}
                  </td>
                  <td className="py-3 px-3 font-mono text-[11px] text-blue-700">
                    {p.tech.slice(0, 3).join(', ')}
                  </td>
                  <td className="py-3 px-3 text-slate-600">
                    {p.cleaningSummary.cleanedRows.toLocaleString()} cleaned rows
                  </td>
                  <td className="py-3 px-3 text-slate-700">
                    {p.number === 1 && 'RFM Segmentation, Pareto 80/20, YoY Growth'}
                    {p.number === 2 && 'Churn Rate, Multi-Product Paradox, Risk Scoring'}
                    {p.number === 3 && 'On-Time Delivery (OTD), Route Bottlenecks, Scorecards'}
                    {p.number === 4 && 'Multi-Stage Funnel, CAC/ROAS, Channel Attribution'}
                  </td>
                  <td className="py-3 px-3 text-slate-600 italic">
                    {p.number === 1 && 'Top 14% Champions generate 38% revenue; Technology has 28.4% margin'}
                    {p.number === 2 && 'Customers with 3-4 products churn at 78%+ vs 8.1% for 2 products'}
                    {p.number === 3 && 'Kolkata Hub dispatch latency (2.4 days) drives OTD down to 71.2%'}
                    {p.number === 4 && 'LinkedIn Ads achieves 7.2x ROAS; Influencer marketing loses budget (0.82x)'}
                  </td>
                  <td className="py-3 px-3 text-right whitespace-nowrap">
                    <button
                      onClick={() => onSelectProject(p.id)}
                      className="text-blue-600 hover:text-blue-800 font-semibold text-xs flex items-center gap-1 justify-end ml-auto"
                    >
                      <span>View</span>
                      <ArrowRight className="w-3 h-3" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Technical Skills & Experience Section */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Skills Column */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 className="text-base font-bold text-slate-900">Technical Skills Inventory</h2>
            <span className="text-xs text-slate-500">From Farjad Zeya's Resume</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {FARJAD_PROFILE.skills.map((cat, idx) => (
              <div key={idx} className="space-y-1.5">
                <div className="text-xs font-semibold text-slate-900 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                  <span>{cat.category}</span>
                </div>
                <div className="flex flex-wrap items-center gap-1.5 text-xs text-slate-600">
                  {cat.items.map((skill, sIdx) => (
                    <React.Fragment key={sIdx}>
                      <span className="bg-slate-50 text-slate-700 px-2 py-0.5 rounded border border-slate-100 text-[11px]">
                        {skill}
                      </span>
                    </React.Fragment>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Current Role Spotlight */}
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-5 text-white space-y-3 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-emerald-400 text-xs font-medium uppercase tracking-wider">
              <CheckCircle2 className="w-4 h-4" />
              <span>Current Professional Role</span>
            </div>
            <h3 className="text-base font-bold text-white">
              Maintenance Data Analyst
            </h3>
            <div className="text-xs text-slate-400">
              CK Infrastructure Ltd · Aug 2026 – Present
            </div>
            <ul className="text-xs text-slate-300 space-y-1.5 pt-2 list-disc list-inside">
              <li>Maintains diesel consumption databases and equipment meter readings across the fleet.</li>
              <li>Builds Excel Pivot Table dashboards and monthly MIS reports for leadership.</li>
              <li>Flags machinery consumption anomalies to drive operational fuel savings.</li>
            </ul>
          </div>

          <button
            onClick={onOpenResume}
            className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white py-2 rounded text-xs font-medium transition-colors border border-slate-700 mt-3"
          >
            Review Full Experience (3 Roles)
          </button>
        </div>
      </section>
    </div>
  );
};
