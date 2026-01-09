import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'FAQ - Häufige Fragen | domulex.ai Immobilienrecht KI',
  description: 'Häufig gestellte Fragen zu domulex.ai: Rechtsquellen, Datenbank, Tarife, Datenschutz und Funktionen. Alles über unsere KI-Plattform für Immobilienrecht.',
  keywords: ['FAQ', 'Häufige Fragen', 'Immobilienrecht', 'KI', 'Rechtsquellen', 'Tarife', 'domulex.ai', 'Mietrecht', 'WEG'],
  alternates: {
    canonical: 'https://domulex.ai/faq',
  },
  openGraph: {
    title: 'FAQ - Häufige Fragen | domulex.ai',
    description: 'Antworten auf häufig gestellte Fragen zu domulex.ai: Rechtsquellen, Funktionen, Tarife und Datenschutz.',
    url: 'https://domulex.ai/faq',
    siteName: 'domulex.ai',
    locale: 'de_DE',
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'FAQ | domulex.ai',
    description: 'Häufig gestellte Fragen zu domulex.ai - KI für Immobilienrecht.',
  },
};

export default function FAQLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
