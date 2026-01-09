'use client';

import Link from 'next/link';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';

export default function FunktionenPage() {
  return (
    <div className="min-h-screen bg-[#fafaf8]">
      <PremiumHeader activePage="funktionen" />

      <main className="pt-32 pb-20">
        {/* Hero */}
        <section className="px-4 pb-20 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-[#fafaf8] via-white to-[#f0f4f8]"></div>
          <div className="absolute top-10 right-1/4 w-64 h-64 bg-[#b8860b]/5 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-1/4 w-48 h-48 bg-[#1e3a5f]/5 rounded-full blur-3xl"></div>
          <div className="max-w-4xl mx-auto text-center relative">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-[#1e3a5f]/5 border border-[#1e3a5f]/10 rounded-full text-sm font-medium text-[#1e3a5f] mb-6">
              <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full animate-pulse"></span>
              Plattform-Übersicht
            </span>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-[#1e3a5f] mb-6 tracking-tight">
              Alle Funktionen im <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#b8860b] to-[#d4a50f]">Überblick</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Entdecken Sie die Tools, die Ihre Arbeit mit Immobilienrecht revolutionieren
            </p>
          </div>
        </section>

        {/* Professional-Features (Verwalter & Investoren) */}
        <section className="py-16 px-4 bg-white">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 border border-blue-200 rounded-full mb-6">
                <span className="text-xl">🏢</span>
                <span className="text-blue-700 text-sm font-semibold">Professional – 39€/Monat</span>
              </div>
              <h2 className="text-3xl font-bold text-[#1e3a5f] mb-4">
                Für Verwalter & Investoren
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Eine Plattform für alles: Objekte, Mieter, Abrechnungen, Verträge
              </p>
            </div>

            {/* INVESTOR Section */}
            <div className="mb-12">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">📈</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-[#1e3a5f]">Für Investoren & Vermieter</h3>
                  <p className="text-gray-500">Kaufen Sie kein Objekt mehr blind – analysieren Sie vorher</p>
                </div>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { icon: '📈', title: 'KI-Renditerechner', desc: 'Lohnt sich das Objekt? Brutto-/Nettorendite, 10-Jahres-Cashflow', highlight: true },
                  { icon: '🤖', title: 'KI-Vertragsanalyse', desc: 'Kaufvertrag prüfen bevor Sie unterschreiben – Risiken erkennen' },
                  { icon: '💰', title: 'Steuer-Optimierung', desc: 'AfA richtig nutzen, Spekulationsfrist, Grunderwerbsteuer sparen' },
                  { icon: '🏗️', title: 'Baurecht-Assistent', desc: 'Mängel nach Kauf? VOB/BGB, Gewährleistung, Verjährungsfristen' }
                ].map((item, idx) => (
                  <div key={idx} className={`rounded-xl p-6 ${item.highlight ? 'bg-gradient-to-br from-emerald-50 to-green-50 border-2 border-emerald-300 shadow-md' : 'bg-gray-50 border border-gray-200'}`}>
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-3xl">{item.icon}</span>
                      <h4 className="font-semibold text-[#1e3a5f]">{item.title}</h4>
                    </div>
                    <p className="text-gray-600 text-sm">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* IMMOBILIENVERWALTER Section */}
            <div className="mb-12">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center">
                  <span className="text-2xl">🏠</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-[#1e3a5f]">Für Immobilienverwalter</h3>
                  <p className="text-gray-500">Weniger Verwaltungsaufwand, mehr Zeit für Ihre Eigentümer</p>
                </div>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { icon: '🏘️', title: 'KI-Immobilienverwaltung', desc: 'Mieter, Eigentümer, Mahnwesen, Zähler, Mieterhöhung, Handwerker', highlight: true },
                  { icon: '📊', title: 'Nebenkostenabrechnung', desc: '17 Kostenarten nach BetrKV, BGH-konform, Export pro Mieter' },
                  { icon: '📋', title: 'WEG-Verwaltung', desc: 'Beschlussbuch, Eigentümerversammlungen, Umsetzungsstatus' },
                  { icon: '🤖', title: 'KI-Vertragsanalyse', desc: 'Mietverträge prüfen, Risiko-Klauseln erkennen' }
                ].map((item, idx) => (
                  <div key={idx} className={`rounded-xl p-6 ${item.highlight ? 'bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-300 shadow-md' : 'bg-gray-50 border border-gray-200'}`}>
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-3xl">{item.icon}</span>
                      <h4 className="font-semibold text-[#1e3a5f]">{item.title}</h4>
                    </div>
                    <p className="text-gray-600 text-sm">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="text-center">
              <Link 
                href="/auth/register?plan=professional"
                className="inline-flex items-center gap-2 px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold text-lg shadow-lg transition-colors"
              >
                Professional starten – 39€/Monat
              </Link>
            </div>
          </div>
        </section>

        {/* Divider */}
        <div className="max-w-6xl mx-auto px-4">
          <div className="h-px bg-gradient-to-r from-transparent via-gray-300 to-transparent"></div>
        </div>

        {/* Kanzlei-Features (Lawyer Pro) */}
        <section className="py-16 px-4 bg-[#fafaf8]">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-[#b8860b]/10 border border-[#b8860b]/20 rounded-full mb-6">
                <span className="text-xl">⚖️</span>
                <span className="text-[#b8860b] text-sm font-semibold">Lawyer Pro – 69€/Monat</span>
              </div>
              <h2 className="text-3xl font-bold text-[#1e3a5f] mb-4">
                Für Juristen & Kanzleien
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                CRM, Dokumentenmanagement und KI-Rechtsassistenz in einem System
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 mb-12">
              {[
                {
                  icon: '👥',
                  title: 'Mandantenverwaltung (CRM)',
                  desc: 'Professionelles Client-Management mit KI-Insights',
                  features: ['Zentrale Mandantenverwaltung & Kontaktdaten', 'Case-Tracking mit Aktenführung', 'KI-Fallanalyse & Strategieempfehlungen', 'Fristenverwaltung & Wiedervorlagen']
                },
                {
                  icon: '📁',
                  title: 'Dokumentenmanagement',
                  desc: 'Intelligente Akten-Organisation mit KI-Suche',
                  features: ['Automatische Kategorisierung', 'Semantische KI-Suche', 'Dokumenten-Zusammenfassungen', 'Verknüpfung mit Mandaten']
                },
                {
                  icon: '📝',
                  title: 'Schriftsatz-Generierung',
                  desc: 'Automatische Erstellung juristischer Dokumente',
                  features: ['Klagen, Mahnungen, Kündigungen, Kaufverträge', 'Mietverträge mit individuellen Klauseln', 'Korrekte juristische Formulierungen', 'Druckfertige, professionelle Dokumente']
                },
                {
                  icon: '🔍',
                  title: 'Quellenfilter & Recherche',
                  desc: 'Gezielte Suche in allen Rechtsquellen',
                  features: ['Filter: Gesetze, Urteile, Literatur, Verwaltung', 'Gerichtsebenen: EuGH, BGH, BFH, OLG, LG, AG', 'Umfangreiche Urteile und Kommentare', 'Quellenangaben mit Paragrafen & Aktenzeichen']
                }
              ].map((item, idx) => (
                <div key={idx} className="bg-white rounded-xl p-8 border border-gray-200 shadow-sm">
                  <div className="flex items-start gap-4">
                    <div className="w-14 h-14 bg-[#1e3a5f] rounded-xl flex items-center justify-center text-2xl text-white flex-shrink-0">
                      {item.icon}
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-[#1e3a5f] mb-2">{item.title}</h3>
                      <p className="text-gray-600 mb-4">{item.desc}</p>
                      <ul className="space-y-2 text-gray-600 text-sm">
                        {item.features.map((f, i) => (
                          <li key={i} className="flex items-center gap-2">
                            <span className="text-green-600">✓</span> {f}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Value Proposition */}
            <div className="bg-[#1e3a5f] rounded-2xl p-8 md:p-12">
              <div className="grid md:grid-cols-2 gap-8 items-center">
                <div>
                  <h3 className="text-2xl font-bold text-white mb-4">
                    Sparen Sie bis zu 300€ pro Monat
                  </h3>
                  <p className="text-blue-200 mb-6">
                    Ersetzen Sie teure Einzellösungen durch eine integrierte Plattform.
                  </p>
                  <div className="space-y-3">
                    {[
                      { name: 'CRM-Software (Salesforce, HubSpot)', price: '~150€' },
                      { name: 'Dokumenten-DMS', price: '~80€' },
                      { name: 'Legal-AI-Tools', price: '~120€' }
                    ].map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between text-white">
                        <span>{item.name}</span>
                        <span className="text-blue-300 line-through">{item.price}</span>
                      </div>
                    ))}
                    <div className="border-t border-white/20 pt-3 mt-3">
                      <div className="flex items-center justify-between">
                        <span className="text-white font-semibold">Alles bei domulex.ai</span>
                        <span className="text-[#b8860b] font-bold text-2xl">nur 69€</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="text-center">
                  <Link 
                    href="/auth/register?plan=lawyer"
                    className="inline-block px-8 py-4 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-xl font-bold text-lg shadow-lg transition-colors"
                  >
                    Lawyer Pro starten →
                  </Link>
                  <p className="text-blue-200 text-sm mt-4">Monatlich kündbar • 14 Tage Widerrufsrecht</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Basis-Features */}
        <section className="py-16 px-4 bg-white">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 border border-gray-200 rounded-full mb-6">
                <span className="text-xl">🏠</span>
                <span className="text-gray-700 text-sm font-semibold">Basis – 19€/Monat</span>
              </div>
              <h2 className="text-3xl font-bold text-[#1e3a5f] mb-4">
                Für Mieter & Eigentümer
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Die wichtigsten Tools für private Nutzung
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-10">
              {[
                { icon: '💬', title: 'KI-Rechtsassistent', desc: 'Mietrecht, WEG-Recht, Steuerfragen – 25 Anfragen/Monat' },
                { icon: '📝', title: 'Musterbriefe', desc: 'Mängelanzeige, Mieterhöhung, Kündigung – rechtssichere Vorlagen' },
                { icon: '📊', title: 'Nebenkostenprüfung', desc: 'KI analysiert Ihre Abrechnung auf Fehler' }
              ].map((item, idx) => (
                <div key={idx} className="bg-gray-50 rounded-xl p-6 border border-gray-200 text-center">
                  <span className="text-4xl mb-4 block">{item.icon}</span>
                  <h3 className="font-semibold text-[#1e3a5f] mb-2">{item.title}</h3>
                  <p className="text-gray-600 text-sm">{item.desc}</p>
                </div>
              ))}
            </div>

            <div className="text-center">
              <Link 
                href="/auth/register?plan=basis"
                className="inline-flex items-center gap-2 px-8 py-4 bg-gray-800 hover:bg-gray-900 text-white rounded-xl font-semibold text-lg shadow-lg transition-colors"
              >
                Basis starten – 19€/Monat
              </Link>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-24 px-4 bg-gradient-to-br from-[#1e3a5f] via-[#1e3a5f] to-[#152a45] relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#b8860b]/10 via-transparent to-transparent"></div>
          <div className="absolute top-0 left-1/4 w-64 h-64 bg-[#b8860b]/10 rounded-full blur-3xl"></div>
          <div className="max-w-4xl mx-auto text-center relative">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6 tracking-tight">
              Noch unsicher?
            </h2>
            <p className="text-xl text-blue-200/80 mb-10 leading-relaxed">
              Testen Sie domulex.ai mit 3 kostenlosen Anfragen
            </p>
            <Link 
              href="/auth/register"
              className="group inline-flex items-center gap-3 px-12 py-5 bg-gradient-to-r from-[#b8860b] to-[#d4a50f] hover:from-[#a07608] hover:to-[#b8860b] text-white rounded-2xl font-bold text-lg shadow-2xl shadow-[#b8860b]/40 hover:shadow-[#b8860b]/50 transition-all duration-300 hover:-translate-y-1"
            >
              Kostenlos registrieren
              <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
        </section>
      </main>

      <PremiumFooter />
    </div>
  );
}
