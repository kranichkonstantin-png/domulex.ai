'use client';

import Link from 'next/link';
import Image from 'next/image';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';

// Presseartikel und Veröffentlichungen über domulex.ai
const pressArticles = [
  {
    id: 1,
    title: 'domulex.ai startet digitalen Rechtsassistenten gegen den Bürokratie-Burnout in der Hausverwaltung',
    source: 'OpenPR',
    sourceUrl: 'https://www.openpr.de',
    articleUrl: 'https://www.openpr.de/news/1300426/domulex-ai-startet-digitalen-Rechtsassistenten-gegen-den-Buerokratie-Burnout-in-der-Hausverwaltung.html',
    publishedAt: '2026-01-08',
    excerpt: 'Das Legal-Tech-Startup domulex.ai launcht eine B2B-Plattform für Rechtsanwälte, Hausverwaltungen und Immobilieninvestoren zur rechtssicheren Bewältigung von Immobilienfragen.',
    logo: '/images/press/openpr-logo.png',
    type: 'Pressemitteilung'
  },
];

// Formatiere Datum auf Deutsch
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });
};

export default function PressePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <PremiumHeader />
      
      <main className="pt-32 pb-16">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              📰 Presse & Medien
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Veröffentlichungen und Berichterstattung über <span className="text-[#1e3a5f] font-semibold">domulex</span><span className="text-[#b8860b] font-semibold">.ai</span> in externen Medien
            </p>
          </div>

          {/* Press Contact Box */}
          <div className="bg-[#1e3a5f] text-white rounded-2xl p-6 md:p-8 mb-12">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold mb-2">Presseanfragen</h2>
                <p className="text-blue-100">
                  Für Medienanfragen, Interviews oder Bildmaterial kontaktieren Sie uns gerne.
                </p>
              </div>
              <a 
                href="mailto:presse@domulex.ai" 
                className="inline-flex items-center justify-center px-6 py-3 bg-white text-[#1e3a5f] font-semibold rounded-lg hover:bg-gray-100 transition-colors"
              >
                ✉️ presse@domulex.ai
              </a>
            </div>
          </div>

          {/* Articles Grid */}
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Aktuelle Veröffentlichungen
            </h2>
            
            {pressArticles.length === 0 ? (
              <div className="text-center py-12 bg-gray-50 rounded-xl">
                <p className="text-gray-500">Noch keine Presseartikel verfügbar.</p>
              </div>
            ) : (
              <div className="grid gap-6">
                {pressArticles.map((article) => (
                  <a
                    key={article.id}
                    href={article.articleUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block bg-white rounded-xl shadow-md hover:shadow-lg transition-all border border-gray-100 overflow-hidden group"
                  >
                    <div className="p-6 md:p-8">
                      <div className="flex flex-col md:flex-row md:items-start gap-4">
                        {/* Content */}
                        <div className="flex-1">
                          <div className="flex flex-wrap items-center gap-2 mb-3">
                            <span className="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                              {article.type}
                            </span>
                            <span className="text-sm text-gray-500">
                              {formatDate(article.publishedAt)}
                            </span>
                          </div>
                          
                          <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-[#1e3a5f] transition-colors">
                            {article.title}
                          </h3>
                          
                          <p className="text-gray-600 mb-4">
                            {article.excerpt}
                          </p>
                          
                          <div className="flex items-center gap-2 text-sm">
                            <span className="font-medium text-gray-700">Quelle:</span>
                            <span className="text-[#1e3a5f] font-semibold">{article.source}</span>
                            <span className="text-gray-400">→</span>
                            <span className="text-blue-600 group-hover:underline">Artikel lesen</span>
                          </div>
                        </div>
                        
                        {/* External Link Icon */}
                        <div className="hidden md:flex items-center justify-center w-12 h-12 bg-gray-100 rounded-full group-hover:bg-[#1e3a5f] transition-colors">
                          <svg className="w-5 h-5 text-gray-500 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                          </svg>
                        </div>
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>

          {/* Pressematerial Section */}
          <div className="mt-16 bg-gray-50 rounded-2xl p-6 md:p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              📁 Pressematerial
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-2">🖼️ Logo & Bildmaterial</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Offizielle Logos und Grafiken für redaktionelle Verwendung.
                </p>
                <a 
                  href="mailto:presse@domulex.ai?subject=Anfrage%20Pressematerial"
                  className="text-[#1e3a5f] font-medium hover:underline"
                >
                  Auf Anfrage verfügbar →
                </a>
              </div>
              <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h3 className="font-semibold text-gray-900 mb-2">📄 Pressemitteilungen</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Aktuelle Pressemitteilungen als PDF zum Download.
                </p>
                <a 
                  href="mailto:presse@domulex.ai?subject=Anfrage%20Pressemitteilungen"
                  className="text-[#1e3a5f] font-medium hover:underline"
                >
                  Auf Anfrage verfügbar →
                </a>
              </div>
            </div>
          </div>

          {/* About Box */}
          <div className="mt-12 bg-white rounded-2xl p-6 md:p-8 border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Über <span className="text-[#1e3a5f]">domulex</span><span className="text-[#b8860b]">.ai</span>
            </h2>
            <p className="text-gray-600 mb-4">
              <span className="text-[#1e3a5f] font-semibold">domulex</span><span className="text-[#b8860b] font-semibold">.ai</span> ist die KI-gestützte Rechtsplattform für Immobilienrecht. 
              Entwickelt für Vermieter, Mieter, Hausverwaltungen, Rechtsanwälte und Immobilieninvestoren, die schnelle 
              und fundierte Antworten auf mietrechtliche Fragestellungen benötigen. Die Plattform liefert präzise Rechtsanalysen 
              zu Mietrecht, WEG-Recht, Nebenkostenabrechnungen und Immobiliensteuerrecht – basierend auf über 50.000 Fachquellen.
            </p>
            <p className="text-gray-600">
              <strong>Gründung:</strong> 2025 &nbsp;|&nbsp; 
              <strong>Gründer:</strong> Konstantin Kranich (Jurist)
            </p>
          </div>

          {/* Back Link */}
          <div className="mt-12 text-center">
            <Link 
              href="/"
              className="inline-flex items-center text-[#1e3a5f] font-medium hover:underline"
            >
              ← Zurück zur Startseite
            </Link>
          </div>

        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
