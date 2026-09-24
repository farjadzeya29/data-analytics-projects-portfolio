import React, { useState } from 'react';
import { Folder, FileText, Code, FileCode, Copy, Check, Terminal, Database, FileSpreadsheet } from 'lucide-react';
import { ProjectMeta } from '../data/portfolioData';

interface RepoExplorerViewProps {
  project: ProjectMeta;
}

export const RepoExplorerView: React.FC<RepoExplorerViewProps> = ({ project }) => {
  // Construct the repository files dictionary
  const repoFiles: { name: string; folder: string; content: string; language: string }[] = [
    { name: "README.md", folder: "/", content: project.readmeMd, language: "markdown" },
    { name: "requirements.txt", folder: "/", content: "pandas>=2.0.0\nnumpy>=1.24.0\nmatplotlib>=3.7.0\nstreamlit>=1.28.0\n", language: "text" },
    { name: "streamlit_app.py", folder: "/", content: project.streamlitCode, language: "python" },
    { name: "schema.sql", folder: "sql/", content: project.sqlFiles[0]?.content || "", language: "sql" },
    { name: "data_analysis.sql", folder: "sql/", content: project.sqlFiles[1]?.content || "", language: "sql" },
    { name: "advanced_queries.sql", folder: "sql/", content: project.sqlFiles[2]?.content || "", language: "sql" },
    { name: "data_cleaning.py", folder: "src/", content: project.pythonFiles[0]?.content || "", language: "python" },
    { name: "analysis.py", folder: "src/", content: project.pythonFiles[1]?.content || "", language: "python" },
    { name: "dax_measures.dax", folder: "dashboard/", content: project.daxMeasures, language: "dax" },
    { name: "insights.md", folder: "reports/", content: project.insightsMd, language: "markdown" }
  ];

  if (project.excelGuide) {
    repoFiles.push({ name: "excel_analysis_guide.md", folder: "reports/", content: project.excelGuide, language: "markdown" });
  }

  const [selectedFileIndex, setSelectedFileIndex] = useState(0);
  const [copied, setCopied] = useState(false);

  const activeFile = repoFiles[selectedFileIndex] || repoFiles[0];

  const handleCopy = () => {
    navigator.clipboard.writeText(activeFile.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getFileIcon = (name: string) => {
    if (name.endsWith('.sql')) return <Database className="w-3.5 h-3.5 text-orange-400" />;
    if (name.endsWith('.py')) return <Terminal className="w-3.5 h-3.5 text-blue-400" />;
    if (name.endsWith('.dax')) return <Code className="w-3.5 h-3.5 text-yellow-400" />;
    if (name.endsWith('.md')) return <FileText className="w-3.5 h-3.5 text-emerald-400" />;
    return <FileCode className="w-3.5 h-3.5 text-slate-400" />;
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="bg-white border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="text-xs font-semibold text-blue-600 uppercase tracking-wider flex items-center gap-1.5">
            <Folder className="w-3.5 h-3.5" />
            <span>Repository & Codebase Explorer</span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-0.5">
            {project.title} (GitHub-Ready Structure)
          </h2>
        </div>

        <div className="flex items-center gap-2 text-xs font-mono bg-slate-50 border border-slate-200 px-3 py-1.5 rounded text-slate-600">
          <span>cd projects/{project.id} && streamlit run streamlit_app.py</span>
        </div>
      </div>

      {/* Explorer Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* File Tree Column */}
        <div className="lg:col-span-4 bg-white border border-slate-200 rounded-lg p-4 space-y-3">
          <div className="text-xs font-bold text-slate-900 uppercase tracking-wider border-b border-slate-100 pb-2 flex items-center justify-between">
            <span>Project Files ({repoFiles.length})</span>
            <span className="text-[10px] text-slate-400 font-mono">/projects/{project.id}</span>
          </div>

          <div className="space-y-1">
            {repoFiles.map((file, idx) => (
              <button
                key={file.name}
                onClick={() => setSelectedFileIndex(idx)}
                className={`w-full text-left px-2.5 py-1.5 rounded text-xs font-mono flex items-center justify-between transition-colors ${
                  selectedFileIndex === idx
                    ? 'bg-blue-50 text-blue-800 font-semibold border border-blue-200'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  {getFileIcon(file.name)}
                  <span className="truncate">{file.folder}{file.name}</span>
                </div>
                <span className="text-[10px] text-slate-400 uppercase">{file.language}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Code Content Column */}
        <div className="lg:col-span-8 bg-slate-900 border border-slate-800 rounded-lg overflow-hidden text-white shadow-sm flex flex-col">
          <div className="bg-slate-800/80 px-4 py-2.5 border-b border-slate-700 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
              {getFileIcon(activeFile.name)}
              <span className="font-semibold text-white">{activeFile.folder}{activeFile.name}</span>
            </div>

            <button
              onClick={handleCopy}
              className="bg-slate-700 hover:bg-slate-600 text-slate-200 px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center gap-1 border border-slate-600"
              title="Copy file contents"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy Code'}</span>
            </button>
          </div>

          <div className="p-4 max-h-[500px] overflow-y-auto font-mono text-xs text-slate-300 leading-relaxed scrollbar-thin scrollbar-thumb-slate-700">
            <pre className="whitespace-pre-wrap">{activeFile.content}</pre>
          </div>
        </div>
      </div>
    </div>
  );
};
