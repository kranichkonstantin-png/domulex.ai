import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Hilfe & FAQ | domulex.ai - Immobilienrecht KI',
  description: 'Häufig gestellte Fragen zu domulex.ai: Tarife, Funktionen, Rechtsanalyse, Vertragsanalyse, Steuer-Optimierung. Support für Ihr Immobilienrecht-KI-Tool.',
  keywords: [
    'domulex hilfe',
    'domulex faq',
    'immobilienrecht fragen',
    'mietrecht hilfe',
    'weg-recht fragen',
    'ki rechtsberatung',
    'vertragsanalyse faq',
    'steuer immobilien fragen',
    'bgh urteile suchen',
    'rechts-ki deutschland'
  ],
  openGraph: {
    title: 'Hilfe & FAQ | domulex.ai',
    description: 'Antworten auf alle Fragen zu domulex.ai - Ihrer KI-Plattform für deutsches Immobilienrecht.',
    url: 'https://domulex.ai/hilfe',
    siteName: 'domulex.ai',
    locale: 'de_DE',
    type: 'website',
  },
  alternates: {
    canonical: 'https://domulex.ai/hilfe',
  },
};

// JSON-LD FAQ Schema für bessere SEO
const faqSchema = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Was bietet domulex.ai?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "domulex.ai ist Ihre KI-Plattform für deutsches Immobilienrecht. Wir analysieren Ihren individuellen Fall basierend auf über 50.000 Rechtsdokumenten: Mietrecht (BGB §§535-580a), WEG-Recht, Baurecht, Maklerrecht und Immobiliensteuerrecht."
      }
    },
    {
      "@type": "Question", 
      "name": "Welche Tarife bietet domulex.ai?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "domulex.ai bietet drei Tarife: Basis (19€/Monat, 50 Anfragen), Professional (39€/Monat, 250 Anfragen) und Lawyer Pro (69€/Monat, unbegrenzte Anfragen für Rechtsanwälte). Ein kostenloser Test mit 3 Anfragen ist verfügbar."
      }
    },
    {
      "@type": "Question",
      "name": "Kann domulex.ai bei Steuerfragen helfen?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ja! Unsere Datenbank enthält über 100 BFH-Urteile und BMF-Schreiben zum Immobiliensteuerrecht: AfA-Berechnung, Spekulationsfrist (10 Jahre), Grunderwerbsteuer und Werbungskosten bei Vermietung."
      }
    },
    {
      "@type": "Question",
      "name": "Was leistet die Vertragsanalyse?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Die Vertragsanalyse prüft Miet- und Kaufverträge auf unwirksame Klauseln (z.B. Schönheitsreparaturen), fehlende Pflichtangaben, versteckte Risiken und Abweichungen vom Standard."
      }
    },
    {
      "@type": "Question",
      "name": "Wie werden meine Daten geschützt?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "domulex.ai ist DSGVO-konform mit Serverstandort Deutschland, Zero Data Retention (Chat-Inhalte werden nicht dauerhaft gespeichert) und SSL-Verschlüsselung."
      }
    },
    {
      "@type": "Question",
      "name": "Was ist Lawyer Pro?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Lawyer Pro (69€/Monat) ist unser Tarif für Juristen: Unbegrenzte Anfragen, Mandanten-CRM mit KI-Aktenführung, Schriftsatzgenerierung, erweiterte Quellenfilter und 50.000+ Rechtsquellen."
      }
    }
  ]
};

export default function HilfeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      {children}
    </>
  );
}
