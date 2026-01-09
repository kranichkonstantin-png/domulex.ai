'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import Link from 'next/link';
import { useDropzone } from 'react-dropzone';
import Logo from '@/components/Logo';
import UpgradeModal from '@/components/UpgradeModal';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth, db } from '@/lib/firebase';
import { doc, getDoc, updateDoc, increment } from 'firebase/firestore';
import { hasTierAccess } from '@/lib/tierUtils';

const CHAT_API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';

// Backend Contract Analysis Response Type
interface ClauseAnalysis {
  clause_type: string;
  clause_text: string;
  risk_level: 'RED' | 'YELLOW' | 'GREEN';
  legal_standard: string;
  comparison: string;
  recommendation?: string;
  source_title?: string;
  source_url?: string;
}

interface ContractAnalysisResponse {
  contract_name: string;
  jurisdiction: string;
  user_role: string;
  clauses: ClauseAnalysis[];
  overall_risk: 'RED' | 'YELLOW' | 'GREEN';
  summary: string;
  total_clauses_analyzed: number;
  red_flags: number;
  yellow_flags: number;
  green_flags: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';

const analyzeContract = async (file: File, userTier: string, userRole?: string, clientRef?: string, idToken?: string): Promise<ContractAnalysisResponse> => {
  // Erstelle FormData für Multipart Upload
  const formData = new FormData();
  formData.append('file', file);
  formData.append('jurisdiction', 'DE');
  formData.append('user_role', userRole || 'TENANT');
  formData.append('user_tier', userTier);
  if (clientRef) {
    formData.append('client_reference', clientRef);
  }

  const headers: HeadersInit = {};
  if (idToken) {
    headers['Authorization'] = `Bearer ${idToken}`;
  }

  const response = await fetch(`${API_URL}/analyze_contract`, {
    method: 'POST',
    headers,
    body: formData
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unbekannter Fehler' }));
    throw new Error(error.detail || 'Vertragsanalyse fehlgeschlagen');
  }
  
  return response.json();
};

export default function VertragsanalysePage() {
  const [user, setUser] = useState<User | null>(null);
  const [userTier, setUserTier] = useState<string>('free');
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<ContractAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedClause, setSelectedClause] = useState<ClauseAnalysis | null>(null);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [queriesUsed, setQueriesUsed] = useState(0);
  const [queriesLimit, setQueriesLimit] = useState(0);
  
  // Chat state
  const [showChat, setShowChat] = useState(false);
  const [chatMessages, setChatMessages] = useState<Array<{role: 'user' | 'assistant', content: string}>>([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  
  // Lawyer-specific state
  const [clientReference, setClientReference] = useState('');
  const [selectedRole, setSelectedRole] = useState<'TENANT' | 'LANDLORD' | 'BUYER' | 'SELLER'>('TENANT');
  const [generatingReport, setGeneratingReport] = useState(false);
  const [generatingAlternatives, setGeneratingAlternatives] = useState(false);
  const [alternativeClause, setAlternativeClause] = useState<{original: ClauseAnalysis, alternatives: string[]} | null>(null);

  // Check if user has access (Professional or Lawyer)
  const hasAccess = hasTierAccess(userTier, 'professional');
  
  // Wrapper for actions that require tier
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  // Auth & Tier Check
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      setUser(currentUser);
      if (currentUser) {
        try {
          const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
          if (userDoc.exists()) {
            const data = userDoc.data();
            const tier = data.tier || data.dashboardType || 'free';
            console.log('[ContractAnalysis] Loaded tier:', tier, 'hasAccess:', hasTierAccess(tier, 'professional'));
            setUserTier(tier);
            setQueriesUsed(data.queriesUsed || 0);
            setQueriesLimit(data.queriesLimit || 0);
          }
        } catch (e) {
          console.error('Error loading user tier:', e);
        }
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setResult(null);
      setError(null);
    }
  }, []);

  // File formats based on tier - Lawyer gets all formats
  const isLawyer = userTier === 'lawyer';
  
  // Define accepted formats as a constant to satisfy TypeScript
  const lawyerFormats: Record<string, string[]> = {
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/vnd.ms-excel': ['.xls'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
    'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff'],
    'text/plain': ['.txt'],
    'text/csv': ['.csv'],
    'text/html': ['.html', '.htm'],
    'application/rtf': ['.rtf'],
    'message/rfc822': ['.eml'],
    'application/vnd.ms-outlook': ['.msg']
  };
  
  const standardFormats: Record<string, string[]> = {
    'application/pdf': ['.pdf']
  };
  
  const formatHint = isLawyer 
    ? 'PDF, Word, Excel, Bilder, Text, HTML, RTF, E-Mail' 
    : 'PDF';

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop: (acceptedFiles: File[]) => {
      // Check tier access when file is dropped
      if (!hasAccess) {
        setShowUpgradeModal(true);
        return;
      }
      onDrop(acceptedFiles);
    },
    accept: isLawyer ? lawyerFormats : standardFormats,
    maxSize: isLawyer ? 25 * 1024 * 1024 : 10 * 1024 * 1024,
    multiple: false,
    noClick: true // Disable default click to handle manually
  });

  // Handle click on dropzone with tier check
  const handleDropzoneClick = () => {
    requireTier(() => open());
  };

  const handleAnalyze = async () => {
    if (!file || !user) return;
    
    // Check query limit (Lawyer has unlimited)
    if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
      setError('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif.');
      setShowUpgradeModal(true);
      return;
    }
    
    setAnalyzing(true);
    setError(null);
    
    try {
      // Get Firebase ID token for authentication
      const idToken = await user.getIdToken();
      const analysisResult = await analyzeContract(file, userTier, selectedRole, clientReference, idToken);
      setResult(analysisResult);
      
      // Increment query count (costs 1 query for Professional)
      if (userTier !== 'lawyer') {
        await updateDoc(doc(db, 'users', user.uid), {
          queriesUsed: increment(1)
        });
        setQueriesUsed(prev => prev + 1);
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Fehler bei der Analyse';
      setError(errorMessage);
    } finally {
      setAnalyzing(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'RED': return 'bg-red-100 text-red-800 border-red-300';
      case 'YELLOW': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'GREEN': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getRiskBadge = (risk: string) => {
    switch (risk) {
      case 'RED': return { bg: 'bg-red-500', text: '❌ Kritisch', icon: '🔴' };
      case 'YELLOW': return { bg: 'bg-yellow-500', text: '⚠️ Prüfen', icon: '🟡' };
      case 'GREEN': return { bg: 'bg-green-500', text: '✅ OK', icon: '🟢' };
      default: return { bg: 'bg-gray-500', text: 'Unbekannt', icon: '⚪' };
    }
  };

  // Alle User haben Zugang - Anfragen-Limit wird über queriesUsed/queriesLimit kontrolliert
  // (Free: 3, Basis: 50, Professional: 250, Lawyer: unbegrenzt)

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="animate-spin text-4xl">⚙️</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-[106px]">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">← Dashboard</Link>
              <Logo size="sm" />
            </div>
            <h1 className="text-lg font-semibold text-[#1e3a5f]">KI-Vertragsanalyse</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        <>
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-[#1e3a5f]">KI-Vertragsanalyse</h1>
            <p className="text-gray-600 mt-2">Laden Sie Ihren Vertrag hoch und erhalten Sie eine detaillierte rechtliche Analyse</p>
          </div>

          {/* Locked view for FREE users */}
          {!hasAccess && (
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8 mb-6">
              <div className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center bg-gray-50">
                <p className="text-4xl mb-4">🔒</p>
                <p className="text-lg font-medium text-gray-700">Diese Funktion erfordert ein Upgrade</p>
                <p className="text-sm text-gray-500 mt-2">Die KI-Vertragsanalyse ist ab dem Professional-Tarif verfügbar.</p>
                <button
                  onClick={() => setShowUpgradeModal(true)}
                  className="mt-6 px-6 py-3 bg-[#1e3a5f] text-white rounded-lg font-medium hover:bg-[#2d4a6f] transition-colors"
                >
                  🚀 Jetzt upgraden
                </button>
              </div>
            </div>
          )}

          {hasAccess && !result && (
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8 mb-6">
              <div {...getRootProps()} onClick={handleDropzoneClick} className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${isDragActive ? 'border-[#1e3a5f] bg-[#1e3a5f]/5' : file ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-[#1e3a5f]'}`}>
                <input {...getInputProps()} />
                {file ? (
                  <div>
                    <p className="text-4xl mb-4">📄</p>
                    <p className="text-lg font-medium text-[#1e3a5f]">{file.name}</p>
                    <p className="text-sm text-gray-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    <p className="text-sm text-green-600 mt-3">✓ Datei bereit zur Analyse</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-4xl mb-4">📤</p>
                    <p className="text-lg font-medium text-gray-700">{isDragActive ? 'Datei hier ablegen...' : 'Vertrag hochladen'}</p>
                    <p className="text-sm text-gray-500 mt-2">Ziehen Sie eine Datei hierher oder klicken Sie zum Auswählen</p>
                    <p className="text-xs text-gray-400 mt-4">Formate: {formatHint} • Max. {isLawyer ? '25' : '10'} MB</p>
                  </div>
                )}
              </div>

              {/* Lawyer-specific options */}
              {isLawyer && file && (
                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-[#1e3a5f]/5 rounded-xl border border-[#1e3a5f]/20">
                  <div>
                    <label className="block text-sm font-medium text-[#1e3a5f] mb-2">⚖️ Mandantenrolle</label>
                    <select 
                      value={selectedRole} 
                      onChange={(e) => setSelectedRole(e.target.value as 'TENANT' | 'LANDLORD' | 'BUYER' | 'SELLER')}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                    >
                      <option value="TENANT">Mieter</option>
                      <option value="LANDLORD">Vermieter</option>
                      <option value="BUYER">Käufer</option>
                      <option value="SELLER">Verkäufer</option>
                    </select>
                    <p className="text-xs text-gray-500 mt-1">Analyse aus Sicht Ihres Mandanten</p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-[#1e3a5f] mb-2">📁 Mandantenreferenz (optional)</label>
                    <input 
                      type="text" 
                      value={clientReference} 
                      onChange={(e) => setClientReference(e.target.value)}
                      placeholder="z.B. Aktenzeichen, Mandantenname..."
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                    />
                    <p className="text-xs text-gray-500 mt-1">Erscheint im Gutachten-Export</p>
                  </div>
                </div>
              )}

              {file && (
                  <div className="mt-6 flex flex-col sm:flex-row gap-4">
                    <button onClick={() => { setFile(null); setResult(null); }} className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">
                      Andere Datei wählen
                    </button>
                    <button onClick={handleAnalyze} disabled={analyzing} className="flex-1 px-6 py-3 bg-[#1e3a5f] text-white rounded-lg hover:bg-[#2d4a6f] disabled:opacity-50 font-medium">
                      {analyzing ? (
                        <span className="flex items-center justify-center gap-2">
                          <span className="animate-spin">⚙️</span>
                          Analysiere... (kann 30-60 Sekunden dauern)
                        </span>
                      ) : '🔍 Vertrag analysieren'}
                    </button>
                  </div>
                )}
                {file && userTier !== 'lawyer' && (
                  <p className="text-xs text-orange-600 mt-2 text-center">Verbraucht 1 Anfrage ({queriesLimit - queriesUsed} übrig)</p>
                )}

                {error && (
                  <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                    <p className="font-medium">Fehler bei der Analyse</p>
                    <p className="text-sm mt-1">{error}</p>
                  </div>
                )}
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {/* Übersicht */}
                <div className={`rounded-xl border-2 p-6 ${getRiskColor(result.overall_risk)}`}>
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold flex items-center gap-2">
                      {getRiskBadge(result.overall_risk).icon} Gesamtbewertung
                    </h2>
                    <span className={`px-3 py-1 rounded-full text-white text-sm font-medium ${getRiskBadge(result.overall_risk).bg}`}>
                      {getRiskBadge(result.overall_risk).text}
                    </span>
                  </div>
                  <p className="text-gray-700">{result.summary}</p>
                  <div className="grid grid-cols-3 gap-2 sm:gap-4 mt-4">
                    <div className="text-center p-2 sm:p-3 bg-white/50 rounded-lg">
                      <p className="text-xl sm:text-2xl font-bold text-red-600">{result.red_flags}</p>
                      <p className="text-[10px] sm:text-xs text-gray-600">Kritisch</p>
                    </div>
                    <div className="text-center p-2 sm:p-3 bg-white/50 rounded-lg">
                      <p className="text-xl sm:text-2xl font-bold text-yellow-600">{result.yellow_flags}</p>
                      <p className="text-[10px] sm:text-xs text-gray-600">Zu prüfen</p>
                    </div>
                    <div className="text-center p-2 sm:p-3 bg-white/50 rounded-lg">
                      <p className="text-xl sm:text-2xl font-bold text-green-600">{result.green_flags}</p>
                      <p className="text-[10px] sm:text-xs text-gray-600">In Ordnung</p>
                    </div>
                  </div>
                </div>

                {/* Klausel-Liste */}
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">
                    📋 Analysierte Klauseln ({result.total_clauses_analyzed})
                  </h2>
                  <div className="space-y-3">
                    {result.clauses.map((clause, index) => (
                      <div 
                        key={index}
                        onClick={() => setSelectedClause(selectedClause === clause ? null : clause)}
                        className={`p-4 rounded-lg border cursor-pointer transition-all hover:shadow-md ${getRiskColor(clause.risk_level)} ${selectedClause === clause ? 'ring-2 ring-[#1e3a5f]' : ''}`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className="text-xl">{getRiskBadge(clause.risk_level).icon}</span>
                            <div>
                              <p className="font-medium">{clause.clause_type}</p>
                              <p className="text-xs text-gray-600 truncate max-w-md">
                                {clause.clause_text.substring(0, 80)}...
                              </p>
                            </div>
                          </div>
                          <span className="text-sm">{selectedClause === clause ? '▼' : '▶'}</span>
                        </div>
                        
                        {selectedClause === clause && (
                          <div className="mt-4 pt-4 border-t border-current/20 space-y-3">
                            <div>
                              <p className="text-xs font-medium uppercase text-gray-500 mb-1">Klauseltext</p>
                              <p className="text-sm bg-white/50 p-2 rounded">{clause.clause_text}</p>
                            </div>
                            <div>
                              <p className="text-xs font-medium uppercase text-gray-500 mb-1">Bewertung</p>
                              <p className="text-sm">{clause.comparison}</p>
                            </div>
                            {clause.recommendation && (
                              <div>
                                <p className="text-xs font-medium uppercase text-gray-500 mb-1">💡 Empfehlung</p>
                                <p className="text-sm font-medium">{clause.recommendation}</p>
                              </div>
                            )}
                            <div>
                              <p className="text-xs font-medium uppercase text-gray-500 mb-1">Rechtliche Grundlage</p>
                              <p className="text-sm text-gray-600">{clause.legal_standard}</p>
                              {clause.source_url && (
                                <a 
                                  href={clause.source_url} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="text-xs text-blue-600 hover:underline mt-1 block"
                                >
                                  📚 {clause.source_title || 'Quelle ansehen'}
                                </a>
                              )}
                            </div>
                            
                            {/* Lawyer-only: Generate alternative clause */}
                            {isLawyer && clause.risk_level !== 'GREEN' && (
                              <div className="pt-3 border-t border-current/20">
                                <button
                                  onClick={async (e) => {
                                    e.stopPropagation();
                                    setGeneratingAlternatives(true);
                                    try {
                                      const response = await fetch(`${API_URL}/generate_alternative_clause`, {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify({
                                          clause_text: clause.clause_text,
                                          clause_type: clause.clause_type,
                                          user_role: selectedRole,
                                          risk_level: clause.risk_level
                                        })
                                      });
                                      if (response.ok) {
                                        const data = await response.json();
                                        setAlternativeClause({ original: clause, alternatives: data.alternatives || [] });
                                      }
                                    } catch (err) {
                                      console.error('Error generating alternatives:', err);
                                    } finally {
                                      setGeneratingAlternatives(false);
                                    }
                                  }}
                                  disabled={generatingAlternatives}
                                  className="text-xs px-3 py-1.5 bg-[#1e3a5f] text-white rounded hover:bg-[#2d4a6f] disabled:opacity-50"
                                >
                                  {generatingAlternatives ? '⏳ Generiere...' : '✏️ Alternative Klausel generieren'}
                                </button>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Alternative Clause Modal for Lawyers */}
                {alternativeClause && isLawyer && (
                  <div className="bg-white rounded-xl border border-[#1e3a5f]/30 shadow-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-[#1e3a5f]">✏️ Alternative Klauselvorschläge</h3>
                      <button onClick={() => setAlternativeClause(null)} className="text-gray-400 hover:text-gray-600">✕</button>
                    </div>
                    <div className="mb-4 p-3 bg-red-50 rounded-lg">
                      <p className="text-xs font-medium text-red-600 mb-1">Original ({alternativeClause.original.clause_type})</p>
                      <p className="text-sm text-gray-700">{alternativeClause.original.clause_text}</p>
                    </div>
                    <div className="space-y-3">
                      {alternativeClause.alternatives.map((alt, idx) => (
                        <div key={idx} className="p-3 bg-green-50 rounded-lg border border-green-200">
                          <p className="text-xs font-medium text-green-600 mb-1">Alternative {idx + 1}</p>
                          <p className="text-sm text-gray-700">{alt}</p>
                          <button 
                            onClick={() => navigator.clipboard.writeText(alt)}
                            className="text-xs text-[#1e3a5f] hover:underline mt-2"
                          >
                            📋 In Zwischenablage kopieren
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Aktionen */}
                <div className="flex flex-wrap gap-4">
                  <button 
                    onClick={() => { setFile(null); setResult(null); setSelectedClause(null); setShowChat(false); setChatMessages([]); setAlternativeClause(null); }} 
                    className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                  >
                    📄 Neuen Vertrag analysieren
                  </button>
                  
                  {/* Lawyer-only: Export as PDF report */}
                  {isLawyer && (
                    <button 
                      onClick={async () => {
                        setGeneratingReport(true);
                        try {
                          const response = await fetch(`${API_URL}/export_contract_report`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                              analysis: result,
                              client_reference: clientReference,
                              user_role: selectedRole
                            })
                          });
                          if (response.ok) {
                            const blob = await response.blob();
                            const url = window.URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `Rechtsgutachten_${result.contract_name}_${new Date().toISOString().split('T')[0]}.pdf`;
                            a.click();
                            window.URL.revokeObjectURL(url);
                          }
                        } catch (err) {
                          console.error('Export error:', err);
                          setError('PDF-Export fehlgeschlagen');
                        } finally {
                          setGeneratingReport(false);
                        }
                      }}
                      disabled={generatingReport}
                      className="px-6 py-3 bg-amber-600 text-white rounded-lg hover:bg-amber-700 disabled:opacity-50"
                    >
                      {generatingReport ? '⏳ Erstelle PDF...' : '📥 Als Gutachten exportieren (PDF)'}
                    </button>
                  )}
                  
                  {hasTierAccess(userTier, 'professional') && (
                    <button 
                      onClick={() => setShowChat(!showChat)} 
                      className={`px-6 py-3 rounded-lg transition-colors ${showChat ? 'bg-gray-200 text-gray-700' : 'bg-[#1e3a5f] text-white hover:bg-[#2d4a6f]'}`}
                    >
                      🤖 {showChat ? 'Chat ausblenden' : 'Mit KI über Vertrag sprechen'}
                    </button>
                  )}
                </div>

                {/* Integrierter Chat */}
                {showChat && (
                  <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                    <div className="bg-[#1e3a5f] text-white px-4 py-3 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-xl">💬</span>
                        <span className="font-medium">Vertrag besprechen</span>
                      </div>
                      <span className="text-xs text-white/70">Basierend auf der Analyse oben</span>
                    </div>
                    
                    {/* Chat Messages */}
                    <div data-chat-container className="h-80 overflow-y-auto p-4 space-y-4 bg-gray-50">
                      {chatMessages.length === 0 && (
                        <div className="text-center text-gray-500 py-8">
                          <p className="text-lg mb-2">🤖</p>
                          <p className="text-sm">Stellen Sie Fragen zu Ihrem Vertrag.</p>
                          <p className="text-xs mt-1">z.B. &quot;Ist die Zwangsvollstreckungsklausel üblich?&quot;</p>
                          <p className="text-xs mt-3 text-orange-600 font-medium">⚠️ Nur vertragsbezogene Fragen - jede Anfrage verbraucht Ihr Kontingent!</p>
                        </div>
                      )}
                      {chatMessages.map((msg, idx) => (
                        <div key={idx} data-chat-message data-user-message={msg.role === 'user' && idx === chatMessages.length - 2 ? "true" : undefined} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                          <div className={`max-w-[80%] rounded-lg px-4 py-2 ${msg.role === 'user' ? 'bg-[#1e3a5f] text-white' : 'bg-white border border-gray-200 text-gray-800'}`}>
                            <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                          </div>
                        </div>
                      ))}
                      {chatLoading && (
                        <div className="flex justify-start">
                          <div className="bg-white border border-gray-200 rounded-lg px-4 py-2">
                            <div className="flex gap-1">
                              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></span>
                              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></span>
                              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></span>
                            </div>
                          </div>
                        </div>
                      )}
                      <div ref={chatEndRef} />
                    </div>
                    
                    {/* Chat Input */}
                    <div className="border-t border-gray-200 p-4">
                      <form onSubmit={async (e) => {
                        e.preventDefault();
                        if (!chatInput.trim() || chatLoading || !user) return;
                        
                        // Check query limit (Lawyer has unlimited)
                        if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
                          setChatMessages(prev => [...prev, { role: 'assistant', content: 'Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für weitere Fragen.' }]);
                          setShowUpgradeModal(true);
                          return;
                        }
                        
                        const userMessage = chatInput.trim();
                        setChatInput('');
                        setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);
                        setChatLoading(true);
                        
                        // Scroll to see user message
                        setTimeout(() => {
                          const container = document.querySelector('[data-chat-container]');
                          if (container) {
                            container.scrollTop = container.scrollHeight;
                          }
                        }, 100);
                        
                        try {
                          // Build context from analysis
                          const analysisContext = result ? `
VERTRAGSANALYSE-KONTEXT:
Vertrag: ${result.contract_name}
Gesamtbewertung: ${result.overall_risk === 'RED' ? 'Kritisch' : result.overall_risk === 'YELLOW' ? 'Prüfenswert' : 'Unbedenklich'}
Zusammenfassung: ${result.summary}

Analysierte Klauseln:
${result.clauses.map(c => `- ${c.clause_type} (${c.risk_level}): ${c.clause_text.substring(0, 200)}...
  Bewertung: ${c.comparison}
  Empfehlung: ${c.recommendation || 'Keine'}`).join('\n\n')}
` : '';
                          
                          const response = await fetch(`${CHAT_API_URL}/query`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                              query: `${analysisContext}\n\nNUTZERFRAGE ZUM VERTRAG:\n${userMessage}`,
                              user_role: 'TENANT',
                              target_jurisdiction: 'DE',
                              user_language: 'de'
                            })
                          });
                          
                          if (!response.ok) throw new Error('Fehler bei der Anfrage');
                          
                          const data = await response.json();
                          setChatMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
                          
                          // Update query count (only for non-lawyer)
                          if (userTier !== 'lawyer') {
                            await updateDoc(doc(db, 'users', user.uid), {
                              queriesUsed: increment(1)
                            });
                            setQueriesUsed(prev => prev + 1);
                          }
                        } catch (err) {
                          console.error('Chat error:', err);
                          setChatMessages(prev => [...prev, { role: 'assistant', content: 'Entschuldigung, es gab einen Fehler. Bitte versuchen Sie es erneut.' }]);
                        } finally {
                          setChatLoading(false);
                          setTimeout(() => {
                            // Scroll zur User-Frage mit 80px Offset, damit Nutzer Frage oben sieht
                            const chatContainer = document.querySelector('[data-chat-container]');
                            const userMessage = document.querySelector('[data-user-message="true"]');
                            if (userMessage && chatContainer) {
                              const rect = userMessage.getBoundingClientRect();
                              const containerRect = chatContainer.getBoundingClientRect();
                              const scrollOffset = rect.top - containerRect.top + (chatContainer as HTMLElement).scrollTop - 80;
                              (chatContainer as HTMLElement).scrollTo({ top: scrollOffset, behavior: 'smooth' });
                            }
                          }, 100);
                        }
                      }} className="flex gap-2">
                        <input
                          type="text"
                          value={chatInput}
                          onChange={(e) => setChatInput(e.target.value)}
                          placeholder="Frage zum Vertrag stellen..."
                          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                          disabled={chatLoading}
                        />
                        <button
                          type="submit"
                          disabled={chatLoading || !chatInput.trim()}
                          className="px-4 py-2 bg-[#1e3a5f] text-white rounded-lg hover:bg-[#2d4a6f] disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          Senden
                        </button>
                      </form>
                      <p className="text-xs text-gray-500 mt-2">
                        💡 Die KI hat Zugriff auf die komplette Vertragsanalyse oben.
                        {userTier !== 'lawyer' && (
                          <span className="ml-2 text-orange-600">
                            ({queriesLimit - queriesUsed} Anfragen übrig)
                          </span>
                        )}
                      </p>
                    </div>
                  </div>
                )}

                {/* Rechtlicher Hinweis */}
                <div className="bg-amber-50 rounded-xl p-4 text-sm text-amber-800">
                  <p className="font-medium mb-1">⚖️ Rechtlicher Hinweis</p>
                  <p>Diese KI-gestützte Analyse ersetzt keine Rechtsberatung. Bei komplexen Fragen oder wichtigen Entscheidungen sollten Sie einen Rechtsanwalt konsultieren.</p>
                </div>
              </div>
            )}

            {!result && !file && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <p className="text-2xl mb-3">🔍</p>
                  <h3 className="font-semibold text-[#1e3a5f]">Klausel-Erkennung</h3>
                  <p className="text-sm text-gray-600 mt-2">KI identifiziert automatisch alle wichtigen Klauseln in Ihrem Vertrag</p>
                </div>
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <p className="text-2xl mb-3">⚖️</p>
                  <h3 className="font-semibold text-[#1e3a5f]">Rechtsprüfung</h3>
                  <p className="text-sm text-gray-600 mt-2">Vergleich mit aktueller BGH-Rechtsprechung und BGB-Vorgaben</p>
                </div>
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <p className="text-2xl mb-3">💡</p>
                  <h3 className="font-semibold text-[#1e3a5f]">Handlungsempfehlungen</h3>
                  <p className="text-sm text-gray-600 mt-2">Konkrete Empfehlungen für Verhandlungen oder rechtliche Schritte</p>
                </div>
              </div>
            )}
          </>
      </div>

      {/* Upgrade Modal for non-lawyer users */}
      <UpgradeModal 
        isOpen={showUpgradeModal} 
        onClose={() => setShowUpgradeModal(false)}
        feature="KI-Vertragsanalyse"
        requiredTier="lawyer"
      />
    </div>
  );
}
