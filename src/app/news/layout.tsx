import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Immobilienrecht News & Urteile 2026 | domulex.ai',
  description: 'Aktuelle News zu Immobilienrecht: BGH-Urteile, Gesetzesänderungen, Mietrecht, WEG-Recht und Steuerrecht. Juristische Analysen für Vermieter, Eigentümer und Investoren.',
  keywords: ['Immobilienrecht', 'News', 'BGH Urteile', 'Mietrecht', 'WEG-Recht', 'Grundsteuer', 'Heizungsgesetz', 'GEG', 'Vermieter', '2026'],
  alternates: {
    canonical: 'https://domulex.ai/news',
  },
  openGraph: {
    title: 'Immobilienrecht News & Urteile 2026 | domulex.ai',
    description: 'Aktuelle Urteile, Gesetzesänderungen und juristische Analysen für Immobilien-Profis.',
    url: 'https://domulex.ai/news',
    siteName: 'domulex.ai',
    locale: 'de_DE',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Immobilienrecht News 2026 | domulex.ai',
    description: 'Aktuelle Urteile und Gesetzesänderungen im Immobilienrecht.',
  },
};

export default function NewsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
