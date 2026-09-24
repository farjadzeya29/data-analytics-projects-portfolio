import React, { useState } from 'react';
import { 
  BarChart3, 
  Database, 
  Terminal, 
  Layers, 
  ShieldCheck, 
  FileText, 
  Folder,
  ArrowLeft,
  ChevronRight
} from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';
import { ProjectDashboard } from './ProjectDashboard';
import { SqlQueryStudio } from './SqlQueryStudio';
import { PythonPipelineView } from './PythonPipelineView';
import { PowerBiSpecView } from './PowerBiSpecView';
import { DataQualityAuditView } from './DataQualityAuditView';
import { ExecutiveReportView } from './ExecutiveReportView';
import { RepoExplorerView } from './RepoExplorerView';

interface ProjectViewProps {
  project: ProjectMeta;
  onBackToOverview: () => void;
}

export const ProjectView: React.FC<ProjectViewProps> = ({ project, onBackToOverview }) => {
  const [subTab, setSubTab] = useState<'dashboard' | 'sql' | 'python' | 'powerbi' | 'audit' | 'report' | 'repo'>('dashboard');

  const navItems = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: <BarChart3 className="w-3.5 h-3.5" /> },
    { id: 'sql', label: 'SQL Query Studio', icon: <Database className="w-3.5 h-3.5" /> },
    { id: 'python', label: 'Python Pipeline & EDA', icon: <Terminal className="w-3.5 h-3.5" /> },
    { id: 'powerbi', label: 'Power BI & DAX Specs', icon: <Layers className="w-3.5 h-3.5" /> },
    { id: 'audit', label: 'Data Quality & Hygiene', icon: <ShieldCheck className="w-3.5 h-3.5" /> },
    { id: 'report', label: 'Strategic Report', icon: <FileText className="w-3.5 h-3.5" /> },
    { id: 'repo', label: 'Repo Code Explorer', icon: <Folder className="w-3.5 h-3.5" /> }
  ] as const;

  return (
    <div className="space-y-6 pb-16">
      {/* Breadcrumb & Project Header */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <button 
            onClick={onBackToOverview}
            className="hover:text-blue-600 transition-colors flex items-center gap-1 font-medium"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Portfolio Overview</span>
          </button>
          <ChevronRight className="w-3 h-3 text-slate-400" />
          <span className="font-semibold text-slate-800">Project {project.number}: {project.shortTitle}</span>
        </div>

        {/* Project Badge & Title */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 sm:p-6 text-white space-y-3 shadow-xs">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-semibold tracking-wider uppercase">
              <span>Project #{project.number}</span>
              <span aria-hidden="true">·</span>
              <span>{project.tech.join(' · ')}</span>
            </div>
            <div className="text-xs text-slate-400 font-mono">
              /projects/{project.id}
            </div>
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
            {project.title}
          </h1>

          <p className="text-slate-300 text-xs sm:text-sm max-w-3xl leading-relaxed">
            {project.tagline}
          </p>

          <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-400 italic">
            <span className="font-semibold text-slate-300 not-italic">Resume Objective: </span>
            "{project.resumeBullet1} {project.resumeBullet2}"
          </div>
        </div>
      </div>

      {/* Sub-Navigation Tabs Bar */}
      <div className="border-b border-slate-200 bg-white rounded-lg p-1.5 shadow-2xs overflow-x-auto scrollbar-none">
        <nav className="flex items-center gap-1 min-w-max">
          {navItems.map((item) => {
            const isActive = subTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setSubTab(item.id)}
                className={`px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center gap-1.5 ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Sub-Tab Content */}
      <div className="animate-in fade-in duration-150">
        {subTab === 'dashboard' && <ProjectDashboard project={project} />}
        {subTab === 'sql' && <SqlQueryStudio project={project} />}
        {subTab === 'python' && <PythonPipelineView project={project} />}
        {subTab === 'powerbi' && <PowerBiSpecView project={project} />}
        {subTab === 'audit' && <DataQualityAuditView project={project} />}
        {subTab === 'report' && <ExecutiveReportView project={project} />}
        {subTab === 'repo' && <RepoExplorerView project={project} />}
      </div>
    </div>
  );
};
