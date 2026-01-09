'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';

// News-Artikel Daten mit 3-stelligen IDs für Google News Optimierung
const newsArticles = [
  {
    id: 107,
    slug: 'co2-kostenaufteilung-abrechnung-2026-107',
    title: 'Abrechnungs-Falle 2026: CO2-Kostenaufteilung korrekt berechnen',
    excerpt: 'Ab Januar 2026 drohen Vermietern bei der Nebenkostenabrechnung Fehlerquellen durch das CO2-Stufenmodell. Jurist K. Kranich erklärt die Risiken und Lösungen.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2026-01-02',
    category: 'Nebenkosten',
    readTime: '5 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/co2-kostenaufteilung.jpeg?alt=media&token=1a530624-7807-40e1-9a21-0de5ce96daec',
    featured: true
  },
  {
    id: 101,
    slug: 'heizungsgesetz-2026-was-vermieter-wissen-muessen-101',
    title: 'Heizungsgesetz 2026: Was Vermieter jetzt wissen müssen',
    excerpt: 'Das neue Gebäudeenergiegesetz (GEG) tritt in verschärfter Form in Kraft. Wir analysieren die wichtigsten Änderungen für Immobilienbesitzer und Vermieter.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2026-01-02',
    category: 'Gesetzgebung',
    readTime: '6 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/heizungsgesetz_2026.jpeg?alt=media&token=9c0eb525-5fe8-4dbb-9250-323228da2d33',
    featured: false
  },
  {
    id: 102,
    slug: 'bgh-urteil-indexmiete-januar-2026-102',
    title: 'BGH-Urteil zur Indexmiete: Neue Grenzen für Mieterhöhungen',
    excerpt: 'Der Bundesgerichtshof hat in einem wegweisenden Urteil die Grenzen von Indexmietverträgen konkretisiert. Das bedeutet das Urteil für Vermieter und Mieter.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2026-01-01',
    category: 'Rechtsprechung',
    readTime: '5 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/bgh_indexmiete.jpeg?alt=media&token=136dbf60-03a6-489d-b24f-7be2e46ad10f',
    featured: true
  },
  {
    id: 103,
    slug: 'grundsteuer-reform-2026-berechnung-103',
    title: 'Grundsteuer-Reform 2026: So berechnen Sie die neue Belastung',
    excerpt: 'Die Grundsteuer-Reform ist in Kraft. Wir erklären Schritt für Schritt, wie Sie Ihre neue Grundsteuer berechnen und welche Einspruchsmöglichkeiten bestehen.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2025-12-28',
    category: 'Steuern',
    readTime: '8 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/grundsteuerreform%202026.jpeg?alt=media&token=22f07396-c79d-4231-8302-6ef236b7244c',
    featured: false
  },
  {
    id: 104,
    slug: 'mietpreisbremse-verlaengerung-2026-104',
    title: 'Mietpreisbremse bis 2029 verlängert: Das neue Gesetz im Überblick',
    excerpt: 'Der Bundestag hat am 26. Juni 2025 die Verlängerung der Mietpreisbremse bis Ende 2029 beschlossen. Wir erklären die Hintergründe und was das für Mieter und Vermieter bedeutet.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2025-12-20',
    category: 'Gesetzgebung',
    readTime: '4 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/mietpreisbremse_2028.jpeg?alt=media&token=3e895b61-03f0-47a4-be56-2a40391909ba',
    featured: false
  },
  {
    id: 105,
    slug: 'weg-reform-2026-digitale-eigentuemerversammlung-105',
    title: 'WEG-Reform 2026: Digitale Eigentümerversammlung wird Standard',
    excerpt: 'Das neue WEG-Änderungsgesetz erleichtert digitale Eigentümerversammlungen erheblich. Was das für Ihre WEG bedeutet.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2025-12-15',
    category: 'WEG-Recht',
    readTime: '5 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/weg-reform_2026.jpeg?alt=media&token=e324ed34-25c1-459e-93d0-3456a272ae5c',
    featured: false
  },
  {
    id: 106,
    slug: 'energieausweis-pflicht-2026-bussgelder-106',
    title: 'Energieausweis-Pflicht 2026: Höhere Bußgelder bei Verstößen',
    excerpt: 'Ab Januar 2026 gelten verschärfte Regeln für Energieausweise. Bei Verstößen drohen nun Bußgelder bis zu 15.000 Euro.',
    author: 'Konstantin Kranich',
    authorRole: 'Jurist & Gründer',
    publishedAt: '2025-12-10',
    category: 'Immobilienrecht',
    readTime: '4 Min.',
    image: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/energieausweis_bussgeld.jpeg?alt=media&token=d65b73e0-5d31-4bb5-917f-b2c8b7c8678b',
    featured: false
  }
];

const categories = ['Alle', 'Gesetzgebung', 'Rechtsprechung', 'Steuern', 'WEG-Recht', 'Immobilienrecht', 'Nebenkosten'];

// Typ für Presse-Veröffentlichungen
interface PressPublication {
  id: number;
  title: string;
  source: string;
  sourceUrl: string;
  publishedAt: string;
  type: 'article' | 'interview' | 'mention' | 'podcast' | 'guest-post';
  excerpt: string;
  logo?: string;
}

// Externe Veröffentlichungen / Presse
const pressPublications: PressPublication[] = [
  // Beispiel-Einträge - hier können echte Veröffentlichungen hinzugefügt werden
  /*
  {
    id: 1,
    title: 'Wie KI das Immobilienrecht revolutioniert',
    source: 'Handelsblatt',
    sourceUrl: 'https://www.handelsblatt.com/...',
    publishedAt: '2026-01-05',
    type: 'interview',
    excerpt: 'Domulex-Gründer Konstantin Kranich über die Zukunft von Legal-Tech im Immobilienrecht.',
    logo: '/press/handelsblatt.png'
  },
  */
];

function formatDate(dateString: string) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('de-DE', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  }).format(date);
}

export default function NewsPage() {
  const [activeCategory, setActiveCategory] = useState('Alle');
  
  const filteredArticles = activeCategory === 'Alle' 
    ? newsArticles 
    : newsArticles.filter(a => a.category === activeCategory);
  
  const featuredArticles = filteredArticles.filter(a => a.featured);
  const regularArticles = filteredArticles.filter(a => !a.featured);

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      <PremiumHeader activePage="news" />

      {/* Hero Section */}
      <section className="pt-36 pb-16 bg-gradient-to-br from-[#1e3a5f] via-[#1e3a5f] to-[#152a45] relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#b8860b]/10 via-transparent to-transparent"></div>
        <div className="absolute top-20 right-1/4 w-64 h-64 bg-[#b8860b]/10 rounded-full blur-3xl"></div>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 text-center relative">
          <span className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-sm font-medium text-white mb-6">
            <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full animate-pulse"></span>
            Aktuelles
          </span>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 tracking-tight">
            Immobilienrecht <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#b8860b] to-[#d4a50f]">News</span>
          </h1>
          <p className="text-xl text-blue-100/80 max-w-2xl mx-auto leading-relaxed">
            Aktuelle Urteile, Gesetzesänderungen und Analysen für Vermieter, 
            Eigentümer und Immobilien-Profis – von Juristen kommentiert.
          </p>
        </div>
      </section>

      {/* Kategorien */}
      <section className="py-6 bg-white border-b border-gray-100 sticky top-[106px] z-40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex gap-3 overflow-x-auto pb-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                  cat === activeCategory 
                    ? 'bg-[#1e3a5f] text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </section>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
        {/* Featured Articles */}
        {featuredArticles.length > 0 && (
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-[#1e3a5f] mb-6">Top-Meldungen</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {featuredArticles.map((article) => (
              <Link
                key={article.id}
                href={`/news/${article.slug}`}
                className="group bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden hover:shadow-lg transition-shadow"
              >
                <div className="aspect-video bg-gradient-to-br from-[#1e3a5f] to-[#3d5a7f] relative overflow-hidden">
                  {article.image ? (
                    <Image
                      src={article.image}
                      alt={article.title}
                      fill
                      className="object-cover"
                      sizes="(max-width: 768px) 100vw, 50vw"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="text-6xl opacity-50">📰</span>
                    </div>
                  )}
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                      {article.category}
                    </span>
                    <time className="text-sm text-gray-500" dateTime={article.publishedAt}>
                      {formatDate(article.publishedAt)}
                    </time>
                  </div>
                  <h3 className="text-xl font-bold text-[#1e3a5f] mb-2 group-hover:text-blue-600 transition-colors">
                    {article.title}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-2">
                    {article.excerpt}
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <img 
                        src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/redakteur.jpeg?alt=media&token=e9ace397-f255-44ee-9138-f08cd9ccd0a6"
                        alt={article.author}
                        className="w-8 h-8 rounded-full object-cover"
                      />
                      <div>
                        <p className="text-sm font-medium text-[#1e3a5f]">{article.author}</p>
                        <p className="text-xs text-gray-500">{article.authorRole}</p>
                      </div>
                    </div>
                    <span className="text-sm text-gray-500">{article.readTime}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>
        )}

        {/* Regular Articles */}
        {regularArticles.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold text-[#1e3a5f] mb-6">
            {activeCategory === 'Alle' ? 'Weitere Meldungen' : `${activeCategory} Artikel`}
          </h2>
          <div className="space-y-6">
            {regularArticles.map((article) => (
              <Link
                key={article.id}
                href={`/news/${article.slug}`}
                className="group flex gap-6 bg-white rounded-xl border border-gray-100 shadow-sm p-4 hover:shadow-lg transition-shadow"
              >
                <div className="w-32 h-24 bg-gradient-to-br from-[#1e3a5f] to-[#3d5a7f] rounded-lg overflow-hidden flex-shrink-0 relative">
                  {article.image ? (
                    <Image
                      src={article.image}
                      alt={article.title}
                      fill
                      className="object-cover"
                      sizes="128px"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="text-3xl opacity-50">📰</span>
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                      {article.category}
                    </span>
                    <time className="text-sm text-gray-500" dateTime={article.publishedAt}>
                      {formatDate(article.publishedAt)}
                    </time>
                    <span className="text-sm text-gray-400">•</span>
                    <span className="text-sm text-gray-500">{article.readTime}</span>
                  </div>
                  <h3 className="text-lg font-bold text-[#1e3a5f] mb-1 group-hover:text-blue-600 transition-colors truncate">
                    {article.title}
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-1">
                    {article.excerpt}
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </section>
        )}

        {/* Empty State */}
        {filteredArticles.length === 0 && (
          <div className="text-center py-16">
            <span className="text-6xl mb-4 block">📭</span>
            <h3 className="text-xl font-bold text-[#1e3a5f] mb-2">Keine Artikel gefunden</h3>
            <p className="text-gray-600 mb-4">In dieser Kategorie gibt es noch keine Artikel.</p>
            <button 
              onClick={() => setActiveCategory('Alle')}
              className="text-blue-600 hover:underline"
            >
              Alle Artikel anzeigen
            </button>
          </div>
        )}

        {/* Presse & Veröffentlichungen */}
        {pressPublications.length > 0 && (
          <section className="mt-16">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-2xl">📰</span>
              <h2 className="text-2xl font-bold text-[#1e3a5f]">Presse & Veröffentlichungen</h2>
            </div>
            <p className="text-gray-600 mb-6">
              domulex.ai in den Medien – Interviews, Gastbeiträge und Erwähnungen.
            </p>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {pressPublications.map((pub) => (
                <a
                  key={pub.id}
                  href={pub.sourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group bg-white rounded-xl border border-gray-100 shadow-sm p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-center justify-between mb-4">
                    <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                      pub.type === 'interview' ? 'bg-purple-100 text-purple-800' :
                      pub.type === 'guest-post' ? 'bg-green-100 text-green-800' :
                      pub.type === 'podcast' ? 'bg-orange-100 text-orange-800' :
                      pub.type === 'mention' ? 'bg-gray-100 text-gray-800' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {pub.type === 'interview' ? '🎤 Interview' :
                       pub.type === 'guest-post' ? '✍️ Gastbeitrag' :
                       pub.type === 'podcast' ? '🎙️ Podcast' :
                       pub.type === 'mention' ? '📌 Erwähnung' :
                       '📄 Artikel'}
                    </span>
                    <time className="text-sm text-gray-500" dateTime={pub.publishedAt}>
                      {formatDate(pub.publishedAt)}
                    </time>
                  </div>
                  <h3 className="text-lg font-bold text-[#1e3a5f] mb-2 group-hover:text-blue-600 transition-colors">
                    {pub.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {pub.excerpt}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">
                      {pub.source}
                    </span>
                    <span className="text-blue-600 text-sm group-hover:underline">
                      Lesen →
                    </span>
                  </div>
                </a>
              ))}
            </div>
          </section>
        )}

        {/* Newsletter CTA */}
        <section className="mt-20 bg-gradient-to-br from-[#1e3a5f] to-[#2d4a6f] rounded-3xl p-10 md:p-14 text-center relative overflow-hidden shadow-2xl">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-[#b8860b]/20 via-transparent to-transparent"></div>
          <div className="relative">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Immer informiert bleiben
            </h2>
            <p className="text-blue-200/80 mb-8 max-w-xl mx-auto leading-relaxed">
              Erhalten Sie wichtige Urteile und Gesetzesänderungen direkt per E-Mail – 
              kompakt zusammengefasst von unserer Juristen-Redaktion.
            </p>
            <form className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Ihre E-Mail-Adresse"
                className="flex-1 px-5 py-4 rounded-xl border-0 focus:ring-2 focus:ring-[#b8860b] bg-white/95 backdrop-blur-sm text-gray-800 placeholder-gray-500 shadow-lg"
              />
              <button
                type="submit"
                className="px-8 py-4 bg-gradient-to-r from-[#b8860b] to-[#d4a50f] text-white font-semibold rounded-xl hover:from-[#a07608] hover:to-[#b8860b] transition-all duration-300 shadow-lg shadow-[#b8860b]/30 hover:-translate-y-0.5"
              >
                Anmelden
              </button>
            </form>
            <p className="text-sm text-blue-200/60 mt-4">
              Kein Spam. Abmeldung jederzeit möglich.
            </p>
          </div>
        </section>
      </main>

      <PremiumFooter />
    </div>
  );
}
