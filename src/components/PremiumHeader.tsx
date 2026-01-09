'use client';

import Link from 'next/link';
import Logo from '@/components/Logo';

interface PremiumHeaderProps {
  activePage?: 'funktionen' | 'preise' | 'news' | 'faq' | 'zielgruppen' | 'none';
}

export default function PremiumHeader({ activePage = 'none' }: PremiumHeaderProps) {
  const navItems = [
    { href: '/funktionen', label: 'Funktionen', key: 'funktionen' as const },
    { href: '/#zielgruppen', label: 'Für wen?', key: 'zielgruppen' as const },
    { href: '/preise', label: 'Preise', key: 'preise' as const },
    { href: '/news', label: 'News', key: 'news' as const },
    { href: '/faq', label: 'FAQ', key: 'faq' as const },
  ];

  return (
    <header>
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100/50 shadow-sm" aria-label="Hauptnavigation">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-[106px]">
            <Link href="/">
              <Logo size="sm" />
            </Link>
            {/* Desktop Navigation */}
            <ul className="hidden md:flex items-center gap-8" role="list">
              {navItems.map((item) => (
                <li key={item.key}>
                  {activePage === item.key ? (
                    <span className="text-[#1e3a5f] font-semibold border-b-2 border-[#b8860b] pb-1">
                      {item.label}
                    </span>
                  ) : (
                    <Link 
                      href={item.href} 
                      className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 rounded"
                    >
                      {item.label}
                    </Link>
                  )}
                </li>
              ))}
              <li>
                <Link 
                  href="/auth/login" 
                  className="group relative px-5 py-2.5 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] hover:from-[#2d4a6f] hover:to-[#1e3a5f] text-white rounded-xl font-medium transition-all duration-300 shadow-lg shadow-[#1e3a5f]/25 hover:shadow-xl hover:shadow-[#1e3a5f]/30 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2"
                >
                  Anmelden
                </Link>
              </li>
            </ul>
            {/* Mobile */}
            <Link 
              href="/auth/login" 
              className="md:hidden px-4 py-2 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] text-white rounded-xl font-medium text-sm shadow-lg shadow-[#1e3a5f]/25 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2"
            >
              Anmelden
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}
