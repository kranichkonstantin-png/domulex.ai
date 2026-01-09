'use client';

import Link from 'next/link';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';

interface FAQ {
  question: string;
  answer: string;
  category: string;
}

const FAQ_DATABASE: FAQ[] = [
  // === DATENBANK & QUELLEN ===
  {
    category: "Datenbank & Quellen",
    question: "Welche Rechtsquellen enthält domulex.ai?",
    answer: "Unsere Datenbank umfasst über 50.000 deutsche Rechtsdokumente:\n\n📖 GESETZE & VERORDNUNGEN:\n• BGB (Mietrecht §§535-580a, Sachenrecht §§854-1296)\n• WEG (Wohnungseigentumsgesetz)\n• BauGB, BauNVO, LBO aller Bundesländer\n• MaBV (Makler- und Bauträgerverordnung)\n• HeizKV, EnEV, GEG (Energierecht)\n• EStG, GrEStG, GrStG (Steuerrecht)\n\n⚖️ RECHTSPRECHUNG:\n• 2.500+ BGH-Urteile (Miet-, Kauf-, WEG-Recht)\n• 500+ BFH-Entscheidungen (Immobiliensteuerrecht)\n• EuGH-Urteile mit Deutschlandbezug\n• OLG/LG-Urteile (im Lawyer Pro Tarif)\n\n📋 VERWALTUNGSVORSCHRIFTEN:\n• BMF-Schreiben (AfA-Tabellen, Werbungskosten)\n• EStR, GrEStR, ErbStR\n• Finanzamts-Richtlinien\n\n📚 FACHLITERATUR (Lawyer Pro):\n• Palandt, MüKo, Staudinger Kommentare\n• Beck'sche Handbücher\n• NZM, ZMR Zeitschriften-Fundstellen"
  },
  {
    category: "Datenbank & Quellen",
    question: "Wie aktuell sind die Rechtsinformationen?",
    answer: "Unsere Datenbank wird kontinuierlich gepflegt:\n\n• GESETZE: Konsolidierte Fassungen nach jeder Gesetzesänderung\n• BGH-URTEILE: Neue Entscheidungen werden zeitnah ergänzt\n• BFH-URTEILE: Aktuelle Steuerrechtsprechung laufend aktualisiert\n• BMF-SCHREIBEN: Neue Verwaltungsanweisungen bei Veröffentlichung\n\n✓ Das exakte Quelldatum wird bei jeder Antwort angezeigt\n✓ Veraltete Rechtsprechung wird als überholt gekennzeichnet\n✓ Gesetzesänderungen werden mit Inkrafttreten-Datum markiert"
  },
  {
    category: "Datenbank & Quellen",
    question: "Warum kann ich den Quellen vertrauen?",
    answer: "domulex.ai nutzt ausschließlich offizielle, verifizierte Rechtsquellen:\n\n✓ Gesetze: Aus dem BGBl und offiziellen Gesetzesportalen\n✓ BGH/BFH-Urteile: Aus der amtlichen Sammlung und juris\n✓ BMF-Schreiben: Direkt vom Bundesfinanzministerium\n✓ Keine Wikipedia, Foren oder ungeprüfte Inhalte\n\nBei jeder Antwort sehen Sie:\n• Exakte Fundstelle (z.B. BGH VIII ZR 123/20)\n• Datum der Entscheidung\n• Relevante Leitsätze\n• Link zur Originalquelle (wo verfügbar)"
  },
  // === PLATTFORM & FUNKTIONEN ===
  {
    category: "Plattform & Funktionen",
    question: "Was kann der Rechts-Chat?",
    answer: "Der Rechts-Chat analysiert Ihren individuellen Fall:\n\n🔍 FALLANALYSE:\n• Schildern Sie Ihre konkrete Situation\n• Die KI erkennt relevante Rechtsfragen\n• Antwort mit passenden §§ und Urteilen\n\n📋 AUSGABE ENTHÄLT:\n• Rechtliche Einordnung Ihres Falls\n• Einschlägige Paragraphen mit Erklärung\n• Relevante BGH-Urteile zu Ihrem Sachverhalt\n• Konkrete Handlungsempfehlungen\n• Musterformulierungen (z.B. für Schreiben an Vermieter)\n\n💡 BEISPIELE:\n• 'Mein Vermieter hat die Miete um 15% erhöht...'\n• 'Schönheitsreparaturen laut Mietvertrag alle 3 Jahre...'\n• 'Hausgeldnachzahlung in der WEG-Abrechnung...'\n• 'AfA für vermietete Eigentumswohnung Baujahr 1995...'"
  },
  {
    category: "Plattform & Funktionen",
    question: "Was ist die Vertragsanalyse?",
    answer: "Die Vertragsanalyse (ab Professional) prüft Ihre Verträge auf Herz und Nieren:\n\n📄 MIETVERTRÄGE:\n• Unwirksame Schönheitsreparatur-Klauseln (BGH-Rechtsprechung)\n• Unzulässige Kündigungsausschlüsse\n• Fehlerhafte Betriebskostenpauschalen\n• Unzulässige Kautions-Regelungen\n• Index-/Staffelmieten-Prüfung\n\n🏠 KAUFVERTRÄGE:\n• Gewährleistungsausschlüsse\n• Besitzübergang und Gefahrtragung\n• Finanzierungsvorbehalte\n• Notarkosten-Verteilung\n\n📊 ERGEBNIS:\n• Risikobewertung (Grün/Gelb/Rot)\n• Erklärung jeder problematischen Klausel\n• Konkrete Nachverhandlungs-Vorschläge\n• Musterschreiben zur Nachbesserung"
  },
  {
    category: "Plattform & Funktionen",
    question: "Was bietet der Renditerechner?",
    answer: "Der Renditerechner (ab Professional) für Investoren:\n\n📊 RENDITE-BERECHNUNG:\n• Bruttomietrendite\n• Nettomietrendite (nach Kosten)\n• Eigenkapitalrendite\n• Cashflow vor/nach Steuern\n\n💰 STEUER-KALKULATION:\n• AfA-Berechnung (2%, 2.5%, 3% je nach Baujahr)\n• Werbungskosten-Optimierung\n• Abschreibung für Sanierungen\n• Zinsabzug bei Finanzierung\n\n📈 PROGNOSE:\n• 10-Jahres-Cashflow-Projektion\n• Wertsteigerungsszenarien\n• Tilgungsfortschritt\n• Vermögensaufbau-Simulation"
  },
  {
    category: "Plattform & Funktionen",
    question: "Welche Musterbriefe und Vorlagen gibt es?",
    answer: "Über 50 rechtssichere Vorlagen + eigene Vorlagen erstellen:\n\n📝 EIGENE VORLAGEN (alle Tarife):\n• Mit KI individuelle Dokumente erstellen\n• Vorlagen speichern und wiederverwenden\n• Stellungnahmen, Schreiben, Anträge\n\n📝 MIETRECHT:\n• Mieterhöhungsverlangen (§558 BGB)\n• Betriebskostenwiderspruch\n• Mängelanzeige mit Fristsetzung\n• Kündigung (ordentlich/außerordentlich)\n• Kautionsrückforderung\n\n🏢 WEG-RECHT:\n• Beschlussanfechtung\n• Einsichtnahme Verwaltungsunterlagen\n• Sondereigentum-Nutzung\n\n⚖️ SCHRIFTSÄTZE (Lawyer Pro):\n• Klageschriften (Mietrecht, WEG)\n• Klageerwiderungen\n• Berufungsbegründungen\n• Anträge auf einstweilige Verfügung"
  },
  // === STEUERRECHT ===
  {
    category: "Steuerrecht",
    question: "Welche Steuerthemen deckt domulex.ai ab?",
    answer: "Steuerrechtliche Informationen zu Immobilien:\n\n📊 EINKOMMENSTEUER:\n• AfA-Berechnung für alle Gebäudetypen\n• Sonder-AfA für Neubau-Mietwohnungen\n• Erhaltungsaufwand vs. Herstellungskosten\n• Werbungskosten bei Vermietung\n• Fahrtkosten, Kontoführung, Steuerberaterkosten\n\n🏠 GRUNDERWERBSTEUER:\n• Steuersätze je Bundesland (3,5% - 6,5%)\n• Share Deals und Grundstücksgesellschaften\n• Befreiungstatbestände\n\n💶 SPEKULATIONSFRIST:\n• 10-Jahres-Frist bei Grundstücken\n• Eigennutzung und Ausnahmen\n• Gewinnberechnung\n\n📋 QUELLEN:\n• 100+ BFH-Urteile\n• Aktuelle BMF-Schreiben\n• Einkommensteuer-Richtlinien\n\n⚠️ Hinweis: Für verbindliche steuerliche Auskünfte wenden Sie sich an Ihren Steuerberater."
  },
  // === TARIFE & PREISE ===
  {
    category: "Tarife & Preise",
    question: "Welche Tarife gibt es im Detail?",
    answer: "Drei Tarife für unterschiedliche Bedürfnisse:\n\n🔹 BASIS (19€/Monat) – Für Mieter & Eigentümer:\n• 50 Anfragen/Monat\n• Mietrecht, WEG & Nachbarrecht\n• Steuer-Basics (AfA, Werbungskosten)\n• Musterbriefe & eigene Vorlagen mit KI erstellen\n• Nebenkostenrechner\n• E-Mail-Support\n\n🔸 PROFESSIONAL (39€/Monat) – Für Verwalter & Investoren:\n• 250 Anfragen/Monat\n• KI-Vertragsanalyse (Miet- & Kaufverträge)\n• Portfolio-Dashboard für Objekte\n• Steuer-Optimierung & Spekulationsfrist\n• KI-Renditerechner mit Prognose\n• Automatische Nebenkostenabrechnung\n• Baurecht-Assistent\n• Prioritäts-Support\n\n🔶 LAWYER PRO (69€/Monat) – Für Juristen:\n• Unbegrenzte Anfragen\n• Mandanten-CRM mit KI-Aktenführung\n• KI-Fallanalyse mit Erfolgsaussichten\n• KI-Rechtsprechungsanalyse (BGH/OLG/LG)\n• Fristenverwaltung & Wiedervorlagen\n• KI-Schriftsatzgenerierung\n• Dokumentenmanagement\n• 50.000+ Rechtsquellen-Datenbank"
  },
  {
    category: "Tarife & Preise",
    question: "Gibt es einen kostenlosen Test?",
    answer: "Ja! So können Sie domulex.ai testen:\n\n✓ Kostenlose Registrierung (keine Kreditkarte nötig)\n✓ 3 vollwertige Anfragen inklusive\n✓ Voller Zugang zur Basis-Datenbank\n✓ Keine automatische Verlängerung\n\nDie 3 Test-Anfragen reichen, um:\n• Eine konkrete Rechtsfrage zu klären\n• Die Qualität der Antworten zu prüfen\n• Die Quellenangaben zu verifizieren"
  },
  {
    category: "Tarife & Preise",
    question: "Was ist das Mandanten-CRM (Lawyer Pro)?",
    answer: "Das Mandanten-CRM für Juristen:\n\n👥 MANDANTENVERWALTUNG:\n• Mandantenakte mit allen Dokumenten\n• Automatische Fristenverwaltung\n• Wiedervorlagen mit Benachrichtigung\n\n🤖 KI-AKTENFÜHRUNG:\n• Automatische Zusammenfassung neuer Dokumente\n• Rechtsfragen aus Mandantenkorrespondenz extrahieren\n• Relevante Rechtsprechung pro Akte\n\n📝 SCHRIFTSATZGENERIERUNG:\n• Klageschriften auf Knopfdruck\n• Automatische BGH-Zitate\n• Export in Word/PDF"
  },
  // === KONTO & DATENSCHUTZ ===
  {
    category: "Konto & Datenschutz",
    question: "Wie werden meine Daten geschützt?",
    answer: "Höchste Datenschutz-Standards mit Google Cloud:\n\n🔒 GOOGLE CLOUD ZERTIFIZIERUNGEN:\n• ISO 27001 – Informationssicherheit\n• ISO 27017 – Cloud-Security\n• ISO 27018 – Schutz personenbezogener Daten\n• SOC 1, SOC 2, SOC 3 – Audit-Zertifizierungen\n• C5-Testat des BSI – Deutsche Cloud-Sicherheit\n\n🏢 SERVERSTANDORT:\n• Google Cloud Frankfurt (europe-west3)\n• Daten verlassen Deutschland nicht\n• TLS 1.3 Ende-zu-Ende-Verschlüsselung\n\n📋 RECHTLICH:\n• DSGVO-konform\n• EU-Standardvertragsklauseln\n• AV-Vertrag auf Anfrage\n• Datenschutzbeauftragter benannt\n\n🗑️ ZERO DATA RETENTION:\n• Chat-Inhalte werden NICHT dauerhaft gespeichert\n• Keine Weitergabe an Dritte\n• Keine Nutzung für KI-Training\n\n✓ Ihre Rechtsfragen bleiben vertraulich\n✓ Mandantendaten werden nicht ausgewertet"
  },
  {
    category: "Konto & Datenschutz",
    question: "Kann ich jederzeit kündigen?",
    answer: "Ja, volle Flexibilität:\n\n• Monatlich kündbar (zum Monatsende)\n• 14 Tage Widerrufsrecht (auch für Gewerbliche!)\n• Keine Mindestlaufzeit\n• Keine versteckten Kosten\n\nSo kündigen Sie:\n1. Mein Bereich → Abonnement\n2. Klick auf 'Kündigen'\n3. Bestätigung per E-Mail\n\nNach Kündigung:\n• Zugang bis Abrechnungsperiode-Ende\n• Keine weiteren Abbuchungen\n• Daten auf Wunsch löschbar"
  },
  // === TECHNISCHES ===
  {
    category: "Technisches",
    question: "Auf welchen Geräten funktioniert domulex.ai?",
    answer: "domulex.ai läuft überall:\n\n💻 DESKTOP:\n• Chrome, Firefox, Safari, Edge\n• Windows, Mac, Linux\n\n📱 MOBIL:\n• Responsive Design\n• iPhone, Android\n• Tablet-optimiert\n\n🔧 ANFORDERUNGEN:\n• Moderner Browser (letzte 2 Versionen)\n• JavaScript aktiviert\n• Stabile Internetverbindung\n\nKeine Installation nötig - direkt im Browser nutzbar."
  },
  {
    category: "Technisches",
    question: "Welches Recht wird abgedeckt?",
    answer: "Fokus auf deutsches Immobilienrecht:\n\n✅ ENTHALTEN:\n• Deutsches Mietrecht (BGB)\n• WEG-Recht\n• Deutsches Baurecht\n• Maklerrecht (MaBV)\n• Deutsches Steuerrecht\n\n❌ NOCH NICHT ENTHALTEN:\n• Österreichisches Recht (ABGB)\n• Schweizer Recht (OR)\n• Sonstiges Auslandsrecht\n\n🔜 GEPLANT:\n• Österreich\n• Schweiz\n• Spanien\n• USA\n• Dubai/VAE"
  }
];

// Kategorien gruppieren
const categories = [...new Set(FAQ_DATABASE.map(faq => faq.category))];

export default function FAQPage() {
  return (
    <div className="min-h-screen bg-[#fafaf8]">
      <PremiumHeader activePage="faq" />

      {/* Hero */}
      <section className="pt-36 pb-12 px-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#fafaf8] via-white to-[#f0f4f8]"></div>
        <div className="absolute top-20 right-1/3 w-64 h-64 bg-[#b8860b]/5 rounded-full blur-3xl"></div>
        <div className="max-w-4xl mx-auto text-center relative">
          <span className="inline-flex items-center gap-2 px-4 py-2 bg-[#1e3a5f]/5 border border-[#1e3a5f]/10 rounded-full text-sm font-medium text-[#1e3a5f] mb-6">
            <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full"></span>
            Hilfe & Support
          </span>
          <h1 className="text-4xl md:text-5xl font-bold text-[#1e3a5f] mb-4 tracking-tight">Häufig gestellte <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#b8860b] to-[#d4a50f]">Fragen</span></h1>
          <p className="text-xl text-gray-600 leading-relaxed">Alles, was Sie über domulex.ai wissen müssen</p>
        </div>
      </section>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 pb-12">
        {/* FAQ Categories */}
        {categories.map((category) => (
          <div key={category} className="mb-8">
            <h2 className="text-xl font-semibold text-[#1e3a5f] mb-4 flex items-center gap-2">
              {category === "Datenbank & Quellen" && "📚"}
              {category === "Plattform & Funktionen" && "🏠"}
              {category === "Steuerrecht" && "📊"}
              {category === "Tarife & Preise" && "💳"}
              {category === "Konto & Datenschutz" && "🔒"}
              {category === "Technisches" && "⚙️"}
              {category}
            </h2>
            <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className="divide-y divide-gray-100">
                {FAQ_DATABASE.filter(faq => faq.category === category).map((faq, index) => (
                  <details key={index} className="group">
                    <summary className="cursor-pointer p-4 font-medium text-gray-700 hover:bg-gray-50 list-none flex justify-between items-center">
                      {faq.question}
                      <span className="text-gray-400 group-open:rotate-180 transition-transform ml-4">▼</span>
                    </summary>
                    <div className="px-4 pb-4 text-gray-600 whitespace-pre-line border-l-2 border-[#b8860b] ml-4 mr-4 mb-4">
                      {faq.answer}
                    </div>
                  </details>
                ))}
              </div>
            </div>
          </div>
        ))}

        {/* Kontakt Info */}
        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm text-center">
            <div className="text-3xl mb-3">📧</div>
            <h3 className="font-semibold text-[#1e3a5f] mb-2">E-Mail Support</h3>
            <a href="mailto:kontakt@domulex.ai" className="text-[#b8860b] hover:text-[#9a7209]">
              kontakt@domulex.ai
            </a>
          </div>
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm text-center">
            <div className="text-3xl mb-3">🤖</div>
            <h3 className="font-semibold text-[#1e3a5f] mb-2">KI-Support</h3>
            <Link href="/hilfe" className="text-[#b8860b] hover:text-[#9a7209]">
              Chat starten →
            </Link>
          </div>
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm text-center">
            <div className="text-3xl mb-3">📚</div>
            <h3 className="font-semibold text-[#1e3a5f] mb-2">Datenschutz</h3>
            <Link href="/datenschutz" className="text-[#b8860b] hover:text-[#9a7209]">
              Mehr erfahren →
            </Link>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-16 bg-gradient-to-br from-[#1e3a5f] to-[#2d4a6f] rounded-3xl p-10 text-center text-white relative overflow-hidden shadow-2xl">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-[#b8860b]/20 via-transparent to-transparent"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold mb-4">Keine Antwort gefunden?</h2>
            <p className="text-blue-100/80 mb-8 text-lg">Unser KI-Support hilft Ihnen gerne weiter.</p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Link href="/hilfe" className="group bg-gradient-to-r from-[#b8860b] to-[#d4a50f] hover:from-[#a07608] hover:to-[#b8860b] px-8 py-4 rounded-xl font-semibold transition-all duration-300 shadow-lg shadow-[#b8860b]/30 hover:-translate-y-1 inline-flex items-center gap-2">
                KI-Support Chat
                <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
              <Link href="/auth/register" className="bg-white/10 hover:bg-white/20 backdrop-blur-sm px-8 py-4 rounded-xl font-semibold transition-all duration-300 hover:-translate-y-1">
                Kostenlos registrieren
              </Link>
            </div>
          </div>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
