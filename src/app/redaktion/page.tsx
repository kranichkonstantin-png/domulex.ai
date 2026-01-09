import Link from 'next/link';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Redaktion & Autoren | domulex.ai - Immobilienrecht KI',
  description: 'Das Redaktionsteam von domulex.ai: Jurist Konstantin Kranich und Experten für deutsches Immobilienrecht. E-E-A-T-konforme Inhalte mit 50.000+ Rechtsquellen.',
  keywords: ['Redaktion', 'Autoren', 'Immobilienrecht', 'Jurist', 'Legal Tech', 'Konstantin Kranich', 'domulex.ai'],
  alternates: {
    canonical: 'https://domulex.ai/redaktion',
  },
  openGraph: {
    title: 'Redaktion & Autoren | domulex.ai',
    description: 'Das Redaktionsteam von domulex.ai: Jurist Konstantin Kranich - Experte für deutsches Immobilienrecht und Legal Tech.',
    url: 'https://domulex.ai/redaktion',
    siteName: 'domulex.ai',
    locale: 'de_DE',
    type: 'profile',
  },
  twitter: {
    card: 'summary',
    title: 'Redaktion & Autoren | domulex.ai',
    description: 'Das Redaktionsteam von domulex.ai: Jurist Konstantin Kranich - Experte für Immobilienrecht.',
  },
};

const teamMembers = [
  {
    id: 'konstantin-kranich',
    name: 'Konstantin Kranich',
    role: 'Gründer & CEO',
    title: 'Jurist | Legal Tech Spezialist',
    image: null,
    initials: 'KK',
    bio: `Konstantin Kranich verbindet juristische Expertise mit technologischer Innovation. Nach mehrjähriger Tätigkeit in der Immobilienwirtschaft und juristischen Beratung erkannte er das enorme Potenzial von KI für die Rechtspraxis – und gründete domulex.ai.

Seine Karriere führte ihn von klassischer Immobilienberatung über Investmentanalysen bis hin zur Entwicklung KI-gestützter Rechtslösungen. Als Legal Tech Spezialist treibt er die Automatisierung juristischer Prozesse voran und macht professionelle Rechtsanalyse für jeden zugänglich.

Mit domulex.ai revolutioniert er die Art, wie Juristen, Vermieter, Investoren und Immobilienprofis rechtliche Fragen klären – schnell, präzise und rund um die Uhr verfügbar.`,
    expertise: [
      'Immobilienrecht (Miet-, WEG-, Maklerrecht)',
      'Immobilieninvestment & Portfolioanalyse',
      'KI-Prozessoptimierung & Automatisierung',
      'Legal Tech & PropTech',
      'Vertragsanalyse & Due Diligence'
    ],
    credentials: [
      'Jurist',
      'Legal Tech & AI Spezialist',
      'Immobilieninvestor',
      'Gründer domulex.ai'
    ],
    social: {
      email: 'k.kranich@domulex.ai'
    }
  }
];

// Schema.org für Redaktionsseite (E-E-A-T)
const jsonLdOrganization = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'domulex.ai',
  url: 'https://domulex.ai',
  logo: 'https://domulex.ai/logo.png',
  description: 'KI-gestützte Rechtsplattform für deutsches Immobilienrecht',
  foundingDate: '2024',
  founder: {
    '@type': 'Person',
    name: 'Konstantin Kranich',
    jobTitle: 'Jurist & Gründer',
    url: 'https://domulex.ai/gruender'
  },
  address: {
    '@type': 'PostalAddress',
    addressCountry: 'DE'
  }
};

const jsonLdPerson = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: 'Konstantin Kranich',
  jobTitle: 'Jurist & Gründer',
  url: 'https://domulex.ai/redaktion#konstantin-kranich',
  worksFor: {
    '@type': 'Organization',
    name: 'domulex.ai',
    url: 'https://domulex.ai'
  },
  knowsAbout: ['Immobilienrecht', 'Mietrecht', 'WEG-Recht', 'Legal Tech', 'KI']
};

export default function RedaktionPage() {
  return (
    <>
      {/* Schema.org JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdOrganization) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdPerson) }}
      />
      
    <div className="min-h-screen bg-[#fafaf8]">
      <PremiumHeader />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 pt-36 pb-12">
        {/* Hero */}
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-[#1e3a5f] mb-4">
            Unsere Redaktion
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            domulex.ai vereint juristische Kompetenz im Immobilienrecht mit modernster KI-Technologie – 
            für schnelle, fundierte Antworten auf Ihre Rechtsfragen.
          </p>
        </header>

        {/* Redaktionsbild */}
        <div className="mb-16 flex justify-center">
          <div className="relative max-w-3xl w-full">
            <div className="absolute -inset-4 bg-gradient-to-br from-[#1e3a5f]/10 to-[#c9a227]/10 rounded-3xl blur-xl"></div>
            <img 
              src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/redaktion.jpeg?alt=media&token=898b7ff6-ee67-45ee-9858-7d687e0d915a"
              alt="domulex.ai Redaktion - Juristische Expertise trifft KI-Technologie für Immobilienrecht"
              className="relative w-full rounded-2xl shadow-xl border border-gray-100"
              loading="eager"
            />
          </div>
        </div>

        {/* Redaktionelle Standards */}
        <section className="mb-16">
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
            <h2 className="text-2xl font-bold text-[#1e3a5f] mb-6">
              Unsere redaktionellen Standards
            </h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">⚖️</span>
                </div>
                <div>
                  <h3 className="font-semibold text-[#1e3a5f] mb-1">Juristische Expertise</h3>
                  <p className="text-sm text-gray-600">
                    Alle Inhalte werden von Juristen mit Expertise im Immobilienrecht erstellt und geprüft.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">📚</span>
                </div>
                <div>
                  <h3 className="font-semibold text-[#1e3a5f] mb-1">Quellenbasiert</h3>
                  <p className="text-sm text-gray-600">
                    Unsere Analysen basieren auf BGH-Urteilen, Gesetzen und anerkannter Fachliteratur.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">🔄</span>
                </div>
                <div>
                  <h3 className="font-semibold text-[#1e3a5f] mb-1">Aktualität</h3>
                  <p className="text-sm text-gray-600">
                    Wir aktualisieren unsere Inhalte bei Gesetzesänderungen und neuer Rechtsprechung.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">🎯</span>
                </div>
                <div>
                  <h3 className="font-semibold text-[#1e3a5f] mb-1">Praxisnähe</h3>
                  <p className="text-sm text-gray-600">
                    Wir übersetzen komplexes Recht in verständliche, handlungsorientierte Informationen.
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-8 p-4 bg-blue-50 rounded-xl">
              <h4 className="font-semibold text-[#1e3a5f] mb-2">Unser Qualitätsprozess</h4>
              <ol className="text-sm text-gray-600 space-y-2">
                <li className="flex gap-2">
                  <span className="font-semibold text-blue-600">1.</span>
                  Recherche in Primärquellen (Gesetze, Urteile, Kommentare)
                </li>
                <li className="flex gap-2">
                  <span className="font-semibold text-blue-600">2.</span>
                  Erstellung durch Juristen mit praktischer Immobilien-Erfahrung
                </li>
                <li className="flex gap-2">
                  <span className="font-semibold text-blue-600">3.</span>
                  KI-gestützte Qualitätskontrolle und Plausibilitätsprüfung
                </li>
                <li className="flex gap-2">
                  <span className="font-semibold text-blue-600">4.</span>
                  Kontinuierliche Überwachung auf Gesetzesänderungen
                </li>
              </ol>
            </div>
          </div>
        </section>

        {/* Verantwortlicher Redakteur */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-[#1e3a5f] mb-8 text-center">
            Verantwortlicher Redakteur
          </h2>
          
          {teamMembers.map((member) => (
            <div 
              key={member.id} 
              id={member.id}
              className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 scroll-mt-24"
            >
              <div className="flex flex-col md:flex-row gap-6">
                {/* Foto */}
                <div className="flex-shrink-0">
                  <img 
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/redakteur.jpeg?alt=media&token=e9ace397-f255-44ee-9138-f08cd9ccd0a6"
                    alt={member.name}
                    className="w-32 h-32 rounded-2xl object-cover shadow-md mx-auto md:mx-0"
                  />
                </div>

                {/* Info */}
                <div className="flex-1">
                  <div className="mb-4">
                    <h3 className="text-2xl font-bold text-[#1e3a5f]">{member.name}</h3>
                    <p className="text-lg text-gray-600">{member.role}</p>
                    <p className="text-sm text-blue-600 font-medium">{member.title}</p>
                  </div>

                  <div className="prose prose-sm max-w-none text-gray-600 mb-6">
                    {member.bio.split('\n\n').map((paragraph, i) => (
                      <p key={i}>{paragraph}</p>
                    ))}
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    {/* Expertise */}
                    <div>
                      <h4 className="font-semibold text-[#1e3a5f] mb-2">Fachgebiete</h4>
                      <ul className="space-y-1">
                        {member.expertise.map((item) => (
                          <li key={item} className="text-sm text-gray-600 flex items-center gap-2">
                            <span className="text-green-500">✓</span> {item}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Credentials */}
                    <div>
                      <h4 className="font-semibold text-[#1e3a5f] mb-2">Qualifikationen</h4>
                      <ul className="space-y-1">
                        {member.credentials.map((item) => (
                          <li key={item} className="text-sm text-gray-600 flex items-center gap-2">
                            <span className="text-blue-500">•</span> {item}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Social Links */}
                  <div className="mt-6 flex gap-4">
                    {member.social.email && (
                      <a 
                        href={`mailto:${member.social.email}`}
                        className="text-gray-400 hover:text-blue-600 transition-colors"
                        aria-label="E-Mail senden"
                      >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* Kontakt */}
        <section>
          <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] rounded-2xl p-8 text-center">
            <h2 className="text-2xl font-bold text-white mb-4">
              Kontakt zur Redaktion
            </h2>
            <p className="text-blue-100 mb-6 max-w-lg mx-auto">
              Haben Sie Fragen zu unseren Inhalten oder möchten Sie auf einen Fehler hinweisen? 
              Wir freuen uns über Ihre Nachricht.
            </p>
            <a
              href="mailto:redaktion@domulex.ai"
              className="inline-block px-6 py-3 bg-white text-[#1e3a5f] font-semibold rounded-lg hover:bg-gray-100 transition-colors"
            >
              redaktion@domulex.ai
            </a>
          </div>
        </section>
      </main>

      <PremiumFooter />
    </div>
    </>
  );
}
