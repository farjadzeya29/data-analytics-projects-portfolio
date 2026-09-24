/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { PortfolioOverview } from './components/PortfolioOverview';
import { ProjectView } from './components/ProjectView';
import { GitReposDocView } from './components/GitReposDocView';
import { ResumeModal } from './components/ResumeModal';
import { PROJECTS_DATA, FARJAD_PROFILE } from './data/portfolioData';
import { Mail, Phone, MapPin, Layers, Heart, Code2 } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [isResumeOpen, setIsResumeOpen] = useState<boolean>(false);

  const selectedProject = PROJECTS_DATA.find((p) => p.id === activeTab);

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 flex flex-col font-sans antialiased selection:bg-blue-600 selection:text-white">
      {/* Persistent Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenResume={() => setIsResumeOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {activeTab === 'overview' && (
          <PortfolioOverview
            onSelectProject={(projectId) => setActiveTab(projectId)}
            onOpenResume={() => setIsResumeOpen(true)}
          />
        )}

        {activeTab === 'readme' && <GitReposDocView />}

        {selectedProject && (
          <ProjectView
            project={selectedProject}
            onBackToOverview={() => setActiveTab('overview')}
          />
        )}
      </main>

      {/* Site Footer */}
      <footer className="bg-slate-900 border-t border-slate-800 text-white mt-auto py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
          <div className="space-y-1 text-center sm:text-left">
            <div className="font-semibold text-white">
              {FARJAD_PROFILE.name} — Data Analyst Portfolio
            </div>
            <div>
              Specialized in Python (pandas, NumPy), SQL (MySQL), Microsoft Excel & Power BI
            </div>
          </div>

          <div className="flex items-center gap-6">
            <a 
              href={`mailto:${FARJAD_PROFILE.email}`} 
              className="hover:text-white transition-colors flex items-center gap-1.5"
            >
              <Mail className="w-3.5 h-3.5 text-blue-400" />
              <span>{FARJAD_PROFILE.email}</span>
            </a>
            <a 
              href={`tel:${FARJAD_PROFILE.phone}`} 
              className="hover:text-white transition-colors flex items-center gap-1.5"
            >
              <Phone className="w-3.5 h-3.5 text-emerald-400" />
              <span>{FARJAD_PROFILE.phone}</span>
            </a>
            <button
              onClick={() => setIsResumeOpen(true)}
              className="hover:text-white transition-colors font-medium text-slate-300"
            >
              View Resume
            </button>
          </div>
        </div>
      </footer>

      {/* Full Resume Modal */}
      <ResumeModal
        isOpen={isResumeOpen}
        onClose={() => setIsResumeOpen(false)}
      />
    </div>
  );
}
