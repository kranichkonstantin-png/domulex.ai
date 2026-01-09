import { MetadataRoute } from 'next';

// Für static export
export const dynamic = 'force-static';

// News-Artikel Slugs (muss mit news/[slug]/page.tsx synchron gehalten werden)
const newsArticleSlugs = [
  'co2-kostenaufteilung-abrechnung-2026-107',
  'heizungsgesetz-2026-was-vermieter-wissen-muessen-101',
  'bgh-urteil-indexmiete-januar-2026-102',
  'grundsteuer-reform-2026-berechnung-103',
  'mietpreisbremse-verlaengerung-2026-104',
  'weg-reform-2026-digitale-eigentuemerversammlung-105',
  'energieausweis-pflicht-2026-bussgelder-106',
];

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://domulex.ai';
  const currentDate = new Date().toISOString();

  // Hauptseiten
  const mainPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: currentDate,
      changeFrequency: 'weekly',
      priority: 1.0,
    },
    {
      url: `${baseUrl}/news`,
      lastModified: currentDate,
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/faq`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${baseUrl}/redaktion`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${baseUrl}/gruender`,
      lastModified: currentDate,
      changeFrequency: 'monthly',
      priority: 0.6,
    },
    {
      url: `${baseUrl}/impressum`,
      lastModified: currentDate,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/datenschutz`,
      lastModified: currentDate,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/agb`,
      lastModified: currentDate,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
  ];

  // News-Artikel dynamisch hinzufügen
  const newsPages: MetadataRoute.Sitemap = newsArticleSlugs.map((slug) => ({
    url: `${baseUrl}/news/${slug}`,
    lastModified: currentDate,
    changeFrequency: 'monthly' as const,
    priority: 0.8,
  }));

  return [...mainPages, ...newsPages];
}
