'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc, collection, addDoc, getDocs, deleteDoc, updateDoc, query, where, increment } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import TemplateEditor from '@/components/TemplateEditor';
import Logo from '@/components/Logo';
import UpgradeModal from '@/components/UpgradeModal';
import { saveTemplateAsMuster } from '@/lib/documentService';
import { hasTierAccess } from '@/lib/tierUtils';

interface Template {
  id: string;
  name: string;
  category: string;
  description: string;
  icon: string;
  forRoles: string[];
  content: string;
  isCustom?: boolean;
  userId?: string;
  createdAt?: string;
}

const TEMPLATES: Template[] = [
  // Mieter-Vorlagen
  {
    id: 'maengelanzeige',
    name: 'Mängelanzeige',
    category: 'Mieter',
    description: 'Mängel in der Wohnung dem Vermieter melden',
    icon: '🔧',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Mängelanzeige für die Wohnung [Adresse der Wohnung]

Sehr geehrte/r Immobilien Schmidt GmbH,

hiermit zeige ich Ihnen folgenden Mangel in der von mir gemieteten Wohnung an:

Beschreibung des Mangels:
[Hier den Mangel detailliert beschreiben, z.B. "Im Badezimmer ist an der Decke ein ca. 50 cm großer Wasserfleck entstanden. Es tropft Wasser von der Decke."]

Der Mangel besteht seit: 28.01.2026

Ich bitte Sie, den Mangel unverzüglich, spätestens jedoch bis zum [Frist, z.B. 14 Tage], zu beseitigen.

Bis zur Beseitigung des Mangels behalte ich mir vor, die Miete gemäß § 536 BGB zu mindern.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'mietminderung',
    name: 'Mietminderung ankündigen',
    category: 'Mieter',
    description: 'Miete wegen Mängeln mindern',
    icon: '💶',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Mietminderung wegen [Art des Mangels]

Sehr geehrte/r Immobilien Schmidt GmbH,

ich beziehe mich auf meine Mängelanzeige vom [Datum der Mängelanzeige].

Trotz meiner Aufforderung wurde der angezeigte Mangel bisher nicht beseitigt:
[Kurze Beschreibung des Mangels]

Gemäß § 536 BGB ist die Miete kraft Gesetzes gemindert, solange die Tauglichkeit der Mietsache zum vertragsgemäßen Gebrauch aufgehoben oder gemindert ist.

Unter Berücksichtigung der Rechtsprechung zu vergleichbaren Mängeln halte ich eine Minderungsquote von [X]% für angemessen.

Ich werde daher ab dem 28.01.2026 die monatliche Miete um [Betrag]€ mindern, bis der Mangel beseitigt ist.

Ich fordere Sie nochmals auf, den Mangel umgehend zu beseitigen.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'nebenkosteneinspruch',
    name: 'Einspruch Nebenkostenabrechnung',
    category: 'Mieter',
    description: 'Widerspruch gegen Nebenkostenabrechnung',
    icon: '📊',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Widerspruch gegen die Nebenkostenabrechnung für [Jahr]

Sehr geehrte/r Immobilien Schmidt GmbH,

ich habe Ihre Nebenkostenabrechnung vom 28.01.2026 für den Abrechnungszeitraum [Jahr] erhalten.

Nach Prüfung der Abrechnung widerspreche ich dieser aus folgenden Gründen:

1. [Grund 1, z.B. "Die Position 'Hausmeisterkosten' erscheint mir mit [Betrag]€ unverhältnismäßig hoch."]

2. [Grund 2, z.B. "Der verwendete Umlageschlüssel entspricht nicht den mietvertraglichen Vereinbarungen."]

Gemäß § 556 Abs. 3 BGB bitte ich um:
- Einsicht in die Originalbelege
- Nachvollziehbare Aufschlüsselung der beanstandeten Positionen

Bis zur Klärung behalte ich mir vor, die Nachzahlung in Höhe von [Betrag]€ zurückzuhalten.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'kuendigung_mieter',
    name: 'Kündigung Mietvertrag',
    category: 'Mieter',
    description: 'Ordentliche Kündigung als Mieter',
    icon: '📤',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Ordentliche Kündigung des Mietvertrags

Sehr geehrte/r Immobilien Schmidt GmbH,

hiermit kündige ich den zwischen uns bestehenden Mietvertrag vom [Datum des Mietvertrags] über die Wohnung [Adresse der Wohnung] ordentlich und fristgerecht zum [Kündigungstermin, z.B. 31.03.2026].

Alternativ kündige ich zum nächstmöglichen Termin.

Ich bitte um schriftliche Bestätigung der Kündigung.

Den Termin zur Wohnungsübergabe stimme ich gerne mit Ihnen ab. Bitte kontaktieren Sie mich hierfür unter [Telefonnummer/E-Mail].

Alle Mietzahlungen werde ich wie vereinbart bis zum Mietende leisten.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Kopie des Mietvertrags`
  },
  {
    id: 'kautionsrueckforderung',
    name: 'Kaution zurückfordern',
    category: 'Mieter',
    description: 'Rückzahlung der Mietkaution verlangen',
    icon: '💰',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
[Ihre neue Adresse]
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Rückforderung der Mietkaution
Ehemaliges Mietobjekt: [Adresse der alten Wohnung]

Sehr geehrte/r Immobilien Schmidt GmbH,

das Mietverhältnis über die oben genannte Wohnung endete am 28.01.2026. Die Wohnungsübergabe erfolgte am [Datum des Übergabeprotokolls].

Bei Mietbeginn habe ich eine Kaution in Höhe von [Betrag]€ hinterlegt.

Gemäß § 551 BGB fordere ich Sie auf, die Kaution zuzüglich der angefallenen Zinsen innerhalb von 14 Tagen auf folgendes Konto zu überweisen:

Kontoinhaber: Max Mustermann
IBAN: [Ihre IBAN]
BIC: [BIC]

Die Wohnung wurde gemäß Übergabeprotokoll in ordnungsgemäßem Zustand zurückgegeben. Berechtigte Gegenansprüche bestehen nicht.

Sollte die Zahlung nicht fristgerecht erfolgen, werde ich ohne weitere Ankündigung rechtliche Schritte einleiten.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Kopie des Übergabeprotokolls`
  },
  {
    id: 'untervermietung_antrag',
    name: 'Antrag auf Untervermietung',
    category: 'Mieter',
    description: 'Erlaubnis zur Untervermietung beantragen',
    icon: '👥',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Antrag auf Erlaubnis zur Untervermietung
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte/r Immobilien Schmidt GmbH,

hiermit bitte ich Sie um Erlaubnis, einen Teil meiner Wohnung unterzuvermieten.

Untermieter:
Name: [Name des Untermieters]
Geburtsdatum: 28.01.2026
Beruf: [Beruf]

Zu untervermietender Bereich:
[z.B. "Ein Zimmer (ca. 15 m²) der 3-Zimmer-Wohnung"]

Zeitraum:
[Befristet vom ... bis ... / Unbefristet ab ...]

Grund für die Untervermietung:
[z.B. "Beruflich bedingter Auslandsaufenthalt" / "Finanzielle Entlastung nach Trennung"]

Gemäß § 553 BGB habe ich einen Anspruch auf Erteilung der Erlaubnis, wenn nach Abschluss des Mietvertrags ein berechtigtes Interesse an der Untervermietung entstanden ist.

Ich bitte um schriftliche Mitteilung Ihrer Entscheidung.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'modernisierung_widerspruch',
    name: 'Widerspruch Modernisierung',
    category: 'Mieter',
    description: 'Härteeinwand gegen Modernisierungsmaßnahme',
    icon: '🏗️',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Härteeinwand gegen angekündigte Modernisierung
Mietobjekt: [Adresse der Wohnung]
Ihr Schreiben vom: [Datum der Modernisierungsankündigung]

Sehr geehrte/r Immobilien Schmidt GmbH,

ich widerspreche der von Ihnen angekündigten Modernisierungsmaßnahme unter Berufung auf § 555d Abs. 2 BGB (Härteeinwand).

Die angekündigten Maßnahmen:
[Beschreibung der geplanten Modernisierung]

Härtegründe:
1. [z.B. "Die zu erwartende Mieterhöhung von [Betrag]€ übersteigt meine finanziellen Möglichkeiten. Mein monatliches Nettoeinkommen beträgt [Betrag]€."]

2. [z.B. "Die Baumaßnahmen würden aufgrund meiner gesundheitlichen Situation (ärztliches Attest liegt bei) eine unzumutbare Belastung darstellen."]

Die Modernisierung würde für mich eine Härte bedeuten, die auch unter Würdigung der berechtigten Interessen des Vermieters nicht zu rechtfertigen ist.

Ich bitte um Berücksichtigung meines Härteeinwands.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: [ggf. Einkommensnachweis, ärztliches Attest]`
  },
  {
    id: 'schoenheitsreparaturen',
    name: 'Ablehnung Schönheitsreparaturen',
    category: 'Mieter',
    description: 'Unwirksame Renovierungsklausel ablehnen',
    icon: '🎨',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Immobilien Schmidt GmbH
Hausverwaltung Straße 5
12345 Berlin

Berlin, den 29.12.2025

Betreff: Ablehnung der geforderten Schönheitsreparaturen
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte/r Immobilien Schmidt GmbH,

Sie fordern mich in Ihrem Schreiben vom 28.01.2026 auf, bei Auszug Schönheitsreparaturen durchzuführen bzw. die Kosten hierfür zu übernehmen.

Diese Forderung weise ich zurück.

Begründung:
Die Schönheitsreparaturklausel in § [Nummer] unseres Mietvertrags ist nach der aktuellen BGH-Rechtsprechung unwirksam, weil:

☐ Die Wohnung wurde mir unrenoviert übergeben (BGH, VIII ZR 185/14)
☐ Die Klausel enthält starre Fristen ohne Berücksichtigung des tatsächlichen Renovierungsbedarfs
☐ Die Farbwahlklausel ist zu eng gefasst (BGH, VIII ZR 224/07)
☐ Die Klausel verpflichtet zu einer Endrenovierung unabhängig vom Zustand

Da die Klausel unwirksam ist, bin ich nicht zur Durchführung von Schönheitsreparaturen verpflichtet. Die Wohnung werde ich besenrein und in dem Zustand zurückgeben, der dem normalen Verschleiß entspricht.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'laermbelaestigung',
    name: 'Beschwerde Lärmbelästigung',
    category: 'Mieter',
    description: 'Lärmbelästigung durch Nachbarn melden',
    icon: '🔊',
    forRoles: ['MIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Vermieters/Hausverwaltung]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Beschwerde wegen anhaltender Lärmbelästigung
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte Damen und Herren,

hiermit beschwere ich mich über anhaltende Lärmbelästigung durch [Nachbar Name/Wohnung Nr.].

Art der Lärmbelästigung:
[z.B. "Laute Musik, Partys, Trampeln, Hundegebell"]

Betroffene Zeiten:
[z.B. "Regelmäßig zwischen 22:00 und 02:00 Uhr, insbesondere an Wochenenden"]

Dokumentierte Vorfälle:
- [Datum, Uhrzeit]: [Beschreibung]
- [Datum, Uhrzeit]: [Beschreibung]
- [Datum, Uhrzeit]: [Beschreibung]

Die Lärmbelästigung beeinträchtigt meine Nachtruhe erheblich und stellt eine Verletzung der Hausordnung sowie eine Störung des Hausfriedens dar.

Ich bitte Sie, den störenden Mieter zur Einhaltung der Ruhezeiten aufzufordern. Sollte die Störung andauern, behalte ich mir vor, die Miete gemäß § 536 BGB zu mindern.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Lärmprotokoll`
  },
  // Eigentümer-Vorlagen
  {
    id: 'antrag_eigentuemerversammlung',
    name: 'Antrag zur Eigentümerversammlung',
    category: 'Eigentümer',
    description: 'TOP für die Eigentümerversammlung beantragen',
    icon: '📋',
    forRoles: ['EIGENTUEMER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Hausverwaltung]
[Adresse der Hausverwaltung]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Antrag auf Aufnahme eines Tagesordnungspunkts
Eigentümergemeinschaft [Name/Adresse der WEG]

Sehr geehrte Damen und Herren,

hiermit beantrage ich, folgenden Tagesordnungspunkt auf die Agenda der nächsten ordentlichen Eigentümerversammlung zu setzen:

TOP: [Bezeichnung des Themas]

Beschlussvorschlag:
[Hier den konkreten Beschlusstext formulieren, z.B. "Die Eigentümergemeinschaft beschließt, die Fassade des Gebäudes im Jahr 2026 zu sanieren. Die Kosten werden aus der Instandhaltungsrücklage finanziert."]

Begründung:
[Hier die Begründung für den Antrag darlegen]

Ich bitte um Bestätigung des Eingangs sowie um Information über die Aufnahme in die Tagesordnung.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'widerspruch_beschluss',
    name: 'Widerspruch gegen WEG-Beschluss',
    category: 'Eigentümer',
    description: 'Einspruch gegen Eigentümerbeschluss',
    icon: '⚖️',
    forRoles: ['EIGENTUEMER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Hausverwaltung]
[Adresse der Hausverwaltung]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Widerspruch gegen Beschluss der Eigentümerversammlung vom 28.01.2026
Eigentümergemeinschaft [Name/Adresse der WEG]
TOP [Nummer]: [Bezeichnung]

Sehr geehrte Damen und Herren,

hiermit widerspreche ich dem in der Eigentümerversammlung vom 28.01.2026 gefassten Beschluss zu TOP [Nummer].

Begründung meines Widerspruchs:

1. [Grund 1, z.B. formeller Mangel]
2. [Grund 2, z.B. inhaltlicher Mangel]

Ich behalte mir vor, den Beschluss gemäß § 44 WEG gerichtlich anzufechten.

Ich bitte um Aufnahme dieses Widerspruchs in die Beschlusssammlung sowie um schriftliche Bestätigung.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Hinweis: Die Anfechtungsfrist beträgt einen Monat ab Beschlussfassung (§ 46 WEG).`
  },
  // Vermieter-Vorlagen
  {
    id: 'mieterhoehung',
    name: 'Mieterhöhung',
    category: 'Vermieter',
    description: 'Mieterhöhung bis zur ortsüblichen Vergleichsmiete',
    icon: '📈',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Mieterhöhungsverlangen gemäß § 558 BGB

Sehr geehrte/r [Name des Mieters],

hiermit mache ich von meinem Recht auf Mietanpassung gemäß § 558 BGB Gebrauch.

Die aktuelle Nettokaltmiete beträgt: [Betrag]€
Die neue Nettokaltmiete soll betragen: [neuer Betrag]€
Erhöhung: [Differenz]€ ([Prozent]%)

Begründung:
Die ortsübliche Vergleichsmiete für vergleichbare Wohnungen liegt gemäß dem Mietspiegel der Stadt [Stadt] bei [Vergleichsmiete]€ pro m². Bei einer Wohnfläche von [qm] m² ergibt sich eine ortsübliche Miete von [Betrag]€.

Ich bitte Sie, der Mieterhöhung zuzustimmen. Die erhöhte Miete wird erstmals für den übernächsten Monat nach Zugang dieses Schreibens fällig, also ab dem 28.01.2026.

Sie haben gemäß § 558b BGB eine Überlegungsfrist bis zum Ablauf des übernächsten Monats.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Auszug aus dem Mietspiegel`
  },
  {
    id: 'abmahnung_mieter',
    name: 'Abmahnung Mieter',
    category: 'Vermieter',
    description: 'Abmahnung wegen Vertragsverletzung',
    icon: '⚠️',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Abmahnung wegen [Art der Vertragsverletzung]
Mietvertrag vom 28.01.2026

Sehr geehrte/r [Name des Mieters],

hiermit mahne ich Sie wegen folgender Vertragsverletzung ab:

[Beschreibung der Vertragsverletzung, z.B.:
- Wiederholte Ruhestörung am [Datum/Uhrzeit]
- Nicht genehmigte Tierhaltung
- Beschädigung des Gemeinschaftseigentums]

Dieses Verhalten stellt eine Verletzung Ihrer Pflichten aus dem Mietvertrag dar, insbesondere [§ des Mietvertrags oder gesetzliche Grundlage].

Ich fordere Sie auf, das vertragswidrige Verhalten unverzüglich einzustellen.

Sollte sich ein gleichartiger oder vergleichbarer Vorfall wiederholen, sehe ich mich gezwungen, das Mietverhältnis fristlos, hilfsweise fristgerecht zu kündigen.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'kuendigung_vermieter',
    name: 'Kündigung durch Vermieter',
    category: 'Vermieter',
    description: 'Ordentliche Kündigung wegen Eigenbedarf',
    icon: '📤',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Per Einschreiben mit Rückschein

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Ordentliche Kündigung des Mietverhältnisses wegen Eigenbedarfs

Sehr geehrte/r [Name des Mieters],

hiermit kündige ich das zwischen uns bestehende Mietverhältnis über die Wohnung Hauptstraße 15, 50667 Köln ordentlich zum [Kündigungstermin].

Kündigungsgrund: Eigenbedarf gemäß § 573 Abs. 2 Nr. 2 BGB

Begründung:
[Detaillierte Begründung des Eigenbedarfs, z.B.:
"Ich benötige die Wohnung für meinen Sohn [Name, geb. am Datum], der derzeit in Berlin wohnt und aufgrund seiner Arbeitsstelle in Berlin eine Wohnung in der Nähe benötigt. Er ist als [Beruf] bei [Arbeitgeber] beschäftigt."]

Die Kündigungsfrist beträgt aufgrund der Mietdauer von [Zeitraum] gemäß § 573c BGB [3/6/9] Monate.

Widerspruchsrecht:
Ich weise Sie darauf hin, dass Sie der Kündigung gemäß § 574 BGB widersprechen können, wenn die Beendigung des Mietverhältnisses für Sie oder Ihre Familie eine besondere Härte bedeuten würde. Der Widerspruch muss schriftlich erfolgen und mir spätestens zwei Monate vor Beendigung des Mietverhältnisses zugehen.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  // Investor-Vorlagen
  {
    id: 'kaufabsicht',
    name: 'Kaufabsichtserklärung',
    category: 'Investor',
    description: 'Verbindliche Kaufabsicht bekunden',
    icon: '🏢',
    forRoles: ['INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

[Ihr Name / Firma]
Musterstraße 12
12345 Berlin

[Name des Verkäufers/Maklers]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Verbindliche Kaufabsichtserklärung
Objekt: [Adresse/Bezeichnung der Immobilie]

Sehr geehrte/r [Name],

nach eingehender Prüfung der von Ihnen übermittelten Unterlagen und der Besichtigung am 28.01.2026 erkläre ich hiermit meine verbindliche Kaufabsicht für das oben genannte Objekt.

Mein Kaufangebot:

Kaufpreis: [Betrag]€ (in Worten: [Betrag in Worten] Euro)

Finanzierung: [Bar/Finanzierung - bei Finanzierung: bereits bestätigte Finanzierungszusage der [Bank] liegt vor]

Notartermin: Ich bin ab 28.01.2026 zeitlich flexibel für einen Beurkundungstermin.

Besondere Vereinbarungen:
- [z.B. Übernahme bestehender Mietverhältnisse]
- [z.B. Inventar/Einbauten]

Dieses Angebot ist gültig bis zum 28.01.2026.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlagen:
- Finanzierungsbestätigung
- Personalausweis (Kopie)`
  },
  {
    id: 'due_diligence',
    name: 'Due-Diligence-Anfrage',
    category: 'Investor',
    description: 'Unterlagen für Immobilienprüfung anfordern',
    icon: '🔍',
    forRoles: ['INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

[Ihr Name / Firma]
Musterstraße 12
12345 Berlin

[Name des Verkäufers/Maklers]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Anforderung Due-Diligence-Unterlagen
Objekt: [Adresse/Bezeichnung der Immobilie]

Sehr geehrte/r [Name],

für die weitere Prüfung des oben genannten Objekts bitte ich um Übersendung folgender Unterlagen:

Rechtliche Unterlagen:
☐ Aktueller Grundbuchauszug (nicht älter als 3 Monate)
☐ Teilungserklärung mit Nachträgen (bei WEG)
☐ Baulastenverzeichnis
☐ Altlastenauskunft

Mietverträge & Einnahmen:
☐ Alle aktuellen Mietverträge inkl. Nachträge
☐ Mieterliste mit Soll-Mieten
☐ Mietrückstandsliste
☐ Nebenkostenabrechnungen der letzten 3 Jahre

Technische Unterlagen:
☐ Baupläne/Grundrisse
☐ Energieausweis
☐ Wartungsnachweise (Heizung, Aufzug)
☐ Aufstellung durchgeführter Instandhaltungen

WEG-Unterlagen (falls zutreffend):
☐ Protokolle der letzten 3 Eigentümerversammlungen
☐ Aktuelle Jahresabrechnung
☐ Wirtschaftsplan
☐ Stand Instandhaltungsrücklage

Ich bitte um Bereitstellung der Unterlagen bis zum 28.01.2026, bevorzugt digital.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'finanzierungsanfrage',
    name: 'Finanzierungsanfrage Bank',
    category: 'Investor',
    description: 'Anfrage zur Immobilienfinanzierung',
    icon: '🏦',
    forRoles: ['INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Bank]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Finanzierungsanfrage Immobilienkauf

Sehr geehrte Damen und Herren,

ich beabsichtige den Erwerb folgender Immobilie und bitte um ein Finanzierungsangebot:

Objektdaten:
Adresse: [Adresse der Immobilie]
Art: [ETW/MFH/Gewerbe]
Baujahr: [Jahr]
Wohnfläche: [qm] m²
Anzahl Einheiten: 2

Kaufpreis und Kosten:
Kaufpreis: [Betrag]€
Grunderwerbsteuer ([X]%): [Betrag]€
Notar & Grundbuch (ca. 2%): [Betrag]€
Maklergebühr: [Betrag]€
Gesamtkosten: [Betrag]€

Finanzierungswunsch:
Eigenkapital: [Betrag]€
Darlehensbetrag: [Betrag]€
Zinsbindung: [10/15/20] Jahre
Tilgung: [2/3]% p.a.

Mieteinnahmen:
Aktuelle Jahresnettokaltmiete: [Betrag]€
Erwartete Mietrendite: [X]%

Zu meiner Person:
Beruf: [Beruf]
Jahresbruttoeinkommen: [Betrag]€
Weitere Immobilien: 2 Objekte, Wert ca. [Betrag]€

Ich bitte um Zusendung eines unverbindlichen Angebots.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlagen:
- Exposé der Immobilie
- Einkommensnachweise
- Selbstauskunft`
  },
  {
    id: 'mietanpassung_kauf',
    name: 'Mietanpassung nach Eigentümerwechsel',
    category: 'Investor',
    description: 'Mieter über Eigentümerwechsel informieren',
    icon: '🔄',
    forRoles: ['INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

[Ihr Name / Firma]
Musterstraße 12
12345 Berlin

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Mitteilung über Eigentümerwechsel
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte/r [Name des Mieters],

hiermit teile ich Ihnen mit, dass ich mit Wirkung zum 28.01.2026 Eigentümer des oben genannten Mietobjekts geworden bin.

Der Eigentumsübergang wurde am 28.01.2026 im Grundbuch eingetragen. Ich trete damit gemäß § 566 BGB in alle Rechte und Pflichten aus dem bestehenden Mietvertrag ein.

Ihr Mietvertrag bleibt unverändert bestehen. Es ergeben sich für Sie keine Änderungen hinsichtlich der Mietbedingungen.

Ab sofort gilt für alle Angelegenheiten folgende Kontaktadresse:

[Ihr Name / Firma]
Hauptstraße 15, 50667 Köln
Telefon: [Nummer]
E-Mail: [E-Mail]

Bitte überweisen Sie die Miete ab dem 28.01.2026 auf folgendes Konto:

Kontoinhaber: [Name]
IBAN: DE89 3704 0044 0532 0130 00
BIC: [BIC]
Verwendungszweck: Miete [Wohnungsbezeichnung]

Ich freue mich auf eine gute Zusammenarbeit.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  // Weitere Vermieter-Vorlagen
  {
    id: 'mahnung_mietrueckstand',
    name: 'Mahnung Mietrückstand',
    category: 'Vermieter',
    description: 'Zahlungserinnerung bei ausstehender Miete',
    icon: '💸',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Mahnung - Mietrückstand
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte/r [Name des Mieters],

bei Durchsicht meiner Unterlagen musste ich feststellen, dass folgende Mietzahlungen noch ausstehen:

Monat [Monat/Jahr]: [Betrag]€
Monat [Monat/Jahr]: [Betrag]€
Gesamt: [Gesamtbetrag]€

Ich fordere Sie auf, den offenen Betrag bis zum [Frist, z.B. 10 Tage] auf folgendes Konto zu überweisen:

IBAN: DE89 3704 0044 0532 0130 00
Verwendungszweck: Miete [Monate] + Nachname

Sollte die Zahlung bereits erfolgt sein, betrachten Sie dieses Schreiben als gegenstandslos und teilen Sie mir bitte das Überweisungsdatum mit.

Ich weise Sie darauf hin, dass ich bei ausbleibendem Zahlungseingang gezwungen bin, rechtliche Schritte einzuleiten. Gemäß § 543 Abs. 2 Nr. 3 BGB bin ich bei einem Mietrückstand von mehr als einer Monatsmiete zur fristlosen Kündigung berechtigt.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'modernisierungsankuendigung',
    name: 'Modernisierungsankündigung',
    category: 'Vermieter',
    description: 'Ankündigung von Modernisierungsmaßnahmen',
    icon: '🏗️',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Ankündigung von Modernisierungsmaßnahmen gemäß § 555c BGB
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte/r [Name des Mieters],

hiermit kündige ich folgende Modernisierungsmaßnahmen an:

1. Art der Maßnahme:
[Detaillierte Beschreibung, z.B. "Erneuerung der Heizungsanlage, Einbau einer modernen Gaszentralheizung mit Brennwerttechnik"]

2. Voraussichtlicher Beginn: 28.01.2026
   Voraussichtliche Dauer: [Zeitraum]

3. Zu erwartende Mieterhöhung:
Gemäß § 559 BGB können 8% der für die Wohnung aufgewendeten Modernisierungskosten auf die Jahresmiete umgelegt werden.

Erwartete Kosten für Ihre Wohnung: [Betrag]€
Monatliche Mieterhöhung: ca. [Betrag]€

4. Voraussichtliche Auswirkungen:
[z.B. "Während der Arbeiten wird die Heizung für ca. 3 Tage nicht zur Verfügung stehen. Ersatzheizgeräte werden gestellt."]

Bitte gewähren Sie den Handwerkern Zutritt zur Wohnung. Die genauen Termine werden rechtzeitig mitgeteilt.

Härteeinwand: Sie können bis zum Ende des Monats, der auf den Zugang dieser Ankündigung folgt, Einwände wegen persönlicher Härte geltend machen (§ 555d Abs. 3 BGB).

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'betriebskostenabrechnung',
    name: 'Betriebskostenabrechnung Anschreiben',
    category: 'Vermieter',
    description: 'Begleitschreiben zur Nebenkostenabrechnung',
    icon: '📊',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

Berlin, den 29.12.2025

Betreff: Betriebskostenabrechnung für das Jahr [Jahr]
Mietobjekt: [Adresse der Wohnung]

Sehr geehrte/r [Name des Mieters],

anbei erhalten Sie die Betriebskostenabrechnung für den Zeitraum vom 28.01.2026 bis zum 28.01.2026.

Zusammenfassung:
Gesamtkosten anteilig: [Betrag]€
Ihre Vorauszahlungen: [Betrag]€

☐ Nachzahlung: [Betrag]€
☐ Guthaben: [Betrag]€

[Bei Nachzahlung:]
Ich bitte Sie, den Nachzahlungsbetrag bis zum [Frist] auf das bekannte Konto zu überweisen.

[Bei Guthaben:]
Das Guthaben wird mit der nächsten Mietzahlung verrechnet / auf Ihr Konto überwiesen.

Anpassung der Vorauszahlung:
Aufgrund der Abrechnung wird die monatliche Vorauszahlung ab 28.01.2026 von [alter Betrag]€ auf [neuer Betrag]€ angepasst.

Die neue Gesamtmiete beträgt: [Betrag]€

Belegeinsicht:
Gemäß § 259 BGB haben Sie das Recht, die Belege einzusehen. Bitte vereinbaren Sie hierzu einen Termin.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Betriebskostenabrechnung [Jahr]`
  },
  {
    id: 'mieterselbstauskunft',
    name: 'Mieterselbstauskunft anfordern',
    category: 'Vermieter',
    description: 'Selbstauskunft von Mietinteressenten',
    icon: '📝',
    forRoles: ['VERMIETER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name des Interessenten]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Mieterselbstauskunft für [Adresse der Wohnung]

Sehr geehrte/r [Name],

vielen Dank für Ihr Interesse an der oben genannten Wohnung.

Um Ihre Bewerbung prüfen zu können, bitte ich Sie, die beiliegende Selbstauskunft auszufüllen und zusammen mit folgenden Unterlagen einzureichen:

☐ Ausgefüllte Selbstauskunft (Anlage)
☐ Kopie des Personalausweises
☐ Gehaltsnachweise der letzten 3 Monate
☐ Mietschuldenfreiheitsbescheinigung des aktuellen Vermieters
☐ SCHUFA-Auskunft (nicht älter als 3 Monate)

Hinweis zum Datenschutz:
Ihre Daten werden ausschließlich zur Prüfung Ihrer Mietbewerbung verwendet und nach Abschluss des Verfahrens gelöscht, sofern kein Mietverhältnis zustande kommt.

Bitte senden Sie die Unterlagen bis zum 28.01.2026 an obige Adresse oder per E-Mail an [E-Mail].

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Formular Mieterselbstauskunft`
  },
  // Weitere Eigentümer-Vorlagen
  {
    id: 'einsicht_unterlagen',
    name: 'Einsicht Verwaltungsunterlagen',
    category: 'Eigentümer',
    description: 'Akteneinsicht bei der Hausverwaltung',
    icon: '📁',
    forRoles: ['EIGENTUEMER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Hausverwaltung]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Antrag auf Einsichtnahme in Verwaltungsunterlagen
Eigentümergemeinschaft: [Name/Adresse der WEG]
Einheit Nr.: [Nummer]

Sehr geehrte Damen und Herren,

als Mitglied der oben genannten Eigentümergemeinschaft beantrage ich gemäß § 18 Abs. 4 WEG Einsicht in folgende Verwaltungsunterlagen:

☐ Jahresabrechnungen der letzten [3] Jahre
☐ Wirtschaftspläne der letzten [3] Jahre
☐ Protokolle der Eigentümerversammlungen
☐ Beschlusssammlung
☐ Verwaltervertrag
☐ Versicherungsverträge
☐ Wartungs- und Serviceverträge
☐ Kontoauszüge des Gemeinschaftskontos
☐ Rechnungen für durchgeführte Instandhaltungen
☐ [Weitere Unterlagen]

Ich bitte um Terminvorschläge für die Einsichtnahme in Ihren Geschäftsräumen oder alternativ um Übersendung von Kopien (Kosten übernehme ich).

Mein Einsichtsrecht ergibt sich aus § 18 Abs. 4 WEG sowie den Grundsätzen ordnungsmäßiger Verwaltung.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  {
    id: 'sondereigentum_aenderung',
    name: 'Antrag Änderung Sondereigentum',
    category: 'Eigentümer',
    description: 'Genehmigung für bauliche Veränderung beantragen',
    icon: '🔨',
    forRoles: ['EIGENTUEMER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Hausverwaltung]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Antrag auf Genehmigung einer baulichen Veränderung
Eigentümergemeinschaft: [Name/Adresse der WEG]
Einheit Nr.: [Nummer]

Sehr geehrte Damen und Herren,

hiermit beantrage ich die Genehmigung für folgende bauliche Maßnahme in/an meinem Sondereigentum:

Geplante Maßnahme:
[Detaillierte Beschreibung, z.B. "Verglasung des Balkons mit Schiebeelementen gemäß beiliegendem Plan"]

Begründung:
[z.B. "Besserer Wetterschutz und erhöhter Wohnkomfort"]

Technische Details:
- Ausführende Firma: [Name]
- Geplanter Zeitraum: [Datum bis Datum]
- Geschätzte Kosten: [Betrag]€ (werden vollständig von mir getragen)

Betroffene Bereiche:
☐ Nur Sondereigentum
☐ Gemeinschaftseigentum ist (nicht wesentlich) betroffen

Ich bitte um Aufnahme als Tagesordnungspunkt in der nächsten Eigentümerversammlung.

Beschlussvorschlag:
"Die Eigentümergemeinschaft genehmigt dem Eigentümer [Name] die [Beschreibung der Maßnahme]. Die Kosten trägt der Antragsteller vollständig."

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlagen:
- Technische Zeichnung/Plan
- Kostenvoranschlag`
  },
  {
    id: 'beschwerde_verwaltung',
    name: 'Beschwerde über Hausverwaltung',
    category: 'Eigentümer',
    description: 'Mängel der Verwaltung beanstanden',
    icon: '📧',
    forRoles: ['EIGENTUEMER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Hausverwaltung]
[Geschäftsführung]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Beschwerde über Verwaltungsmängel
Eigentümergemeinschaft: [Name/Adresse der WEG]

Sehr geehrte Damen und Herren,

als Mitglied der oben genannten Eigentümergemeinschaft muss ich folgende Mängel in der Verwaltungstätigkeit beanstanden:

1. [Mangel 1, z.B.:]
"Die Jahresabrechnung 2024 liegt bis heute nicht vor, obwohl § 28 Abs. 3 WEG eine Vorlage innerhalb von 12 Monaten nach Ablauf des Wirtschaftsjahres verlangt."

2. [Mangel 2, z.B.:]
"Meine Anfragen vom 28.01.2026 und 28.01.2026 zu [Thema] wurden nicht beantwortet."

3. [Mangel 3, z.B.:]
"Der am 28.01.2026 gemeldete Wasserschaden im Treppenhaus wurde bis heute nicht behoben."

Ich fordere Sie auf, die genannten Mängel bis zum [Frist] zu beheben.

Sollte keine Besserung eintreten, behalte ich mir vor:
- Den Vorgang bei der nächsten Eigentümerversammlung zur Sprache zu bringen
- Die Abberufung des Verwalters zu beantragen
- Rechtliche Schritte einzuleiten

Ich erwarte Ihre Stellungnahme bis zum 28.01.2026.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Kopie an: [ggf. Verwaltungsbeirat]`
  },
  {
    id: 'ruecklage_erhoehung',
    name: 'Antrag Erhöhung Instandhaltungsrücklage',
    category: 'Eigentümer',
    description: 'Beschlussantrag zur Rücklagenerhöhung',
    icon: '💰',
    forRoles: ['EIGENTUEMER'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

[Name der Hausverwaltung]
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Antrag auf Erhöhung der Instandhaltungsrücklage
Eigentümergemeinschaft: [Name/Adresse der WEG]

Sehr geehrte Damen und Herren,

hiermit beantrage ich, folgenden Tagesordnungspunkt auf die nächste Eigentümerversammlung zu setzen:

TOP: Erhöhung der Instandhaltungsrücklage

Beschlussvorschlag:
"Die Eigentümergemeinschaft beschließt, die monatliche Zuführung zur Instandhaltungsrücklage von derzeit [aktueller Betrag]€ auf [neuer Betrag]€ pro Monat zu erhöhen. Die Erhöhung erfolgt ab dem 28.01.2026."

Begründung:
1. Die aktuelle Rücklage beträgt ca. [Betrag]€ bei einer Wohnfläche von [qm] m². Das entspricht nur [X]€/m² und liegt deutlich unter dem empfohlenen Wert von mindestens 10€/m².

2. Folgende größere Instandhaltungsmaßnahmen stehen in den nächsten Jahren an:
   - [Maßnahme 1]: geschätzt [Betrag]€
   - [Maßnahme 2]: geschätzt [Betrag]€
   - [Maßnahme 3]: geschätzt [Betrag]€

3. Eine ausreichende Rücklage vermeidet Sonderumlagen und sichert den Werterhalt unserer Immobilie.

Ich bitte um Bestätigung der Aufnahme in die Tagesordnung.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann`
  },
  // Allgemeine Vorlagen
  {
    id: 'vollmacht_immobilie',
    name: 'Vollmacht Immobilienangelegenheiten',
    category: 'Allgemein',
    description: 'Bevollmächtigung für Immobiliensachen',
    icon: '📜',
    forRoles: ['MIETER', 'EIGENTUEMER', 'VERMIETER', 'INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

VOLLMACHT

Hiermit bevollmächtige ich,

Vollmachtgeber:
Name: [Ihr vollständiger Name]
Geburtsdatum: 28.01.2026
Adresse: [Vollständige Adresse]
Personalausweis-Nr.: [Nummer]

den/die Bevollmächtigte/n:

Name: [Name des Bevollmächtigten]
Geburtsdatum: 28.01.2026
Adresse: [Vollständige Adresse]

mich in folgenden Angelegenheiten zu vertreten:

☐ Eigentümerversammlungen der WEG Hauptstraße 15, 50667 Köln
☐ Kommunikation mit der Hausverwaltung
☐ Wohnungsübergaben (Einzug/Auszug)
☐ Unterzeichnung von Mietverträgen
☐ Entgegennahme von Kündigungen
☐ Geltendmachung von Ansprüchen aus dem Mietverhältnis
☐ Sonstiges: [Beschreibung]

Gültigkeitsdauer:
☐ Unbefristet bis zum schriftlichen Widerruf
☐ Befristet vom 28.01.2026 bis 28.01.2026

☐ Untervollmacht ist gestattet
☐ Untervollmacht ist nicht gestattet

Berlin, den 29.12.2025

_____________________________
[Unterschrift Vollmachtgeber]

Ich nehme die Vollmacht an:

_____________________________
[Unterschrift Bevollmächtigter]`
  },
  {
    id: 'grundbuchauskunft',
    name: 'Auskunft Grundbuchamt',
    category: 'Allgemein',
    description: 'Grundbuchauszug anfordern',
    icon: '📋',
    forRoles: ['EIGENTUEMER', 'INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Amtsgericht Berlin
Grundbuchamt
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Antrag auf Erteilung eines Grundbuchauszugs

Sehr geehrte Damen und Herren,

hiermit beantrage ich einen Grundbuchauszug für folgendes Grundstück:

Grundbuch von: [Ort/Gemarkung]
Band: [falls bekannt]
Blatt: [falls bekannt]
Flurstück: [Nummer]
Anschrift: [Adresse des Grundstücks]

Art des Auszugs:
☐ Einfacher Auszug (ohne gelöschte Eintragungen)
☐ Vollständiger Auszug (mit gelöschten Eintragungen)
☐ Beglaubigte Abschrift

Berechtigtes Interesse:
[Begründung, z.B.:]
☐ Ich bin Eigentümer des Grundstücks
☐ Ich beabsichtige den Kauf des Grundstücks (Kaufabsicht liegt vor)
☐ Ich bin Gläubiger einer eingetragenen Grundschuld
☐ Sonstiges: [Begründung]

Die Gebühren in Höhe von [10€ einfach / 20€ beglaubigt] überweise ich nach Erhalt der Rechnung.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlage: Kopie Personalausweis`
  },
  {
    id: 'widerspruch_grundsteuer',
    name: 'Einspruch Grundsteuerbescheid',
    category: 'Allgemein',
    description: 'Widerspruch gegen Grundsteuerwertbescheid',
    icon: '🏛️',
    forRoles: ['EIGENTUEMER', 'INVESTOR'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Max Mustermann
Musterstraße 12
12345 Berlin

Finanzamt Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Berlin, den 29.12.2025

Betreff: Einspruch gegen den Grundsteuerwertbescheid
Aktenzeichen: 12 C 345/24
Steuernummer: [Nummer]
Grundstück: Hauptstraße 15, 50667 Köln

Sehr geehrte Damen und Herren,

gegen den Grundsteuerwertbescheid vom 28.01.2026 lege ich hiermit fristgerecht Einspruch ein.

Begründung:

1. Fehlerhafte Wohnfläche:
Im Bescheid wurde eine Wohnfläche von [angegebene qm] m² zugrunde gelegt. Die tatsächliche Wohnfläche beträgt jedoch nur [korrekte qm] m² gemäß beiliegender Berechnung.

2. [Weiterer Grund, z.B.:]
Der Bodenrichtwert von [Wert]€/m² ist für dieses Grundstück nicht zutreffend, da [Begründung].

3. [Weiterer Grund, z.B.:]
Das Gebäudealter wurde mit [Jahr] angegeben, tatsächlich wurde das Gebäude jedoch erst [Jahr] fertiggestellt.

Antrag:
Ich beantrage die Korrektur des Grundsteuerwerts unter Berücksichtigung der oben genannten Punkte.

Ferner beantrage ich Aussetzung der Vollziehung gemäß § 361 AO.

Mit freundlichen Grüßen

[Unterschrift]
Max Mustermann

Anlagen:
- Wohnflächenberechnung
- [weitere Nachweise]`
  },
  // Anwalt-Vorlagen
  {
    id: 'klage_mietzahlung',
    name: 'Klage auf Mietzahlung',
    category: 'Klagen & Schriftsätze',
    description: 'Klageschrift wegen rückständiger Miete',
    icon: '⚖️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Klage

in Sachen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Beklagten], Hauptstraße 15, 50667 Köln
- Beklagter -

wegen: Mietzahlung
Streitwert: [Betrag]€

Namens und in Vollmacht des Klägers erhebe ich Klage und beantrage:

1. Der Beklagte wird verurteilt, an den Kläger [Betrag]€ nebst Zinsen in Höhe von 5 Prozentpunkten über dem jeweiligen Basiszinssatz seit dem 28.01.2026 zu zahlen.

2. Der Beklagte trägt die Kosten des Rechtsstreits.

3. Das Urteil ist vorläufig vollstreckbar.

Begründung:

I. Sachverhalt

Der Kläger ist Eigentümer und Vermieter der Wohnung Hauptstraße 15, 50667 Köln. Der Beklagte ist Mieter dieser Wohnung aufgrund Mietvertrags vom 28.01.2026.
Beweis: Mietvertrag (Anlage K1)

Die vereinbarte monatliche Miete beträgt [Betrag]€ (Nettokaltmiete) zzgl. [Betrag]€ Betriebskostenvorauszahlung, insgesamt [Betrag]€.

Der Beklagte hat die Miete für folgende Monate nicht gezahlt:
- [Monat/Jahr]: [Betrag]€
- [Monat/Jahr]: [Betrag]€
- [Monat/Jahr]: [Betrag]€
Summe: [Gesamtbetrag]€

Beweis: Kontoauszüge (Anlage K2)

Eine Mahnung erfolgte mit Schreiben vom 28.01.2026.
Beweis: Mahnschreiben (Anlage K3)

II. Rechtliche Würdigung

Der Anspruch auf Zahlung der rückständigen Miete ergibt sich aus § 535 Abs. 2 BGB i.V.m. dem Mietvertrag.

Der Zinsanspruch folgt aus §§ 286, 288 BGB.

[Unterschrift Rechtsanwalt]

Anlagen:
- K1: Mietvertrag
- K2: Kontoauszüge
- K3: Mahnschreiben
- Vollmacht`
  },
  {
    id: 'raeumungsklage',
    name: 'Räumungsklage',
    category: 'Klagen & Schriftsätze',
    description: 'Klage auf Räumung und Herausgabe',
    icon: '🏠',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Klage

in Sachen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Beklagten], [Adresse der Mietsache]
- Beklagter -

wegen: Räumung und Herausgabe
Streitwert: [Jahresmiete = Betrag]€

Namens und in Vollmacht des Klägers erhebe ich Klage und beantrage:

1. Der Beklagte wird verurteilt, die im Hause Hauptstraße 15, 50667 Köln gelegene Wohnung im 3. OG, bestehend aus 2 Zimmern, Küche, Bad, Flur, [weitere Räume], zu räumen und geräumt an den Kläger herauszugeben.

2. Der Beklagte trägt die Kosten des Rechtsstreits.

3. Der Kläger ist berechtigt, die Zwangsvollstreckung gegen Sicherheitsleistung durchzuführen. Die Sicherheitsleistung kann durch selbstschuldnerische Bürgschaft einer deutschen Großbank erbracht werden.

4. Dem Beklagten wird eine Räumungsfrist von [4 Wochen] bewilligt.

Begründung:

I. Sachverhalt

1. Der Kläger ist Eigentümer des Grundstücks Hauptstraße 15, 50667 Köln.
Beweis: Grundbuchauszug (Anlage K1)

2. Der Beklagte bewohnt die streitgegenständliche Wohnung aufgrund Mietvertrags vom 28.01.2026.
Beweis: Mietvertrag (Anlage K2)

3. Mit Schreiben vom 28.01.2026 kündigte der Kläger das Mietverhältnis
☐ ordentlich wegen Eigenbedarfs gemäß § 573 Abs. 2 Nr. 2 BGB
☐ fristlos wegen Zahlungsverzugs gemäß § 543 Abs. 2 Nr. 3 BGB
☐ fristlos wegen vertragswidrigen Verhaltens gemäß § 543 BGB
zum 28.01.2026.
Beweis: Kündigungsschreiben (Anlage K3)

4. [Bei Zahlungsverzug:]
Der Beklagte schuldet zum Zeitpunkt der Kündigung Miete für mehr als zwei Monate in Höhe von [Betrag]€.
Beweis: Kontoauszüge (Anlage K4)

5. Der Beklagte hat die Wohnung trotz Aufforderung nicht geräumt.

II. Rechtliche Würdigung

Der Räumungsanspruch ergibt sich aus § 546 Abs. 1 BGB.

Das Mietverhältnis ist durch die wirksame Kündigung vom 28.01.2026 beendet worden.

[Unterschrift Rechtsanwalt]

Anlagen:
- K1: Grundbuchauszug
- K2: Mietvertrag
- K3: Kündigungsschreiben
- K4: Kontoauszüge/Nachweis Zahlungsrückstand
- Vollmacht`
  },
  {
    id: 'klageerwiderung',
    name: 'Klageerwiderung Mietrecht',
    category: 'Klagen & Schriftsätze',
    description: 'Verteidigung gegen Räumungs- oder Zahlungsklage',
    icon: '🛡️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Klageerwiderung

in Sachen

[Name des Klägers]
- Kläger -

gegen

[Name des Mandanten]
- Beklagter -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

wegen: [Räumung/Mietzahlung]

Namens und in Vollmacht des Beklagten beantrage ich:

Die Klage wird abgewiesen.

Hilfsweise:

Dem Beklagten wird eine angemessene Räumungsfrist gewährt.

Begründung:

I. Sachverhalt

Der Sachvortrag des Klägers wird mit folgenden Maßgaben bestritten:

1. [Bestrittener Punkt 1]
Beweis: [Beweismittel]

2. [Bestrittener Punkt 2]
Beweis: [Beweismittel]

II. Rechtliche Würdigung

Die Klage ist unbegründet.

1. [Erstes Argument, z.B.:]
Die Kündigung ist formunwirksam, da [Begründung fehlt/nicht ausreichend konkret].
Vgl. BGH, Urteil vom 28.01.2026, Az. [Az.]

2. [Zweites Argument, z.B.:]
Die Kündigung ist materiell unwirksam, da [Eigenbedarf nicht nachgewiesen/vorgeschoben].

3. [Bei Mietminderung:]
Die Miete war gemäß § 536 BGB kraft Gesetzes gemindert. Der Beklagte hat den Mangel am 28.01.2026 angezeigt.
Beweis: Mängelanzeige (Anlage B1)

III. Hilfsweise: Härteeinwand

Für den Fall, dass das Gericht die Kündigung für wirksam erachten sollte:

Der Beklagte widerspricht der Kündigung gemäß § 574 BGB wegen besonderer Härte:
- [Härtegrund 1, z.B. hohes Alter, Krankheit]
- [Härtegrund 2, z.B. lange Mietdauer, keine Ersatzwohnung verfügbar]

Beweis: [Ärztliches Attest/Wohnungssuche-Nachweise] (Anlage B2)

[Unterschrift Rechtsanwalt]

Anlagen:
- B1: [Anlage]
- B2: [Anlage]
- Vollmacht`
  },
  {
    id: 'mahnbescheid_antrag',
    name: 'Antrag Mahnbescheid',
    category: 'Kündigungen & Mahnungen',
    description: 'Antrag auf Erlass eines Mahnbescheids',
    icon: '📋',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht [zuständiges Mahngericht]
- Mahnabteilung -
Hauptstraße 15, 50667 Köln
12345 Berlin

Antrag auf Erlass eines Mahnbescheids

Antragsteller:
[Name/Firma des Mandanten]
Hauptstraße 15, 50667 Köln
12345 Berlin

Prozessbevollmächtigte:
Rechtsanwaltskanzlei Dr. Schneider & Partner
Hauptstraße 15, 50667 Köln

Antragsgegner:
[Name des Schuldners]
Hauptstraße 15, 50667 Köln
12345 Berlin

Ich beantrage namens und in Vollmacht des Antragstellers den Erlass eines Mahnbescheids über folgende Forderung:

Hauptforderung:

1. Rückständige Miete [Monate] gemäß Mietvertrag vom 28.01.2026
   über die Wohnung Hauptstraße 15, 50667 Köln
   Betrag: [Betrag]€

2. [ggf. weitere Position:]
   Nebenkostennachzahlung [Jahr]
   Betrag: [Betrag]€

Summe Hauptforderung: [Betrag]€

Nebenforderungen:

Zinsen: 5 Prozentpunkte über dem jeweiligen Basiszinssatz
ab: 28.01.2026 (Verzugseintritt)
auf: [Hauptforderung]€

Vorgerichtliche Rechtsanwaltskosten:
Gegenstandswert: [Betrag]€
1,3 Geschäftsgebühr Nr. 2300 VV RVG: [Betrag]€
Auslagenpauschale Nr. 7002 VV RVG: [Betrag]€
19% USt.: [Betrag]€
Summe: [Betrag]€

Mahnkosten: [Betrag]€

Gesamtbetrag: [Betrag]€

Anspruchsgrundlage: § 535 Abs. 2 BGB, Mietvertrag

Zuständiges Gericht für streitiges Verfahren:
Amtsgericht Berlin (Belegenheit der Mietsache)

Die Gerichtskosten sollen durch Lastschrift eingezogen werden.
Gläubiger-ID: [ID]
Mandatsreferenz: [Referenz]

[Unterschrift Rechtsanwalt]

Anlage: Vollmacht`
  },
  {
    id: 'abmahnung_anwalt',
    name: 'Anwaltliche Abmahnung',
    category: 'Kündigungen & Mahnungen',
    description: 'Außergerichtliche Abmahnung durch Anwalt',
    icon: '⚠️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

Per Einschreiben/Rückschein

[Name des Gegners]
Hauptstraße 15, 50667 Köln
12345 Berlin

28.01.2026

Unser Zeichen: [Az.]
Ihr Zeichen: -

Betreff: Außergerichtliche Interessenvertretung [Mandantenname] ./. Sie
hier: Abmahnung wegen [Sachverhalt]

Sehr geehrte/r [Name],

in obiger Angelegenheit zeige ich an, dass ich [Mandantenname], Hauptstraße 15, 50667 Köln, anwaltlich vertrete. Eine entsprechende Vollmacht ist beigefügt.

Mein Mandant hat mich beauftragt, folgende Angelegenheit außergerichtlich zu klären:

Sachverhalt:
[Detaillierte Darstellung des Sachverhalts]

Rechtliche Bewertung:
Ihr Verhalten stellt eine Verletzung von [Rechtsnorm/Vertragspflicht] dar.

[Bei Mietrückstand:]
Sie schulden meinem Mandanten rückständige Miete in Höhe von [Betrag]€ für die Monate [Auflistung].

[Bei Vertragsverletzung:]
Ihr Verhalten verstößt gegen § [X] des Mietvertrags vom 28.01.2026.

Aufforderung:
Namens und im Auftrag meines Mandanten fordere ich Sie auf:

1. [Konkrete Forderung, z.B. Zahlung von [Betrag]€]
2. [ggf. Unterlassung des vertragswidrigen Verhaltens]

Frist: 28.01.2026 (14 Tage ab Zugang)

Sollten Sie dieser Aufforderung nicht fristgemäß nachkommen, werde ich meinen Mandanten anweisen, gerichtliche Schritte einzuleiten. Die dadurch entstehenden weiteren Kosten werden Sie zu tragen haben.

Kosten dieser anwaltlichen Tätigkeit:
Gegenstandswert: [Betrag]€
1,3 Geschäftsgebühr: [Betrag]€
Auslagenpauschale: [Betrag]€
19% USt.: [Betrag]€
Gesamt: [Betrag]€

Diese Kosten sind von Ihnen gemäß § 286 BGB zu erstatten.

Mit freundlichen Grüßen

[Unterschrift]
[Rechtsanwalt Name]

Anlage: Vollmacht`
  },
  {
    id: 'vergleichsvorschlag',
    name: 'Vergleichsvorschlag',
    category: 'Musterbriefe',
    description: 'Außergerichtlicher Vergleichsvorschlag',
    icon: '🤝',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

[Gegnerischer Anwalt/Gegner]
Hauptstraße 15, 50667 Köln
12345 Berlin

28.01.2026

Unser Zeichen: [Az.]
Ihr Zeichen: [Az.]

Betreff: [Mandant] ./. [Gegner]
hier: Vergleichsvorschlag

Sehr geehrte/r Kollege/Kollegin, [oder: Sehr geehrte/r Name]

in obiger Angelegenheit unterbreite ich namens meines Mandanten folgenden Vergleichsvorschlag zur gütlichen Beilegung der Streitigkeit:

Vergleich

1. [Erste Regelung, z.B.:]
Die Parteien sind sich einig, dass das Mietverhältnis über die Wohnung Hauptstraße 15, 50667 Köln einvernehmlich zum 28.01.2026 beendet wird.

2. [Zweite Regelung, z.B.:]
Der Beklagte verpflichtet sich, die Wohnung bis zum 28.01.2026 geräumt und besenrein an den Kläger herauszugeben.

3. [Dritte Regelung, z.B.:]
Der Kläger verzichtet auf die Geltendmachung rückständiger Miete in Höhe von [Betrag]€ / Der Beklagte zahlt in Raten [Betrag]€ monatlich.

4. [Regelung zur Kaution:]
Die Kaution in Höhe von [Betrag]€ wird nach Ablauf der 6-monatigen Abrechnungsfrist an den Beklagten ausgezahlt / mit den Forderungen des Klägers verrechnet.

5. [Kostenregelung:]
Die Kosten des Rechtsstreits werden gegeneinander aufgehoben / trägt der [Kläger/Beklagte].

Jede Partei trägt ihre außergerichtlichen Kosten selbst.

6. Mit diesem Vergleich sind alle wechselseitigen Ansprüche aus dem Mietverhältnis abgegolten.

Ich bitte um Mitteilung, ob Ihre Partei mit dem Vergleich einverstanden ist, bis zum 28.01.2026.

Mit kollegialen Grüßen

[Unterschrift]
[Rechtsanwalt Name]`
  },
  {
    id: 'kuendigung_eigenbedarf_anwalt',
    name: 'Kündigung Eigenbedarf (Anwalt)',
    category: 'Kündigungen & Mahnungen',
    description: 'Eigenbedarfskündigung mit allen Formalien',
    icon: '📤',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

Per Einschreiben/Rückschein

An alle Mieter der Wohnung Hauptstraße 15, 50667 Köln:

[Name Mieter 1]
[Name Mieter 2 - falls vorhanden]
[Adresse der Mietsache]
12345 Berlin

28.01.2026

Unser Zeichen: [Az.]

Ordentliche Kündigung des Mietverhältnisses wegen Eigenbedarfs

Sehr geehrte/r [Name(n)],

in Vertretung von [Mandantenname], Hauptstraße 15, 50667 Köln, Eigentümer der von Ihnen gemieteten Wohnung, kündige ich das zwischen Ihnen und meinem Mandanten bestehende Mietverhältnis über die Wohnung

[genaue Adresse],
3. OG, [Lage links/rechts/Mitte],
bestehend aus 2 Zimmern, Küche, Bad, [weitere Räume],

ordentlich gemäß § 573 Abs. 2 Nr. 2 BGB wegen Eigenbedarfs

zum [Kündigungstermin]

hilfsweise zum nächstmöglichen Termin.

I. Kündigungsgrund: Eigenbedarf

Mein Mandant benötigt die Wohnung für [Bedarfsperson]:

Name: [vollständiger Name]
Geburtsdatum: 28.01.2026
Verwandtschaftsverhältnis: [z.B. Tochter/Sohn/Mutter/Vater/Enkel]
Aktuelle Wohnsituation: [z.B. wohnt zur Miete in Berlin, 2-Zimmer-Wohnung]

Begründung des Wohnbedarfs:
[Ausführliche, konkrete Begründung, z.B.:]
"Die Tochter meines Mandanten, Frau [Name], hat am 28.01.2026 eine Arbeitsstelle als [Beruf] bei [Arbeitgeber] in Berlin angetreten. Ihr bisheriger Wohnort Berlin liegt ca. [X] km von der Arbeitsstelle entfernt. Ein tägliches Pendeln ist unzumutbar. Die Wohnung meines Mandanten befindet sich in unmittelbarer Nähe zur Arbeitsstelle (ca. [X] km)."

II. Kündigungsfrist

Das Mietverhältnis besteht seit dem [Datum des Mietvertragsbeginns], mithin seit [X Jahren/Monaten]. Die Kündigungsfrist beträgt gemäß § 573c Abs. 1 BGB daher [3/6/9] Monate.

III. Widerspruchsrecht

Gemäß §§ 574 ff. BGB können Sie der Kündigung widersprechen, wenn die Beendigung des Mietverhältnisses für Sie, Ihre Familie oder andere Haushaltsangehörige eine Härte bedeuten würde, die auch unter Würdigung der berechtigten Interessen des Vermieters nicht zu rechtfertigen ist.

Der Widerspruch muss schriftlich erfolgen und dem Vermieter spätestens zwei Monate vor Beendigung des Mietverhältnisses zugegangen sein.

IV. Kein Angebot einer Ersatzwohnung

☐ Meinem Mandanten steht keine vergleichbare Wohnung zur Verfügung.
☐ Eine Ersatzwohnung wird angeboten: [Details]

Mit freundlichen Grüßen

[Unterschrift]
[Rechtsanwalt Name]

Anlagen:
- Vollmacht`
  },
  {
    id: 'fristlose_kuendigung_anwalt',
    name: 'Fristlose Kündigung (Anwalt)',
    category: 'Kündigungen & Mahnungen',
    description: 'Außerordentliche Kündigung wegen Zahlungsverzug',
    icon: '🚨',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

Per Einschreiben/Rückschein UND Boten

[Name des Mieters]
[Adresse der Mietsache]
12345 Berlin

28.01.2026

Unser Zeichen: [Az.]

Außerordentliche fristlose Kündigung, hilfsweise ordentliche Kündigung

Sehr geehrte/r [Name],

in Vertretung von [Mandantenname], Eigentümer und Vermieter der von Ihnen gemieteten Wohnung Hauptstraße 15, 50667 Köln, kündige ich das zwischen Ihnen bestehende Mietverhältnis

außerordentlich fristlos gemäß § 543 Abs. 2 Nr. 3 BGB,

hilfsweise ordentlich gemäß § 573 Abs. 2 Nr. 1 BGB zum [nächstmöglicher Termin].

I. Kündigungsgrund

Sie befinden sich mit der Mietzahlung erheblich in Verzug.

Folgende Mieten sind offen:

| Monat | Fällig seit | Betrag |
|-------|-------------|--------|
| [Monat/Jahr] | 28.01.2026 | [Betrag]€ |
| [Monat/Jahr] | 28.01.2026 | [Betrag]€ |
| [Monat/Jahr] | 28.01.2026 | [Betrag]€ |
|**Gesamt:** | | **[Summe]€** |

Der Rückstand übersteigt damit die Miete für zwei aufeinanderfolgende Termine / erreicht einen Betrag, der der Miete für zwei Monate entspricht.

II. Voraussetzungen der fristlosen Kündigung

Die Voraussetzungen des § 543 Abs. 2 Nr. 3 BGB sind erfüllt:
- Die Miete ist gemäß § [X] des Mietvertrags jeweils zum [3. Werktag] im Voraus fällig
- Sie befinden sich mit mehr als einer Monatsmiete länger als einen Monat in Verzug
  ODER mit einem Betrag, der zwei Monatsmieten erreicht, in Verzug

III. Abwendung der Kündigung

Ich weise Sie darauf hin, dass die fristlose Kündigung gemäß § 569 Abs. 3 Nr. 2 BGB unwirksam wird, wenn Sie den gesamten Rückstand in Höhe von [Betrag]€ innerhalb von zwei Monaten nach Zustellung der Räumungsklage begleichen.

Dies gilt jedoch nicht, wenn innerhalb der letzten zwei Jahre bereits einmal wegen Zahlungsverzugs gekündigt wurde und diese Kündigung durch Zahlung unwirksam wurde.

IV. Aufforderung zur Räumung

Ich fordere Sie auf, die Wohnung bis spätestens [Datum = 2 Wochen] zu räumen und ordnungsgemäß an meinen Mandanten herauszugeben.

Sollten Sie dieser Aufforderung nicht nachkommen, werde ich unverzüglich Räumungsklage erheben.

Mit freundlichen Grüßen

[Unterschrift]
[Rechtsanwalt Name]

Anlagen:
- Vollmacht
- Aufstellung Mietrückstand`
  },
  {
    id: 'vollstreckungsauftrag',
    name: 'Vollstreckungsauftrag Räumung',
    category: 'Klagen & Schriftsätze',
    description: 'Auftrag an Gerichtsvollzieher zur Zwangsräumung',
    icon: '🔐',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An den
Gerichtsvollzieher bei dem Amtsgericht Berlin
Verteilerstelle
Hauptstraße 15, 50667 Köln
12345 Berlin

28.01.2026

Unser Zeichen: [Az.]

Vollstreckungsauftrag - Räumung

Gläubiger:
[Name des Mandanten]
Hauptstraße 15, 50667 Köln
12345 Berlin

Prozessbevollmächtigte:
Rechtsanwaltskanzlei Dr. Schneider & Partner
Hauptstraße 15, 50667 Köln

Schuldner:
[Name des Räumungsschuldners]
Bisher wohnhaft: [Adresse der zu räumenden Wohnung]
12345 Berlin

Sehr geehrte Damen und Herren,

namens und im Auftrag des Gläubigers erteile ich den Auftrag zur Zwangsvollstreckung wie folgt:

Titel:
Urteil des Amtsgerichts Berlin vom 28.01.2026, Az. 12 C 345/24
☐ mit vorläufiger Vollstreckbarkeit gegen Sicherheitsleistung
☐ ohne Sicherheitsleistung (rechtskräftig seit 28.01.2026)

Vollstreckungsmaßnahme:

1. Räumung der Wohnung
[genaue Adresse]
3. OG, [Lage]
bestehend aus 2 Zimmern, Küche, Bad, [Kellerraum, Stellplatz etc.]

2. Herausgabe der Schlüssel

3. Einweisung des Gläubigers in den Besitz

Hinweise:

☐ Es handelt sich um eine "Berliner Räumung" (§ 885a ZPO). Der Gläubiger verzichtet auf die Mitnahme beweglicher Sachen. Es wird nur um Besitzeinweisung gebeten.

☐ Klassische Räumung mit Abtransport. Ein Spediteur wird beauftragt.

Der Schuldner ist nach Kenntnis des Gläubigers:
☐ allein wohnhaft
☐ mit 2 weiteren Personen wohnhaft

Kostenvorschuss:
Ein Kostenvorschuss in Höhe von [Betrag]€ wird überwiesen / liegt als Verrechnungsscheck bei.

Ich bitte um:
1. Terminmitteilung mindestens 3 Wochen im Voraus
2. Vorab-Information über voraussichtliche Kosten
3. Benachrichtigung bei Vollstreckungshindernissen

Mit freundlichen Grüßen

[Unterschrift]
[Rechtsanwalt Name]

Anlagen:
- Vollstreckbare Ausfertigung des Titels
- Zustellungsnachweis
- Vollmacht
- Kostenvorschuss (Scheck/Überweisungsträger)`
  },
  {
    id: 'widerspruch_weg_beschluss_anwalt',
    name: 'Anfechtungsklage WEG-Beschluss',
    category: 'Klagen & Schriftsätze',
    description: 'Klage auf Ungültigerklärung eines WEG-Beschlusses',
    icon: '🏛️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Klage

in Sachen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Verwalters] als Zustellungsbevollmächtigter
der Wohnungseigentümergemeinschaft [Adresse der WEG]
Hauptstraße 15, 50667 Köln
- Beklagte -

wegen: Anfechtung von Beschlüssen der Eigentümerversammlung
Streitwert: [Betrag]€

Namens und in Vollmacht des Klägers erhebe ich Klage und beantrage:

1. Der in der Eigentümerversammlung vom 28.01.2026 zu TOP [Nummer] gefasste Beschluss "[Wortlaut des Beschlusses]" wird für ungültig erklärt.

2. Die Beklagte trägt die Kosten des Rechtsstreits.

3. Das Urteil ist vorläufig vollstreckbar.

Begründung:

I. Zulässigkeit

1. Der Kläger ist Mitglied der beklagten Wohnungseigentümergemeinschaft als Eigentümer der Einheit Nr. [Nummer].
Beweis: Grundbuchauszug (Anlage K1)

2. Die Klage ist fristgerecht erhoben. Die Eigentümerversammlung fand am 28.01.2026 statt. Die Monatsfrist des § 45 WEG ist gewahrt.

II. Begründetheit

Der angefochtene Beschluss ist für ungültig zu erklären.

A. Formelle Mängel

[z.B.:]
1. Die Einladungsfrist des § 24 Abs. 4 S. 2 WEG (3 Wochen) wurde nicht eingehalten.
Beweis: Einladungsschreiben (Anlage K2)

2. Die Tagesordnung war nicht hinreichend bestimmt.

B. Materielle Mängel

[z.B.:]
1. Der Beschluss widerspricht den Grundsätzen ordnungsmäßiger Verwaltung (§ 19 Abs. 1 WEG).

2. Der Beschluss überschreitet die Beschlusskompetenz der Eigentümergemeinschaft.

3. Der Beschluss verstößt gegen die Teilungserklärung.

III. Aussetzung der Vollziehung

Ich beantrage ferner, die Vollziehung des angefochtenen Beschlusses bis zur rechtskräftigen Entscheidung auszusetzen (§ 44 Abs. 3 WEG).

[Unterschrift Rechtsanwalt]

Anlagen:
- K1: Grundbuchauszug
- K2: Einladung zur Eigentümerversammlung
- K3: Protokoll der Eigentümerversammlung
- Vollmacht`
  },
  {
    id: 'mietminderung_klage',
    name: 'Klage auf Mietminderung/Mangelbeseitigung',
    category: 'Klagen & Schriftsätze',
    description: 'Klage des Mieters auf Mangelbeseitigung',
    icon: '🔧',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Klage

in Sachen

[Name des Mandanten/Mieters], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

Immobilien Schmidt GmbH, Hauptstraße 15, 50667 Köln
- Beklagter -

wegen: Mangelbeseitigung, Feststellung Mietminderung
Streitwert: [Betrag]€

Namens und in Vollmacht des Klägers erhebe ich Klage und beantrage:

1. Der Beklagte wird verurteilt, den Mangel [genaue Beschreibung, z.B. "Schimmelbefall an der Nordwand des Schlafzimmers"] in der vom Kläger gemieteten Wohnung Hauptstraße 15, 50667 Köln fachgerecht zu beseitigen.

2. Es wird festgestellt, dass die Miete für die Wohnung Hauptstraße 15, 50667 Köln seit dem 28.01.2026 um [X]% gemindert ist.

3. Der Beklagte wird verurteilt, an den Kläger überzahlte Miete in Höhe von [Betrag]€ nebst Zinsen in Höhe von 5 Prozentpunkten über dem Basiszinssatz seit Rechtshängigkeit zurückzuzahlen.

4. Der Beklagte trägt die Kosten des Rechtsstreits.

Begründung:

I. Sachverhalt

1. Der Kläger ist Mieter der Wohnung Hauptstraße 15, 50667 Köln aufgrund Mietvertrags vom 28.01.2026.
Beweis: Mietvertrag (Anlage K1)

2. Die monatliche Miete beträgt [Betrag]€.

3. Seit 28.01.2026 besteht folgender Mangel:
[Detaillierte Beschreibung des Mangels]
Beweis: Fotos (Anlage K2), Sachverständigengutachten (Anlage K3)

4. Der Kläger hat den Mangel mit Schreiben vom 28.01.2026 angezeigt.
Beweis: Mängelanzeige (Anlage K4)

5. Trotz Fristsetzung bis zum 28.01.2026 hat der Beklagte den Mangel nicht beseitigt.

II. Rechtliche Würdigung

1. Der Anspruch auf Mangelbeseitigung ergibt sich aus § 535 Abs. 1 S. 2 BGB.

2. Die Mietminderung tritt kraft Gesetzes gemäß § 536 Abs. 1 BGB ein.

3. Nach der Rechtsprechung zu vergleichbaren Mängeln ist eine Minderung von [X]% angemessen.
Vgl. [Rechtsprechungsnachweis]

[Unterschrift Rechtsanwalt]

Anlagen:
- K1: Mietvertrag
- K2: Fotos des Mangels
- K3: Sachverständigengutachten (falls vorhanden)
- K4: Mängelanzeige
- Vollmacht`
  },
  {
    id: 'schadensersatz_vermieter',
    name: 'Klage auf Schadensersatz (Vermieter)',
    category: 'Klagen & Schriftsätze',
    description: 'Schadensersatzklage wegen Beschädigung der Mietsache',
    icon: '💰',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Klage

in Sachen

[Name des Mandanten/Vermieters], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des ehemaligen Mieters], [neue Adresse]
- Beklagter -

wegen: Schadensersatz
Streitwert: [Betrag]€

Namens und in Vollmacht des Klägers erhebe ich Klage und beantrage:

1. Der Beklagte wird verurteilt, an den Kläger [Betrag]€ nebst Zinsen in Höhe von 5 Prozentpunkten über dem Basiszinssatz seit dem 28.01.2026 zu zahlen.

2. Der Beklagte trägt die Kosten des Rechtsstreits.

3. Das Urteil ist vorläufig vollstreckbar.

Begründung:

I. Sachverhalt

1. Der Beklagte war Mieter der Wohnung Hauptstraße 15, 50667 Köln aufgrund Mietvertrags vom 28.01.2026.
Beweis: Mietvertrag (Anlage K1)

2. Das Mietverhältnis endete am 28.01.2026. Die Wohnung wurde am 28.01.2026 zurückgegeben.
Beweis: Übergabeprotokoll (Anlage K2)

3. Bei der Übergabe wurden folgende Schäden festgestellt, die über normale Abnutzung hinausgehen:

| Schaden | Kosten |
|---------|--------|
| [Beschreibung 1] | [Betrag]€ |
| [Beschreibung 2] | [Betrag]€ |
| [Beschreibung 3] | [Betrag]€ |
| **Gesamt:** | **[Summe]€** |

Beweis: Übergabeprotokoll (Anlage K2), Fotos (Anlage K3), Kostenvoranschlag (Anlage K4)

4. Die Mietkaution in Höhe von [Betrag]€ wurde bereits verrechnet. Es verbleibt ein Restschaden von [Betrag]€.

II. Rechtliche Würdigung

Der Anspruch ergibt sich aus § 280 Abs. 1 BGB i.V.m. § 535 BGB.

Der Beklagte hat seine Obhutspflichten aus dem Mietvertrag verletzt. Die Schäden gehen über die normale Abnutzung hinaus und sind vom Beklagten zu vertreten.

[Unterschrift Rechtsanwalt]

Anlagen:
- K1: Mietvertrag
- K2: Übergabeprotokoll
- K3: Fotos der Schäden
- K4: Kostenvoranschläge/Rechnungen
- Vollmacht`
  },
  {
    id: 'berufung_mietrecht',
    name: 'Berufung Mietrecht',
    category: 'Klagen & Schriftsätze',
    description: 'Berufungsschrift gegen erstinstanzliches Urteil',
    icon: '📑',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Landgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Berufung

In dem Rechtsstreit

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger und Berufungskläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Gegners], Hauptstraße 15, 50667 Köln
- Beklagter und Berufungsbeklagter -

wegen: [Räumung/Mietzahlung/etc.]

Az. erstinstanzlich: [Aktenzeichen AG]
Urteil des Amtsgerichts Berlin vom 28.01.2026

lege ich namens und in Vollmacht des Klägers gegen das am 28.01.2026 zugestellte Urteil des Amtsgerichts Berlin vom 28.01.2026

Berufung

ein.

Die Berufungsbegründung wird innerhalb der Berufungsbegründungsfrist nachgereicht.

Vorsorglich beantrage ich bereits jetzt:

1. Das Urteil des Amtsgerichts Berlin vom 28.01.2026, Az. [Az.], wird aufgehoben.

2. [Anträge entsprechend der Erstinstanz]

3. Der Beklagte trägt die Kosten beider Rechtszüge.

4. Das Urteil ist vorläufig vollstreckbar.

Streitwert: [Betrag]€

[Unterschrift Rechtsanwalt]

Anlage: Vollmacht

---

[Berufungsbegründung - separates Schreiben:]

Berufungsbegründung

In dem Rechtsstreit [wie oben]

begründe ich die Berufung wie folgt:

I. Kurze Zusammenfassung des Sachverhalts

[Sachverhalt]

II. Fehlerhafte Tatsachenfeststellung

Das Amtsgericht hat folgenden Sachverhalt fehlerhaft festgestellt:
[Darstellung]

III. Rechtsfehler

Das Amtsgericht hat folgende Rechtsnormen fehlerhaft angewendet:

1. [Rechtsnorm 1] wurde fehlerhaft ausgelegt, weil [Begründung].

2. Die Rechtsprechung des BGH zu [Thema] wurde nicht beachtet.
Vgl. BGH, Urteil vom 28.01.2026, Az. [Az.]

IV. Ergebnis

Bei zutreffender Würdigung hätte das Amtsgericht der Klage stattgeben müssen.

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'einstweilige_verfuegung',
    name: 'Antrag einstweilige Verfügung',
    category: 'Klagen & Schriftsätze',
    description: 'Eilantrag bei dringenden Mietstreitigkeiten',
    icon: '⚡',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

EILT! - Antrag auf Erlass einer einstweiligen Verfügung

In Sachen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Antragsteller -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Gegners], Hauptstraße 15, 50667 Köln
- Antragsgegner -

wegen: [Unterlassung/Besitzstörung/etc.]
Streitwert: [Betrag]€

beantrage ich namens und in Vollmacht des Antragstellers den Erlass einer einstweiligen Verfügung, auch ohne mündliche Verhandlung:

1. Dem Antragsgegner wird bei Meidung eines Ordnungsgeldes bis zu 250.000€, ersatzweise Ordnungshaft, oder Ordnungshaft bis zu 6 Monaten für jeden Fall der Zuwiderhandlung untersagt,

[Konkretes Verbot, z.B.:]
☐ die Wohnung des Antragstellers Hauptstraße 15, 50667 Köln ohne dessen Zustimmung zu betreten.
☐ Bauarbeiten in der Wohnung des Antragstellers durchzuführen.
☐ die Versorgung der Wohnung mit [Strom/Wasser/Heizung] zu unterbrechen.

2. Der Antragsgegner trägt die Kosten des Verfahrens.

Begründung:

I. Sachverhalt (Verfügungsanspruch)

[Darstellung des Sachverhalts]

Glaubhaftmachung: Eidesstattliche Versicherung (Anlage ASt 1)

II. Dringlichkeit (Verfügungsgrund)

Die Sache ist dringlich, weil:
[Begründung der Dringlichkeit, z.B.:]
- Der Antragsgegner hat angekündigt, [Handlung] am 28.01.2026 durchzuführen.
- Dem Antragsteller drohen irreparable Nachteile.
- Ein Hauptsacheverfahren würde zu spät kommen.

III. Rechtliche Würdigung

Der Anspruch ergibt sich aus §§ [935, 940 ZPO i.V.m. materielle Rechtsgrundlage].

[Unterschrift Rechtsanwalt]

Anlagen:
- ASt 1: Eidesstattliche Versicherung
- Vollmacht`
  },
  {
    id: 'prozesskostenhilfe',
    name: 'Antrag Prozesskostenhilfe',
    category: 'Klagen & Schriftsätze',
    description: 'PKH-Antrag für bedürftige Mandanten',
    icon: '📋',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: [falls vorhanden]

Antrag auf Bewilligung von Prozesskostenhilfe

In Sachen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger/Beklagter -

gegen

[Name des Gegners], Hauptstraße 15, 50667 Köln
- Beklagter/Kläger -

wegen: [Streitgegenstand]

beantrage ich namens und in Vollmacht des [Klägers/Beklagten]:

1. Dem [Kläger/Beklagten] wird für die beabsichtigte Klage / die Rechtsverteidigung Prozesskostenhilfe ohne Ratenzahlung bewilligt.

2. Dem [Kläger/Beklagten] wird [Rechtsanwalt Name] beigeordnet.

Begründung:

I. Bedürftigkeit

Der Antragsteller ist nicht in der Lage, die Kosten der Prozessführung aufzubringen.

Sein monatliches Nettoeinkommen beträgt: [Betrag]€
Vermögen: [Beschreibung oder "keines"]
Monatliche Belastungen: [Miete, Unterhalt etc.]

Beweis: Erklärung über die persönlichen und wirtschaftlichen Verhältnisse (Anlage)

II. Erfolgsaussicht

Die beabsichtigte Rechtsverfolgung / Rechtsverteidigung bietet hinreichende Aussicht auf Erfolg und ist nicht mutwillig.

[Kurze Darstellung des Sachverhalts und der Rechtslage]

III. Beabsichtigte Klage / Rechtsverteidigung

☐ Es soll Klage erhoben werden mit den Anträgen:
[Anträge]

☐ Es soll Klageerwiderung eingereicht werden. Der Antragsteller beabsichtigt, Klageabweisung zu beantragen.

[Unterschrift Rechtsanwalt]

Anlagen:
- Erklärung über die persönlichen und wirtschaftlichen Verhältnisse (ausgefüllt)
- Belege über Einkommen und Vermögen
- [Entwurf der Klageschrift / Klageerwiderung]
- Vollmacht`
  },
  {
    id: 'zeugenfragebogen',
    name: 'Beweisantritt mit Zeugen',
    category: 'Klagen & Schriftsätze',
    description: 'Schriftsatz mit Zeugenbenennung',
    icon: '👥',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

In Sachen

[Kläger] ./. [Beklagter]

reiche ich folgenden

Schriftsatz

nebst Beweisantritt ein:

I. Sachvortrag

Zu dem Vortrag der Gegenseite im Schriftsatz vom 28.01.2026 nehme ich wie folgt Stellung:

[Detaillierter Sachvortrag]

II. Beweisantritt

Zum Beweis der Behauptung, dass [zu beweisende Tatsache],

benenne ich als Zeugen:

1. [Vorname Nachname]
   [Vollständige Adresse]
   12345 Berlin
   
   Der Zeuge wird bekunden, dass [erwartete Aussage].

2. [Vorname Nachname]
   [Vollständige Adresse]
   12345 Berlin
   
   Der Zeuge wird bekunden, dass [erwartete Aussage].

Alternativ/Ergänzend biete ich an:

☐ Sachverständigengutachten
☐ Parteivernehmung des [Klägers/Beklagten]
☐ Inaugenscheinnahme

III. Antrag

Ich beantrage, Termin zur mündlichen Verhandlung zu bestimmen und die benannten Zeugen zu laden.

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'streitverkuendung',
    name: 'Streitverkündung',
    category: 'Klagen & Schriftsätze',
    description: 'Streitverkündungsschrift an Dritte',
    icon: '📨',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Streitverkündung

In dem Rechtsstreit

[Kläger], Hauptstraße 15, 50667 Köln
- Kläger -

gegen

[Mandant], Hauptstraße 15, 50667 Köln
- Beklagter -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

wegen: [Streitgegenstand]

verkünde ich namens und in Vollmacht des Beklagten dem

[Name des Streitverkündeten]
Hauptstraße 15, 50667 Köln
12345 Berlin

den Streit.

I. Gegenstand des Rechtsstreits

Der Kläger macht gegen den Beklagten [Anspruch] geltend.
[Kurze Sachverhaltsdarstellung]

II. Grund der Streitverkündung

Der Beklagte verkündet dem Streitverkündeten den Streit, weil:

[Begründung, z.B.:]
☐ Der Streitverkündete hat dem Beklagten die Freiheit von Mängeln zugesichert.
☐ Der Streitverkündete ist dem Beklagten zum Regress verpflichtet.
☐ Der Streitverkündete hat [Handlung], die zum Rechtsstreit geführt hat.

Sollte der Beklagte in diesem Rechtsstreit unterliegen, wird er den Streitverkündeten in Regress nehmen.

III. Aufforderung zum Beitritt

Der Streitverkündete wird aufgefordert, dem Rechtsstreit auf Seiten des Beklagten beizutreten.

Er hat die Möglichkeit, dem Rechtsstreit beizutreten (§ 74 ZPO). Die Wirkungen der Streitverkündung treten unabhängig von einem Beitritt ein (§ 68 ZPO).

[Unterschrift Rechtsanwalt]

---

[Zusätzlich: Zustellung an Streitverkündeten per Einschreiben]`
  },
  {
    id: 'befangenheitsantrag',
    name: 'Befangenheitsantrag',
    category: 'Klagen & Schriftsätze',
    description: 'Ablehnung eines Richters wegen Befangenheit',
    icon: '⚖️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Befangenheitsantrag

In dem Rechtsstreit

[Kläger] ./. [Beklagter]

lehne ich namens und in Vollmacht des [Klägers/Beklagten] den zuständigen Richter/die zuständige Richterin

[Name des Richters]

wegen Besorgnis der Befangenheit ab.

Begründung:

I. Sachverhalt

[Darstellung der Umstände, die die Besorgnis der Befangenheit begründen]

In der mündlichen Verhandlung vom 28.01.2026 / Im Beschluss vom 28.01.2026 hat der abgelehnte Richter:

1. [Konkrete Handlung/Äußerung 1]
2. [Konkrete Handlung/Äußerung 2]

Glaubhaftmachung: ☐ Terminsprotokoll ☐ Eidesstattliche Versicherung (Anlage)

II. Rechtliche Würdigung

Gemäß § 42 Abs. 2 ZPO kann ein Richter wegen Besorgnis der Befangenheit abgelehnt werden, wenn ein Grund vorliegt, der geeignet ist, Misstrauen gegen seine Unparteilichkeit zu rechtfertigen.

Die geschilderten Umstände begründen die Besorgnis, dass der abgelehnte Richter der Sache nicht unvoreingenommen gegenübersteht, weil:

[Subsumtion]

Es kommt nicht darauf an, ob der Richter tatsächlich befangen ist. Ausreichend ist, dass aus der Sicht einer vernünftigen Partei Anlass besteht, an der Unvoreingenommenheit zu zweifeln.

III. Antrag

Ich beantrage, den Richter [Name] wegen Besorgnis der Befangenheit abzulehnen und einen anderen Richter zur Entscheidung zu bestimmen.

Ferner beantrage ich, keine Entscheidung in der Hauptsache zu treffen, bis über das Ablehnungsgesuch entschieden ist (§ 47 ZPO).

[Unterschrift Rechtsanwalt]

Anlage: [Eidesstattliche Versicherung / Terminsprotokoll]`
  },
  {
    id: 'vollstreckungsabwehr',
    name: 'Vollstreckungsabwehrklage',
    category: 'Klagen & Schriftsätze',
    description: 'Klage gegen Zwangsvollstreckung',
    icon: '🛡️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Vollstreckungsabwehrklage
gemäß § 767 ZPO

In Sachen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Gläubigers], Hauptstraße 15, 50667 Köln
- Beklagter -

wegen: Unzulässigkeit der Zwangsvollstreckung
Streitwert: [Betrag]€

erhebe ich namens und in Vollmacht des Klägers Klage und beantrage:

1. Die Zwangsvollstreckung aus dem Urteil des Amtsgerichts Berlin vom 28.01.2026, Az. [Az.], wird für unzulässig erklärt.

2. Der Beklagte trägt die Kosten des Rechtsstreits.

3. Das Urteil ist vorläufig vollstreckbar.

4. Hilfsweise: Es wird die einstweilige Einstellung der Zwangsvollstreckung angeordnet (§ 769 ZPO).

Begründung:

I. Sachverhalt

1. Der Beklagte betreibt gegen den Kläger die Zwangsvollstreckung aus dem Urteil des Amtsgerichts Berlin vom 28.01.2026, Az. [Az.], wegen einer Forderung in Höhe von [Betrag]€.

2. Die titulierte Forderung ist erloschen, weil:

☐ Der Kläger hat die Forderung am 28.01.2026 vollständig beglichen.
Beweis: Überweisungsbeleg (Anlage K1)

☐ Die Forderung ist verjährt. Die Verjährung trat am 28.01.2026 ein.

☐ Der Kläger hat wirksam aufgerechnet mit einer Gegenforderung aus [Rechtsgrund].
Beweis: Aufrechnungserklärung (Anlage K2)

☐ Die Parteien haben am 28.01.2026 einen Vergleich geschlossen.
Beweis: Vergleichsvereinbarung (Anlage K3)

II. Rechtliche Würdigung

Gemäß § 767 ZPO kann der Schuldner Einwendungen gegen den Anspruch selbst im Wege der Klage geltend machen.

Die Einwendung des Klägers ist nach Entstehung des Titels entstanden und daher berücksichtigungsfähig.

[Unterschrift Rechtsanwalt]

Anlagen:
- Vollstreckbarer Titel (Kopie)
- K1/K2/K3: Nachweise
- Vollmacht`
  },
  {
    id: 'kostenausgleichung',
    name: 'Kostenfestsetzungsantrag',
    category: 'Klagen & Schriftsätze',
    description: 'Antrag auf Festsetzung erstattungsfähiger Kosten',
    icon: '💶',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
- Rechtspfleger/in -
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Kostenfestsetzungsantrag

In dem Rechtsstreit

[Obsiegende Partei], Hauptstraße 15, 50667 Köln
- Kläger/Beklagter -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Unterlegene Partei], Hauptstraße 15, 50667 Köln
- Beklagter/Kläger -

wegen: [Streitgegenstand]

beantrage ich die Festsetzung der dem [Kläger/Beklagten] zu erstattenden Kosten wie folgt:

I. Gerichtskosten

Gezahlter Vorschuss: [Betrag]€
(festgesetzt lt. Kostenrechnung vom 28.01.2026)

II. Rechtsanwaltskosten

Streitwert: [Betrag]€

1. Verfahrensgebühr Nr. 3100 VV RVG (1,3): [Betrag]€
2. Terminsgebühr Nr. 3104 VV RVG (1,2): [Betrag]€
3. Einigungsgebühr Nr. 1000 VV RVG (1,0): [Betrag]€ [falls Vergleich]
4. Auslagenpauschale Nr. 7002 VV RVG: [Betrag]€
5. Fahrtkosten Nr. 7003 VV RVG: [Betrag]€
6. Abwesenheitsgeld Nr. 7005 VV RVG: [Betrag]€
7. Kopierkosten Nr. 7000 VV RVG: [Betrag]€

Zwischensumme netto: [Betrag]€
19% Umsatzsteuer Nr. 7008 VV RVG: [Betrag]€
Summe Rechtsanwaltskosten: [Betrag]€

III. Sonstige Kosten

[z.B. Zeugenauslagen, Sachverständigenkosten]

IV. Gesamtsumme

Gerichtskosten: [Betrag]€
Rechtsanwaltskosten: [Betrag]€
Sonstige Kosten: [Betrag]€
**Gesamt zu erstatten: [Betrag]€**

Die Kostenentscheidung ergibt sich aus dem Urteil vom 28.01.2026.

Ich beantrage, die zu erstattenden Kosten auf [Betrag]€ nebst Zinsen in Höhe von 5 Prozentpunkten über dem Basiszinssatz seit Antragstellung festzusetzen.

[Unterschrift Rechtsanwalt]

Anlagen:
- Kostenrechnung
- Quittungen/Belege`
  },
  {
    id: 'widerklage',
    name: 'Widerklage',
    category: 'Klagen & Schriftsätze',
    description: 'Gegenklage im laufenden Verfahren',
    icon: '🔄',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Widerklage

In dem Rechtsstreit

[Name des Klägers], Hauptstraße 15, 50667 Köln
- Kläger und Widerbeklagter -

gegen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Beklagter und Widerkläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

wegen: [ursprünglicher Streitgegenstand]

erhebe ich namens und in Vollmacht des Beklagten Widerklage und beantrage:

1. Der Kläger und Widerbeklagte wird verurteilt, an den Beklagten und Widerkläger [Betrag]€ nebst Zinsen in Höhe von 5 Prozentpunkten über dem Basiszinssatz seit 28.01.2026 zu zahlen.

2. Der Kläger und Widerbeklagte trägt die Kosten des Rechtsstreits.

3. Das Urteil ist vorläufig vollstreckbar.

Begründung der Widerklage:

I. Zulässigkeit

Die Widerklage ist gemäß § 33 ZPO zulässig. Sie steht mit dem Klageanspruch in rechtlichem Zusammenhang, da beide Ansprüche aus demselben Mietverhältnis resultieren.

II. Sachverhalt

[Sachverhaltsdarstellung zur Widerklage]

III. Anspruchsgrundlage

Der Widerklageanspruch ergibt sich aus [Rechtsgrundlage, z.B.]:
☐ § 536a BGB (Schadensersatz wegen Mängeln)
☐ § 812 BGB (Rückzahlung überzahlter Miete)
☐ § 280 BGB (Schadensersatz)

[Ausführungen]

Streitwert der Widerklage: [Betrag]€

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'klaegerweiterung',
    name: 'Klageerweiterung',
    category: 'Klagen & Schriftsätze',
    description: 'Erweiterung der Klageanträge',
    icon: '➕',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Klageerweiterung

In dem Rechtsstreit

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Beklagten], Hauptstraße 15, 50667 Köln
- Beklagter -

wegen: [Streitgegenstand]

erweitere ich namens und in Vollmacht des Klägers die Klage wie folgt:

I. Erweiterter Klageantrag

Neben den bisherigen Anträgen beantrage ich nunmehr zusätzlich:

[Nummer]. Der Beklagte wird verurteilt, [neuer Antrag].

II. Begründung der Klageerweiterung

1. Seit Klageerhebung sind folgende neue Tatsachen eingetreten:
[Darstellung]

2. Die Klageerweiterung ist sachdienlich im Sinne des § 264 Nr. 2 ZPO, da:
- Sie auf demselben Lebenssachverhalt beruht
- Keine wesentliche Verzögerung des Rechtsstreits zu erwarten ist
- Eine einheitliche Entscheidung prozessökonomisch ist

3. Der erweiterte Anspruch ergibt sich aus:
[Rechtsgrundlage und Subsumtion]

III. Streitwert

Der Streitwert erhöht sich durch die Klageerweiterung von [alter Betrag]€ auf [neuer Betrag]€.

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'klageruecknahme',
    name: 'Klagerücknahme',
    category: 'Klagen & Schriftsätze',
    description: 'Rücknahme der Klage',
    icon: '↩️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

In dem Rechtsstreit

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Kläger -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

gegen

[Name des Beklagten], Hauptstraße 15, 50667 Köln
- Beklagter -

wegen: [Streitgegenstand]

nehme ich namens und in Vollmacht des Klägers die Klage zurück.

☐ Die Klagerücknahme erfolgt vor Beginn der mündlichen Verhandlung (§ 269 Abs. 1 ZPO). Eine Zustimmung des Beklagten ist nicht erforderlich.

☐ Die Klagerücknahme erfolgt nach Beginn der mündlichen Verhandlung (§ 269 Abs. 1 ZPO). Die Einwilligung des Beklagten liegt vor / wird beantragt.

Begründung:
[Optional: z.B. "Die Parteien haben sich außergerichtlich geeinigt."]

Kostenantrag:

☐ Der Kläger übernimmt die Kosten des Rechtsstreits (§ 269 Abs. 3 ZPO).
☐ Die Kosten des Rechtsstreits trägt der Beklagte, da dieser den Anlass zur Klage gegeben und den Anspruch sofort anerkannt / erfüllt hat (§ 269 Abs. 3 S. 2, 2. Alt. ZPO).

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'versaeumnisurteil_einspruch',
    name: 'Einspruch gegen Versäumnisurteil',
    category: 'Klagen & Schriftsätze',
    description: 'Einspruch nach Versäumnisurteil',
    icon: '⏰',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Einspruch gegen Versäumnisurteil

In dem Rechtsstreit

[Name des Klägers], Hauptstraße 15, 50667 Köln
- Kläger -

gegen

[Name des Mandanten], Hauptstraße 15, 50667 Köln
- Beklagter -

Prozessbevollmächtigte: Rechtsanwaltskanzlei Dr. Schneider & Partner

wegen: [Streitgegenstand]

lege ich namens und in Vollmacht des Beklagten gegen das am [Zustellungsdatum] zugestellte Versäumnisurteil vom [Datum des Versäumnisurteils]

Einspruch

ein.

Die Einspruchsfrist ist gewahrt. Das Versäumnisurteil wurde am 28.01.2026 zugestellt. Die zweiwöchige Einspruchsfrist (§ 339 ZPO) läuft am 28.01.2026 ab.

Ich beantrage:

1. Das Versäumnisurteil vom 28.01.2026 wird aufgehoben.

2. Die Klage wird abgewiesen.

3. Der Kläger trägt die Kosten des Rechtsstreits.

Begründung:

I. Grund für das Versäumnis

Der Beklagte war am Termin vom 28.01.2026 nicht erschienen, weil:
[Begründung, z.B. Krankheit, nicht rechtzeitige Ladung, Terminsüberschneidung]

II. Zur Sache

Das Versäumnisurteil ist aufzuheben, weil die Klage unbegründet ist.

[Sachvortrag und rechtliche Würdigung]

Beweis: [Beweismittel]

[Unterschrift Rechtsanwalt]

Anlage: Vollmacht`
  },
  {
    id: 'wiedereinsetzung',
    name: 'Wiedereinsetzung in den vorigen Stand',
    category: 'Klagen & Schriftsätze',
    description: 'Antrag bei versäumter Frist',
    icon: '🔓',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht/Landgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Antrag auf Wiedereinsetzung in den vorigen Stand

In dem Rechtsstreit

[Partei 1] ./. [Partei 2]

beantrage ich namens und in Vollmacht des [Klägers/Beklagten]:

1. Dem [Kläger/Beklagten] wird Wiedereinsetzung in den vorigen Stand gegen die Versäumung der [Bezeichnung der Frist, z.B. Berufungsfrist/Berufungsbegründungsfrist/Klageerwiderungsfrist] gewährt.

2. Die versäumte Prozesshandlung wird hiermit nachgeholt.

Begründung:

I. Versäumung der Frist

Die [Bezeichnung der Frist] endete am 28.01.2026. Die Frist wurde versäumt.

II. Fehlendes Verschulden

Die Partei war ohne ihr Verschulden an der Einhaltung der Frist gehindert (§ 233 ZPO).

[Darstellung der Hinderungsgründe, z.B.:]
☐ Krankheit der Partei
☐ Organisationsverschulden des Gerichts (verspätete Zustellung)
☐ Höhere Gewalt
☐ Unverschuldete Rechtsunkenntnis
☐ Anwaltsversäumnis, das der Partei nicht zuzurechnen ist

Glaubhaftmachung: [Eidesstattliche Versicherung / Ärztliches Attest] (Anlage)

III. Fristgerechte Antragstellung

Der Antrag auf Wiedereinsetzung ist fristgerecht. Das Hindernis ist am 28.01.2026 weggefallen. Die zweiwöchige Antragsfrist (§ 234 ZPO) ist gewahrt.

IV. Nachholung der versäumten Handlung

Gleichzeitig mit diesem Antrag hole ich die versäumte Prozesshandlung nach:

[Versäumte Prozesshandlung, z.B. Berufungsschrift, Berufungsbegründung]

[Unterschrift Rechtsanwalt]

Anlagen:
- Glaubhaftmachung
- Nachgeholte Prozesshandlung
- Vollmacht`
  },
  {
    id: 'rechtsmittelverzicht',
    name: 'Rechtsmittelverzicht',
    category: 'Klagen & Schriftsätze',
    description: 'Erklärung des Rechtsmittelverzichts',
    icon: '✅',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Rechtsmittelverzicht

In dem Rechtsstreit

[Partei 1], Hauptstraße 15, 50667 Köln
- Kläger -

gegen

[Partei 2], Hauptstraße 15, 50667 Köln
- Beklagter -

wegen: [Streitgegenstand]

erkläre ich namens und in Vollmacht des [Klägers/Beklagten]:

Auf Rechtsmittel gegen das Urteil des Amtsgerichts Berlin vom 28.01.2026, verkündet am 28.01.2026, wird verzichtet.

Ich bitte um:

1. Aktenvermerk über den Rechtsmittelverzicht
2. Erteilung einer Rechtskraftbescheinigung
3. Erteilung einer vollstreckbaren Ausfertigung

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'fristverlängerung',
    name: 'Antrag auf Fristverlängerung',
    category: 'Klagen & Schriftsätze',
    description: 'Verlängerung prozessualer Fristen',
    icon: '📅',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Antrag auf Fristverlängerung

In dem Rechtsstreit

[Partei 1] ./. [Partei 2]

beantrage ich namens und in Vollmacht des [Klägers/Beklagten]:

Die Frist zur [Bezeichnung]:
☐ Klageerwiderung
☐ Stellungnahme zum Schriftsatz vom 28.01.2026
☐ Berufungsbegründung
☐ Vorlage von [Unterlagen]

wird um 2 Wochen verlängert, mithin bis zum [neues Datum].

Begründung:

[Begründung, z.B.:]
☐ Umfangreicher Sachverhalt erfordert intensive Prüfung
☐ Einholung von Informationen/Unterlagen vom Mandanten erforderlich
☐ Urlaubsabwesenheit des Unterzeichners
☐ Arbeitsüberlastung der Kanzlei
☐ Krankheit
☐ Abstimmung mit weiteren Beteiligten erforderlich

☐ Der Gegner wurde informiert und hat keine Einwände.
☐ Der Gegner hat der Fristverlängerung zugestimmt.
☐ Es handelt sich um die erste Fristverlängerung.

Die Fristverlängerung führt nicht zu einer Verzögerung des Rechtsstreits, da [Begründung].

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'schriftsatznachlass',
    name: 'Antrag auf Schriftsatznachlass',
    category: 'Klagen & Schriftsätze',
    description: 'Nachreichung eines Schriftsatzes beantragen',
    icon: '📝',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Schriftsatz

In dem Rechtsstreit

[Partei 1] ./. [Partei 2]

nehme ich namens und in Vollmacht des [Klägers/Beklagten] wie folgt Stellung:

I. Antrag auf Schriftsatznachlass

Zu dem in der mündlichen Verhandlung vom 28.01.2026 gehaltenen neuen Vortrag der Gegenseite beantrage ich Schriftsatznachlass gemäß § 283 ZPO.

Die Gegenseite hat erstmals vorgetragen:
[Neuer Vortrag]

Eine Stellungnahme hierzu war in der mündlichen Verhandlung nicht möglich, da:
☐ Der Vortrag überraschend neu war
☐ Eine Prüfung der Behauptungen erforderlich ist
☐ Rücksprache mit dem Mandanten erforderlich ist
☐ Einholung von Unterlagen/Informationen erforderlich ist

Ich bitte um Gewährung einer Frist von [2/3] Wochen zur schriftlichen Stellungnahme.

II. Hilfsweise: Terminsvertagung

Hilfsweise beantrage ich Vertagung des Termins, damit zu dem neuen Vortrag Stellung genommen werden kann.

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'aussetzung_verfahren',
    name: 'Antrag auf Aussetzung des Verfahrens',
    category: 'Klagen & Schriftsätze',
    description: 'Aussetzung wegen Vorgreiflichkeit',
    icon: '⏸️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Antrag auf Aussetzung des Verfahrens

In dem Rechtsstreit

[Partei 1] ./. [Partei 2]

beantrage ich namens und in Vollmacht des [Klägers/Beklagten]:

Das Verfahren wird gemäß § 148 ZPO ausgesetzt.

Begründung:

Die Entscheidung des Rechtsstreits hängt von dem Bestehen oder Nichtbestehen eines Rechtsverhältnisses ab, das Gegenstand eines anderen anhängigen Rechtsstreits ist.

Vorgreifliches Verfahren:
Gericht: [Bezeichnung des Gerichts]
Aktenzeichen: [Az.]
Parteien: [Parteien des anderen Verfahrens]
Gegenstand: [Streitgegenstand]

Vorgreiflichkeit:
[Darstellung, warum die Entscheidung des anderen Verfahrens für den hiesigen Rechtsstreit vorgreiflich ist]

Die Aussetzung ist sachgerecht, weil:
1. Divergierende Entscheidungen vermieden werden
2. Keine Beweisprobleme durch doppelte Verfahren entstehen
3. Prozessökonomie gewahrt wird

Ich rege an, das Verfahren bis zur rechtskräftigen Entscheidung im vorgreiflichen Verfahren auszusetzen.

[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'ruhe_verfahren',
    name: 'Antrag auf Ruhen des Verfahrens',
    category: 'Klagen & Schriftsätze',
    description: 'Gemeinsamer Antrag auf Ruhen',
    icon: '💤',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

Rechtsanwaltskanzlei Dr. Schneider & Partner
Bahnhofstraße 45, 60329 Frankfurt
Tel: 069/12345678, Fax: 069/12345679
mail@ra-schneider.de

An das
Amtsgericht Berlin
Hauptstraße 15, 50667 Köln
12345 Berlin

Az.: 12 C 345/24

Gemeinsamer Antrag auf Ruhen des Verfahrens

In dem Rechtsstreit

[Partei 1] ./. [Partei 2]

beantragen beide Parteien übereinstimmend das Ruhen des Verfahrens gemäß § 251 ZPO.

Begründung:

Die Parteien befinden sich in außergerichtlichen Vergleichsverhandlungen und sind zuversichtlich, eine einvernehmliche Lösung zu finden.

Das Ruhen des Verfahrens wird für die Dauer von [3/6] Monaten beantragt.

☐ Der Gegner hat der Ruhensanordnung zugestimmt (Anlage).
☐ Die Zustimmung des Gegners wird noch übermittelt.

Wir beantragen, das Verfahren bis zum 28.01.2026 ruhen zu lassen und dann von Amts wegen auf eine mögliche Wiederaufnahme hinzuweisen.

[Unterschrift Rechtsanwalt Kläger]

Einverstanden:

[Unterschrift Rechtsanwalt Beklagter]`
  },
  {
    id: 'unterlassungserklaerung',
    name: 'Unterlassungserklärung',
    category: 'Musterbriefe',
    description: 'Strafbewehrte Unterlassungserklärung',
    icon: '🛑',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

STRAFBEWEHRTE UNTERLASSUNGSERKLÄRUNG

Ich/Wir,

[Name des Unterlassungsschuldners]
Hauptstraße 15, 50667 Köln

gebe(n) gegenüber

[Name des Unterlassungsgläubigers]
Hauptstraße 15, 50667 Köln

folgende strafbewehrte Unterlassungserklärung ab:

1. UNTERLASSUNGSVERPFLICHTUNG

Ich/Wir verpflichte(n) mich/uns, es ab sofort zu unterlassen,

☐ [Konkrete Beschreibung der zu unterlassenden Handlung]

☐ die Mietsache vertragswidrig zu nutzen, insbesondere 3

☐ ruhestörenden Lärm zu verursachen, insbesondere 3

☐ unberechtigt Gemeinschaftsflächen zu nutzen

☐ [Sonstige Unterlassungspflicht]

2. VERTRAGSSTRAFE

Für jeden Fall der Zuwiderhandlung gegen die vorstehende Unterlassungsverpflichtung verpflichte(n) ich/wir mich/uns zur Zahlung einer Vertragsstrafe in Höhe von 1.200,00 € an den Unterlassungsgläubiger.

Die Vertragsstrafe ist der Höhe nach angemessen und wird vom Unterlassungsgläubiger nach billigem Ermessen festgesetzt, wobei im Streitfall die Festsetzung durch das zuständige Gericht überprüft werden kann.

3. KOSTENANERKENNTNIS

Ich/Wir erkenne(n) an, die durch die Abmahnung entstandenen Kosten in Höhe von 1.200,00 € zu tragen.

☐ Die Kosten werden bis zum 28.01.2026 bezahlt.
☐ Die Kosten sind bereits beglichen.

4. UNTERWERFUNG

Diese Unterlassungserklärung ist unwiderruflich und gilt unbefristet.

Berlin, den 29.12.2025

_______________________
[Unterschrift Unterlassungsschuldner]`
  },
  {
    id: 'vergleichsvereinbarung',
    name: 'Vergleichsvereinbarung',
    category: 'Vertragsrecht',
    description: 'Außergerichtliche Einigung',
    icon: '⚖️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

VERGLEICHSVEREINBARUNG

Zwischen

[Name Partei 1], Hauptstraße 15, 50667 Köln
- nachfolgend "Partei 1" genannt -

vertreten durch: [Rechtsanwalt, Kanzlei]

und

[Name Partei 2], Hauptstraße 15, 50667 Köln
- nachfolgend "Partei 2" genannt -

vertreten durch: [Rechtsanwalt, Kanzlei]

wird zur Beilegung der Streitigkeiten aus/wegen

[Beschreibung des Streitgegenstands, z.B. Mietverhältnis, WEG-Angelegenheit]

folgender Vergleich geschlossen:

§ 1 Präambel
Die Parteien streiten über [kurze Beschreibung des Streitgegenstands].
Zur Vermeidung weiterer Auseinandersetzungen und der damit verbundenen Kosten und Risiken einigen sich die Parteien wie folgt:

§ 2 Zahlungsverpflichtung
Partei [1/2] zahlt an Partei [1/2] einen Betrag von 1.200,00 €.

Die Zahlung erfolgt:
☐ in einer Summe bis zum 28.01.2026
☐ in 3 Raten à 1.200,00 €, fällig jeweils zum 3 eines Monats, beginnend am 28.01.2026

Zahlungsverzug mit einer Rate führt zur sofortigen Fälligkeit des gesamten Restbetrages.

§ 3 Weitere Verpflichtungen
[Individuelle Vereinbarungen, z.B.:]
☐ Räumung der Mietsache bis zum 28.01.2026
☐ Durchführung von Reparaturen
☐ Unterlassung bestimmter Handlungen
☐ Rückgabe von Gegenständen

§ 4 Erledigungserklärung
Mit vollständiger Erfüllung dieser Vereinbarung sind sämtliche wechselseitigen Ansprüche der Parteien aus dem streitgegenständlichen Sachverhalt abgegolten und erledigt.

Ausgenommen hiervon sind:
☐ keine Ausnahmen
☐ [konkrete Ausnahmen]

§ 5 Anhängige Verfahren
☐ Das beim Amtsgericht Berlin-Mitte unter Az. 3 anhängige Verfahren wird für erledigt erklärt. Die Kosten werden [gegeneinander aufgehoben / getragen von ___].
☐ Es ist kein Verfahren anhängig.

§ 6 Vertraulichkeit
Die Parteien verpflichten sich, über den Inhalt dieser Vereinbarung Stillschweigen zu bewahren.

§ 7 Schlussbestimmungen
Änderungen und Ergänzungen bedürfen der Schriftform.
Sollte eine Bestimmung unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.
Jede Partei erhält eine Ausfertigung dieses Vergleichs.

Berlin, den 29.12.2025

_______________________          _______________________
Partei 1 / RA                    Partei 2 / RA`
  },
  {
    id: 'prozessvollmacht',
    name: 'Prozessvollmacht',
    category: 'Sonstiges',
    description: 'Vollmacht zur Prozessführung',
    icon: '📜',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

PROZESSVOLLMACHT

Hiermit bevollmächtige ich / bevollmächtigen wir

Vollmachtgeber:
[Name / Firma]
Hauptstraße 15, 50667 Köln
[Geburtsdatum / Handelsregister]

den / die Rechtsanwalt / Rechtsanwältin / die Rechtsanwälte der Kanzlei

Rechtsanwaltskanzlei Weber & Kollegen
Hauptstraße 15, 50667 Köln

in der Rechtssache

gegen / betreffend: [Gegner / Sache]
wegen: [Streitgegenstand]

zu meiner / unserer Vertretung.

Die Vollmacht umfasst:

1. PROZESSVERTRETUNG
☑ Vertretung vor allen Gerichten aller Instanzen und Gerichtsbarkeiten
☑ Erhebung und Abwehr von Klagen, Anträgen und Rechtsmitteln
☑ Einlegung und Rücknahme von Rechtsmitteln
☑ Vertretung in Nebenverfahren (Arrest, einstweilige Verfügung, Kostenfestsetzung)

2. VERGLEICHSBEFUGNIS
☑ Abschluss von Vergleichen
☑ Verzicht auf Ansprüche
☑ Anerkenntnis von Ansprüchen

3. VOLLSTRECKUNG
☑ Betreiben und Abwehr der Zwangsvollstreckung
☑ Entgegennahme von Geldern und Wertgegenständen
☑ Erteilung von Quittungen

4. ZUSTELLUNGEN
☑ Entgegennahme von Zustellungen
☑ Empfangnahme von Willenserklärungen

5. UNTERVOLLMACHT
☑ Erteilung von Untervollmacht an Rechtsanwälte und Rechtsreferendare

6. BESONDERE BEFUGNISSE
☐ Akteneinsicht
☐ Vertretung vor Behörden
☐ Außergerichtliche Verhandlungen
☐ [weitere Befugnisse]

Diese Vollmacht gilt:
☐ unbefristet bis zum Widerruf
☐ befristet bis zum 28.01.2026
☐ für das oben genannte Verfahren

Die Vollmacht erstreckt sich auch auf die Geltendmachung datenschutzrechtlicher Auskunfts- und Löschungsansprüche.

Berlin, den 29.12.2025

_______________________
[Unterschrift Vollmachtgeber]

Vollmacht angenommen:

_______________________
[Unterschrift Rechtsanwalt]`
  },
  {
    id: 'pachtvertrag',
    name: 'Pachtvertrag Grundstück',
    category: 'Vertragsrecht',
    description: 'Pachtvertrag für landwirtschaftliche/gewerbliche Nutzung',
    icon: '🌾',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

PACHTVERTRAG

Zwischen

[Name Verpächter], Hauptstraße 15, 50667 Köln
- nachfolgend "Verpächter" genannt -

und

[Name Pächter], Hauptstraße 15, 50667 Köln
- nachfolgend "Pächter" genannt -

wird folgender Pachtvertrag geschlossen:

§ 1 Pachtgegenstand
Verpachtet wird das Grundstück:
Gemarkung: 3
Flur: 3, Flurstück: 3
Größe: ca. 3 m² / ha
Nutzungsart: [landwirtschaftlich / gewerblich / Garten]

§ 2 Pachtdauer
Der Pachtvertrag beginnt am 28.01.2026 und läuft:
☐ auf unbestimmte Zeit mit Kündigungsfrist von 3 Monaten zum 28.01.2026
☐ befristet bis zum 28.01.2026

§ 3 Pachtzins
Der jährliche Pachtzins beträgt 1.200,00 € und ist [jährlich/halbjährlich/vierteljährlich] im Voraus zum 28.01.2026 zu zahlen.

☐ Der Pachtzins wird jährlich an die Entwicklung des Verbraucherpreisindex angepasst.

§ 4 Nutzung
Das Grundstück darf ausschließlich für folgende Zwecke genutzt werden:
3

Bauliche Veränderungen bedürfen der vorherigen schriftlichen Zustimmung.

§ 5 Instandhaltung
Der Pächter verpflichtet sich zur ordnungsgemäßen Bewirtschaftung und Pflege.
☐ Kleinreparaturen trägt der Pächter.
☐ Größere Reparaturen trägt der Verpächter.

§ 6 Versicherung
☐ Der Pächter versichert die auf dem Grundstück befindlichen Einrichtungen.
☐ Der Verpächter unterhält eine Grundstücksversicherung.

§ 7 Rückgabe
Bei Beendigung ist das Grundstück im ordnungsgemäßen Zustand zurückzugeben.

Berlin, den 29.12.2025

_______________________          _______________________
Verpächter                       Pächter`
  },
  {
    id: 'bautraegervertrag',
    name: 'Bauträgervertrag',
    category: 'Kaufverträge',
    description: 'Vertrag zum Erwerb einer Neubauimmobilie vom Bauträger',
    icon: '🏗️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

BAUTRÄGERVERTRAG
(gemäß MaBV - Makler- und Bauträgerverordnung)

Zwischen

[Bauträger GmbH]
Geschäftsführer: 3
Hauptstraße 15, 50667 Köln
- nachfolgend "Bauträger" genannt -

und

[Name Erwerber], Hauptstraße 15, 50667 Köln
- nachfolgend "Erwerber" genannt -

wird folgender Bauträgervertrag geschlossen:

§ 1 Vertragsgegenstand
Der Bauträger verpflichtet sich, dem Erwerber nach Maßgabe dieses Vertrages das Grundstück zu übertragen und darauf ein Gebäude zu errichten.

1.1 Grundstück:
Gemarkung: 3, Flur: 3, Flurstück: 3
Grundstücksgröße: 3 m²
Grundbuch: Blatt 3

1.2 Gebäude:
Wohnung Nr. 3 im 3 OG
Wohnfläche: ca. 3 m²
Ausstattung: gemäß Baubeschreibung (Anlage 1)
Bauplanungsrechtliche Grundlagen: Baugenehmigung vom 28.01.2026

1.3 Zubehör:
☐ Tiefgaragenstellplatz Nr. 3
☐ Kellerraum Nr. 3

§ 2 Kaufpreis
Der Gesamtkaufpreis beträgt: 1.200,00 € und setzt sich wie folgt zusammen:

- Grundstücksanteil: 1.200,00 €
- Gebäudeanteil: 1.200,00 €
- Stellplatz: 1.200,00 €
- Gesamt: 1.200,00 €

§ 3 Zahlungsplan (gemäß § 3 MaBV)
Die Zahlungen erfolgen nach Baufortschritt:

1. Nach Beginn der Erdarbeiten: max. 30% = 1.200,00 €
2. Nach Rohbaufertigstellung inkl. Zimmererarbeiten: max. 28% = 1.200,00 €
3. Nach Dacheindeckung: max. 8% = 1.200,00 €
4. Nach Fenstermontage: max. 10% = 1.200,00 €
5. Nach Innenputz: max. 5% = 1.200,00 €
6. Nach Estrich: max. 5% = 1.200,00 €
7. Nach Fliesenarbeiten: max. 4% = 1.200,00 €
8. Nach vollständiger Fertigstellung: max. 7% = 1.200,00 €
9. Nach Besitzübergabe: max. 3% = 1.200,00 €

§ 4 Sicherheiten
Der Bauträger stellt eine Bankbürgschaft oder Gewährleistungsbürgschaft über 1.200,00 € zur Verfügung.

§ 5 Fertigstellung
Die Fertigstellung ist bis spätestens 28.01.2026 vorgesehen.
Bei Verzögerung: [Vertragsstrafe / Schadensersatz]

§ 6 Gewährleistung
Die Gewährleistungsfrist beträgt 5 Jahre ab Abnahme gemäß § 634a BGB.

§ 7 Auflassungsvormerkung
Zur Sicherung des Übereignungsanspruchs wird eine Auflassungsvormerkung im Grundbuch eingetragen.

§ 8 Notarkosten und Grunderwerbsteuer
Die Notarkosten, Grundbuchkosten und Grunderwerbsteuer trägt der Erwerber.

Berlin, den 29.12.2025

_______________________          _______________________
Bauträger                        Erwerber

Notarielle Beurkundung erforderlich gem. § 311b BGB!`
  },
  {
    id: 'schenkungsvertrag',
    name: 'Schenkungsvertrag Immobilie',
    category: 'Vertragsrecht',
    description: 'Übertragung von Immobilien durch Schenkung',
    icon: '🎁',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

SCHENKUNGSVERTRAG

Zwischen

[Name Schenker], Hauptstraße 15, 50667 Köln
- nachfolgend "Schenker" genannt -

und

[Name Beschenkter], Hauptstraße 15, 50667 Köln
- nachfolgend "Beschenkter" genannt -

wird folgender Schenkungsvertrag geschlossen:

§ 1 Schenkungsgegenstand
Der Schenker schenkt dem Beschenkten das folgende Grundstück:

Gemarkung: 3
Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Grundstücksgröße: 3 m²
Bebauung: [Beschreibung]

§ 2 Eigentumsübertragung
Der Schenker überträgt das Eigentum lastenfrei.

Bestehende Lasten und Beschränkungen:
☐ Keine
☐ [Aufzählung von Grunddienstbarkeiten, Wegerechten, etc.]

§ 3 Schenkung
Die Übereignung erfolgt unentgeltlich im Wege der Schenkung gemäß § 516 BGB.

§ 4 Rückforderungsvorbehalt
☐ Die Schenkung erfolgt ohne Rückforderungsvorbehalt.
☐ Die Schenkung erfolgt unter dem Vorbehalt des Widerrufs bei grobem Undank (§ 530 BGB).
☐ Die Schenkung erfolgt unter dem Vorbehalt der Rückforderung bei Verarmung des Schenkers (§ 528 BGB).

§ 5 Nießbrauch
☐ Der Schenker behält sich den lebenslangen Nießbrauch vor (Eintragung im Grundbuch).
☐ Der Schenker behält sich ein lebenslanges Wohnrecht vor.
☐ Kein Nießbrauch / Wohnrecht.

§ 6 Auflage
☐ Der Beschenkte verpflichtet sich, [Auflage, z.B. Pflege des Schenkers].
☐ Keine Auflagen.

§ 7 Besitzübergang
Der Besitz geht über am: 28.01.2026

§ 8 Kosten
Die Kosten der notariellen Beurkundung, Grundbucheintragung und Grunderwerbsteuer trägt:
☐ der Beschenkte
☐ der Schenker
☐ jeder zur Hälfte

§ 9 Abänderungsvorbehalt
☐ Der Schenker behält sich das Recht vor, diesen Vertrag durch letztwillige Verfügung abzuändern.

Berlin, den 29.12.2025

_______________________          _______________________
Schenker                         Beschenkter

Notarielle Beurkundung erforderlich gem. § 518 Abs. 1 BGB!`
  },
  {
    id: 'teilungserklaerung',
    name: 'Teilungserklärung WEG',
    category: 'Vertragsrecht',
    description: 'Begründung von Wohnungseigentum',
    icon: '🏢',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

TEILUNGSERKLÄRUNG
gemäß § 8 WEG (Wohnungseigentumsgesetz)

Der Eigentümer

Thomas Wagner
Hauptstraße 15, 50667 Köln

Eigentümer des Grundstücks

Gemarkung: 3, Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Grundstücksgröße: 3 m²

erklärt hiermit die Teilung des Eigentums gemäß §§ 3, 8 WEG wie folgt:

§ 1 Aufteilung des Grundstücks
Das auf dem Grundstück befindliche Gebäude wird in Wohnungseigentum und Teileigentum aufgeteilt.

§ 2 Sondereigentum
Das Sondereigentum wird wie folgt begründet:

Wohnung Nr. 1 (WE 1):
- Lage: Erdgeschoss
- Wohnfläche: ca. 3 m²
- Räume: 2 Zimmer, Küche, Bad, [weitere]
- Miteigentumsanteil: 3/[Summe]

Wohnung Nr. 2 (WE 2):
- Lage: 1. Obergeschoss
- Wohnfläche: ca. 3 m²
- Räume: 2 Zimmer, Küche, Bad, [weitere]
- Miteigentumsanteil: 3/[Summe]

[weitere Einheiten...]

§ 3 Gemeinschaftliches Eigentum
Gemeinschaftliches Eigentum sind insbesondere:
- Grundstück
- Fundamente und tragende Wände
- Dach und Fassade
- Treppenhaus und Flure
- Heizungsanlage
- Außenanlagen

§ 4 Sondernutzungsrechte
☐ WE 1: Gartenanteil von ca. 3 m² (gemäß Plan)
☐ WE 2: Stellplatz Nr. 3
☐ [weitere Sondernutzungsrechte]

§ 5 Kostenverteilung
Die Kosten des gemeinschaftlichen Eigentums werden nach Miteigentumsanteilen verteilt.

Ausnahmen:
☐ Heizkosten nach Verbrauch
☐ [weitere Ausnahmen]

§ 6 Gemeinschaftsordnung
Für die Verwaltung und Nutzung gelten die Bestimmungen der beigefügten Gemeinschaftsordnung.

Berlin, den 29.12.2025

_______________________
[Eigentümer / Bauträger]

Notarielle Beurkundung und Eintragung im Grundbuch erforderlich!`
  },
  {
    id: 'erbbaurechtsvertrag',
    name: 'Erbbaurechtsvertrag',
    category: 'Grundbuchrecht',
    description: 'Bestellung eines Erbbaurechts',
    icon: '📋',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

ERBBAURECHTSVERTRAG
gemäß ErbbauRG (Erbbaurechtsgesetz)

Zwischen

[Name Grundstückseigentümer], Hauptstraße 15, 50667 Köln
- nachfolgend "Grundstückseigentümer" genannt -

und

[Name Erbbauberechtigter], Hauptstraße 15, 50667 Köln
- nachfolgend "Erbbauberechtigter" genannt -

wird folgender Erbbaurechtsvertrag geschlossen:

§ 1 Bestellung des Erbbaurechts
Der Grundstückseigentümer bestellt zugunsten des Erbbauberechtigten ein Erbbaurecht an dem Grundstück:

Gemarkung: 3, Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Grundstücksgröße: 3 m²

§ 2 Inhalt und Zweck
Das Erbbaurecht wird bestellt zum Zwecke der Errichtung und Unterhaltung von:
☐ Wohngebäude(n) mit 3 Wohneinheiten
☐ Gewerbegebäude
☐ [sonstige Nutzung]

Bebauungsplan: 3
Geschossflächenzahl: 3
Grundflächenzahl: 3

§ 3 Dauer des Erbbaurechts
Das Erbbaurecht wird bestellt für die Dauer von 3 Jahren, beginnend am 28.01.2026.

☐ Verlängerungsoption: [Bedingungen]
☐ Keine Verlängerung vorgesehen.

§ 4 Erbbauzins
Der jährliche Erbbauzins beträgt: 1.200,00 €

Zahlung:
☐ jährlich im Voraus zum 28.01.2026
☐ halbjährlich zum 28.01.2026

Wertsicherung:
☐ Anpassung nach Verbraucherpreisindex alle 3 Jahre
☐ Staffelung: [Staffeln angeben]
☐ Keine Wertsicherung

§ 5 Heimfall
Bei Beendigung des Erbbaurechts fallen die Bauwerke an den Grundstückseigentümer (Heimfall).

Entschädigung:
☐ 3% des Verkehrswerts der Bauwerke
☐ Nach Gutachten
☐ Keine Entschädigung

§ 6 Veräußerung und Belastung
Die Veräußerung oder Belastung des Erbbaurechts bedarf der Zustimmung des Grundstückseigentümers.

☐ Vorkaufsrecht des Grundstückseigentümers
☐ Kein Vorkaufsrecht

§ 7 Instandhaltung
Der Erbbauberechtigte ist verpflichtet, die Bauwerke in ordnungsgemäßem Zustand zu erhalten.

§ 8 Rangvorbehalt
☐ Für die Finanzierung darf das Erbbaurecht bis zu 1.200,00 € belastet werden.

§ 9 Kündigung
Eine außerordentliche Kündigung ist möglich bei:
- Zahlungsverzug von mehr als [2] Jahresbeträgen
- Vertragswidriger Nutzung
- Verfall der Bauwerke

Berlin, den 29.12.2025

_______________________          _______________________
Grundstückseigentümer            Erbbauberechtigter

Notarielle Beurkundung und Eintragung im Grundbuch (Abt. II) erforderlich!`
  },
  {
    id: 'dienstbarkeitsvertrag',
    name: 'Grunddienstbarkeit (Wegerecht)',
    category: 'Grundbuchrecht',
    description: 'Bestellung einer Grunddienstbarkeit',
    icon: '🛤️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

VERTRAG ÜBER DIE BESTELLUNG EINER GRUNDDIENSTBARKEIT

Zwischen

[Name Eigentümer des belasteten Grundstücks]
Hauptstraße 15, 50667 Köln
- nachfolgend "Verpflichteter" genannt -

und

[Name Eigentümer des begünstigten Grundstücks]
Hauptstraße 15, 50667 Köln
- nachfolgend "Berechtigter" genannt -

wird folgender Vertrag über die Bestellung einer Grunddienstbarkeit geschlossen:

§ 1 Belastetes Grundstück (dienendes Grundstück)
Gemarkung: 3, Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Eigentümer: [Verpflichteter]

§ 2 Begünstigtes Grundstück (herrschendes Grundstück)
Gemarkung: 3, Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Eigentümer: [Berechtigter]

§ 3 Inhalt der Grunddienstbarkeit

☐ WEGERECHT:
Der Berechtigte darf das belastete Grundstück mit Fahrzeugen aller Art befahren und zu Fuß begehen.
Lage: gemäß eingetragenem Lageplan (rot markiert)
Breite: 3 m
Länge: 3 m

☐ LEITUNGSRECHT:
Der Berechtigte darf über das belastete Grundstück Ver- und Entsorgungsleitungen verlegen, unterhalten und erneuern.
Art der Leitungen: [Wasser / Abwasser / Strom / Gas / Telekommunikation]

☐ GARAGENRECHT:
Der Berechtigte darf eine Garage auf dem belasteten Grundstück errichten und nutzen.

§ 4 Umfang der Nutzung
Die Dienstbarkeit berechtigt:
☐ zur privaten Nutzung
☐ zur gewerblichen Nutzung
☐ Beschränkung auf [max. Anzahl] Fahrzeuge

§ 5 Instandhaltung und Kosten
☐ Der Berechtigte trägt die Kosten der Instandhaltung und Unterhaltung.
☐ Die Kosten werden geteilt: 3% Verpflichteter / 3% Berechtigter.

Bei Leitungsrechten: Kosten für Verlegung, Wartung und Reparatur trägt der Berechtigte.

§ 6 Verkehrssicherungspflicht
Die Verkehrssicherungspflicht obliegt: [Verpflichteter / Berechtigter / beide]

§ 7 Ablösung
☐ Die Grunddienstbarkeit kann nicht abgelöst werden.
☐ Die Grunddienstbarkeit kann gegen Zahlung von 3€ abgelöst werden.

§ 8 Grundbucheintragung
Die Grunddienstbarkeit wird in Abteilung II des Grundbuchs des belasteten Grundstücks eingetragen.

§ 9 Kosten
Die Kosten der Beurkundung und Eintragung tragen:
☐ der Berechtigte
☐ der Verpflichtete
☐ beide je zur Hälfte

Berlin, den 29.12.2025

_______________________          _______________________
Verpflichteter                   Berechtigter

Notarielle Beurkundung erforderlich!`
  },
  {
    id: 'mietbürgschaft',
    name: 'Mietbürgschaft',
    category: 'Musterbriefe',
    description: 'Bürgschaftserklärung für Mietverhältnis',
    icon: '🤝',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

BÜRGSCHAFTSERKLÄRUNG
(Mietbürgschaft)

Ich/Wir,

[Name des Bürgen]
Hauptstraße 15, 50667 Köln
[Geburtsdatum]

- nachfolgend "Bürge" genannt -

übernehme(n) hiermit die Bürgschaft für

[Name des Mieters]
Hauptstraße 15, 50667 Köln

- nachfolgend "Hauptschuldner" genannt -

gegenüber dem Vermieter

Immobilien Schmidt GmbH
Hauptstraße 15, 50667 Köln

für das Mietverhältnis über die Wohnung/Gewerberäume:

Musterstraße 12, 12345 Berlin

§ 1 Umfang der Bürgschaft
Ich/Wir bürge(n) für alle Ansprüche des Vermieters gegen den Hauptschuldner aus dem Mietverhältnis, insbesondere für:

- Mietzahlungen (Nettokaltmiete und Nebenkosten)
- Schadensersatzansprüche
- Kosten der Rechtsverfolgung
- Rückbaukosten

§ 2 Höchstbetrag
Die Bürgschaft ist der Höhe nach beschränkt auf maximal 1.200,00 € (in Worten: 3 Euro).

☐ Dies entspricht 3 Monatskaltmieten à 1.200,00 €.

§ 3 Art der Bürgschaft
☐ Selbstschuldnerische Bürgschaft gemäß § 773 Abs. 1 Nr. 1 BGB
(Verzicht auf die Einrede der Vorausklage gem. § 771 BGB)

☐ Ausfallbürgschaft
(Inanspruchnahme erst nach erfolgloser Zwangsvollstreckung gegen Hauptschuldner)

§ 4 Dauer der Bürgschaft
Die Bürgschaft gilt:
☐ für die gesamte Dauer des Mietverhältnisses einschließlich Verlängerungen
☐ befristet bis zum 28.01.2026

Die Bürgschaft endet:
- 6 Monate nach Beendigung des Mietverhältnisses und ordnungsgemäßer Rückgabe
- mit vollständiger Erfüllung aller Verpflichtungen des Hauptschuldners

§ 5 Kündigung der Bürgschaft
☐ Die Bürgschaft kann nicht gekündigt werden.
☐ Die Bürgschaft kann mit einer Frist von 3 Monaten zum Monatsende gekündigt werden.

§ 6 Informationspflicht
Der Vermieter verpflichtet sich, den Bürgen unverzüglich über Zahlungsverzug oder Pflichtverletzungen des Hauptschuldners zu informieren.

§ 7 Bonitätsnachweis
Der Bürge erklärt:
☐ Nettoeinkommen von ca. 1.200,00 € monatlich
☐ Vermögen in Höhe von ca. 1.200,00 €
☐ Nachweis liegt bei (Gehaltsabrechnung / Steuerbescheid)

Berlin, den 29.12.2025

_______________________
[Unterschrift Bürge]

Angenommen:

_______________________
[Unterschrift Vermieter]`
  },
  {
    id: 'erbauseinandersetzung',
    name: 'Erbauseinandersetzungsvertrag Immobilie',
    category: 'Vertragsrecht',
    description: 'Auseinandersetzung einer Erbengemeinschaft',
    icon: '👨‍👩‍👧‍👦',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

ERBAUSEINANDERSETZUNGSVERTRAG

Die Miterben des verstorbenen

[Name des Erblassers]
verstorben am 28.01.2026 in Berlin

1. [Name Erbe 1], Hauptstraße 15, 50667 Köln, Erbquote: 3
2. [Name Erbe 2], Hauptstraße 15, 50667 Köln, Erbquote: 3
3. [Name Erbe 3], Hauptstraße 15, 50667 Köln, Erbquote: 3

- nachfolgend "Erbengemeinschaft" genannt -

vereinbaren zur Auseinandersetzung der Erbengemeinschaft gemäß §§ 2042 ff. BGB folgendes:

§ 1 Nachlassgegenstand
Zum Nachlass gehört insbesondere das Grundstück:

Gemarkung: 3, Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Anschrift: 3
Verkehrswert gemäß Gutachten: 1.200,00 €

§ 2 Teilungsplan
Die Erbengemeinschaft einigt sich auf folgende Auseinandersetzung:

☐ ÜBERNAHME DURCH EINEN MITERBEN:
[Name Erbe] übernimmt das Grundstück zum Wert von 1.200,00 €.

☐ VERKAUF AN DRITTE:
Das Grundstück wird zum Mindestpreis von 1.200,00 € verkauft.
Die Erbengemeinschaft beauftragt [Makler/Person] mit dem Verkauf.

☐ REALTEILUNG:
Das Grundstück wird aufgeteilt in:
- Flurstück 3 für [Erbe 1]
- Flurstück 3 für [Erbe 2]

§ 3 Ausgleichszahlungen
Der übernehmende Erbe zahlt an die weichenden Erben:

- An [Erbe 2]: 1.200,00 € (entspricht 3% Erbquote)
- An [Erbe 3]: 1.200,00 € (entspricht 3% Erbquote)

Zahlungsfrist: 3 nach notarieller Beurkundung

§ 4 Lasten und Verbindlichkeiten
☐ Das Grundstück wird lastenfrei übernommen.
☐ Bestehende Grundschulden in Höhe von 1.200,00 € übernimmt 3.

Nachlassverbindlichkeiten (Bestattungskosten, Steuern) werden entsprechend der Erbquoten getragen.

§ 5 Nutzungen und Lasten bis zur Auseinandersetzung
Für die Zeit bis zur Auseinandersetzung:
☐ [Erbe] darf die Immobilie nutzen und trägt alle Kosten.
☐ Mieteinnahmen werden entsprechend der Erbquoten verteilt.

§ 6 Gewährleistung
Die weichenden Erben gewährleisten nicht für Mängel, es sei denn, sie haben diese arglistig verschwiegen.

§ 7 Abgeltungsklausel
Mit Erfüllung dieses Vertrages sind alle wechselseitigen Ansprüche aus der Erbengemeinschaft abgegolten.

§ 8 Kosten
Die Kosten der Auseinandersetzung (Notar, Grundbuch, Gutachten) tragen die Erben entsprechend ihrer Erbquoten.

Berlin, den 29.12.2025

_______________________          _______________________
Erbe 1                           Erbe 2

_______________________
Erbe 3

Notarielle Beurkundung erforderlich!`
  },
  {
    id: 'vorvertrag_immobilie',
    name: 'Vorvertrag Immobilienkauf',
    category: 'Kaufverträge',
    description: 'Reservierungsvereinbarung vor Kaufvertrag',
    icon: '📝',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

VORVERTRAG / RESERVIERUNGSVEREINBARUNG
zum Kauf einer Immobilie

Zwischen

[Name Verkäufer], Hauptstraße 15, 50667 Köln
- nachfolgend "Verkäufer" genannt -

und

[Name Käufer], Hauptstraße 15, 50667 Köln
- nachfolgend "Käufer" genannt -

wird folgender Vorvertrag geschlossen:

§ 1 Vertragsgegenstand
Der Verkäufer beabsichtigt, dem Käufer folgendes Grundstück zu verkaufen:

Gemarkung: 3, Flur: 3, Flurstück: 3
Grundbuchblatt: 3
Anschrift: 3

§ 2 Kaufpreis
Der Kaufpreis soll 1.200,00 € betragen.

§ 3 Verpflichtung zum Hauptvertrag
Die Parteien verpflichten sich, bis zum 28.01.2026 einen notariellen Kaufvertrag abzuschließen.

Notar: [Name, Anschrift]
Termin: [Datum, Uhrzeit]

§ 4 Reservierung / Exklusivität
Der Verkäufer verpflichtet sich, das Grundstück bis zum 28.01.2026 ausschließlich dem Käufer anzubieten und nicht an Dritte zu veräußern oder zu belasten.

§ 5 Reservierungsgebühr
☐ Der Käufer zahlt eine Reservierungsgebühr von 1.200,00 €.
   - Bei Abschluss des Hauptvertrages: Anrechnung auf den Kaufpreis
   - Bei Nicht-Abschluss aus Gründen des Käufers: Verfall zugunsten Verkäufer
   - Bei Nicht-Abschluss aus Gründen des Verkäufers: Rückzahlung

☐ Keine Reservierungsgebühr.

§ 6 Finanzierungsvorbehalt
Der Käufer steht unter dem Vorbehalt der Finanzierungszusage bis zum 28.01.2026.

Bei Nicht-Erteilung der Finanzierungszusage kann der Käufer vom Vertrag zurücktreten (Nachweis der Absage erforderlich).

§ 7 Due Diligence / Prüfungsrechte
Der Käufer erhält bis zum 28.01.2026 das Recht zur Prüfung:
☐ Grundbuchauszug
☐ Baulastenverzeichnis
☐ Altlastenkataster
☐ Bauunterlagen
☐ Energieausweis
☐ Mietverträge (bei vermieteten Objekten)

§ 8 Rücktrittsrechte
☐ Käufer kann zurücktreten bei: 3
☐ Verkäufer kann zurücktreten bei: 3

§ 9 Vertragsstrafe
Bei schuldhafter Nicht-Erfüllung zahlt die säumige Partei eine Vertragsstrafe von 1.200,00 €.

§ 10 Salvatorische Klausel
Sollte eine Bestimmung unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.

Berlin, den 29.12.2025

_______________________          _______________________
Verkäufer                        Käufer`
  },
  {
    id: 'wohnungsübergabeprotokoll',
    name: 'Wohnungsübergabeprotokoll',
    category: 'Sonstiges',
    description: 'Protokoll bei Ein-/Auszug mit Zustandserfassung',
    icon: '📋',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

WOHNUNGSÜBERGABEPROTOKOLL

Übergabedatum: 3
Übergabezeit: 3 Uhr

Objekt: Hauptstraße 15, 50667 Köln

Anwesende Personen:
☐ Vermieter: [Name]
☐ Mieter: [Name]
☐ Vertreter Vermieter: [Name]
☐ Vertreter Mieter: [Name]
☐ Zeuge: [Name]

Art der Übergabe:
☐ Einzug / Übernahme der Wohnung
☐ Auszug / Rückgabe der Wohnung

═══════════════════════════════════════════════════

1. ZÄHLERSTÄNDE

Strom (Zähler-Nr. 3): [_____] kWh
Gas (Zähler-Nr. 3): [_____] m³
Wasser kalt (Zähler-Nr. 3): [_____] m³
Wasser warm (Zähler-Nr. 3): [_____] m³
Heizung (Zähler-Nr. 3): [_____]

═══════════════════════════════════════════════════

2. SCHLÜSSELÜBERGABE

Übergeben werden:
☐ Haustürschlüssel: 2
☐ Wohnungsschlüssel: 2
☐ Kellerschlüssel: 2
☐ Briefkastenschlüssel: 2
☐ Garagenschlüssel: 2
☐ Sonstige: 3

═══════════════════════════════════════════════════

3. ZUSTAND DER RÄUME

FLUR:
☐ Einwandfrei
☐ Mängel: 3

WOHNZIMMER:
☐ Einwandfrei
☐ Mängel: 3

SCHLAFZIMMER:
☐ Einwandfrei
☐ Mängel: 3

KINDERZIMMER:
☐ Einwandfrei
☐ Mängel: 3

KÜCHE:
☐ Einwandfrei
☐ Einbauküche vorhanden und funktionstüchtig
☐ Mängel: 3

BADEZIMMER:
☐ Einwandfrei
☐ Armaturen dicht
☐ Mängel: 3

BALKON / TERRASSE:
☐ Einwandfrei
☐ Mängel: 3

KELLER:
☐ Einwandfrei
☐ Mängel: 3

═══════════════════════════════════════════════════

4. ALLGEMEINER ZUSTAND

Böden (Parkett/Laminat/Fliesen):
☐ Einwandfrei
☐ Beschädigungen: 3

Wände:
☐ Renoviert / gestrichen
☐ Unrenoviert
☐ Beschädigungen: 3

Fenster und Türen:
☐ Einwandfrei, alle schließen dicht
☐ Mängel: 3

Heizung:
☐ Funktionstüchtig
☐ Mängel: 3

Sanitäre Anlagen:
☐ Einwandfrei
☐ Mängel: 3

═══════════════════════════════════════════════════

5. ZUSÄTZLICHE ANMERKUNGEN

[Freies Textfeld für sonstige Anmerkungen]

═══════════════════════════════════════════════════

6. VEREINBARUNGEN

☐ Schönheitsreparaturen wurden durchgeführt.
☐ Schönheitsreparaturen sind noch durchzuführen bis: 28.01.2026
☐ Mängel werden behoben bis: 28.01.2026
☐ Kaution: 1.200,00 € ist hinterlegt / wird zurückgezahlt

═══════════════════════════════════════════════════

FOTOS

☐ Fotos wurden angefertigt (siehe Anlage)
☐ Keine Fotos

═══════════════════════════════════════════════════

Berlin, den 29.12.2025

_______________________          _______________________
Vermieter / Vertreter            Mieter / Vertreter`
  },
  {
    id: 'nachbarschaftsvereinbarung',
    name: 'Nachbarschaftsvereinbarung',
    category: 'Vertragsrecht',
    description: 'Vereinbarung zwischen Grundstücksnachbarn',
    icon: '🏘️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

NACHBARSCHAFTSVEREINBARUNG

Zwischen den Eigentümern der benachbarten Grundstücke

Grundstück 1:
[Name Eigentümer 1], Hauptstraße 15, 50667 Köln
Gemarkung: 3, Flur: 3, Flurstück: 3
- nachfolgend "Partei 1" genannt -

und

Grundstück 2:
[Name Eigentümer 2], Hauptstraße 15, 50667 Köln
Gemarkung: 3, Flur: 3, Flurstück: 3
- nachfolgend "Partei 2" genannt -

wird folgende Nachbarschaftsvereinbarung geschlossen:

§ 1 Präambel
Die Parteien sind Eigentümer benachbarter Grundstücke und wollen ihr nachbarschaftliches Verhältnis einvernehmlich regeln.

§ 2 GRENZEINRICHTUNGEN

2.1 Grenzzaun / Grenzmauer:
☐ Die Kosten für Errichtung und Unterhaltung werden geteilt (je 50%).
☐ Partei 3 trägt die Kosten allein.
☐ Höhe: 3 m
☐ Material: 3
☐ Standort: auf der Grenze / auf Grundstück von Partei 3

2.2 Grenzhecke:
☐ Pflanzabstand zur Grenze: 3 m
☐ Maximale Höhe: 3 m
☐ Rückschnitt erfolgt durch: 3

§ 3 ÜBERHANG UND ÜBERFALL

3.1 Äste und Wurzeln:
Die Parteien dulden geringfügigen Überhang von Ästen bis 3 m.
Bei Beeinträchtigung: Rückschnitt nach Ankündigung.

3.2 Laub und Nadeln:
Ortsüblicher Laubfall wird gegenseitig geduldet.

§ 4 GRENZABSTÄNDE BEI BAUTEN

Beide Parteien verpflichten sich, die landesrechtlichen Abstandsvorschriften einzuhalten:
- Gebäude: mind. 3 m zur Grenze
- Garagen: mind. 3 m zur Grenze
- Nebenanlagen: mind. 3 m zur Grenze

☐ Ausnahme: [konkrete Vereinbarung]

§ 5 NUTZUNG DES NACHBARGRUNDSTÜCKS

☐ Partei 3 darf das Grundstück der anderen Partei betreten für:
   - Reparaturen an eigenem Gebäude
   - Baumpflege
   - [sonstige Zwecke]
   
Vorherige Ankündigung: 3 Tage

§ 6 REGENWASSER / ENTWÄSSERUNG

☐ Ablauf von Regenwasser auf das Nachbargrundstück wird geduldet.
☐ Jedes Grundstück muss sein Regenwasser auf eigenem Grund ableiten.
☐ Gemeinsame Drainage: Kosten werden 3 geteilt.

§ 7 STELLPLÄTZE / ZUFAHRT

☐ Partei 3 darf die Zufahrt über Grundstück 3 mitbenutzen.
☐ Kosten der Unterhaltung: 3

§ 8 LÄRMEMISSIONEN

Gegenseitige Rücksichtnahme:
- Gartenarbeiten mit lauten Geräten: Werktags 9-12 Uhr und 15-18 Uhr
- Rasenmähen: Werktags 7-20 Uhr, Sonn- und Feiertags nicht
- Musikinstrumente: [Regelung]

§ 9 GRILLEN

☐ Grillen ist auf beiden Grundstücken erlaubt.
☐ Holzkohlegrills mit Rücksicht auf Rauchentwicklung
☐ Häufigkeit: maximal 3 pro Monat

§ 10 HAUSTIERE

☐ Haltung von Haustieren wird gegenseitig geduldet.
☐ Hunde sind an der Grundstücksgrenze anzuleinen.
☐ Katzen dürfen die Grundstücke betreten.

§ 11 DAUER UND BINDUNG

Diese Vereinbarung gilt:
☐ unbefristet und geht auf Rechtsnachfolger über
☐ nur zwischen den jetzigen Eigentümern

☐ Grundbucheintragung als Baulast wird beantragt.

§ 12 STREITBEILEGUNG

Bei Meinungsverschiedenheiten vereinbaren die Parteien zunächst ein Schlichtungsgespräch.

Berlin, den 29.12.2025

_______________________          _______________________
Partei 1                         Partei 2`
  },
  {
    id: 'grundstueckskaufvertrag',
    name: 'Grundstückskaufvertrag (notariell)',
    category: 'Kaufverträge',
    description: 'Vollständiger notarieller Kaufvertrag für Grundstücke',
    icon: '📜',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

GRUNDSTÜCKSKAUFVERTRAG

Verhandelt zu [Ort] am 29.12.2025
vor dem Notar [Name], [Anschrift]
- UR-Nr. [________] -

Erschienen sind:

1. VERKÄUFER:
   [Name, Vorname]
   geboren am [Datum] in [Ort]
   wohnhaft: [Straße, PLZ Ort]
   
   [falls verheiratet:]
   mit Zustimmung der Ehefrau/des Ehemannes:
   [Name, Vorname]
   geboren am [Datum] in [Ort]
   
   - nachfolgend "Verkäufer" genannt -

2. KÄUFER:
   [Name, Vorname]
   geboren am [Datum] in [Ort]
   wohnhaft: [Straße, PLZ Ort]
   
   [falls verheiratet:]
   mit Zustimmung der Ehefrau/des Ehemannes:
   [Name, Vorname]
   geboren am [Datum] in [Ort]
   
   - nachfolgend "Käufer" genannt -

Die Erschienenen schließen folgenden

KAUFVERTRAG

═══════════════════════════════════════════════════

§ 1 KAUFGEGENSTAND

1.1 Der Verkäufer verkauft an den Käufer das im Grundbuch von [Amtsgericht], Blatt [____] eingetragene Grundstück:

Gemarkung: [_____________]
Flur: [___], Flurstück-Nr.: [_______]
Grundstücksgröße: ca. [_____] m²
Grundbuchart: [Wohnungsgrundbuch/Erbbaugrundbuch/etc.]

Anschrift: [Straße, PLZ Ort]

1.2 Das Grundstück ist bebaut mit:
☐ Einfamilienhaus, Baujahr [____], Wohnfläche ca. [___] m²
☐ Mehrfamilienhaus mit [__] Wohneinheiten
☐ unbebaut
☐ [sonstige Bebauung: _________________]

1.3 Zum Kaufgegenstand gehören:
☐ alle wesentlichen Bestandteile des Grundstücks
☐ das fest mit dem Grund und Boden verbundene Zubehör
☐ sämtliche Gebäude, Außenanlagen, Bepflanzungen
☐ [weitere Bestandteile: _________________]

1.4 NICHT zum Kaufgegenstand gehören (Ausnahmen):
☐ [aufzählen, z.B. bewegliche Gegenstände]

═══════════════════════════════════════════════════

§ 2 KAUFPREIS

2.1 Der Kaufpreis beträgt:

[____________] Euro (in Worten: [_____________] Euro)

und setzt sich wie folgt zusammen:
- Grundstücksanteil: [________] €
- Gebäudeanteil: [________] €
- [sonstige Anteile: ________] €

2.2 Der Kaufpreis ist frei von Mehrwertsteuer, da:
☐ Verkäufer ist Privatperson
☐ Verkauf erfolgt steuerfrei gem. § 4 Nr. 9a UStG
☐ [andere Begründung]

☐ Der Kaufpreis unterliegt der Mehrwertsteuer in Höhe von [__]%.

═══════════════════════════════════════════════════

§ 3 FÄLLIGKEIT UND ZAHLUNG

3.1 Der Kaufpreis wird fällig, sobald:
a) eine Auflassungsvormerkung zugunsten des Käufers im Grundbuch eingetragen ist,
b) der Notar dem Käufer mitgeteilt hat, dass alle Löschungsbewilligungen vorliegen oder durch Hinterlegung gesichert sind,
c) der Käufer die Genehmigung zur Eigentumsumschreibung erhalten hat, falls erforderlich (z.B. Vorkaufsrecht der Gemeinde),
d) der Notar die Unbedenklichkeitsbescheinigung des Finanzamts vorgelegt hat oder dem Käufer mitgeteilt hat, dass die Voraussetzungen erfüllt sind.

3.2 Zahlung:
Der Käufer zahlt den Kaufpreis auf das vom Notar anzugebende Konto des Verkäufers.
Zahlungsfrist: innerhalb von [14] Tagen nach Fälligkeit.

3.3 Verzugszinsen:
Bei verspäteter Zahlung: [5] % p.a. über Basiszinssatz.

═══════════════════════════════════════════════════

§ 4 EIGENTUMSÜBERGANG (AUFLASSUNG)

4.1 Der Verkäufer überträgt hiermit das Eigentum an dem Grundstück auf den Käufer (Auflassung gemäß § 925 BGB).

4.2 Der Käufer nimmt die Auflassung an.

4.3 Die Eintragung des Eigentumsübergangs im Grundbuch wird beantragt.

4.4 Der Verkäufer erklärt sich damit einverstanden, dass der Käufer bereits vor Eigentumsübergang mit Zustimmung des Verkäufers Baumaßnahmen durchführen darf.
☐ Ja ☐ Nein

═══════════════════════════════════════════════════

§ 5 AUFLASSUNGSVORMERKUNG

Zur Sicherung des Anspruchs auf Eigentumsübertragung wird zugunsten des Käufers eine Auflassungsvormerkung in Abteilung II des Grundbuchs eingetragen.

Die Bewilligung hierzu erklärt der Verkäufer.

═══════════════════════════════════════════════════

§ 6 BESITZÜBERGANG / NUTZUNGEN UND LASTEN

6.1 Besitzübergang:
Der Besitz, Nutzen und Lasten gehen über am: [TT.MM.JJJJ]

☐ Abweichende Regelung: [_________________]

6.2 Ab Besitzübergang:
- trägt der Käufer alle öffentlichen und privaten Lasten
- stehen dem Käufer alle Nutzungen zu
- trägt der Käufer die Gefahr des zufälligen Untergangs

6.3 Bis zum Besitzübergang:
- verwaltet der Verkäufer das Grundstück ordnungsgemäß
- darf der Verkäufer keine Verfügungen/Verpflichtungen treffen, die über den Besitzübergang hinaus wirken

═══════════════════════════════════════════════════

§ 7 GRUNDBUCHSTAND / LASTEN UND BESCHRÄNKUNGEN

7.1 Das Grundstück ist belastet/beschränkt wie aus dem als Anlage beigefügten Grundbuchauszug ersichtlich:

Abteilung II:
☐ Grunddienstbarkeiten: [_________________]
☐ Wegerechte: [_________________]
☐ Leitungsrechte: [_________________]
☐ Vorkaufsrechte: [_________________]
☐ Auflassungsvormerkungen: [_________________]

Abteilung III:
☐ Grundschulden: [Gläubiger, Betrag]
☐ Hypotheken: [Gläubiger, Betrag]
☐ Rentenschulden: [_________________]

7.2 ÜBERNAHME VON LASTEN:

☐ LASTENFREI:
Der Verkäufer verpflichtet sich, das Grundstück frei von allen Belastungen zu übertragen. Alle Grundpfandrechte (Grundschulden, Hypotheken) werden auf Kosten des Verkäufers gelöscht.

☐ LASTENÜBERNAHME:
Der Käufer übernimmt folgende Lasten:
- Grundschuld von [______] € zugunsten [Bank]
- [weitere Lasten: _________________]

Nicht übernommene Lasten werden auf Kosten des Verkäufers gelöscht.

7.3 Löschungsbewilligungen:
Der Verkäufer verpflichtet sich, alle erforderlichen Löschungsbewilligungen binnen [4 Wochen] beizubringen.

═══════════════════════════════════════════════════

§ 8 VORKAUFSRECHTE / GENEHMIGUNGEN

8.1 Vorkaufsrechte:
☐ Gesetzliches Vorkaufsrecht der Gemeinde liegt vor (§§ 24 ff. BauGB)
☐ Sonstiges Vorkaufsrecht: [_________________]
☐ Kein Vorkaufsrecht bekannt

8.2 Genehmigungen:
☐ Genehmigung nach Grundstücksverkehrsgesetz erforderlich
☐ Genehmigung nach GmbH-Gesetz / Handelsrecht erforderlich
☐ Keine Genehmigungen erforderlich

8.3 Rücktrittsrecht:
Falls eine erforderliche Genehmigung versagt wird, kann der betroffene Teil vom Vertrag zurücktreten.

═══════════════════════════════════════════════════

§ 9 GRUNDERWERBSTEUER

9.1 Die Grunderwerbsteuer trägt: ☐ Käufer ☐ Verkäufer ☐ je zur Hälfte

9.2 Für die steuerliche Unbedenklichkeitsbescheinigung ist zuständig:
Finanzamt [_________________]
Steuernummer des Verkäufers: [_________________]

═══════════════════════════════════════════════════

§ 10 BESCHAFFENHEIT / GEWÄHRLEISTUNG

10.1 ZUSTAND DES GRUNDSTÜCKS:
Der Verkäufer erklärt, dass das Grundstück sich in folgendem Zustand befindet:

Bebauung:
☐ bewohnbar und in ordnungsgemäßem Zustand
☐ renovierungsbedürftig
☐ Baujahr: [____], letzte Sanierung: [____]

Erschließung:
☐ voll erschlossen (Wasser, Abwasser, Strom, Gas)
☐ teilerschlossen: [_________________]

Altlasten:
☐ Dem Verkäufer sind keine Altlasten, Bodenverunreinigungen oder Kampfmittel bekannt
☐ Bekannte Altlasten: [_________________]

Baulasten:
☐ Keine Baulasten eingetragen
☐ Eingetragene Baulasten: [_________________]

10.2 GEWÄHRLEISTUNGSAUSSCHLUSS:
☐ Der Käufer kauft das Grundstück in dem Zustand, in dem es sich befindet ("gekauft wie besichtigt").
☐ Sachmängelgewährleistung ist ausgeschlossen, außer bei arglistig verschwiegenen Mängeln.

☐ GEWÄHRLEISTUNG:
Der Verkäufer gewährleistet für folgende Eigenschaften:
[_________________]

10.3 ENERGIEAUSWEIS:
☐ wurde dem Käufer vorgelegt
☐ wird nachgereicht
☐ nicht erforderlich (unbebaut)

═══════════════════════════════════════════════════

§ 11 MIET- UND PACHTVERHÄLTNISSE

11.1 Das Grundstück ist:
☐ vermietet/verpachtet (siehe Anlage Mietvertrag/Pachtvertrag)
☐ eigen genutzt / leer stehend

11.2 Bei Vermietung:
Der Käufer tritt in die Rechte und Pflichten aus den Miet-/Pachtverhältnissen ein (§ 566 BGB).

Aktuelle Miete/Pacht: [______] € monatlich
Kündigungsfrist: [_________________]
Mietkaution: [______] € (geht auf Käufer über)

═══════════════════════════════════════════════════

§ 12 VOLLMACHT ZUR EIGENTUMSUMSCHREIBUNG

Der Verkäufer erteilt hiermit dem beurkundenden Notar Vollmacht, den Eigentumsübergang im Grundbuch einzutragen bzw. die Eintragung zu beantragen.

═══════════════════════════════════════════════════

§ 13 KOSTEN UND STEUERN

13.1 Die Kosten dieses Vertrages tragen:
☐ Käufer allein
☐ Verkäufer allein
☐ je zur Hälfte

Dazu gehören:
- Notarkosten
- Grundbuchkosten  
- Kosten der Löschungen

13.2 Grunderwerbsteuer: siehe § 9

═══════════════════════════════════════════════════

§ 14 HAFTUNGSAUSSCHLUSS FÜR MAKLER

☐ Der Makler [Name] war an diesem Geschäft beteiligt.
   Maklercourtage: [____] % + MwSt., zu zahlen von: ☐ Käufer ☐ Verkäufer

☐ Es war kein Makler beteiligt.

═══════════════════════════════════════════════════

§ 15 SALVATORISCHE KLAUSEL

Sollten einzelne Bestimmungen dieses Vertrages unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.

═══════════════════════════════════════════════════

§ 16 VERTRAGSAUSFERTIGUNG

Von dieser Urkunde erhält jede Partei eine Ausfertigung.

═══════════════════════════════════════════════════

ANLAGEN:
☐ Grundbuchauszug
☐ Flurkarte/Lageplan
☐ Baulastenverzeichnis
☐ Energieausweis
☐ Mietverträge
☐ [weitere: _________________]

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

VERKÄUFER:                        KÄUFER:

_______________________          _______________________
[Unterschrift]                   [Unterschrift]

_______________________          _______________________
[Ehepartner]                     [Ehepartner]


NOTAR:

_______________________
[Unterschrift + Siegel]

═══════════════════════════════════════════════════
Notarielle Beurkundung gem. § 311b Abs. 1 BGB zwingend erforderlich!
Ohne notarielle Beurkundung ist der Vertrag nichtig.
═══════════════════════════════════════════════════`
  },
  {
    id: 'wohnungskaufvertrag',
    name: 'Wohnungskaufvertrag (WEG)',
    category: 'Kaufverträge',
    description: 'Notarieller Kaufvertrag für Eigentumswohnungen',
    icon: '🏢',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

WOHNUNGSKAUFVERTRAG
(Eigentumswohnung nach WEG)

Verhandelt zu [Ort] am 29.12.2025
vor dem Notar [Name], [Anschrift]
- UR-Nr. [________] -

Erschienen sind:

VERKÄUFER: [Name, Anschrift, Geburtsdatum]
KÄUFER: [Name, Anschrift, Geburtsdatum]

═══════════════════════════════════════════════════

§ 1 KAUFGEGENSTAND

1.1 WOHNUNGSEIGENTUM:
Der Verkäufer verkauft an den Käufer das im Grundbuch von [AG], Blatt [___] eingetragene Wohnungseigentum:

Wohnung Nr. [__] im [__] OG
Gemarkung: [_______], Flur: [__], Flurstück: [__]
Anschrift: [Straße, PLZ Ort]

1.2 SONDEREIGENTUM (§ 3 WEG):
- Wohnfläche: ca. [___] m²
- Zimmer: [__]
- Räume: [Wohnzimmer, Schlafzimmer, Küche, Bad, etc.]
- Balkon/Terrasse: [__] m²

1.3 MITEIGENTUMSANTEIL:
[______]/[______] am gemeinschaftlichen Eigentum

1.4 GEMEINSCHAFTLICHES EIGENTUM (§ 1 Abs. 5 WEG):
- Grundstück
- Gebäude (tragende Wände, Dach, Fassade)
- Treppenhaus, Flure
- Heizungsanlage, Aufzug
- Außenanlagen

1.5 SONDERNUTZUNGSRECHTE:
☐ Stellplatz Nr. [__]
☐ Kellerraum Nr. [__]  
☐ Garten/Terrasse: [__] m²
☐ [sonstige: _______]

═══════════════════════════════════════════════════

§ 2 TEILUNGSERKLÄRUNG

Die Teilungserklärung vom [Datum], eingetragen im Grundbuch am [Datum], regelt:
- Aufteilung des Gebäudes
- Miteigentumsanteile
- Gemeinschaftsordnung
- Hausordnung
- Kostenverteilung

Der Käufer erhält eine beglaubigte Abschrift.

═══════════════════════════════════════════════════

§ 3 KAUFPREIS

3.1 Gesamtkaufpreis: [__________] Euro

davon:
- Wohnung: [_______] €
- Stellplatz: [_______] €
- [sonstige: _______] €

3.2 ☐ Umsatzsteuerfrei gem. § 4 Nr. 9a UStG
    ☐ zzgl. [__]% MwSt = [_______] €

═══════════════════════════════════════════════════

§ 4 EIGENTÜMERGEMEINSCHAFT

4.1 BESCHLÜSSE:
Der Käufer tritt in alle bestehenden WEG-Beschlüsse ein.

4.2 HAUSGELD:
Monatliches Hausgeld: ca. [______] €
(Verwaltung, Instandhaltung, Betriebskosten)

4.3 INSTANDHALTUNGSRÜCKLAGE:
Aktueller Stand: [______] €
☐ bleibt bei der Gemeinschaft
☐ anteilige Auszahlung an Verkäufer: [____] €

4.4 VERWALTER:
[Name], [Anschrift]
Vertrag läuft bis: [Datum]

═══════════════════════════════════════════════════

§ 5 GEWÄHRLEISTUNG

5.1 Der Käufer kauft die Wohnung "wie besichtigt".

5.2 Sachmängelgewährleistung ist ausgeschlossen, außer bei arglistig verschwiegenen Mängeln.

5.3 ZUSTAND:
☐ renoviert / neuwertig
☐ gepflegt / bewohnbar
☐ renovierungsbedürftig

5.4 Baujahr Gebäude: [____]
    Letzte Sanierung: [____]

═══════════════════════════════════════════════════

§ 6 VERMIETUNG

☐ Die Wohnung ist vermietet
    Mieter: [Name]
    Miete: [____] € kalt + [___] € NK
    Mietvertrag seit: [Datum]
    Kaution: [____] € (geht auf Käufer über)

☐ Die Wohnung ist frei / eigengenutzt

═══════════════════════════════════════════════════

§ 7 BESITZÜBERGANG

Besitz, Nutzen und Lasten gehen über am: [TT.MM.JJJJ]

Ab diesem Zeitpunkt:
- trägt der Käufer das Hausgeld
- zahlt der Käufer Versicherungen
- stehen dem Käufer Mieteinnahmen zu

═══════════════════════════════════════════════════

§ 8 SONSTIGES

Energieausweis: ☐ vorgelegt ☐ wird nachgereicht
Wohnflächenberechnung: ☐ liegt vor
Protokolle letzte Eigentümerversammlungen: ☐ übergeben

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

VERKÄUFER:                    KÄUFER:

___________________          ___________________

NOTAR:
___________________

═══════════════════════════════════════════════════
Notarielle Beurkundung gem. § 311b BGB erforderlich!
═══════════════════════════════════════════════════`
  },
  {
    id: 'auflassungserklaerung',
    name: 'Auflassungserklärung',
    category: 'Grundbuchrecht',
    description: 'Einigung über Eigentumsübergang § 925 BGB',
    icon: '✍️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

AUFLASSUNGSERKLÄRUNG
gem. § 925 BGB

Verhandelt am 29.12.2025
vor Notar [Name], [Anschrift]

VERÄUSSERER:
[Name, Anschrift, Geburtsdatum]

ERWERBER:
[Name, Anschrift, Geburtsdatum]

═══════════════════════════════════════════════════

§ 1 GRUNDSTÜCK

Gegenstand ist das im Grundbuch von [AG], Blatt [___] eingetragene Grundstück:

Gemarkung: [_______]
Flur: [__], Flurstück: [______]
Grundbuchblatt: [______]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

§ 2 AUFLASSUNG

Der Veräußerer überträgt hiermit das Eigentum an dem Grundstück auf den Erwerber (Auflassung gemäß § 925 BGB).

Der Erwerber nimmt die Auflassung an.

═══════════════════════════════════════════════════

§ 3 GRUNDBUCHEINTRAGUNG

Die Beteiligten bewilligen die Eintragung der Eigentumsumschreibung im Grundbuch.

Der Veräußerer erteilt dem Notar Vollmacht zur Antragstellung.

═══════════════════════════════════════════════════

§ 4 KOSTEN

Die Kosten trägt: ☐ Erwerber ☐ Veräußerer ☐ je zur Hälfte

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

_______________________          _______________________
Veräußerer                       Erwerber

_______________________
Notar (mit Siegel)

═══════════════════════════════════════════════════
Notarielle Beurkundung gem. § 925 BGB zwingend!
═══════════════════════════════════════════════════`
  },
  {
    id: 'loeschungsbewilligung_grundschuld',
    name: 'Löschungsbewilligung Grundschuld',
    category: 'Grundbuchrecht',
    description: 'Zur Löschung von Grundschulden nach Tilgung',
    icon: '🗑️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

LÖSCHUNGSBEWILLIGUNG
für Grundschuld

[Name der Bank / des Gläubigers]
[Anschrift]

- nachfolgend "Gläubiger" -

bewilligt hiermit die Löschung der nachstehend bezeichneten Grundschuld:

═══════════════════════════════════════════════════

BELASTETES GRUNDSTÜCK:

Grundbuch von [Amtsgericht], Blatt [______]
Gemarkung: [_______]
Flur: [__], Flurstück: [______]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

GRUNDSCHULD:

Eingetragen in Abteilung III unter lfd. Nr. [__]

Betrag: [__________] Euro
Gläubiger: [Name der Bank]
Eingetragen am: [Datum]

☐ mit Brief
☐ ohne Brief (Brieferteilungsausschluss)

═══════════════════════════════════════════════════

LÖSCHUNGSBEWILLIGUNG:

Der Gläubiger bewilligt die vollständige Löschung der vorgenannten Grundschuld aus Abteilung III des Grundbuchs.

☐ Die zur Grundschuld gehörende Zwangsversteigerungsvollstreckungsunterwerfung ist ebenfalls zu löschen.

═══════════════════════════════════════════════════

GRUNDSCHULDBRIEF:

☐ Der Grundschuldbrief wird in Urschrift beigefügt.
☐ Es wurde kein Brief erteilt (Brieferteilungsausschluss).
☐ Der Brief ist verloren gegangen (Aufgebotsverfahren: Az. [___]).

═══════════════════════════════════════════════════

VOLLSTÄNDIGE TILGUNG:

Der Gläubiger bestätigt, dass die gesicherte Forderung vollständig getilgt ist und keine Ansprüche mehr bestehen.

═══════════════════════════════════════════════════

VOLLMACHT:

Der Gläubiger erteilt dem Grundstückseigentümer sowie jedem Notar Vollmacht, die Löschung der Grundschuld im Grundbuch zu beantragen.

═══════════════════════════════════════════════════

BEGLAUBIGUNG:

☐ Die Unterschrift wird notariell beglaubigt.
☐ Die Unterschrift wird durch das Grundbuchamt beglaubigt.

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

[Name der Bank / Gläubiger]

_______________________
Unterschrift (mit Stempel)

_______________________
Beglaubigungsvermerk

═══════════════════════════════════════════════════
HINWEIS:
Die Löschung kann erst erfolgen, wenn die Löschungsbewilligung
mit beglaubigter Unterschrift dem Grundbuchamt vorliegt.
═══════════════════════════════════════════════════`
  },
  {
    id: 'grundschuldbestellung',
    name: 'Grundschuldbestellung',
    category: 'Grundbuchrecht',
    description: 'Zur Absicherung von Darlehen',
    icon: '🏦',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

GRUNDSCHULDBESTELLUNG

Verhandelt am 29.12.2025
vor Notar [Name], [Anschrift]
- UR-Nr. [________] -

Erschienen:

GRUNDSTÜCKSEIGENTÜMER (Besteller):
[Name, Anschrift, Geburtsdatum]
☐ mit Zustimmung des Ehepartners: [Name]

GLÄUBIGER:
[Name der Bank], [Anschrift]
vertreten durch: [_______]

═══════════════════════════════════════════════════

§ 1 BELASTETES GRUNDSTÜCK

Grundbuch von [Amtsgericht], Blatt [______]
Gemarkung: [_______], Flur: [__], Flurstück: [______]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

§ 2 GRUNDSCHULDBESTELLUNG

Der Grundstückseigentümer bestellt zugunsten des Gläubigers eine

☐ Briefgrundschuld
☐ Buchgrundschuld (ohne Brief)

in Höhe von: [__________] Euro (in Worten: [___________] Euro)

zuzüglich [__]% Jahreszinsen.

═══════════════════════════════════════════════════

§ 3 ZWECK DER GRUNDSCHULD

Die Grundschuld dient zur Sicherung:

☐ Darlehen über [_______] € vom [Datum]
   Darlehensvertrag vom [Datum]
   
☐ aller bestehenden und künftigen Forderungen aus der Geschäftsverbindung

☐ [sonstiger Zweck: _________________]

Sicherungszweckvereinbarung: siehe Anlage

═══════════════════════════════════════════════════

§ 4 ZINSEN UND NEBENLEISTUNGEN

Zinssatz: [__]% jährlich

Nebenleistungen:
☐ Verzugszinsen: [__]% p.a.
☐ Kosten der Rechtsverfolgung
☐ Sonstige: [_________________]

═══════════════════════════════════════════════════

§ 5 ZWANGSVOLLSTRECKUNGSUNTERWERFUNG

Der Grundstückseigentümer unterwirft sich der sofortigen Zwangsvollstreckung in das Grundstück wegen der Grundschuld und der Zinsen.

☐ Zusätzlich: Unterwerfung in das gesamte Vermögen (§ 800 ZPO)

═══════════════════════════════════════════════════

§ 6 EINTRAGUNG IM GRUNDBUCH

Die Grundschuld wird eingetragen in:

Abteilung III unter laufender Nr. [__]

☐ im 1. Rang (erstrangig)
☐ im Rang nach lfd. Nr. [__]
☐ im gleichrangigen Verhältnis mit lfd. Nr. [__]

Rangvorbehalt:
☐ Für weitere Belastungen bis [_____] € wird der Rang vorbehalten.

═══════════════════════════════════════════════════

§ 7 GRUNDSCHULDBRIEF

☐ BRIEFGRUNDSCHULD:
   Der Grundschuldbrief wird erteilt und dem Gläubiger ausgehändigt.
   
☐ BUCHGRUNDSCHULD:
   Die Erteilung eines Grundschuldbriefes ist ausgeschlossen (§ 1116 Abs. 2 BGB).

═══════════════════════════════════════════════════

§ 8 DINGLICHES VERWERTUNGSRECHT

Bei Fälligkeit der Grundschuld ist der Gläubiger berechtigt:

☐ Zwangsversteigerung des Grundstücks zu betreiben
☐ Zwangsverwaltung anzuordnen

═══════════════════════════════════════════════════

§ 9 ABTRETUNG UND TEILUNG

☐ Die Grundschuld ist abtretbar.
☐ Die Grundschuld ist teilbar.

═══════════════════════════════════════════════════

§ 10 KOSTEN

Die Kosten der Bestellung (Notar, Grundbuch) trägt:
☐ der Grundstückseigentümer
☐ der Gläubiger
☐ je zur Hälfte

═══════════════════════════════════════════════════

§ 11 EINTRAGUNGSVOLLMACHT

Der Notar wird bevollmächtigt, die Eintragung der Grundschuld zu beantragen.

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

GRUNDSTÜCKSEIGENTÜMER:

_______________________
[Unterschrift]

_______________________
[Ehepartner]

NOTAR:

_______________________
(mit Siegel)

═══════════════════════════════════════════════════
Notarielle Beurkundung gem. § 1192 BGB i.V.m. § 873 BGB
zwingend erforderlich!
═══════════════════════════════════════════════════`
  },
  {
    id: 'reallast_vertrag',
    name: 'Reallast-Vertrag',
    category: 'Grundbuchrecht',
    description: 'Wiederkehrende Leistungen aus Grundstück',
    icon: '💶',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

REALLAST-BESTELLUNG
gem. §§ 1105 ff. BGB

Verhandelt am 29.12.2025
vor Notar [Name], [Anschrift]

VERPFLICHTETER (Grundstückseigentümer):
[Name, Anschrift, Geburtsdatum]

BERECHTIGTER:
[Name, Anschrift, Geburtsdatum]

═══════════════════════════════════════════════════

§ 1 BELASTETES GRUNDSTÜCK

Grundbuch von [AG], Blatt [___]
Gemarkung: [_______], Flur: [__], Flurstück: [__]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

§ 2 REALLAST

Der Verpflichtete bestellt zugunsten des Berechtigten eine Reallast mit folgendem Inhalt:

☐ LEIBRENTE / ALTENTEILSLEISTUNG:
   Monatlich: [______] Euro
   Jährlich: [______] Euro
   Zahlung zum: [Monatsletzten / Monatsersten]

☐ VERSORGUNGSLEISTUNGEN:
   - Wohnrecht im [Beschreibung]
   - Verpflegung
   - Pflege im Krankheitsfall
   - [weitere: _________________]

☐ NATURALLEISTUNGEN:
   [Beschreibung: z.B. Lieferung von Heizmaterial, etc.]

☐ SONSTIGE LEISTUNGEN:
   [_________________]

═══════════════════════════════════════════════════

§ 3 DAUER DER REALLAST

☐ Lebenslänglich für: [Name des Berechtigten]
☐ Befristet bis: [Datum]
☐ Unbefristet

═══════════════════════════════════════════════════

§ 4 WERTSICHERUNG

☐ Die Zahlungen werden jährlich an den Verbraucherpreisindex angepasst.
☐ Keine Wertsicherung.

═══════════════════════════════════════════════════

§ 5 ABLÖSUNG

☐ Die Reallast kann nicht abgelöst werden.
☐ Die Reallast kann abgelöst werden gegen Zahlung von: [_____] €
☐ Die Reallast kann abgelöst werden nach Vereinbarung.

═══════════════════════════════════════════════════

§ 6 ZWANGSVOLLSTRECKUNGSUNTERWERFUNG

Der Verpflichtete unterwirft sich der sofortigen Zwangsvollstreckung in das Grundstück wegen rückständiger Leistungen.

═══════════════════════════════════════════════════

§ 7 GRUNDBUCHEINTRAGUNG

Die Reallast wird eingetragen in Abteilung II des Grundbuchs.

Rang: ☐ 1. Rang ☐ nach lfd. Nr. [__]

═══════════════════════════════════════════════════

§ 8 KOSTEN

Notarkosten und Grundbuchkosten trägt: ☐ Verpflichteter ☐ Berechtigter

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

_______________________          _______________________
Verpflichteter                   Berechtigter

_______________________
Notar

═══════════════════════════════════════════════════
Notarielle Beurkundung gem. § 1108 BGB erforderlich!
═══════════════════════════════════════════════════`
  },
  {
    id: 'vorkaufsrechtsverzicht',
    name: 'Vorkaufsrechtsverzicht',
    category: 'Sonstiges',
    description: 'Verzicht auf gesetzliches/vertragliches Vorkaufsrecht',
    icon: '🚫',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

VERZICHT AUF VORKAUFSRECHT

Der/Die Vorkaufsberechtigte

[Name, Anschrift, Geburtsdatum]

verzichtet hiermit unwiderruflich auf die Ausübung des

☐ gesetzlichen Vorkaufsrechts gem. § 463 BGB
☐ vertraglichen Vorkaufsrechts
☐ dinglichen Vorkaufsrechts (eingetragen im Grundbuch)

betreffend das Grundstück:

═══════════════════════════════════════════════════

GRUNDSTÜCK:

Grundbuch von [AG], Blatt [___]
Gemarkung: [_______], Flur: [__], Flurstück: [__]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

VORKAUFSRECHT:

☐ Eingetragen in Abteilung II unter lfd. Nr. [__]
☐ Vereinbart im Vertrag vom [Datum]
☐ Gesetzliches Vorkaufsrecht der Gemeinde gem. §§ 24 ff. BauGB

═══════════════════════════════════════════════════

KAUFVERTRAG:

Der Verzicht erfolgt im Zusammenhang mit dem Kaufvertrag:

Verkäufer: [Name]
Käufer: [Name]
Kaufpreis: [_________] €
Notarvertrag vom: [Datum]

═══════════════════════════════════════════════════

VERZICHTSERKLÄRUNG:

Der Vorkaufsberechtigte erklärt hiermit unwiderruflich:

1. Er verzichtet auf die Ausübung des Vorkaufsrechts.

2. Er erteilt seine Zustimmung zum Verkauf des Grundstücks an den vorgenannten Käufer.

3. Er verpflichtet sich, keine Ansprüche aus dem Vorkaufsrecht geltend zu machen.

☐ Der Verzicht erfolgt entgeltlich gegen Zahlung von [_____] €.
☐ Der Verzicht erfolgt unentgeltlich.

═══════════════════════════════════════════════════

LÖSCHUNGSBEWILLIGUNG:

☐ Der Vorkaufsberechtigte bewilligt die Löschung des dinglichen Vorkaufsrechts aus Abteilung II des Grundbuchs.

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

_______________________
Vorkaufsberechtigter

☐ Notarielle Beglaubigung der Unterschrift

_______________________
Beglaubigungsvermerk

═══════════════════════════════════════════════════
Bei dinglichen Vorkaufsrechten:
Notarielle Beglaubigung der Unterschrift erforderlich!
═══════════════════════════════════════════════════`
  },
  {
    id: 'niessbrauchsvertrag',
    name: 'Nießbrauchsvertrag',
    category: 'Grundbuchrecht',
    description: 'Bestellung eines Nießbrauchsrechts an Immobilien',
    icon: '🏡',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

NIESSBRAUCHSBESTELLUNG
gem. §§ 1030 ff. BGB

Verhandelt am 29.12.2025
vor Notar [Name], [Anschrift]

EIGENTÜMER (Besteller):
[Name, Anschrift, Geburtsdatum]

NIESSBRAUCHSBERECHTIGTER:
[Name, Anschrift, Geburtsdatum]

═══════════════════════════════════════════════════

§ 1 BELASTETES GRUNDSTÜCK

Grundbuch von [AG], Blatt [___]
Gemarkung: [_______], Flur: [__], Flurstück: [__]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

§ 2 NIESSBRA UCHSBESTELLUNG

Der Eigentümer bestellt zugunsten des Nießbrauchsberechtigten ein

☐ lebenslanges
☐ zeitlich befristetes bis [Datum]

Nießbrauchsrecht an dem vorgenannten Grundstück.

═══════════════════════════════════════════════════

§ 3 UMFANG DES NIESSBRAUCHS

Der Nießbrauchsberechtigte ist berechtigt:

☐ WOHNRECHT:
   - Nutzung der gesamten Immobilie
   - Nutzung folgender Räume: [_________________]
   - Mitnutzung von: [Garten, Garage, etc.]

☐ VERMIETUNGSRECHT:
   - Vermietung der Immobilie oder Teilen davon
   - Mieteinnahmen stehen dem Nießbrauchsberechtigten zu

☐ VOLLSTÄNDIGER NIESSBRAUCH:
   - Alle Nutzungen der Immobilie
   - Alle Früchte und Erträge (Mieten, etc.)

═══════════════════════════════════════════════════

§ 4 PFLICHTEN DES NIESSBRAUCHSBERECHTIGTEN

4.1 ERHALTUNGSPFLICHT:
Der Nießbrauchsberechtigte ist verpflichtet, die Immobilie in ordnungsgemäßem Zustand zu erhalten.

4.2 INSTANDHALTUNG:
☐ Laufende Instandhaltung trägt der Nießbrauchsberechtigte.
☐ Außergewöhnliche Reparaturen trägt der Eigentümer.

4.3 LASTEN UND ABGABEN:
Der Nießbrauchsberechtigte trägt:
☐ Grundsteuer
☐ Versicherungen (Gebäude, Haftpflicht)
☐ Betriebskosten (Wasser, Heizung, Müll, etc.)
☐ Schornsteinfeger
☐ [sonstige: _________________]

Der Eigentümer trägt:
☐ außergewöhnliche Lasten
☐ Grundschuldzinsen
☐ [sonstige: _________________]

═══════════════════════════════════════════════════

§ 5 VERÄNDERUNGEN

Der Nießbrauchsberechtigte darf:
☐ keine baulichen Veränderungen vornehmen
☐ nur mit Zustimmung des Eigentümers bauliche Veränderungen vornehmen
☐ geringfügige Anpassungen vornehmen

═══════════════════════════════════════════════════

§ 6 VERSICHERUNG

☐ Der Nießbrauchsberechtigte versichert die Immobilie angemessen.
☐ Der Eigentümer unterhält die Versicherung, Prämien zahlt der Nießbrauchsberechtigte.

═══════════════════════════════════════════════════

§ 7 ABLÖSUNGSRECHT

☐ Der Nießbrauch kann nicht abgelöst werden.
☐ Der Nießbrauch kann abgelöst werden gegen Zahlung von [_____] €.
☐ Ablösung nach Vereinbarung möglich.

═══════════════════════════════════════════════════

§ 8 ÜBERTRAGBARKEIT

☐ Der Nießbrauch ist nicht übertragbar (höchstpersönlich).
☐ Der Nießbrauch ist übertragbar mit Zustimmung des Eigentümers.

═══════════════════════════════════════════════════

§ 9 BEENDIGUNG

Der Nießbrauch endet:
☐ mit dem Tod des Nießbrauchsberechtigten
☐ am [Datum]
☐ durch Verzicht
☐ bei schwerwiegender Pflichtverletzung (Kündigung)

═══════════════════════════════════════════════════

§ 10 GRUNDBUCHEINTRAGUNG

Der Nießbrauch wird eingetragen in Abteilung II des Grundbuchs.

Rang: ☐ 1. Rang ☐ nach lfd. Nr. [__]

═══════════════════════════════════════════════════

§ 11 KOSTEN

Notar- und Grundbuchkosten trägt: ☐ Eigentümer ☐ Nießbrauchsberechtigter

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

_______________________          _______________________
Eigentümer                       Nießbrauchsberechtigter

_______________________
Notar

═══════════════════════════════════════════════════
Notarielle Beurkundung gem. § 873 BGB erforderlich!
═══════════════════════════════════════════════════`
  },
  {
    id: 'baulastverpflichtung',
    name: 'Baulastverpflichtung',
    category: 'Sonstiges',
    description: 'Öffentlich-rechtliche Verpflichtung gegenüber Baubehörde',
    icon: '🏗️',
    forRoles: ['ANWALT'],
    content: `⚠️ HINWEIS: Diese Vorlage dient nur zu Informationszwecken und stellt keine Rechtsberatung dar.

BAULASTERKLÄRUNG

An die
[Bauaufsichtsbehörde / Untere Bauaufsicht]
[Anschrift]

BAULASTVERPFLICHTETER (Grundstückseigentümer):
[Name, Anschrift, Geburtsdatum]

═══════════════════════════════════════════════════

BELASTETES GRUNDSTÜCK:

Gemarkung: [_______]
Flur: [__], Flurstück: [______]
Grundbuch: [AG], Blatt [___]
Anschrift: [Straße, PLZ Ort]

═══════════════════════════════════════════════════

BAULASTERKLÄRUNG:

Der Grundstückseigentümer verpflichtet sich gegenüber der Bauaufsichtsbehörde zu folgender Baulast:

☐ ABSTANDSFLÄCHENBAULAST:
   Der Grundstückseigentümer verpflichtet sich, die von dem Nachbargrundstück [Flurstück Nr.] überfallenden Abstandsflächen zu dulden.
   
   Ausmaß: [____] m × [____] m
   Siehe Lageplan (Anlage)

☐ STELLPLATZBAULAST:
   Der Grundstückseigentümer verpflichtet sich, auf dem Grundstück dauerhaft [__] Stellplätze für das Bauvorhaben auf Grundstück [Flurstück Nr.] bereitzustellen und zu unterhalten.

☐ GRENZBEBAUUNG:
   Der Grundstückseigentümer duldet die Bebauung an der gemeinsamen Grundstücksgrenze durch das Nachbargrundstück [Flurstück Nr.].

☐ ZUFAHRTSBAULAST:
   Der Grundstückseigentümer gestattet die Nutzung seines Grundstücks als Zufahrt für das Grundstück [Flurstück Nr.].
   Breite: [__] m, Lage: siehe Plan

☐ ÜBERBAUUNG:
   Der Grundstückseigentümer duldet die Überbauung seines Grundstücks durch [Beschreibung: z.B. Dachüberstand, Balkon] vom Nachbargrundstück [Flurstück Nr.].

☐ SONSTIGE BAULAST:
   [genaue Beschreibung: _________________]

═══════════════════════════════════════════════════

UMFANG DER BAULAST:

Die Baulast gilt:
☐ unbefristet
☐ befristet bis [Datum]
☐ bis zur Aufhebung durch die Bauaufsichtsbehörde

═══════════════════════════════════════════════════

BEGÜNSTIGTES GRUNDSTÜCK:

☐ Grundstück: Flur [__], Flurstück [__]
   Eigentümer: [Name]
   
Die Baulast erfolgt zugunsten des Bauvorhabens:
[Beschreibung des Bauvorhabens]

═══════════════════════════════════════════════════

WIRKUNG:

1. Die Baulast bindet den Verpflichteten und seine Rechtsnachfolger.

2. Die Baulast wird in das Baulastenverzeichnis eingetragen.

3. Ein Anspruch auf Löschung besteht nur mit Zustimmung der Bauaufsichtsbehörde und ggf. des Begünstigten.

☐ Die Baulast wird als Vermerk im Grundbuch eingetragen (freiwillig).

═══════════════════════════════════════════════════

ENTGELT:

☐ Die Baulast wird unentgeltlich erteilt.
☐ Der Begünstigte zahlt eine Entschädigung von [_____] €.
☐ Regelung der Gegenleistung: [_________________]

═══════════════════════════════════════════════════

ZUSTIMMUNG:

☐ Der Ehepartner stimmt dieser Baulast zu:
   [Name, Unterschrift]
   
☐ Der dinglich Berechtigte (z.B. Grundschuldgläubiger) stimmt zu:
   [Name, Unterschrift]

═══════════════════════════════════════════════════

ANLAGEN:
☐ Lageplan im Maßstab 1:[___]
☐ Bauzeichnungen
☐ [weitere: _________________]

═══════════════════════════════════════════════════

[Ort], den 29.12.2025

_______________________
Grundstückseigentümer

☐ Notarielle Beglaubigung der Unterschrift:

_______________________
Notar/Beglaubigungsbehörde

═══════════════════════════════════════════════════

VERMERK DER BAUAUFSICHTSBEHÖRDE:

Die Baulast wird eingetragen in das Baulastenverzeichnis unter Nr. [_____].

[Ort], den [Datum]

_______________________
Bauaufsichtsbehörde (Stempel)

═══════════════════════════════════════════════════
HINWEIS:
Baulasten sind öffentlich-rechtliche Verpflichtungen und binden
auch Rechtsnachfolger. Eintragung im Baulastenverzeichnis.
═══════════════════════════════════════════════════`
  }
];

function TemplatesContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [userData, setUserData] = useState<any>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [showEditor, setShowEditor] = useState(false);
  const [editedContent, setEditedContent] = useState<string | null>(null);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const [queriesUsed, setQueriesUsed] = useState(0);
  const [queriesLimit, setQueriesLimit] = useState(0);
  
  // Check if user has access for templates (Basis or higher)
  const hasAccess = hasTierAccess(userTier, 'basis');
  
  // Wrapper for actions that require tier
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };
  
  // Neue States für benutzerdefinierte Vorlagen
  const [customTemplates, setCustomTemplates] = useState<Template[]>([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [isCreatingTemplate, setIsCreatingTemplate] = useState(false);
  const [newTemplateName, setNewTemplateName] = useState('');
  const [newTemplateType, setNewTemplateType] = useState('');
  const [newTemplateContext, setNewTemplateContext] = useState('');
  const [kiGeneratedContent, setKiGeneratedContent] = useState('');
  
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';

  // Fetch user data to determine dashboard type
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        setCurrentUser(user);
        const userDoc = await getDoc(doc(db, 'users', user.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          setUserData(data);
          const tier = data.tier || data.dashboardType || 'free';
          setUserTier(tier);
          setQueriesUsed(data.queriesUsed || 0);
          setQueriesLimit(data.queriesLimit || 0);
        }
        // Lade benutzerdefinierte Vorlagen
        await loadCustomTemplates(user.uid);
      } else {
        router.push('/auth/login');
      }
    });
    return () => unsubscribe();
  }, [router]);

  // URL-Parameter für Fallanalyse-Links verarbeiten
  useEffect(() => {
    const createType = searchParams.get('create');
    const context = searchParams.get('context');
    const streitpunkt = searchParams.get('streitpunkt');
    
    if (createType) {
      setNewTemplateType(createType);
      setNewTemplateContext(context ? decodeURIComponent(context) : '');
      if (streitpunkt) {
        setNewTemplateContext(prev => prev + '\n\nStreitpunkt: ' + decodeURIComponent(streitpunkt));
      }
      setShowCreateModal(true);
    }
  }, [searchParams]);

  // Benutzerdefinierte Vorlagen laden
  const loadCustomTemplates = async (userId: string) => {
    try {
      const q = query(collection(db, 'custom_templates'), where('userId', '==', userId));
      const snapshot = await getDocs(q);
      const templates: Template[] = [];
      snapshot.forEach((doc) => {
        templates.push({ id: doc.id, ...doc.data() } as Template);
      });
      setCustomTemplates(templates);
    } catch (error) {
      console.error('Fehler beim Laden der Vorlagen:', error);
    }
  };

  // KI-Vorlage generieren
  const generateTemplateWithKI = async () => {
    if (!newTemplateType.trim()) return;
    
    // Check query limit for non-lawyer users
    if (userTier !== 'lawyer' && queriesUsed >= queriesLimit) {
      alert('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für KI-Vorlagen.');
      setShowUpgradeModal(true);
      return;
    }
    
    setIsCreatingTemplate(true);
    
    try {
      const instructions = `Erstelle eine vollständige, professionelle Vorlage für: ${newTemplateType}. 
${newTemplateContext ? `Sachverhalt/Kontext: ${newTemplateContext}` : ''}
Erstelle ein rechtssicheres Dokument mit allen erforderlichen Elementen: Absender, Empfänger, Datum, Betreff, Anrede, Haupttext mit rechtlichen Punkten, Fristsetzung falls relevant, Grußformel und Unterschrift. Verwende [PLATZHALTER] für variable Daten.`;

      const response = await fetch(`${API_URL}/templates/fill`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          template_name: newTemplateType,
          template_content: '[VORLAGE]',
          instructions: instructions,
        }),
      });

      if (!response.ok) {
        throw new Error('Fehler bei der Vorlagen-Generierung');
      }

      const data = await response.json();
      setKiGeneratedContent(data.filled_content || '');
      setNewTemplateName(newTemplateType);
      
      // Increment query count for non-lawyer users
      if (currentUser && userTier !== 'lawyer') {
        await updateDoc(doc(db, 'users', currentUser.uid), {
          queriesUsed: increment(1)
        });
        setQueriesUsed(prev => prev + 1);
      }
    } catch (error) {
      console.error('Fehler:', error);
      alert('Fehler bei der KI-Generierung. Bitte versuchen Sie es erneut.');
    } finally {
      setIsCreatingTemplate(false);
    }
  };

  // Vorlage speichern
  const saveCustomTemplate = async () => {
    if (!currentUser || !kiGeneratedContent || !newTemplateName) return;
    
    try {
      const newTemplate: Omit<Template, 'id'> = {
        name: newTemplateName,
        category: 'Meine Vorlagen',
        description: `Erstellt am ${new Date().toLocaleDateString('de-DE')}`,
        icon: '📝',
        forRoles: [],
        content: kiGeneratedContent,
        isCustom: true,
        userId: currentUser.uid,
        createdAt: new Date().toISOString(),
      };
      
      const docRef = await addDoc(collection(db, 'custom_templates'), newTemplate);
      
      // Zur Liste hinzufügen
      setCustomTemplates(prev => [...prev, { id: docRef.id, ...newTemplate }]);
      
      // Modal schließen und zurücksetzen
      setShowCreateModal(false);
      setNewTemplateName('');
      setNewTemplateType('');
      setNewTemplateContext('');
      setKiGeneratedContent('');
      
      alert('Vorlage erfolgreich gespeichert!');
    } catch (error) {
      console.error('Fehler beim Speichern:', error);
      alert('Fehler beim Speichern der Vorlage.');
    }
  };

  // Vorlage löschen
  const deleteCustomTemplate = async (templateId: string) => {
    if (!confirm('Möchten Sie diese Vorlage wirklich löschen?')) return;
    
    try {
      await deleteDoc(doc(db, 'custom_templates', templateId));
      setCustomTemplates(prev => prev.filter(t => t.id !== templateId));
      if (selectedTemplate?.id === templateId) {
        setSelectedTemplate(null);
      }
    } catch (error) {
      console.error('Fehler beim Löschen:', error);
    }
  };

  // Vorlage aktualisieren (nach Bearbeitung)
  const updateCustomTemplate = async (templateId: string, newContent: string) => {
    try {
      await updateDoc(doc(db, 'custom_templates', templateId), {
        content: newContent,
        updatedAt: new Date().toISOString(),
      });
      setCustomTemplates(prev => prev.map(t => 
        t.id === templateId ? { ...t, content: newContent } : t
      ));
    } catch (error) {
      console.error('Fehler beim Aktualisieren:', error);
    }
  };

  // Determine which templates to show based on dashboard type
  const getAvailableTemplates = () => {
    if (!userData) return [];
    
    const dashboardType = userData.dashboardType || 'basis';
    const userTier = userData.tier || 'basis';
    
    // Lawyer sieht ALLE Vorlagen
    if (dashboardType === 'lawyer' || userTier === 'lawyer') {
      return [...TEMPLATES, ...customTemplates];
    }
    
    // Professional sieht: Investor, Verwalter, Vermieter, Eigentümer + eigene
    if (dashboardType === 'professional' || userTier === 'professional') {
      const allowedRoles = ['INVESTOR', 'VERWALTER', 'VERMIETER', 'EIGENTUEMER', 'MIETER'];
      const systemTemplates = TEMPLATES.filter(t => 
        t.forRoles && t.forRoles.some(role => allowedRoles.includes(role))
      );
      return [...systemTemplates, ...customTemplates];
    }
    
    // Basis sieht: Mieter, Eigentümer, Vermieter Vorlagen + eigene
    const basisRoles = ['MIETER', 'EIGENTUEMER', 'VERMIETER'];
    const systemTemplates = TEMPLATES.filter(t => 
      t.forRoles && t.forRoles.some(role => basisRoles.includes(role))
    );
    return [...systemTemplates, ...customTemplates];
  };

  // Kategorien dynamisch basierend auf Dashboard-Typ
  const getCategories = () => {
    if (!userData) return ['all'];
    
    const dashboardType = userData.dashboardType || 'basis';
    
    // Immer "Meine Vorlagen" anzeigen wenn vorhanden
    const hasCustom = customTemplates.length > 0;
    
    // Anwalt bekommt strukturierte Kategorien nach Dokumenttyp
    if (dashboardType === 'lawyer' || userData.tier === 'lawyer') {
      return [
        'all',
        ...(hasCustom ? ['Meine Vorlagen'] : []),
        'Musterbriefe',
        'Kündigungen & Mahnungen', 
        'Klagen & Schriftsätze',
        'Kaufverträge',
        'Grundbuchrecht',
        'Vertragsrecht',
        'Sonstiges'
      ];
    }
    
    // Basis & Professional bekommen Rollen-Kategorien + Meine Vorlagen
    const systemCategories = [...new Set(availableTemplates.filter(t => !t.isCustom).map(t => t.category))];
    return ['all', ...(hasCustom ? ['Meine Vorlagen'] : []), ...systemCategories];
  };

  const availableTemplates = getAvailableTemplates();
  const categories = getCategories();
  
  const filteredTemplates = selectedCategory === 'all' 
    ? availableTemplates 
    : availableTemplates.filter(t => t.category === selectedCategory);

  const copyToClipboard = (template: Template) => {
    navigator.clipboard.writeText(template.content);
    setCopiedId(template.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const downloadTemplate = (template: Template) => {
    const blob = new Blob([template.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${template.name.replace(/\s+/g, '_')}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Vorlage ins Dokumentenmanagement speichern
  const [savingToDocMgmt, setSavingToDocMgmt] = useState(false);
  const saveToDocumentManagement = async (template: Template) => {
    if (!currentUser) {
      alert('Bitte zuerst anmelden');
      return;
    }
    
    setSavingToDocMgmt(true);
    try {
      const docId = await saveTemplateAsMuster(
        currentUser.uid,
        template.name,
        editedContent || template.content
      );
      console.log('Document saved with ID:', docId);
      alert('✅ Vorlage wurde im Dokumentenmanagement gespeichert!');
    } catch (error: any) {
      console.error('Error saving to document management:', error);
      console.error('Error details:', error?.code, error?.message);
      alert(`Fehler beim Speichern: ${error?.message || 'Unbekannter Fehler'}`);
    } finally {
      setSavingToDocMgmt(false);
    }
  };

  const handleSaveFromEditor = (content: string) => {
    setEditedContent(content);
    setShowEditor(false);
    // Copy to clipboard automatically
    navigator.clipboard.writeText(content);
    setCopiedId(selectedTemplate?.id || null);
    setTimeout(() => setCopiedId(null), 3000);
  };

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Create Template Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-[#1e3a5f]">✨ Neue Vorlage mit KI erstellen</h2>
                <button onClick={() => {
                  setShowCreateModal(false);
                  setKiGeneratedContent('');
                  setNewTemplateName('');
                  setNewTemplateType('');
                  setNewTemplateContext('');
                }} className="text-gray-400 hover:text-gray-600 text-2xl">×</button>
              </div>
            </div>
            
            <div className="p-6 space-y-4">
              {!kiGeneratedContent ? (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Dokumenttyp *</label>
                    <select
                      value={newTemplateType}
                      onChange={(e) => setNewTemplateType(e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                    >
                      <option value="">-- Bitte wählen --</option>
                      <option value="Mahnung">Mahnung</option>
                      <option value="Fristsetzung">Fristsetzung</option>
                      <option value="Klageschrift">Klageschrift</option>
                      <option value="Stellungnahme">Stellungnahme</option>
                      <option value="Vergleichsvorschlag">Vergleichsvorschlag</option>
                      <option value="Widerspruch">Widerspruch</option>
                      <option value="Kündigung">Kündigung</option>
                      <option value="Abmahnung">Abmahnung</option>
                      <option value="Mietminderung">Mietminderungsankündigung</option>
                      <option value="Mängelanzeige">Mängelanzeige</option>
                      <option value="Nebenkostenwiderspruch">Nebenkostenwiderspruch</option>
                      <option value="Räumungsaufforderung">Räumungsaufforderung</option>
                      <option value="Sonstiges">Sonstiges Dokument</option>
                    </select>
                  </div>
                  
                  {newTemplateType === 'Sonstiges' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Dokumentbezeichnung</label>
                      <input
                        type="text"
                        value={newTemplateName}
                        onChange={(e) => setNewTemplateName(e.target.value)}
                        placeholder="z.B. Antrag auf Fristverlängerung"
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                      />
                    </div>
                  )}
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Kontext / Sachverhalt (optional)</label>
                    <textarea
                      value={newTemplateContext}
                      onChange={(e) => setNewTemplateContext(e.target.value)}
                      rows={5}
                      placeholder="Beschreiben Sie den Sachverhalt oder die Situation, für die das Dokument erstellt werden soll..."
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                    />
                  </div>
                  
                  <button
                    onClick={() => {
                      if (!hasAccess) {
                        setShowUpgradeModal(true);
                        return;
                      }
                      generateTemplateWithKI();
                    }}
                    disabled={!newTemplateType || isCreatingTemplate}
                    className={`w-full py-4 rounded-lg font-bold flex items-center justify-center gap-2 ${hasAccess ? 'bg-[#1e3a5f] text-white hover:bg-[#2d4a6f]' : 'bg-gray-300 text-gray-500 cursor-not-allowed'} disabled:opacity-50 disabled:cursor-not-allowed`}
                  >
                    {isCreatingTemplate ? (
                      <>
                        <span className="animate-spin">🔄</span> KI generiert Vorlage...
                      </>
                    ) : (
                      <>
                        {hasAccess ? '🤖 Vorlage mit KI generieren' : '🔒 Vorlage mit KI generieren (Basis-Tarif erforderlich)'}
                      </>
                    )}
                  </button>
                </>
              ) : (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Vorlagenname</label>
                    <input
                      type="text"
                      value={newTemplateName}
                      onChange={(e) => setNewTemplateName(e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Generierte Vorlage (bearbeitbar)</label>
                    <textarea
                      value={kiGeneratedContent}
                      onChange={(e) => setKiGeneratedContent(e.target.value)}
                      rows={15}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] font-mono text-sm"
                    />
                  </div>
                  
                  <div className="flex gap-3">
                    <button
                      onClick={() => setKiGeneratedContent('')}
                      className="flex-1 py-3 border border-gray-300 rounded-lg font-medium hover:bg-gray-50"
                    >
                      ↩️ Neu generieren
                    </button>
                    <button
                      onClick={saveCustomTemplate}
                      className="flex-1 py-3 bg-green-600 text-white rounded-lg font-bold hover:bg-green-700"
                    >
                      💾 Als Vorlage speichern
                    </button>
                  </div>
                  
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(kiGeneratedContent);
                      alert('In die Zwischenablage kopiert!');
                    }}
                    className="w-full py-3 bg-[#b8860b] text-white rounded-lg font-medium hover:bg-[#9a7209]"
                  >
                    📋 Nur kopieren (nicht speichern)
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* KI Editor Modal */}
      {showEditor && selectedTemplate && (
        <TemplateEditor
          template={{
            id: selectedTemplate.id,
            name: selectedTemplate.name,
            content: editedContent || selectedTemplate.content,
          }}
          onClose={() => setShowEditor(false)}
          onSave={(content) => {
            handleSaveFromEditor(content);
            // Falls es eine custom Vorlage ist, auch in Firebase speichern
            if (selectedTemplate.isCustom) {
              updateCustomTemplate(selectedTemplate.id, content);
            }
          }}
          userTier={userData?.tier}
          queriesRemaining={queriesLimit - queriesUsed}
          onQueryUsed={async () => {
            if (currentUser && userTier !== 'lawyer') {
              await updateDoc(doc(db, 'users', currentUser.uid), {
                queriesUsed: increment(1)
              });
              setQueriesUsed(prev => prev + 1);
            }
          }}
        />
      )}

      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-[106px]">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">
                ← Dashboard
              </Link>
              <Logo size="sm" />
            </div>
            <h1 className="text-lg font-semibold text-[#1e3a5f]">Musterbriefe & Vorlagen</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-[#1e3a5f]">Musterbriefe & Vorlagen</h1>
            <p className="text-gray-600 mt-2">Rechtssichere Vorlagen für Ihre Korrespondenz</p>
          </div>
          <div className="flex items-center gap-4">
            {/* Kontingent-Anzeige für Basis und Profi */}
            {userTier && userTier !== 'lawyer' && (
              <div className="px-4 py-2 bg-[#1e3a5f] text-white rounded-lg text-sm font-medium">
                {Math.max(0, queriesLimit - queriesUsed)} von {queriesLimit} Anfragen übrig
              </div>
            )}
            <button
              onClick={() => requireTier(() => setShowCreateModal(true))}
              className="px-6 py-3 bg-[#1e3a5f] text-white rounded-lg font-bold hover:bg-[#2d4a6f] flex items-center gap-2"
            >
              ✨ Neue Vorlage erstellen
            </button>
          </div>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === cat
                  ? 'bg-[#1e3a5f] text-white'
                  : 'bg-white border border-gray-200 text-gray-700 hover:border-[#1e3a5f]'
              }`}
            >
              {cat === 'all' ? 'Alle' : cat}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Template List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm divide-y divide-gray-100 max-h-[700px] overflow-y-auto">
              {filteredTemplates.map((template) => (
                <div
                  key={template.id}
                  className={`relative p-4 hover:bg-gray-50 transition-colors cursor-pointer ${
                    selectedTemplate?.id === template.id ? 'bg-[#1e3a5f]/5 border-l-4 border-[#1e3a5f]' : ''
                  }`}
                  onClick={() => setSelectedTemplate(template)}
                >
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">{template.icon}</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-[#1e3a5f]">{template.name}</p>
                        {template.isCustom && (
                          <span className="px-2 py-0.5 bg-purple-100 text-purple-700 text-xs rounded-full">Eigene</span>
                        )}
                      </div>
                      <p className="text-xs text-[#b8860b]">{template.category}</p>
                      <p className="text-sm text-gray-500 mt-1">{template.description}</p>
                    </div>
                    {template.isCustom && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteCustomTemplate(template.id);
                        }}
                        className="p-1 text-red-400 hover:text-red-600 hover:bg-red-50 rounded"
                        title="Vorlage löschen"
                      >
                        🗑️
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Template Preview */}
          <div className="lg:col-span-2">
            {selectedTemplate ? (
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
                <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{selectedTemplate.icon}</span>
                    <div>
                      <h2 className="font-semibold text-[#1e3a5f]">{selectedTemplate.name}</h2>
                      <p className="text-sm text-gray-500">{selectedTemplate.category}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        if (!hasAccess) {
                          setShowUpgradeModal(true);
                          return;
                        }
                        setEditedContent(null);
                        setShowEditor(true);
                      }}
                      className={`px-4 py-2 text-sm rounded-lg font-medium ${hasAccess ? 'bg-[#1e3a5f] text-white hover:bg-[#2d4a6f]' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
                    >
                      {hasAccess ? '🤖 Mit KI anpassen' : '🔒 Mit KI anpassen'}
                    </button>
                    <button
                      onClick={() => {
                        if (!hasAccess) {
                          setShowUpgradeModal(true);
                          return;
                        }
                        copyToClipboard(selectedTemplate);
                      }}
                      className={`px-4 py-2 text-sm rounded-lg transition-colors ${
                        copiedId === selectedTemplate.id
                          ? 'bg-green-500 text-white'
                          : hasAccess 
                            ? 'border border-gray-300 hover:bg-gray-50' 
                            : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      }`}
                    >
                      {copiedId === selectedTemplate.id ? '✓ Kopiert!' : (hasAccess ? '📋 Kopieren' : '🔒 Kopieren')}
                    </button>
                    <button
                      onClick={() => {
                        if (!hasAccess) {
                          setShowUpgradeModal(true);
                          return;
                        }
                        downloadTemplate(selectedTemplate);
                      }}
                      className={`px-4 py-2 text-sm rounded-lg ${hasAccess ? 'border border-gray-300 hover:bg-gray-50' : 'bg-gray-200 text-gray-500 cursor-not-allowed'}`}
                    >
                      {hasAccess ? '⬇️ Download' : '🔒 Download'}
                    </button>
                    <button
                      onClick={() => requireTier(() => saveToDocumentManagement(selectedTemplate))}
                      disabled={savingToDocMgmt}
                      className="px-4 py-2 text-sm border border-blue-300 text-blue-600 rounded-lg hover:bg-blue-50 disabled:opacity-50"
                    >
                      {savingToDocMgmt ? '⏳...' : '📁 Speichern'}
                    </button>
                  </div>
                </div>
                <div className="p-6">
                  <pre className="whitespace-pre-wrap font-mono text-sm text-gray-700 bg-gray-50 p-4 rounded-lg max-h-[500px] overflow-y-auto">
                    {editedContent || selectedTemplate.content}
                  </pre>
                </div>
                <div className="p-4 border-t border-gray-100 bg-gradient-to-r from-blue-50 to-amber-50">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-700">
                      🤖 <strong>NEU:</strong> Lassen Sie die KI diese Vorlage mit Ihren Daten ausfüllen!
                    </p>
                    <button
                      onClick={() => {
                        if (!hasAccess) {
                          setShowUpgradeModal(true);
                          return;
                        }
                        setEditedContent(null);
                        setShowEditor(true);
                      }}
                      className={`px-4 py-2 text-sm rounded-lg ${hasAccess ? 'bg-[#b8860b] text-white hover:bg-[#9a7209]' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
                    >
                      {hasAccess ? 'Jetzt anpassen →' : '🔒 Upgrade erforderlich'}
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
                <p className="text-6xl mb-4">✉️</p>
                <p className="text-lg text-gray-600">Wählen Sie eine Vorlage aus der Liste</p>
                <p className="text-sm text-gray-500 mt-2">
                  Alle Vorlagen sind rechtssicher formuliert
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="lawyer"
        feature="Neue Vorlagen erstellen"
      />
    </div>
  );
}

export default function TemplatesPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">⚙️</div>
          <p className="text-gray-600">Vorlagen werden geladen...</p>
        </div>
      </div>
    }>
      <TemplatesContent />
    </Suspense>
  );
}
