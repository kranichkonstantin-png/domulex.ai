import { MetadataRoute } from 'next';

// Für static export
export const dynamic = 'force-static';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/api/',
          '/admin/',
          '/auth/',
          '/konto/',
          '/dashboard/',
          '/app/',
          '/_next/',
        ],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        disallow: [
          '/api/',
          '/admin/',
          '/auth/',
          '/konto/',
          '/dashboard/',
          '/app/',
        ],
      },
      {
        userAgent: 'Googlebot-News',
        allow: '/news/',
      },
    ],
    sitemap: 'https://domulex.ai/sitemap.xml',
    host: 'https://domulex.ai',
  };
}
