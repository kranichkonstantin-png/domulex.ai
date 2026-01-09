'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import UpgradeModal from '@/components/UpgradeModal';
import { auth, db } from '@/lib/firebase';
import { hasTierAccess } from '@/lib/tierUtils';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc, updateDoc, increment } from 'firebase/firestore';
import { useDropzone } from 'react-dropzone';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';

interface AnalyseErgebnis {
  gesamtBewertung: 'ok' | 'warnung' | 'fehler';
  zusammenfassung: string;
  positionen: {
    name: string;
    betrag: number;
    status: 'ok' | 'warnung' | 'fehler';
    meldung: string;
    rechtslage?: string;
  }[];
  einsparpotenzial: number;
  empfehlungen: string[];
  musterbrief?: string;
}

export default function NebenkostenPruefungPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const [queriesUsed, setQueriesUsed] = useState(0);
  const [queriesLimit, setQueriesLimit] = useState(0);
  
  // Basis tier or higher has access
  const hasAccess = hasTierAccess(userTier, 'basis');
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };
  
  // Upload State
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyseErgebnis | null>(null);
  const [rawAnalysis, setRawAnalysis] = useState<string>('');
  const [showRaw, setShowRaw] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      setUser(currentUser);
      
      // Load user tier
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      if (userDoc.exists()) {
        const data = userDoc.data();
        const tier = data.tier || data.dashboardType || 'free';
        setUserTier(tier);
        setQueriesUsed(data.queriesUsed || 0);
        setQueriesLimit(data.queriesLimit || 0);
      }
      
      setLoading(false);
    });
    return () => unsubscribe();
  }, [router]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setResult(null);
      setError(null);
      setRawAnalysis('');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tif'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/plain': ['.txt'],
      'text/csv': ['.csv'],
      'text/html': ['.html', '.htm'],
      'application/xml': ['.xml'],
      'message/rfc822': ['.eml'],
      'application/vnd.ms-outlook': ['.msg']
    },
    maxSize: 10 * 1024 * 1024,
    multiple: false
  });

  const analyzeDocument = async () => {
    if (!file || !user) return;
    
    // Check query limit for non-lawyer users
    if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
      setError('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für weitere Analysen.');
      setShowUpgradeModal(true);
      return;
    }
    
    setAnalyzing(true);
    setError(null);
    
    try {
      // Schritt 1: Dokument hochladen und Text extrahieren
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', user.uid);
      
      const uploadResponse = await fetch(`${API_URL}/upload/document`, {
        method: 'POST',
        body: formData
      });
      
      if (!uploadResponse.ok) {
        throw new Error('Dokument konnte nicht verarbeitet werden');
      }
      
      const uploadData = await uploadResponse.json();
      // Use full extracted text for proper analysis
      const extractedText = uploadData.extracted_text_full || uploadData.extracted_text_preview || '';
      
      if (!extractedText || extractedText.length < 50) {
        throw new Error('Der Text konnte nicht aus dem Dokument extrahiert werden. Bitte stellen Sie sicher, dass es sich um eine lesbare Nebenkostenabrechnung handelt.');
      }
      
      // Schritt 2: KI-Analyse der Nebenkostenabrechnung
      const analysePrompt = `Du bist ein Experte für deutsches Mietrecht. Analysiere diese Nebenkostenabrechnung und prüfe sie auf Fehler.

DOKUMENT-TEXT:
${extractedText}

Prüfe bitte:
1. Sind alle Positionen umlagefähig nach § 2 BetrKV? (Nicht umlagefähig: Verwaltungskosten, Instandhaltungsrücklage, Reparaturen, Bankgebühren, Leerstand)
2. Sind die Kosten pro m² im normalen Bereich? (Nebenkosten sollten 2,50-4,00 €/m²/Monat sein)
3. Ist die Abrechnung fristgerecht (12 Monate nach Ende des Abrechnungszeitraums)?
4. Sind Heizkosten korrekt nach Verbrauch (50-70%) und Fläche abgerechnet?
5. Gibt es doppelte Positionen oder unklare Bezeichnungen?

Antworte in diesem Format:
GESAMTBEWERTUNG: [OK/WARNUNG/FEHLER]

ZUSAMMENFASSUNG:
[2-3 Sätze Gesamteinschätzung]

POSITIONEN:
- [Positionsname]: [BETRAG €] - [OK/WARNUNG/FEHLER] - [Kurze Begründung]
...

EINSPARPOTENZIAL: [X] €

EMPFEHLUNGEN:
1. [Empfehlung]
2. [Empfehlung]
...

RECHTLICHE HINWEISE:
[Relevante Paragraphen und BGH-Urteile]`;

      const queryResponse = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: analysePrompt,
          target_jurisdiction: 'DE'
        })
      });
      
      if (!queryResponse.ok) {
        throw new Error('KI-Analyse fehlgeschlagen');
      }
      
      const queryData = await queryResponse.json();
      const kiAntwort = queryData.answer || queryData.response || '';
      
      setRawAnalysis(kiAntwort);
      
      // Parse die KI-Antwort
      const parsedResult = parseKiAntwort(kiAntwort);
      setResult(parsedResult);
      
      // Increment query count for non-lawyer users
      if (userTier !== 'lawyer') {
        await updateDoc(doc(db, 'users', user.uid), {
          queriesUsed: increment(1)
        });
        setQueriesUsed(prev => prev + 1);
      }
      
    } catch (err) {
      console.error('Analyse-Fehler:', err);
      setError(err instanceof Error ? err.message : 'Fehler bei der Analyse');
    } finally {
      setAnalyzing(false);
    }
  };

  const parseKiAntwort = (antwort: string): AnalyseErgebnis => {
    // Gesamtbewertung extrahieren
    let gesamtBewertung: 'ok' | 'warnung' | 'fehler' = 'ok';
    if (antwort.toLowerCase().includes('fehler') && antwort.toLowerCase().includes('gesamtbewertung')) {
      gesamtBewertung = 'fehler';
    } else if (antwort.toLowerCase().includes('warnung')) {
      gesamtBewertung = 'warnung';
    }
    
    // Zusammenfassung extrahieren
    const zusammenfassungMatch = antwort.match(/ZUSAMMENFASSUNG:?\s*([\s\S]*?)(?=POSITIONEN:|EINSPARPOTENZIAL:|$)/i);
    const zusammenfassung = zusammenfassungMatch ? zusammenfassungMatch[1].trim() : 
      'Die Nebenkostenabrechnung wurde analysiert. Details siehe unten.';
    
    // Positionen extrahieren
    const positionen: AnalyseErgebnis['positionen'] = [];
    const positionenMatch = antwort.match(/POSITIONEN:?\s*([\s\S]*?)(?=EINSPARPOTENZIAL:|EMPFEHLUNGEN:|$)/i);
    if (positionenMatch) {
      const lines = positionenMatch[1].split('\n').filter(l => l.trim().startsWith('-'));
      lines.forEach(line => {
        const parts = line.replace(/^-\s*/, '').split(/[-–:]/);
        if (parts.length >= 2) {
          const name = parts[0].trim();
          const betragMatch = line.match(/(\d+[.,]?\d*)\s*€/);
          const betrag = betragMatch ? parseFloat(betragMatch[1].replace(',', '.')) : 0;
          
          let status: 'ok' | 'warnung' | 'fehler' = 'ok';
          if (line.toLowerCase().includes('fehler') || line.toLowerCase().includes('nicht umlagefähig')) {
            status = 'fehler';
          } else if (line.toLowerCase().includes('warnung') || line.toLowerCase().includes('hoch') || line.toLowerCase().includes('prüfen')) {
            status = 'warnung';
          }
          
          positionen.push({
            name,
            betrag,
            status,
            meldung: parts.slice(1).join(' - ').trim() || 'Geprüft'
          });
        }
      });
    }
    
    // Einsparpotenzial extrahieren
    const einsparMatch = antwort.match(/EINSPARPOTENZIAL:?\s*(\d+[.,]?\d*)/i);
    const einsparpotenzial = einsparMatch ? parseFloat(einsparMatch[1].replace(',', '.')) : 0;
    
    // Empfehlungen extrahieren
    const empfehlungen: string[] = [];
    const empfMatch = antwort.match(/EMPFEHLUNGEN:?\s*([\s\S]*?)(?=RECHTLICHE|MUSTERBRIEF|$)/i);
    if (empfMatch) {
      const lines = empfMatch[1].split('\n').filter(l => l.trim().match(/^\d+\.|^-/));
      lines.forEach(line => {
        const text = line.replace(/^\d+\.\s*|^-\s*/, '').trim();
        if (text.length > 10) empfehlungen.push(text);
      });
    }
    
    // Musterbrief generieren bei Fehlern
    let musterbrief: string | undefined;
    if (gesamtBewertung === 'fehler') {
      const fehlerPositionen = positionen.filter(p => p.status === 'fehler');
      musterbrief = `Betreff: Widerspruch gegen Nebenkostenabrechnung

Sehr geehrte Damen und Herren,

gegen die mir zugesandte Nebenkostenabrechnung lege ich hiermit fristgerecht Widerspruch ein.

Die Abrechnung weist folgende Fehler auf:

${fehlerPositionen.map((f, i) => `${i + 1}. ${f.name}: ${f.meldung}`).join('\n\n')}

Ich fordere Sie auf, die Abrechnung entsprechend zu korrigieren und mir eine berichtigte Abrechnung zukommen zu lassen.

Gleichzeitig mache ich von meinem Recht auf Belegeinsicht gemäß § 259 BGB Gebrauch.

Mit freundlichen Grüßen
[Ihr Name]`;
    }
    
    return {
      gesamtBewertung,
      zusammenfassung,
      positionen,
      einsparpotenzial,
      empfehlungen,
      musterbrief
    };
  };

  const getBewertungStyle = (bewertung: string) => {
    switch (bewertung) {
      case 'fehler': return { bg: 'bg-red-100', border: 'border-red-300', text: 'text-red-800', icon: '❌' };
      case 'warnung': return { bg: 'bg-yellow-100', border: 'border-yellow-300', text: 'text-yellow-800', icon: '⚠️' };
      default: return { bg: 'bg-green-100', border: 'border-green-300', text: 'text-green-800', icon: '✅' };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black flex items-center justify-center">
        <div className="animate-spin text-4xl">⚙️</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-xl border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-16">
            <Link href="/dashboard" className="text-gray-400 hover:text-white">← Dashboard</Link>
            <h1 className="text-lg font-semibold text-white">KI-Nebenkostenprüfung</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 pt-24 pb-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">📊 Nebenkostenabrechnung prüfen</h1>
          <p className="text-gray-400 mt-2">
            Laden Sie Ihre Nebenkostenabrechnung als PDF oder Foto hoch. 
            Unsere KI prüft sie auf Fehler und nicht umlagefähige Kosten.
          </p>
        </div>

        {/* Upgrade-Sperre für FREE-Nutzer */}
        {!hasAccess && !result && (
          <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-xl border border-[#b8860b]/30 p-8 mb-6 text-center">
            <div className="w-20 h-20 bg-[#b8860b]/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl">🔒</span>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Premium-Funktion</h3>
            <p className="text-gray-400 mb-4">
              Die KI-Nebenkostenprüfung ist ab dem <strong className="text-[#b8860b]">Basis-Tarif</strong> verfügbar.
            </p>
            <div className="bg-gray-800/50 rounded-lg p-4 mb-6 text-left max-w-md mx-auto">
              <p className="text-sm font-medium text-gray-300 mb-2">Mit dieser Funktion können Sie:</p>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>✓ Nebenkostenabrechnungen automatisch prüfen</li>
                <li>✓ Nicht umlagefähige Kosten erkennen</li>
                <li>✓ Einsparpotenzial berechnen lassen</li>
                <li>✓ Rechtssichere Widerspruchsbriefe generieren</li>
              </ul>
            </div>
            <button
              onClick={() => setShowUpgradeModal(true)}
              className="px-8 py-3 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-lg font-medium transition-colors"
            >
              🚀 Jetzt auf Basis upgraden
            </button>
            <p className="text-xs text-gray-500 mt-4">
              Ab 19€/Monat • Jederzeit kündbar
            </p>
          </div>
        )}

        {/* Upload-Bereich - nur für zahlende Nutzer */}
        {hasAccess && !result && (
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-8 mb-6">
            <div 
              {...getRootProps()} 
              className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors
                ${isDragActive ? 'border-blue-500 bg-blue-500/10' : 
                  file ? 'border-green-500 bg-green-900/30' : 'border-gray-600 hover:border-blue-500'}`}
            >
              <input {...getInputProps()} />
              {file ? (
                <div>
                  <p className="text-4xl mb-4">📄</p>
                  <p className="text-lg font-medium text-white">{file.name}</p>
                  <p className="text-sm text-gray-400 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  <p className="text-sm text-green-400 mt-3">✓ Bereit zur Analyse</p>
                </div>
              ) : (
                <div>
                  <p className="text-5xl mb-4">📤</p>
                  <p className="text-lg font-medium text-gray-300">
                    {isDragActive ? 'Datei hier ablegen...' : 'Nebenkostenabrechnung hochladen'}
                  </p>
                  <p className="text-sm text-gray-400 mt-2">
                    Ziehen Sie die Datei hierher oder klicken Sie zum Auswählen
                  </p>
                  <p className="text-xs text-gray-400 mt-4">
                    Unterstützte Formate: PDF, Word, Excel, Bilder, Text, CSV, HTML, E-Mail • Max. 10 MB
                  </p>
                </div>
              )}
            </div>

            {file && (
              <div className="mt-6 flex flex-col sm:flex-row gap-4">
                <button 
                  onClick={() => { setFile(null); setResult(null); setError(null); }} 
                  className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-700"
                >
                  Andere Datei wählen
                </button>
                <button 
                  onClick={analyzeDocument} 
                  disabled={analyzing}
                  className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
                >
                  {analyzing ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="animate-spin">⚙️</span>
                      Analysiere... (kann 30-60 Sekunden dauern)
                    </span>
                  ) : '🔍 Abrechnung prüfen'}
                </button>
              </div>
            )}
            {file && userTier !== 'lawyer' && (
              <p className="text-xs text-orange-400 mt-3 text-center">Verbraucht 1 Anfrage ({queriesLimit - queriesUsed} übrig)</p>
            )}

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                <p className="font-medium">Fehler bei der Analyse</p>
                <p className="text-sm mt-1">{error}</p>
              </div>
            )}
          </div>
        )}

        {/* Ergebnis-Anzeige */}
        {result && (
          <div className="space-y-6">
            {/* Gesamtbewertung */}
            <div className={`rounded-xl border-2 p-6 ${getBewertungStyle(result.gesamtBewertung).bg} ${getBewertungStyle(result.gesamtBewertung).border}`}>
              <div className="flex items-center gap-3 mb-4">
                <span className="text-4xl">{getBewertungStyle(result.gesamtBewertung).icon}</span>
                <div>
                  <h2 className={`text-xl font-bold ${getBewertungStyle(result.gesamtBewertung).text}`}>
                    {result.gesamtBewertung === 'fehler' ? 'Fehler gefunden!' : 
                     result.gesamtBewertung === 'warnung' ? 'Hinweise vorhanden' : 'Abrechnung OK'}
                  </h2>
                  <p className="text-gray-700">{result.zusammenfassung}</p>
                </div>
              </div>
              
              {result.einsparpotenzial > 0 && (
                <div className="mt-4 p-3 bg-gray-900/50 rounded-lg">
                  <p className="font-medium text-white">
                    💰 Mögliches Einsparpotenzial: <span className="text-green-400 font-bold">{result.einsparpotenzial.toFixed(2)} €</span>
                  </p>
                </div>
              )}
            </div>

            {/* Einzelne Positionen */}
            {result.positionen.length > 0 && (
              <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">📋 Geprüfte Positionen</h3>
                <div className="space-y-3">
                  {result.positionen.map((pos, index) => (
                    <div 
                      key={index}
                      className={`p-4 rounded-lg border ${getBewertungStyle(pos.status).bg} ${getBewertungStyle(pos.status).border}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2">
                          <span>{getBewertungStyle(pos.status).icon}</span>
                          <span className="font-medium">{pos.name}</span>
                          {pos.betrag > 0 && (
                            <span className="text-sm text-gray-600">({pos.betrag.toFixed(2)} €)</span>
                          )}
                        </div>
                      </div>
                      <p className="text-sm mt-2 text-gray-700">{pos.meldung}</p>
                      {pos.rechtslage && (
                        <p className="text-xs mt-1 text-gray-500 italic">📚 {pos.rechtslage}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Empfehlungen */}
            {result.empfehlungen.length > 0 && (
              <div className="bg-gradient-to-br from-[#1e3a5f] to-[#2d5a8f] rounded-xl p-6 text-white">
                <h3 className="text-lg font-semibold mb-4">💡 Unsere Empfehlungen</h3>
                <ul className="space-y-2">
                  {result.empfehlungen.map((empf, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <span className="text-[#b8860b] font-bold">{index + 1}.</span>
                      <span>{empf}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Musterbrief bei Fehlern */}
            {result.musterbrief && (
              <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
                <h3 className="text-lg font-semibold text-white mb-4">✉️ Muster-Widerspruchsschreiben</h3>
                <div className="bg-gray-900/50 rounded-lg p-4 font-mono text-sm whitespace-pre-wrap text-gray-300">
                  {result.musterbrief}
                </div>
                <button 
                  onClick={() => navigator.clipboard.writeText(result.musterbrief || '')}
                  className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                >
                  📋 In Zwischenablage kopieren
                </button>
              </div>
            )}

            {/* Vollständige KI-Analyse */}
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <button 
                onClick={() => setShowRaw(!showRaw)}
                className="flex items-center justify-between w-full"
              >
                <h3 className="text-lg font-semibold text-white">🤖 Vollständige KI-Analyse</h3>
                <span className="text-gray-400">{showRaw ? '▼' : '▶'}</span>
              </button>
              {showRaw && (
                <div className="mt-4 p-4 bg-gray-900/50 rounded-lg text-sm whitespace-pre-wrap max-h-96 overflow-y-auto text-gray-300">
                  {rawAnalysis}
                </div>
              )}
            </div>

            {/* Aktionen */}
            <div className="flex flex-wrap gap-4">
              <button 
                onClick={() => { setFile(null); setResult(null); setRawAnalysis(''); }} 
                className="px-6 py-3 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-700"
              >
                📄 Neue Abrechnung prüfen
              </button>
              <Link href="/app?prompt=Ich%20habe%20Fragen%20zu%20meiner%20Nebenkostenabrechnung" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                🤖 Mit KI-Berater besprechen
              </Link>
            </div>

            {/* Rechtlicher Hinweis */}
            <div className="bg-amber-50 rounded-xl p-4 text-sm text-amber-800">
              <p className="font-medium mb-1">⚖️ Rechtlicher Hinweis</p>
              <p>Diese KI-gestützte Analyse ersetzt keine Rechtsberatung. Die Prüfung basiert auf den erkannten Daten im Dokument. Bei Unstimmigkeiten empfehlen wir die Konsultation eines Mietervereins oder Rechtsanwalts.</p>
            </div>
          </div>
        )}

        {/* Info-Karten wenn kein Ergebnis */}
        {!result && !file && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <p className="text-2xl mb-3">🔍</p>
              <h3 className="font-semibold text-white">Umlagefähigkeit prüfen</h3>
              <p className="text-sm text-gray-400 mt-2">
                Erkennt nicht umlagefähige Kosten wie Verwaltung, Reparaturen oder Instandhaltungsrücklage
              </p>
            </div>
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <p className="text-2xl mb-3">📊</p>
              <h3 className="font-semibold text-white">Kosten vergleichen</h3>
              <p className="text-sm text-gray-400 mt-2">
                Vergleicht Ihre Nebenkosten mit Durchschnittswerten und erkennt überhöhte Positionen
              </p>
            </div>
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <p className="text-2xl mb-3">✉️</p>
              <h3 className="font-semibold text-white">Widerspruch erstellen</h3>
              <p className="text-sm text-gray-400 mt-2">
                Generiert bei Fehlern automatisch ein Muster-Widerspruchsschreiben
              </p>
            </div>
          </div>
        )}
      </div>
      
      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        feature="Nebenkostenprüfung"
        requiredTier="basis"
      />
    </div>
  );
}
