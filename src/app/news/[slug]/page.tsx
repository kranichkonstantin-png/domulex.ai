import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';
import Image from 'next/image';
import { Metadata } from 'next';
import { marked } from 'marked';

// Configure marked for proper rendering
marked.setOptions({
  breaks: true,
  gfm: true,
});

// Artikel-Datenbank (später aus CMS/Firestore)
const articles: Record<string, {
  id: number;
  title: string;
  excerpt: string;
  content: string;
  author: string;
  authorRole: string;
  authorBio: string;
  publishedAt: string;
  modifiedAt?: string;
  category: string;
  readTime: string;
  tags: string[];
  image?: string;
}> = {
  'co2-kostenaufteilung-abrechnung-2026-107': {
    id: 107,
    title: 'Abrechnungs-Falle 2026: CO2-Kostenaufteilung korrekt berechnen',
    excerpt: 'Ab Januar 2026 drohen Vermietern bei der Nebenkostenabrechnung Fehlerquellen durch das CO2-Stufenmodell. Jurist K. Kranich erklärt die Risiken und Lösungen.',
    content: `
## Abrechnungs-Falle 2026: Warum Vermieter bei der CO2-Abgabe jetzt umdenken müssen

*Wunstorf, 02. Januar 2026* – Mit dem Jahreswechsel beginnt für Hausverwalter und private Vermieter die heiße Phase der Nebenkostenabrechnungen für das vergangene Jahr. Doch Vorsicht: Wer 2026 noch auf alte Excel-Vorlagen setzt, riskiert formelle Fehler. Das Kohlendioxidkostenaufteilungsgesetz (CO2KostAufG) hat die Spielregeln dauerhaft verändert – und die Schonfrist ist vorbei.

### Das Ende der "Durchreich-Mentalität"

Jahrelang galt im deutschen Mietrecht der Grundsatz: "Wer verbraucht, der zahlt." Die CO2-Preis-Komponente auf Öl und Gas konnte vom Vermieter zu 100 Prozent auf den Mieter umgelegt werden. Diese Zeiten sind vorbei.

> Das sogenannte Stufenmodell zwingt Vermieter dazu, die energetische Qualität ihres Gebäudes in die Abrechnung einzupreisen. Je schlechter die Dämmung und die Heizungsanlage, desto höher ist der Anteil, den der Vermieter an den CO2-Kosten selbst tragen muss.
>
> – Konstantin Kranich, Jurist und Gründer von domulex.ai

In der Praxis bedeutet das: Die Zeiten, in denen man einfach die Endsumme der Gasrechnung durch die Quadratmeter teilte, sind vorbei. Vermieter müssen nun aktiv den **spezifischen Kohlendioxidausstoß** der Immobilie ermitteln (in kg CO2 pro Quadratmeter Wohnfläche) und diesen Wert in eine von zehn gesetzlichen Stufen einordnen.

### Fehlerquelle Nr. 1: Die Datenübernahme

Das größte Risiko in der Abrechnungsperiode 2026 liegt in der Datenbasis. Zwar sind Energieversorger verpflichtet, die notwendigen Daten (Emissionsmenge, CO2-Kosten) auf ihren Rechnungen auszuweisen, doch die Übertragung in die Mietabrechnung ist fehleranfällig.

Wir sehen in der Praxis oft zwei Fehler:

1. **Falsche Einstufung**: Die Einordnung in das Stufenmodell wird falsch berechnet oder schlichtweg vergessen
2. **Fehlende Differenzierung**: Bei gemischt genutzten Gebäuden (Gewerbe und Wohnen) wird die vorgeschriebene Differenzierung nicht sauber durchgeführt

### Das Risiko: Pauschale Kürzung durch den Mieter

Der Gesetzgeber hat dem CO2KostAufG scharfe Zähne verliehen. Ignoriert ein Vermieter die Aufteilungspflichten oder weist er die CO2-Kostenanteile nicht transparent aus, greift eine Sanktionsklausel.

Gemäß **§ 7 CO2KostAufG** hat der Mieter in solchen Fällen das Recht, seinen Anteil an den Heizkosten pauschal um **3 Prozent zu kürzen**.

> Bei großen Beständen summieren sich diese 3 Prozent schnell zu empfindlichen Beträgen. Noch gefährlicher ist jedoch das Risiko, dass die gesamte Abrechnung aufgrund formeller Mängel als unwirksam angegriffen wird. Dann droht im schlimmsten Fall der vollständige Ausfall der Nachzahlung.

### Das CO2-Stufenmodell im Überblick

| Stufe | CO2-Ausstoß (kg/m²/Jahr) | Mieter-Anteil | Vermieter-Anteil |
|-------|--------------------------|---------------|------------------|
| 1 | < 12 | 100% | 0% |
| 2 | 12 – 17 | 90% | 10% |
| 3 | 17 – 22 | 80% | 20% |
| 4 | 22 – 27 | 70% | 30% |
| 5 | 27 – 32 | 60% | 40% |
| 6 | 32 – 37 | 50% | 50% |
| 7 | 37 – 42 | 40% | 60% |
| 8 | 42 – 47 | 30% | 70% |
| 9 | 47 – 52 | 20% | 80% |
| 10 | > 52 | 5% | 95% |

### Technologie als Compliance-Hebel

Angesichts der Komplexität rät der Experte von manuellen Berechnungen ab. Die Fehlerquote bei händischer Übertragung in Tabellenkalkulationen ist unverhältnismäßig hoch.

Die Lösung liegt in der **Automatisierung**. Moderne Kanzlei- und Verwaltungssoftware prüft die Eingaben mittlerweile in Echtzeit auf Plausibilität. Bei domulex.ai haben wir beispielsweise Algorithmen integriert, die die CO2-Werte automatisch gegen die aktuellen gesetzlichen Tabellen abgleichen.

Der Vorteil der KI-gestützten Prüfung: Das System erkennt, ob die eingegebenen Werte (Verbrauch vs. Kosten) logisch konsistent sind und warnt den Verwalter, **bevor** die fehlerhafte Abrechnung im Briefkasten des Mieters landet.

### Fazit: Sorgfalt vor Schnelligkeit

Für das Jahr 2026 gilt: Die korrekte Anwendung der neuen Gesetze ist wichtiger als die schnelle Erledigung. Vermieter und Verwalter sollten ihre Prozesse jetzt digitalisieren, um rechtssicher zu agieren. Wer sich auf veraltete Muster verlässt, zahlt am Ende drauf.

### Rechtsquellen & weiterführende Links

- [CO2KostAufG - Volltext](https://www.gesetze-im-internet.de/co2kostaufg/)
- [§ 7 CO2KostAufG - Kürzungsrecht](https://www.gesetze-im-internet.de/co2kostaufg/__7.html)
- [CO2KostAufG - Stufenmodell (Anlage)](https://www.gesetze-im-internet.de/co2kostaufg/anlage.html)
- [HeizKV - Heizkostenverordnung](https://www.gesetze-im-internet.de/heizkostenv/)

---

*Hinweis: Dieser Artikel dient der allgemeinen Information und ersetzt keine individuelle Rechtsberatung.*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer des Legal-Tech-Unternehmens domulex.ai. Er spezialisiert sich auf die Digitalisierung juristischer Prozesse im Immobilienrecht und entwickelt KI-Lösungen, die Anwälten, Verwaltern und Investoren helfen, rechtssicher und effizient zu arbeiten.',
    publishedAt: '2026-01-02T08:00:00+01:00',
    category: 'Nebenkosten',
    readTime: '5 Min.',
    tags: ['CO2-Kostenaufteilung', 'CO2KostAufG', 'Nebenkostenabrechnung', 'Vermieter', 'Heizkosten', 'Stufenmodell'],
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/co2-kostenaufteilung.jpeg?alt=media&token=1a530624-7807-40e1-9a21-0de5ce96daec'
  },
  'heizungsgesetz-2026-was-vermieter-wissen-muessen-101': {
    id: 101,
    title: 'Heizungsgesetz 2026: Was Vermieter jetzt wissen müssen',
    excerpt: 'Das neue Gebäudeenergiegesetz (GEG) tritt in verschärfter Form in Kraft. Wir analysieren die wichtigsten Änderungen für Immobilienbesitzer und Vermieter.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/heizungsgesetz_2026.jpeg?alt=media&token=9c0eb525-5fe8-4dbb-9250-323228da2d33',
    content: `
## Die wichtigsten Änderungen im Überblick

Mit dem 1. Januar 2026 treten wesentliche Verschärfungen des Gebäudeenergiegesetzes (GEG) in Kraft. Diese Änderungen betreffen insbesondere Vermieter und Immobilieneigentümer, die in den kommenden Jahren Heizungsanlagen austauschen müssen.

### 1. Neue Fristen für den Heizungstausch

Für bestehende Gasheizungen gelten nun verbindliche Austauschfristen:

- **Gebäude mit mehr als 6 Wohneinheiten**: Austausch bis spätestens 2030
- **Gebäude mit 2-6 Wohneinheiten**: Austausch bis spätestens 2032  
- **Einfamilienhäuser**: Austausch bis spätestens 2034

### 2. Erhöhte Förderungen

Die Bundesregierung hat die Fördersätze für den Umstieg auf klimafreundliche Heizungen angepasst:

| Heizungsart | Grundförderung | Mit Klima-Bonus |
|-------------|----------------|-----------------|
| Wärmepumpe | 30% | 45% |
| Pelletheizung | 20% | 35% |
| Fernwärme | 30% | 40% |

### 3. Umlage auf Mieter

Vermieter können die Modernisierungskosten unter bestimmten Voraussetzungen auf die Miete umlegen. Die Umlagefähigkeit ist jedoch begrenzt:

- Maximal 8% der aufgewendeten Kosten pro Jahr
- Modernisierungsmieterhöhung darf 2 €/m² innerhalb von 6 Jahren nicht überschreiten
- Bei Inanspruchnahme von Fördermitteln: Kürzung der umlagefähigen Kosten

### Rechtliche Einordnung

Nach § 559 BGB können Vermieter bei Modernisierungsmaßnahmen die jährliche Miete um 8% der aufgewendeten Kosten erhöhen. Die neuen Regelungen des GEG 2026 schaffen jedoch zusätzliche Pflichten:

> "Der Gebäudeeigentümer hat sicherzustellen, dass bei einem Heizungsaustausch die neue Heizungsanlage mindestens 65% der Wärme aus erneuerbaren Energien bezieht." – § 71 GEG n.F.

### Handlungsempfehlung für Vermieter

1. **Bestandsaufnahme**: Prüfen Sie das Alter und den Zustand Ihrer Heizungsanlagen
2. **Fristen beachten**: Planen Sie den Austausch rechtzeitig vor Ablauf der gesetzlichen Fristen
3. **Förderung beantragen**: Die erhöhten Fördersätze gelten nur bei Antragstellung vor Beginn der Maßnahme
4. **Mieter informieren**: Modernisierungsankündigung mindestens 3 Monate vor Beginn

### Fazit

Das neue Heizungsgesetz stellt Vermieter vor erhebliche Investitionen, bietet aber durch die erhöhten Fördersätze auch Chancen. Eine frühzeitige Planung ist unerlässlich, um die Fristen einzuhalten und von den Förderungen zu profitieren.

### Rechtsquellen & weiterführende Links

- [GEG - Gebäudeenergiegesetz Volltext](https://www.gesetze-im-internet.de/geg/)
- [§ 71 GEG - Anforderungen an Heizungsanlagen](https://www.gesetze-im-internet.de/geg/__71.html)
- [§ 559 BGB - Mieterhöhung nach Modernisierung](https://www.gesetze-im-internet.de/bgb/__559.html)
- [BAFA - Bundesförderung effiziente Gebäude](https://www.bafa.de/DE/Energie/Effiziente_Gebaeude/effiziente_gebaeude_node.html)
- [KfW - Heizungsförderung](https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/Energieeffizient-sanieren/)

---

*Dieser Artikel stellt keine Rechtsberatung dar. Für individuelle Fragen konsultieren Sie bitte einen Fachanwalt.*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer von domulex.ai.',
    publishedAt: '2026-01-02T10:00:00+01:00',
    category: 'Gesetzgebung',
    readTime: '6 Min.',
    tags: ['Heizungsgesetz', 'GEG', 'Vermieter', 'Modernisierung', 'Förderung']
  },
  'bgh-urteil-indexmiete-januar-2026-102': {
    id: 102,
    title: 'BGH-Urteil zur Indexmiete: Neue Grenzen für Mieterhöhungen',
    excerpt: 'Der Bundesgerichtshof hat in einem wegweisenden Urteil die Grenzen von Indexmietverträgen konkretisiert. Das bedeutet das Urteil für Vermieter und Mieter.',
    content: `
## BGH konkretisiert Grenzen der Indexmiete

Der Bundesgerichtshof hat mit Urteil vom 15. Dezember 2025 (Az. VIII ZR 234/24) wichtige Klarstellungen zur Zulässigkeit und den Grenzen von Indexmietvereinbarungen getroffen.

### Der Fall

Die Klägerin, eine Mieterin aus München, wehrte sich gegen eine Indexmieterhöhung von 18,3% binnen zwei Jahren. Der Vermieter hatte die Miete entsprechend dem Verbraucherpreisindex angepasst, was in Zeiten hoher Inflation zu erheblichen Steigerungen führte.

### Die Entscheidung des BGH

Der BGH entschied, dass Indexmietvereinbarungen grundsätzlich wirksam sind, jedoch bestimmten Grenzen unterliegen:

> "Eine Indexmiete, die innerhalb eines Zeitraums von zwei Jahren zu einer Mieterhöhung von mehr als 20% führt, kann im Einzelfall gegen § 138 BGB verstoßen, wenn der Mieter dadurch unangemessen benachteiligt wird."

### Kernaussagen des Urteils

1. **Grundsätzliche Wirksamkeit**: Indexmietvereinbarungen nach § 557b BGB bleiben zulässig
2. **Kappungsgrenze analog**: In Extremfällen kann die Kappungsgrenze des § 558 Abs. 3 BGB analog herangezogen werden
3. **Einzelfallprüfung**: Bei Mieterhöhungen über 15% binnen 3 Jahren ist eine Einzelfallprüfung erforderlich
4. **Härtefallregelung**: Mieter können sich auf § 574 BGB berufen

### Auswirkungen für die Praxis

#### Für Vermieter:
- Indexmieterhöhungen sollten in moderaten Schritten erfolgen
- Bei Erhöhungen über 15%: Dokumentation der Angemessenheit empfohlen
- Kommunikation mit Mietern vor drastischen Erhöhungen ratsam

#### Für Mieter:
- Bei extremen Steigerungen: Rechtsberatung einholen
- Härtefalleinwände prüfen
- Verhandlungsbereitschaft des Vermieters ausloten

### Rechtliche Einordnung

Das Urteil reiht sich in eine Entwicklung der Rechtsprechung ein, die übermäßige Mietbelastungen begrenzt. Bereits in früheren Entscheidungen hatte der BGH betont, dass auch vertraglich vereinbarte Anpassungsmechanismen den Grenzen von Treu und Glauben unterliegen.

### Handlungsempfehlung

Vermieter sollten bei bestehenden Indexmietverträgen prüfen, ob geplante Erhöhungen im Rahmen des vom BGH gebilligten bleiben. Eine schrittweise Anpassung kann rechtssicherer sein als eine einmalige hohe Erhöhung.

### Rechtsquellen & weiterführende Links

- [§ 557b BGB - Indexmiete](https://www.gesetze-im-internet.de/bgb/__557b.html)
- [§ 558 BGB - Mieterhöhung bis zur ortsüblichen Vergleichsmiete](https://www.gesetze-im-internet.de/bgb/__558.html)
- [§ 574 BGB - Widerspruch des Mieters](https://www.gesetze-im-internet.de/bgb/__574.html)
- [BGH-Rechtsprechung Mietrecht](https://www.bundesgerichtshof.de/DE/Entscheidungen/entscheidungen_node.html)
- [Statistisches Bundesamt - Verbraucherpreisindex](https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Verbraucherpreisindex/_inhalt.html)

---

*Aktenzeichen: BGH VIII ZR 234/24, Urteil vom 15. Dezember 2025*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer von domulex.ai.',
    publishedAt: '2026-01-01T09:00:00+01:00',
    category: 'Rechtsprechung',
    readTime: '5 Min.',
    tags: ['BGH', 'Indexmiete', 'Mieterhöhung', 'Urteil', 'Mietrecht'],
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/bgh_indexmiete.jpeg?alt=media&token=136dbf60-03a6-489d-b24f-7be2e46ad10f'
  },
  'grundsteuer-reform-2026-berechnung-103': {
    id: 103,
    title: 'Grundsteuer-Reform 2026: So berechnen Sie die neue Belastung',
    excerpt: 'Die Grundsteuer-Reform ist in Kraft. Wir erklären Schritt für Schritt, wie Sie Ihre neue Grundsteuer berechnen und welche Einspruchsmöglichkeiten bestehen.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/grundsteuerreform%202026.jpeg?alt=media&token=22f07396-c79d-4231-8302-6ef236b7244c',
    content: `
## Die neue Grundsteuer ab 2026

Seit dem 1. Januar 2025 gilt die neue Grundsteuer. Viele Eigentümer haben erstmals Bescheide nach dem neuen Recht erhalten. Wir erklären, wie die Berechnung funktioniert und was Sie tun können, wenn der Bescheid fehlerhaft ist.

### So berechnet sich die neue Grundsteuer

Die Grundsteuer berechnet sich nach folgender Formel:

**Grundsteuerwert × Steuermesszahl × Hebesatz = Grundsteuer**

#### 1. Der Grundsteuerwert

Das Finanzamt ermittelt den Grundsteuerwert Ihres Grundstücks. Dabei werden berücksichtigt:
- Bodenrichtwert
- Grundstücksfläche
- Gebäudeart und Nutzung
- Wohnfläche
- Baujahr

#### 2. Die Steuermesszahl

Die Steuermesszahl beträgt:
- **Wohngrundstücke**: 0,31 ‰
- **Gewerbegrundstücke**: 0,34 ‰

#### 3. Der Hebesatz

Den Hebesatz legt jede Gemeinde selbst fest. Er variiert stark:
- Ländliche Gebiete: oft 300-400%
- Städte: meist 400-600%
- Großstädte: teilweise über 800%

### Beispielrechnung

Ein Einfamilienhaus in Frankfurt am Main:
- Grundsteuerwert: 250.000 €
- Steuermesszahl: 0,31 ‰ = 0,00031
- Hebesatz Frankfurt: 500%

**Rechnung:** 250.000 € × 0,00031 × 500% = **387,50 € pro Jahr**

### Einspruch gegen den Grundsteuerbescheid

Sie haben mehrere Möglichkeiten:

1. **Einspruch gegen den Grundsteuerwertbescheid** (Finanzamt)
   - Frist: 1 Monat nach Bekanntgabe
   - Wichtig: Hier werden die Grundlagen festgelegt

2. **Widerspruch gegen den Grundsteuerbescheid** (Gemeinde)
   - Nur sinnvoll bei Rechenfehlern
   - Nicht bei Streit über den Grundsteuerwert

### Häufige Fehler in Bescheiden

- Falsche Wohnfläche
- Falsches Baujahr
- Fehlerhafte Bodenrichtwerte
- Nicht berücksichtigte Abschläge

### Umlegung auf Mieter

Die Grundsteuer kann weiterhin als Betriebskosten auf Mieter umgelegt werden (§ 2 Nr. 1 BetrKV). Allerdings:

- Nur tatsächlich gezahlte Beträge
- Bei Nebenkosten-Vorauszahlungen: Anpassung erforderlich
- Jahresabrechnung muss die neue Grundsteuer ausweisen

### Rechtsquellen & weiterführende Links

- [Grundsteuergesetz (GrStG)](https://www.gesetze-im-internet.de/grstg_1973/)
- [Bewertungsgesetz (BewG)](https://www.gesetze-im-internet.de/bewg/)
- [§ 2 Nr. 1 BetrKV - Umlagefähigkeit](https://www.gesetze-im-internet.de/betrkv/__2.html)
- [Grundsteuer-Reform Portal](https://www.grundsteuerreform.de/)
- [BORIS - Bodenrichtwerte](https://www.boris.nrw.de/)

---

*Stand: Januar 2026. Regionale Unterschiede möglich.*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer von domulex.ai.',
    publishedAt: '2025-12-28T14:00:00+01:00',
    category: 'Steuern',
    readTime: '8 Min.',
    tags: ['Grundsteuer', 'Reform', 'Berechnung', 'Einspruch', 'Betriebskosten']
  },
  'mietpreisbremse-verlaengerung-2026-104': {
    id: 104,
    title: 'Mietpreisbremse bis 2029 verlängert: Das neue Gesetz im Überblick',
    excerpt: 'Der Bundestag hat am 26. Juni 2025 die Verlängerung der Mietpreisbremse bis Ende 2029 beschlossen. Wir erklären die Hintergründe und was das für Mieter und Vermieter bedeutet.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/mietpreisbremse_2028.jpeg?alt=media&token=3e895b61-03f0-47a4-be56-2a40391909ba',
    content: `
## Mietpreisbremse: Verlängerung bis Ende 2029

Der Bundestag hat am **26. Juni 2025** die Mietpreisbremse nach **§ 556d BGB** bis zum **31. Dezember 2029** verlängert. Ursprünglich sollte die Regelung Ende 2025 auslaufen.

Für den Gesetzentwurf der Koalitionsfraktionen CDU/CSU und SPD (Drucksache 21/322) stimmten auch die Grünen. Die AfD stimmte dagegen, Die Linke enthielt sich.

### Begründung der Verlängerung

Im Gesetz wird die Verlängerung mit den **weiter stark ansteigenden Wiedervermietungsmieten** in Ballungszentren begründet. Ein Auslaufen der Mietpreisbremse hätte laut Gesetzentwurf:

- zu einem Anstieg der Wiedervermietungsmieten geführt
- Menschen mit niedrigem Einkommen aus ihren Wohnvierteln verdrängt
- Familien mit Kindern besonders betroffen

### Rechtsgrundlagen

Die Mietpreisbremse ist geregelt in:
- **§ 556d BGB** - Zulässige Miethöhe bei Mietbeginn
- **§ 556e BGB** - Berücksichtigung der Vormiete
- **§ 556f BGB** - Ausnahmen (Neubau, umfassende Modernisierung)
- **§ 556g BGB** - Rechtsfolgen bei Verstoß

> **Gesetzestext § 556d Abs. 1 BGB:**  
> "Wird ein Mietvertrag über Wohnraum abgeschlossen, der in einem durch Rechtsverordnung nach Absatz 2 bestimmten Gebiet mit einem angespannten Wohnungsmarkt liegt, so darf die Miete zu Beginn des Mietverhältnisses die ortsübliche Vergleichsmiete höchstens um 10 Prozent übersteigen."

### Stimmen aus dem Bundestag

**SPD (Sonja Eichwede):** Die Verlängerung sei ein "erster Schritt". Weitere Regelungen brauche es bei Kurzzeitvermietung, Indexmietverträgen und möbliertem Wohnraum. Eine Expertengruppe soll bis Ende 2026 weitere Vorschläge zum Mietrecht vorlegen.

**CDU/CSU (Prof. Dr. Günter Krings):** Die Mietpreisbremse sei keine Dauerlösung. Das eigentliche Problem löse man durch Neubau, nicht durch Preisregulierung. Die Neubau-Ausnahme (ab Oktober 2014) bleibe bestehen, da sonst das Vertrauen von Investoren gefährdet werde.

**Grüne (Dr. Till Steffen):** Die Verlängerung sei besser als nichts, wirksamer Schutz biete aber nur das von den Grünen vorgeschlagene "Faire-Mieten-Gesetz".

**Die Linke (Caren Lay):** Die Mietpreisbremse "bremse nicht" - die Mieten seien seit Einführung in Großstädten um 50%, in Berlin um 100% gestiegen.

### Ausnahmen bleiben bestehen

Nach **§ 556f BGB** gilt die Mietpreisbremse weiterhin NICHT bei:

1. **Neubauten** - Erstmalige Nutzung nach dem 1. Oktober 2014
2. **Umfassend modernisierte Wohnungen** - Investition > 1/3 des Neubau-Preises
3. **Vormiete über der Grenze** - Wenn der Vormieter bereits mehr zahlte

Die Union setzte sich in den Verhandlungen durch: Eine Anpassung des Stichtags für die Neubau-Ausnahme wurde abgelehnt.

### Angespannte Wohnungsmärkte

Die Landesregierungen bestimmen per Rechtsverordnung, welche Gebiete als "angespannte Wohnungsmärkte" gelten. Ein Markt gilt als angespannt, wenn:

- die Mieten deutlich stärker steigen als im Bundesdurchschnitt
- die Mietbelastung der Haushalte den Durchschnitt deutlich übersteigt

### Abgelehnte Alternativen

Der Bundestag lehnte weitreichendere Vorschläge ab:

**Grünen-Gesetzentwurf "Faires-Mieten-Gesetz"** (Drucksache 21/222): Entfristung der Mietpreisbremse, Einschränkung bei möblierter Vermietung, Kappungsgrenze auf 9% in 3 Jahren, Betrachtungszeitraum für Vergleichsmiete auf 20 Jahre.

**Linken-Antrag** (Drucksache 21/355): Flächendeckende, entfristete Mietpreisbremse, Einfrieren von Bestandsmieten für 6 Jahre, Sanktionen bei Verstößen.

### Weiterführende Links

- [Gesetzestext § 556d BGB](https://www.gesetze-im-internet.de/bgb/__556d.html)
- [Bundestag: Mietpreisbremse bis 2029 verlängert](https://www.bundestag.de/dokumente/textarchiv/2025/kw26-de-mietpreisbremse-1084786)
- [Gesetzentwurf Drucksache 21/322](https://dserver.bundestag.de/btd/21/003/2100322.pdf)

---

*Stand: Januar 2026 | Quelle: Deutscher Bundestag*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer von domulex.ai.',
    publishedAt: '2025-12-20T10:00:00+01:00',
    category: 'Gesetzgebung',
    readTime: '5 Min.',
    tags: ['Mietpreisbremse', 'BGB', 'Mietrecht', 'Vermieter', 'Wohnungsmarkt', 'Bundestag']
  },
  'weg-reform-2026-digitale-eigentuemerversammlung-105': {
    id: 105,
    title: 'WEG-Reform 2026: Digitale Eigentümerversammlung wird Standard',
    excerpt: 'Das neue WEG-Änderungsgesetz erleichtert digitale Eigentümerversammlungen erheblich. Was das für Ihre WEG bedeutet.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/weg-reform_2026.jpeg?alt=media&token=e324ed34-25c1-459e-93d0-3456a272ae5c',
    content: `
## Digitale WEG-Versammlung: Die neuen Regeln

Mit der WEG-Reform 2020 wurden erste Grundlagen für Online-Versammlungen geschaffen. Ab 2026 gelten erweiterte Möglichkeiten durch das **WEG-Digitalisierungsgesetz**.

### Rechtsgrundlagen

Die Eigentümerversammlung ist geregelt in:
- **§ 23 WEG** - Wohnungseigentümerversammlung
- **§ 24 WEG** - Einberufung, Vorsitz, Niederschrift
- **§ 25 WEG** - Mehrheitsbeschluss

### Was hat sich geändert?

Die bisherige Regelung nach **§ 23 Abs. 1 WEG** erforderte für eine rein virtuelle Versammlung die Zustimmung aller Eigentümer. Das war praktisch kaum umsetzbar.

> **§ 23 Abs. 1a WEG (neu):**  
> "Die Wohnungseigentümer können durch Mehrheitsbeschluss festlegen, dass Eigentümerversammlungen auch als Hybridversammlung oder rein virtuell durchgeführt werden können."

### Hybridversammlung vs. rein virtuell

| Versammlungsform | Anforderung |
|------------------|-------------|
| Präsenz | Standard |
| Hybrid (Präsenz + Online) | Einfacher Mehrheitsbeschluss |
| Rein virtuell | 2/3-Mehrheit + erneuter Beschluss jährlich |

### Technische Anforderungen

Die Rechtsprechung hat folgende Mindestanforderungen entwickelt:
- Bild- und Tonübertragung in Echtzeit
- Möglichkeit zur Wortmeldung
- Sichere Identifizierung der Teilnehmer
- Geheime Abstimmung muss möglich sein

### BGH-Rechtsprechung zur WEG-Reform

- **BGH V ZR 176/20** (05.02.2021): Zur Anfechtung von Beschlüssen
- **BGH V ZR 225/21** (08.07.2022): Ladungsfehler bei WEG-Versammlungen
- **BGH V ZR 65/22** (10.11.2023): Beschlusskompetenz bei baulichen Veränderungen

### Muster: Beschluss zur Hybridversammlung

*"Die Wohnungseigentümer beschließen, dass künftige Eigentümerversammlungen auch in hybrider Form durchgeführt werden können. Eigentümer können per Videokonferenz teilnehmen und abstimmen."*

### Weiterführende Links

- [Gesetzestext WEG](https://www.gesetze-im-internet.de/woeigg/)
- [BGH-Rechtsprechung WEG](https://www.bundesgerichtshof.de)

---

*Stand: Januar 2026*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer von domulex.ai.',
    publishedAt: '2025-12-15T10:00:00+01:00',
    category: 'WEG-Recht',
    readTime: '5 Min.',
    tags: ['WEG', 'Eigentümerversammlung', 'Digital', 'Hybridversammlung', 'Reform']
  },
  'energieausweis-pflicht-2026-bussgelder-106': {
    id: 106,
    title: 'Energieausweis-Pflicht 2026: Höhere Bußgelder bei Verstößen',
    excerpt: 'Ab Januar 2026 gelten verschärfte Regeln für Energieausweise. Bei Verstößen drohen nun Bußgelder bis zu 15.000 Euro.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/energieausweis_bussgeld.jpeg?alt=media&token=d65b73e0-5d31-4bb5-917f-b2c8b7c8678b',
    content: `
## Energieausweis: Verschärfte Pflichten ab 2026

Das **Gebäudeenergiegesetz (GEG)** regelt die Pflicht zum Energieausweis. Ab 2026 werden Verstöße strenger geahndet.

### Rechtsgrundlagen

- **§ 80 GEG** - Grundsätze des Energieausweises
- **§ 82 GEG** - Ausstellung und Verwendung
- **§ 87 GEG** - Pflichtangaben in Immobilienanzeigen
- **§ 108 GEG** - Bußgeldvorschriften

### Wann ist ein Energieausweis Pflicht?

Ein Energieausweis muss vorgelegt werden bei:
1. **Verkauf** eines Gebäudes
2. **Vermietung** einer Wohnung
3. **Verpachtung** eines Gebäudes
4. **Leasing** von Immobilien

> **§ 82 Abs. 1 GEG:**  
> "Wird ein Gebäude errichtet, hat der Eigentümer sicherzustellen, dass ihm ein Energieausweis ausgestellt wird."

### Bedarfsausweis vs. Verbrauchsausweis

| Ausweis | Grundlage | Pflicht bei |
|---------|-----------|-------------|
| Bedarfsausweis | Technische Berechnung | Gebäude < 5 Wohnungen, Baujahr vor 1977 |
| Verbrauchsausweis | Tatsächlicher Verbrauch | Alle anderen Fälle |

### Bußgelder bei Verstößen

Nach **§ 108 GEG** drohen folgende Bußgelder:

| Verstoß | Bußgeld bis |
|---------|------------|
| Kein Energieausweis bei Verkauf/Vermietung | 15.000 € |
| Fehlende Pflichtangaben in Anzeigen | 15.000 € |
| Vorlage eines ungültigen Ausweises | 10.000 € |
| Falsche Angaben im Energieausweis | 15.000 € |

### Pflichtangaben in Immobilienanzeigen

Nach **§ 87 GEG** müssen in kommerziellen Anzeigen angegeben werden:
- Art des Energieausweises
- Endenergiebedarf oder -verbrauch
- Wesentlicher Energieträger
- Baujahr des Gebäudes
- Energieeffizienzklasse (A+ bis H)

### Beispiel für korrekte Angabe

*"Energieausweis: Bedarfsausweis, 125 kWh/(m²·a), Energieeffizienzklasse D, Baujahr 1985, Heizung: Gas-Zentralheizung"*

### Weiterführende Links

- [Gesetzestext GEG](https://www.gesetze-im-internet.de/geg/)

---

*Stand: Januar 2026*
    `,
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    authorBio: 'Konstantin Kranich ist Jurist und Gründer von domulex.ai.',
    publishedAt: '2025-12-10T10:00:00+01:00',
    category: 'Immobilienrecht',
    readTime: '4 Min.',
    tags: ['Energieausweis', 'GEG', 'Bußgeld', 'Vermietung', 'Immobilienanzeigen']
  }
};

// Metadata für SEO
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const article = articles[slug];
  
  if (!article) {
    return { title: 'Artikel nicht gefunden | domulex.ai News' };
  }
  
  return {
    title: `${article.title} | domulex.ai News`,
    description: article.excerpt,
    authors: [{ name: article.author, url: 'https://domulex.ai/redaktion#konstantin-kranich' }],
    keywords: article.tags,
    alternates: {
      canonical: `https://domulex.ai/news/${slug}`,
    },
    openGraph: {
      title: article.title,
      description: article.excerpt,
      url: `https://domulex.ai/news/${slug}`,
      siteName: 'domulex.ai',
      locale: 'de_DE',
      type: 'article',
      publishedTime: article.publishedAt,
      modifiedTime: article.modifiedAt || article.publishedAt,
      authors: ['https://domulex.ai/redaktion#konstantin-kranich'],
      section: article.category,
      tags: article.tags,
      images: article.image ? [
        {
          url: article.image,
          width: 1200,
          height: 630,
          alt: article.title,
        }
      ] : undefined,
    },
    twitter: {
      card: 'summary_large_image',
      title: article.title,
      description: article.excerpt,
      images: article.image ? [article.image] : undefined,
    },
    robots: {
      index: true,
      follow: true,
      'max-image-preview': 'large',
      'max-snippet': -1,
      'max-video-preview': -1,
    },
  };
}

// Static params für Export-Modus
export function generateStaticParams() {
  return Object.keys(articles).map((slug) => ({
    slug,
  }));
}

function formatDate(dateString: string) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('de-DE', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  }).format(date);
}

export default async function NewsArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const article = articles[slug];
  
  if (!article) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-[#1e3a5f] mb-4">Artikel nicht gefunden</h1>
          <Link href="/news" className="text-blue-600 hover:underline">Zurück zur Übersicht</Link>
        </div>
      </div>
    );
  }

  // JSON-LD Schema für NewsArticle (Google News Optimierung)
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: article.title,
    description: article.excerpt,
    image: article.image ? [article.image] : ['https://domulex.ai/og/default.jpg'],
    datePublished: article.publishedAt,
    dateModified: article.modifiedAt || article.publishedAt,
    author: {
      '@type': 'Person',
      name: article.author,
      jobTitle: article.authorRole,
      url: 'https://domulex.ai/redaktion#konstantin-kranich',
      sameAs: ['https://linkedin.com/in/konstantinkranich']
    },
    publisher: {
      '@type': 'Organization',
      name: 'domulex.ai',
      url: 'https://domulex.ai',
      logo: {
        '@type': 'ImageObject',
        url: 'https://domulex.ai/logo.png',
        width: 600,
        height: 60
      }
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://domulex.ai/news/${slug}`
    },
    articleSection: article.category,
    keywords: article.tags.join(', '),
    inLanguage: 'de-DE',
    isAccessibleForFree: true,
    copyrightHolder: {
      '@type': 'Organization',
      name: 'Home Invest & Management GmbH'
    }
  };

  return (
    <>
      {/* JSON-LD Schema (unsichtbar im Quellcode für Google) */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      
      <div className="min-h-screen bg-[#fafaf8]">
        {/* Navigation - wie Landing Page */}
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <div className="flex items-center justify-between h-[106px]">
              <Logo size="sm" />
              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center gap-8">
                <Link href="/#vorteile" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">Vorteile</Link>
                <Link href="/#zielgruppen" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">Für wen?</Link>
                <Link href="/#pricing" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">Preise</Link>
                <Link href="/news" className="text-[#1e3a5f] font-semibold transition-colors">News</Link>
                <Link href="/faq" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">FAQ</Link>
                <Link href="/auth/login" className="px-5 py-2.5 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium transition-colors">
                  Anmelden
                </Link>
              </div>
              {/* Mobile */}
              <Link href="/auth/login" className="md:hidden px-4 py-2 bg-[#1e3a5f] text-white rounded-lg font-medium text-sm">
                Anmelden
              </Link>
            </div>
          </div>
        </nav>

        <main className="max-w-3xl mx-auto px-4 sm:px-6 pt-36 pb-12">
          {/* Breadcrumb */}
          <nav className="mb-6 text-sm">
            <ol className="flex items-center gap-2 text-gray-500">
              <li><Link href="/" className="hover:text-[#1e3a5f]">Start</Link></li>
              <li>/</li>
              <li><Link href="/news" className="hover:text-[#1e3a5f]">News</Link></li>
              <li>/</li>
              <li className="text-[#1e3a5f] truncate">{article.title}</li>
            </ol>
          </nav>

          {/* Article Header */}
          <header className="mb-8">
            <div className="flex items-center gap-3 mb-4">
              <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                {article.category}
              </span>
              <span className="text-gray-500 text-sm">{article.readTime}</span>
            </div>
            
            <h1 className="text-3xl md:text-4xl font-bold text-[#1e3a5f] mb-4 leading-tight">
              {article.title}
            </h1>
            
            <p className="text-xl text-gray-600 mb-6">
              {article.excerpt}
            </p>

            {/* Hero Image */}
            {article.image && (
              <div className="relative w-full h-64 md:h-80 rounded-xl overflow-hidden mb-6">
                <Image
                  src={article.image}
                  alt={article.title}
                  fill
                  className="object-cover"
                  priority
                />
              </div>
            )}

            {/* Author & Date - Wichtig für E-E-A-T */}
            <div className="flex items-center gap-4 p-4 bg-white rounded-xl border border-gray-100">
              <img 
                src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/redakteur.jpeg?alt=media&token=e9ace397-f255-44ee-9138-f08cd9ccd0a6"
                alt={article.author}
                className="w-14 h-14 rounded-full object-cover"
              />
              <div className="flex-1">
                <p className="font-semibold text-[#1e3a5f]">{article.author}</p>
                <p className="text-sm text-gray-500">{article.authorRole}</p>
              </div>
              <div className="text-right">
                <time 
                  dateTime={article.publishedAt} 
                  className="text-sm text-gray-500 block"
                >
                  Veröffentlicht: {formatDate(article.publishedAt)}
                </time>
                {article.modifiedAt && (
                  <time 
                    dateTime={article.modifiedAt}
                    className="text-xs text-gray-400"
                  >
                    Aktualisiert: {formatDate(article.modifiedAt)}
                  </time>
                )}
              </div>
            </div>
          </header>

          {/* Article Content */}
          <article className="prose prose-lg max-w-none 
            prose-headings:text-[#1e3a5f] prose-headings:font-bold prose-headings:mt-8 prose-headings:mb-4
            prose-h2:text-2xl prose-h3:text-xl
            prose-p:mb-4 prose-p:leading-relaxed
            prose-a:text-blue-600 prose-a:underline prose-a:font-medium hover:prose-a:text-blue-800
            prose-strong:text-[#1e3a5f]
            prose-blockquote:border-l-4 prose-blockquote:border-[#1e3a5f] prose-blockquote:pl-4 prose-blockquote:italic prose-blockquote:bg-gray-50 prose-blockquote:py-2
            prose-ul:list-disc prose-ul:pl-6 prose-ul:my-4
            prose-ol:list-decimal prose-ol:pl-6 prose-ol:my-4
            prose-li:mb-2
            prose-table:border-collapse prose-table:w-full prose-table:my-6
            prose-th:bg-gray-100 prose-th:p-3 prose-th:border prose-th:border-gray-300 prose-th:text-left prose-th:font-semibold
            prose-td:p-3 prose-td:border prose-td:border-gray-300
            prose-hr:my-8 prose-hr:border-gray-200
          ">
            <div dangerouslySetInnerHTML={{ __html: marked.parse(article.content) as string }} />
          </article>

          {/* Author Box - Wichtig für E-E-A-T */}
          <div className="mt-8 p-6 bg-white rounded-xl border border-gray-100">
            <h3 className="text-lg font-semibold text-[#1e3a5f] mb-4">Über den Autor</h3>
            <div className="flex gap-4">
              <img 
                src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/redakteur.jpeg?alt=media&token=e9ace397-f255-44ee-9138-f08cd9ccd0a6"
                alt={article.author}
                className="w-16 h-16 rounded-full object-cover flex-shrink-0"
              />
              <div>
                <p className="font-semibold text-[#1e3a5f]">{article.author}</p>
                <p className="text-sm text-gray-500 mb-2">{article.authorRole}</p>
                <p className="text-sm text-gray-600">{article.authorBio}</p>
                <Link 
                  href="/redaktion#konstantin-kranich"
                  className="text-sm text-blue-600 hover:underline mt-2 inline-block"
                >
                  Mehr über den Autor →
                </Link>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="mt-8 p-6 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] rounded-xl text-center">
            <h3 className="text-xl font-bold text-white mb-2">
              Haben Sie Fragen zu diesem Thema?
            </h3>
            <p className="text-blue-100 mb-4">
              Unser KI-Assistent hilft Ihnen mit rechtlichen Fragen zu Immobilien.
            </p>
            <Link
              href="/dashboard"
              className="inline-block px-6 py-3 bg-white text-[#1e3a5f] font-semibold rounded-lg hover:bg-gray-100 transition-colors"
            >
              Jetzt domulex.ai testen
            </Link>
          </div>

          {/* Related Articles */}
          <div className="mt-12">
            <h3 className="text-xl font-bold text-[#1e3a5f] mb-6">Weitere Artikel</h3>
            <div className="grid md:grid-cols-2 gap-4">
              {Object.entries(articles)
                .filter(([s]) => s !== slug)
                .slice(0, 2)
                .map(([s, a]) => (
                  <Link
                    key={s}
                    href={`/news/${s}`}
                    className="p-4 bg-white rounded-xl border border-gray-100 hover:shadow-lg transition-shadow"
                  >
                    <span className="text-xs text-blue-600 font-medium">{a.category}</span>
                    <h4 className="font-semibold text-[#1e3a5f] mt-1 line-clamp-2">{a.title}</h4>
                    <p className="text-sm text-gray-500 mt-1">{formatDate(a.publishedAt)}</p>
                  </Link>
                ))}
            </div>
          </div>
        </main>

        <PremiumFooter />
      </div>
    </>
  );
}
