'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, getDocs, addDoc, deleteDoc, doc, updateDoc, getDoc } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import UpgradeModal from '@/components/UpgradeModal';
import { hasTierAccess } from '@/lib/tierUtils';

// Typen
interface Mieter {
  id: string;
  name: string;
  einheit: string;
  flaeche: number;
  personenanzahl: number;
  einzugsdatum: string;
  auszugsdatum?: string;
  email?: string;
  telefon?: string;
  vorauszahlung: number;
  // NEU: Mietdetails
  kaltmiete?: number;
  nebenkosten?: number;
  kaution?: number;
  kautionBezahlt?: boolean;
  vertragsbeginn?: string;
  vertragsende?: string;
  kuendigungsfrist?: number; // Monate
  mietrueckstaende?: number;
}

// NEU: Eigentümer Interface (für WEG)
interface Eigentuemer {
  id: string;
  name: string;
  einheitNr: string;
  email?: string;
  telefon?: string;
  adresse?: string; // Korrespondenzadresse falls abweichend
  miteigentumsanteil: number; // MEA in 1/1000
  stimmrecht?: number;
  sondereigentum?: string; // z.B. "Wohnung Nr. 3, Keller K3, Stellplatz 5"
  hausgeld: number; // monatliches Hausgeld
  hausgeldRueckstand?: number;
  istSelbstnutzer: boolean;
  mieter?: string; // Name des Mieters falls vermietet
}

// NEU: Einheit Interface (Wohnung/Gewerbe)
interface Einheit {
  id: string;
  nummer: string; // z.B. "EG links", "1.OG rechts", "WE 3"
  typ: 'wohnung' | 'gewerbe' | 'stellplatz' | 'keller' | 'sonstiges';
  flaeche: number;
  zimmer?: number;
  etage?: string;
  // Für Mietverwaltung
  mieterId?: string;
  // Für WEG
  eigentuemerId?: string;
  miteigentumsanteil?: number;
}

// NEU: Zahlungseingang
interface Zahlung {
  id: string;
  typ: 'miete' | 'hausgeld' | 'nebenkosten' | 'kaution' | 'sonstiges';
  betrag: number;
  datum: string;
  einheitId?: string;
  mieterId?: string;
  eigentuemerId?: string;
  monat: string; // z.B. "2026-01"
  status: 'erwartet' | 'bezahlt' | 'teilweise' | 'offen' | 'mahnung';
  notizen?: string;
}

// NEU: Mahnung Interface
interface Mahnung {
  id: string;
  mieterId?: string;
  eigentuemerId?: string;
  stufe: 1 | 2 | 3; // Mahnstufe
  betrag: number;
  faelligSeit: string;
  mahnDatum: string;
  status: 'offen' | 'bezahlt' | 'inkasso';
  notizen?: string;
}

// NEU: Zählerstand Interface
interface Zaehlerstand {
  id: string;
  zaehlerId: string;
  zaehlerTyp: 'strom' | 'gas' | 'wasser_kalt' | 'wasser_warm' | 'heizung';
  zaehlerNummer?: string;
  einheitId?: string;
  stand: number;
  datum: string;
  ablesender?: string;
}

// NEU: Handwerker/Dienstleister Interface
interface Handwerker {
  id: string;
  firma: string;
  ansprechpartner?: string;
  kategorie: 'sanitaer' | 'elektro' | 'heizung' | 'dach' | 'maler' | 'garten' | 'reinigung' | 'schluesseldienst' | 'sonstiges';
  telefon: string;
  email?: string;
  adresse?: string;
  notizen?: string;
  bewertung?: 1 | 2 | 3 | 4 | 5;
  letzterEinsatz?: string;
}

// NEU: Beschluss Interface (WEG)
interface Beschluss {
  id: string;
  topNummer: number;
  datum: string;
  versammlungId?: string;
  titel: string;
  beschreibung: string;
  ergebnis: 'angenommen' | 'abgelehnt' | 'vertagt' | 'einstimmig';
  jaStimmen?: number;
  neinStimmen?: number;
  enthaltungen?: number;
  umsetzungsfrist?: string;
  umgesetzt: boolean;
}

// NEU: Wartungstermin Interface
interface Wartungstermin {
  id: string;
  bezeichnung: string;
  typ: 'wartung' | 'pruefung' | 'reparatur' | 'sonstiges';
  faelligkeitsdatum: string;
  intervallMonate?: number;
  kosten?: number;
  erledigt: boolean;
  notizen?: string;
}

// NEU: Dokument Interface
interface Dokument {
  id: string;
  name: string;
  typ: 'mietvertrag' | 'protokoll' | 'rechnung' | 'versicherung' | 'sonstiges';
  datum: string;
  notizen?: string;
}

interface Objekt {
  id: string;
  adresse: string;
  plz: string;
  ort: string;
  gesamtflaeche: number;
  gesamteinheiten: number;
  baujahr?: number;
  heizungstyp: string;
  energieausweis?: string;
  typ: 'mfh' | 'efh' | 'weg' | 'gewerbe';
  mieter: Mieter[];
  wartungstermine?: Wartungstermin[];
  dokumente?: Dokument[];
  createdAt: Date;
  updatedAt?: Date;
  notizen?: string;
  // NEU: Finanzdaten
  kaufpreis?: number;
  kreditrate?: number;
  // NEU: Einheiten & WEG
  einheiten?: Einheit[];
  eigentuemer?: Eigentuemer[];
  zahlungen?: Zahlung[];
  mahnungen?: Mahnung[];
  zaehlerstaende?: Zaehlerstand[];
  beschluesse?: Beschluss[];
  // WEG-spezifisch
  wegName?: string;
  verwalterSeit?: string;
  wirtschaftsjahr?: string; // z.B. "01.01. - 31.12."
  instandhaltungsruecklage?: number;
  hausgeldGesamt?: number;
}

const HEIZUNGSTYPEN = [
  { id: 'gas', label: 'Erdgas' },
  { id: 'oel', label: 'Heizöl' },
  { id: 'fernwaerme', label: 'Fernwärme' },
  { id: 'waermepumpe', label: 'Wärmepumpe' },
  { id: 'pellets', label: 'Holzpellets' },
];

const OBJEKT_TYPEN = [
  { id: 'mfh', label: 'Mehrfamilienhaus', icon: '🏢' },
  { id: 'efh', label: 'Einfamilienhaus', icon: '🏠' },
  { id: 'weg', label: 'WEG', icon: '🏘️' },
  { id: 'gewerbe', label: 'Gewerbe', icon: '🏪' },
];

type SortOption = 'name' | 'mieter' | 'flaeche' | 'einnahmen';

// Wartungstypen
const WARTUNGS_TYPEN = [
  { id: 'wartung', label: 'Wartung', icon: '🔧' },
  { id: 'pruefung', label: 'Prüfung', icon: '✅' },
  { id: 'reparatur', label: 'Reparatur', icon: '🛠️' },
  { id: 'sonstiges', label: 'Sonstiges', icon: '📋' },
];

// NEU: Handwerker-Kategorien
const HANDWERKER_KATEGORIEN = [
  { id: 'sanitaer', label: 'Sanitär/Klempner', icon: '🚿' },
  { id: 'elektro', label: 'Elektriker', icon: '⚡' },
  { id: 'heizung', label: 'Heizung/Klima', icon: '🔥' },
  { id: 'dach', label: 'Dachdecker', icon: '🏠' },
  { id: 'maler', label: 'Maler/Lackierer', icon: '🎨' },
  { id: 'garten', label: 'Garten/Außen', icon: '🌳' },
  { id: 'reinigung', label: 'Reinigung', icon: '🧹' },
  { id: 'schluesseldienst', label: 'Schlüsseldienst', icon: '🔑' },
  { id: 'sonstiges', label: 'Sonstiges', icon: '🔧' },
];

// NEU: Zählertypen
const ZAEHLER_TYPEN = [
  { id: 'strom' as const, label: 'Strom', icon: '⚡', einheit: 'kWh' },
  { id: 'gas' as const, label: 'Gas', icon: '🔥', einheit: 'm³' },
  { id: 'wasser_kalt' as const, label: 'Kaltwasser', icon: '💧', einheit: 'm³' },
  { id: 'wasser_warm' as const, label: 'Warmwasser', icon: '🚿', einheit: 'm³' },
  { id: 'heizung' as const, label: 'Heizung', icon: '🌡️', einheit: 'kWh' },
];

// ===== DEMO-DATEN FÜR FREE-NUTZER (sofort sichtbar) =====
const DEMO_OBJEKTE: Objekt[] = [
  {
    id: 'demo-mfh',
    adresse: 'Musterstraße 15',
    plz: '10115',
    ort: 'Berlin',
    gesamtflaeche: 450,
    gesamteinheiten: 6,
    baujahr: 1998,
    heizungstyp: 'gas',
    typ: 'mfh',
    kaufpreis: 850000,
    kreditrate: 2450,
    notizen: '📋 Demo-Objekt zur Demonstration der Funktionen.',
    createdAt: new Date(),
    einheiten: [
      { id: 'e1', nummer: 'EG links', typ: 'wohnung', flaeche: 65, zimmer: 2, etage: 'EG' },
      { id: 'e2', nummer: 'EG rechts', typ: 'wohnung', flaeche: 72, zimmer: 3, etage: 'EG' },
      { id: 'e3', nummer: '1.OG links', typ: 'wohnung', flaeche: 65, zimmer: 2, etage: '1.OG' },
      { id: 'e4', nummer: '1.OG rechts', typ: 'wohnung', flaeche: 72, zimmer: 3, etage: '1.OG' },
      { id: 'e5', nummer: '2.OG links', typ: 'wohnung', flaeche: 88, zimmer: 4, etage: '2.OG' },
      { id: 'e6', nummer: '2.OG rechts', typ: 'wohnung', flaeche: 88, zimmer: 4, etage: '2.OG' },
    ],
    mieter: [
      { id: 'm1', name: 'Schmidt, Maria', einheit: 'EG links', flaeche: 65, personenanzahl: 1, einzugsdatum: '2022-03-01', email: 'maria.schmidt@email.de', telefon: '030-12345678', vorauszahlung: 250, kaltmiete: 650, nebenkosten: 250, kaution: 1950, kautionBezahlt: true, kuendigungsfrist: 3 },
      { id: 'm2', name: 'Müller, Hans & Eva', einheit: 'EG rechts', flaeche: 72, personenanzahl: 2, einzugsdatum: '2020-07-15', email: 'mueller.familie@email.de', telefon: '030-23456789', vorauszahlung: 280, kaltmiete: 720, nebenkosten: 280, kaution: 2160, kautionBezahlt: true, kuendigungsfrist: 3 },
      { id: 'm3', name: 'Weber, Thomas', einheit: '1.OG links', flaeche: 65, personenanzahl: 1, einzugsdatum: '2023-01-01', email: 'thomas.weber@email.de', telefon: '030-34567890', vorauszahlung: 250, kaltmiete: 680, nebenkosten: 250, kaution: 2040, kautionBezahlt: true, kuendigungsfrist: 3 },
      { id: 'm4', name: 'Fischer, Familie', einheit: '1.OG rechts', flaeche: 72, personenanzahl: 4, einzugsdatum: '2019-04-01', email: 'fischer@email.de', telefon: '030-45678901', vorauszahlung: 290, kaltmiete: 750, nebenkosten: 290, kaution: 2250, kautionBezahlt: true, kuendigungsfrist: 3, mietrueckstaende: 290 },
      { id: 'm5', name: 'Hoffmann, Petra', einheit: '2.OG links', flaeche: 88, personenanzahl: 2, einzugsdatum: '2021-09-01', email: 'p.hoffmann@email.de', telefon: '030-56789012', vorauszahlung: 340, kaltmiete: 920, nebenkosten: 340, kaution: 2760, kautionBezahlt: true, kuendigungsfrist: 3 },
    ],
    wartungstermine: [
      { id: 'w1', bezeichnung: 'Heizungswartung', typ: 'wartung', faelligkeitsdatum: '2026-01-08', intervallMonate: 12, kosten: 350, erledigt: false },
      { id: 'w2', bezeichnung: 'Schornsteinfeger', typ: 'pruefung', faelligkeitsdatum: '2026-01-12', intervallMonate: 12, kosten: 80, erledigt: false },
      { id: 'w3', bezeichnung: 'Rauchwarnmelder prüfen', typ: 'pruefung', faelligkeitsdatum: '2026-01-20', intervallMonate: 12, kosten: 150, erledigt: false },
      { id: 'w4', bezeichnung: 'Wasserzähler ablesen', typ: 'wartung', faelligkeitsdatum: '2026-01-03', intervallMonate: 12, kosten: 0, erledigt: false },
    ],
    zaehlerstaende: [
      { id: 'z1', zaehlerId: 'strom-haus', zaehlerTyp: 'strom', zaehlerNummer: 'S-2024-001', stand: 45230, datum: '2025-12-31', ablesender: 'Hausverwaltung' },
      { id: 'z2', zaehlerId: 'gas-haus', zaehlerTyp: 'gas', zaehlerNummer: 'G-2024-001', stand: 12450, datum: '2025-12-31', ablesender: 'Hausverwaltung' },
    ],
  },
  {
    id: 'demo-weg',
    adresse: 'Eigentümerweg 42',
    plz: '80333',
    ort: 'München',
    gesamtflaeche: 520,
    gesamteinheiten: 8,
    baujahr: 2005,
    heizungstyp: 'fernwaerme',
    typ: 'weg',
    wegName: 'WEG Eigentümerweg 42',
    verwalterSeit: '2024-01-01',
    wirtschaftsjahr: '01.01. - 31.12.',
    instandhaltungsruecklage: 125000,
    hausgeldGesamt: 3200,
    notizen: '📋 Demo-WEG zur Demonstration der Eigentümerverwaltung.',
    createdAt: new Date(),
    einheiten: [
      { id: 'we1', nummer: 'WE 1', typ: 'wohnung', flaeche: 55, zimmer: 2, etage: 'EG', miteigentumsanteil: 110 },
      { id: 'we2', nummer: 'WE 2', typ: 'wohnung', flaeche: 72, zimmer: 3, etage: 'EG', miteigentumsanteil: 144 },
      { id: 'we3', nummer: 'WE 3', typ: 'wohnung', flaeche: 55, zimmer: 2, etage: '1.OG', miteigentumsanteil: 110 },
      { id: 'we4', nummer: 'WE 4', typ: 'wohnung', flaeche: 72, zimmer: 3, etage: '1.OG', miteigentumsanteil: 144 },
    ],
    eigentuemer: [
      { id: 'eig1', name: 'Bauer, Friedrich', einheitNr: 'WE 1', email: 'f.bauer@email.de', telefon: '089-11111111', miteigentumsanteil: 110, stimmrecht: 1, sondereigentum: 'Wohnung Nr. 1, Keller K1', hausgeld: 350, istSelbstnutzer: true },
      { id: 'eig2', name: 'Schneider, Ingrid', einheitNr: 'WE 2', email: 'i.schneider@email.de', telefon: '089-22222222', miteigentumsanteil: 144, stimmrecht: 1, sondereigentum: 'Wohnung Nr. 2, Keller K2', hausgeld: 420, istSelbstnutzer: false, mieter: 'Klein, Michael' },
      { id: 'eig3', name: 'Koch, Werner & Helga', einheitNr: 'WE 3', email: 'koch.we@email.de', telefon: '089-33333333', miteigentumsanteil: 110, stimmrecht: 1, sondereigentum: 'Wohnung Nr. 3, Keller K3', hausgeld: 350, istSelbstnutzer: true },
      { id: 'eig4', name: 'Wagner Immobilien GmbH', einheitNr: 'WE 4', email: 'verwaltung@wagner-immo.de', telefon: '089-44444444', miteigentumsanteil: 144, stimmrecht: 1, sondereigentum: 'Wohnung Nr. 4, Keller K4', hausgeld: 480, hausgeldRueckstand: 960, istSelbstnutzer: false, mieter: 'Braun, Familie' },
    ],
    mieter: [],
    wartungstermine: [
      { id: 'ww1', bezeichnung: 'Aufzug TÜV-Prüfung', typ: 'pruefung', faelligkeitsdatum: '2026-01-15', intervallMonate: 24, kosten: 450, erledigt: false },
      { id: 'ww2', bezeichnung: 'Tiefgarage Wartung', typ: 'wartung', faelligkeitsdatum: '2026-01-25', intervallMonate: 12, kosten: 280, erledigt: false },
      { id: 'ww3', bezeichnung: 'Treppenhausreinigung', typ: 'wartung', faelligkeitsdatum: '2026-01-02', intervallMonate: 1, kosten: 120, erledigt: false },
    ],
    beschluesse: [
      { id: 'b1', topNummer: 1, datum: '2025-06-15', titel: 'Instandhaltungsrücklage erhöhen', beschreibung: 'Erhöhung der monatlichen Rücklage um 50€ pro WE ab 01.01.2026', ergebnis: 'angenommen', jaStimmen: 5, neinStimmen: 1, enthaltungen: 0, umsetzungsfrist: '2026-01-01', umgesetzt: true },
      { id: 'b2', topNummer: 2, datum: '2025-06-15', titel: 'Fassadensanierung 2026', beschreibung: 'Beauftragung für Fassadensanierung, Kosten ca. 85.000€', ergebnis: 'angenommen', jaStimmen: 6, neinStimmen: 0, enthaltungen: 0, umsetzungsfrist: '2026-04-01', umgesetzt: false },
    ],
  },
];

const DEMO_HANDWERKER: Handwerker[] = [
  { id: 'hw1', firma: 'Sanitär Schmidt GmbH', ansprechpartner: 'Peter Schmidt', kategorie: 'sanitaer', telefon: '030-88776655', email: 'info@sanitaer-schmidt.de', adresse: 'Klempnerweg 5, 10115 Berlin', notizen: '24h Notdienst verfügbar', bewertung: 5 },
  { id: 'hw2', firma: 'Elektro Blitz', ansprechpartner: 'Michael Blitz', kategorie: 'elektro', telefon: '030-99887766', email: 'blitz@elektro-blitz.de', adresse: 'Stromstraße 12, 10117 Berlin', notizen: 'Spezialisiert auf Altbau', bewertung: 4 },
  { id: 'hw3', firma: 'Heizung Warm & Co', ansprechpartner: 'Thomas Warm', kategorie: 'heizung', telefon: '030-77665544', email: 'service@warm-heizung.de', adresse: 'Wärmeweg 8, 10119 Berlin', notizen: 'Gas- und Ölheizung, Wärmepumpen', bewertung: 5 },
  { id: 'hw4', firma: 'Malermeister Farbe', ansprechpartner: 'Anna Farbe', kategorie: 'maler', telefon: '030-55443322', email: 'info@maler-farbe.de', adresse: 'Farbweg 3, 10115 Berlin', bewertung: 4 },
];

export default function ObjektePage() {
  const [user, setUser] = useState<any>(null);
  const [objekte, setObjekte] = useState<Objekt[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showMieterModal, setShowMieterModal] = useState<string | null>(null);
  const [selectedObjekt, setSelectedObjekt] = useState<Objekt | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('name');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const [showWartungModal, setShowWartungModal] = useState<string | null>(null);
  const [showDetailView, setShowDetailView] = useState<string | null>(null);
  // NEU: Einheiten, Eigentümer, Zahlungen
  const [showEinheitenModal, setShowEinheitenModal] = useState<string | null>(null);
  const [showEigentuemerModal, setShowEigentuemerModal] = useState<string | null>(null);
  const [showZahlungenModal, setShowZahlungenModal] = useState<string | null>(null);
  const [activeDetailTab, setActiveDetailTab] = useState<'uebersicht' | 'einheiten' | 'mieter' | 'eigentuemer' | 'zahlungen' | 'wartung' | 'zaehler' | 'mahnungen' | 'beschluesse'>('uebersicht');
  // NEU: Mahnwesen, Zähler, Handwerker, Beschlüsse
  const [showMahnungModal, setShowMahnungModal] = useState<string | null>(null);
  const [showZaehlerModal, setShowZaehlerModal] = useState<string | null>(null);
  const [showHandwerkerModal, setShowHandwerkerModal] = useState(false);
  const [showBeschlussModal, setShowBeschlussModal] = useState<string | null>(null);
  const [handwerker, setHandwerker] = useState<Handwerker[]>([]);
  const [showMieterhoeungRechner, setShowMieterhoeungRechner] = useState(false);
  const router = useRouter();

  // Tier-Check Helper (Professional or Lawyer)
  const hasAccess = hasTierAccess(userTier, 'professional');
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  // Neues Objekt Formular
  const [newObjekt, setNewObjekt] = useState({
    adresse: '',
    plz: '',
    ort: '',
    gesamtflaeche: 0,
    gesamteinheiten: 1,
    baujahr: undefined as number | undefined,
    heizungstyp: 'gas',
    energieausweis: '',
    typ: 'mfh' as const,
    notizen: '',
  });

  // Neuer Mieter Formular
  const [newMieter, setNewMieter] = useState({
    name: '',
    einheit: '',
    flaeche: 0,
    personenanzahl: 1,
    einzugsdatum: '',
    email: '',
    telefon: '',
    vorauszahlung: 0,
  });

  // NEU: Neuer Wartungstermin Formular
  const [newWartung, setNewWartung] = useState({
    bezeichnung: '',
    typ: 'wartung' as 'wartung' | 'pruefung' | 'reparatur' | 'sonstiges',
    faelligkeitsdatum: '',
    intervallMonate: 12,
    kosten: 0,
    notizen: '',
  });

  // NEU: Neue Einheit Formular
  const [newEinheit, setNewEinheit] = useState({
    nummer: '',
    typ: 'wohnung' as Einheit['typ'],
    flaeche: 0,
    zimmer: 0,
    etage: '',
    miteigentumsanteil: 0,
  });

  // NEU: Neuer Eigentümer Formular
  const [newEigentuemer, setNewEigentuemer] = useState({
    name: '',
    einheitNr: '',
    email: '',
    telefon: '',
    adresse: '',
    miteigentumsanteil: 0,
    hausgeld: 0,
    istSelbstnutzer: true,
    mieter: '',
    sondereigentum: '',
  });

  // NEU: Neue Zahlung Formular
  const [newZahlung, setNewZahlung] = useState({
    typ: 'miete' as Zahlung['typ'],
    betrag: 0,
    datum: new Date().toISOString().split('T')[0],
    monat: new Date().toISOString().slice(0, 7),
    mieterId: '',
    eigentuemerId: '',
    notizen: '',
  });

  // NEU: Mahnung Formular
  const [newMahnung, setNewMahnung] = useState({
    mieterId: '' as string | undefined,
    eigentuemerId: '' as string | undefined,
    stufe: 1 as 1 | 2 | 3,
    betrag: 0,
    faelligSeit: new Date().toISOString().split('T')[0],
  });

  // NEU: Zählerstand Formular
  const [newZaehlerstand, setNewZaehlerstand] = useState({
    zaehlerTyp: 'strom' as Zaehlerstand['zaehlerTyp'],
    zaehlerNummer: '',
    einheitId: '' as string | undefined,
    stand: 0,
    datum: new Date().toISOString().split('T')[0],
  });

  // NEU: Handwerker Formular
  const [newHandwerker, setNewHandwerker] = useState({
    firma: '',
    ansprechpartner: '',
    kategorie: 'sanitaer' as Handwerker['kategorie'],
    telefon: '',
    email: '',
    adresse: '',
    notizen: '',
  });

  // NEU: Beschluss Formular
  const [newBeschluss, setNewBeschluss] = useState({
    topNummer: 1,
    datum: new Date().toISOString().split('T')[0],
    titel: '',
    beschreibung: '',
    ergebnis: 'angenommen' as Beschluss['ergebnis'],
    jaStimmen: 0,
    neinStimmen: 0,
    enthaltungen: 0,
  });

  // Fällige Wartungstermine berechnen (über alle Objekte)
  const getFaelligeWartungen = () => {
    const heute = new Date();
    const in30Tagen = new Date();
    in30Tagen.setDate(in30Tagen.getDate() + 30);
    
    const faellig: { objekt: Objekt; wartung: Wartungstermin }[] = [];
    objekte.forEach(objekt => {
      objekt.wartungstermine?.filter(w => !w.erledigt).forEach(wartung => {
        const datum = new Date(wartung.faelligkeitsdatum);
        if (datum <= in30Tagen) {
          faellig.push({ objekt, wartung });
        }
      });
    });
    return faellig.sort((a, b) => 
      new Date(a.wartung.faelligkeitsdatum).getTime() - new Date(b.wartung.faelligkeitsdatum).getTime()
    );
  };

  const faelligeWartungen = getFaelligeWartungen();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      setUser(currentUser);
      
      // Tier laden
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      let tier = 'free';
      if (userDoc.exists()) {
        tier = userDoc.data().tier || userDoc.data().dashboardType || 'free';
        setUserTier(tier);
      }
      
      // Für FREE-Nutzer: Demo-Daten sofort anzeigen (nicht aus DB laden)
      if (!hasTierAccess(tier, 'professional')) {
        setObjekte(DEMO_OBJEKTE);
        setHandwerker(DEMO_HANDWERKER);
        setLoading(false);
        return;
      }
      
      // Für Professional/Lawyer: Echte Daten aus Firestore
      await loadObjekte(currentUser.uid);
      await loadHandwerker(currentUser.uid);
    });

    return () => unsubscribe();
  }, [router]);

  const loadObjekte = async (userId: string) => {
    setLoading(true);
    console.log('[Objekte] Loading for user:', userId);
    try {
      // Simple query without orderBy (Firestore may need index for subcollection orderBy)
      const colRef = collection(db, 'users', userId, 'objekte');
      const snapshot = await getDocs(colRef);
      console.log('[Objekte] Loaded docs:', snapshot.size);
      const docs = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
        createdAt: doc.data().createdAt?.toDate() || new Date(),
        updatedAt: doc.data().updatedAt?.toDate(),
        mieter: doc.data().mieter || []
      })) as Objekt[];
      // Sort manually by createdAt descending
      docs.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
      console.log('[Objekte] Parsed objekte:', docs);
      setObjekte(docs);
    } catch (error) {
      console.error('[Objekte] Error loading:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddObjekt = async () => {
    if (!user || !newObjekt.adresse) return;

    try {
      const docRef = await addDoc(collection(db, 'users', user.uid, 'objekte'), {
        ...newObjekt,
        mieter: [],
        createdAt: new Date(),
      });

      const created: Objekt = {
        id: docRef.id,
        ...newObjekt,
        mieter: [],
        createdAt: new Date(),
      };

      setObjekte(prev => [created, ...prev]);
      setShowAddModal(false);
      setNewObjekt({
        adresse: '',
        plz: '',
        ort: '',
        gesamtflaeche: 0,
        gesamteinheiten: 1,
        baujahr: undefined,
        heizungstyp: 'gas',
        energieausweis: '',
        typ: 'mfh',
        notizen: '',
      });
    } catch (error) {
      console.error('Error adding objekt:', error);
    }
  };

  const handleAddMieter = async (objektId: string) => {
    if (!user || !newMieter.name) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const mieterId = `mieter-${Date.now()}`;
    const updatedMieter = [...objekt.mieter, { ...newMieter, id: mieterId }];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        mieter: updatedMieter,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, mieter: updatedMieter, updatedAt: new Date() } : o
      ));

      setShowMieterModal(null);
      setNewMieter({
        name: '',
        einheit: '',
        flaeche: 0,
        personenanzahl: 1,
        einzugsdatum: '',
        email: '',
        telefon: '',
        vorauszahlung: 0,
      });
    } catch (error) {
      console.error('Error adding mieter:', error);
    }
  };

  const handleDeleteObjekt = async (objektId: string) => {
    if (!user) return;

    try {
      await deleteDoc(doc(db, 'users', user.uid, 'objekte', objektId));
      setObjekte(prev => prev.filter(o => o.id !== objektId));
    } catch (error) {
      console.error('Error deleting objekt:', error);
    }
  };

  const handleDeleteMieter = async (objektId: string, mieterId: string) => {
    if (!user) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const updatedMieter = objekt.mieter.filter(m => m.id !== mieterId);

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        mieter: updatedMieter,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, mieter: updatedMieter, updatedAt: new Date() } : o
      ));
    } catch (error) {
      console.error('Error deleting mieter:', error);
    }
  };

  // NEU: Wartungstermin hinzufügen
  const handleAddWartung = async (objektId: string) => {
    if (!user || !newWartung.bezeichnung || !newWartung.faelligkeitsdatum) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const wartungId = `wartung-${Date.now()}`;
    const neueWartung: Wartungstermin = {
      id: wartungId,
      bezeichnung: newWartung.bezeichnung,
      typ: newWartung.typ,
      faelligkeitsdatum: newWartung.faelligkeitsdatum,
      intervallMonate: newWartung.intervallMonate,
      kosten: newWartung.kosten,
      erledigt: false,
      notizen: newWartung.notizen,
    };
    const updatedWartungen = [...(objekt.wartungstermine || []), neueWartung];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        wartungstermine: updatedWartungen,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, wartungstermine: updatedWartungen, updatedAt: new Date() } : o
      ));

      setShowWartungModal(null);
      setNewWartung({
        bezeichnung: '',
        typ: 'wartung',
        faelligkeitsdatum: '',
        intervallMonate: 12,
        kosten: 0,
        notizen: '',
      });
    } catch (error) {
      console.error('Error adding wartung:', error);
    }
  };

  // NEU: Wartungstermin als erledigt markieren
  const handleToggleWartung = async (objektId: string, wartungId: string) => {
    if (!user) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const updatedWartungen = objekt.wartungstermine?.map(w => {
      if (w.id === wartungId) {
        // Wenn erledigt: Neuen Termin mit Intervall erstellen (falls vorhanden)
        if (!w.erledigt && w.intervallMonate) {
          const naechstesDatum = new Date(w.faelligkeitsdatum);
          naechstesDatum.setMonth(naechstesDatum.getMonth() + w.intervallMonate);
          return { ...w, erledigt: true, faelligkeitsdatum: naechstesDatum.toISOString().split('T')[0] };
        }
        return { ...w, erledigt: !w.erledigt };
      }
      return w;
    }) || [];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        wartungstermine: updatedWartungen,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, wartungstermine: updatedWartungen, updatedAt: new Date() } : o
      ));
    } catch (error) {
      console.error('Error toggling wartung:', error);
    }
  };

  // NEU: Wartungstermin löschen
  const handleDeleteWartung = async (objektId: string, wartungId: string) => {
    if (!user) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const updatedWartungen = objekt.wartungstermine?.filter(w => w.id !== wartungId) || [];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        wartungstermine: updatedWartungen,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, wartungstermine: updatedWartungen, updatedAt: new Date() } : o
      ));
    } catch (error) {
      console.error('Error deleting wartung:', error);
    }
  };

  // NEU: Einheit hinzufügen
  const handleAddEinheit = async (objektId: string) => {
    if (!user || !newEinheit.nummer) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const einheitId = `einheit-${Date.now()}`;
    const neueEinheit: Einheit = {
      id: einheitId,
      nummer: newEinheit.nummer,
      typ: newEinheit.typ,
      flaeche: newEinheit.flaeche,
      zimmer: newEinheit.zimmer,
      etage: newEinheit.etage,
      miteigentumsanteil: newEinheit.miteigentumsanteil,
    };
    const updatedEinheiten = [...(objekt.einheiten || []), neueEinheit];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        einheiten: updatedEinheiten,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, einheiten: updatedEinheiten, updatedAt: new Date() } : o
      ));

      setNewEinheit({ nummer: '', typ: 'wohnung', flaeche: 0, zimmer: 0, etage: '', miteigentumsanteil: 0 });
    } catch (error) {
      console.error('Error adding einheit:', error);
    }
  };

  // NEU: Eigentümer hinzufügen
  const handleAddEigentuemer = async (objektId: string) => {
    if (!user || !newEigentuemer.name) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const eigentuemerId = `eigentuemer-${Date.now()}`;
    const neuerEigentuemer: Eigentuemer = {
      id: eigentuemerId,
      name: newEigentuemer.name,
      einheitNr: newEigentuemer.einheitNr,
      email: newEigentuemer.email,
      telefon: newEigentuemer.telefon,
      adresse: newEigentuemer.adresse,
      miteigentumsanteil: newEigentuemer.miteigentumsanteil,
      hausgeld: newEigentuemer.hausgeld,
      istSelbstnutzer: newEigentuemer.istSelbstnutzer,
      mieter: newEigentuemer.mieter,
      sondereigentum: newEigentuemer.sondereigentum,
    };
    const updatedEigentuemer = [...(objekt.eigentuemer || []), neuerEigentuemer];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        eigentuemer: updatedEigentuemer,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, eigentuemer: updatedEigentuemer, updatedAt: new Date() } : o
      ));

      setNewEigentuemer({ name: '', einheitNr: '', email: '', telefon: '', adresse: '', miteigentumsanteil: 0, hausgeld: 0, istSelbstnutzer: true, mieter: '', sondereigentum: '' });
      setShowEigentuemerModal(null);
    } catch (error) {
      console.error('Error adding eigentuemer:', error);
    }
  };

  // NEU: Eigentümer löschen
  const handleDeleteEigentuemer = async (objektId: string, eigentuemerId: string) => {
    if (!user) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const updatedEigentuemer = objekt.eigentuemer?.filter(e => e.id !== eigentuemerId) || [];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        eigentuemer: updatedEigentuemer,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, eigentuemer: updatedEigentuemer, updatedAt: new Date() } : o
      ));
    } catch (error) {
      console.error('Error deleting eigentuemer:', error);
    }
  };

  // NEU: Zahlung hinzufügen
  const handleAddZahlung = async (objektId: string) => {
    if (!user || !newZahlung.betrag) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const zahlungId = `zahlung-${Date.now()}`;
    const neueZahlung: Zahlung = {
      id: zahlungId,
      typ: newZahlung.typ,
      betrag: newZahlung.betrag,
      datum: newZahlung.datum,
      monat: newZahlung.monat,
      mieterId: newZahlung.mieterId,
      eigentuemerId: newZahlung.eigentuemerId,
      status: 'bezahlt',
      notizen: newZahlung.notizen,
    };
    const updatedZahlungen = [...(objekt.zahlungen || []), neueZahlung];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        zahlungen: updatedZahlungen,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, zahlungen: updatedZahlungen, updatedAt: new Date() } : o
      ));

      setNewZahlung({ typ: 'miete', betrag: 0, datum: new Date().toISOString().split('T')[0], monat: new Date().toISOString().slice(0, 7), mieterId: '', eigentuemerId: '', notizen: '' });
      setShowZahlungenModal(null);
    } catch (error) {
      console.error('Error adding zahlung:', error);
    }
  };

  // Berechnung: Offene Zahlungen / Rückstände
  const getZahlungsrueckstaende = () => {
    let mietrueckstand = 0;
    let hausgeldrueckstand = 0;
    
    objekte.forEach(objekt => {
      // Mietrückstände
      objekt.mieter?.forEach(m => {
        mietrueckstand += m.mietrueckstaende || 0;
      });
      // Hausgeldrückstände (WEG)
      objekt.eigentuemer?.forEach(e => {
        hausgeldrueckstand += e.hausgeldRueckstand || 0;
      });
    });
    
    return { mietrueckstand, hausgeldrueckstand, gesamt: mietrueckstand + hausgeldrueckstand };
  };

  const rueckstaende = getZahlungsrueckstaende();

  // NEU: Mahnung erstellen
  const handleAddMahnung = async (objektId: string) => {
    if (!user || !newMahnung.betrag) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const mahnungId = `mahnung-${Date.now()}`;
    const neueMahnung: Mahnung = {
      id: mahnungId,
      mieterId: newMahnung.mieterId,
      eigentuemerId: newMahnung.eigentuemerId,
      stufe: newMahnung.stufe,
      betrag: newMahnung.betrag,
      faelligSeit: newMahnung.faelligSeit,
      mahnDatum: new Date().toISOString().split('T')[0],
      status: 'offen',
    };
    const updatedMahnungen = [...(objekt.mahnungen || []), neueMahnung];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        mahnungen: updatedMahnungen,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, mahnungen: updatedMahnungen, updatedAt: new Date() } : o
      ));

      setNewMahnung({ mieterId: '', eigentuemerId: '', stufe: 1, betrag: 0, faelligSeit: '' });
      setShowMahnungModal(null);
    } catch (error) {
      console.error('Error adding mahnung:', error);
    }
  };

  // NEU: Mahnung als bezahlt markieren
  const handleMahnungBezahlt = async (objektId: string, mahnungId: string) => {
    if (!user) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const updatedMahnungen = objekt.mahnungen?.map(m =>
      m.id === mahnungId ? { ...m, status: 'bezahlt' as const } : m
    ) || [];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        mahnungen: updatedMahnungen,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, mahnungen: updatedMahnungen, updatedAt: new Date() } : o
      ));
    } catch (error) {
      console.error('Error updating mahnung:', error);
    }
  };

  // NEU: Zählerstand erfassen
  const handleAddZaehlerstand = async (objektId: string) => {
    if (!user || !newZaehlerstand.stand) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const zaehlerstandId = `zaehler-${Date.now()}`;
    const neuerZaehlerstand: Zaehlerstand = {
      id: zaehlerstandId,
      zaehlerId: `${newZaehlerstand.zaehlerTyp}-${newZaehlerstand.einheitId || 'allgemein'}`,
      zaehlerTyp: newZaehlerstand.zaehlerTyp,
      zaehlerNummer: newZaehlerstand.zaehlerNummer,
      einheitId: newZaehlerstand.einheitId,
      stand: newZaehlerstand.stand,
      datum: newZaehlerstand.datum,
    };
    const updatedZaehlerstaende = [...(objekt.zaehlerstaende || []), neuerZaehlerstand];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        zaehlerstaende: updatedZaehlerstaende,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, zaehlerstaende: updatedZaehlerstaende, updatedAt: new Date() } : o
      ));

      setNewZaehlerstand({ zaehlerTyp: 'strom', zaehlerNummer: '', einheitId: '', stand: 0, datum: new Date().toISOString().split('T')[0] });
      setShowZaehlerModal(null);
    } catch (error) {
      console.error('Error adding zaehlerstand:', error);
    }
  };

  // NEU: Handwerker hinzufügen (global)
  const handleAddHandwerker = async () => {
    if (!user || !newHandwerker.firma || !newHandwerker.telefon) return;

    const handwerkerId = `handwerker-${Date.now()}`;
    const neuerHandwerker: Handwerker = {
      id: handwerkerId,
      firma: newHandwerker.firma,
      ansprechpartner: newHandwerker.ansprechpartner,
      kategorie: newHandwerker.kategorie,
      telefon: newHandwerker.telefon,
      email: newHandwerker.email,
      adresse: newHandwerker.adresse,
      notizen: newHandwerker.notizen,
    };

    try {
      await addDoc(collection(db, 'users', user.uid, 'handwerker'), neuerHandwerker);
      setHandwerker(prev => [...prev, neuerHandwerker]);

      setNewHandwerker({ firma: '', ansprechpartner: '', kategorie: 'sanitaer', telefon: '', email: '', adresse: '', notizen: '' });
      setShowHandwerkerModal(false);
    } catch (error) {
      console.error('Error adding handwerker:', error);
    }
  };

  // NEU: Handwerker laden
  const loadHandwerker = async (userId: string) => {
    try {
      const handwerkerRef = collection(db, 'users', userId, 'handwerker');
      const snapshot = await getDocs(handwerkerRef);
      const list: Handwerker[] = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as Handwerker[];
      setHandwerker(list);
    } catch (error) {
      console.error('Error loading handwerker:', error);
    }
  };

  // NEU: Beschluss hinzufügen
  const handleAddBeschluss = async (objektId: string) => {
    if (!user || !newBeschluss.titel) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const beschlussId = `beschluss-${Date.now()}`;
    const neuerBeschluss: Beschluss = {
      id: beschlussId,
      topNummer: newBeschluss.topNummer,
      datum: new Date().toISOString().split('T')[0],
      titel: newBeschluss.titel,
      beschreibung: newBeschluss.beschreibung,
      ergebnis: newBeschluss.ergebnis,
      jaStimmen: newBeschluss.jaStimmen,
      neinStimmen: newBeschluss.neinStimmen,
      enthaltungen: newBeschluss.enthaltungen,
      umgesetzt: false,
    };
    const updatedBeschluesse = [...(objekt.beschluesse || []), neuerBeschluss];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        beschluesse: updatedBeschluesse,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, beschluesse: updatedBeschluesse, updatedAt: new Date() } : o
      ));

      setNewBeschluss({ topNummer: 1, datum: new Date().toISOString().split('T')[0], titel: '', beschreibung: '', ergebnis: 'angenommen', jaStimmen: 0, neinStimmen: 0, enthaltungen: 0 });
      setShowBeschlussModal(null);
    } catch (error) {
      console.error('Error adding beschluss:', error);
    }
  };

  // NEU: Beschluss als umgesetzt markieren
  const handleBeschlussUmgesetzt = async (objektId: string, beschlussId: string) => {
    if (!user) return;

    const objekt = objekte.find(o => o.id === objektId);
    if (!objekt) return;

    const updatedBeschluesse = objekt.beschluesse?.map(b =>
      b.id === beschlussId ? { ...b, umgesetzt: !b.umgesetzt } : b
    ) || [];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'objekte', objektId), {
        beschluesse: updatedBeschluesse,
        updatedAt: new Date(),
      });

      setObjekte(prev => prev.map(o =>
        o.id === objektId ? { ...o, beschluesse: updatedBeschluesse, updatedAt: new Date() } : o
      ));
    } catch (error) {
      console.error('Error updating beschluss:', error);
    }
  };

  // Offene Mahnungen zählen
  const getOffeneMahnungen = () => {
    let count = 0;
    let betrag = 0;
    objekte.forEach(o => {
      o.mahnungen?.filter(m => m.status === 'offen').forEach(m => {
        count++;
        betrag += m.betrag;
      });
    });
    return { count, betrag };
  };

  const offeneMahnungen = getOffeneMahnungen();

  // Filtern und Sortieren
  const filteredObjekte = objekte
    .filter(o =>
      o.adresse.toLowerCase().includes(searchTerm.toLowerCase()) ||
      o.ort.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'mieter':
          return (b.mieter?.length || 0) - (a.mieter?.length || 0);
        case 'flaeche':
          return (b.gesamtflaeche || 0) - (a.gesamtflaeche || 0);
        case 'einnahmen':
          const einnahmenA = a.mieter?.reduce((s, m) => s + (m.vorauszahlung || 0), 0) || 0;
          const einnahmenB = b.mieter?.reduce((s, m) => s + (m.vorauszahlung || 0), 0) || 0;
          return einnahmenB - einnahmenA;
        default:
          return a.adresse.localeCompare(b.adresse);
      }
    });

  // Berechnungen für KPIs
  const totalMieter = objekte.reduce((sum, o) => sum + (o.mieter?.length || 0), 0);
  const totalEigentuemer = objekte.reduce((sum, o) => sum + (o.eigentuemer?.length || 0), 0);
  const totalFlaeche = objekte.reduce((sum, o) => sum + (o.gesamtflaeche || 0), 0);
  const monatlicheEinnahmen = objekte.reduce((sum, o) => sum + (o.mieter?.reduce((s, m) => s + (m.vorauszahlung || 0), 0) || 0), 0);
  const monatlichesHausgeld = objekte.reduce((sum, o) => sum + (o.eigentuemer?.reduce((s, e) => s + (e.hausgeld || 0), 0) || 0), 0);
  const leerstehendeEinheiten = objekte.reduce((sum, o) => sum + Math.max(0, (o.gesamteinheiten || 0) - (o.mieter?.length || 0)), 0);
  const wegObjekte = objekte.filter(o => o.typ === 'weg').length;
  const mietObjekte = objekte.filter(o => o.typ !== 'weg').length;

  const getTypIcon = (typ: string) => {
    return OBJEKT_TYPEN.find(t => t.id === typ)?.icon || '🏠';
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* Header */}
      <header className="bg-gray-900/80 backdrop-blur-xl border-b border-gray-800 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div className="flex items-center gap-2 sm:gap-4">
              <Link href="/dashboard" className="text-gray-400 hover:text-white transition-colors text-sm sm:text-base">
                ← <span className="hidden sm:inline">Dashboard</span>
              </Link>
              <div className="h-6 w-px bg-gray-700 hidden sm:block" />
              <h1 className="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                <span className="text-xl sm:text-2xl">🏢</span> <span className="hidden xs:inline">Meine </span>Objekte
              </h1>
            </div>
            <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
              <button
                onClick={() => setShowHandwerkerModal(true)}
                className="px-3 sm:px-4 py-2 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white rounded-lg font-medium transition-all flex items-center gap-1 sm:gap-2 text-sm whitespace-nowrap shadow-lg"
              >
                🔧 <span className="hidden sm:inline">Handwerker</span>
              </button>
              <button
                onClick={() => setShowMieterhoeungRechner(true)}
                className="px-3 sm:px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-lg font-medium transition-all flex items-center gap-1 sm:gap-2 text-sm whitespace-nowrap shadow-lg"
              >
                📈 <span className="hidden sm:inline">Mieterhöhung</span>
              </button>
              <button
                onClick={() => requireTier(() => setShowAddModal(true))}
                className="px-3 sm:px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors flex items-center gap-1 sm:gap-2 text-sm whitespace-nowrap"
              >
                <span>+</span> <span className="hidden sm:inline">Neues </span>Objekt
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* FREE User Banner */}
        {!hasAccess && (
          <div className="mb-6 p-4 bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/50 rounded-xl">
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <span className="text-4xl">🔒</span>
              <div className="flex-1 text-center sm:text-left">
                <p className="text-white font-bold text-lg">Demo-Ansicht - Volle Funktionen mit Upgrade</p>
                <p className="text-gray-300 text-sm">Sie sehen Beispieldaten. Mit Professional können Sie Ihre eigenen Objekte verwalten.</p>
              </div>
              <button
                onClick={() => setShowUpgradeModal(true)}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg font-medium whitespace-nowrap shadow-lg"
              >
                ⬆️ Jetzt upgraden
              </button>
            </div>
          </div>
        )}

        {/* KPI Dashboard - kompakt für Mobile */}
        {objekte.length > 0 && (
          <div className="grid grid-cols-3 sm:grid-cols-3 md:grid-cols-6 gap-1.5 sm:gap-3 mb-4 sm:mb-8">
            <div className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 rounded-lg sm:rounded-xl p-2 sm:p-4 border border-blue-500/30">
              <p className="text-blue-400 text-[10px] sm:text-xs font-medium">Objekte</p>
              <p className="text-lg sm:text-2xl font-bold text-white">{objekte.length}</p>
            </div>
            <div className="bg-gradient-to-br from-green-600/20 to-green-800/20 rounded-lg sm:rounded-xl p-2 sm:p-4 border border-green-500/30">
              <p className="text-green-400 text-[10px] sm:text-xs font-medium">Mieter</p>
              <p className="text-lg sm:text-2xl font-bold text-white">{totalMieter}</p>
            </div>
            <div className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 rounded-lg sm:rounded-xl p-2 sm:p-4 border border-purple-500/30">
              <p className="text-purple-400 text-[10px] sm:text-xs font-medium">WEG</p>
              <p className="text-lg sm:text-2xl font-bold text-white">{totalEigentuemer}</p>
            </div>
            <div className="bg-gradient-to-br from-cyan-600/20 to-cyan-800/20 rounded-lg sm:rounded-xl p-2 sm:p-4 border border-cyan-500/30">
              <p className="text-cyan-400 text-[10px] sm:text-xs font-medium">Fläche</p>
              <p className="text-lg sm:text-2xl font-bold text-white">{totalFlaeche.toLocaleString()}<span className="text-xs sm:text-sm"> m²</span></p>
            </div>
            <div className="bg-gradient-to-br from-amber-600/20 to-amber-800/20 rounded-lg sm:rounded-xl p-2 sm:p-4 border border-amber-500/30">
              <p className="text-amber-400 text-[10px] sm:text-xs font-medium">Einnahmen</p>
              <p className="text-lg sm:text-2xl font-bold text-white">{monatlicheEinnahmen.toLocaleString()}<span className="text-xs"> €</span></p>
            </div>
            <div className="bg-gradient-to-br from-pink-600/20 to-pink-800/20 rounded-lg sm:rounded-xl p-2 sm:p-4 border border-pink-500/30">
              <p className="text-pink-400 text-[10px] sm:text-xs font-medium">Hausgeld</p>
              <p className="text-lg sm:text-2xl font-bold text-white">{monatlichesHausgeld.toLocaleString()}<span className="text-xs"> €</span></p>
            </div>
          </div>
        )}

        {/* Rückstände-Warnung */}
        {rueckstaende.gesamt > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 sm:p-4 mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0">
            <div className="flex items-center gap-3">
              <span className="text-2xl">💸</span>
              <div>
                <p className="text-red-400 font-medium text-sm sm:text-base">Zahlungsrückstände</p>
                <p className="text-red-300/70 text-xs sm:text-sm">
                  {rueckstaende.mietrueckstand > 0 && `Miete: ${rueckstaende.mietrueckstand.toLocaleString()} € `}
                  {rueckstaende.hausgeldrueckstand > 0 && `Hausgeld: ${rueckstaende.hausgeldrueckstand.toLocaleString()} €`}
                </p>
              </div>
            </div>
            <p className="text-xl sm:text-2xl font-bold text-red-400 text-right sm:text-left">{rueckstaende.gesamt.toLocaleString()} €</p>
          </div>
        )}

        {/* Leerstand-Warnung */}
        {leerstehendeEinheiten > 0 && (
          <div className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-4 mb-6 flex items-center gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="text-orange-400 font-medium">Leerstand erkannt</p>
              <p className="text-orange-300/70 text-sm">{leerstehendeEinheiten} Einheit{leerstehendeEinheiten > 1 ? 'en' : ''} nicht vermietet – {(leerstehendeEinheiten * 500).toLocaleString()} € potenzielle Mehreinnahmen/Mon.</p>
            </div>
          </div>
        )}

        {/* NEU: Wartungstermine-Warnung */}
        {faelligeWartungen.length > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">🔧</span>
              <div>
                <p className="text-red-400 font-medium">Anstehende Wartungstermine</p>
                <p className="text-red-300/70 text-sm">{faelligeWartungen.length} Termin{faelligeWartungen.length > 1 ? 'e' : ''} in den nächsten 30 Tagen</p>
              </div>
            </div>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {faelligeWartungen.slice(0, 5).map(({ objekt, wartung }) => {
                const heute = new Date();
                const faelligkeit = new Date(wartung.faelligkeitsdatum);
                const tage = Math.ceil((faelligkeit.getTime() - heute.getTime()) / (1000 * 60 * 60 * 24));
                const istUeberfaellig = tage < 0;
                
                return (
                  <div key={wartung.id} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-2 text-sm">
                    <div className="flex items-center gap-2 min-w-0 flex-1">
                      <span className="flex-shrink-0">{WARTUNGS_TYPEN.find(t => t.id === wartung.typ)?.icon || '📋'}</span>
                      <span className="text-white font-medium truncate">{wartung.bezeichnung}</span>
                      <span className="text-gray-500 hidden sm:inline">•</span>
                      <span className="text-gray-400 truncate hidden sm:inline">{objekt.adresse}</span>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className={`text-xs sm:text-sm ${istUeberfaellig ? 'text-red-400 font-bold' : tage <= 7 ? 'text-orange-400' : 'text-yellow-400'}`}>
                        {istUeberfaellig ? `${Math.abs(tage)}d überfällig!` : `in ${tage}d`}
                      </span>
                      {hasAccess ? (
                        <button
                          onClick={() => handleToggleWartung(objekt.id, wartung.id)}
                          className="px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-xs"
                        >
                          ✓
                        </button>
                      ) : (
                        <span className="px-2 py-1 bg-gray-700 text-gray-500 rounded text-xs">🔐</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* NEU: Mahnungen-Warnung */}
        {offeneMahnungen.count > 0 && (
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">📬</span>
              <div>
                <p className="text-yellow-400 font-medium">Offene Mahnungen</p>
                <p className="text-yellow-300/70 text-sm">{offeneMahnungen.count} offene Mahnung{offeneMahnungen.count > 1 ? 'en' : ''} - {offeneMahnungen.betrag.toLocaleString()} € ausstehend</p>
              </div>
            </div>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {objekte.filter(o => o.mahnungen?.some(m => m.status === 'offen')).slice(0, 5).map(objekt => {
                const mahnungenOffen = objekt.mahnungen!.filter(m => m.status === 'offen');
                const gesamtbetrag = mahnungenOffen.reduce((sum, m) => sum + m.betrag, 0);
                const hoechsteStufe = Math.max(...mahnungenOffen.map(m => m.stufe));
                
                return (
                  <div key={objekt.id} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className={hoechsteStufe === 3 ? 'text-red-400' : hoechsteStufe === 2 ? 'text-orange-400' : 'text-yellow-400'}>
                        {hoechsteStufe === 3 ? '🚨' : hoechsteStufe === 2 ? '⚠️' : '📩'}
                      </span>
                      <span className="text-white font-medium">{objekt.adresse}</span>
                      <span className="text-gray-500">•</span>
                      <span className="text-gray-400">{mahnungenOffen.length} Mahnung{mahnungenOffen.length > 1 ? 'en' : ''}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-400 font-medium">{gesamtbetrag.toLocaleString()} €</span>
                      <span className={`text-xs px-2 py-0.5 rounded ${
                        hoechsteStufe === 3 ? 'bg-red-500/20 text-red-400' : 
                        hoechsteStufe === 2 ? 'bg-orange-500/20 text-orange-400' : 
                        'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        Stufe {hoechsteStufe}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Suche & Sortierung */}
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 mb-6">
          <input
            type="text"
            placeholder="Objekte suchen..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full sm:flex-1 sm:min-w-[200px] sm:max-w-md px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
          <div className="flex gap-2 overflow-x-auto pb-1 sm:pb-0">
            <span className="text-gray-500 text-sm self-center hidden sm:block">Sortieren:</span>
            {[
              { id: 'name', label: 'Name' },
              { id: 'mieter', label: 'Mieter' },
              { id: 'flaeche', label: 'Fläche' },
              { id: 'einnahmen', label: '€' },
            ].map(opt => (
              <button
                key={opt.id}
                onClick={() => setSortBy(opt.id as SortOption)}
                className={`px-3 py-2 rounded-lg text-sm transition-colors whitespace-nowrap ${
                  sortBy === opt.id 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Objekte Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : filteredObjekte.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🏠</div>
            <h3 className="text-xl font-bold text-white mb-2">Keine Objekte vorhanden</h3>
            <p className="text-gray-400 mb-6">Erstellen Sie Ihr erstes Objekt.</p>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              + Erstes Objekt anlegen
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredObjekte.map(objekt => {
              // Leerstand berechnen
              const leerstand = objekt.gesamteinheiten - objekt.mieter.length;
              const hatLeerstand = leerstand > 0;
              
              // Mieterhöhungspotenzial: Mieter mit Einzug > 15 Monate
              const heute = new Date();
              const mieterMitPotenzial = objekt.mieter.filter(m => {
                if (!m.einzugsdatum) return false;
                const einzug = new Date(m.einzugsdatum);
                const monate = (heute.getTime() - einzug.getTime()) / (1000 * 60 * 60 * 24 * 30);
                return monate >= 15;
              });
              
              return (
              <div key={objekt.id} className="bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden hover:border-gray-600 transition-colors">
                {/* Status-Banner */}
                {(hatLeerstand || mieterMitPotenzial.length > 0) && (
                  <div className="flex">
                    {hatLeerstand && (
                      <div className="flex-1 bg-orange-500/20 text-orange-400 text-xs py-1 px-3 text-center">
                        ⚠️ {leerstand} Einheit{leerstand > 1 ? 'en' : ''} leer
                      </div>
                    )}
                    {mieterMitPotenzial.length > 0 && (
                      <div className="flex-1 bg-blue-500/20 text-blue-400 text-xs py-1 px-3 text-center">
                        📈 {mieterMitPotenzial.length}x Mieterhöhung möglich
                      </div>
                    )}
                  </div>
                )}
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{getTypIcon(objekt.typ)}</span>
                      <div>
                        <h3 className="font-bold text-white">{objekt.adresse}</h3>
                        <p className="text-sm text-gray-400">{objekt.plz} {objekt.ort}</p>
                      </div>
                    </div>
                    {hasAccess && (
                      <button
                        onClick={() => handleDeleteObjekt(objekt.id)}
                        className="text-gray-500 hover:text-red-400 transition-colors"
                      >
                        🗑️
                      </button>
                    )}
                  </div>

                  {/* Details */}
                  <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                    <div className="bg-gray-900/50 rounded-lg p-3">
                      <p className="text-gray-500 text-xs">Fläche</p>
                      <p className="text-white font-medium">{objekt.gesamtflaeche} m²</p>
                    </div>
                    <div className="bg-gray-900/50 rounded-lg p-3">
                      <p className="text-gray-500 text-xs">Einheiten</p>
                      <p className="text-white font-medium">{objekt.gesamteinheiten}</p>
                    </div>
                    <div className="bg-gray-900/50 rounded-lg p-3">
                      <p className="text-gray-500 text-xs">Heizung</p>
                      <p className="text-white font-medium">{HEIZUNGSTYPEN.find(h => h.id === objekt.heizungstyp)?.label || '-'}</p>
                    </div>
                    <div className="bg-gray-900/50 rounded-lg p-3">
                      <p className="text-gray-500 text-xs">Mieter</p>
                      <p className="text-white font-medium">{objekt.mieter.length}</p>
                    </div>
                  </div>

                  {/* Einnahmen-Übersicht */}
                  {objekt.mieter.length > 0 && (
                    <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3 mb-4">
                      <div className="flex justify-between items-center">
                        <span className="text-green-400 text-sm">💰 Vorauszahlungen/Mon.</span>
                        <span className="text-green-300 font-bold">{objekt.mieter.reduce((s, m) => s + (m.vorauszahlung || 0), 0).toLocaleString()} €</span>
                      </div>
                    </div>
                  )}

                  {/* Mieter Liste */}
                  {objekt.mieter.length > 0 && (
                    <div className="mb-4">
                      <p className="text-xs text-gray-500 mb-2">Mieter/Eigentümer:</p>
                      <div className="space-y-1 max-h-24 overflow-y-auto">
                        {objekt.mieter.map(m => (
                          <div key={m.id} className="flex items-center justify-between text-sm bg-gray-900/30 rounded px-2 py-1">
                            <span className="text-gray-300">{m.name} ({m.einheit})</span>
                            {hasAccess && (
                              <button
                                onClick={() => handleDeleteMieter(objekt.id, m.id)}
                                className="text-gray-600 hover:text-red-400 text-xs"
                              >
                                ✕
                              </button>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="space-y-2">
                    <div className="flex gap-2">
                      <button
                        onClick={() => requireTier(() => setShowMieterModal(objekt.id))}
                        className={`flex-1 py-2 rounded-lg text-sm transition-colors ${hasAccess ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-gray-800/50 text-gray-500 cursor-not-allowed'}`}
                      >
                        {!hasAccess && '🔒 '}+ Mieter
                      </button>
                      <button
                        onClick={() => requireTier(() => setShowWartungModal(objekt.id))}
                        className={`flex-1 py-2 rounded-lg text-sm transition-colors ${hasAccess ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-gray-800/50 text-gray-500 cursor-not-allowed'}`}
                      >
                        {!hasAccess && '🔒 '}🔧 Wartung
                      </button>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => requireTier(() => window.location.href = `/app/nebenkosten-abrechnung?objekt=${objekt.id}`)}
                        className={`flex-1 py-2 rounded-lg text-sm text-center transition-colors ${hasAccess ? 'bg-green-600 hover:bg-green-700 text-white' : 'bg-green-600/30 text-green-400/60 cursor-not-allowed'}`}
                      >
                        {!hasAccess && '🔒 '}📊 Abrechnung
                      </button>
                      <button
                        onClick={() => setShowDetailView(objekt.id)}
                        className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
                      >
                        📋 Details
                      </button>
                    </div>
                    <button
                      onClick={() => requireTier(() => window.location.href = `/app?prompt=Analysiere%20mein%20Objekt%20${encodeURIComponent(objekt.adresse)}%20mit%20${objekt.gesamtflaeche}m²%20Fläche,%20${objekt.einheiten}%20Einheiten%20und%20${objekt.mieter.length}%20Mietern.%20Heizung:%20${encodeURIComponent(objekt.heizungstyp)}.%20Prüfe%20Leerstandsrisiko,%20Mietpreispotenzial,%20Nebenkostenoptimierung,%20energetische%20Sanierung%20und%20steuerliche%20Optimierung.`)}
                      className={`block w-full py-2 border rounded-lg text-sm text-center transition-colors ${hasAccess ? 'bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border-purple-500/30' : 'bg-purple-600/10 text-purple-400/60 border-purple-500/20 cursor-not-allowed'}`}
                    >
                      {!hasAccess && '🔒 '}🤖 KI-Analyse
                    </button>
                  </div>
                </div>
              </div>
            )})}
          </div>
        )}
      </div>

      {/* Add Objekt Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">Neues Objekt anlegen</h2>
                <button onClick={() => setShowAddModal(false)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            <div className="p-6 space-y-4">
              {/* Typ */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Objekttyp</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {OBJEKT_TYPEN.map(typ => (
                    <button
                      key={typ.id}
                      onClick={() => setNewObjekt({ ...newObjekt, typ: typ.id as any })}
                      className={`p-2 sm:p-3 rounded-lg border text-center transition-colors ${
                        newObjekt.typ === typ.id
                          ? 'border-blue-500 bg-blue-500/20 text-white'
                          : 'border-gray-700 bg-gray-800/50 text-gray-400 hover:border-gray-600'
                      }`}
                    >
                      <span className="text-2xl block mb-1">{typ.icon}</span>
                      <span className="text-xs">{typ.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Adresse */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Straße & Hausnummer *</label>
                <input
                  type="text"
                  value={newObjekt.adresse}
                  onChange={(e) => setNewObjekt({ ...newObjekt, adresse: e.target.value })}
                  placeholder="Musterstraße 123"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">PLZ *</label>
                  <input
                    type="text"
                    value={newObjekt.plz}
                    onChange={(e) => setNewObjekt({ ...newObjekt, plz: e.target.value })}
                    placeholder="12345"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Ort *</label>
                  <input
                    type="text"
                    value={newObjekt.ort}
                    onChange={(e) => setNewObjekt({ ...newObjekt, ort: e.target.value })}
                    placeholder="Berlin"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Gesamtfläche (m²)</label>
                  <input
                    type="number"
                    value={newObjekt.gesamtflaeche || ''}
                    onChange={(e) => setNewObjekt({ ...newObjekt, gesamtflaeche: parseFloat(e.target.value) || 0 })}
                    placeholder="500"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Einheiten</label>
                  <input
                    type="number"
                    value={newObjekt.gesamteinheiten || ''}
                    onChange={(e) => setNewObjekt({ ...newObjekt, gesamteinheiten: parseInt(e.target.value) || 1 })}
                    placeholder="6"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Heizungstyp</label>
                  <select
                    value={newObjekt.heizungstyp}
                    onChange={(e) => setNewObjekt({ ...newObjekt, heizungstyp: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500"
                  >
                    {HEIZUNGSTYPEN.map(h => (
                      <option key={h.id} value={h.id}>{h.label}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Baujahr</label>
                  <input
                    type="number"
                    value={newObjekt.baujahr || ''}
                    onChange={(e) => setNewObjekt({ ...newObjekt, baujahr: parseInt(e.target.value) || undefined })}
                    placeholder="1985"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Notizen</label>
                <textarea
                  value={newObjekt.notizen}
                  onChange={(e) => setNewObjekt({ ...newObjekt, notizen: e.target.value })}
                  placeholder="Interne Notizen zum Objekt..."
                  rows={3}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 resize-none"
                />
              </div>
            </div>
            <div className="p-6 border-t border-gray-700 flex gap-3">
              <button
                onClick={() => setShowAddModal(false)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                Abbrechen
              </button>
              <button
                onClick={handleAddObjekt}
                disabled={!newObjekt.adresse || !newObjekt.plz || !newObjekt.ort}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
              >
                Objekt speichern
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Mieter Modal */}
      {showMieterModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">
                  {objekte.find(o => o.id === showMieterModal)?.typ === 'weg' ? 'Eigentümer' : 'Mieter'} hinzufügen
                </h2>
                <button onClick={() => setShowMieterModal(null)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Name *</label>
                <input
                  type="text"
                  value={newMieter.name}
                  onChange={(e) => setNewMieter({ ...newMieter, name: e.target.value })}
                  placeholder="Max Mustermann"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Einheit *</label>
                  <input
                    type="text"
                    value={newMieter.einheit}
                    onChange={(e) => setNewMieter({ ...newMieter, einheit: e.target.value })}
                    placeholder="EG links"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Fläche (m²)</label>
                  <input
                    type="number"
                    value={newMieter.flaeche || ''}
                    onChange={(e) => setNewMieter({ ...newMieter, flaeche: parseFloat(e.target.value) || 0 })}
                    placeholder="75"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Personen</label>
                  <input
                    type="number"
                    min="1"
                    value={newMieter.personenanzahl}
                    onChange={(e) => setNewMieter({ ...newMieter, personenanzahl: parseInt(e.target.value) || 1 })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Einzug</label>
                  <input
                    type="date"
                    value={newMieter.einzugsdatum}
                    onChange={(e) => setNewMieter({ ...newMieter, einzugsdatum: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">E-Mail</label>
                  <input
                    type="email"
                    value={newMieter.email}
                    onChange={(e) => setNewMieter({ ...newMieter, email: e.target.value })}
                    placeholder="max@beispiel.de"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Telefon</label>
                  <input
                    type="tel"
                    value={newMieter.telefon}
                    onChange={(e) => setNewMieter({ ...newMieter, telefon: e.target.value })}
                    placeholder="+49 123 456789"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Monatliche Vorauszahlung (€)</label>
                <input
                  type="number"
                  value={newMieter.vorauszahlung || ''}
                  onChange={(e) => setNewMieter({ ...newMieter, vorauszahlung: parseFloat(e.target.value) || 0 })}
                  placeholder="200"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>
            </div>
            <div className="p-6 border-t border-gray-700 flex gap-3">
              <button
                onClick={() => setShowMieterModal(null)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                Abbrechen
              </button>
              <button
                onClick={() => handleAddMieter(showMieterModal)}
                disabled={!newMieter.name || !newMieter.einheit}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
              >
                Speichern
              </button>
            </div>
          </div>
        </div>
      )}

      {/* NEU: Wartungstermin Modal */}
      {showWartungModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">🔧 Wartungstermin hinzufügen</h2>
                <button onClick={() => setShowWartungModal(null)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            <div className="p-6 space-y-4">
              {/* Typ */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Typ</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {WARTUNGS_TYPEN.map(typ => (
                    <button
                      key={typ.id}
                      onClick={() => setNewWartung({ ...newWartung, typ: typ.id as any })}
                      className={`p-2 sm:p-3 rounded-lg border text-center transition-colors ${
                        newWartung.typ === typ.id
                          ? 'border-blue-500 bg-blue-500/20 text-white'
                          : 'border-gray-700 bg-gray-800/50 text-gray-400 hover:border-gray-600'
                      }`}
                    >
                      <span className="text-2xl block mb-1">{typ.icon}</span>
                      <span className="text-xs">{typ.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Bezeichnung *</label>
                <input
                  type="text"
                  value={newWartung.bezeichnung}
                  onChange={(e) => setNewWartung({ ...newWartung, bezeichnung: e.target.value })}
                  placeholder="z.B. Heizungswartung, Rauchmelder-Prüfung..."
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Fälligkeitsdatum *</label>
                  <input
                    type="date"
                    value={newWartung.faelligkeitsdatum}
                    onChange={(e) => setNewWartung({ ...newWartung, faelligkeitsdatum: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Intervall (Monate)</label>
                  <input
                    type="number"
                    min="0"
                    value={newWartung.intervallMonate}
                    onChange={(e) => setNewWartung({ ...newWartung, intervallMonate: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">0 = einmalig</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Geschätzte Kosten (€)</label>
                <input
                  type="number"
                  value={newWartung.kosten || ''}
                  onChange={(e) => setNewWartung({ ...newWartung, kosten: parseFloat(e.target.value) || 0 })}
                  placeholder="z.B. 150"
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Notizen</label>
                <textarea
                  value={newWartung.notizen}
                  onChange={(e) => setNewWartung({ ...newWartung, notizen: e.target.value })}
                  placeholder="Zusätzliche Informationen..."
                  rows={2}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>
            </div>
            <div className="p-6 border-t border-gray-700 flex gap-3">
              <button
                onClick={() => setShowWartungModal(null)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                Abbrechen
              </button>
              <button
                onClick={() => handleAddWartung(showWartungModal)}
                disabled={!newWartung.bezeichnung || !newWartung.faelligkeitsdatum}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
              >
                Termin speichern
              </button>
            </div>
          </div>
        </div>
      )}

      {/* NEU: Detail-Ansicht Modal */}
      {showDetailView && (() => {
        const objekt = objekte.find(o => o.id === showDetailView);
        if (!objekt) return null;
        const istWEG = objekt.typ === 'weg';
        
        return (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-700 sticky top-0 bg-gray-900 z-10">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{getTypIcon(objekt.typ)}</span>
                    <div>
                      <h2 className="text-xl font-bold text-white">{objekt.adresse}</h2>
                      <p className="text-gray-400">{objekt.plz} {objekt.ort} {istWEG && objekt.wegName && `• ${objekt.wegName}`}</p>
                    </div>
                  </div>
                  <button onClick={() => { setShowDetailView(null); setActiveDetailTab('uebersicht'); }} className="text-gray-400 hover:text-white">✕</button>
                </div>
                
                {/* Tab-Navigation */}
                <div className="flex gap-2 flex-wrap">
                  <button
                    onClick={() => setActiveDetailTab('uebersicht')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'uebersicht' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                  >📊 Übersicht</button>
                  <button
                    onClick={() => setActiveDetailTab('einheiten')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'einheiten' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                  >🏠 Einheiten ({objekt.einheiten?.length || 0})</button>
                  {!istWEG && (
                    <button
                      onClick={() => setActiveDetailTab('mieter')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'mieter' ? 'bg-green-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                    >👥 Mieter ({objekt.mieter?.length || 0})</button>
                  )}
                  {istWEG && (
                    <button
                      onClick={() => setActiveDetailTab('eigentuemer')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'eigentuemer' ? 'bg-purple-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                    >👤 Eigentümer ({objekt.eigentuemer?.length || 0})</button>
                  )}
                  <button
                    onClick={() => setActiveDetailTab('zahlungen')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'zahlungen' ? 'bg-amber-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                  >💰 Zahlungen ({objekt.zahlungen?.length || 0})</button>
                  <button
                    onClick={() => setActiveDetailTab('wartung')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'wartung' ? 'bg-red-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                  >🔧 Wartung ({objekt.wartungstermine?.length || 0})</button>
                  <button
                    onClick={() => setActiveDetailTab('zaehler')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'zaehler' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                  >📊 Zähler ({objekt.zaehlerstaende?.length || 0})</button>
                  <button
                    onClick={() => setActiveDetailTab('mahnungen')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'mahnungen' ? 'bg-yellow-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                  >📬 Mahnungen ({objekt.mahnungen?.filter(m => m.status === 'offen').length || 0})</button>
                  {istWEG && (
                    <button
                      onClick={() => setActiveDetailTab('beschluesse')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeDetailTab === 'beschluesse' ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
                    >📋 Beschlüsse ({objekt.beschluesse?.length || 0})</button>
                  )}
                </div>
              </div>
              
              <div className="p-6">
                {/* Übersicht Tab */}
                {activeDetailTab === 'uebersicht' && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className="bg-gray-800/50 rounded-lg p-3">
                        <p className="text-xs text-gray-500">Fläche</p>
                        <p className="text-white font-medium">{objekt.gesamtflaeche} m²</p>
                      </div>
                      <div className="bg-gray-800/50 rounded-lg p-3">
                        <p className="text-xs text-gray-500">Einheiten</p>
                        <p className="text-white font-medium">{objekt.gesamteinheiten}</p>
                      </div>
                      <div className="bg-gray-800/50 rounded-lg p-3">
                        <p className="text-xs text-gray-500">Baujahr</p>
                        <p className="text-white font-medium">{objekt.baujahr || '-'}</p>
                      </div>
                      <div className="bg-gray-800/50 rounded-lg p-3">
                        <p className="text-xs text-gray-500">Heizung</p>
                        <p className="text-white font-medium">{HEIZUNGSTYPEN.find(h => h.id === objekt.heizungstyp)?.label || '-'}</p>
                      </div>
                    </div>
                    
                    {/* WEG-spezifische Infos */}
                    {istWEG && (
                      <div className="bg-purple-900/20 border border-purple-700/30 rounded-xl p-4">
                        <h3 className="text-purple-400 font-medium mb-3">🏘️ WEG-Informationen</h3>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                          <div>
                            <p className="text-xs text-gray-500">Instandhaltungsrücklage</p>
                            <p className="text-white font-medium">{(objekt.instandhaltungsruecklage || 0).toLocaleString()} €</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Hausgeld gesamt/Mon.</p>
                            <p className="text-white font-medium">{(objekt.eigentuemer?.reduce((s, e) => s + (e.hausgeld || 0), 0) || 0).toLocaleString()} €</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Verwalter seit</p>
                            <p className="text-white font-medium">{objekt.verwalterSeit || '-'}</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Notizen */}
                    {objekt.notizen && (
                      <div>
                        <h3 className="text-sm font-medium text-gray-400 mb-3">📝 Notizen</h3>
                        <div className="bg-gray-800/50 rounded-lg p-3">
                          <p className="text-gray-300 text-sm whitespace-pre-wrap">{objekt.notizen}</p>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Einheiten Tab */}
                {activeDetailTab === 'einheiten' && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="text-white font-medium">Einheiten verwalten</h3>
                      <button
                        onClick={() => setShowEinheitenModal(objekt.id)}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm"
                      >+ Einheit hinzufügen</button>
                    </div>
                    
                    {!objekt.einheiten?.length ? (
                      <div className="text-center py-8 text-gray-500">
                        <span className="text-4xl block mb-2">🏠</span>
                        Keine Einheiten angelegt
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {objekt.einheiten.map(e => (
                          <div key={e.id} className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                            <div className="flex items-start justify-between">
                              <div>
                                <p className="text-white font-medium">{e.nummer}</p>
                                <p className="text-gray-400 text-sm">
                                  {e.typ === 'wohnung' ? '🏠' : e.typ === 'gewerbe' ? '🏪' : e.typ === 'stellplatz' ? '🅿️' : '📦'} {e.typ}
                                  {e.flaeche && ` • ${e.flaeche}m²`}
                                  {e.zimmer && ` • ${e.zimmer} Zi.`}
                                  {e.etage && ` • ${e.etage}`}
                                </p>
                                {e.miteigentumsanteil && <p className="text-purple-400 text-xs">MEA: {e.miteigentumsanteil}/1000</p>}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Mieter Tab */}
                {activeDetailTab === 'mieter' && !istWEG && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="text-white font-medium">Mieterverwaltung</h3>
                      <button
                        onClick={() => setShowMieterModal(objekt.id)}
                        className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm"
                      >+ Mieter hinzufügen</button>
                    </div>
                    
                    {!objekt.mieter?.length ? (
                      <div className="text-center py-8 text-gray-500">
                        <span className="text-4xl block mb-2">👥</span>
                        Keine Mieter vorhanden
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {objekt.mieter.map(m => {
                          const einzug = new Date(m.einzugsdatum);
                          const heute = new Date();
                          const monate = Math.floor((heute.getTime() - einzug.getTime()) / (1000 * 60 * 60 * 24 * 30));
                          const hatRueckstand = (m.mietrueckstaende || 0) > 0;
                          
                          return (
                            <div key={m.id} className={`bg-gray-800/50 rounded-lg p-4 border ${hatRueckstand ? 'border-red-600/50' : 'border-gray-700'}`}>
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2">
                                    <p className="text-white font-medium">{m.name}</p>
                                    {hatRueckstand && <span className="text-xs bg-red-600/20 text-red-400 px-2 py-0.5 rounded">Rückstand</span>}
                                  </div>
                                  <p className="text-gray-400 text-sm">
                                    {m.einheit} • {m.flaeche}m² • {m.personenanzahl} Pers. • seit {einzug.toLocaleDateString('de-DE')} ({monate} Mon.)
                                  </p>
                                  <div className="flex gap-4 mt-2 text-xs text-gray-500">
                                    {m.email && <span>📧 {m.email}</span>}
                                    {m.telefon && <span>📞 {m.telefon}</span>}
                                  </div>
                                  <div className="flex gap-4 mt-2 text-sm">
                                    {m.kaltmiete && <span className="text-blue-400">Kalt: {m.kaltmiete}€</span>}
                                    {m.nebenkosten && <span className="text-cyan-400">NK: {m.nebenkosten}€</span>}
                                    {m.kaution && <span className={m.kautionBezahlt ? 'text-green-400' : 'text-yellow-400'}>Kaution: {m.kaution}€ {m.kautionBezahlt ? '✓' : '(offen)'}</span>}
                                  </div>
                                </div>
                                <div className="text-right">
                                  <p className="text-green-400 font-bold text-lg">{m.vorauszahlung}€/Mon.</p>
                                  {hatRueckstand && <p className="text-red-400 text-sm">-{m.mietrueckstaende}€ offen</p>}
                                  {monate >= 15 && <p className="text-xs text-blue-400 mt-1">📈 Mieterhöhung möglich</p>}
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}

                {/* Eigentümer Tab (WEG) */}
                {activeDetailTab === 'eigentuemer' && istWEG && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <h3 className="text-white font-medium">WEG Eigentümer</h3>
                        <p className="text-gray-500 text-sm">
                          Gesamt MEA: {objekt.eigentuemer?.reduce((s, e) => s + (e.miteigentumsanteil || 0), 0) || 0}/1000
                        </p>
                      </div>
                      <button
                        onClick={() => setShowEigentuemerModal(objekt.id)}
                        className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm"
                      >+ Eigentümer hinzufügen</button>
                    </div>
                    
                    {!objekt.eigentuemer?.length ? (
                      <div className="text-center py-8 text-gray-500">
                        <span className="text-4xl block mb-2">👤</span>
                        Keine Eigentümer erfasst
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {objekt.eigentuemer.map(e => {
                          const hatRueckstand = (e.hausgeldRueckstand || 0) > 0;
                          
                          return (
                            <div key={e.id} className={`bg-gray-800/50 rounded-lg p-4 border ${hatRueckstand ? 'border-red-600/50' : 'border-gray-700'}`}>
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2">
                                    <p className="text-white font-medium">{e.name}</p>
                                    <span className="text-xs bg-purple-600/20 text-purple-400 px-2 py-0.5 rounded">{e.einheitNr}</span>
                                    {e.istSelbstnutzer ? (
                                      <span className="text-xs bg-green-600/20 text-green-400 px-2 py-0.5 rounded">Selbstnutzer</span>
                                    ) : (
                                      <span className="text-xs bg-blue-600/20 text-blue-400 px-2 py-0.5 rounded">Vermietet</span>
                                    )}
                                    {hatRueckstand && <span className="text-xs bg-red-600/20 text-red-400 px-2 py-0.5 rounded">Rückstand</span>}
                                  </div>
                                  <p className="text-gray-400 text-sm mt-1">
                                    MEA: {e.miteigentumsanteil}/1000 ({((e.miteigentumsanteil / 1000) * 100).toFixed(1)}%)
                                    {e.stimmrecht && ` • ${e.stimmrecht} Stimme${e.stimmrecht > 1 ? 'n' : ''}`}
                                  </p>
                                  {e.sondereigentum && <p className="text-gray-500 text-xs mt-1">📋 {e.sondereigentum}</p>}
                                  {!e.istSelbstnutzer && e.mieter && <p className="text-blue-400 text-xs mt-1">👤 Mieter: {e.mieter}</p>}
                                  <div className="flex gap-4 mt-2 text-xs text-gray-500">
                                    {e.email && <span>📧 {e.email}</span>}
                                    {e.telefon && <span>📞 {e.telefon}</span>}
                                  </div>
                                </div>
                                <div className="text-right">
                                  <p className="text-pink-400 font-bold text-lg">{e.hausgeld}€/Mon.</p>
                                  {hatRueckstand && <p className="text-red-400 text-sm">-{e.hausgeldRueckstand}€ offen</p>}
                                </div>
                              </div>
                              <div className="mt-3 pt-3 border-t border-gray-700 flex justify-end gap-2">
                                <button className="text-gray-400 hover:text-white text-sm">✏️ Bearbeiten</button>
                                <button
                                  onClick={() => handleDeleteEigentuemer(objekt.id, e.id)}
                                  className="text-gray-400 hover:text-red-400 text-sm"
                                >🗑️ Löschen</button>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}

                {/* Zahlungen Tab */}
                {activeDetailTab === 'zahlungen' && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="text-white font-medium">Zahlungseingänge</h3>
                      <button
                        onClick={() => setShowZahlungenModal(objekt.id)}
                        className="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-sm"
                      >+ Zahlung erfassen</button>
                    </div>
                    
                    {!objekt.zahlungen?.length ? (
                      <div className="text-center py-8 text-gray-500">
                        <span className="text-4xl block mb-2">💰</span>
                        Keine Zahlungen erfasst
                      </div>
                    ) : (
                      <div className="bg-gray-800/50 rounded-xl overflow-hidden">
                        <table className="w-full text-sm">
                          <thead className="bg-gray-900/50">
                            <tr>
                              <th className="text-left p-3 text-gray-400">Datum</th>
                              <th className="text-left p-3 text-gray-400">Typ</th>
                              <th className="text-left p-3 text-gray-400">Monat</th>
                              <th className="text-left p-3 text-gray-400">Von</th>
                              <th className="text-right p-3 text-gray-400">Betrag</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-gray-700">
                            {objekt.zahlungen.slice(0, 20).map(z => {
                              const person = z.mieterId 
                                ? objekt.mieter?.find(m => m.id === z.mieterId)?.name
                                : objekt.eigentuemer?.find(e => e.id === z.eigentuemerId)?.name;
                              
                              return (
                                <tr key={z.id} className="hover:bg-gray-700/30">
                                  <td className="p-3 text-gray-300">{new Date(z.datum).toLocaleDateString('de-DE')}</td>
                                  <td className="p-3">
                                    <span className={`px-2 py-0.5 rounded text-xs ${
                                      z.typ === 'miete' ? 'bg-green-600/20 text-green-400' :
                                      z.typ === 'hausgeld' ? 'bg-pink-600/20 text-pink-400' :
                                      z.typ === 'kaution' ? 'bg-blue-600/20 text-blue-400' :
                                      'bg-gray-600/20 text-gray-400'
                                    }`}>
                                      {z.typ}
                                    </span>
                                  </td>
                                  <td className="p-3 text-gray-400">{z.monat}</td>
                                  <td className="p-3 text-gray-300">{person || '-'}</td>
                                  <td className="p-3 text-right text-green-400 font-medium">+{z.betrag.toLocaleString()}€</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                )}

                {/* Wartung Tab */}
                {activeDetailTab === 'wartung' && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <h3 className="text-white font-medium">Wartungstermine</h3>
                      <button
                        onClick={() => { setShowDetailView(null); setShowWartungModal(objekt.id); }}
                        className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm"
                      >+ Wartung hinzufügen</button>
                    </div>
                    
                    {!objekt.wartungstermine?.length ? (
                      <div className="text-center py-8 text-gray-500">
                        <span className="text-4xl block mb-2">🔧</span>
                        Keine Wartungstermine geplant
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {objekt.wartungstermine.map(w => {
                          const faelligkeit = new Date(w.faelligkeitsdatum);
                          const heute = new Date();
                          const tage = Math.ceil((faelligkeit.getTime() - heute.getTime()) / (1000 * 60 * 60 * 24));
                          
                          return (
                            <div key={w.id} className={`rounded-lg p-3 flex items-center justify-between ${
                              w.erledigt ? 'bg-gray-800/30' : tage < 0 ? 'bg-red-900/30 border border-red-700/50' : tage < 30 ? 'bg-yellow-900/20 border border-yellow-700/50' : 'bg-gray-800/50'
                            }`}>
                              <div className="flex items-center gap-3">
                                <span className="text-xl">{WARTUNGS_TYPEN.find(t => t.id === w.typ)?.icon}</span>
                                <div>
                                  <p className={`font-medium ${w.erledigt ? 'text-gray-500 line-through' : 'text-white'}`}>{w.bezeichnung}</p>
                                  <p className="text-xs text-gray-400">
                                    {faelligkeit.toLocaleDateString('de-DE')}
                                    {w.intervallMonate ? ` (alle ${w.intervallMonate} Monate)` : ' (einmalig)'}
                                    {w.kosten ? ` • ca. ${w.kosten}€` : ''}
                                  </p>
                                </div>
                              </div>
                              <div className="flex items-center gap-2">
                                {!w.erledigt && (
                                  <span className={`text-xs ${tage < 0 ? 'text-red-400' : tage < 30 ? 'text-yellow-400' : 'text-gray-400'}`}>
                                    {tage < 0 ? `${Math.abs(tage)}d überfällig` : `in ${tage}d`}
                                  </span>
                                )}
                                <button
                                  onClick={() => handleToggleWartung(objekt.id, w.id)}
                                  className={`px-2 py-1 rounded text-xs ${w.erledigt ? 'bg-gray-700 text-gray-400' : 'bg-green-600 text-white'}`}
                                >
                                  {w.erledigt ? 'Wiederherstellen' : '✓ Erledigt'}
                                </button>
                                <button
                                  onClick={() => handleDeleteWartung(objekt.id, w.id)}
                                  className="text-gray-500 hover:text-red-400"
                                >🗑️</button>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}

                {/* Zähler Tab */}
                {activeDetailTab === 'zaehler' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-white">📊 Zählerstandserfassung</h3>
                      <button
                        onClick={() => {
                          setShowZaehlerModal(objekt.id);
                        }}
                        className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-sm"
                      >+ Zählerstand erfassen</button>
                    </div>
                    {(!objekt.zaehlerstaende || objekt.zaehlerstaende.length === 0) ? (
                      <div className="text-center py-8 bg-gray-800/30 rounded-xl">
                        <p className="text-4xl mb-2">📊</p>
                        <p className="text-gray-400">Keine Zählerstände erfasst</p>
                        <p className="text-gray-500 text-sm">Erfassen Sie Zählerstände für BK-Abrechnungen</p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {ZAEHLER_TYPEN.map(typ => {
                          const zaehlerDesTyps = objekt.zaehlerstaende!.filter(z => z.zaehlerTyp === typ.id);
                          if (zaehlerDesTyps.length === 0) return null;
                          
                          const sortiert = [...zaehlerDesTyps].sort((a, b) => 
                            new Date(b.datum).getTime() - new Date(a.datum).getTime()
                          );
                          const letzter = sortiert[0];
                          const vorletzter = sortiert[1];
                          const verbrauch = vorletzter ? letzter.stand - vorletzter.stand : null;
                          
                          return (
                            <div key={typ.id} className="bg-gray-800/50 rounded-lg p-4">
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-2">
                                  <span className="text-xl">{typ.icon}</span>
                                  <span className="text-white font-medium">{typ.label}</span>
                                  <span className="text-gray-500 text-sm">({zaehlerDesTyps.length} Messungen)</span>
                                </div>
                                <span className="text-lg font-bold text-cyan-400">
                                  {letzter.stand.toLocaleString()} {typ.einheit}
                                </span>
                              </div>
                              {verbrauch !== null && (
                                <div className="flex items-center gap-2 text-sm">
                                  <span className="text-gray-400">Verbrauch seit letzter Ablesung:</span>
                                  <span className={verbrauch > 0 ? 'text-yellow-400' : 'text-green-400'}>
                                    {verbrauch > 0 ? '+' : ''}{verbrauch.toLocaleString()} {typ.einheit}
                                  </span>
                                </div>
                              )}
                              <div className="mt-2 text-xs text-gray-500">
                                Letzte Ablesung: {new Date(letzter.datum).toLocaleDateString('de-DE')}
                                {letzter.zaehlerNummer && ` • Zähler-Nr: ${letzter.zaehlerNummer}`}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}

                {/* Mahnungen Tab */}
                {activeDetailTab === 'mahnungen' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-white">📬 Mahnwesen</h3>
                      <button
                        onClick={() => {
                          setShowMahnungModal(objekt.id);
                        }}
                        className="px-3 py-1.5 bg-yellow-600 hover:bg-yellow-700 text-white rounded-lg text-sm"
                      >+ Mahnung erstellen</button>
                    </div>
                    {(!objekt.mahnungen || objekt.mahnungen.length === 0) ? (
                      <div className="text-center py-8 bg-gray-800/30 rounded-xl">
                        <p className="text-4xl mb-2">✅</p>
                        <p className="text-gray-400">Keine Mahnungen</p>
                        <p className="text-gray-500 text-sm">Alle Zahlungen sind aktuell</p>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {objekt.mahnungen.map(m => {
                          const tageUeberfaellig = Math.floor((new Date().getTime() - new Date(m.faelligSeit).getTime()) / (1000 * 60 * 60 * 24));
                          
                          return (
                            <div key={m.id} className={`rounded-lg p-3 flex items-center justify-between ${
                              m.status === 'bezahlt' ? 'bg-gray-800/30' : 
                              m.stufe === 3 ? 'bg-red-900/30 border border-red-700/50' :
                              m.stufe === 2 ? 'bg-orange-900/30 border border-orange-700/50' :
                              'bg-yellow-900/20 border border-yellow-700/50'
                            }`}>
                              <div className="flex items-center gap-3">
                                <span className="text-xl">
                                  {m.status === 'bezahlt' ? '✅' : m.status === 'inkasso' ? '⚖️' : 
                                   m.stufe === 3 ? '🚨' : m.stufe === 2 ? '⚠️' : '📩'}
                                </span>
                                <div>
                                  <p className={`font-medium ${m.status === 'bezahlt' ? 'text-gray-500 line-through' : 'text-white'}`}>
                                    {m.betrag.toLocaleString()} € - Stufe {m.stufe}
                                  </p>
                                  <p className="text-xs text-gray-400">
                                    Fällig seit {new Date(m.faelligSeit).toLocaleDateString('de-DE')}
                                    {m.status === 'offen' && ` • ${tageUeberfaellig} Tage überfällig`}
                                    {m.eigentuemerId && ' • Eigentümer'}
                                    {m.mieterId && ' • Mieter'}
                                  </p>
                                </div>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className={`text-xs px-2 py-0.5 rounded ${
                                  m.status === 'bezahlt' ? 'bg-green-500/20 text-green-400' :
                                  m.status === 'inkasso' ? 'bg-purple-500/20 text-purple-400' :
                                  'bg-yellow-500/20 text-yellow-400'
                                }`}>
                                  {m.status === 'bezahlt' ? 'Bezahlt' : m.status === 'inkasso' ? 'Inkasso' : 'Offen'}
                                </span>
                                {m.status === 'offen' && (
                                  <button
                                    onClick={() => handleMahnungBezahlt(objekt.id, m.id)}
                                    className="px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-xs"
                                  >✓ Bezahlt</button>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                    
                    {/* Mahnungsvorlagen Info */}
                    <div className="bg-gray-800/30 rounded-xl p-4 mt-4">
                      <h4 className="text-white font-medium mb-2">📋 Mahnungsstufen</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex items-center gap-2">
                          <span className="text-yellow-400">📩 Stufe 1:</span>
                          <span className="text-gray-400">Zahlungserinnerung (Frist: 7 Tage)</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-orange-400">⚠️ Stufe 2:</span>
                          <span className="text-gray-400">1. Mahnung mit Mahngebühr (Frist: 14 Tage)</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-red-400">🚨 Stufe 3:</span>
                          <span className="text-gray-400">Letzte Mahnung vor Inkasso/Anwalt</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Beschlüsse Tab (nur WEG) */}
                {activeDetailTab === 'beschluesse' && istWEG && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-medium text-white">📋 Beschlussbuch</h3>
                      <button
                        onClick={() => {
                          setShowBeschlussModal(objekt.id);
                        }}
                        className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm"
                      >+ Beschluss hinzufügen</button>
                    </div>
                    {(!objekt.beschluesse || objekt.beschluesse.length === 0) ? (
                      <div className="text-center py-8 bg-gray-800/30 rounded-xl">
                        <p className="text-4xl mb-2">📋</p>
                        <p className="text-gray-400">Keine Beschlüsse erfasst</p>
                        <p className="text-gray-500 text-sm">Erfassen Sie Beschlüsse der Eigentümerversammlungen</p>
                      </div>
                    ) : (
                      <div className="space-y-2">
                        {[...objekt.beschluesse].sort((a, b) => new Date(b.datum).getTime() - new Date(a.datum).getTime()).map(b => (
                          <div key={b.id} className={`rounded-lg p-3 flex items-center justify-between ${
                            b.umgesetzt ? 'bg-gray-800/30' : 'bg-gray-800/50'
                          }`}>
                            <div className="flex items-center gap-3">
                              <span className="text-xl">
                                {b.umgesetzt ? '✅' : b.ergebnis === 'angenommen' || b.ergebnis === 'einstimmig' ? '✓' : 
                                 b.ergebnis === 'abgelehnt' ? '✗' : '⏳'}
                              </span>
                              <div>
                                <p className={`font-medium ${b.umgesetzt ? 'text-gray-500' : 'text-white'}`}>
                                  TOP {b.topNummer}: {b.titel}
                                </p>
                                <p className="text-xs text-gray-400">
                                  {new Date(b.datum).toLocaleDateString('de-DE')}
                                  {b.jaStimmen !== undefined && b.neinStimmen !== undefined && 
                                    ` • ${b.jaStimmen} Ja / ${b.neinStimmen} Nein`}
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className={`text-xs px-2 py-0.5 rounded ${
                                b.ergebnis === 'einstimmig' ? 'bg-green-500/20 text-green-400' :
                                b.ergebnis === 'angenommen' ? 'bg-blue-500/20 text-blue-400' :
                                b.ergebnis === 'abgelehnt' ? 'bg-red-500/20 text-red-400' :
                                'bg-gray-500/20 text-gray-400'
                              }`}>
                                {b.ergebnis === 'einstimmig' ? 'Einstimmig' :
                                 b.ergebnis === 'angenommen' ? 'Angenommen' :
                                 b.ergebnis === 'abgelehnt' ? 'Abgelehnt' : 'Vertagt'}
                              </span>
                              {!b.umgesetzt && (b.ergebnis === 'angenommen' || b.ergebnis === 'einstimmig') && (
                                <button
                                  onClick={() => handleBeschlussUmgesetzt(objekt.id, b.id)}
                                  className="px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-xs"
                                >✓ Umgesetzt</button>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })()}

      {/* NEU: Eigentümer hinzufügen Modal */}
      {showEigentuemerModal && (() => {
        const objekt = objekte.find(o => o.id === showEigentuemerModal);
        if (!objekt) return null;
        
        return (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-lg w-full">
              <div className="p-6 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-white">👤 Eigentümer hinzufügen</h2>
                  <button onClick={() => setShowEigentuemerModal(null)} className="text-gray-400 hover:text-white">✕</button>
                </div>
              </div>
              <div className="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-300 mb-2">Name *</label>
                    <input
                      type="text"
                      value={newEigentuemer.name}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, name: e.target.value })}
                      placeholder="z.B. Dr. Müller"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Einheit Nr. *</label>
                    <input
                      type="text"
                      value={newEigentuemer.einheitNr}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, einheitNr: e.target.value })}
                      placeholder="z.B. WE 3"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">MEA (1/1000) *</label>
                    <input
                      type="number"
                      value={newEigentuemer.miteigentumsanteil || ''}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, miteigentumsanteil: Number(e.target.value) })}
                      placeholder="z.B. 85"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Hausgeld €/Mon.</label>
                    <input
                      type="number"
                      value={newEigentuemer.hausgeld || ''}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, hausgeld: Number(e.target.value) })}
                      placeholder="z.B. 350"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Nutzung</label>
                    <div className="flex gap-2">
                      <button
                        onClick={() => setNewEigentuemer({ ...newEigentuemer, istSelbstnutzer: true })}
                        className={`flex-1 py-2 rounded-lg text-sm ${newEigentuemer.istSelbstnutzer ? 'bg-green-600 text-white' : 'bg-gray-800 text-gray-400'}`}
                      >Selbstnutzer</button>
                      <button
                        onClick={() => setNewEigentuemer({ ...newEigentuemer, istSelbstnutzer: false })}
                        className={`flex-1 py-2 rounded-lg text-sm ${!newEigentuemer.istSelbstnutzer ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400'}`}
                      >Vermietet</button>
                    </div>
                  </div>
                  {!newEigentuemer.istSelbstnutzer && (
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-gray-300 mb-2">Mieter Name</label>
                      <input
                        type="text"
                        value={newEigentuemer.mieter}
                        onChange={(e) => setNewEigentuemer({ ...newEigentuemer, mieter: e.target.value })}
                        className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                  )}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">E-Mail</label>
                    <input
                      type="email"
                      value={newEigentuemer.email}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, email: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Telefon</label>
                    <input
                      type="tel"
                      value={newEigentuemer.telefon}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, telefon: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-300 mb-2">Sondereigentum</label>
                    <input
                      type="text"
                      value={newEigentuemer.sondereigentum}
                      onChange={(e) => setNewEigentuemer({ ...newEigentuemer, sondereigentum: e.target.value })}
                      placeholder="z.B. Wohnung Nr. 3, Keller K3, Stellplatz 5"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                </div>
              </div>
              <div className="p-6 border-t border-gray-700 flex gap-3">
                <button
                  onClick={() => setShowEigentuemerModal(null)}
                  className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg"
                >Abbrechen</button>
                <button
                  onClick={() => handleAddEigentuemer(showEigentuemerModal)}
                  disabled={!newEigentuemer.name || !newEigentuemer.einheitNr}
                  className="flex-1 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 text-white rounded-lg"
                >Eigentümer speichern</button>
              </div>
            </div>
          </div>
        );
      })()}

      {/* NEU: Zahlung erfassen Modal */}
      {showZahlungenModal && (() => {
        const objekt = objekte.find(o => o.id === showZahlungenModal);
        if (!objekt) return null;
        const istWEG = objekt.typ === 'weg';
        
        return (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-md w-full">
              <div className="p-6 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-white">💰 Zahlung erfassen</h2>
                  <button onClick={() => setShowZahlungenModal(null)} className="text-gray-400 hover:text-white">✕</button>
                </div>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Zahlungstyp</label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { id: 'miete', label: 'Miete', icon: '🏠' },
                      { id: 'hausgeld', label: 'Hausgeld', icon: '🏘️' },
                      { id: 'nebenkosten', label: 'NK-Nachz.', icon: '📊' },
                      { id: 'kaution', label: 'Kaution', icon: '🔐' },
                      { id: 'sonstiges', label: 'Sonstiges', icon: '📋' },
                    ].map(t => (
                      <button
                        key={t.id}
                        onClick={() => setNewZahlung({ ...newZahlung, typ: t.id as Zahlung['typ'] })}
                        className={`p-2 rounded-lg border text-center text-sm ${
                          newZahlung.typ === t.id ? 'border-amber-500 bg-amber-500/20 text-white' : 'border-gray-700 bg-gray-800/50 text-gray-400'
                        }`}
                      >
                        <span className="block mb-1">{t.icon}</span>
                        {t.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Betrag € *</label>
                    <input
                      type="number"
                      value={newZahlung.betrag || ''}
                      onChange={(e) => setNewZahlung({ ...newZahlung, betrag: Number(e.target.value) })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Datum</label>
                    <input
                      type="date"
                      value={newZahlung.datum}
                      onChange={(e) => setNewZahlung({ ...newZahlung, datum: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Für Monat</label>
                  <input
                    type="month"
                    value={newZahlung.monat}
                    onChange={(e) => setNewZahlung({ ...newZahlung, monat: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Von {istWEG ? 'Eigentümer' : 'Mieter'}</label>
                  <select
                    value={istWEG ? newZahlung.eigentuemerId : newZahlung.mieterId}
                    onChange={(e) => istWEG 
                      ? setNewZahlung({ ...newZahlung, eigentuemerId: e.target.value })
                      : setNewZahlung({ ...newZahlung, mieterId: e.target.value })
                    }
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                  >
                    <option value="">Auswählen...</option>
                    {istWEG 
                      ? objekt.eigentuemer?.map(e => <option key={e.id} value={e.id}>{e.name} ({e.einheitNr})</option>)
                      : objekt.mieter?.map(m => <option key={m.id} value={m.id}>{m.name} ({m.einheit})</option>)
                    }
                  </select>
                </div>
              </div>
              <div className="p-6 border-t border-gray-700 flex gap-3">
                <button
                  onClick={() => setShowZahlungenModal(null)}
                  className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg"
                >Abbrechen</button>
                <button
                  onClick={() => handleAddZahlung(showZahlungenModal)}
                  disabled={!newZahlung.betrag}
                  className="flex-1 py-3 bg-amber-600 hover:bg-amber-700 disabled:bg-gray-700 text-white rounded-lg"
                >Zahlung speichern</button>
              </div>
            </div>
          </div>
        );
      })()}

      {/* NEU: Zählerstand Modal */}
      {showZaehlerModal && (() => {
        const objekt = objekte.find(o => o.id === showZaehlerModal);
        if (!objekt) return null;
        
        return (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-md w-full">
              <div className="p-6 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-white">📊 Zählerstand erfassen</h2>
                  <button onClick={() => setShowZaehlerModal(null)} className="text-gray-400 hover:text-white">✕</button>
                </div>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Zählertyp *</label>
                  <div className="grid grid-cols-5 gap-2">
                    {ZAEHLER_TYPEN.map(typ => (
                      <button
                        key={typ.id}
                        onClick={() => setNewZaehlerstand({ ...newZaehlerstand, zaehlerTyp: typ.id })}
                        className={`p-2 rounded-lg border text-center text-sm ${
                          newZaehlerstand.zaehlerTyp === typ.id ? 'border-cyan-500 bg-cyan-500/20 text-white' : 'border-gray-700 bg-gray-800/50 text-gray-400'
                        }`}
                      >
                        <span className="block text-xl mb-1">{typ.icon}</span>
                        <span className="text-xs">{typ.label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Zählerstand *</label>
                    <input
                      type="number"
                      step="0.01"
                      value={newZaehlerstand.stand || ''}
                      onChange={(e) => setNewZaehlerstand({ ...newZaehlerstand, stand: Number(e.target.value) })}
                      placeholder="z.B. 12345.67"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Datum *</label>
                    <input
                      type="date"
                      value={newZaehlerstand.datum}
                      onChange={(e) => setNewZaehlerstand({ ...newZaehlerstand, datum: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Zähler-Nummer</label>
                  <input
                    type="text"
                    value={newZaehlerstand.zaehlerNummer || ''}
                    onChange={(e) => setNewZaehlerstand({ ...newZaehlerstand, zaehlerNummer: e.target.value })}
                    placeholder="z.B. 1234567890"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                {objekt.einheiten && objekt.einheiten.length > 0 && (
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Für Einheit (optional)</label>
                    <select
                      value={newZaehlerstand.einheitId || ''}
                      onChange={(e) => setNewZaehlerstand({ ...newZaehlerstand, einheitId: e.target.value || undefined })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    >
                      <option value="">Gesamtobjekt</option>
                      {objekt.einheiten.map(e => (
                        <option key={e.id} value={e.id}>{e.nummer} ({e.typ})</option>
                      ))}
                    </select>
                  </div>
                )}
              </div>
              <div className="p-6 border-t border-gray-700 flex gap-3">
                <button
                  onClick={() => setShowZaehlerModal(null)}
                  className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg"
                >Abbrechen</button>
                <button
                  onClick={() => handleAddZaehlerstand(showZaehlerModal)}
                  disabled={!newZaehlerstand.stand || !newZaehlerstand.datum}
                  className="flex-1 py-3 bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-700 text-white rounded-lg"
                >Speichern</button>
              </div>
            </div>
          </div>
        );
      })()}

      {/* NEU: Mahnung Modal */}
      {showMahnungModal && (() => {
        const objekt = objekte.find(o => o.id === showMahnungModal);
        if (!objekt) return null;
        const istWEG = objekt.typ === 'weg';
        
        return (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-md w-full">
              <div className="p-6 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-white">📬 Mahnung erstellen</h2>
                  <button onClick={() => setShowMahnungModal(null)} className="text-gray-400 hover:text-white">✕</button>
                </div>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Mahnstufe *</label>
                  <div className="grid grid-cols-3 gap-2">
                    {[1, 2, 3].map(stufe => (
                      <button
                        key={stufe}
                        onClick={() => setNewMahnung({ ...newMahnung, stufe: stufe as 1 | 2 | 3 })}
                        className={`p-3 rounded-lg border text-center ${
                          newMahnung.stufe === stufe 
                            ? stufe === 3 ? 'border-red-500 bg-red-500/20 text-white' :
                              stufe === 2 ? 'border-orange-500 bg-orange-500/20 text-white' :
                              'border-yellow-500 bg-yellow-500/20 text-white'
                            : 'border-gray-700 bg-gray-800/50 text-gray-400'
                        }`}
                      >
                        <span className="block text-xl mb-1">
                          {stufe === 1 ? '📩' : stufe === 2 ? '⚠️' : '🚨'}
                        </span>
                        <span className="text-sm">Stufe {stufe}</span>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Betrag € *</label>
                    <input
                      type="number"
                      value={newMahnung.betrag || ''}
                      onChange={(e) => setNewMahnung({ ...newMahnung, betrag: Number(e.target.value) })}
                      placeholder="z.B. 850"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Fällig seit *</label>
                    <input
                      type="date"
                      value={newMahnung.faelligSeit}
                      onChange={(e) => setNewMahnung({ ...newMahnung, faelligSeit: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    {istWEG ? 'Eigentümer' : 'Mieter'} (optional)
                  </label>
                  <select
                    value={istWEG ? newMahnung.eigentuemerId || '' : newMahnung.mieterId || ''}
                    onChange={(e) => istWEG 
                      ? setNewMahnung({ ...newMahnung, eigentuemerId: e.target.value || undefined })
                      : setNewMahnung({ ...newMahnung, mieterId: e.target.value || undefined })
                    }
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                  >
                    <option value="">Allgemein</option>
                    {istWEG 
                      ? objekt.eigentuemer?.map(e => <option key={e.id} value={e.id}>{e.name} ({e.einheitNr})</option>)
                      : objekt.mieter?.map(m => <option key={m.id} value={m.id}>{m.name} ({m.einheit})</option>)
                    }
                  </select>
                </div>
              </div>
              <div className="p-6 border-t border-gray-700 flex gap-3">
                <button
                  onClick={() => setShowMahnungModal(null)}
                  className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg"
                >Abbrechen</button>
                <button
                  onClick={() => handleAddMahnung(showMahnungModal)}
                  disabled={!newMahnung.betrag || !newMahnung.faelligSeit}
                  className="flex-1 py-3 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-700 text-white rounded-lg"
                >Mahnung erstellen</button>
              </div>
            </div>
          </div>
        );
      })()}

      {/* NEU: Beschluss Modal (WEG) */}
      {showBeschlussModal && (() => {
        const objekt = objekte.find(o => o.id === showBeschlussModal);
        if (!objekt || objekt.typ !== 'weg') return null;
        
        return (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-lg w-full">
              <div className="p-6 border-b border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-white">📋 Beschluss erfassen</h2>
                  <button onClick={() => setShowBeschlussModal(null)} className="text-gray-400 hover:text-white">✕</button>
                </div>
              </div>
              <div className="p-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">TOP-Nummer *</label>
                    <input
                      type="number"
                      value={newBeschluss.topNummer || ''}
                      onChange={(e) => setNewBeschluss({ ...newBeschluss, topNummer: Number(e.target.value) })}
                      placeholder="z.B. 5"
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Datum *</label>
                    <input
                      type="date"
                      value={newBeschluss.datum}
                      onChange={(e) => setNewBeschluss({ ...newBeschluss, datum: e.target.value })}
                      className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Beschluss-Titel *</label>
                  <input
                    type="text"
                    value={newBeschluss.titel}
                    onChange={(e) => setNewBeschluss({ ...newBeschluss, titel: e.target.value })}
                    placeholder="z.B. Dachsanierung genehmigt"
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Ergebnis *</label>
                  <div className="grid grid-cols-4 gap-2">
                    {[
                      { id: 'einstimmig', label: 'Einstimmig', icon: '✓✓' },
                      { id: 'angenommen', label: 'Angenommen', icon: '✓' },
                      { id: 'abgelehnt', label: 'Abgelehnt', icon: '✗' },
                      { id: 'vertagt', label: 'Vertagt', icon: '⏳' },
                    ].map(r => (
                      <button
                        key={r.id}
                        onClick={() => setNewBeschluss({ ...newBeschluss, ergebnis: r.id as Beschluss['ergebnis'] })}
                        className={`p-2 rounded-lg border text-center text-sm ${
                          newBeschluss.ergebnis === r.id 
                            ? r.id === 'einstimmig' ? 'border-green-500 bg-green-500/20 text-white' :
                              r.id === 'angenommen' ? 'border-blue-500 bg-blue-500/20 text-white' :
                              r.id === 'abgelehnt' ? 'border-red-500 bg-red-500/20 text-white' :
                              'border-gray-500 bg-gray-500/20 text-white'
                            : 'border-gray-700 bg-gray-800/50 text-gray-400'
                        }`}
                      >
                        <span className="block mb-1">{r.icon}</span>
                        {r.label}
                      </button>
                    ))}
                  </div>
                </div>

                {(newBeschluss.ergebnis === 'angenommen' || newBeschluss.ergebnis === 'abgelehnt') && (
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Ja-Stimmen</label>
                      <input
                        type="number"
                        value={newBeschluss.jaStimmen || ''}
                        onChange={(e) => setNewBeschluss({ ...newBeschluss, jaStimmen: Number(e.target.value) })}
                        className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Nein-Stimmen</label>
                      <input
                        type="number"
                        value={newBeschluss.neinStimmen || ''}
                        onChange={(e) => setNewBeschluss({ ...newBeschluss, neinStimmen: Number(e.target.value) })}
                        className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white"
                      />
                    </div>
                  </div>
                )}
              </div>
              <div className="p-6 border-t border-gray-700 flex gap-3">
                <button
                  onClick={() => setShowBeschlussModal(null)}
                  className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg"
                >Abbrechen</button>
                <button
                  onClick={() => handleAddBeschluss(showBeschlussModal)}
                  disabled={!newBeschluss.topNummer || !newBeschluss.titel || !newBeschluss.datum}
                  className="flex-1 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-700 text-white rounded-lg"
                >Speichern</button>
              </div>
            </div>
          </div>
        );
      })()}

      {/* NEU: Handwerker-Verwaltung Modal */}
      {showHandwerkerModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">🔧 Handwerker-Kontakte</h2>
                <button onClick={() => setShowHandwerkerModal(false)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            
            {/* FREE-Nutzer Banner */}
            {!hasAccess && (
              <div className="mx-6 mt-4 p-4 bg-gradient-to-r from-orange-500/20 to-amber-500/20 border border-orange-500/50 rounded-xl">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">🔒</span>
                  <div className="flex-1">
                    <p className="text-white font-medium">Upgrade für Handwerker-Verwaltung</p>
                    <p className="text-gray-300 text-sm">Mit Professional können Sie Handwerker speichern und verwalten.</p>
                  </div>
                  <button
                    onClick={() => { setShowHandwerkerModal(false); setShowUpgradeModal(true); }}
                    className="px-4 py-2 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg font-medium text-sm whitespace-nowrap"
                  >
                    Jetzt upgraden
                  </button>
                </div>
              </div>
            )}
            
            <div className="p-6 overflow-y-auto max-h-[70vh]">
              {/* Neuen Handwerker hinzufügen */}
              <div className={`bg-gray-800/50 rounded-xl p-4 mb-6 ${!hasAccess ? 'opacity-50 pointer-events-none' : ''}`}>
                <h3 className="text-white font-medium mb-3">➕ Neuen Handwerker hinzufügen</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                  <input
                    type="text"
                    value={newHandwerker.firma}
                    onChange={(e) => setNewHandwerker({ ...newHandwerker, firma: e.target.value })}
                    placeholder="Firma / Name *"
                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm"
                  />
                  <select
                    value={newHandwerker.kategorie}
                    onChange={(e) => setNewHandwerker({ ...newHandwerker, kategorie: e.target.value as Handwerker['kategorie'] })}
                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm"
                  >
                    {HANDWERKER_KATEGORIEN.map(k => (
                      <option key={k.id} value={k.id}>{k.icon} {k.label}</option>
                    ))}
                  </select>
                  <input
                    type="tel"
                    value={newHandwerker.telefon}
                    onChange={(e) => setNewHandwerker({ ...newHandwerker, telefon: e.target.value })}
                    placeholder="Telefon *"
                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm"
                  />
                  <button
                    onClick={() => requireTier(() => handleAddHandwerker())}
                    disabled={!newHandwerker.firma || !newHandwerker.telefon}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white rounded-lg text-sm"
                  >+ Hinzufügen</button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
                  <input
                    type="email"
                    value={newHandwerker.email || ''}
                    onChange={(e) => setNewHandwerker({ ...newHandwerker, email: e.target.value })}
                    placeholder="E-Mail"
                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm"
                  />
                  <input
                    type="text"
                    value={newHandwerker.adresse || ''}
                    onChange={(e) => setNewHandwerker({ ...newHandwerker, adresse: e.target.value })}
                    placeholder="Adresse"
                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm"
                  />
                  <input
                    type="text"
                    value={newHandwerker.notizen || ''}
                    onChange={(e) => setNewHandwerker({ ...newHandwerker, notizen: e.target.value })}
                    placeholder="Notizen"
                    className="px-3 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white text-sm"
                  />
                </div>
              </div>

              {/* Handwerker-Liste nach Kategorie */}
              {handwerker.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-5xl mb-3">🔧</p>
                  <p className="text-gray-400 text-lg">Keine Handwerker hinterlegt</p>
                  <p className="text-gray-500 text-sm">{hasAccess ? 'Fügen Sie Ihre Handwerker-Kontakte hinzu' : 'Mit einem Upgrade können Sie hier Ihre Handwerker verwalten'}</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {HANDWERKER_KATEGORIEN.map(kategorie => {
                    const handwerkerInKategorie = handwerker.filter(h => h.kategorie === kategorie.id);
                    if (handwerkerInKategorie.length === 0) return null;
                    
                    return (
                      <div key={kategorie.id}>
                        <h4 className="text-gray-400 text-sm mb-2 flex items-center gap-2">
                          <span>{kategorie.icon}</span>
                          <span>{kategorie.label} ({handwerkerInKategorie.length})</span>
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {handwerkerInKategorie.map(h => (
                            <div key={h.id} className="bg-gray-800/50 rounded-lg p-3 flex items-center justify-between">
                              <div>
                                <p className="text-white font-medium">{h.firma}</p>
                                <div className="flex items-center gap-2 text-sm text-gray-400">
                                  <a href={`tel:${h.telefon}`} className="hover:text-blue-400">📞 {h.telefon}</a>
                                  {h.email && <a href={`mailto:${h.email}`} className="hover:text-blue-400">✉️</a>}
                                </div>
                                {h.notizen && <p className="text-xs text-gray-500 mt-1">{h.notizen}</p>}
                              </div>
                              {h.bewertung && (
                                <div className="text-yellow-400 text-sm">
                                  {'⭐'.repeat(h.bewertung)}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* NEU: KI-Mieterhöhungsassistent Modal */}
      {showMieterhoeungRechner && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-start justify-center z-50 overflow-y-auto p-2 sm:p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-2xl w-full mt-4 sm:mt-8 mb-4">
            <div className="p-4 sm:p-6 border-b border-gray-700">
              <div className="flex items-center justify-between gap-2">
                <div className="min-w-0">
                  <h2 className="text-lg sm:text-xl font-bold text-white truncate">📈 KI-Mieterhöhungsassistent</h2>
                  <p className="text-gray-400 text-xs sm:text-sm mt-1">Rechtssichere Prüfung nach §§ 558-560 BGB</p>
                </div>
                <button onClick={() => setShowMieterhoeungRechner(false)} className="text-gray-400 hover:text-white text-2xl flex-shrink-0">✕</button>
              </div>
            </div>
            
            {/* FREE-Nutzer Banner */}
            {!hasAccess && (
              <div className="mx-4 sm:mx-6 mt-4 p-4 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/50 rounded-xl">
                <div className="flex flex-col sm:flex-row items-center gap-3">
                  <span className="text-3xl">🔒</span>
                  <div className="flex-1 text-center sm:text-left">
                    <p className="text-white font-medium">Upgrade für Mieterhöhungsassistent</p>
                    <p className="text-gray-300 text-sm">Berechnen Sie rechtssichere Mieterhöhungen mit KI.</p>
                  </div>
                  <button
                    onClick={() => { setShowMieterhoeungRechner(false); setShowUpgradeModal(true); }}
                    className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium text-sm whitespace-nowrap"
                  >
                    Jetzt upgraden
                  </button>
                </div>
              </div>
            )}
            
            <div className={`p-4 sm:p-6 space-y-4 sm:space-y-5 max-h-[75vh] overflow-y-auto ${!hasAccess ? 'opacity-50 pointer-events-none' : ''}`}>
              {/* Schritt 1: Basisdaten */}
              <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-3 sm:p-4">
                <h3 className="text-blue-400 font-medium mb-3 text-sm sm:text-base">1️⃣ Mietverhältnis</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                  <div>
                    <label className="block text-xs sm:text-sm text-gray-300 mb-1">Aktuelle Kaltmiete €</label>
                    <input type="number" id="me-aktuell" placeholder="850" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm" />
                  </div>
                  <div>
                    <label className="block text-xs sm:text-sm text-gray-300 mb-1">Wohnfläche m²</label>
                    <input type="number" id="me-flaeche" placeholder="65" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm" />
                  </div>
                  <div>
                    <label className="block text-xs sm:text-sm text-gray-300 mb-1">Mietbeginn</label>
                    <input type="date" id="me-mietbeginn" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm" />
                  </div>
                  <div>
                    <label className="block text-xs sm:text-sm text-gray-300 mb-1">Letzte Erhöhung</label>
                    <input type="date" id="me-letzte" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm" />
                  </div>
                </div>
              </div>

              {/* Schritt 2: Erhöhungsart */}
              <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-3 sm:p-4">
                <h3 className="text-purple-400 font-medium mb-3 text-sm sm:text-base">2️⃣ Erhöhungsgrund (§ 558 BGB)</h3>
                <div className="grid grid-cols-3 gap-2 sm:gap-3">
                  <button id="me-art-spiegel" onClick={() => {
                    ['me-art-spiegel', 'me-art-index', 'me-art-modern'].forEach(id => {
                      const el = document.getElementById(id);
                      if (el) {
                        el.classList.remove('border-green-500', 'bg-green-500/20');
                        el.classList.add('border-gray-700');
                      }
                    });
                    document.getElementById('me-art-spiegel')?.classList.add('border-green-500', 'bg-green-500/20');
                    document.getElementById('me-art-spiegel')?.classList.remove('border-gray-700');
                  }} className="p-2 sm:p-3 rounded-lg border border-gray-700 bg-gray-800/50 text-center hover:bg-gray-800">
                    <span className="text-xl sm:text-2xl block mb-1">🏠</span>
                    <span className="text-white text-xs sm:text-sm font-medium">Mietspiegel</span>
                  </button>
                  <button id="me-art-index" onClick={() => {
                    ['me-art-spiegel', 'me-art-index', 'me-art-modern'].forEach(id => {
                      const el = document.getElementById(id);
                      if (el) {
                        el.classList.remove('border-green-500', 'bg-green-500/20');
                        el.classList.add('border-gray-700');
                      }
                    });
                    document.getElementById('me-art-index')?.classList.add('border-green-500', 'bg-green-500/20');
                    document.getElementById('me-art-index')?.classList.remove('border-gray-700');
                  }} className="p-2 sm:p-3 rounded-lg border border-gray-700 bg-gray-800/50 text-center hover:bg-gray-800">
                    <span className="text-xl sm:text-2xl block mb-1">📊</span>
                    <span className="text-white text-xs sm:text-sm font-medium">Index</span>
                  </button>
                  <button id="me-art-modern" onClick={() => {
                    ['me-art-spiegel', 'me-art-index', 'me-art-modern'].forEach(id => {
                      const el = document.getElementById(id);
                      if (el) {
                        el.classList.remove('border-green-500', 'bg-green-500/20');
                        el.classList.add('border-gray-700');
                      }
                    });
                    document.getElementById('me-art-modern')?.classList.add('border-green-500', 'bg-green-500/20');
                    document.getElementById('me-art-modern')?.classList.remove('border-gray-700');
                  }} className="p-2 sm:p-3 rounded-lg border border-gray-700 bg-gray-800/50 text-center hover:bg-gray-800">
                    <span className="text-xl sm:text-2xl block mb-1">🔧</span>
                    <span className="text-white text-xs sm:text-sm font-medium">Modern.</span>
                  </button>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mt-3 sm:mt-4">
                  <div>
                    <label className="block text-xs sm:text-sm text-gray-300 mb-1">Ortsübliche Miete €/m²</label>
                    <input type="number" id="me-ortsueblich" step="0.01" placeholder="12.50" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm" />
                  </div>
                  <div>
                    <label className="block text-xs sm:text-sm text-gray-300 mb-1">PLZ (für Kappungsgrenze)</label>
                    <input type="text" id="me-plz" placeholder="31515" className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm" />
                  </div>
                </div>
              </div>

              {/* KI-Analyse Button */}
              <button
                onClick={() => {
                  const aktuell = parseFloat((document.getElementById('me-aktuell') as HTMLInputElement).value) || 0;
                  const flaeche = parseFloat((document.getElementById('me-flaeche') as HTMLInputElement).value) || 0;
                  const ortsueblich = parseFloat((document.getElementById('me-ortsueblich') as HTMLInputElement).value) || 0;
                  const mietbeginn = (document.getElementById('me-mietbeginn') as HTMLInputElement).value;
                  const letzte = (document.getElementById('me-letzte') as HTMLInputElement).value;
                  const plz = (document.getElementById('me-plz') as HTMLInputElement).value;
                  
                  // Kappungsgrenze: 15% in angespannten Märkten, sonst 20%
                  const angespannt = ['10', '20', '22', '30', '40', '50', '60', '70', '80', '81'].some(p => plz.startsWith(p));
                  const kappung = angespannt ? 0.15 : 0.20;
                  const kappungText = angespannt ? '15% (angespannter Markt)' : '20%';
                  
                  // Sperrfrist prüfen (15 Monate nach letzter Erhöhung)
                  const letzteDate = letzte ? new Date(letzte) : null;
                  const mietbeginnDate = mietbeginn ? new Date(mietbeginn) : null;
                  const heute = new Date();
                  const sperrfristEnde = letzteDate ? new Date(letzteDate.getTime() + 15 * 30 * 24 * 60 * 60 * 1000) : 
                                         mietbeginnDate ? new Date(mietbeginnDate.getTime() + 12 * 30 * 24 * 60 * 60 * 1000) : null;
                  const sperrfristOk = !sperrfristEnde || heute > sperrfristEnde;
                  
                  // Berechnung
                  const maxSpiegel = ortsueblich * flaeche;
                  const maxKappung = aktuell * (1 + kappung);
                  const maxErhoeht = Math.min(maxSpiegel, maxKappung);
                  const differenz = maxErhoeht - aktuell;
                  
                  const resultDiv = document.getElementById('me-ergebnis');
                  if (resultDiv) {
                    resultDiv.innerHTML = `
                      <div class="space-y-3 sm:space-y-4">
                        <h4 class="text-white font-bold text-base sm:text-lg flex items-center gap-2">🤖 KI-Rechtsprüfung</h4>
                        
                        <!-- Prüfungsergebnisse -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                          <div class="bg-gray-800 rounded-lg p-2 sm:p-3">
                            <div class="flex items-center gap-2 mb-1">
                              ${sperrfristOk ? '<span class="text-green-400">✓</span>' : '<span class="text-red-400">✗</span>'}
                              <span class="text-gray-300 text-xs sm:text-sm">Sperrfrist (§ 558 I BGB)</span>
                            </div>
                            <span class="text-xs ${sperrfristOk ? 'text-green-400' : 'text-red-400'}">${sperrfristOk ? 'Erfüllt' : 'Nicht erfüllt!'}</span>
                          </div>
                          <div class="bg-gray-800 rounded-lg p-2 sm:p-3">
                            <div class="flex items-center gap-2 mb-1">
                              <span class="text-green-400">✓</span>
                              <span class="text-gray-300 text-xs sm:text-sm">Kappungsgrenze</span>
                            </div>
                            <span class="text-xs text-blue-400">${kappungText}</span>
                          </div>
                          <div class="bg-gray-800 rounded-lg p-2 sm:p-3">
                            <div class="flex items-center gap-2 mb-1">
                              ${aktuell < maxSpiegel ? '<span class="text-green-400">✓</span>' : '<span class="text-amber-400">⚠</span>'}
                              <span class="text-gray-300 text-xs sm:text-sm">Ortsübliche Miete</span>
                            </div>
                            <span class="text-xs ${aktuell < maxSpiegel ? 'text-green-400' : 'text-amber-400'}">${aktuell < maxSpiegel ? 'Erhöhung möglich' : 'Auf Niveau'}</span>
                          </div>
                          <div class="bg-gray-800 rounded-lg p-2 sm:p-3">
                            <div class="flex items-center gap-2 mb-1">
                              <span class="text-blue-400">ℹ</span>
                              <span class="text-gray-300 text-xs sm:text-sm">Formvorschriften</span>
                            </div>
                            <span class="text-xs text-gray-400">Schriftform erforderlich</span>
                          </div>
                        </div>

                        <!-- Berechnung -->
                        <div class="bg-green-500/10 border border-green-500/30 rounded-lg p-3 sm:p-4">
                          <div class="text-center">
                            <span class="text-gray-400 text-xs sm:text-sm">Max. rechtssichere Erhöhung</span>
                            <div class="text-2xl sm:text-3xl font-bold text-green-400 mt-1">${maxErhoeht.toFixed(2)} €</div>
                            <span class="text-green-400 text-xs sm:text-sm">+${differenz.toFixed(2)} €/Mon. (+${((differenz/aktuell)*100).toFixed(1)}%)</span>
                          </div>
                          <div class="grid grid-cols-2 gap-3 sm:gap-4 mt-3 sm:mt-4 text-xs sm:text-sm">
                            <div class="text-center">
                              <span class="text-gray-400 block">Max. Mietspiegel</span>
                              <span class="text-white font-medium">${maxSpiegel.toFixed(2)} €</span>
                            </div>
                            <div class="text-center">
                              <span class="text-gray-400 block">Max. Kappung</span>
                              <span class="text-white font-medium">${maxKappung.toFixed(2)} €</span>
                            </div>
                          </div>
                        </div>

                        <!-- CTA -->
                        <button 
                          id="me-generate-btn"
                          class="block w-full py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium text-center text-sm sm:text-base transition-colors cursor-pointer"
                        >
                          🤖 Schreiben generieren
                        </button>
                      </div>
                    `;
                    resultDiv.style.display = 'block';
                    
                    // Event-Listener für den Button - direkt nach DOM-Update
                    const genBtn = document.getElementById('me-generate-btn');
                    if (genBtn) {
                      genBtn.addEventListener('click', function() {
                        const promptText = 'Erstelle ein rechtssicheres Mieterhöhungsschreiben nach §558 BGB. Aktuelle Kaltmiete: ' + aktuell + ' Euro, Neue Kaltmiete: ' + maxErhoeht.toFixed(2) + ' Euro, Wohnfläche: ' + flaeche + ' m², Ortsübliche Vergleichsmiete: ' + ortsueblich + ' Euro pro m², Kappungsgrenze: ' + kappungText + '. Das Schreiben muss enthalten: 1. Korrekte Anrede und Betreff 2. Begründung der Erhöhung mit Verweis auf Mietspiegel 3. Hinweis auf Kappungsgrenze 4. Zustimmungsfrist nach Paragraph 558b BGB 5. Wirksamkeitszeitpunkt 6. Höfliche Formulierung';
                        window.location.href = '/app?prompt=' + encodeURIComponent(promptText);
                      });
                    }
                  }
                }}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium flex items-center justify-center gap-2"
              >
                🤖 KI-Rechtsprüfung starten
              </button>

              <div id="me-ergebnis" className="hidden"></div>

              <div className="bg-gray-800/50 rounded-lg p-3 text-xs text-gray-400">
                <p><strong>§ 558 BGB:</strong> Kappungsgrenze 20% (15% in angespannten Märkten) in 3 Jahren. Sperrfrist: 15 Monate nach letzter Erhöhung.</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        feature="Objektverwaltung"
        requiredTier="professional"
      />
    </div>
  );
}
