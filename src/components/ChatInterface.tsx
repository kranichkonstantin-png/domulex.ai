'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { QueryRequest, QueryResponse, apiClient, LegalDocument, QuotaExceededError } from '@/lib/api';
import { checkAnonymousQueryLimit, incrementAnonymousQuery } from '@/lib/ip-limit';
import { onAuthChange, getUserProfile } from '@/lib/auth';
import { User } from 'firebase/auth';
import { auth } from '@/lib/firebase';
import AuthModal from './AuthModal';
import UpgradeModal from './UpgradeModal';
import SourceFilter, { SourceFilterOptions, filtersToApiFormat } from './SourceFilter';
import { FileUpload } from './FileUpload';

// Hilfsfunktion: Generiere Link für Rechtsquellen
const generateSourceUrl = (source: LegalDocument): string => {
  // Wenn bereits URL vorhanden und nicht leer
  if (source.source_url && source.source_url.trim() !== '') {
    return source.source_url;
  }
  
  const title = source.title || '';
  const docType = source.document_type || '';
  
  // BGB Paragraphen → gesetze-im-internet.de
  if (title.includes('BGB §') || title.includes('§') && title.includes('BGB')) {
    const match = title.match(/§\s*(\d+[a-z]?)/i);
    if (match) {
      return `https://www.gesetze-im-internet.de/bgb/__${match[1]}.html`;
    }
  }
  
  // WEG Paragraphen
  if (title.includes('WEG §') || (title.includes('§') && title.includes('WEG'))) {
    const match = title.match(/§\s*(\d+[a-z]?)/i);
    if (match) {
      return `https://www.gesetze-im-internet.de/woeigg/__${match[1]}.html`;
    }
  }
  
  // MietNovG, BauGB etc.
  if (title.includes('BauGB §')) {
    const match = title.match(/§\s*(\d+[a-z]?)/i);
    if (match) {
      return `https://www.gesetze-im-internet.de/bbaug/__${match[1]}.html`;
    }
  }
  
  // BGH Urteile → bundesgerichtshof.de
  if (docType === 'URTEIL' && title.includes('BGH')) {
    const azMatch = title.match(/([IVX]+)\s*ZR\s*(\d+)\/(\d+)/i);
    if (azMatch) {
      return `https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/${azMatch[1]}_ZR_${azMatch[2]}/${azMatch[3]}`;
    }
  }
  
  // BFH Urteile
  if (docType === 'URTEIL' && title.includes('BFH')) {
    return `https://www.bundesfinanzhof.de/de/entscheidungen/`;
  }
  
  // Allgemeine Gesetzes-Suche
  if (docType === 'GESETZ' || title.includes('§')) {
    return `https://www.gesetze-im-internet.de/`;
  }
  
  // Keine URL generierbar
  return '';
};

// Re-use UploadedDocument interface from FileUpload (shared type)
interface UploadedDocument {
  id: string;
  filename: string;
  doc_type: string;
  char_count: number;
  word_count: number;
  ocr_applied: boolean;
  extracted_text_preview?: string;
  extracted_text_full?: string;  // Full text for analysis
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: LegalDocument[];
  warning?: string;
}

interface ChatInterfaceProps {
  jurisdiction: 'DE' | 'ES' | 'US';
  role: string; // Flexible Rollen: INVESTOR, LANDLORD, TENANT, OWNER, MANAGER, MIETER, EIGENTUEMER, VERMIETER, ANWALT, VERWALTER
  language: 'de' | 'es' | 'en';
  subJurisdiction?: string;
  initialMessage?: string; // Optionaler initialer Prompt aus URL
}

// Konstanten für Free-Tier-Limits
const FREE_QUERIES_BEFORE_REGISTER = 3;  // 3 Anfragen ohne Registrierung (IP-basiert)
const FREE_QUERIES_BEFORE_UPGRADE = 3;   // 3 Anfragen als registrierter Free-User

// Mock-Auth-Status ersetzt durch echte Firebase Auth
const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [userProfile, setUserProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const unsubscribe = onAuthChange(async (firebaseUser) => {
      setUser(firebaseUser);
      
      if (firebaseUser) {
        const profile = await getUserProfile(firebaseUser.uid);
        setUserProfile(profile);
      } else {
        setUserProfile(null);
      }
      
      setLoading(false);
    });
    
    return () => unsubscribe();
  }, []);
  
  const isLoggedIn = !!user;
  // WICHTIG: "tier" (neu) hat Vorrang vor "plan" (alt) für Kompatibilität
  const userPlan = userProfile?.tier || userProfile?.plan || 'free';
  
  return { isLoggedIn, userPlan, user, userProfile, loading };
};

// Query-Counter Hook mit Fingerprint-basiertem Tracking
const useQueryCounter = (isLoggedIn: boolean, userProfile: any) => {
  const [queryCount, setQueryCount] = useState(0);
  const [canQuery, setCanQuery] = useState(true);
  
  useEffect(() => {
    if (!isLoggedIn) {
      // Für Gäste: Browser-Fingerprint-basiertes Limit
      const { queriesUsed, canQuery: allowed } = checkAnonymousQueryLimit();
      setQueryCount(queriesUsed);
      setCanQuery(allowed);
    } else if (userProfile) {
      // Für eingeloggte User: Daten aus Firestore
      setQueryCount(userProfile.queriesUsed || 0);
      setCanQuery(userProfile.queriesUsed < userProfile.queriesLimit);
    }
  }, [isLoggedIn, userProfile]);
  
  const incrementQuery = async () => {
    if (!isLoggedIn) {
      // Fingerprint-basiertes Inkrement
      const success = incrementAnonymousQuery();
      if (success) {
        setQueryCount(prev => prev + 1);
        const { canQuery: allowed } = checkAnonymousQueryLimit();
        setCanQuery(allowed);
      } else {
        setCanQuery(false);
      }
    } else if (userProfile) {
      // Optimistisches Update für eingeloggte User
      const newCount = queryCount + 1;
      setQueryCount(newCount);
      setCanQuery(newCount < userProfile.queriesLimit);
    }
  };
  
  return { queryCount, incrementQuery, ipLimitReached: !canQuery };
};

// Query-Counter Badge
function QueryBadge({ current, max, isUnlimited }: { current: number; max: number; isUnlimited: boolean }) {
  if (isUnlimited) {
    return (
      <div className="flex items-center gap-2 px-3 py-1 bg-green-500/20 rounded-full border border-green-500">
        <span className="text-green-300 text-sm font-medium">∞ Unbegrenzt</span>
      </div>
    );
  }
  
  const remaining = Math.max(0, max - current);
  const isLow = remaining <= 1;
  
  return (
    <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${
      isLow ? 'bg-red-500/20 border-red-400' : 'bg-white/10 border-white/30'
    }`}>
      <span className={`text-sm font-medium ${isLow ? 'text-red-300' : 'text-white'}`}>
        {remaining} von {max} Anfragen übrig
      </span>
    </div>
  );
}

export default function ChatInterface({
  jurisdiction,
  role,
  language,
  subJurisdiction,
  initialMessage,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [uploadedDocuments, setUploadedDocuments] = useState<UploadedDocument[]>([]);
  const [initialMessageSent, setInitialMessageSent] = useState(false);
  const [sourceFilters, setSourceFilters] = useState<SourceFilterOptions>({
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
  });
  const [usePublicSources, setUsePublicSources] = useState(false);  // 🔑 Toggle für öffentliche Quellen
  
  const { isLoggedIn, userPlan, user, userProfile } = useAuth();
  const { queryCount, incrementQuery, ipLimitReached } = useQueryCounter(isLoggedIn, userProfile);
  
  // Ref für Auto-Scroll
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-Scroll zur User-Frage wenn neue Antwort kommt
  const scrollToNewMessage = () => {
    if (messagesContainerRef.current && messages.length >= 2) {
      // Scroll zur vorletzten Nachricht (User-Frage), damit Nutzer seine Frage oben sieht
      // und die Antwort darunter lesen kann
      const container = messagesContainerRef.current;
      const userMessage = container.querySelector('[data-user-message="true"]');
      if (userMessage) {
        // Erst zur User-Nachricht scrollen, dann 80px Offset nach unten
        const rect = userMessage.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        const scrollOffset = rect.top - containerRect.top + container.scrollTop - 80;
        container.scrollTo({ top: scrollOffset, behavior: 'smooth' });
      }
    }
  };
  
  useEffect(() => {
    // Kleines Timeout damit DOM aktualisiert ist
    const timer = setTimeout(() => {
      scrollToNewMessage();
    }, 100);
    return () => clearTimeout(timer);
  }, [messages]);
  
  // Lawyer ist unbegrenzt
  const isUnlimited = userPlan === 'lawyer';
  
  // Source-Filter NUR für Lawyer-Tier anzeigen
  const showSourceFilter = userPlan === 'lawyer';
  
  // Limits: Free=3, Basis=50, Professional=250, Lawyer=unbegrenzt
  const getMaxQueries = () => {
    if (!isLoggedIn) return FREE_QUERIES_BEFORE_REGISTER;  // 3
    if (userPlan === 'free') return FREE_QUERIES_BEFORE_UPGRADE;  // 3
    if (userPlan === 'basis' || userPlan === 'mieter_plus') return 50;  // Legacy support
    if (userPlan === 'professional') return 250;
    if (userPlan === 'lawyer') return 999999;  // Unbegrenzt
    return FREE_QUERIES_BEFORE_UPGRADE;
  };
  const maxQueries = getMaxQueries();
  const canQuery = isUnlimited || queryCount < maxQueries;

  // Effect für initialen Message aus URL
  useEffect(() => {
    if (initialMessage && !initialMessageSent && !loading) {
      setInitialMessageSent(true);
      setInput(initialMessage);
      // Automatisch absenden nach kurzer Verzögerung
      setTimeout(() => {
        const form = document.querySelector('form');
        if (form) {
          form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        }
      }, 500);
    }
  }, [initialMessage, initialMessageSent, loading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    // Prüfe IP-Limit für Gäste
    if (!isLoggedIn && (ipLimitReached || queryCount >= FREE_QUERIES_BEFORE_REGISTER)) {
      setShowRegisterModal(true);
      return;
    }
    
    // Prüfe ob Upgrade erforderlich
    if (!isUnlimited && queryCount >= maxQueries) {
      setShowUpgradeModal(true);
      return;
    }

    const userMessage: Message = {
      role: 'user',
      content: input,
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Für Lawyer: Benutzerdefinierte Filter anwenden
      // Für Basis/Professional: Nur verlässliche Quellen (Gesetze + Höchstgerichte BGH, BFH, EuGH)
      let filters: { source_filter: string[] | null | undefined; gerichtsebene_filter: string[] | null | undefined };
      
      if (showSourceFilter) {
        // Lawyer: Benutzerdefinierte Filter
        filters = filtersToApiFormat(sourceFilters);
      } else {
        // Basis/Professional: Nur verlässliche Quellen (Gesetze + Höchstgerichte)
        // KEINE Literatur, Kommentare oder Instanzgerichte (OLG, LG, AG) für Rechtslaien
        filters = {
          source_filter: ['GESETZ', 'URTEIL', 'VERWALTUNG'],  // Nur Gesetze, Urteile, Verwaltungsvorschriften
          gerichtsebene_filter: ['EuGH', 'BGH', 'BFH'],  // Nur Höchstgerichte - verlässlich und verbindlich
        };
      }
      
      const request: QueryRequest = {
        query: input,
        target_jurisdiction: jurisdiction,
        user_role: role,
        user_language: language,
        sub_jurisdiction: subJurisdiction,
        user_id: user?.uid,  // Send user ID for backend quota tracking
        user_tier: userPlan,
        source_filter: filters.source_filter ?? undefined,
        gerichtsebene_filter: filters.gerichtsebene_filter ?? undefined,
        use_public_sources: userPlan === 'lawyer' ? usePublicSources : false,  // 🔑 Nur Lawyer kann öffentliche Quellen aktivieren
        uploaded_documents: uploadedDocuments.map(doc => ({
          document_id: doc.id,
          text: doc.extracted_text_full || doc.extracted_text_preview || '',  // Use full text if available
        })),
      };

      const response = await apiClient.query(request);
      
      // Zähle erfolgreiche Anfrage (nur lokal für UI-State)
      // Backend inkrementiert queriesUsed in Firestore automatisch
      await incrementQuery();

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        warning: response.jurisdiction_warning,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      
      // Nach Antwort: Prüfe ob Registrierung/Upgrade nötig
      if (!isLoggedIn && queryCount + 1 >= FREE_QUERIES_BEFORE_REGISTER) {
        setTimeout(() => setShowRegisterModal(true), 1500);
      } else if (isLoggedIn && !isUnlimited && queryCount + 1 >= maxQueries) {
        setTimeout(() => setShowUpgradeModal(true), 1500);
      }
      
    } catch (error) {
      // Handle quota exceeded error
      if (error instanceof QuotaExceededError) {
        setShowUpgradeModal(true);
        const errorMessage: Message = {
          role: 'assistant',
          content: `⚠️ ${error.message}\n\nBitte upgraden Sie Ihren Plan für weitere Anfragen.`,
        };
        setMessages((prev) => [...prev, errorMessage]);
      } else {
        const errorMessage: Message = {
          role: 'assistant',
          content: `⚠️ ${error instanceof Error ? error.message : 'Ein Fehler ist aufgetreten. Bitte stellen Sie nur themenbezogene Immobilienrechts-Fragen.'}`,
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Query Counter Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-[#1e3a5f] border-b border-[#1e3a5f]/80">
        <div className="flex items-center gap-3">
          {!isLoggedIn ? (
            <button
              onClick={() => setShowRegisterModal(true)}
              className="text-sm text-[#b8860b] hover:text-[#d4a84b]"
            >
              Anmelden für mehr Anfragen →
            </button>
          ) : (
            <span className="text-sm text-white">
              Eingeloggt • {userPlan.charAt(0).toUpperCase() + userPlan.slice(1)}-Tarif
            </span>
          )}
        </div>
        <QueryBadge current={queryCount} max={maxQueries} isUnlimited={isUnlimited} />
      </div>

      {/* Source Filter - Quellenauswahl direkt im Hauptchat */}
      {showSourceFilter && (
        <div className="px-4 pt-4 pb-2">
          <div className="bg-gradient-to-r from-[#1e3a5f]/5 to-[#b8860b]/5 rounded-lg p-3 mb-2">
            <div className="flex items-center gap-2 mb-2">
              <svg className="w-4 h-4 text-[#b8860b]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              <span className="text-sm font-semibold text-gray-700">Quellenauswahl für Ihre Suche</span>
            </div>
            <SourceFilter value={sourceFilters} onChange={setSourceFilters} />
            
            {/* Toggle für öffentliche Quellen (nur für Anwälte) */}
            {userPlan === 'lawyer' && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <label className="flex items-center justify-between cursor-pointer group">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">⚖️</span>
                    <div>
                      <p className="text-sm font-semibold text-gray-700 group-hover:text-[#1e3a5f] transition-colors">
                        Allgemeines KI-Wissen verwenden (statt Datenbank)
                      </p>
                      <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded">
                        <p className="text-xs font-bold text-green-900 mb-2">
                          <span className="px-2 py-0.5 bg-green-100 text-green-800 rounded font-medium mr-1">AUS</span>
                          Nur verlässliche, geprüfte Datenbank:
                        </p>
                        <div className="text-xs text-green-800 space-y-1 ml-3">
                          <p>📚 <strong>Gesetze:</strong> BGB, WEG, BauGB, GrEStG, GrStG, BetrKV, HeizkostenV, EStG, UStG, AO + LBOs</p>
                          <p>⚖️ <strong>Rechtsprechung:</strong> Urteile (BGH, BFH, EuGH, OLG/LG/AG)</p>
                          <p>📖 <strong>Fachliteratur:</strong> Kommentare (Palandt, MüKo, Staudinger, Schmidt)</p>
                          <p>📋 <strong>Verwaltungsrecht:</strong> BMF-Schreiben, EStR, UStAE, GrEStR, ErbStR</p>
                        </div>
                      </div>
                      <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded">
                        <p className="text-xs font-bold text-red-900 mb-1">
                          <span className="px-2 py-0.5 bg-red-100 text-red-800 rounded font-medium mr-1">AN</span>
                          Allgemeines KI-Chatbot-Wissen ohne Datenbankgrundlage
                        </p>
                        <p className="text-xs text-red-700 font-semibold mt-2">
                          ⚠️ WARNUNG: Bei Aktivierung steht die verlässliche, verbindliche Datenbank NICHT mehr zur Verfügung!
                        </p>
                        <p className="text-xs text-red-600 mt-1">
                          Die KI nutzt dann nur ihr allgemeines Trainingswissen mit erhöhtem Risiko für Halluzinationen und ungenaue Rechtsauskünfte.
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="relative">
                    <input
                      type="checkbox"
                      checked={usePublicSources}
                      onChange={(e) => setUsePublicSources(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[#b8860b]/20 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#b8860b]"></div>
                  </div>
                </label>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Messages */}
      <div ref={messagesContainerRef} className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-lg">Stelle deine erste Rechtsfrage...</p>
            <p className="text-sm mt-2">
              Beispiel: &quot;Was sind meine Rechte als Mieter bei Mieterhöhung?&quot;
            </p>
            <p className="text-sm mt-3 text-orange-500 font-medium">
              ⚠️ Nur themenbezogene Rechtsfragen - jede Anfrage verbraucht Ihr Kontingent!
            </p>
            {!isLoggedIn && (
              <div className="mt-6 p-4 bg-blue-600/10 border border-blue-600/30 rounded-lg inline-block">
                <p className="text-sm text-blue-300">
                  💡 <strong>Tipp:</strong> Registrieren Sie sich kostenlos für 3 Test-Anfragen!
                </p>
                <button
                  onClick={() => setShowRegisterModal(true)}
                  className="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
                >
                  Jetzt kostenlos registrieren
                </button>
              </div>
            )}
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            data-user-message={message.role === 'user' && index === messages.length - 2 ? "true" : undefined}
            data-last-message={index === messages.length - 1 ? "true" : undefined}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
              }`}
            >
              <div className="whitespace-pre-wrap">{message.content}</div>

              {/* Sources */}
              {message.sources && message.sources.length > 0 && (
                <details className="mt-4 text-sm">
                  <summary className="cursor-pointer font-semibold">
                    📚 Quellen ({message.sources.length})
                  </summary>
                  <div className="mt-2 space-y-2">
                    {message.sources.map((source, idx) => {
                      const url = generateSourceUrl(source);
                      return (
                        <div key={idx} className="border-l-2 border-gray-400 pl-2">
                          {url ? (
                            <a
                              href={url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="font-semibold text-blue-600 hover:underline flex items-center gap-1"
                            >
                              {source.title}
                              <span className="text-xs">🔗</span>
                            </a>
                          ) : (
                            <span className="font-semibold">{source.title}</span>
                          )}
                          <p className="text-xs text-gray-600 dark:text-gray-400">
                            {source.jurisdiction} • {source.document_type} •{' '}
                            {source.publication_date}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </details>
              )}

              {/* Warning */}
              {message.warning && (
                <div className="mt-2 p-2 bg-yellow-100 dark:bg-yellow-900 rounded text-sm">
                  ⚠️ {message.warning}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}
        
        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Limit Warning Banner */}
      {!canQuery && (
        <div className="mx-4 mb-2 p-3 bg-amber-100 border border-amber-500 rounded-lg">
          <p className="text-amber-900 text-sm font-medium">
            {!isLoggedIn 
              ? '🔒 Registrieren Sie sich kostenlos, um weitere Anfragen zu stellen.'
              : `🔒 Sie haben Ihre ${maxQueries} Anfragen aufgebraucht. Upgraden Sie für mehr Anfragen.`}
          </p>
          <button
            onClick={() => isLoggedIn ? setShowUpgradeModal(true) : setShowRegisterModal(true)}
            className="mt-2 px-4 py-1 bg-amber-600 hover:bg-amber-700 text-white rounded text-sm transition-colors"
          >
            {isLoggedIn ? 'Jetzt upgraden' : 'Kostenlos registrieren'}
          </button>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-slate-700 p-4">
        {/* File Upload - Gesperrt wenn keine Anfragen mehr */}
        <div className="mb-3">
          <FileUpload 
            onUpload={(doc: UploadedDocument) => {
              setUploadedDocuments(prev => [...prev, doc]);
            }}
            maxSize={10 * 1024 * 1024} // 10MB
            maxFiles={userPlan === 'lawyer' ? 10 : userPlan === 'professional' ? 5 : 3}
            disabled={!canQuery}
          />
        </div>

        {/* Uploaded Documents List */}
        {uploadedDocuments.length > 0 && (
          <div className="mb-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-blue-900 dark:text-blue-100">
                📎 Hochgeladene Dokumente ({uploadedDocuments.length})
              </span>
              <button
                type="button"
                onClick={() => setUploadedDocuments([])}
                className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400"
              >
                Alle entfernen
              </button>
            </div>
            <div className="space-y-1">
              {uploadedDocuments.map((doc, idx) => (
                <div key={idx} className="flex items-center justify-between text-xs text-blue-800 dark:text-blue-200">
                  <span className="truncate flex-1">{doc.filename}</span>
                  <button
                    type="button"
                    onClick={() => setUploadedDocuments(prev => prev.filter((_, i) => i !== idx))}
                    className="ml-2 text-red-600 hover:text-red-800"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={canQuery ? 'Stelle deine Rechtsfrage...' : 'Registrieren/Upgraden für mehr Anfragen...'}
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700"
            disabled={loading || !canQuery}
          />
          <button
            type="submit"
            disabled={loading || !input.trim() || !canQuery}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Lädt...' : 'Senden'}
          </button>
        </div>
      </form>
      
      {/* Modals */}
      <AuthModal 
        isOpen={showRegisterModal} 
        onClose={() => setShowRegisterModal(false)}
        mode="register"
        onSuccess={() => {
          setShowRegisterModal(false);
          window.location.reload();
        }}
      />
      <UpgradeModal 
        isOpen={showUpgradeModal} 
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="basis"
        feature="KI-Chat Anfragen"
      />
    </div>
  );
}
