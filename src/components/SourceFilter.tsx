'use client';

import { useState } from 'react';

export interface SourceFilterOptions {
  gesetz: boolean;
  urteil: boolean;
  literatur: boolean;
  verwaltung: boolean;
  gerichtsebene: {
    eugh: boolean;
    bgh: boolean;
    bfh: boolean;
    fg: boolean;      // NEU: Finanzgerichte
    olg: boolean;
    lg: boolean;
    ag: boolean;
    vg: boolean;      // NEU: Verwaltungsgerichte
    ovg: boolean;     // NEU: Oberverwaltungsgerichte
  };
}

interface SourceFilterProps {
  value: SourceFilterOptions;
  onChange: (filters: SourceFilterOptions) => void;
}

const DEFAULT_FILTERS: SourceFilterOptions = {
  gesetz: true,
  urteil: true,
  literatur: true,
  verwaltung: true,
  gerichtsebene: {
    eugh: true,
    bgh: true,
    bfh: true,
    fg: true,       // NEU: Finanzgerichte
    olg: true,
    lg: true,
    ag: true,
    vg: true,       // NEU: Verwaltungsgerichte
    ovg: true,      // NEU: Oberverwaltungsgerichte
  },
};

export default function SourceFilter({ value, onChange }: SourceFilterProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleSource = (source: keyof Omit<SourceFilterOptions, 'gerichtsebene'>) => {
    onChange({
      ...value,
      [source]: !value[source],
    });
  };

  const toggleGerichtsebene = (ebene: keyof SourceFilterOptions['gerichtsebene']) => {
    onChange({
      ...value,
      gerichtsebene: {
        ...value.gerichtsebene,
        [ebene]: !value.gerichtsebene[ebene],
      },
    });
  };

  const selectAll = () => {
    onChange(DEFAULT_FILTERS);
  };

  const deselectAll = () => {
    onChange({
      gesetz: false,
      urteil: false,
      literatur: false,
      verwaltung: false,
      gerichtsebene: {
        eugh: false,
        bgh: false,
        bfh: false,
        fg: false,
        olg: false,
        lg: false,
        ag: false,
        vg: false,
        ovg: false,
      },
    });
  };

  // Count active filters
  const activeFilters = 
    (value.gesetz ? 1 : 0) +
    (value.literatur ? 1 : 0) +
    (value.verwaltung ? 1 : 0) +
    (value.urteil && (value.gerichtsebene.eugh || value.gerichtsebene.bgh || value.gerichtsebene.bfh || value.gerichtsebene.fg || value.gerichtsebene.olg || value.gerichtsebene.lg || value.gerichtsebene.ag || value.gerichtsebene.vg || value.gerichtsebene.ovg) ? 1 : 0);

  return (
    <div className="border border-gray-200 rounded-lg bg-white shadow-sm">
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition-colors rounded-lg"
      >
        <div className="flex items-center gap-2">
          <svg className="w-5 h-5 text-[#b8860b]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <span className="font-medium text-gray-900">Quellenfilter</span>
          <span className="text-xs px-2 py-0.5 bg-[#b8860b]/10 text-[#b8860b] rounded-full font-medium">
            {activeFilters} aktiv
          </span>
        </div>
        <svg
          className={`w-5 h-5 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-4 pb-4 space-y-4 border-t border-gray-100">
          {/* Quick Actions */}
          <div className="flex gap-2 pt-3">
            <button
              onClick={selectAll}
              className="flex-1 px-3 py-1.5 text-xs font-medium text-[#b8860b] border border-[#b8860b] rounded-md hover:bg-[#b8860b]/5 transition-colors"
            >
              Alle auswählen
            </button>
            <button
              onClick={deselectAll}
              className="flex-1 px-3 py-1.5 text-xs font-medium text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            >
              Alle abwählen
            </button>
          </div>

          {/* Document Types */}
          <div>
            <h4 className="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide">Dokumenttypen</h4>
            <div className="space-y-2">
              <label className="flex items-center gap-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                <input
                  type="checkbox"
                  checked={value.gesetz}
                  onChange={() => toggleSource('gesetz')}
                  className="w-4 h-4 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                />
                <div className="flex-1">
                  <span className="text-sm font-medium text-gray-900">Gesetze</span>
                  <p className="text-xs text-gray-500">BGB, WEG, BauGB, GrEStG, EStG, UStG, BetrKV + 16 LBOs</p>
                </div>
              </label>

              <label className="flex items-center gap-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                <input
                  type="checkbox"
                  checked={value.literatur}
                  onChange={() => toggleSource('literatur')}
                  className="w-4 h-4 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                />
                <div className="flex-1">
                  <span className="text-sm font-medium text-gray-900">Literatur</span>
                  <p className="text-xs text-gray-500">1.900+ Kommentare: Palandt, MüKo, Staudinger, Schmidt</p>
                </div>
              </label>

              <label className="flex items-center gap-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                <input
                  type="checkbox"
                  checked={value.verwaltung}
                  onChange={() => toggleSource('verwaltung')}
                  className="w-4 h-4 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                />
                <div className="flex-1">
                  <span className="text-sm font-medium text-gray-900">Verwaltungsrecht</span>
                  <p className="text-xs text-gray-500">750+ BMF-Schreiben, EStR, UStAE, GrEStR, ErbStR</p>
                </div>
              </label>

              <div className="border-l-2 border-gray-200 pl-4">
                <label className="flex items-center gap-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={value.urteil}
                    onChange={() => toggleSource('urteil')}
                    className="w-4 h-4 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                  />
                  <div className="flex-1">
                    <span className="text-sm font-medium text-gray-900">Rechtsprechung</span>
                    <p className="text-xs text-gray-500">Urteile: EuGH, BGH, BFH, FG, OLG, LG, AG, VG, OVG</p>
                  </div>
                </label>

                {/* Gerichtsebenen (nur sichtbar wenn Urteil aktiv) */}
                {value.urteil && (
                  <div className="mt-2 ml-6 space-y-1.5 bg-gray-50 p-3 rounded-md">
                    <h5 className="text-xs font-semibold text-gray-600 mb-2">Gerichtsebenen</h5>
                    
                    {/* Höchstgerichte */}
                    <p className="text-xs font-bold text-green-700 mt-1">✓ Höchstgerichte (verbindlich)</p>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.eugh}
                        onChange={() => toggleGerichtsebene('eugh')}
                        className="w-3.5 h-3.5 text-[#1e3a5f] border-gray-300 rounded focus:ring-[#1e3a5f]"
                      />
                      <span className="text-xs text-gray-700">🇪🇺 EuGH (Europäischer Gerichtshof)</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.bgh}
                        onChange={() => toggleGerichtsebene('bgh')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">BGH (Bundesgerichtshof) - 2.700+ Urteile</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.bfh}
                        onChange={() => toggleGerichtsebene('bfh')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">BFH (Bundesfinanzhof) - 1.100+ Urteile</span>
                    </label>
                    
                    {/* Finanzgerichtsbarkeit */}
                    <div className="border-t border-gray-200 my-2"></div>
                    <p className="text-xs font-bold text-blue-700">💰 Finanzgerichtsbarkeit</p>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.fg}
                        onChange={() => toggleGerichtsebene('fg')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">FG (Finanzgerichte) - 2.400+ Urteile</span>
                    </label>
                    
                    {/* Ordentliche Gerichtsbarkeit */}
                    <div className="border-t border-gray-200 my-2"></div>
                    <p className="text-xs font-bold text-gray-600">⚖️ Ordentliche Gerichtsbarkeit</p>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.olg}
                        onChange={() => toggleGerichtsebene('olg')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">OLG (Oberlandesgerichte) - 2.000+ Urteile</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.lg}
                        onChange={() => toggleGerichtsebene('lg')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">LG (Landgerichte) - 2.520+ Urteile</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.ag}
                        onChange={() => toggleGerichtsebene('ag')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">AG (Amtsgerichte) - 9.000+ Urteile</span>
                    </label>
                    
                    {/* Verwaltungsgerichtsbarkeit */}
                    <div className="border-t border-gray-200 my-2"></div>
                    <p className="text-xs font-bold text-purple-700">🏛️ Verwaltungsgerichtsbarkeit</p>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.ovg}
                        onChange={() => toggleGerichtsebene('ovg')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">OVG/VGH (Oberverwaltungsgerichte) - 800+ Urteile</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={value.gerichtsebene.vg}
                        onChange={() => toggleGerichtsebene('vg')}
                        className="w-3.5 h-3.5 text-[#b8860b] border-gray-300 rounded focus:ring-[#b8860b]"
                      />
                      <span className="text-xs text-gray-700">VG (Verwaltungsgerichte) - 1.240+ Urteile</span>
                    </label>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Helper function to convert filter options to API format
export function filtersToApiFormat(filters: SourceFilterOptions): { 
  source_filter: string[] | null; 
  gerichtsebene_filter: string[] | null;
} {
  const docTypes: string[] = [];
  
  if (filters.gesetz) docTypes.push('GESETZ');
  if (filters.literatur) docTypes.push('LITERATUR');
  if (filters.verwaltung) docTypes.push('VERWALTUNG');
  
  // For Urteile, only include if at least one Gerichtsebene is selected
  if (filters.urteil) {
    if (filters.gerichtsebene.eugh || filters.gerichtsebene.bgh || filters.gerichtsebene.bfh || 
        filters.gerichtsebene.fg || filters.gerichtsebene.olg || filters.gerichtsebene.lg || 
        filters.gerichtsebene.ag || filters.gerichtsebene.vg || filters.gerichtsebene.ovg) {
      docTypes.push('URTEIL');
    }
  }
  
  // Build gerichtsebene filter
  const gerichtsebenen: string[] = [];
  if (filters.urteil) {
    if (filters.gerichtsebene.eugh) gerichtsebenen.push('EuGH');
    if (filters.gerichtsebene.bgh) gerichtsebenen.push('BGH');
    if (filters.gerichtsebene.bfh) gerichtsebenen.push('BFH');
    if (filters.gerichtsebene.fg) gerichtsebenen.push('FG');
    if (filters.gerichtsebene.olg) gerichtsebenen.push('OLG');
    if (filters.gerichtsebene.lg) gerichtsebenen.push('LG');
    if (filters.gerichtsebene.ag) gerichtsebenen.push('AG');
    if (filters.gerichtsebene.vg) gerichtsebenen.push('VG');
    if (filters.gerichtsebene.ovg) gerichtsebenen.push('OVG');
  }
  
  // If all types are selected, return null (no filter)
  const sourceFilter = docTypes.length === 4 ? null : (docTypes.length === 0 ? [] : docTypes);
  
  // If all Gerichtsebenen selected (9) or none, return null
  const gerichtsebeneFilter = gerichtsebenen.length === 0 || gerichtsebenen.length === 9 ? null : gerichtsebenen;
  
  return {
    source_filter: sourceFilter,
    gerichtsebene_filter: gerichtsebeneFilter,
  };
}
