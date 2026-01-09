'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Logo from '@/components/Logo';
import UpgradeModal from '@/components/UpgradeModal';
import { auth, db } from '@/lib/firebase';
import { hasTierAccess } from '@/lib/tierUtils';
import { onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';

interface Urteil {
  gericht: string;
  aktenzeichen: string;
  datum: string;
  thema: string;
  leitsatz: string;
  relevanz: number;
  quelle?: string;
}

interface AnalyseErgebnis {
  zusammenfassung: string;
  urteile: Urteil[];
  rechtslage: string;
  empfehlung: string;
  anwendbareNormen: string[];
}

const GERICHTSEBENEN = [
  { id: 'alle', label: 'Alle Gerichte' },
  { id: 'BGH', label: 'Bundesgerichtshof (BGH)' },
  { id: 'OLG', label: 'Oberlandesgerichte (OLG)' },
  { id: 'LG', label: 'Landgerichte (LG)' },
  { id: 'AG', label: 'Amtsgerichte (AG)' },
];

const RECHTSGEBIETE = [
  { id: 'alle', label: 'Alle Rechtsgebiete' },
  { id: 'mietrecht', label: 'Mietrecht' },
  { id: 'kaufrecht', label: 'Immobilienkaufrecht' },
  { id: 'weg', label: 'WEG-Recht' },
  { id: 'baurecht', label: 'Baurecht' },
  { id: 'maklerrecht', label: 'Maklerrecht' },
  { id: 'nachbarrecht', label: 'Nachbarrecht' },
];

// ===== DEMO-DATEN FÜR FREE/PROFESSIONAL-NUTZER =====
const DEMO_ERGEBNIS: AnalyseErgebnis = {
  zusammenfassung: 'Die Rechtsprechung zur Mietminderung bei Schimmelbefall ist gefestigt. Der Vermieter trägt grundsätzlich die Darlegungs- und Beweislast für die Ursache des Schimmels. Eine Minderung von 20-25% bei Schimmel im Schlafzimmer wird von der Rechtsprechung regelmäßig anerkannt.',
  urteile: [
    {
      gericht: 'BGH',
      aktenzeichen: 'VIII ZR 138/18',
      datum: '2019-07-10',
      thema: 'Beweislast bei Schimmelbefall',
      leitsatz: 'Der Vermieter trägt die Darlegungs- und Beweislast dafür, dass die Ursache des Schimmelbefalls nicht auf einem Mangel der Mietsache beruht, sondern auf einem Fehlverhalten des Mieters.',
      relevanz: 98,
      quelle: 'NJW 2019, 2842',
    },
    {
      gericht: 'BGH',
      aktenzeichen: 'VIII ZR 67/12',
      datum: '2012-10-10',
      thema: 'Mietminderung bei Gesundheitsgefährdung',
      leitsatz: 'Bei erheblichem Schimmelbefall, der eine Gesundheitsgefährdung darstellt, kann die Miete um 100% gemindert werden, wenn die Wohnung unbewohnbar ist.',
      relevanz: 85,
      quelle: 'NJW 2013, 63',
    },
    {
      gericht: 'LG Berlin',
      aktenzeichen: '65 S 400/17',
      datum: '2018-03-15',
      thema: 'Minderungsquote bei Schimmel',
      leitsatz: 'Schimmelbefall im Schlafzimmer, der auf bauliche Mängel zurückzuführen ist, rechtfertigt eine Mietminderung von 20%.',
      relevanz: 92,
      quelle: 'GE 2018, 589',
    },
    {
      gericht: 'AG München',
      aktenzeichen: '461 C 19847/20',
      datum: '2021-05-20',
      thema: 'Vergleich bei streitiger Ursache',
      leitsatz: 'Bei ungeklärter Schimmelursache ist ein Vergleich mit 15% Mietminderung und Beseitigungspflicht des Vermieters sachgerecht.',
      relevanz: 78,
      quelle: 'ZMR 2021, 742',
    },
    {
      gericht: 'OLG Düsseldorf',
      aktenzeichen: 'I-24 U 58/16',
      datum: '2017-02-14',
      thema: 'Schadensersatz bei Schimmel',
      leitsatz: 'Der Mieter kann bei schuldhafter Verursachung des Schimmels durch den Vermieter neben der Mietminderung auch Schadensersatz für beschädigte Einrichtungsgegenstände verlangen.',
      relevanz: 75,
      quelle: 'NZM 2017, 457',
    },
  ],
  rechtslage: 'Die aktuelle Rechtsprechung ist mieterfreundlich. Der BGH hat 2019 die Beweislast zugunsten des Mieters verteilt. Der Mieter muss nur den Mangel (Schimmel) darlegen, der Vermieter muss beweisen, dass die Ursache nicht baulicher Natur ist. Minderungsquoten von 20-25% bei Schimmel im Schlafzimmer sind etabliert.',
  empfehlung: 'Bei der Vertretung eines Mieters sollte frühzeitig auf die BGH-Rechtsprechung zur Beweislast verwiesen werden. Ein Sachverständigengutachten zur Schimmelursache kann prozessentscheidend sein. Bei unklarer Beweislage ist ein Vergleich mit 15-20% Minderung oft wirtschaftlich sinnvoll.',
  anwendbareNormen: [
    '§ 536 BGB - Mietminderung bei Sach- und Rechtsmängeln',
    '§ 536a BGB - Schadens- und Aufwendungsersatz bei Mängeln',
    '§ 536c BGB - Anzeigepflicht des Mieters',
    '§ 543 BGB - Außerordentliche fristlose Kündigung',
    '§ 823 BGB - Schadensersatzpflicht',
  ],
};

export default function RechtsprechungsanalysePage() {
  const [suchbegriff, setSuchbegriff] = useState('');
  const [gerichtsebene, setGerichtsebene] = useState('alle');
  const [rechtsgebiet, setRechtsgebiet] = useState('alle');
  const [zeitraum, setZeitraum] = useState('alle');
  const [isLoading, setIsLoading] = useState(false);
  const [ergebnis, setErgebnis] = useState<AnalyseErgebnis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [ausgewaehlteUrteile, setAusgewaehlteUrteile] = useState<Set<string>>(new Set());
  const [idToken, setIdToken] = useState<string | null>(null);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';

  const router = useRouter();

  // Check if user has access (Lawyer only)
  const hasAccess = hasTierAccess(userTier, 'lawyer');
  
  // Wrapper for actions that require tier
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  // Get auth token and check tier
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        router.push('/auth/login');
        return;
      }
      
      // Check tier - set tier for soft-lock instead of redirect
      const userDoc = await getDoc(doc(db, 'users', user.uid));
      if (userDoc.exists()) {
        const userData = userDoc.data();
        const tier = userData.tier || userData.dashboardType || 'free';
        setUserTier(tier);
        
        // Only get token for lawyers
        if (tier === 'lawyer') {
          const token = await user.getIdToken();
          setIdToken(token);
        }
      }
    });
    return () => unsubscribe();
  }, [router]);

  // Demo-Ergebnis für FREE/Professional anzeigen
  const zeigeDemoErgebnis = () => {
    setIsLoading(true);
    setError(null);
    setTimeout(() => {
      setErgebnis(DEMO_ERGEBNIS);
      setIsLoading(false);
    }, 1500);
  };

  const sucheRechtsprechung = async () => {
    if (!suchbegriff.trim()) {
      setError('Bitte geben Sie einen Suchbegriff ein.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const prompt = `Du bist ein Rechtsexperte für deutsches Immobilienrecht. Analysiere die aktuelle Rechtsprechung zum folgenden Thema:

SUCHANFRAGE: ${suchbegriff}

FILTER:
- Gerichtsebene: ${gerichtsebene === 'alle' ? 'Alle Gerichte (BGH, OLG, LG, AG)' : gerichtsebene}
- Rechtsgebiet: ${rechtsgebiet === 'alle' ? 'Alle Immobilien-Rechtsgebiete' : rechtsgebiet}
- Zeitraum: ${zeitraum === 'alle' ? 'Alle verfügbaren Urteile' : zeitraum === '5jahre' ? 'Letzte 5 Jahre' : zeitraum === '10jahre' ? 'Letzte 10 Jahre' : 'Letztes Jahr'}

Gib eine strukturierte Analyse mit folgendem JSON-Format zurück:
{
  "zusammenfassung": "Kurze Zusammenfassung der Rechtslage (2-3 Sätze)",
  "urteile": [
    {
      "gericht": "BGH/OLG/LG/AG + Ort",
      "aktenzeichen": "VIII ZR xxx/xx",
      "datum": "TT.MM.JJJJ",
      "thema": "Kurzes Thema",
      "leitsatz": "Der wesentliche Leitsatz des Urteils",
      "relevanz": 95
    }
  ],
  "rechtslage": "Ausführliche Darstellung der aktuellen Rechtslage basierend auf der Rechtsprechung",
  "empfehlung": "Praktische Empfehlung für die anwaltliche Beratung",
  "anwendbareNormen": ["§ 535 BGB", "§ 536 BGB"]
}

Gib mindestens 3-5 relevante Urteile an, sortiert nach Relevanz. Nutze echte Urteile aus der Datenbank.`;

      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        },
        body: JSON.stringify({
          query: prompt,
          target_jurisdiction: 'DE',
          user_role: 'ANWALT',
          source_filter: ['URTEIL', 'RECHTSPRECHUNG'],
        }),
      });

      if (!response.ok) {
        throw new Error('Fehler bei der Rechtsprechungssuche');
      }

      const data = await response.json();
      
      // Parse JSON from response
      const jsonMatch = data.answer?.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          const parsed = JSON.parse(jsonMatch[0]);
          setErgebnis(parsed);
        } catch {
          // Fallback: Create structured result from text
          setErgebnis({
            zusammenfassung: data.response?.substring(0, 300) || 'Analyse abgeschlossen.',
            urteile: [],
            rechtslage: data.response || 'Keine Details verfügbar.',
            empfehlung: 'Bitte prüfen Sie die Rechtslage im Einzelfall.',
            anwendbareNormen: [],
          });
        }
      } else {
        setErgebnis({
          zusammenfassung: data.response?.substring(0, 300) || 'Analyse abgeschlossen.',
          urteile: [],
          rechtslage: data.response || 'Keine Details verfügbar.',
          empfehlung: 'Bitte prüfen Sie die Rechtslage im Einzelfall.',
          anwendbareNormen: [],
        });
      }
    } catch (err) {
      setError('Fehler bei der Rechtsprechungsanalyse. Bitte versuchen Sie es erneut.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleUrteilAuswahl = (aktenzeichen: string) => {
    const neu = new Set(ausgewaehlteUrteile);
    if (neu.has(aktenzeichen)) {
      neu.delete(aktenzeichen);
    } else {
      neu.add(aktenzeichen);
    }
    setAusgewaehlteUrteile(neu);
  };

  const exportiereAuswahl = () => {
    if (!ergebnis || ausgewaehlteUrteile.size === 0) return;

    const ausgewaehlte = ergebnis.urteile.filter(u => ausgewaehlteUrteile.has(u.aktenzeichen));
    
    let text = `RECHTSPRECHUNGSANALYSE\n`;
    text += `Suchanfrage: ${suchbegriff}\n`;
    text += `Exportiert am: ${new Date().toLocaleDateString('de-DE')}\n\n`;
    text += `${'='.repeat(60)}\n\n`;
    
    text += `ZUSAMMENFASSUNG:\n${ergebnis.zusammenfassung}\n\n`;
    text += `RECHTSLAGE:\n${ergebnis.rechtslage}\n\n`;
    
    text += `AUSGEWÄHLTE URTEILE (${ausgewaehlte.length}):\n`;
    text += `${'-'.repeat(40)}\n\n`;
    
    ausgewaehlte.forEach((urteil, index) => {
      text += `${index + 1}. ${urteil.gericht} - ${urteil.aktenzeichen}\n`;
      text += `   Datum: ${urteil.datum}\n`;
      text += `   Thema: ${urteil.thema}\n`;
      text += `   Leitsatz: ${urteil.leitsatz}\n\n`;
    });

    text += `\nANWENDBARE NORMEN:\n`;
    ergebnis.anwendbareNormen.forEach(norm => {
      text += `• ${norm}\n`;
    });

    text += `\nEMPFEHLUNG:\n${ergebnis.empfehlung}\n`;
    
    text += `\n${'='.repeat(60)}\n`;
    text += `Generiert mit DOMULEX KI-Rechtsprechungsanalyse\n`;

    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Rechtsprechungsanalyse_${suchbegriff.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-[106px]">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">← Dashboard</Link>
              <Logo size="sm" />
            </div>
            <h1 className="text-lg font-semibold text-[#1e3a5f]">KI-Rechtsprechungsanalyse</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#1e3a5f]">⚖️ KI-Rechtsprechungsanalyse</h1>
          <p className="text-gray-600 mt-2">Durchsuchen Sie die aktuelle Rechtsprechung mit KI-Unterstützung</p>
        </div>

        {/* Suchbereich */}
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 mb-6">
          <div className="space-y-4">
            {/* Suchfeld */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Rechtsfrage oder Stichwort</label>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={suchbegriff}
                  onChange={(e) => setSuchbegriff(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && hasAccess && sucheRechtsprechung()}
                  placeholder="z.B. Schönheitsreparaturen starre Fristen, Eigenbedarfskündigung, Mietminderung Schimmel..."
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                  disabled={!hasAccess}
                />
                {hasAccess ? (
                  <button
                    onClick={() => sucheRechtsprechung()}
                    disabled={isLoading}
                    className="px-6 py-3 bg-[#1e3a5f] text-white rounded-lg font-medium hover:bg-[#2d4a6f] transition-colors disabled:opacity-50"
                  >
                    {isLoading ? '🔍 Suche...' : '🔍 Analysieren'}
                  </button>
                ) : (
                  <button
                    onClick={() => setShowUpgradeModal(true)}
                    className="px-6 py-3 bg-gray-400 text-white rounded-lg font-medium hover:bg-gray-500 transition-colors flex items-center gap-2"
                  >
                    🔒 Upgrade erforderlich
                  </button>
                )}
              </div>
            </div>

            {/* Filter */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Gerichtsebene</label>
                <select
                  value={gerichtsebene}
                  onChange={(e) => setGerichtsebene(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                >
                  {GERICHTSEBENEN.map(g => (
                    <option key={g.id} value={g.id}>{g.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Rechtsgebiet</label>
                <select
                  value={rechtsgebiet}
                  onChange={(e) => setRechtsgebiet(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                >
                  {RECHTSGEBIETE.map(r => (
                    <option key={r.id} value={r.id}>{r.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Zeitraum</label>
                <select
                  value={zeitraum}
                  onChange={(e) => setZeitraum(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                >
                  <option value="alle">Alle Urteile</option>
                  <option value="1jahr">Letztes Jahr</option>
                  <option value="5jahre">Letzte 5 Jahre</option>
                  <option value="10jahre">Letzte 10 Jahre</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Fehler */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 text-red-700">
            {error}
          </div>
        )}

        {/* Ergebnisse */}
        {ergebnis && (
          <div className="space-y-6">
            {/* Demo-Banner für FREE/Professional */}
            {!hasAccess && (
              <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-300 rounded-xl p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">🔐</span>
                    <div>
                      <p className="text-amber-800 font-medium">Demo-Analyse</p>
                      <p className="text-amber-700/70 text-sm">Dies ist eine Beispiel-Rechtsprechungsanalyse. Upgraden Sie für eigene Recherchen.</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setShowUpgradeModal(true)}
                    className="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-lg font-medium text-sm transition-all"
                  >
                    Jetzt upgraden
                  </button>
                </div>
              </div>
            )}

            {/* Zusammenfassung */}
            <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] rounded-xl p-6 text-white">
              <h2 className="text-xl font-bold mb-3">📋 Zusammenfassung</h2>
              <p className="text-white/90">{ergebnis.zusammenfassung}</p>
              
              {ergebnis.anwendbareNormen.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {ergebnis.anwendbareNormen.map((norm, i) => (
                    <span key={i} className="px-3 py-1 bg-white/20 rounded-full text-sm">
                      {norm}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Urteile */}
            {ergebnis.urteile.length > 0 && (
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
                <div className="p-4 border-b border-gray-100 flex justify-between items-center">
                  <h2 className="text-lg font-bold text-[#1e3a5f]">⚖️ Relevante Urteile ({ergebnis.urteile.length})</h2>
                  {ausgewaehlteUrteile.size > 0 && (
                    <button
                      onClick={exportiereAuswahl}
                      className="px-4 py-2 bg-[#b8860b] text-white rounded-lg text-sm font-medium hover:bg-[#a07608]"
                    >
                      📥 {ausgewaehlteUrteile.size} Urteile exportieren
                    </button>
                  )}
                </div>
                <div className="divide-y divide-gray-100">
                  {ergebnis.urteile.map((urteil, index) => (
                    <div key={index} className="p-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={ausgewaehlteUrteile.has(urteil.aktenzeichen)}
                          onChange={() => toggleUrteilAuswahl(urteil.aktenzeichen)}
                          className="mt-1 h-5 w-5 text-[#1e3a5f] rounded border-gray-300"
                        />
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-3">
                              <span className="font-bold text-[#1e3a5f]">{urteil.gericht}</span>
                              <span className="px-2 py-1 bg-gray-100 rounded text-sm font-mono">{urteil.aktenzeichen}</span>
                              <span className="text-gray-500 text-sm">{urteil.datum}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className="text-xs text-gray-500">Relevanz:</span>
                              <div className="w-20 bg-gray-200 rounded-full h-2">
                                <div
                                  className={`h-2 rounded-full ${urteil.relevanz >= 80 ? 'bg-green-500' : urteil.relevanz >= 60 ? 'bg-yellow-500' : 'bg-orange-500'}`}
                                  style={{ width: `${urteil.relevanz}%` }}
                                />
                              </div>
                              <span className="text-sm font-medium">{urteil.relevanz}%</span>
                            </div>
                          </div>
                          <p className="font-medium text-gray-800 mb-1">{urteil.thema}</p>
                          <p className="text-gray-600 text-sm">{urteil.leitsatz}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Rechtslage */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <h2 className="text-lg font-bold text-[#1e3a5f] mb-4">📚 Aktuelle Rechtslage</h2>
              <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-line">
                {ergebnis.rechtslage}
              </div>
            </div>

            {/* Empfehlung */}
            <div className="bg-purple-50 border border-purple-200 rounded-xl p-6">
              <h2 className="text-lg font-bold text-purple-800 mb-3">💡 Empfehlung für die Beratungspraxis</h2>
              <p className="text-purple-700">{ergebnis.empfehlung}</p>
            </div>

            {/* Export alle */}
            <div className="flex justify-center">
              <button
                onClick={() => {
                  // Alle auswählen und exportieren
                  const alle = new Set(ergebnis.urteile.map(u => u.aktenzeichen));
                  setAusgewaehlteUrteile(alle);
                  setTimeout(exportiereAuswahl, 100);
                }}
                className="px-6 py-3 bg-[#1e3a5f] text-white rounded-lg font-medium hover:bg-[#2d4a6f] transition-colors"
              >
                📥 Vollständige Analyse exportieren
              </button>
            </div>
          </div>
        )}

        {/* Beispielsuchen */}
        {!ergebnis && !isLoading && (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
            <h3 className="text-lg font-bold text-[#1e3a5f] mb-4">💡 Beispielsuchen</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                'Schönheitsreparaturen starre Fristenregelung unwirksam',
                'Eigenbedarfskündigung Voraussetzungen BGH',
                'Mietminderung bei Schimmelbefall Höhe',
                'Nebenkostenabrechnung Formelle Fehler',
                'Kaution Verjährung Rückzahlung',
                'Gewerbemietvertrag Indexmiete Anpassung',
              ].map((beispiel, i) => (
                <button
                  key={i}
                  onClick={() => setSuchbegriff(beispiel)}
                  className="text-left px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-gray-700 transition-colors"
                >
                  🔍 {beispiel}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="lawyer"
        feature="Rechtsprechungssuche"
      />
    </div>
  );
}
