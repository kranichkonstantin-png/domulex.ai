'use client';

import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';

export default function ImpressumPage() {
  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Header */}
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

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 pt-32 pb-12">
        <div className="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm">
          <h1 className="text-3xl font-bold text-[#1e3a5f] mb-8">Impressum</h1>
          
          <div className="prose max-w-none space-y-6 text-gray-700">
            
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Angaben gemäß § 5 DDG</h2>
              <p className="leading-relaxed">
                <strong className="text-[#1e3a5f]">Home Invest & Management GmbH</strong><br />
                Zur Maate 19<br />
                31515 Wunstorf<br />
                Deutschland
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Vertreten durch</h2>
              <p>
                Geschäftsführer: Konstantin Kranich
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Handelsregister</h2>
              <p>
                Registergericht: Amtsgericht Hannover<br />
                Registernummer: HRB 220181
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Umsatzsteuer-ID</h2>
              <p>
                Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz:<br />
                <strong className="text-[#1e3a5f]">DE361149434</strong>
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Kontakt</h2>
              <p>
                E-Mail: <a href="mailto:kontakt@domulex.ai" className="text-[#1e3a5f] hover:text-[#2d4a6f]">kontakt@domulex.ai</a>
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
              <p>
                Konstantin Kranich<br />
                Zur Maate 19<br />
                31515 Wunstorf
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Streitbeilegung</h2>
              <p>
                Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer 
                Verbraucherschlichtungsstelle teilzunehmen.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Haftung für Inhalte</h2>
              <p>
                Als Diensteanbieter sind wir gemäß § 7 Abs.1 DDG für eigene Inhalte auf diesen Seiten nach den 
                allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG sind wir als Diensteanbieter jedoch nicht 
                verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen 
                zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen.
              </p>
              <p className="mt-2">
                Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen 
                Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt 
                der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden von entsprechenden 
                Rechtsverletzungen werden wir diese Inhalte umgehend entfernen.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Haftung für Links</h2>
              <p>
                Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. 
                Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der 
                verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Die 
                verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft. 
                Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Urheberrecht</h2>
              <p>
                Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem 
                deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung 
                außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen 
                Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den privaten, nicht 
                kommerziellen Gebrauch gestattet.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">Hinweis zur KI-Nutzung</h2>
              <p>
                domulex.ai ist eine KI-gestützte Plattform für Immobilienrecht. Die bereitgestellten Informationen 
                dienen ausschließlich zu Informationszwecken und stellen keine Rechtsberatung dar. Für verbindliche 
                rechtliche Auskünfte wenden Sie sich bitte an einen zugelassenen Rechtsanwalt.
              </p>
            </section>

          </div>

          <div className="mt-8 pt-6 border-t border-gray-200 text-sm text-gray-500">
            Stand: Dezember 2025
          </div>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
