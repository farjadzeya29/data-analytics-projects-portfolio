import React from 'react';
import { 
  BarChart3, 
  Database, 
  FileText, 
  Terminal, 
  ExternalLink, 
  Mail, 
  Phone, 
  MapPin, 
  Briefcase, 
  GraduationCap,
  Layers,
  ChevronRight,
  TrendingUp,
  ShieldCheck,
  Truck,
  Target,
  ShoppingBag
} from 'lucide-react';
import { FARJAD_PROFILE, PROJECTS_DATA } from '../data/portfolioData';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onOpenResume: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, onOpenResume }) => {
  const getProjectIcon = (num: number) => {
    switch (num) {
      case 1: return <ShoppingBag className="w-4 h-4" />;
      case 2: return <ShieldCheck className="w-4 h-4" />;
      case 3: return <Truck className="w-4 h-4" />;
      case 4: return <Target className="w-4 h-4" />;
      default: return <Layers className="w-4 h-4" />;
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-900/95 backdrop-blur border-b border-slate-800 text-white">
      {/* Top Banner with Contact & Credentials */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex flex-wrap items-center justify-between gap-3 text-xs border-b border-slate-800/60">
        <div className="flex items-center gap-4 text-slate-300">
          <div className="flex items-center gap-1.5 font-semibold text-white tracking-wide">
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span>{FARJAD_PROFILE.name}</span>
            <span className="text-slate-500">|</span>
            <span className="text-emerald-400 font-medium">{FARJAD_PROFILE.title}</span>
          </div>
          <span className="hidden sm:inline text-slate-600">·</span>
          <div className="hidden sm:flex items-center gap-1 text-slate-400">
            <Briefcase className="w-3.5 h-3.5 text-slate-400" />
            <span>CK Infrastructure Ltd (Maintenance Data Analyst)</span>
          </div>
        </div>

        <div className="flex items-center gap-4 text-slate-400">
          <a 
            href={`mailto:${FARJAD_PROFILE.email}`} 
            className="hover:text-white flex items-center gap-1 transition-colors"
          >
            <Mail className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden md:inline">{FARJAD_PROFILE.email}</span>
          </a>
          <a 
            href={`tel:${FARJAD_PROFILE.phone}`} 
            className="hover:text-white flex items-center gap-1 transition-colors"
          >
            <Phone className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden md:inline">{FARJAD_PROFILE.phone}</span>
          </a>
          <button
            onClick={onOpenResume}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-2.5 py-1 rounded text-xs font-medium transition-colors border border-slate-700 flex items-center gap-1"
          >
            <FileText className="w-3 h-3 text-emerald-400" />
            <span>View Resume</span>
          </button>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex items-center justify-between overflow-x-auto scrollbar-none">
        <nav className="flex items-center gap-1.5 min-w-max">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'overview'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Portfolio Overview</span>
          </button>

          <span className="text-slate-700 mx-1">|</span>

          {PROJECTS_DATA.map((p) => {
            const isActive = activeTab === p.id;
            return (
              <button
                key={p.id}
                onClick={() => setActiveTab(p.id)}
                className={`px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center gap-2 ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
                }`}
              >
                <span className={`w-4 h-4 rounded-full text-[10px] flex items-center justify-center font-bold ${
                  isActive ? 'bg-white text-blue-700' : 'bg-slate-800 text-slate-300 border border-slate-700'
                }`}>
                  {p.number}
                </span>
                <span>{p.shortTitle}</span>
              </button>
            );
          })}

          <span className="text-slate-700 mx-1">|</span>

          <button
            onClick={() => setActiveTab('readme')}
            className={`px-3 py-1.5 rounded text-xs font-medium transition-colors flex items-center gap-1.5 ${
              activeTab === 'readme'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Git Repos & Docs</span>
          </button>
        </nav>
      </div>
    </header>
  );
};
