import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  // Basis SEO
  title: {
    default: "domulex.ai – KI-Rechtsassistent für Immobilienrecht | Mietrecht, Steuer, WEG",
    template: "%s | domulex.ai"
  },
  description: "Effiziente Rechtsanalyse im Immobilienbereich durch moderne KI. Sofortige Antworten zu Mietrecht, WEG, Nebenkosten, Steuern & Verträgen – basierend auf 50.000+ Rechtsquellen. Entwickelt von Juristen.",
  keywords: [
    "Immobilienrecht", "Mietrecht", "KI Rechtsberatung", "Nebenkostenabrechnung", 
    "WEG Recht", "Vermieter", "Mieter", "Hausverwaltung", "Immobilien Steuer",
    "AfA Rechner", "Mieterhöhung", "Kündigungsschreiben", "BGH Urteile",
    "Legal Tech", "Rechtsassistent", "domulex"
  ],
  authors: [{ name: "Konstantin Kranich", url: "https://domulex.ai/redaktion" }],
  creator: "Home Invest & Management GmbH",
  publisher: "domulex.ai",
  
  // Canonical & Robots
  metadataBase: new URL("https://domulex.ai"),
  alternates: {
    canonical: "https://domulex.ai"
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1
    }
  },
  
  // Open Graph (Facebook, LinkedIn)
  openGraph: {
    type: "website",
    locale: "de_DE",
    url: "https://domulex.ai",
    siteName: "domulex.ai",
    title: "domulex.ai – KI-Rechtsassistent für Immobilienrecht",
    description: "Sofortige Antworten zu Mietrecht, WEG, Nebenkosten & Steuern. 50.000+ Rechtsquellen, entwickelt von Juristen.",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "domulex.ai - KI für Immobilienrecht"
      }
    ]
  },
  
  // Twitter Card
  twitter: {
    card: "summary_large_image",
    title: "domulex.ai – KI-Rechtsassistent für Immobilienrecht",
    description: "Sofortige Antworten zu Mietrecht, WEG, Nebenkosten & Steuern. Entwickelt von Juristen.",
    images: ["/og-image.jpg"],
    creator: "@domulex_ai"
  },
  
  // App & Icons
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "domulex.ai"
  },
  icons: {
    icon: [
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" }
    ],
    apple: [
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" }
    ]
  },
  
  // Verification (optional - später eintragen)
  // verification: {
  //   google: "YOUR_GOOGLE_VERIFICATION_CODE",
  // },
  
  // Kategorie
  category: "Legal Technology"
};

// JSON-LD Structured Data für Organization & WebSite
const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'Organization',
      '@id': 'https://domulex.ai/#organization',
      name: 'domulex.ai',
      alternateName: 'Home Invest & Management GmbH',
      url: 'https://domulex.ai',
      logo: {
        '@type': 'ImageObject',
        url: 'https://domulex.ai/logo.png',
        width: 512,
        height: 512
      },
      sameAs: [
        'https://linkedin.com/company/domulex'
      ],
      contactPoint: {
        '@type': 'ContactPoint',
        email: 'kontakt@domulex.ai',
        contactType: 'customer service',
        availableLanguage: 'German'
      },
      founder: {
        '@type': 'Person',
        name: 'Konstantin Kranich',
        jobTitle: 'Jurist & Gründer'
      },
      address: {
        '@type': 'PostalAddress',
        addressLocality: 'Wunstorf',
        addressCountry: 'DE'
      }
    },
    {
      '@type': 'WebSite',
      '@id': 'https://domulex.ai/#website',
      url: 'https://domulex.ai',
      name: 'domulex.ai',
      description: 'KI-Rechtsassistent für Immobilienrecht',
      publisher: { '@id': 'https://domulex.ai/#organization' },
      inLanguage: 'de-DE',
      potentialAction: {
        '@type': 'SearchAction',
        target: 'https://domulex.ai/dashboard?q={search_term_string}',
        'query-input': 'required name=search_term_string'
      }
    },
    {
      '@type': 'SoftwareApplication',
      '@id': 'https://domulex.ai/#app',
      name: 'domulex.ai',
      applicationCategory: 'LegalService',
      operatingSystem: 'Web',
      offers: [
        {
          '@type': 'Offer',
          name: 'Basis',
          price: '19.00',
          priceCurrency: 'EUR',
          priceValidUntil: '2026-12-31',
          availability: 'https://schema.org/InStock'
        },
        {
          '@type': 'Offer',
          name: 'Professional',
          price: '39.00',
          priceCurrency: 'EUR',
          priceValidUntil: '2026-12-31',
          availability: 'https://schema.org/InStock'
        },
        {
          '@type': 'Offer',
          name: 'Lawyer Pro',
          price: '69.00',
          priceCurrency: 'EUR',
          priceValidUntil: '2026-12-31',
          availability: 'https://schema.org/InStock'
        }
      ],
      aggregateRating: {
        '@type': 'AggregateRating',
        ratingValue: '4.8',
        reviewCount: '127',
        bestRating: '5',
        worstRating: '1'
      }
    }
  ]
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="de">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
