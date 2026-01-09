import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Gründer-Story: Konstantin Kranich | domulex.ai',
  description: 'Die Geschichte hinter domulex.ai: Jurist Konstantin Kranich erklärt, warum er eine KI-Plattform für Immobilienrecht entwickelt hat. Von der Idee zum Legal Tech Startup.',
  keywords: ['Gründer', 'Startup', 'Legal Tech', 'Konstantin Kranich', 'Immobilienrecht', 'KI', 'domulex.ai', 'PropTech'],
  alternates: {
    canonical: 'https://domulex.ai/gruender',
  },
  openGraph: {
    title: 'Gründer-Story: Konstantin Kranich | domulex.ai',
    description: 'Die Geschichte hinter domulex.ai – Jurist Konstantin Kranich und seine Vision für Legal Tech im Immobilienrecht.',
    url: 'https://domulex.ai/gruender',
    siteName: 'domulex.ai',
    locale: 'de_DE',
    type: 'profile',
    images: [
      {
        url: 'https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/gruender.jpeg?alt=media',
        width: 1200,
        height: 630,
        alt: 'Konstantin Kranich - Gründer domulex.ai',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Gründer-Story: Konstantin Kranich | domulex.ai',
    description: 'Die Geschichte hinter domulex.ai – von der Idee zum Legal Tech Startup.',
  },
};

export default function GruenderPage() {
  return (
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
              <Link href="/news" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">News</Link>
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

      <main className="max-w-3xl mx-auto px-4 sm:px-6 pt-36 pb-16">
        {/* Hero */}
        <header className="text-center mb-12">
          <div className="w-24 h-24 bg-gradient-to-br from-[#1e3a5f] to-[#3d5a7f] rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6">
            KK
          </div>
          <h1 className="text-4xl font-bold text-[#1e3a5f] mb-2">
            Gründer-Story
          </h1>
          <p className="text-lg text-gray-500">
            Die Vision hinter domulex.ai
          </p>
        </header>

        {/* Content */}
        <article className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 md:p-12">
          <div className="prose prose-lg max-w-none">
            <p className="text-xl text-[#1e3a5f] font-medium leading-relaxed">
              Herzlich willkommen,
            </p>
            
            <p className="text-gray-700 leading-relaxed">
              mein Name ist <strong>Konstantin Kranich</strong>. Ich bin Jurist, Gründer von domulex.ai – aber im Herzen bleibe ich Praktiker.
            </p>

            <div className="my-8 p-6 bg-gradient-to-r from-blue-50 to-amber-50 rounded-xl border-l-4 border-[#c9a227]">
              <p className="text-gray-700 leading-relaxed m-0">
                Als Jurist kenne ich den enormen Druck, unter dem wir arbeiten: Das Haftungsrisiko bei jeder Auskunft, die komplexen Fristenkalender und der Anspruch, fehlerfreie Schriftsätze zu liefern. Gleichzeitig bin ich als Immobilieninvestor und Entwickler auf der anderen Seite tätig und weiß, wie sehr die Immobilienwirtschaft unter ineffizienten rechtlichen Prozessen leidet.
              </p>
            </div>

            <p className="text-gray-700 leading-relaxed">
              Ich habe domulex.ai entwickelt, weil die bestehenden Lösungen für Kanzleien oft veraltet und starre „Insellösungen" waren.
            </p>

            <p className="text-gray-700 leading-relaxed">
              Mein Anspruch war eine <strong>High-End-Plattform</strong>, die den tiefen fachlichen Anforderungen von Juristen genügt, aber so intuitiv ist, dass auch Immobilienprofis damit arbeiten können.
            </p>

            <h2 className="text-2xl font-bold text-[#1e3a5f] mt-10 mb-6 flex items-center gap-3">
              <span className="text-3xl">🎯</span>
              Unsere Philosophie: Ein Tool, verschiedene Flughöhen.
            </h2>

            {/* Lawyer Pro */}
            <div className="my-8 p-6 bg-[#1e3a5f] rounded-xl text-white">
              <h3 className="text-xl font-bold text-[#c9a227] mb-3 flex items-center gap-2">
                <span>⚖️</span> Für meine Kollegen aus der Rechtsberatung (Lawyer Pro)
              </h3>
              <p className="text-gray-200 leading-relaxed m-0">
                Wir haben eine komplette Kanzlei-Suite gebaut. CRM, Fristenmanagement und eine KI, die <em>wirklich</em> juristisch arbeitet. Sie schreibt Klageschriften, prüft Verträge auf Risiken und liefert Quellen – <strong>ohne Halluzinationen</strong>. Es ist das Werkzeug, das ich mir für meine eigene Arbeit immer gewünscht habe.
              </p>
            </div>

            {/* Immobilien-Profis */}
            <div className="my-8 p-6 bg-amber-50 rounded-xl border border-amber-100">
              <h3 className="text-xl font-bold text-[#1e3a5f] mb-3 flex items-center gap-2">
                <span>🏢</span> Für Immobilien-Profis, Entwickler & Verwalter
              </h3>
              <p className="text-gray-700 leading-relaxed m-0">
                Sie profitieren von derselben mächtigen Technologie. Wir automatisieren Ihre Standardprozesse (wie Nebenkosten oder Mietverträge), damit Sie rechtssicher agieren, ohne für jede Frage ein Mandat eröffnen zu müssen.
              </p>
            </div>

            {/* Eigentümer & Mieter */}
            <div className="my-8 p-6 bg-green-50 rounded-xl border border-green-100">
              <h3 className="text-xl font-bold text-[#1e3a5f] mb-3 flex items-center gap-2">
                <span>🏠</span> Für Eigentümer & Mieter
              </h3>
              <p className="text-gray-700 leading-relaxed m-0">
                Wir demokratisieren den Zugang zum Recht, indem wir komplexe Fragen einfach und verlässlich beantworten.
              </p>
            </div>

            {/* Call to Action */}
            <div className="my-10 text-center p-8 bg-gradient-to-br from-[#1e3a5f] to-[#2d4a6f] rounded-2xl text-white">
              <p className="text-lg leading-relaxed mb-6">
                Ich lade Sie ein – ob als Anwaltskollege oder Immobilienunternehmer – die Arbeit mit domulex.ai zu testen. 
              </p>
              <p className="text-xl font-semibold text-[#c9a227] mb-6">
                Es ist Zeit, dass unsere Werkzeuge so professionell werden wie unsere Arbeit.
              </p>
              <Link 
                href="/auth/register" 
                className="inline-block px-8 py-3 bg-[#c9a227] hover:bg-[#b8922c] text-white font-semibold rounded-lg transition-colors"
              >
                Jetzt kostenlos testen
              </Link>
            </div>

            {/* Signature */}
            <div className="mt-10 pt-8 border-t border-gray-200">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-[#1e3a5f] to-[#3d5a7f] rounded-full flex items-center justify-center text-white text-xl font-bold flex-shrink-0">
                  KK
                </div>
                <div>
                  <p className="text-gray-600 mb-1">Ihr</p>
                  <p className="text-xl font-bold text-[#1e3a5f]">Konstantin Kranich</p>
                  <p className="text-sm text-[#c9a227] font-medium">Jurist & Immobilieninvestor</p>
                </div>
              </div>
            </div>
          </div>
        </article>

        {/* Links */}
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          <Link 
            href="/redaktion" 
            className="px-6 py-3 bg-white border border-gray-200 hover:border-[#1e3a5f] text-[#1e3a5f] rounded-lg font-medium transition-colors"
          >
            Zur Redaktion →
          </Link>
          <Link 
            href="/news" 
            className="px-6 py-3 bg-white border border-gray-200 hover:border-[#1e3a5f] text-[#1e3a5f] rounded-lg font-medium transition-colors"
          >
            Aktuelle News →
          </Link>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
