'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import UpgradeModal from '@/components/UpgradeModal';
import { auth, db } from '@/lib/firebase';
import { hasTierAccess } from '@/lib/tierUtils';
import { onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';

interface FallAnalyse {
  zusammenfassung: string;
  erfolgsaussichten: number;
  risikoeinschaetzung: 'gering' | 'mittel' | 'hoch';
  empfehlung: 'klage' | 'vergleich' | 'ablehnung' | 'weiteresPruefung';
  empfehlungText: string;
  naechsteSchritte: {
    schritt: string;
    dokument: string;
    prioritaet: 'hoch' | 'mittel' | 'niedrig';
  }[];
  aehnlicheUrteile: {
    gericht: string;
    aktenzeichen: string;
    datum: string;
    ausgang: 'gewonnen' | 'verloren' | 'vergleich';
    kurzfassung: string;
    relevanz: number;
  }[];
  rechtlicheArgumente: {
    proMandant: string[];
    contraMandant: string[];
  };
  anwendbareNormen: string[];
  prozesskostenSchaetzung?: {
    eigeneKosten: number;
    gegnerKosten: number;
    gerichtskosten: number;
  };
}

const RECHTSGEBIETE = [
  { id: 'mietrecht', label: 'Mietrecht', beispiele: 'Kündigung, Mietminderung, Schönheitsreparaturen' },
  { id: 'weg', label: 'WEG-Recht', beispiele: 'Beschlussanfechtung, Sonderumlage, Verwalter' },
  { id: 'kaufrecht', label: 'Immobilienkauf', beispiele: 'Mängel, Rücktritt, Arglist' },
  { id: 'baurecht', label: 'Baurecht', beispiele: 'Mängel, VOB, Abnahme, Gewährleistung' },
  { id: 'nachbarrecht', label: 'Nachbarrecht', beispiele: 'Überbau, Immissionen, Grenzstreit' },
  { id: 'maklerrecht', label: 'Maklerrecht', beispiele: 'Provision, Widerrufsrecht' },
];

const PARTEIROLLEN = [
  { id: 'mieter', label: 'Mieter' },
  { id: 'vermieter', label: 'Vermieter' },
  { id: 'kaeufer', label: 'Käufer' },
  { id: 'verkaeufer', label: 'Verkäufer' },
  { id: 'eigentuemer', label: 'WEG-Eigentümer' },
  { id: 'bauherr', label: 'Bauherr' },
  { id: 'unternehmer', label: 'Bauunternehmer' },
];

// ===== DEMO-DATEN FÜR FREE/PROFESSIONAL-NUTZER =====
const DEMO_ANALYSE: FallAnalyse = {
  zusammenfassung: 'Der Mandant (Mieter) mindert seit 3 Monaten die Miete um 20% wegen Schimmelbefall im Schlafzimmer. Der Vermieter bestreitet einen Mangel und hat Klage auf Zahlung der einbehaltenen Miete erhoben.',
  erfolgsaussichten: 72,
  risikoeinschaetzung: 'mittel',
  empfehlung: 'vergleich',
  empfehlungText: 'Die Rechtslage ist für den Mandanten grundsätzlich günstig, da Schimmelbefall einen erheblichen Mangel darstellt. Allerdings besteht Beweisrisiko hinsichtlich der Ursache (baulich vs. Lüftungsverhalten). Ein Vergleich mit 15% Mietminderung und Beseitigungspflicht des Vermieters erscheint wirtschaftlich sinnvoll.',
  naechsteSchritte: [
    { schritt: 'Sachverständigengutachten zur Schimmelursache beantragen', dokument: 'Beweisantrag', prioritaet: 'hoch' },
    { schritt: 'Mängelanzeigen und Schriftverkehr zusammenstellen', dokument: 'Mängelrüge', prioritaet: 'hoch' },
    { schritt: 'Fotodokumentation des Schimmels sichern', dokument: 'Beweismittel', prioritaet: 'mittel' },
    { schritt: 'Vergleichsverhandlungen mit Gegenseite führen', dokument: 'Vergleichsvorschlag', prioritaet: 'mittel' },
  ],
  aehnlicheUrteile: [
    { gericht: 'BGH', aktenzeichen: 'VIII ZR 138/18', datum: '2019-07-10', ausgang: 'gewonnen', kurzfassung: 'Mieter muss nur darlegen, dass Mangel vorhanden ist. Vermieter trägt Beweislast für Ursache.', relevanz: 95 },
    { gericht: 'LG Berlin', aktenzeichen: '65 S 400/17', datum: '2018-03-15', ausgang: 'gewonnen', kurzfassung: '20% Mietminderung bei Schimmel im Schlafzimmer angemessen.', relevanz: 88 },
    { gericht: 'AG München', aktenzeichen: '461 C 19847/20', datum: '2021-05-20', ausgang: 'vergleich', kurzfassung: 'Vergleich mit 15% Minderung bei streitiger Schimmelursache.', relevanz: 82 },
  ],
  rechtlicheArgumente: {
    proMandant: [
      'Schimmelbefall stellt einen erheblichen Mangel dar (§ 536 BGB)',
      'Mieter hat Mangel ordnungsgemäß angezeigt (§ 536c BGB)',
      'BGH: Vermieter trägt Beweislast für Ursache des Schimmels',
      'Minderung kraft Gesetzes ohne Vorankündigung (§ 536 BGB)',
    ],
    contraMandant: [
      'Vermieter behauptet falsches Lüftungsverhalten des Mieters',
      'Keine unabhängige Feststellung der Schimmelursache bisher',
      'Mögliches Mitverschulden bei unzureichender Beheizung',
    ],
  },
  anwendbareNormen: [
    '§ 536 BGB - Mietminderung bei Sach- und Rechtsmängeln',
    '§ 536a BGB - Schadens- und Aufwendungsersatz',
    '§ 536c BGB - Anzeigepflicht des Mieters',
    '§ 543 BGB - Außerordentliche fristlose Kündigung',
  ],
  prozesskostenSchaetzung: {
    eigeneKosten: 1850,
    gegnerKosten: 1850,
    gerichtskosten: 438,
  },
};

export default function FallanalysePage() {
  const [rechtsgebiet, setRechtsgebiet] = useState('mietrecht');
  const [partei, setPartei] = useState('mieter');
  const [sachverhalt, setSachverhalt] = useState('');
  const [streitpunkt, setStreitpunkt] = useState('');
  const [streitwert, setStreitwert] = useState<number | ''>('');
  const [beweislage, setBeweislage] = useState('gut');
  
  const [isLoading, setIsLoading] = useState(false);
  const [analyse, setAnalyse] = useState<FallAnalyse | null>(null);
  const [error, setError] = useState<string | null>(null);
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

  const analysiereFall = async () => {
    if (!sachverhalt.trim() || !streitpunkt.trim()) {
      setError('Bitte füllen Sie Sachverhalt und Streitpunkt aus.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const prompt = `Du bist ein erfahrener Fachanwalt für Immobilienrecht. Analysiere den folgenden Fall und gib eine fundierte Einschätzung der Erfolgsaussichten.

FALLDETAILS:
- Rechtsgebiet: ${RECHTSGEBIETE.find(r => r.id === rechtsgebiet)?.label}
- Mandant ist: ${PARTEIROLLEN.find(p => p.id === partei)?.label}
- Geschätzter Streitwert: ${streitwert ? `${streitwert} €` : 'Nicht angegeben'}
- Beweislage: ${beweislage === 'gut' ? 'Gut (Dokumente, Zeugen vorhanden)' : beweislage === 'mittel' ? 'Mittel (teilweise Nachweise)' : 'Schwach (wenig Beweise)'}

SACHVERHALT:
${sachverhalt}

STREITPUNKT / RECHTSFRAGE:
${streitpunkt}

Analysiere den Fall und gib eine strukturierte Antwort im folgenden JSON-Format:
{
  "zusammenfassung": "Kurze Zusammenfassung des Falls und der Rechtslage (2-3 Sätze)",
  "erfolgsaussichten": 75,
  "risikoeinschaetzung": "mittel",
  "empfehlung": "klage",
  "empfehlungText": "Ausführliche Begründung der Empfehlung mit konkreten Handlungsschritten",
  "naechsteSchritte": [
    {"schritt": "Außergerichtliches Mahnschreiben versenden", "dokument": "Mahnung", "prioritaet": "hoch"},
    {"schritt": "Frist setzen zur Mängelbeseitigung", "dokument": "Fristsetzung", "prioritaet": "hoch"},
    {"schritt": "Klageschrift vorbereiten", "dokument": "Klageschrift", "prioritaet": "mittel"}
  ],
  "aehnlicheUrteile": [
    {
      "gericht": "BGH",
      "aktenzeichen": "VIII ZR 123/20",
      "datum": "15.03.2021",
      "ausgang": "gewonnen",
      "kurzfassung": "Was wurde entschieden",
      "relevanz": 90
    }
  ],
  "rechtlicheArgumente": {
    "proMandant": ["Argument 1", "Argument 2"],
    "contraMandant": ["Gegenargument 1", "Gegenargument 2"]
  },
  "anwendbareNormen": ["§ 536 BGB", "§ 543 BGB"]
}

WICHTIG für naechsteSchritte:
- Gib 3-5 konkrete nächste Handlungsschritte an
- dokument kann sein: "Mahnung", "Fristsetzung", "Klageschrift", "Stellungnahme", "Vergleichsvorschlag", "Widerspruch", "Kündigung", "Abmahnung", "Mietminderung", "Mängelanzeige", "Sonstiges"
- prioritaet: "hoch", "mittel" oder "niedrig"

Erfolgsaussichten als Zahl 0-100. Risikoeinschätzung: "gering", "mittel" oder "hoch". 
Empfehlung: "klage" (Klage erheben), "vergleich" (Vergleich anstreben), "ablehnung" (Mandat ablehnen) oder "weiteresPruefung" (weitere Prüfung nötig).
Gib mindestens 2-3 ähnliche Urteile an, sortiert nach Relevanz.`;

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
          source_filter: ['URTEIL', 'GESETZ', 'RECHTSPRECHUNG'],
        }),
      });

      if (!response.ok) {
        throw new Error('Fehler bei der Fallanalyse');
      }

      const data = await response.json();
      
      // Parse JSON from response
      const jsonMatch = data.answer?.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          const parsed = JSON.parse(jsonMatch[0]);
          // Ensure naechsteSchritte exists
          if (!parsed.naechsteSchritte) {
            parsed.naechsteSchritte = [];
          }
          setAnalyse(parsed);
        } catch {
          // Fallback
          setAnalyse({
            zusammenfassung: data.answer?.substring(0, 500) || 'Analyse durchgeführt.',
            erfolgsaussichten: 50,
            risikoeinschaetzung: 'mittel',
            empfehlung: 'weiteresPruefung',
            empfehlungText: data.response || 'Weitere Prüfung empfohlen.',
            naechsteSchritte: [],
            aehnlicheUrteile: [],
            rechtlicheArgumente: { proMandant: [], contraMandant: [] },
            anwendbareNormen: [],
          });
        }
      } else {
        setAnalyse({
          zusammenfassung: data.response?.substring(0, 500) || 'Analyse durchgeführt.',
          erfolgsaussichten: 50,
          risikoeinschaetzung: 'mittel',
          empfehlung: 'weiteresPruefung',
          naechsteSchritte: [],
          empfehlungText: data.response || 'Weitere Prüfung empfohlen.',
          aehnlicheUrteile: [],
          rechtlicheArgumente: { proMandant: [], contraMandant: [] },
          anwendbareNormen: [],
        });
      }
    } catch (err) {
      setError('Fehler bei der Fallanalyse. Bitte versuchen Sie es erneut.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const getErfolgsColor = (prozent: number) => {
    if (prozent >= 70) return 'text-green-600 bg-green-50';
    if (prozent >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getRisikoColor = (risiko: string) => {
    if (risiko === 'gering') return 'bg-green-100 text-green-800';
    if (risiko === 'mittel') return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getEmpfehlungBadge = (empfehlung: string) => {
    switch (empfehlung) {
      case 'klage': return { icon: '⚖️', text: 'Klage empfohlen', color: 'bg-green-600 text-white' };
      case 'vergleich': return { icon: '🤝', text: 'Vergleich anstreben', color: 'bg-blue-600 text-white' };
      case 'ablehnung': return { icon: '❌', text: 'Mandat ablehnen', color: 'bg-red-600 text-white' };
      default: return { icon: '🔍', text: 'Weitere Prüfung', color: 'bg-gray-600 text-white' };
    }
  };

  const getAusgangBadge = (ausgang: string) => {
    switch (ausgang) {
      case 'gewonnen': return { text: 'Gewonnen', color: 'bg-green-100 text-green-800' };
      case 'verloren': return { text: 'Verloren', color: 'bg-red-100 text-red-800' };
      default: return { text: 'Vergleich', color: 'bg-blue-100 text-blue-800' };
    }
  };

  const exportiereAnalyse = () => {
    if (!analyse) return;

    const empf = getEmpfehlungBadge(analyse.empfehlung);
    
    let text = `FALLANALYSE - DOMULEX\n`;
    text += `${'='.repeat(60)}\n`;
    text += `Erstellt am: ${new Date().toLocaleDateString('de-DE')}\n\n`;
    
    text += `FALLDETAILS:\n`;
    text += `- Rechtsgebiet: ${RECHTSGEBIETE.find(r => r.id === rechtsgebiet)?.label}\n`;
    text += `- Mandant: ${PARTEIROLLEN.find(p => p.id === partei)?.label}\n`;
    text += `- Streitwert: ${streitwert ? `${streitwert} €` : 'Nicht angegeben'}\n`;
    text += `- Beweislage: ${beweislage}\n\n`;
    
    text += `SACHVERHALT:\n${sachverhalt}\n\n`;
    text += `STREITPUNKT:\n${streitpunkt}\n\n`;
    
    text += `${'='.repeat(60)}\n`;
    text += `ANALYSE-ERGEBNIS\n`;
    text += `${'='.repeat(60)}\n\n`;
    
    text += `ZUSAMMENFASSUNG:\n${analyse.zusammenfassung}\n\n`;
    text += `ERFOLGSAUSSICHTEN: ${analyse.erfolgsaussichten}%\n`;
    text += `RISIKOEINSCHÄTZUNG: ${analyse.risikoeinschaetzung.toUpperCase()}\n`;
    text += `EMPFEHLUNG: ${empf.text}\n\n`;
    
    text += `BEGRÜNDUNG:\n${analyse.empfehlungText}\n\n`;
    
    if (analyse.rechtlicheArgumente.proMandant.length > 0) {
      text += `ARGUMENTE FÜR MANDANT:\n`;
      analyse.rechtlicheArgumente.proMandant.forEach((arg, i) => {
        text += `  ${i + 1}. ${arg}\n`;
      });
      text += `\n`;
    }
    
    if (analyse.rechtlicheArgumente.contraMandant.length > 0) {
      text += `ARGUMENTE GEGEN MANDANT:\n`;
      analyse.rechtlicheArgumente.contraMandant.forEach((arg, i) => {
        text += `  ${i + 1}. ${arg}\n`;
      });
      text += `\n`;
    }
    
    if (analyse.anwendbareNormen.length > 0) {
      text += `ANWENDBARE NORMEN:\n`;
      analyse.anwendbareNormen.forEach(norm => {
        text += `  • ${norm}\n`;
      });
      text += `\n`;
    }
    
    if (analyse.aehnlicheUrteile.length > 0) {
      text += `ÄHNLICHE URTEILE:\n`;
      text += `${'-'.repeat(40)}\n`;
      analyse.aehnlicheUrteile.forEach((urteil, i) => {
        text += `\n${i + 1}. ${urteil.gericht} - ${urteil.aktenzeichen} (${urteil.datum})\n`;
        text += `   Ausgang: ${urteil.ausgang.toUpperCase()}\n`;
        text += `   ${urteil.kurzfassung}\n`;
      });
    }
    
    text += `\n${'='.repeat(60)}\n`;
    text += `Generiert mit DOMULEX KI-Fallanalyse\n`;
    text += `HINWEIS: Diese Analyse ersetzt keine individuelle anwaltliche Prüfung.\n`;

    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Fallanalyse_${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-16">
            <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">← Dashboard</Link>
            <h1 className="text-lg font-semibold text-[#1e3a5f]">KI-Fallanalyse</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#1e3a5f]">🎯 KI-Fallanalyse</h1>
          <p className="text-gray-600 mt-2">Erfolgsaussichten einschätzen • Risiken bewerten • Strategie entwickeln</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Eingabebereich */}
          <div className="lg:col-span-2 space-y-6">
            {/* Grunddaten */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <h2 className="text-lg font-bold text-[#1e3a5f] mb-4">📋 Falldetails</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Rechtsgebiet</label>
                  <select
                    value={rechtsgebiet}
                    onChange={(e) => setRechtsgebiet(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:ring-2 focus:ring-[#1e3a5f]">
                    {RECHTSGEBIETE.map(r => (
                      <option key={r.id} value={r.id}>{r.label}</option>
                    ))}
                  </select>
                  <p className="text-xs text-gray-500 mt-1">{RECHTSGEBIETE.find(r => r.id === rechtsgebiet)?.beispiele}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Mandant ist</label>
                  <select
                    value={partei}
                    onChange={(e) => setPartei(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:ring-2 focus:ring-[#1e3a5f]">
                    {PARTEIROLLEN.map(p => (
                      <option key={p.id} value={p.id}>{p.label}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Geschätzter Streitwert (€)</label>
                  <input
                    type="number"
                    value={streitwert}
                    onChange={(e) => setStreitwert(e.target.value ? Number(e.target.value) : '')}
                    placeholder="z.B. 5000"
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-[#1e3a5f]"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Beweislage</label>
                  <select
                    value={beweislage}
                    onChange={(e) => setBeweislage(e.target.value)}
                    className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-gray-900 focus:ring-2 focus:ring-[#1e3a5f]">
                    <option value="gut">Gut (Dokumente, Zeugen vorhanden)</option>
                    <option value="mittel">Mittel (teilweise Nachweise)</option>
                    <option value="schwach">Schwach (wenig Beweise)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Sachverhalt */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <h2 className="text-lg font-bold text-[#1e3a5f] mb-4">📝 Sachverhalt</h2>
              <textarea
                value={sachverhalt}
                onChange={(e) => setSachverhalt(e.target.value)}
                rows={6}
                placeholder="Beschreiben Sie den Sachverhalt ausführlich: Was ist passiert? Wann? Wer ist beteiligt? Welche Dokumente liegen vor?"
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-[#1e3a5f]"
              />
            </div>

            {/* Streitpunkt */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <h2 className="text-lg font-bold text-[#1e3a5f] mb-4">⚡ Streitpunkt / Rechtsfrage</h2>
              <textarea
                value={streitpunkt}
                onChange={(e) => setStreitpunkt(e.target.value)}
                rows={3}
                placeholder="Was ist das konkrete Ziel des Mandanten? Was soll erreicht werden? z.B. 'Mietminderung wegen Schimmel durchsetzen' oder 'Eigenbedarfskündigung abwehren'"
                className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-[#1e3a5f]"
              />
            </div>

            {/* Analyse-Button */}
            {hasAccess ? (
              <button
                onClick={() => {
                  if (!sachverhalt.trim() || !streitpunkt.trim()) {
                    setError('Bitte füllen Sie Sachverhalt und Streitpunkt aus.');
                    return;
                  }
                  analysiereFall();
                }}
                disabled={isLoading}
                className="w-full py-4 bg-[#1e3a5f] text-white rounded-xl font-bold text-lg hover:bg-[#2d4a6f] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? '🔄 KI analysiert Fall...' : '🎯 Fall analysieren'}
              </button>
            ) : (
              <button
                onClick={() => setShowUpgradeModal(true)}
                className="w-full py-4 bg-gray-400 text-white rounded-xl font-bold text-lg cursor-pointer hover:bg-gray-500 transition-colors flex items-center justify-center gap-2"
              >
                🔒 Upgrade auf Lawyer Pro erforderlich
              </button>
            )}

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
                {error}
              </div>
            )}
          </div>

          {/* Seitenleiste mit Tipps */}
          <div className="space-y-6">
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-5">
              <h3 className="font-bold text-blue-800 mb-3">💡 Tipps für gute Ergebnisse</h3>
              <ul className="text-sm text-blue-700 space-y-2">
                <li>• Beschreiben Sie den Sachverhalt chronologisch</li>
                <li>• Nennen Sie konkrete Daten und Beträge</li>
                <li>• Erwähnen Sie vorhandene Beweismittel</li>
                <li>• Formulieren Sie eine klare Rechtsfrage</li>
              </ul>
            </div>

            <div className="bg-amber-50 border border-amber-200 rounded-xl p-5">
              <h3 className="font-bold text-amber-700 mb-3">⚠️ Hinweis</h3>
              <p className="text-sm text-amber-600">
                Diese KI-Analyse dient als Ersteinschätzung und ersetzt nicht die individuelle anwaltliche Prüfung. 
                Die Erfolgsaussichten basieren auf vergleichbarer Rechtsprechung.
              </p>
            </div>
          </div>
        </div>

        {/* Ergebnisbereich */}
        {analyse && (
          <div className="mt-8 space-y-6">
            {/* Demo-Banner für FREE/Professional */}
            {!hasAccess && (
              <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-300 rounded-xl p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">🔐</span>
                    <div>
                      <p className="text-amber-800 font-medium">Demo-Analyse</p>
                      <p className="text-amber-700/70 text-sm">Dies ist eine Beispiel-Fallanalyse. Upgraden Sie für Ihre eigenen Fälle.</p>
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

            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-[#1e3a5f]">📊 Analyse-Ergebnis</h2>
              <button
                onClick={exportiereAnalyse}
                className="px-4 py-2 bg-[#1e3a5f] text-white rounded-lg font-medium hover:bg-[#2d4a6f]"
              >
                📥 Analyse exportieren
              </button>
            </div>

            {/* Hauptergebnis */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Erfolgsaussichten */}
              <div className={`rounded-xl p-6 text-center ${getErfolgsColor(analyse.erfolgsaussichten)}`}>
                <p className="text-sm font-medium mb-1">Erfolgsaussichten</p>
                <p className="text-4xl font-bold">{analyse.erfolgsaussichten}%</p>
              </div>

              {/* Risiko */}
              <div className={`rounded-xl p-6 text-center ${getRisikoColor(analyse.risikoeinschaetzung)}`}>
                <p className="text-sm font-medium mb-1">Prozessrisiko</p>
                <p className="text-2xl font-bold capitalize">{analyse.risikoeinschaetzung}</p>
              </div>

              {/* Empfehlung */}
              <div className={`rounded-xl p-6 text-center ${getEmpfehlungBadge(analyse.empfehlung).color}`}>
                <p className="text-sm font-medium mb-1 opacity-90">Empfehlung</p>
                <p className="text-xl font-bold">
                  {getEmpfehlungBadge(analyse.empfehlung).icon} {getEmpfehlungBadge(analyse.empfehlung).text}
                </p>
              </div>
            </div>

            {/* Zusammenfassung */}
            <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] rounded-xl p-6 text-white">
              <h3 className="text-lg font-bold mb-3">📋 Zusammenfassung</h3>
              <p className="text-white/90">{analyse.zusammenfassung}</p>
            </div>

            {/* Empfehlungstext */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <h3 className="text-lg font-bold text-[#1e3a5f] mb-3">💼 Strategieempfehlung</h3>
              <p className="text-gray-700 whitespace-pre-line">{analyse.empfehlungText}</p>
            </div>

            {/* Nächste Schritte mit Vorlagen-Links */}
            {analyse.naechsteSchritte && analyse.naechsteSchritte.length > 0 && (
              <div className="bg-purple-50 border border-purple-200 rounded-xl p-6">
                <h3 className="text-lg font-bold text-purple-800 mb-4">🚀 Nächste Schritte</h3>
                <div className="space-y-3">
                  {analyse.naechsteSchritte.map((schritt, i) => (
                    <div key={i} className="flex items-center justify-between bg-white rounded-lg p-4 border border-gray-100">
                      <div className="flex items-center gap-3">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm ${
                          schritt.prioritaet === 'hoch' ? 'bg-red-500' : 
                          schritt.prioritaet === 'mittel' ? 'bg-yellow-500' : 'bg-gray-500'
                        }`}>
                          {i + 1}
                        </span>
                        <div>
                          <p className="font-medium text-gray-900">{schritt.schritt}</p>
                          <p className="text-xs text-gray-500">
                            Priorität: <span className={`font-medium ${
                              schritt.prioritaet === 'hoch' ? 'text-red-600' : 
                              schritt.prioritaet === 'mittel' ? 'text-yellow-600' : 'text-gray-500'
                            }`}>{schritt.prioritaet}</span>
                          </p>
                        </div>
                      </div>
                      <Link 
                        href={`/app/templates?create=${encodeURIComponent(schritt.dokument)}&context=${encodeURIComponent(sachverhalt.substring(0, 200))}&streitpunkt=${encodeURIComponent(streitpunkt.substring(0, 100))}`}
                        className="px-4 py-2 bg-purple-600 text-white rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors flex items-center gap-2"
                      >
                        ✍️ {schritt.dokument} erstellen
                      </Link>
                    </div>
                  ))}
                </div>
                <p className="text-xs text-purple-600 mt-4">
                  💡 Klicken Sie auf einen Schritt, um die passende Vorlage mit KI zu erstellen
                </p>
              </div>
            )}

            {/* Argumente Pro/Contra */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {analyse.rechtlicheArgumente.proMandant.length > 0 && (
                <div className="bg-green-50 border border-green-200 rounded-xl p-5">
                  <h3 className="font-bold text-green-800 mb-3">✅ Argumente für Mandant</h3>
                  <ul className="space-y-2">
                    {analyse.rechtlicheArgumente.proMandant.map((arg, i) => (
                      <li key={i} className="text-green-700 text-sm flex gap-2">
                        <span>•</span>
                        <span>{arg}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {analyse.rechtlicheArgumente.contraMandant.length > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-5">
                  <h3 className="font-bold text-red-800 mb-3">⚠️ Argumente gegen Mandant</h3>
                  <ul className="space-y-2">
                    {analyse.rechtlicheArgumente.contraMandant.map((arg, i) => (
                      <li key={i} className="text-red-700 text-sm flex gap-2">
                        <span>•</span>
                        <span>{arg}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Anwendbare Normen */}
            {analyse.anwendbareNormen.length > 0 && (
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
                <h3 className="font-bold text-[#1e3a5f] mb-3">📚 Anwendbare Normen</h3>
                <div className="flex flex-wrap gap-2">
                  {analyse.anwendbareNormen.map((norm, i) => (
                    <span key={i} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm font-medium border border-blue-200">
                      {norm}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Ähnliche Urteile */}
            {analyse.aehnlicheUrteile.length > 0 && (
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
                <div className="p-4 border-b border-gray-100">
                  <h3 className="text-lg font-bold text-[#1e3a5f]">⚖️ Ähnliche Urteile</h3>
                </div>
                <div className="divide-y divide-gray-100">
                  {analyse.aehnlicheUrteile.map((urteil, index) => (
                    <div key={index} className="p-4 hover:bg-gray-50">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <span className="font-bold text-gray-900">{urteil.gericht}</span>
                          <span className="px-2 py-1 bg-gray-100 rounded text-sm font-mono text-gray-700">{urteil.aktenzeichen}</span>
                          <span className="text-gray-500 text-sm">{urteil.datum}</span>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getAusgangBadge(urteil.ausgang).color}`}>
                            {getAusgangBadge(urteil.ausgang).text}
                          </span>
                          <span className="text-xs text-gray-500">{urteil.relevanz}% relevant</span>
                        </div>
                      </div>
                      <p className="text-gray-600 text-sm">{urteil.kurzfassung}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="lawyer"
        feature="KI-Fallanalyse"
      />
    </div>
  );
}
