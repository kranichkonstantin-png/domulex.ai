'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc, collection, addDoc, updateDoc, increment } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import UpgradeModal from '@/components/UpgradeModal';
import { hasTierAccess } from '@/lib/tierUtils';

interface ImmobilienDaten {
  kaufpreis: number;
  nebenkosten_prozent: number;
  renovierung: number;
  eigenkapital: number;
  zinssatz: number;
  tilgung: number;
  laufzeit: number;
  kaltmiete: number;
  nebenkosten_umlage: number;
  verwaltung: number;
  instandhaltung_prozent: number;
  mietausfall_prozent: number;
  wertsteigerung_prozent: number;
  // NEU: Multi-Einheiten & Steuer
  anzahlEinheiten: number;
  wohnflaeche: number;
  baujahr: number;
  grundstuecksanteil: number; // % Kaufpreis = Grundstück (nicht abschreibbar)
  steuersatz: number; // Persönlicher Grenzsteuersatz
}

const initialDaten: ImmobilienDaten = {
  kaufpreis: 300000,
  nebenkosten_prozent: 12,
  renovierung: 10000,
  eigenkapital: 80000,
  zinssatz: 4.0,
  tilgung: 2.0,
  laufzeit: 30,
  kaltmiete: 1200,
  nebenkosten_umlage: 200,
  verwaltung: 30,
  instandhaltung_prozent: 1.0,
  mietausfall_prozent: 3.0,
  wertsteigerung_prozent: 2.0,
  // NEU
  anzahlEinheiten: 1,
  wohnflaeche: 80,
  baujahr: 1990,
  grundstuecksanteil: 20,
  steuersatz: 42,
};

// Vordefinierte KI-Erklärungen für Kennzahlen
const KENNZAHL_ERKLAERUNGEN: Record<string, { titel: string; erklaerung: string }> = {
  bruttorendite: {
    titel: 'Bruttorendite',
    erklaerung: `Die Bruttorendite zeigt das Verhältnis der Jahresmiete zum Kaufpreis – ohne Berücksichtigung von Nebenkosten, Finanzierung oder Leerstand.

**Formel:** (Jahresmiete ÷ Kaufpreis) × 100

**Richtwerte:**
• Unter 4%: Eher unattraktiv, typisch in Großstädten
• 4-6%: Durchschnittlich, meist sichere Lagen
• Über 6%: Attraktiv, aber Risiko prüfen

**Rechtlicher Hinweis:**
Die Bruttorendite ist eine erste Orientierung. Sie berücksichtigt keine Kaufnebenkosten (Grunderwerbsteuer, Notar, Makler) und keine laufenden Kosten. Für eine realistische Einschätzung ist die Nettorendite relevanter.`
  },
  nettorendite: {
    titel: 'Nettorendite',
    erklaerung: `Die Nettorendite berücksichtigt alle laufenden Kosten und zeigt die tatsächliche Verzinsung Ihres Kapitals vor Steuern.

**Formel:** ((Jahresmiete - Kosten) ÷ Gesamtinvestition) × 100

**Berücksichtigt werden:**
• Nicht umlegbare Nebenkosten
• Verwaltungskosten
• Instandhaltungsrücklage
• Mietausfallwagnis (§ 29 II. BV: ca. 2%)

**Richtwerte:**
• Unter 3%: Kritisch hinterfragen
• 3-5%: Solide Rendite
• Über 5%: Sehr gut

**Steuerliche Aspekte:**
Nach § 7 Abs. 4 EStG können Sie 2-3% AfA (Absetzung für Abnutzung) auf den Gebäudeanteil geltend machen. Dies verbessert die Rendite nach Steuern erheblich.`
  },
  eigenkapitalrendite: {
    titel: 'Eigenkapitalrendite (Leverage-Effekt)',
    erklaerung: `Die Eigenkapitalrendite zeigt, wie sich Ihr eingesetztes Eigenkapital verzinst – unter Einbeziehung der Fremdfinanzierung.

**Leverage-Effekt:**
Wenn die Gesamtrendite über dem Fremdkapitalzins liegt, erhöht Fremdfinanzierung Ihre Eigenkapitalrendite. Liegt sie darunter, verstärkt der Hebel die Verluste.

**Formel:** ((Nettoertrag - Zinsen) ÷ Eigenkapital) × 100

**Richtwerte:**
• Unter 5%: Leverage-Effekt wirkt negativ
• 5-10%: Gute Rendite
• Über 10%: Sehr gute Hebelwirkung

**Risiko-Hinweis:**
Eine hohe Eigenkapitalrendite durch viel Fremdkapital bedeutet auch höheres Risiko. Bei Mietausfall oder Zinserhöhung können die Belastungen schnell die Einnahmen übersteigen.`
  },
  mietmultiplikator: {
    titel: 'Mietmultiplikator (Kaufpreisfaktor)',
    erklaerung: `Der Mietmultiplikator zeigt, nach wie vielen Jahren sich die Immobilie durch Mieteinnahmen "bezahlt" hätte.

**Formel:** Kaufpreis ÷ Jahresnettokaltmiete

**Richtwerte nach Lage:**
• A-Städte (München, Frankfurt): 25-35
• B-Städte (Leipzig, Hannover): 18-25
• C-Städte/ländlich: 12-18

**Umkehrrechnung:**
• Faktor 20 = 5% Bruttorendite
• Faktor 25 = 4% Bruttorendite
• Faktor 33 = 3% Bruttorendite

**Praxis-Tipp:**
Ein hoher Multiplikator kann dennoch sinnvoll sein, wenn die Lage Wertsteigerung verspricht. In schwachen Märkten sind niedrige Faktoren oft mit Vermietungsrisiken verbunden.`
  },
  cashflow: {
    titel: 'Monatlicher Cashflow',
    erklaerung: `Der Cashflow zeigt, was nach Abzug aller Kosten und der Kreditrate monatlich übrig bleibt.

**Formel:** Nettomiete - laufende Kosten - Kreditrate

**Arten:**
• Positiver Cashflow: Die Immobilie trägt sich selbst
• Negativer Cashflow: Sie müssen monatlich zuschießen
• Break-even: Einnahmen = Ausgaben

**Steuerliche Betrachtung:**
Auch bei negativem Cashflow kann eine Immobilie rentabel sein. Die AfA (2-3% vom Gebäudewert) ist steuerlich absetzbar, obwohl sie kein echter Geldabfluss ist.

**Empfehlung:**
Für Kapitalanleger empfiehlt sich ein leicht positiver Cashflow, um Puffer für unerwartete Ausgaben zu haben. Ein Richtwert sind 50-100 €/Monat pro Einheit.`
  }
};

export default function RenditerechnerPage() {
  const [daten, setDaten] = useState<ImmobilienDaten>(initialDaten);
  const [kiAnalyse, setKiAnalyse] = useState<string>('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showKiAnalyse, setShowKiAnalyse] = useState(false);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const [user, setUser] = useState<User | null>(null);
  const [queriesUsed, setQueriesUsed] = useState(0);
  const [queriesLimit, setQueriesLimit] = useState(0);
  const [objektAdresse, setObjektAdresse] = useState<string>('');
  const [savingObjekt, setSavingObjekt] = useState(false);
  const router = useRouter();
  
  // KI-Erklärung State
  const [kiErklaerung, setKiErklaerung] = useState<string>('');
  const [kiErklaerungTitel, setKiErklaerungTitel] = useState<string>('');
  const [showKiErklaerung, setShowKiErklaerung] = useState(false);

  // Tier-Check Helper (Professional or Lawyer)
  const hasAccess = hasTierAccess(userTier, 'professional');
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  // Als Objekt speichern
  const saveAsObjekt = async () => {
    if (!user || !objektAdresse.trim()) {
      alert('Bitte geben Sie eine Objektadresse ein.');
      return;
    }

    setSavingObjekt(true);
    try {
      // Adresse parsen
      const parts = objektAdresse.split(',');
      const strasse = parts[0]?.trim() || objektAdresse;
      const rest = parts[1]?.trim() || '';
      const plzMatch = rest.match(/^(\d{5})\s*(.*)$/);
      const plz = plzMatch?.[1] || '';
      const ort = plzMatch?.[2] || rest;

      const objektData = {
        adresse: strasse,
        plz: plz,
        ort: ort,
        gesamtflaeche: Math.round(daten.kaufpreis / 3000), // Schätzung: 3000€/m²
        gesamteinheiten: 1,
        typ: 'efh' as const,
        heizungstyp: 'gas',
        kaufpreis: daten.kaufpreis,
        kaltmiete: daten.kaltmiete,
        notizen: `Renditerechner-Import: Kaufpreis ${daten.kaufpreis.toLocaleString()}€, Miete ${daten.kaltmiete}€/Mon.`,
        mieter: [],
        createdAt: new Date(),
      };

      await addDoc(collection(db, 'users', user.uid, 'objekte'), objektData);
      alert('✅ Objekt erfolgreich in der Objektverwaltung gespeichert!');
      setObjektAdresse('');
    } catch (error) {
      console.error('Error saving objekt:', error);
      alert('Fehler beim Speichern des Objekts.');
    } finally {
      setSavingObjekt(false);
    }
  };

  // Auth & Tier laden
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      
      setUser(currentUser);
      
      // Tier laden
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      if (userDoc.exists()) {
        const data = userDoc.data();
        const tier = data.tier || data.dashboardType || 'free';
        setUserTier(tier);
        setQueriesUsed(data.queriesUsed || 0);
        setQueriesLimit(data.queriesLimit || 0);
      }
    });

    return () => unsubscribe();
  }, [router]);

  const update = (key: keyof ImmobilienDaten, value: number) => {
    setDaten(prev => ({ ...prev, [key]: value }));
  };
  
  // KI-Erklärung anzeigen
  const showKennzahlErklaerung = (key: string) => {
    const erklaerung = KENNZAHL_ERKLAERUNGEN[key];
    if (erklaerung) {
      setKiErklaerungTitel(erklaerung.titel);
      setKiErklaerung(erklaerung.erklaerung);
      setShowKiErklaerung(true);
    }
  };

  // Berechnungen
  const kaufnebenkosten = daten.kaufpreis * (daten.nebenkosten_prozent / 100);
  const gesamtinvestition = daten.kaufpreis + kaufnebenkosten + daten.renovierung;
  const darlehensbetrag = gesamtinvestition - daten.eigenkapital;
  
  // Jährliche Werte
  const jahresKaltmiete = daten.kaltmiete * 12;
  const monatlicheRate = (darlehensbetrag * (daten.zinssatz + daten.tilgung) / 100) / 12;
  const jährlicheRate = monatlicheRate * 12;
  const jährlicheZinsen = darlehensbetrag * (daten.zinssatz / 100);
  const jährlicheTilgung = darlehensbetrag * (daten.tilgung / 100);
  
  // Kosten
  const jährlicheVerwaltung = daten.verwaltung * 12;
  const jährlicheInstandhaltung = daten.kaufpreis * (daten.instandhaltung_prozent / 100);
  const jährlicherMietausfall = jahresKaltmiete * (daten.mietausfall_prozent / 100);
  const gesamteJährlicheKosten = jährlicheVerwaltung + jährlicheInstandhaltung + jährlicherMietausfall;
  
  // Renditen
  const bruttorendite = (jahresKaltmiete / daten.kaufpreis) * 100;
  const nettoMieteinnahmen = jahresKaltmiete - gesamteJährlicheKosten;
  const nettorendite = (nettoMieteinnahmen / gesamtinvestition) * 100;
  
  // Cashflow vor Steuern
  const cashflowVorSteuern = nettoMieteinnahmen - jährlicheRate;
  const monatlichCashflow = cashflowVorSteuern / 12;
  
  // NEU: AfA-Berechnung nach § 7 Abs. 4 EStG
  // Gebäudewert = Kaufpreis - Grundstücksanteil
  const gebaeudeWert = daten.kaufpreis * (1 - daten.grundstuecksanteil / 100);
  // AfA-Satz: 2% für Baujahr < 1925, 2.5% für 1925-2023, 3% ab 2024 (degressive AfA)
  const afaSatz = daten.baujahr < 1925 ? 2.5 : daten.baujahr >= 2024 ? 3.0 : 2.0;
  const jährlicheAfa = gebaeudeWert * (afaSatz / 100);
  
  // NEU: Steuerliche Vorteile
  // Werbungskosten = Zinsen + Verwaltung + Instandhaltung + AfA
  const werbungskosten = jährlicheZinsen + jährlicheVerwaltung + jährlicheInstandhaltung + jährlicheAfa;
  const zuVersteuern = jahresKaltmiete - werbungskosten;
  const steuerlicheErsparnis = zuVersteuern < 0 ? Math.abs(zuVersteuern) * (daten.steuersatz / 100) : 0;
  const steuerlast = zuVersteuern > 0 ? zuVersteuern * (daten.steuersatz / 100) : 0;
  
  // Cashflow NACH Steuern
  const cashflowNachSteuern = cashflowVorSteuern - steuerlast + steuerlicheErsparnis;
  const monatlichCashflowNachSteuern = cashflowNachSteuern / 12;
  
  // Eigenkapitalrendite (vor Steuern)
  const eigenkapitalRendite = ((nettoMieteinnahmen - jährlicheZinsen) / daten.eigenkapital) * 100;
  
  // NEU: Eigenkapitalrendite NACH Steuern (inkl. AfA-Effekt)
  const eigenkapitalRenditeNachSteuern = ((cashflowNachSteuern + jährlicheTilgung) / daten.eigenkapital) * 100;
  
  // Vermögensaufbau nach 10 Jahren
  const getilgtNach10Jahren = Math.min(darlehensbetrag, jährlicheTilgung * 10);
  const wertNach10Jahren = daten.kaufpreis * Math.pow(1 + daten.wertsteigerung_prozent / 100, 10);
  const vermoegensZuwachs = (wertNach10Jahren - daten.kaufpreis) + getilgtNach10Jahren;
  
  // NEU: Vermögensaufbau mit Steuerersparnis
  const steuerersparnisGesamt10Jahre = steuerlicheErsparnis * 10;
  const vermoegensZuwachsNachSteuern = vermoegensZuwachs + steuerersparnisGesamt10Jahre;
  
  // Mietmultiplikator
  const mietmultiplikator = daten.kaufpreis / jahresKaltmiete;
  
  // NEU: Pro Einheit Kennzahlen
  const cashflowProEinheit = monatlichCashflow / daten.anzahlEinheiten;
  const mieteProQm = daten.kaltmiete / daten.wohnflaeche;
  const kaufpreisProQm = daten.kaufpreis / daten.wohnflaeche;

  // KI-Analyse anfordern
  const requestKiAnalyse = async () => {
    // Check query limit for non-lawyer users
    if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
      setKiAnalyse('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für KI-Analysen.');
      setShowKiAnalyse(true);
      setShowUpgradeModal(true);
      return;
    }
    
    setIsAnalyzing(true);
    try {
      const prompt = `Analysiere diese Immobilieninvestition als Finanzberater:

**Investitionsdaten:**
- Kaufpreis: ${formatEuro(daten.kaufpreis)} €
- Kaufnebenkosten: ${formatEuro(kaufnebenkosten)} € (${daten.nebenkosten_prozent}%)
- Renovierung: ${formatEuro(daten.renovierung)} €
- Gesamtinvestition: ${formatEuro(gesamtinvestition)} €

**Finanzierung:**
- Eigenkapital: ${formatEuro(daten.eigenkapital)} €
- Darlehensbetrag: ${formatEuro(darlehensbetrag)} €
- Zinssatz: ${daten.zinssatz}%, Tilgung: ${daten.tilgung}%
- Monatliche Rate: ${formatEuro(monatlicheRate)} €

**Einnahmen & Kosten:**
- Kaltmiete: ${formatEuro(daten.kaltmiete)} €/Monat
- Jahresmiete: ${formatEuro(jahresKaltmiete)} €
- Jährliche Kosten: ${formatEuro(gesamteJährlicheKosten)} €

**Berechnete Kennzahlen:**
- Bruttorendite: ${bruttorendite.toFixed(2)}%
- Nettorendite: ${nettorendite.toFixed(2)}%
- Eigenkapitalrendite: ${eigenkapitalRendite.toFixed(2)}%
- Monatlicher Cashflow: ${formatEuro(monatlichCashflow)} €
- Mietmultiplikator: ${mietmultiplikator.toFixed(1)} Jahre
- Vermögensaufbau 10 Jahre: ${formatEuro(vermoegensZuwachs)} €

Bitte analysiere:
1. Ist das Investment aus Rendite-Sicht attraktiv?
2. Welche Risiken bestehen?
3. Steuerliche Optimierungsmöglichkeiten (AfA, Werbungskosten)?
4. Vergleich mit typischen Marktrenditen?
5. Empfehlung: Kaufen oder nicht?

Antworte strukturiert mit konkreten Handlungsempfehlungen.`;

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app'}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: prompt,
          target_jurisdiction: 'DE'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setKiAnalyse(data.answer || data.response || 'Keine Analyse verfügbar.');
        setShowKiAnalyse(true);
        
        // Increment query count for non-lawyer users
        if (user && userTier !== 'lawyer') {
          await updateDoc(doc(db, 'users', user.uid), {
            queriesUsed: increment(1)
          });
          setQueriesUsed(prev => prev + 1);
        }
      } else {
        setKiAnalyse('KI-Analyse konnte nicht geladen werden. Bitte versuchen Sie es später erneut.');
        setShowKiAnalyse(true);
      }
    } catch (error) {
      console.error('KI-Analyse Fehler:', error);
      setKiAnalyse('Verbindungsfehler zur KI. Bitte prüfen Sie Ihre Internetverbindung.');
      setShowKiAnalyse(true);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const formatEuro = (value: number) => {
    return value.toLocaleString('de-DE', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* KI-Erklärung Modal */}
      {showKiErklaerung && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-[60] flex items-center justify-center p-4">
          <div className="bg-gray-900 border border-gray-700 rounded-2xl max-w-2xl w-full max-h-[80vh] overflow-hidden shadow-2xl">
            <div className="flex items-center justify-between p-4 border-b border-gray-700 bg-gradient-to-r from-blue-500/10 to-purple-500/10">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🤖</span>
                <div>
                  <h3 className="text-lg font-bold text-white">KI-Erklärung</h3>
                  <p className="text-sm text-blue-400">{kiErklaerungTitel}</p>
                </div>
              </div>
              <button
                onClick={() => setShowKiErklaerung(false)}
                className="text-gray-400 hover:text-white p-2 hover:bg-gray-800 rounded-lg transition-colors"
              >
                ✕
              </button>
            </div>
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="prose prose-invert max-w-none">
                <div className="whitespace-pre-wrap text-gray-300 leading-relaxed">{kiErklaerung}</div>
              </div>
            </div>
            <div className="p-4 border-t border-gray-700 bg-gray-800/50 flex justify-between items-center">
              <p className="text-xs text-gray-500">Powered by Domulex KI • Keine Finanzberatung</p>
              <button
                onClick={() => setShowKiErklaerung(false)}
                className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition-colors"
              >
                Schließen
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-xl border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-16">
            <Link href="/dashboard" className="text-gray-400 hover:text-white">
              ← Dashboard
            </Link>
            <h1 className="text-lg font-semibold text-white">KI-Renditerechner</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-24">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Immobilien-Renditerechner</h1>
          <p className="text-gray-400 mt-2">Berechnen Sie die Rentabilität Ihrer Immobilieninvestition</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Eingabe */}
          <div className="lg:col-span-2 space-y-6">
            {/* Kaufdaten */}
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">🏠 Objektdaten</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Kaufpreis (€)</label>
                  <input
                    type="number"
                    value={daten.kaufpreis}
                    onChange={(e) => update('kaufpreis', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Wohnfläche (m²)</label>
                  <input
                    type="number"
                    value={daten.wohnflaeche}
                    onChange={(e) => update('wohnflaeche', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Einheiten</label>
                  <input
                    type="number"
                    min="1"
                    value={daten.anzahlEinheiten}
                    onChange={(e) => update('anzahlEinheiten', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Baujahr</label>
                  <input
                    type="number"
                    value={daten.baujahr}
                    onChange={(e) => update('baujahr', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Kaufnebenkosten (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={daten.nebenkosten_prozent}
                    onChange={(e) => update('nebenkosten_prozent', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Renovierung (€)</label>
                  <input
                    type="number"
                    value={daten.renovierung}
                    onChange={(e) => update('renovierung', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Grundstücksanteil (%)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    max="50"
                    value={daten.grundstuecksanteil}
                    onChange={(e) => update('grundstuecksanteil', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                  <p className="text-xs text-gray-500 mt-0.5">Für AfA-Berechnung</p>
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Grenzsteuersatz (%)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    max="45"
                    value={daten.steuersatz}
                    onChange={(e) => update('steuersatz', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
              </div>
              <div className="mt-3 p-3 bg-gray-900/50 rounded-lg text-sm">
                <div className="grid grid-cols-2 gap-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Kaufnebenkosten:</span>
                    <span className="font-medium text-white">{formatEuro(kaufnebenkosten)} €</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">€/m²:</span>
                    <span className="font-medium text-white">{formatEuro(kaufpreisProQm)} €</span>
                  </div>
                </div>
                <div className="flex justify-between font-bold text-white mt-1">
                  <span>Gesamtinvestition:</span>
                  <span>{formatEuro(gesamtinvestition)} €</span>
                </div>
              </div>
            </div>

            {/* Finanzierung */}
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">💳 Finanzierung</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Eigenkapital (€)</label>
                  <input
                    type="number"
                    value={daten.eigenkapital}
                    onChange={(e) => update('eigenkapital', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Zinssatz (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={daten.zinssatz}
                    onChange={(e) => update('zinssatz', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Tilgung (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={daten.tilgung}
                    onChange={(e) => update('tilgung', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Laufzeit (Jahre)</label>
                  <input
                    type="number"
                    value={daten.laufzeit}
                    onChange={(e) => update('laufzeit', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
              </div>
              <div className="mt-3 p-3 bg-gray-900/50 rounded-lg text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Darlehensbetrag:</span>
                  <span className="font-medium text-white">{formatEuro(darlehensbetrag)} €</span>
                </div>
                <div className="flex justify-between font-bold text-white">
                  <span>Monatliche Rate:</span>
                  <span>{formatEuro(monatlicheRate)} €</span>
                </div>
              </div>
            </div>

            {/* Einnahmen/Kosten */}
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">💰 Mieteinnahmen & Kosten</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Kaltmiete/Monat (€)</label>
                  <input
                    type="number"
                    value={daten.kaltmiete}
                    onChange={(e) => update('kaltmiete', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Verwaltung/Monat (€)</label>
                  <input
                    type="number"
                    value={daten.verwaltung}
                    onChange={(e) => update('verwaltung', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Instandhaltung (%/Jahr)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={daten.instandhaltung_prozent}
                    onChange={(e) => update('instandhaltung_prozent', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Mietausfall (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={daten.mietausfall_prozent}
                    onChange={(e) => update('mietausfall_prozent', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Wertsteigerung (%/Jahr)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={daten.wertsteigerung_prozent}
                    onChange={(e) => update('wertsteigerung_prozent', Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Ergebnisse */}
          <div className="space-y-6">
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6 sticky top-4">
              <h2 className="text-lg font-semibold text-white mb-4">📊 Renditekennzahlen</h2>
              
              <div className="space-y-4">
                {/* Hauptrenditen */}
                <div className="grid grid-cols-2 gap-4">
                  <div className={`p-4 rounded-lg text-center ${bruttorendite >= 5 ? 'bg-green-900/30 border border-green-700' : 'bg-yellow-900/30 border border-yellow-700'}`}>
                    <div className="flex items-center justify-center gap-2">
                      <p className="text-xs text-gray-400">Bruttorendite</p>
                      <button
                        onClick={() => showKennzahlErklaerung('bruttorendite')}
                        className="text-blue-400 hover:text-blue-300 text-xs"
                        title="KI-Erklärung"
                      >
                        ℹ️
                      </button>
                    </div>
                    <p className={`text-2xl font-bold ${bruttorendite >= 5 ? 'text-green-400' : 'text-yellow-400'}`}>
                      {bruttorendite.toFixed(2)}%
                    </p>
                  </div>
                  <div className={`p-4 rounded-lg text-center ${nettorendite >= 4 ? 'bg-green-900/30 border border-green-700' : 'bg-yellow-900/30 border border-yellow-700'}`}>
                    <div className="flex items-center justify-center gap-2">
                      <p className="text-xs text-gray-400">Nettorendite</p>
                      <button
                        onClick={() => showKennzahlErklaerung('nettorendite')}
                        className="text-blue-400 hover:text-blue-300 text-xs"
                        title="KI-Erklärung"
                      >
                        ℹ️
                      </button>
                    </div>
                    <p className={`text-2xl font-bold ${nettorendite >= 4 ? 'text-green-400' : 'text-yellow-400'}`}>
                      {nettorendite.toFixed(2)}%
                    </p>
                  </div>
                </div>

                <div className={`p-4 rounded-lg text-center ${eigenkapitalRendite >= 8 ? 'bg-green-900/30 border border-green-700' : eigenkapitalRendite >= 5 ? 'bg-yellow-900/30 border border-yellow-700' : 'bg-red-900/30 border border-red-700'}`}>
                  <div className="flex items-center justify-center gap-2">
                    <p className="text-xs text-gray-400">Eigenkapitalrendite</p>
                    <button
                      onClick={() => showKennzahlErklaerung('eigenkapitalrendite')}
                      className="text-blue-400 hover:text-blue-300 text-xs"
                      title="KI-Erklärung"
                    >
                      ℹ️
                    </button>
                  </div>
                  <p className={`text-2xl font-bold ${eigenkapitalRendite >= 8 ? 'text-green-400' : eigenkapitalRendite >= 5 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {eigenkapitalRendite.toFixed(2)}%
                  </p>
                </div>

                {/* Cashflow */}
                <div className={`p-4 rounded-lg ${monatlichCashflow >= 0 ? 'bg-green-900/30 border border-green-700' : 'bg-red-900/30 border border-red-700'}`}>
                  <div className="flex items-center gap-2">
                    <p className="text-sm text-gray-400">Monatlicher Cashflow (vor Steuern)</p>
                    <button
                      onClick={() => showKennzahlErklaerung('cashflow')}
                      className="text-blue-400 hover:text-blue-300 text-xs"
                      title="KI-Erklärung"
                    >
                      ℹ️
                    </button>
                  </div>
                  <p className={`text-2xl font-bold ${monatlichCashflow >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {monatlichCashflow >= 0 ? '+' : ''}{formatEuro(monatlichCashflow)} €
                  </p>
                  {daten.anzahlEinheiten > 1 && (
                    <p className="text-xs text-gray-500">({formatEuro(cashflowProEinheit)} € pro Einheit)</p>
                  )}
                </div>

                {/* NEU: Steuer-Sektion */}
                <div className="p-4 rounded-lg bg-indigo-900/20 border border-indigo-700/50">
                  <p className="text-sm font-medium text-indigo-300 mb-3">📋 Steuerliche Betrachtung</p>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-400">AfA ({afaSatz}% von {formatEuro(gebaeudeWert)}€):</span>
                      <span className="text-indigo-300 font-medium">{formatEuro(jährlicheAfa)} €/Jahr</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Werbungskosten gesamt:</span>
                      <span className="text-indigo-300">{formatEuro(werbungskosten)} €</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Zu versteuern:</span>
                      <span className={zuVersteuern < 0 ? 'text-green-400' : 'text-amber-400'}>{formatEuro(zuVersteuern)} €</span>
                    </div>
                    {steuerlicheErsparnis > 0 && (
                      <div className="flex justify-between font-medium pt-1 border-t border-indigo-700/30">
                        <span className="text-green-400">✓ Steuerersparnis:</span>
                        <span className="text-green-400">+{formatEuro(steuerlicheErsparnis)} €/Jahr</span>
                      </div>
                    )}
                    {steuerlast > 0 && (
                      <div className="flex justify-between font-medium pt-1 border-t border-indigo-700/30">
                        <span className="text-amber-400">Steuerlast:</span>
                        <span className="text-amber-400">-{formatEuro(steuerlast)} €/Jahr</span>
                      </div>
                    )}
                  </div>
                  <div className="mt-3 pt-3 border-t border-indigo-700/30">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-300 font-medium">Cashflow nach Steuern:</span>
                      <span className={`text-xl font-bold ${monatlichCashflowNachSteuern >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {monatlichCashflowNachSteuern >= 0 ? '+' : ''}{formatEuro(monatlichCashflowNachSteuern)} €/Mon.
                      </span>
                    </div>
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>EK-Rendite nach Steuern:</span>
                      <span className={eigenkapitalRenditeNachSteuern >= 8 ? 'text-green-400' : 'text-gray-400'}>
                        {eigenkapitalRenditeNachSteuern.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Mietmultiplikator */}
                <div className="pb-4 border-b border-gray-700">
                  <div className="flex items-center gap-2">
                    <p className="text-sm text-gray-400">Mietmultiplikator</p>
                    <button
                      onClick={() => showKennzahlErklaerung('mietmultiplikator')}
                      className="text-blue-400 hover:text-blue-300 text-xs"
                      title="KI-Erklärung"
                    >
                      ℹ️
                    </button>
                  </div>
                  <p className="text-xl font-bold text-white">{mietmultiplikator.toFixed(1)} Jahre</p>
                  <p className="text-xs text-gray-500">
                    {mietmultiplikator <= 20 ? '✅ Gut' : mietmultiplikator <= 25 ? '⚠️ Durchschnittlich' : '❌ Teuer'}
                  </p>
                </div>

                {/* 10-Jahres-Prognose */}
                <div className="bg-gradient-to-br from-[#1e3a5f] to-[#2d4a6f] p-4 rounded-lg text-white">
                  <p className="text-sm opacity-80">Vermögensaufbau nach 10 Jahren</p>
                  <p className="text-2xl font-bold">+{formatEuro(vermoegensZuwachs)} €</p>
                  <div className="mt-2 text-xs opacity-70">
                    <p>Tilgung: {formatEuro(getilgtNach10Jahren)} €</p>
                    <p>Wertsteigerung: {formatEuro(wertNach10Jahren - daten.kaufpreis)} €</p>
                  </div>
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <button
                  onClick={() => requireTier(() => requestKiAnalyse())}
                  disabled={isAnalyzing}
                  className="block w-full text-center py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all disabled:opacity-50 font-medium"
                >
                  {isAnalyzing ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                      KI analysiert...
                    </span>
                  ) : (
                    '🤖 KI-Investment-Analyse starten'
                  )}
                </button>
                <Link
                  href="/app?prompt=Wie%20optimiere%20ich%20die%20Steuerlast%20meiner%20Immobilien%3F%20AfA%2C%20Werbungskosten%2C%20Spekulationsfrist"
                  className="block w-full text-center py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  💰 Steuer-Optimierung berechnen
                </Link>

                {/* In Objektverwaltung speichern */}
                {user && (
                  <div className="mt-4 pt-4 border-t border-gray-700">
                    <p className="text-xs text-gray-400 mb-2">📁 Objekt speichern</p>
                    <input
                      type="text"
                      value={objektAdresse}
                      onChange={(e) => setObjektAdresse(e.target.value)}
                      placeholder="Adresse eingeben (z.B. Musterstr. 1, Berlin)"
                      className="w-full p-2 mb-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 text-sm"
                    />
                    <button
                      onClick={() => requireTier(() => saveAsObjekt())}
                      disabled={savingObjekt || !objektAdresse.trim()}
                      className="w-full py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
                    >
                      {savingObjekt ? (
                        <span className="flex items-center justify-center gap-2">
                          <span className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                          Wird gespeichert...
                        </span>
                      ) : (
                        '💾 In Objektverwaltung speichern'
                      )}
                    </button>
                  </div>
                )}
              </div>

              {/* KI-Analyse Ergebnis */}
              {showKiAnalyse && kiAnalyse && (
                <div className="mt-4 p-4 bg-purple-900/30 rounded-lg border border-purple-700">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-purple-300 flex items-center gap-2">
                      🤖 KI-Investment-Analyse
                    </h3>
                    <button
                      onClick={() => setShowKiAnalyse(false)}
                      className="text-purple-400 hover:text-purple-300 text-sm"
                    >
                      ✕ Schließen
                    </button>
                  </div>
                  <div className="prose prose-sm prose-invert max-w-none text-gray-300 whitespace-pre-wrap text-sm">
                    {kiAnalyse}
                  </div>
                </div>
              )}

              {/* Bewertung - INNERHALB der Karte */}
              <div className="mt-6 pt-4 border-t border-gray-700">
                <p className="font-medium text-amber-400 mb-2 text-sm">📈 Richtwerte</p>
                <ul className="space-y-1 text-xs text-gray-400">
                  <li>• Bruttorendite: ab 5% gut</li>
                  <li>• Nettorendite: ab 4% gut</li>
                  <li>• Eigenkapitalrendite: ab 8% sehr gut</li>
                  <li>• Mietmultiplikator: unter 20 = gute Lage</li>
                  <li>• Positiver Cashflow: ab Tag 1 empfohlen</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        feature="Renditerechner"
        requiredTier="professional"
      />
    </div>
  );
}
