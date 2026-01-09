'use client';

import { useState, useEffect, Suspense } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc, collection, getDocs, addDoc, updateDoc, increment } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import UpgradeModal from '@/components/UpgradeModal';
import { hasTierAccess } from '@/lib/tierUtils';

// CO2-Stufenmodell nach CO2KostAufG (§ 5, § 6)
const CO2_STUFEN = [
  { stufe: 1, maxCO2: 12, mieterAnteil: 100, vermieterAnteil: 0 },
  { stufe: 2, maxCO2: 17, mieterAnteil: 90, vermieterAnteil: 10 },
  { stufe: 3, maxCO2: 22, mieterAnteil: 80, vermieterAnteil: 20 },
  { stufe: 4, maxCO2: 27, mieterAnteil: 70, vermieterAnteil: 30 },
  { stufe: 5, maxCO2: 32, mieterAnteil: 60, vermieterAnteil: 40 },
  { stufe: 6, maxCO2: 37, mieterAnteil: 50, vermieterAnteil: 50 },
  { stufe: 7, maxCO2: 42, mieterAnteil: 40, vermieterAnteil: 60 },
  { stufe: 8, maxCO2: 47, mieterAnteil: 30, vermieterAnteil: 70 },
  { stufe: 9, maxCO2: 52, mieterAnteil: 20, vermieterAnteil: 80 },
  { stufe: 10, maxCO2: Infinity, mieterAnteil: 5, vermieterAnteil: 95 },
];

// Heizungstypen für CO2-Berechnung
const HEIZUNGSTYPEN = [
  { id: 'gas', label: 'Erdgas', co2FaktorKgProKwh: 0.201 },
  { id: 'oel', label: 'Heizöl', co2FaktorKgProKwh: 0.266 },
  { id: 'fernwaerme', label: 'Fernwärme', co2FaktorKgProKwh: 0.130 },
  { id: 'waermepumpe', label: 'Wärmepumpe', co2FaktorKgProKwh: 0.0 },
  { id: 'pellets', label: 'Holzpellets', co2FaktorKgProKwh: 0.023 },
];

// Typen
interface Mieter {
  id: string;
  name: string;
  einheit: string;
  flaeche: number;
  personenanzahl: number;
  einzugsdatum: string;
  auszugsdatum?: string;
}

interface Kostenposition {
  id: string;
  bezeichnung: string;
  kategorie: string;
  gesamtbetrag: number;
  umlageschluessel: 'flaeche' | 'personenzahl' | 'einheiten' | 'verbrauch' | 'miteigentumsanteil';
  umlagefaehig: boolean;
  rechtsgrundlage: string;
  hinweis?: string;
}

interface Vorauszahlung {
  mieterId: string;
  betrag: number;
  monate: number;
}

interface AbrechnungErgebnis {
  mieterId: string;
  mieterName: string;
  einheit: string;
  gesamtkosten: number;
  anteil: number;
  vorauszahlungen: number;
  nachzahlung: number;
  co2Kosten?: {
    gesamt: number;
    mieterAnteil: number;
    vermieterAnteil: number;
    stufe: number;
    co2ProQm: number;
  };
  positionen: {
    bezeichnung: string;
    gesamtbetrag: number;
    anteil: number;
    schluessel: string;
  }[];
}

// Energiedaten Interface für CO2-Berechnung
interface Energiedaten {
  heizungstyp: string;
  jahresverbrauchKwh: number;
  co2KostenGesamt: number;
  brennstoffkosten: number;
  energieausweis?: string;
}

// Standard-Kostenarten nach § 2 BetrKV
const STANDARD_KOSTENARTEN: Omit<Kostenposition, 'id' | 'gesamtbetrag'>[] = [
  { bezeichnung: 'Grundsteuer', kategorie: 'Öffentliche Lasten', umlageschluessel: 'miteigentumsanteil', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 1 BetrKV' },
  { bezeichnung: 'Wasserversorgung', kategorie: 'Wasser/Abwasser', umlageschluessel: 'verbrauch', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 2 BetrKV' },
  { bezeichnung: 'Entwässerung', kategorie: 'Wasser/Abwasser', umlageschluessel: 'verbrauch', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 3 BetrKV' },
  { bezeichnung: 'Heizkosten', kategorie: 'Heizung/Warmwasser', umlageschluessel: 'verbrauch', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 4 BetrKV, HeizKV', hinweis: '50-70% nach Verbrauch' },
  { bezeichnung: 'Warmwasser', kategorie: 'Heizung/Warmwasser', umlageschluessel: 'verbrauch', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 5 BetrKV, HeizKV' },
  { bezeichnung: 'Verbundene Heizung/Warmwasser', kategorie: 'Heizung/Warmwasser', umlageschluessel: 'verbrauch', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 6 BetrKV' },
  { bezeichnung: 'Aufzug', kategorie: 'Gebäudebetrieb', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 7 BetrKV' },
  { bezeichnung: 'Straßenreinigung', kategorie: 'Reinigung', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 8 BetrKV' },
  { bezeichnung: 'Müllabfuhr', kategorie: 'Reinigung', umlageschluessel: 'personenzahl', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 8 BetrKV' },
  { bezeichnung: 'Gebäudereinigung', kategorie: 'Reinigung', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 9 BetrKV' },
  { bezeichnung: 'Ungezieferbekämpfung', kategorie: 'Reinigung', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 9 BetrKV' },
  { bezeichnung: 'Gartenpflege', kategorie: 'Außenanlagen', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 10 BetrKV' },
  { bezeichnung: 'Beleuchtung Allgemeinflächen', kategorie: 'Gebäudebetrieb', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 11 BetrKV' },
  { bezeichnung: 'Schornsteinreinigung', kategorie: 'Gebäudebetrieb', umlageschluessel: 'einheiten', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 12 BetrKV' },
  { bezeichnung: 'Sach- und Haftpflichtversicherung', kategorie: 'Versicherungen', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 13 BetrKV' },
  { bezeichnung: 'Hauswart', kategorie: 'Gebäudebetrieb', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 14 BetrKV', hinweis: 'Ohne Reparaturarbeiten' },
  { bezeichnung: 'Gemeinschaftsantenne/Kabelanschluss', kategorie: 'Sonstiges', umlageschluessel: 'einheiten', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 15 BetrKV' },
  { bezeichnung: 'Waschraum', kategorie: 'Sonstiges', umlageschluessel: 'personenzahl', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 16 BetrKV' },
  { bezeichnung: 'Sonstige Betriebskosten', kategorie: 'Sonstiges', umlageschluessel: 'flaeche', umlagefaehig: true, rechtsgrundlage: '§ 2 Nr. 17 BetrKV', hinweis: 'Nur wenn im Mietvertrag vereinbart' },
];

// ===== DEMO-DATEN FÜR FREE-NUTZER =====
const DEMO_ERGEBNISSE: AbrechnungErgebnis[] = [
  {
    mieterId: 'demo-1',
    mieterName: 'Familie Müller',
    einheit: 'Wohnung 1, EG links',
    gesamtkosten: 2847.50,
    anteil: 28.5,
    vorauszahlungen: 2400.00,
    nachzahlung: 447.50,
    co2Kosten: {
      gesamt: 312.40,
      mieterAnteil: 249.92,
      vermieterAnteil: 62.48,
      stufe: 4,
      co2ProQm: 25.3,
    },
    positionen: [
      { bezeichnung: 'Grundsteuer', gesamtbetrag: 1850.00, anteil: 527.25, schluessel: 'Fläche (28,5%)' },
      { bezeichnung: 'Wasserversorgung', gesamtbetrag: 1240.00, anteil: 353.40, schluessel: 'Fläche (28,5%)' },
      { bezeichnung: 'Heizkosten', gesamtbetrag: 4200.00, anteil: 1197.00, schluessel: 'Fläche (28,5%)' },
      { bezeichnung: 'Müllabfuhr', gesamtbetrag: 890.00, anteil: 267.00, schluessel: 'Personen (3/10)' },
      { bezeichnung: 'Gebäudereinigung', gesamtbetrag: 720.00, anteil: 205.20, schluessel: 'Fläche (28,5%)' },
      { bezeichnung: 'Versicherungen', gesamtbetrag: 1045.00, anteil: 297.65, schluessel: 'Fläche (28,5%)' },
    ],
  },
  {
    mieterId: 'demo-2',
    mieterName: 'Hr. Schmidt',
    einheit: 'Wohnung 2, EG rechts',
    gesamtkosten: 1923.80,
    anteil: 19.2,
    vorauszahlungen: 2100.00,
    nachzahlung: -176.20,
    co2Kosten: {
      gesamt: 210.60,
      mieterAnteil: 168.48,
      vermieterAnteil: 42.12,
      stufe: 4,
      co2ProQm: 25.3,
    },
    positionen: [
      { bezeichnung: 'Grundsteuer', gesamtbetrag: 1850.00, anteil: 355.20, schluessel: 'Fläche (19,2%)' },
      { bezeichnung: 'Wasserversorgung', gesamtbetrag: 1240.00, anteil: 238.08, schluessel: 'Fläche (19,2%)' },
      { bezeichnung: 'Heizkosten', gesamtbetrag: 4200.00, anteil: 806.40, schluessel: 'Fläche (19,2%)' },
      { bezeichnung: 'Müllabfuhr', gesamtbetrag: 890.00, anteil: 89.00, schluessel: 'Personen (1/10)' },
      { bezeichnung: 'Gebäudereinigung', gesamtbetrag: 720.00, anteil: 138.24, schluessel: 'Fläche (19,2%)' },
      { bezeichnung: 'Versicherungen', gesamtbetrag: 1045.00, anteil: 200.64, schluessel: 'Fläche (19,2%)' },
    ],
  },
  {
    mieterId: 'demo-3',
    mieterName: 'Fr. Weber',
    einheit: 'Wohnung 3, 1. OG links',
    gesamtkosten: 2156.40,
    anteil: 21.5,
    vorauszahlungen: 2000.00,
    nachzahlung: 156.40,
    co2Kosten: {
      gesamt: 236.20,
      mieterAnteil: 188.96,
      vermieterAnteil: 47.24,
      stufe: 4,
      co2ProQm: 25.3,
    },
    positionen: [
      { bezeichnung: 'Grundsteuer', gesamtbetrag: 1850.00, anteil: 397.75, schluessel: 'Fläche (21,5%)' },
      { bezeichnung: 'Wasserversorgung', gesamtbetrag: 1240.00, anteil: 266.60, schluessel: 'Fläche (21,5%)' },
      { bezeichnung: 'Heizkosten', gesamtbetrag: 4200.00, anteil: 903.00, schluessel: 'Fläche (21,5%)' },
      { bezeichnung: 'Müllabfuhr', gesamtbetrag: 890.00, anteil: 178.00, schluessel: 'Personen (2/10)' },
      { bezeichnung: 'Gebäudereinigung', gesamtbetrag: 720.00, anteil: 154.80, schluessel: 'Fläche (21,5%)' },
      { bezeichnung: 'Versicherungen', gesamtbetrag: 1045.00, anteil: 224.67, schluessel: 'Fläche (21,5%)' },
    ],
  },
];

const DEMO_KI_ANALYSE = `## 🤖 KI-Analyse der Nebenkostenabrechnung

### Zusammenfassung
Die Nebenkostenabrechnung für das Abrechnungsjahr 2024 ist formal korrekt erstellt. Die Gesamtbetriebskosten von **9.945,00 €** wurden entsprechend der Wohnfläche und Personenanzahl auf die 3 Mietparteien umgelegt.

### CO₂-Kostenaufteilung (CO2KostAufG)
Das Gebäude liegt in **Stufe 4** mit 25,3 kg CO₂/m²/Jahr. Die Aufteilung:
- Mieteranteil: **70%**
- Vermieteranteil: **30%**

💡 **Tipp:** Durch energetische Sanierung (z.B. Dämmung, neue Fenster) können Sie in eine niedrigere Stufe wechseln und die Vermieterkosten senken.

### Abrechnungsergebnisse
| Mieter | Nachzahlung/Guthaben |
|--------|---------------------|
| Familie Müller | +447,50 € (Nachzahlung) |
| Hr. Schmidt | -176,20 € (Guthaben) |
| Fr. Weber | +156,40 € (Nachzahlung) |

### Rechtliche Hinweise
- **Abrechnungsfrist (§ 556 Abs. 3 BGB):** Die Abrechnung muss dem Mieter bis spätestens 12 Monate nach Ende des Abrechnungszeitraums zugehen.
- **Einwendungsfrist:** Der Mieter hat 12 Monate Zeit, Einwendungen gegen die Abrechnung zu erheben.
- **Belegeinsicht:** Auf Verlangen müssen Sie dem Mieter Einsicht in die Belege gewähren.

### Empfehlungen
1. ✅ Abrechnung zeitnah an alle Mieter versenden
2. ✅ Belege für eventuelle Rückfragen bereithalten
3. ✅ Vorauszahlungen für nächstes Jahr ggf. anpassen`;

// Gespeichertes Objekt Interface
interface GespeichertesObjekt {
  id: string;
  adresse: string;
  plz: string;
  ort: string;
  gesamtflaeche: number;
  gesamteinheiten: number;
  heizungstyp: string;
  mieter: Array<{
    id: string;
    name: string;
    einheit: string;
    flaeche: number;
    personenanzahl: number;
    einzugsdatum: string;
    auszugsdatum?: string;
    vorauszahlung: number;
  }>;
}

// Wrapper für Suspense
export default function NebenkostenabrechnungPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    }>
      <NebenkostenabrechnungContent />
    </Suspense>
  );
}

function NebenkostenabrechnungContent() {
  const searchParams = useSearchParams();
  const objektIdFromUrl = searchParams.get('objekt');

  // State
  const [user, setUser] = useState<any>(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [kiAnalyse, setKiAnalyse] = useState<string>('');
  const [showKiAnalyse, setShowKiAnalyse] = useState(false);
  const [gespeicherteObjekte, setGespeicherteObjekte] = useState<GespeichertesObjekt[]>([]);
  const [selectedObjektId, setSelectedObjektId] = useState<string | null>(objektIdFromUrl);
  const [loadingObjekte, setLoadingObjekte] = useState(true);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const [queriesUsed, setQueriesUsed] = useState(0);
  const [queriesLimit, setQueriesLimit] = useState(0);
  
  // Tier-Check Helper (Professional or Lawyer)
  const hasAccess = hasTierAccess(userTier, 'professional');
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };
  
  // KI-Erklärung State
  const [kiErklaerung, setKiErklaerung] = useState<string>('');
  const [kiErklaerungTitel, setKiErklaerungTitel] = useState<string>('');
  const [showKiErklaerung, setShowKiErklaerung] = useState(false);
  const [loadingKiErklaerung, setLoadingKiErklaerung] = useState(false);
  
  // NEU: Verwalter-Features
  const [showObjektUebersicht, setShowObjektUebersicht] = useState(false);
  
  // Fristenberechnung nach § 556 Abs. 3 BGB (12 Monate nach Ende Abrechnungszeitraum)
  const berechneFrist = (abrechnungsende: string): { frist: Date; tageVerbleibend: number; status: 'ok' | 'warnung' | 'kritisch' | 'ueberschritten' } => {
    if (!abrechnungsende) return { frist: new Date(), tageVerbleibend: 365, status: 'ok' };
    const ende = new Date(abrechnungsende);
    const frist = new Date(ende);
    frist.setFullYear(frist.getFullYear() + 1);
    const heute = new Date();
    const diffMs = frist.getTime() - heute.getTime();
    const tageVerbleibend = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
    
    let status: 'ok' | 'warnung' | 'kritisch' | 'ueberschritten' = 'ok';
    if (tageVerbleibend < 0) status = 'ueberschritten';
    else if (tageVerbleibend < 30) status = 'kritisch';
    else if (tageVerbleibend < 90) status = 'warnung';
    
    return { frist, tageVerbleibend, status };
  };
  
  // Objektdaten
  const [objektdaten, setObjektdaten] = useState({
    adresse: '',
    gesamtflaeche: 0,
    gesamteinheiten: 0,
    abrechnungszeitraumStart: '',
    abrechnungszeitraumEnde: '',
    abrechnungsjahr: new Date().getFullYear() - 1,
  });

  // Mieter
  const [mieter, setMieter] = useState<Mieter[]>([]);
  
  // Kostenpositionen
  const [kostenpositionen, setKostenpositionen] = useState<Kostenposition[]>([]);
  
  // Vorauszahlungen
  const [vorauszahlungen, setVorauszahlungen] = useState<Vorauszahlung[]>([]);
  
  // Ergebnisse
  const [ergebnisse, setErgebnisse] = useState<AbrechnungErgebnis[]>([]);

  // Energiedaten für CO2-Kostenaufteilung
  const [energiedaten, setEnergiedaten] = useState<Energiedaten>({
    heizungstyp: 'gas',
    jahresverbrauchKwh: 0,
    co2KostenGesamt: 0,
    brennstoffkosten: 0,
    energieausweis: '',
  });

  // Auth & Objekte laden
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (currentUser) {
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
        
        await loadGespeicherteObjekte(currentUser.uid);
      } else {
        setLoadingObjekte(false);
      }
    });
    return () => unsubscribe();
  }, []);

  // Objekte aus Firestore laden
  const loadGespeicherteObjekte = async (userId: string) => {
    try {
      const snapshot = await getDocs(collection(db, 'users', userId, 'objekte'));
      const objekte = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as GespeichertesObjekt[];
      setGespeicherteObjekte(objekte);

      // Wenn Objekt-ID von URL, automatisch laden
      if (objektIdFromUrl) {
        const objekt = objekte.find(o => o.id === objektIdFromUrl);
        if (objekt) {
          loadObjektDaten(objekt);
        }
      }
    } catch (error) {
      console.error('Error loading objekte:', error);
    } finally {
      setLoadingObjekte(false);
    }
  };

  // Objektdaten in Formular laden
  const loadObjektDaten = (objekt: GespeichertesObjekt) => {
    setSelectedObjektId(objekt.id);
    setObjektdaten({
      adresse: `${objekt.adresse}, ${objekt.plz} ${objekt.ort}`,
      gesamtflaeche: objekt.gesamtflaeche,
      gesamteinheiten: objekt.gesamteinheiten,
      abrechnungszeitraumStart: `${new Date().getFullYear() - 1}-01-01`,
      abrechnungszeitraumEnde: `${new Date().getFullYear() - 1}-12-31`,
      abrechnungsjahr: new Date().getFullYear() - 1,
    });
    setEnergiedaten(prev => ({ ...prev, heizungstyp: objekt.heizungstyp }));
    
    // Mieter übernehmen
    const mieterDaten: Mieter[] = objekt.mieter.map(m => ({
      id: m.id,
      name: m.name,
      einheit: m.einheit,
      flaeche: m.flaeche,
      personenanzahl: m.personenanzahl,
      einzugsdatum: m.einzugsdatum || `${new Date().getFullYear() - 1}-01-01`,
      auszugsdatum: m.auszugsdatum,
    }));
    setMieter(mieterDaten);

    // Vorauszahlungen übernehmen
    const vorauszahlungenDaten: Vorauszahlung[] = objekt.mieter.map(m => ({
      mieterId: m.id,
      betrag: m.vorauszahlung || 0,
      monate: 12,
    }));
    setVorauszahlungen(vorauszahlungenDaten);
  };

  // CO2-Stufe berechnen
  const berechneCO2Stufe = (): { stufe: number; co2ProQm: number; mieterAnteil: number; vermieterAnteil: number } => {
    if (!energiedaten.jahresverbrauchKwh || !objektdaten.gesamtflaeche) {
      return { stufe: 1, co2ProQm: 0, mieterAnteil: 100, vermieterAnteil: 0 };
    }

    const heizung = HEIZUNGSTYPEN.find(h => h.id === energiedaten.heizungstyp);
    const co2FaktorKg = heizung?.co2FaktorKgProKwh || 0.201;
    
    // CO2-Ausstoß in kg/m²/Jahr berechnen
    const co2Gesamt = energiedaten.jahresverbrauchKwh * co2FaktorKg;
    const co2ProQm = co2Gesamt / objektdaten.gesamtflaeche;

    // Stufe ermitteln
    const stufe = CO2_STUFEN.find(s => co2ProQm < s.maxCO2) || CO2_STUFEN[9];
    
    return {
      stufe: stufe.stufe,
      co2ProQm: Math.round(co2ProQm * 10) / 10,
      mieterAnteil: stufe.mieterAnteil,
      vermieterAnteil: stufe.vermieterAnteil,
    };
  };

  // Initialisierung Standard-Kostenarten
  useEffect(() => {
    if (kostenpositionen.length === 0) {
      const initialKosten = STANDARD_KOSTENARTEN.map((k, i) => ({
        ...k,
        id: `kosten-${i}`,
        gesamtbetrag: 0,
      }));
      setKostenpositionen(initialKosten);
    }
  }, [kostenpositionen.length]);

  // Mieter hinzufügen
  const addMieter = () => {
    const newMieter: Mieter = {
      id: `mieter-${Date.now()}`,
      name: '',
      einheit: '',
      flaeche: 0,
      personenanzahl: 1,
      einzugsdatum: objektdaten.abrechnungszeitraumStart,
    };
    setMieter([...mieter, newMieter]);
    // Vorauszahlung hinzufügen
    setVorauszahlungen([...vorauszahlungen, { mieterId: newMieter.id, betrag: 0, monate: 12 }]);
  };

  // Mieter entfernen
  const removeMieter = (id: string) => {
    setMieter(mieter.filter(m => m.id !== id));
    setVorauszahlungen(vorauszahlungen.filter(v => v.mieterId !== id));
  };

  // Mieter aktualisieren
  const updateMieter = (id: string, field: keyof Mieter, value: string | number) => {
    setMieter(mieter.map(m => m.id === id ? { ...m, [field]: value } : m));
  };

  // Vorauszahlung aktualisieren
  const updateVorauszahlung = (mieterId: string, field: keyof Vorauszahlung, value: number) => {
    setVorauszahlungen(vorauszahlungen.map(v => 
      v.mieterId === mieterId ? { ...v, [field]: value } : v
    ));
  };

  // Objekt in Objektverwaltung speichern
  const [savingObjekt, setSavingObjekt] = useState(false);
  const saveAsObjekt = async () => {
    if (!user || !objektdaten.adresse || mieter.length === 0) {
      alert('Bitte geben Sie eine Adresse und mindestens einen Mieter ein.');
      return;
    }

    setSavingObjekt(true);
    try {
      // Adresse parsen (Format: "Straße, PLZ Ort")
      const adressParts = objektdaten.adresse.split(',');
      const strasse = adressParts[0]?.trim() || objektdaten.adresse;
      const plzOrt = adressParts[1]?.trim() || '';
      const plzMatch = plzOrt.match(/^(\d{5})\s+(.*)$/);
      const plz = plzMatch?.[1] || '';
      const ort = plzMatch?.[2] || plzOrt;

      const objektData = {
        adresse: strasse,
        plz: plz,
        ort: ort,
        gesamtflaeche: objektdaten.gesamtflaeche,
        gesamteinheiten: objektdaten.gesamteinheiten || mieter.length,
        heizungstyp: energiedaten.heizungstyp,
        typ: 'mfh' as const,
        mieter: mieter.map(m => ({
          id: m.id,
          name: m.name,
          einheit: m.einheit,
          flaeche: m.flaeche,
          personenanzahl: m.personenanzahl,
          einzugsdatum: m.einzugsdatum,
          vorauszahlung: vorauszahlungen.find(v => v.mieterId === m.id)?.betrag || 0,
        })),
        createdAt: new Date(),
      };

      const docRef = await addDoc(collection(db, 'users', user.uid, 'objekte'), objektData);
      setSelectedObjektId(docRef.id);
      
      // Objekte-Liste aktualisieren
      await loadGespeicherteObjekte(user.uid);
      
      alert('✅ Objekt erfolgreich in der Objektverwaltung gespeichert!');
    } catch (error) {
      console.error('Error saving objekt:', error);
      alert('Fehler beim Speichern des Objekts.');
    } finally {
      setSavingObjekt(false);
    }
  };

  // Kostenposition aktualisieren
  const updateKostenposition = (id: string, field: keyof Kostenposition, value: unknown) => {
    setKostenpositionen(kostenpositionen.map(k => 
      k.id === id ? { ...k, [field]: value } : k
    ));
  };

  // Berechnungslogik
  const berechneAnteil = (
    mieterData: Mieter,
    kostenposition: Kostenposition,
    alleMieter: Mieter[]
  ): number => {
    if (!kostenposition.umlagefaehig || kostenposition.gesamtbetrag === 0) return 0;

    // Zeitanteil berechnen (bei unterjährigem Ein-/Auszug)
    const start = new Date(objektdaten.abrechnungszeitraumStart);
    const ende = new Date(objektdaten.abrechnungszeitraumEnde);
    const einzug = new Date(mieterData.einzugsdatum);
    const auszug = mieterData.auszugsdatum ? new Date(mieterData.auszugsdatum) : ende;
    
    const gesamtTage = Math.ceil((ende.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1;
    const mieterStart = einzug > start ? einzug : start;
    const mieterEnde = auszug < ende ? auszug : ende;
    const mieterTage = Math.max(0, Math.ceil((mieterEnde.getTime() - mieterStart.getTime()) / (1000 * 60 * 60 * 24)) + 1);
    const zeitanteil = mieterTage / gesamtTage;

    // Grundwert je nach Umlageschlüssel
    let anteil = 0;
    switch (kostenposition.umlageschluessel) {
      case 'flaeche':
        const gesamtFlaeche = alleMieter.reduce((sum, m) => sum + m.flaeche, 0);
        anteil = gesamtFlaeche > 0 ? (mieterData.flaeche / gesamtFlaeche) * kostenposition.gesamtbetrag : 0;
        break;
      case 'personenzahl':
        const gesamtPersonen = alleMieter.reduce((sum, m) => sum + m.personenanzahl, 0);
        anteil = gesamtPersonen > 0 ? (mieterData.personenanzahl / gesamtPersonen) * kostenposition.gesamtbetrag : 0;
        break;
      case 'einheiten':
        anteil = alleMieter.length > 0 ? kostenposition.gesamtbetrag / alleMieter.length : 0;
        break;
      case 'verbrauch':
        // Bei Verbrauch nehmen wir Fläche als Proxy (echte Verbrauchsdaten wären besser)
        const gesamtFlaecheV = alleMieter.reduce((sum, m) => sum + m.flaeche, 0);
        anteil = gesamtFlaecheV > 0 ? (mieterData.flaeche / gesamtFlaecheV) * kostenposition.gesamtbetrag : 0;
        break;
      case 'miteigentumsanteil':
        // Proxy: Flächenanteil
        const gesamtFlaecheM = alleMieter.reduce((sum, m) => sum + m.flaeche, 0);
        anteil = gesamtFlaecheM > 0 ? (mieterData.flaeche / gesamtFlaecheM) * kostenposition.gesamtbetrag : 0;
        break;
    }

    return anteil * zeitanteil;
  };

  // Demo-Abrechnung für FREE-Nutzer anzeigen
  const zeigeDemoAbrechnung = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setErgebnisse(DEMO_ERGEBNISSE);
      setKiAnalyse(DEMO_KI_ANALYSE);
      setCurrentStep(5);
      setIsGenerating(false);
    }, 1500); // Kurze Animation für besseres UX
  };

  // Abrechnung generieren
  const generiereAbrechnung = async () => {
    setIsGenerating(true);
    
    // CO2-Stufe berechnen
    const co2Stufe = berechneCO2Stufe();
    
    // Für jeden Mieter Abrechnung erstellen
    const results: AbrechnungErgebnis[] = mieter.map(m => {
      const positionen = kostenpositionen
        .filter(k => k.umlagefaehig && k.gesamtbetrag > 0)
        .map(k => ({
          bezeichnung: k.bezeichnung,
          gesamtbetrag: k.gesamtbetrag,
          anteil: berechneAnteil(m, k, mieter),
          schluessel: getSchluesselText(k.umlageschluessel),
        }));

      // CO2-Kosten berechnen (anteilig nach Fläche)
      const gesamtFlaeche = mieter.reduce((sum, mi) => sum + mi.flaeche, 0);
      const flaechenAnteil = gesamtFlaeche > 0 ? m.flaeche / gesamtFlaeche : 0;
      const co2KostenAnteil = energiedaten.co2KostenGesamt * flaechenAnteil;
      const co2MieterAnteil = co2KostenAnteil * (co2Stufe.mieterAnteil / 100);
      const co2VermieterAnteil = co2KostenAnteil * (co2Stufe.vermieterAnteil / 100);

      const gesamtkosten = positionen.reduce((sum, p) => sum + p.anteil, 0) + co2MieterAnteil;
      const vorauszahlung = vorauszahlungen.find(v => v.mieterId === m.id);
      const gezahlteVorauszahlungen = vorauszahlung ? vorauszahlung.betrag * vorauszahlung.monate : 0;
      
      return {
        mieterId: m.id,
        mieterName: m.name,
        einheit: m.einheit,
        gesamtkosten,
        anteil: 100, // wird später berechnet
        vorauszahlungen: gezahlteVorauszahlungen,
        nachzahlung: gesamtkosten - gezahlteVorauszahlungen,
        co2Kosten: energiedaten.co2KostenGesamt > 0 ? {
          gesamt: co2KostenAnteil,
          mieterAnteil: co2MieterAnteil,
          vermieterAnteil: co2VermieterAnteil,
          stufe: co2Stufe.stufe,
          co2ProQm: co2Stufe.co2ProQm,
        } : undefined,
        positionen,
      };
    });

    setErgebnisse(results);
    setCurrentStep(5);
    setIsGenerating(false);

    // KI-Analyse anfordern
    await requestKiAnalyse(results);
  };

  const getSchluesselText = (schluessel: string): string => {
    switch (schluessel) {
      case 'flaeche': return 'nach Wohnfläche';
      case 'personenzahl': return 'nach Personenzahl';
      case 'einheiten': return 'nach Wohneinheiten';
      case 'verbrauch': return 'nach Verbrauch';
      case 'miteigentumsanteil': return 'nach MEA';
      default: return schluessel;
    }
  };

  // KI-Analyse
  const requestKiAnalyse = async (results: AbrechnungErgebnis[]) => {
    // Check query limit for non-lawyer users
    if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
      setKiAnalyse('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für KI-Analysen.');
      setShowUpgradeModal(true);
      return;
    }
    
    try {
      const prompt = `Analysiere diese Nebenkostenabrechnung als Immobilienrechts-Experte:

**Objekt:** ${objektdaten.adresse}
**Abrechnungszeitraum:** ${objektdaten.abrechnungszeitraumStart} bis ${objektdaten.abrechnungszeitraumEnde}
**Gesamtfläche:** ${objektdaten.gesamtflaeche} m²
**Einheiten:** ${objektdaten.gesamteinheiten}

**Kostenpositionen:**
${kostenpositionen.filter(k => k.gesamtbetrag > 0).map(k => 
  `- ${k.bezeichnung}: ${k.gesamtbetrag.toFixed(2)} € (${getSchluesselText(k.umlageschluessel)}) - ${k.rechtsgrundlage}`
).join('\n')}

**Gesamtkosten:** ${kostenpositionen.reduce((sum, k) => sum + k.gesamtbetrag, 0).toFixed(2)} €

**Abrechnungsergebnisse:**
${results.map(r => 
  `- ${r.mieterName} (${r.einheit}): Anteil ${r.gesamtkosten.toFixed(2)} €, Vorauszahlung ${r.vorauszahlungen.toFixed(2)} €, ${r.nachzahlung >= 0 ? 'Nachzahlung' : 'Guthaben'}: ${Math.abs(r.nachzahlung).toFixed(2)} €`
).join('\n')}

Prüfe bitte:
1. Sind alle Kostenarten nach BetrKV umlagefähig?
2. Sind die Umlageschlüssel korrekt gewählt?
3. Gibt es formelle Anforderungen zu beachten (§ 556 BGB)?
4. Stimmen die Verhältnisse plausibel?
5. Welche Optimierungsmöglichkeiten gibt es?
6. Wichtige BGH-Rechtsprechung zur Nebenkostenabrechnung?

Antworte strukturiert mit praktischen Handlungsempfehlungen für den Vermieter.`;

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
        
        // Increment query count for non-lawyer users
        if (user && userTier !== 'lawyer') {
          await updateDoc(doc(db, 'users', user.uid), {
            queriesUsed: increment(1)
          });
          setQueriesUsed(prev => prev + 1);
        }
      }
    } catch (error) {
      console.error('KI-Analyse Fehler:', error);
      setKiAnalyse('KI-Analyse konnte nicht geladen werden.');
    }
  };

  // KI-Erklärung für einzelne Themen
  const requestKiErklaerung = async (thema: string, kontext: string) => {
    // Check query limit for non-lawyer users
    if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
      setKiErklaerungTitel(thema);
      setKiErklaerung('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für KI-Erklärungen.');
      setShowKiErklaerung(true);
      setShowUpgradeModal(true);
      return;
    }
    
    setLoadingKiErklaerung(true);
    setKiErklaerungTitel(thema);
    setShowKiErklaerung(true);
    setKiErklaerung('');

    try {
      const prompt = `Du bist ein Experte für deutsches Mietrecht und Nebenkostenabrechnungen. Erkläre verständlich und praxisnah:

**Thema:** ${thema}

**Kontext:** ${kontext}

Erkläre:
1. Was bedeutet das genau?
2. Welche rechtlichen Grundlagen gibt es? (BGB, BetrKV, etc.)
3. Was muss der Vermieter beachten?
4. Praktische Tipps und häufige Fehler
5. Aktuelle BGH-Rechtsprechung (falls relevant)

Antworte prägnant und strukturiert. Verwende Beispiele wo hilfreich.`;

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
        setKiErklaerung(data.answer || data.response || 'Keine Erklärung verfügbar.');
        
        // Increment query count for non-lawyer users
        if (user && userTier !== 'lawyer') {
          await updateDoc(doc(db, 'users', user.uid), {
            queriesUsed: increment(1)
          });
          setQueriesUsed(prev => prev + 1);
        }
      } else {
        setKiErklaerung('Erklärung konnte nicht geladen werden.');
      }
    } catch (error) {
      console.error('KI-Erklärung Fehler:', error);
      setKiErklaerung('Erklärung konnte nicht geladen werden. Bitte versuchen Sie es später erneut.');
    } finally {
      setLoadingKiErklaerung(false);
    }
  };

  // Info-Button Komponente
  const KiInfoButton = ({ thema, kontext, klein = false }: { thema: string; kontext: string; klein?: boolean }) => (
    <button
      type="button"
      onClick={() => requestKiErklaerung(thema, kontext)}
      className={`inline-flex items-center justify-center text-blue-400 hover:text-blue-300 hover:bg-blue-500/20 rounded-full transition-all ${
        klein ? 'w-5 h-5 text-xs ml-1' : 'w-6 h-6 text-sm ml-2'
      }`}
      title={`KI-Erklärung: ${thema}`}
    >
      <span>?</span>
    </button>
  );

  // PDF-Export (vereinfacht)
  const exportPDF = (ergebnis: AbrechnungErgebnis) => {
    const co2Section = ergebnis.co2Kosten ? `
CO2-KOSTENAUFTEILUNG (gem. CO2KostAufG)
---------------------------------------
Stufe: ${ergebnis.co2Kosten.stufe} von 10 (${ergebnis.co2Kosten.co2ProQm} kg CO2/m²/Jahr)
CO2-Kosten anteilig: ${ergebnis.co2Kosten.gesamt.toFixed(2)} €
Mieter-Anteil: ${ergebnis.co2Kosten.mieterAnteil.toFixed(2)} €
Vermieter-Anteil: ${ergebnis.co2Kosten.vermieterAnteil.toFixed(2)} €

` : '';

    const content = `
NEBENKOSTENABRECHNUNG
=====================

Vermieter: [Ihr Name]
Objekt: ${objektdaten.adresse}

Mieter: ${ergebnis.mieterName}
Einheit: ${ergebnis.einheit}
Abrechnungszeitraum: ${objektdaten.abrechnungszeitraumStart} bis ${objektdaten.abrechnungszeitraumEnde}

KOSTENAUFSTELLUNG
-----------------
${ergebnis.positionen.map(p => 
  `${p.bezeichnung}
  Gesamtkosten: ${p.gesamtbetrag.toFixed(2)} €
  Ihr Anteil (${p.schluessel}): ${p.anteil.toFixed(2)} €
`).join('\n')}
${co2Section}
ZUSAMMENFASSUNG
---------------
Gesamtbetrag Nebenkosten: ${ergebnis.gesamtkosten.toFixed(2)} €
Ihre Vorauszahlungen: ${ergebnis.vorauszahlungen.toFixed(2)} €
${ergebnis.nachzahlung >= 0 
  ? `Nachzahlung: ${ergebnis.nachzahlung.toFixed(2)} €` 
  : `Guthaben: ${Math.abs(ergebnis.nachzahlung).toFixed(2)} €`}

Zahlungsfrist: 30 Tage nach Zugang

Bitte überweisen Sie den Betrag auf folgendes Konto:
[Kontodetails einfügen]

Hinweis gemäß § 556 Abs. 3 BGB:
Gegen diese Abrechnung können Sie innerhalb von 12 Monaten nach Zugang Einwendungen erheben.
${ergebnis.co2Kosten ? `
Hinweis zur CO2-Kostenaufteilung gemäß § 6 CO2KostAufG:
Die Aufteilung der CO2-Kosten erfolgt nach dem gesetzlichen Stufenmodell basierend 
auf dem spezifischen CO2-Ausstoß des Gebäudes.
` : ''}
Mit freundlichen Grüßen
[Ihr Name]

---
Erstellt mit domulex.ai - KI-Nebenkostenabrechnung (inkl. CO2KostAufG-Konformität)
    `;

    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Nebenkostenabrechnung_${ergebnis.mieterName.replace(/\s/g, '_')}_${objektdaten.abrechnungsjahr}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Render Steps
  const renderStep1 = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-blue-500/20">
        <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
          <span className="text-2xl">🏠</span> Objektdaten
        </h3>
        <p className="text-gray-400 text-sm">Wählen Sie ein gespeichertes Objekt oder geben Sie die Daten manuell ein.</p>
      </div>

      {/* Gespeicherte Objekte Auswahl */}
      {user && gespeicherteObjekte.length > 0 && (
        <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
          <label className="block text-sm font-medium text-gray-300 mb-3">📁 Gespeichertes Objekt laden</label>
          <div className="flex flex-wrap gap-3">
            {gespeicherteObjekte.map((objekt) => (
              <button
                key={objekt.id}
                onClick={() => loadObjektDaten(objekt)}
                className={`px-4 py-3 rounded-lg border transition-all text-left ${
                  selectedObjektId === objekt.id
                    ? 'bg-blue-600 border-blue-500 text-white'
                    : 'bg-gray-700/50 border-gray-600 text-gray-300 hover:border-blue-500'
                }`}
              >
                <span className="font-medium">{objekt.adresse}</span>
                <span className="text-sm block opacity-75">{objekt.plz} {objekt.ort}</span>
                <span className="text-xs opacity-60">{objekt.mieter?.length || 0} Mieter • {objekt.gesamtflaeche}m²</span>
              </button>
            ))}
          </div>
          <div className="mt-3 flex items-center gap-2 text-sm text-gray-400">
            <span>💡</span>
            <span>Objekte können in der <a href="/app/objekte" className="text-blue-400 hover:underline">Objektverwaltung</a> angelegt werden.</span>
          </div>
        </div>
      )}

      {user && gespeicherteObjekte.length === 0 && !loadingObjekte && (
        <div className="bg-gray-800/30 rounded-xl p-6 border border-dashed border-gray-600">
          <p className="text-gray-400 text-sm">
            <span className="text-lg mr-2">💡</span>
            Tipp: In der <a href="/app/objekte" className="text-blue-400 hover:underline">Objektverwaltung</a> können Sie Objekte und Mieter dauerhaft speichern und hier laden.
          </p>
        </div>
      )}

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-700"></div>
        </div>
        <div className="relative flex justify-center">
          <span className="px-3 bg-gray-900 text-gray-500 text-sm">oder manuell eingeben</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-300 mb-2">Objektadresse *</label>
          <input
            type="text"
            value={objektdaten.adresse}
            onChange={(e) => setObjektdaten({ ...objektdaten, adresse: e.target.value })}
            placeholder="Musterstraße 123, 12345 Berlin"
            className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Gesamtwohnfläche (m²) *</label>
          <input
            type="number"
            value={objektdaten.gesamtflaeche || ''}
            onChange={(e) => setObjektdaten({ ...objektdaten, gesamtflaeche: parseFloat(e.target.value) || 0 })}
            placeholder="500"
            className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Anzahl Wohneinheiten *</label>
          <input
            type="number"
            value={objektdaten.gesamteinheiten || ''}
            onChange={(e) => setObjektdaten({ ...objektdaten, gesamteinheiten: parseInt(e.target.value) || 0 })}
            placeholder="6"
            className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Abrechnungszeitraum Start *</label>
          <input
            type="date"
            value={objektdaten.abrechnungszeitraumStart}
            onChange={(e) => setObjektdaten({ ...objektdaten, abrechnungszeitraumStart: e.target.value })}
            className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Abrechnungszeitraum Ende *</label>
          <input
            type="date"
            value={objektdaten.abrechnungszeitraumEnde}
            onChange={(e) => setObjektdaten({ ...objektdaten, abrechnungszeitraumEnde: e.target.value })}
            className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
        <p className="text-amber-400 text-sm flex items-start gap-2">
          <span className="text-lg">⚠️</span>
          <span className="flex-1">
            <strong>§ 556 Abs. 3 BGB:</strong> Die Abrechnung muss dem Mieter spätestens 12 Monate nach Ende des Abrechnungszeitraums zugehen.
            <KiInfoButton 
              thema="Abrechnungsfrist nach § 556 Abs. 3 BGB" 
              kontext="Vermieter muss Nebenkostenabrechnung binnen 12 Monaten nach Abrechnungszeitraum zustellen. Was passiert bei Fristversäumnis? Welche Ausnahmen gibt es? Wann beginnt die Frist? Wie wird zugestellt?"
              klein
            />
          </span>
        </p>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-xl p-6 border border-green-500/20">
        <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
          <span className="text-2xl">👥</span> Mieter & Einheiten
        </h3>
        <p className="text-gray-400 text-sm">Erfassen Sie alle Mieter mit ihren Wohnungen und Vorauszahlungen.</p>
      </div>

      {mieter.length === 0 ? (
        <div className="text-center py-12 bg-gray-800/30 rounded-xl border border-dashed border-gray-700">
          <p className="text-gray-400 mb-4">Noch keine Mieter erfasst</p>
          <button
            onClick={addMieter}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            + Ersten Mieter hinzufügen
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {mieter.map((m, index) => (
            <div key={m.id} className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-lg font-semibold text-white">Mieter {index + 1}</h4>
                <button
                  onClick={() => removeMieter(m.id)}
                  className="text-red-400 hover:text-red-300 text-sm"
                >
                  Entfernen
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Name *</label>
                  <input
                    type="text"
                    value={m.name}
                    onChange={(e) => updateMieter(m.id, 'name', e.target.value)}
                    placeholder="Max Mustermann"
                    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Wohneinheit *</label>
                  <input
                    type="text"
                    value={m.einheit}
                    onChange={(e) => updateMieter(m.id, 'einheit', e.target.value)}
                    placeholder="EG links"
                    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Wohnfläche (m²) *</label>
                  <input
                    type="number"
                    value={m.flaeche || ''}
                    onChange={(e) => updateMieter(m.id, 'flaeche', parseFloat(e.target.value) || 0)}
                    placeholder="75"
                    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Personenanzahl</label>
                  <input
                    type="number"
                    min="1"
                    value={m.personenanzahl}
                    onChange={(e) => updateMieter(m.id, 'personenanzahl', parseInt(e.target.value) || 1)}
                    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Einzugsdatum</label>
                  <input
                    type="date"
                    value={m.einzugsdatum}
                    onChange={(e) => updateMieter(m.id, 'einzugsdatum', e.target.value)}
                    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Auszugsdatum (falls)</label>
                  <input
                    type="date"
                    value={m.auszugsdatum || ''}
                    onChange={(e) => updateMieter(m.id, 'auszugsdatum', e.target.value)}
                    className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                  />
                </div>
              </div>

              {/* Vorauszahlungen */}
              <div className="mt-4 pt-4 border-t border-gray-700">
                <h5 className="text-sm font-medium text-gray-300 mb-3">Vorauszahlungen</h5>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Monatliche Vorauszahlung (€)</label>
                    <input
                      type="number"
                      value={vorauszahlungen.find(v => v.mieterId === m.id)?.betrag || 0}
                      onChange={(e) => updateVorauszahlung(m.id, 'betrag', parseFloat(e.target.value) || 0)}
                      placeholder="200"
                      className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Anzahl Monate</label>
                    <input
                      type="number"
                      min="1"
                      max="12"
                      value={vorauszahlungen.find(v => v.mieterId === m.id)?.monate || 12}
                      onChange={(e) => updateVorauszahlung(m.id, 'monate', parseInt(e.target.value) || 12)}
                      className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500"
                    />
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Summe Vorauszahlungen: {((vorauszahlungen.find(v => v.mieterId === m.id)?.betrag || 0) * (vorauszahlungen.find(v => v.mieterId === m.id)?.monate || 12)).toFixed(2)} €
                </p>
              </div>
            </div>
          ))}

          <button
            onClick={addMieter}
            className="w-full py-3 border-2 border-dashed border-gray-600 text-gray-400 hover:border-blue-500 hover:text-blue-400 rounded-lg transition-colors"
          >
            + Weiteren Mieter hinzufügen
          </button>
        </div>
      )}

      {mieter.length > 0 && (
        <div className="space-y-4">
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
            <p className="text-blue-400 text-sm">
              <strong>Summe Wohnflächen:</strong> {mieter.reduce((sum, m) => sum + m.flaeche, 0).toFixed(2)} m² von {objektdaten.gesamtflaeche} m² erfasst
            </p>
          </div>
          
          {/* Als Objekt speichern Button - nur wenn nicht bereits ein gespeichertes Objekt geladen wurde */}
          {!selectedObjektId && objektdaten.adresse && (
            <button
              onClick={saveAsObjekt}
              disabled={savingObjekt}
              className="w-full py-3 bg-green-600 hover:bg-green-700 disabled:bg-green-800 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
            >
              {savingObjekt ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Speichern...
                </>
              ) : (
                <>
                  💾 In Objektverwaltung speichern
                </>
              )}
            </button>
          )}
        </div>
      )}
    </div>
  );

  const renderStep3 = () => {
    const kategorien = [...new Set(kostenpositionen.map(k => k.kategorie))];
    const gesamtkosten = kostenpositionen.reduce((sum, k) => sum + k.gesamtbetrag, 0);

    return (
      <div className="space-y-6">
        <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-xl p-6 border border-purple-500/20">
          <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
            <span className="text-2xl">💰</span> Kostenpositionen (§ 2 BetrKV)
            <KiInfoButton 
              thema="Umlagefähige Betriebskosten nach BetrKV" 
              kontext="Welche Kosten dürfen nach der Betriebskostenverordnung (BetrKV) auf Mieter umgelegt werden? Was ist nicht umlagefähig? Verwaltungskosten, Instandhaltung?"
            />
          </h3>
          <p className="text-gray-400 text-sm">Tragen Sie die Jahreskosten für jede Position ein.</p>
        </div>

        {kategorien.map(kategorie => (
          <div key={kategorie} className="bg-gray-800/30 rounded-xl p-6 border border-gray-700">
            <h4 className="text-lg font-semibold text-white mb-4 flex items-center">
              {kategorie}
              <KiInfoButton 
                thema={`Betriebskosten: ${kategorie}`} 
                kontext={`Erkläre die Kostenart "${kategorie}" in der Nebenkostenabrechnung. Was gehört dazu? Welcher Umlageschlüssel ist typisch? Was sind häufige Streitpunkte?`}
                klein
              />
            </h4>
            <div className="space-y-3">
              {kostenpositionen.filter(k => k.kategorie === kategorie).map(position => (
                <div key={position.id} className="grid grid-cols-12 gap-4 items-center">
                  <div className="col-span-5">
                    <div className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={position.umlagefaehig}
                        onChange={(e) => updateKostenposition(position.id, 'umlagefaehig', e.target.checked)}
                        className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-blue-500"
                      />
                      <div className="flex-1">
                        <span className="text-white text-sm">{position.bezeichnung}</span>
                        <button
                          type="button"
                          onClick={() => requestKiErklaerung(
                            position.bezeichnung,
                            `Erkläre die Betriebskostenposition "${position.bezeichnung}" (${position.rechtsgrundlage}). Was ist umlagefähig? Welcher Umlageschlüssel? Typische Fehler? Aktuelle BGH-Rechtsprechung?`
                          )}
                          className="ml-1 text-blue-400 hover:text-blue-300 text-xs"
                          title="KI-Erklärung"
                        >
                          ⓘ
                        </button>
                        {position.hinweis && (
                          <span className="text-xs text-gray-500 block">{position.hinweis}</span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="col-span-3">
                    <input
                      type="number"
                      value={position.gesamtbetrag || ''}
                      onChange={(e) => updateKostenposition(position.id, 'gesamtbetrag', parseFloat(e.target.value) || 0)}
                      placeholder="0,00"
                      className="w-full px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm text-right focus:border-blue-500"
                    />
                  </div>
                  <div className="col-span-2">
                    <select
                      value={position.umlageschluessel}
                      onChange={(e) => updateKostenposition(position.id, 'umlageschluessel', e.target.value)}
                      className="w-full px-2 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-xs focus:border-blue-500"
                    >
                      <option value="flaeche">Fläche</option>
                      <option value="personenzahl">Personen</option>
                      <option value="einheiten">Einheiten</option>
                      <option value="verbrauch">Verbrauch</option>
                      <option value="miteigentumsanteil">MEA</option>
                    </select>
                  </div>
                  <div className="col-span-2 text-right">
                    <span className="text-xs text-gray-500">{position.rechtsgrundlage}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

        <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-xl p-6 border border-green-500/30">
          <div className="flex justify-between items-center">
            <span className="text-xl font-bold text-white">Gesamtkosten:</span>
            <span className="text-2xl font-bold text-green-400">{gesamtkosten.toFixed(2)} €</span>
          </div>
          <p className="text-sm text-gray-400 mt-2">
            Pro m²: {objektdaten.gesamtflaeche > 0 ? (gesamtkosten / objektdaten.gesamtflaeche).toFixed(2) : '0.00'} €/m²/Jahr
          </p>
        </div>

        {/* Umlageschlüssel Erklärung */}
        <div className="bg-gray-800/30 rounded-lg p-4 border border-gray-700">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-gray-400 text-sm font-medium">Umlageschlüssel verstehen</span>
            <KiInfoButton 
              thema="Umlageschlüssel in der Nebenkostenabrechnung" 
              kontext="Erkläre die verschiedenen Umlageschlüssel: Wohnfläche, Personenzahl, Wohneinheiten, Verbrauch, Miteigentumsanteile. Wann ist welcher Schlüssel sinnvoll? Was sagt die Rechtsprechung?"
            />
          </div>
          <div className="grid grid-cols-5 gap-2 text-xs text-gray-400">
            <div className="flex items-center gap-1"><span className="text-blue-400">📐</span> Fläche = m²</div>
            <div className="flex items-center gap-1"><span className="text-green-400">👥</span> Personen</div>
            <div className="flex items-center gap-1"><span className="text-yellow-400">🏠</span> Einheiten</div>
            <div className="flex items-center gap-1"><span className="text-orange-400">📊</span> Verbrauch</div>
            <div className="flex items-center gap-1"><span className="text-purple-400">%</span> MEA</div>
          </div>
        </div>
      </div>
    );
  };

  // Step 4: CO2-Kostenaufteilung nach CO2KostAufG
  const renderStep4 = () => {
    const co2Berechnung = berechneCO2Stufe();
    const heizungLabel = HEIZUNGSTYPEN.find(h => h.id === energiedaten.heizungstyp)?.label || 'Erdgas';

    return (
      <div className="space-y-6">
        <div className="bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-xl p-6 border border-green-500/20">
          <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
            <span className="text-2xl">🌱</span> CO₂-Kostenaufteilung (CO2KostAufG)
            <KiInfoButton 
              thema="CO2-Kostenaufteilungsgesetz (CO2KostAufG)" 
              kontext="Was ist das CO2KostAufG? Seit wann gilt es? Wie funktioniert das 10-Stufen-Modell? Was muss der Vermieter beachten? Welche Ausnahmen gibt es (Denkmalschutz, Milieuschutz)?"
            />
          </h3>
          <p className="text-gray-400 text-sm">
            Pflicht seit 2023: Die CO₂-Kosten müssen zwischen Mieter und Vermieter aufgeteilt werden.
          </p>
        </div>

        {/* Heizungsdaten */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
              Heizungstyp *
              <KiInfoButton 
                thema="Heizungstypen und CO₂-Emissionsfaktoren" 
                kontext="Erkläre die verschiedenen Heizungstypen (Erdgas, Heizöl, Fernwärme, Wärmepumpe, Pellets) und ihre CO2-Emissionsfaktoren. Woher kommen die Werte? Wie wirkt sich die Wahl auf die CO2-Kostenaufteilung aus?"
                klein
              />
            </label>
            <select
              value={energiedaten.heizungstyp}
              onChange={(e) => setEnergiedaten({ ...energiedaten, heizungstyp: e.target.value })}
              className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-green-500 focus:ring-1 focus:ring-green-500"
            >
              {HEIZUNGSTYPEN.map(h => (
                <option key={h.id} value={h.id}>{h.label} ({h.co2FaktorKgProKwh} kg CO₂/kWh)</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Jahresverbrauch (kWh) *</label>
            <input
              type="number"
              value={energiedaten.jahresverbrauchKwh || ''}
              onChange={(e) => setEnergiedaten({ ...energiedaten, jahresverbrauchKwh: parseFloat(e.target.value) || 0 })}
              placeholder="z.B. 50000"
              className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-green-500 focus:ring-1 focus:ring-green-500"
            />
            <p className="text-xs text-gray-500 mt-1">Aus Ihrer Jahresabrechnung des Energieversorgers</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
              CO₂-Kosten gesamt (€) *
              <KiInfoButton 
                thema="CO₂-Kosten auf der Energierechnung" 
                kontext="Wo finde ich die CO2-Kosten auf meiner Energieabrechnung? Wie werden sie berechnet? Was ist der aktuelle CO2-Preis pro Tonne? Wie entwickelt sich der Preis?"
                klein
              />
            </label>
            <input
              type="number"
              value={energiedaten.co2KostenGesamt || ''}
              onChange={(e) => setEnergiedaten({ ...energiedaten, co2KostenGesamt: parseFloat(e.target.value) || 0 })}
              placeholder="z.B. 450"
              className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-green-500 focus:ring-1 focus:ring-green-500"
            />
            <p className="text-xs text-gray-500 mt-1">Steht auf Ihrer Energieabrechnung als "CO₂-Abgabe" oder "CO₂-Kosten"</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2 flex items-center">
              Energieausweis (optional)
              <KiInfoButton 
                thema="Energieausweis und Einstufung" 
                kontext="Was sagt der Energieausweis aus? Unterschied Verbrauchs- vs. Bedarfsausweis? Welche Energieeffizienzklasse entspricht welchem CO2-Ausstoß? Wann ist ein Energieausweis Pflicht?"
                klein
              />
            </label>
            <select
              value={energiedaten.energieausweis || ''}
              onChange={(e) => setEnergiedaten({ ...energiedaten, energieausweis: e.target.value })}
              className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-green-500 focus:ring-1 focus:ring-green-500"
            >
              <option value="">Nicht angegeben</option>
              <option value="A+">A+ (unter 30 kWh/m²a)</option>
              <option value="A">A (30-50 kWh/m²a)</option>
              <option value="B">B (50-75 kWh/m²a)</option>
              <option value="C">C (75-100 kWh/m²a)</option>
              <option value="D">D (100-130 kWh/m²a)</option>
              <option value="E">E (130-160 kWh/m²a)</option>
              <option value="F">F (160-200 kWh/m²a)</option>
              <option value="G">G (200-250 kWh/m²a)</option>
              <option value="H">H (über 250 kWh/m²a)</option>
            </select>
          </div>
        </div>

        {/* CO2-Stufenmodell Anzeige */}
        {energiedaten.jahresverbrauchKwh > 0 && objektdaten.gesamtflaeche > 0 && (
          <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-xl p-6 border border-green-500/30">
            <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <span>📊</span> Automatische Einstufung nach CO2KostAufG
              <KiInfoButton 
                thema="Das 10-Stufen-Modell des CO2KostAufG" 
                kontext={`Das Gebäude wurde in Stufe ${co2Berechnung.stufe} eingestuft (${co2Berechnung.co2ProQm} kg CO2/m²/Jahr). Erkläre was das bedeutet, wie die Stufen funktionieren, und was der Vermieter tun kann um in eine bessere Stufe zu kommen.`}
              />
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">CO₂-Ausstoß</p>
                <p className="text-2xl font-bold text-white">{co2Berechnung.co2ProQm}</p>
                <p className="text-sm text-gray-400">kg/m²/Jahr</p>
              </div>
              <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">Stufe</p>
                <p className="text-2xl font-bold text-green-400">{co2Berechnung.stufe}</p>
                <p className="text-sm text-gray-400">von 10</p>
              </div>
              <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                <p className="text-xs text-gray-500 mb-1">Aufteilung</p>
                <p className="text-lg font-bold">
                  <span className="text-blue-400">{co2Berechnung.mieterAnteil}%</span>
                  <span className="text-gray-500 mx-2">/</span>
                  <span className="text-orange-400">{co2Berechnung.vermieterAnteil}%</span>
                </p>
                <p className="text-xs text-gray-400">Mieter / Vermieter</p>
              </div>
            </div>

            {energiedaten.co2KostenGesamt > 0 && (
              <div className="bg-gray-900/50 rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-400">CO₂-Kosten Mieter-Anteil</p>
                    <p className="text-xl font-bold text-blue-400">
                      {(energiedaten.co2KostenGesamt * co2Berechnung.mieterAnteil / 100).toFixed(2)} €
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-400">Vermieter trägt</p>
                    <p className="text-xl font-bold text-orange-400">
                      {(energiedaten.co2KostenGesamt * co2Berechnung.vermieterAnteil / 100).toFixed(2)} €
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Stufenmodell Referenz-Tabelle */}
        <div className="bg-gray-800/30 rounded-xl p-6 border border-gray-700">
          <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
            <span>📋</span> CO₂-Stufenmodell nach § 5, § 6 CO2KostAufG
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-400 border-b border-gray-700">
                  <th className="py-2 text-left">Stufe</th>
                  <th className="py-2 text-left">kg CO₂/m²/Jahr</th>
                  <th className="py-2 text-center">Mieter</th>
                  <th className="py-2 text-center">Vermieter</th>
                </tr>
              </thead>
              <tbody>
                {CO2_STUFEN.map((s) => (
                  <tr 
                    key={s.stufe} 
                    className={`border-b border-gray-800 ${co2Berechnung.stufe === s.stufe ? 'bg-green-500/20' : ''}`}
                  >
                    <td className="py-2 text-white">{s.stufe}</td>
                    <td className="py-2 text-gray-300">
                      {s.stufe === 1 ? '< 12' : s.stufe === 10 ? '> 52' : `${CO2_STUFEN[s.stufe - 2]?.maxCO2 || 0} – ${s.maxCO2}`}
                    </td>
                    <td className="py-2 text-center text-blue-400">{s.mieterAnteil}%</td>
                    <td className="py-2 text-center text-orange-400">{s.vermieterAnteil}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Rechtlicher Hinweis */}
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
          <p className="text-amber-400 text-sm flex items-start gap-2">
            <span className="text-lg">⚠️</span>
            <span>
              <strong>§ 7 CO2KostAufG:</strong> Wenn die CO₂-Kostenaufteilung nicht ordnungsgemäß erfolgt, 
              kann der Mieter seinen Heizkostenanteil pauschal um 3% kürzen. Bei Heizung mit {heizungLabel} 
              beträgt Ihr aktueller CO₂-Faktor {HEIZUNGSTYPEN.find(h => h.id === energiedaten.heizungstyp)?.co2FaktorKgProKwh} kg CO₂/kWh.
            </span>
          </p>
        </div>
      </div>
    );
  };

  // Step 5: Ergebnisse (vorher Step 4)
  const renderStep5 = () => (
    <div className="space-y-6">
      {/* Demo-Banner für FREE-Nutzer */}
      {!hasAccess && (
        <div className="bg-gradient-to-r from-amber-500/20 to-orange-500/20 border border-amber-500/40 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🔐</span>
              <div>
                <p className="text-amber-300 font-medium">Demo-Abrechnung</p>
                <p className="text-amber-200/70 text-sm">Dies ist eine Beispiel-Abrechnung. Upgraden Sie für Ihre eigenen Daten.</p>
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

      <div className="bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-xl p-6 border border-green-500/20">
        <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
          <span className="text-2xl">✅</span> Abrechnungsergebnisse
          <KiInfoButton 
            thema="Nebenkostenabrechnung: Formelle Anforderungen" 
            kontext="Welche formellen Anforderungen muss eine Nebenkostenabrechnung erfüllen? Was muss enthalten sein? Wann ist sie unwirksam? Welche Fristen gelten für Einwendungen?"
          />
        </h3>
        <p className="text-gray-400 text-sm">Übersicht aller Mieterabrechnungen für {!hasAccess ? '2024' : objektdaten.abrechnungsjahr}.</p>
      </div>

      {/* Schnell-Hilfe Box */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
        <h4 className="text-sm font-medium text-blue-400 mb-3 flex items-center gap-2">
          <span>💡</span> Schnelle KI-Hilfe
        </h4>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => requestKiErklaerung('Nachzahlung durchsetzen', 'Wie fordere ich als Vermieter eine Nebenkostennachzahlung korrekt ein? Welche Fristen muss ich beachten? Was tun bei Zahlungsverweigerung?')}
            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors"
          >
            Nachzahlung einfordern
          </button>
          <button
            onClick={() => requestKiErklaerung('Guthaben auszahlen', 'Wann muss ich als Vermieter ein Nebenkostenguthaben auszahlen? Welche Fristen gelten? Darf ich mit offenen Forderungen verrechnen?')}
            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors"
          >
            Guthaben auszahlen
          </button>
          <button
            onClick={() => requestKiErklaerung('Einwendungsfristen', 'Welche Fristen hat der Mieter für Einwendungen gegen die Nebenkostenabrechnung? Was passiert nach Fristablauf? § 556 Abs. 3 BGB.')}
            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors"
          >
            Einwendungsfrist Mieter
          </button>
          <button
            onClick={() => requestKiErklaerung('Belegeinsicht gewähren', 'Wann und wie muss ich dem Mieter Belegeinsicht gewähren? Welche Unterlagen müssen vorgelegt werden? Darf ich Kopierkosten berechnen?')}
            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors"
          >
            Belegeinsicht
          </button>
          <button
            onClick={() => requestKiErklaerung('Vorauszahlungen anpassen', 'Wann und wie kann ich die Nebenkostenvorauszahlung anpassen? Welche Grenzen gibt es? Was muss im Mietvertrag stehen?')}
            className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 text-xs rounded-lg transition-colors"
          >
            Vorauszahlung anpassen
          </button>
        </div>
      </div>

      {/* KI-Analyse Button */}
      {kiAnalyse && (
        <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-6">
          <button
            onClick={() => setShowKiAnalyse(!showKiAnalyse)}
            className="flex items-center gap-2 text-purple-400 hover:text-purple-300 font-medium mb-4"
          >
            <span className="text-xl">🤖</span>
            KI-Analyse {showKiAnalyse ? 'ausblenden' : 'anzeigen'}
          </button>
          {showKiAnalyse && (
            <div className="prose prose-invert prose-sm max-w-none">
              <div className="whitespace-pre-wrap text-gray-300">{kiAnalyse}</div>
            </div>
          )}
        </div>
      )}

      {/* Ergebnisse */}
      {ergebnisse.map(ergebnis => (
        <div key={ergebnis.mieterId} className="bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden">
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h4 className="text-lg font-bold text-white">{ergebnis.mieterName}</h4>
                <p className="text-sm text-gray-400">{ergebnis.einheit}</p>
              </div>
              <div className="flex items-center gap-2">
                <div className={`text-2xl font-bold ${ergebnis.nachzahlung >= 0 ? 'text-red-400' : 'text-green-400'}`}>
                  {ergebnis.nachzahlung >= 0 ? '+' : ''}{ergebnis.nachzahlung.toFixed(2)} €
                </div>
                <KiInfoButton 
                  thema={ergebnis.nachzahlung >= 0 ? 'Nachzahlung erklärt' : 'Guthaben erklärt'}
                  kontext={`Der Mieter ${ergebnis.mieterName} hat eine ${ergebnis.nachzahlung >= 0 ? 'Nachzahlung von ' + ergebnis.nachzahlung.toFixed(2) + '€' : 'Gutschrift von ' + Math.abs(ergebnis.nachzahlung).toFixed(2) + '€'}. Gesamtkosten: ${ergebnis.gesamtkosten.toFixed(2)}€, Vorauszahlungen: ${ergebnis.vorauszahlungen.toFixed(2)}€. Erkläre wie das Ergebnis zustande kommt und was die nächsten Schritte sind.`}
                  klein
                />
              </div>
            </div>

            {/* CO2-Kosten Anzeige */}
            {ergebnis.co2Kosten && (
              <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 mb-4">
                <h5 className="text-sm font-medium text-green-400 mb-2 flex items-center gap-2">
                  <span>🌱</span> CO₂-Kostenaufteilung (Stufe {ergebnis.co2Kosten.stufe})
                  <KiInfoButton 
                    thema={`CO₂-Stufe ${ergebnis.co2Kosten.stufe} erklärt`}
                    kontext={`Das Gebäude liegt in Stufe ${ergebnis.co2Kosten.stufe} mit ${ergebnis.co2Kosten.co2ProQm} kg CO2/m²/Jahr. Der Mieter trägt ${CO2_STUFEN[ergebnis.co2Kosten.stufe - 1]?.mieterAnteil || 0}%, der Vermieter ${CO2_STUFEN[ergebnis.co2Kosten.stufe - 1]?.vermieterAnteil || 0}%. Erkläre was der Vermieter tun kann um die Stufe zu verbessern und Kosten zu senken.`}
                    klein
                  />
                </h5>
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <p className="text-xs text-gray-500">CO₂-Kosten anteilig</p>
                    <p className="text-sm font-bold text-white">{ergebnis.co2Kosten.gesamt.toFixed(2)} €</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Ihr Anteil</p>
                    <p className="text-sm font-bold text-blue-400">{ergebnis.co2Kosten.mieterAnteil.toFixed(2)} €</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Vermieter trägt</p>
                    <p className="text-sm font-bold text-orange-400">{ergebnis.co2Kosten.vermieterAnteil.toFixed(2)} €</p>
                  </div>
                </div>
              </div>
            )}

            {/* Kostenaufstellung */}
            <div className="bg-gray-900/50 rounded-lg p-4 mb-4">
              <h5 className="text-sm font-medium text-gray-300 mb-3">Kostenaufstellung</h5>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {ergebnis.positionen.map((p, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span className="text-gray-400">{p.bezeichnung} <span className="text-gray-600">({p.schluessel})</span></span>
                    <span className="text-white">{p.anteil.toFixed(2)} €</span>
                  </div>
                ))}
                {ergebnis.co2Kosten && (
                  <div className="flex justify-between text-sm border-t border-gray-700 pt-2 mt-2">
                    <span className="text-green-400">CO₂-Kostenanteil (nach CO2KostAufG)</span>
                    <span className="text-green-400">{ergebnis.co2Kosten.mieterAnteil.toFixed(2)} €</span>
                  </div>
                )}
              </div>
            </div>

            {/* Zusammenfassung */}
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-gray-900/50 rounded-lg p-3">
                <p className="text-xs text-gray-500">Gesamtkosten</p>
                <p className="text-lg font-bold text-white">{ergebnis.gesamtkosten.toFixed(2)} €</p>
              </div>
              <div className="bg-gray-900/50 rounded-lg p-3">
                <p className="text-xs text-gray-500">Vorauszahlungen</p>
                <p className="text-lg font-bold text-blue-400">{ergebnis.vorauszahlungen.toFixed(2)} €</p>
              </div>
              <div className={`rounded-lg p-3 ${ergebnis.nachzahlung >= 0 ? 'bg-red-500/20' : 'bg-green-500/20'}`}>
                <p className="text-xs text-gray-400">{ergebnis.nachzahlung >= 0 ? 'Nachzahlung' : 'Guthaben'}</p>
                <p className={`text-lg font-bold ${ergebnis.nachzahlung >= 0 ? 'text-red-400' : 'text-green-400'}`}>
                  {Math.abs(ergebnis.nachzahlung).toFixed(2)} €
                </p>
              </div>
            </div>

            {/* Export Button */}
            <button
              onClick={() => exportPDF(ergebnis)}
              className="w-full mt-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
            >
              <span>📄</span> Abrechnung exportieren
            </button>
          </div>
        </div>
      ))}

      {/* Gesamt-Übersicht */}
      <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-6 border border-blue-500/30">
        <h4 className="text-lg font-bold text-white mb-4">Gesamtübersicht</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <p className="text-xs text-gray-500">Gesamtkosten</p>
            <p className="text-xl font-bold text-white">
              {kostenpositionen.reduce((sum, k) => sum + k.gesamtbetrag, 0).toFixed(2)} €
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Umgelegt</p>
            <p className="text-xl font-bold text-green-400">
              {ergebnisse.reduce((sum, e) => sum + e.gesamtkosten, 0).toFixed(2)} €
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Vorauszahlungen</p>
            <p className="text-xl font-bold text-blue-400">
              {ergebnisse.reduce((sum, e) => sum + e.vorauszahlungen, 0).toFixed(2)} €
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Saldo</p>
            <p className={`text-xl font-bold ${ergebnisse.reduce((sum, e) => sum + e.nachzahlung, 0) >= 0 ? 'text-red-400' : 'text-green-400'}`}>
              {ergebnisse.reduce((sum, e) => sum + e.nachzahlung, 0).toFixed(2)} €
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return objektdaten.adresse && objektdaten.gesamtflaeche > 0 && 
               objektdaten.abrechnungszeitraumStart && objektdaten.abrechnungszeitraumEnde;
      case 2:
        return mieter.length > 0 && mieter.every(m => m.name && m.flaeche > 0);
      case 3:
        return kostenpositionen.some(k => k.gesamtbetrag > 0);
      case 4:
        // CO2-Daten sind optional, aber wenn Heizkosten vorhanden, sollten CO2-Daten eingegeben werden
        return true; // CO2-Step ist optional
      default:
        return true;
    }
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
              {loadingKiErklaerung ? (
                <div className="flex flex-col items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500 mb-4"></div>
                  <p className="text-gray-400">KI analysiert...</p>
                </div>
              ) : (
                <div className="prose prose-invert max-w-none">
                  <div className="whitespace-pre-wrap text-gray-300 leading-relaxed">{kiErklaerung}</div>
                </div>
              )}
            </div>
            <div className="p-4 border-t border-gray-700 bg-gray-800/50 flex justify-between items-center">
              <p className="text-xs text-gray-500">Powered by Domulex KI • Keine Rechtsberatung</p>
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
      <header className="bg-gray-900/80 backdrop-blur-xl border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-4">
            <div className="flex items-center gap-2 sm:gap-4">
              <Link href="/dashboard" className="text-gray-400 hover:text-white transition-colors text-sm sm:text-base">
                ← <span className="hidden sm:inline">Dashboard</span>
              </Link>
              <div className="h-6 w-px bg-gray-700 hidden sm:block" />
              <h1 className="text-base sm:text-xl font-bold text-white flex items-center gap-1 sm:gap-2">
                <span className="text-lg sm:text-2xl">📊</span> <span className="hidden xs:inline">KI-</span>Nebenkostenabr.
              </h1>
            </div>
            <div className="flex items-center gap-2 sm:gap-3">
              {user && gespeicherteObjekte.length > 0 && (
                <button
                  onClick={() => setShowObjektUebersicht(!showObjektUebersicht)}
                  className={`px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                    showObjektUebersicht ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  📋 <span className="hidden sm:inline">Alle </span>Objekte ({gespeicherteObjekte.length})
                </button>
              )}
              <span className="px-2 sm:px-3 py-1 bg-orange-500/20 text-orange-400 text-xs font-medium rounded-full hidden sm:inline-flex">
                VERMIETER
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* NEU: Objektübersicht mit Fristen (Verwalter-View) */}
      {showObjektUebersicht && user && (
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <span>📋</span> Objektübersicht & Abrechnungsfristen
              </h2>
              <button
                onClick={() => setShowObjektUebersicht(false)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>
            
            {/* Fristen-Statistik */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
              <div className="bg-green-900/20 rounded-lg p-3 border border-green-700/30">
                <p className="text-xs text-green-400 mb-1">✅ Im Zeitplan</p>
                <p className="text-xl font-bold text-green-400">
                  {gespeicherteObjekte.filter(() => {
                    const frist = berechneFrist(`${new Date().getFullYear() - 1}-12-31`);
                    return frist.status === 'ok';
                  }).length}
                </p>
              </div>
              <div className="bg-yellow-900/20 rounded-lg p-3 border border-yellow-700/30">
                <p className="text-xs text-yellow-400 mb-1">⚠️ Bald fällig</p>
                <p className="text-xl font-bold text-yellow-400">
                  {gespeicherteObjekte.filter(() => {
                    const frist = berechneFrist(`${new Date().getFullYear() - 1}-12-31`);
                    return frist.status === 'warnung';
                  }).length}
                </p>
              </div>
              <div className="bg-red-900/20 rounded-lg p-3 border border-red-700/30">
                <p className="text-xs text-red-400 mb-1">🚨 Kritisch</p>
                <p className="text-xl font-bold text-red-400">
                  {gespeicherteObjekte.filter(() => {
                    const frist = berechneFrist(`${new Date().getFullYear() - 1}-12-31`);
                    return frist.status === 'kritisch';
                  }).length}
                </p>
              </div>
              <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                <p className="text-xs text-gray-400 mb-1">📊 Gesamt</p>
                <p className="text-xl font-bold text-white">{gespeicherteObjekte.length}</p>
              </div>
            </div>

            {/* Objektliste */}
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {gespeicherteObjekte.map((objekt) => {
                const abrechnungsende = `${new Date().getFullYear() - 1}-12-31`;
                const frist = berechneFrist(abrechnungsende);
                const statusColors = {
                  ok: 'border-green-700/30 bg-green-900/10',
                  warnung: 'border-yellow-700/30 bg-yellow-900/10',
                  kritisch: 'border-red-700/30 bg-red-900/10',
                  ueberschritten: 'border-red-700 bg-red-900/20'
                };
                const statusText = {
                  ok: { icon: '✅', text: `${frist.tageVerbleibend} Tage Zeit`, color: 'text-green-400' },
                  warnung: { icon: '⚠️', text: `Nur noch ${frist.tageVerbleibend} Tage!`, color: 'text-yellow-400' },
                  kritisch: { icon: '🚨', text: `NUR ${frist.tageVerbleibend} TAGE!`, color: 'text-red-400' },
                  ueberschritten: { icon: '❌', text: `${Math.abs(frist.tageVerbleibend)} Tage überschritten!`, color: 'text-red-500' }
                };
                
                return (
                  <div
                    key={objekt.id}
                    className={`flex items-center justify-between p-3 rounded-lg border ${statusColors[frist.status]}`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">🏢</span>
                      <div>
                        <p className="font-medium text-white">{objekt.adresse}</p>
                        <p className="text-xs text-gray-400">{objekt.plz} {objekt.ort} • {objekt.mieter?.length || 0} Mieter</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <p className={`text-sm font-medium ${statusText[frist.status].color}`}>
                          {statusText[frist.status].icon} {statusText[frist.status].text}
                        </p>
                        <p className="text-xs text-gray-500">Frist: {frist.frist.toLocaleDateString('de-DE')}</p>
                      </div>
                      <button
                        onClick={() => {
                          loadObjektDaten(objekt);
                          setShowObjektUebersicht(false);
                        }}
                        className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium"
                      >
                        Abrechnung →
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="mt-3 pt-3 border-t border-gray-700 text-xs text-gray-500">
              ℹ️ Nach § 556 Abs. 3 BGB muss die Nebenkostenabrechnung innerhalb von 12 Monaten nach Ende des Abrechnungszeitraums zugestellt werden.
            </div>
          </div>
        </div>
      )}

      {/* Progress */}
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="flex items-center justify-between mb-8 overflow-x-auto">
          {[
            { step: 1, label: 'Objekt', icon: '🏠' },
            { step: 2, label: 'Mieter', icon: '👥' },
            { step: 3, label: 'Kosten', icon: '💰' },
            { step: 4, label: 'CO₂', icon: '🌱' },
            { step: 5, label: 'Ergebnis', icon: '✅' },
          ].map((s, i) => (
            <div key={s.step} className="flex items-center">
              <button
                onClick={() => s.step < currentStep && setCurrentStep(s.step)}
                disabled={s.step > currentStep}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-all ${
                  currentStep === s.step
                    ? 'bg-blue-600 text-white'
                    : s.step < currentStep
                    ? 'bg-green-600/20 text-green-400 hover:bg-green-600/30 cursor-pointer'
                    : 'bg-gray-800/50 text-gray-500 cursor-not-allowed'
                }`}
              >
                <span className="text-lg">{s.step < currentStep ? '✓' : s.icon}</span>
                <span className="hidden md:inline font-medium text-sm">{s.label}</span>
              </button>
              {i < 4 && <div className={`w-8 h-1 mx-1 rounded ${s.step < currentStep ? 'bg-green-500' : 'bg-gray-700'}`} />}
            </div>
          ))}
        </div>

        {/* Content */}
        <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800 p-6 md:p-8">
          {currentStep === 1 && renderStep1()}
          {currentStep === 2 && renderStep2()}
          {currentStep === 3 && renderStep3()}
          {currentStep === 4 && renderStep4()}
          {currentStep === 5 && renderStep5()}

          {/* Navigation */}
          {currentStep < 5 && (
            <div className="flex justify-between mt-8 pt-6 border-t border-gray-800">
              <button
                onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
                disabled={currentStep === 1}
                className="px-6 py-3 text-gray-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                ← Dashboard
              </button>
              {currentStep < 4 ? (
                <button
                  onClick={() => setCurrentStep(currentStep + 1)}
                  disabled={!canProceed()}
                  className="px-8 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
                >
                  Weiter →
                </button>
              ) : (
                <button
                  onClick={() => hasAccess ? generiereAbrechnung() : zeigeDemoAbrechnung()}
                  disabled={isGenerating}
                  className="px-8 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all flex items-center gap-2"
                >
                  {isGenerating ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Generiere...
                    </>
                  ) : (
                    <>
                      <span>🤖</span> KI-Abrechnung erstellen
                    </>
                  )}
                </button>
              )}
            </div>
          )}

          {currentStep === 5 && (
            <div className="flex justify-center mt-8 pt-6 border-t border-gray-800">
              <button
                onClick={() => {
                  setCurrentStep(1);
                  setErgebnisse([]);
                  setKiAnalyse('');
                  setEnergiedaten({
                    heizungstyp: 'gas',
                    jahresverbrauchKwh: 0,
                    co2KostenGesamt: 0,
                    brennstoffkosten: 0,
                    energieausweis: '',
                  });
                }}
                className="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                Neue Abrechnung erstellen
              </button>
            </div>
          )}
        </div>

        {/* Rechtliche Hinweise */}
        <div className="mt-6 p-4 bg-gray-800/30 rounded-xl border border-gray-700">
          <p className="text-xs text-gray-500 text-center">
            <strong>Hinweis:</strong> Diese KI-Abrechnung ersetzt keine professionelle Prüfung. 
            Gemäß § 556 BGB muss die Abrechnung den formellen Anforderungen entsprechen. 
            Die CO₂-Kostenaufteilung erfolgt nach dem CO2KostAufG (seit 2023 in Kraft).
            Bei Zweifelsfragen konsultieren Sie einen Rechtsanwalt.
          </p>
        </div>
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        feature="Nebenkostenabrechnung"
        requiredTier="professional"
      />
    </div>
  );
}
