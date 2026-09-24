import React from 'react';
import { X, Mail, Phone, MapPin, GraduationCap, Briefcase, FileText, CheckCircle2 } from 'lucide-react';
import { FARJAD_PROFILE } from '../data/portfolioData';

interface ResumeModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ResumeModal: React.FC<ResumeModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-xs overflow-y-auto">
      <div className="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-slate-200 animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="bg-slate-900 text-white p-5 flex items-center justify-between border-b border-slate-800">
          <div>
            <div className="text-xs text-emerald-400 font-medium tracking-wide uppercase">
              Curriculum Vitae & Qualifications
            </div>
            <h2 className="text-xl font-bold text-white mt-0.5">
              {FARJAD_PROFILE.name} <span className="text-slate-400 font-normal">· {FARJAD_PROFILE.title}</span>
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-800 text-xs leading-relaxed">
          {/* Contact Strip */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-3 bg-slate-50 rounded-lg border border-slate-200 text-slate-600">
            <div className="flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-blue-600" />
              <span>{FARJAD_PROFILE.email}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Phone className="w-3.5 h-3.5 text-emerald-600" />
              <span>{FARJAD_PROFILE.phone}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-rose-600" />
              <span>{FARJAD_PROFILE.location}</span>
            </div>
          </div>

          {/* Summary */}
          <div className="space-y-1.5">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1">
              Professional Profile
            </h3>
            <p className="text-slate-700 text-xs leading-relaxed">
              {FARJAD_PROFILE.summary}
            </p>
          </div>

          {/* Education */}
          <div className="space-y-1.5">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1">
              Education
            </h3>
            <div className="flex items-start justify-between">
              <div>
                <div className="font-bold text-slate-900">B.Tech in Computer Science Engineering</div>
                <div className="text-slate-600">Jamia Hamdard University, New Delhi</div>
              </div>
              <div className="font-medium text-slate-500">Graduating 2026</div>
            </div>
          </div>

          {/* Experience */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1">
              Professional Experience
            </h3>
            <div className="space-y-4">
              {FARJAD_PROFILE.experience.map((exp, idx) => (
                <div key={idx} className="space-y-1.5">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-bold text-slate-900">{exp.role}</div>
                      <div className="text-blue-600 font-medium">{exp.company} · {exp.location}</div>
                    </div>
                    <div className="text-slate-500 font-mono text-[11px]">{exp.duration}</div>
                  </div>
                  <ul className="list-disc list-inside space-y-1 text-slate-700">
                    {exp.bullets.map((b, bIdx) => (
                      <li key={bIdx}>{b}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Skills */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1">
              Core Technical Competencies
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {FARJAD_PROFILE.skills.map((cat, idx) => (
                <div key={idx} className="bg-slate-50 p-2.5 rounded border border-slate-200">
                  <div className="font-bold text-slate-900 mb-1">{cat.category}</div>
                  <div className="text-slate-600 text-[11px] leading-snug">
                    {cat.items.join(', ')}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-end">
          <button
            onClick={onClose}
            className="bg-slate-900 hover:bg-slate-800 text-white px-4 py-2 rounded text-xs font-semibold transition-colors"
          >
            Close Resume
          </button>
        </div>
      </div>
    </div>
  );
};
