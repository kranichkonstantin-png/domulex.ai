'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/firebase';
import { onAuthStateChanged } from 'firebase/auth';
import CheckoutModal from '@/components/CheckoutModal';
import Image from 'next/image';
import Logo from '@/components/Logo';
import CookieConsent from '@/components/CookieConsent';

export default function LandingPage() {
  const router = useRouter();
  const [showCheckout, setShowCheckout] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<any>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [lightboxImage, setLightboxImage] = useState<{src: string; alt: string; title: string} | null>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setIsLoggedIn(!!user);
    });
    return () => unsubscribe();
  }, []);

  // ESC-Taste zum Schließen der Lightbox
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setLightboxImage(null);
    };
    if (lightboxImage) {
      document.addEventListener('keydown', handleEsc);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = '';
    };
  }, [lightboxImage]);

  const plans = {
    basis: {
      id: 'basis',
      name: 'Basis',
      price: 19,
      interval: 'monthly' as const,
      features: [
        '25 Anfragen pro Monat',
        '5.000 Rechtsquellen',
        'KI-Mietrecht-Check & WEG-Berater',
        'KI-Steuer-Assistent (AfA, Werbungskosten)',
        'KI-Musterbriefe & eigene Vorlagen erstellen',
        'KI-Nebenkostenprüfung mit Fehleranalyse'
      ]
    },
    professional: {
      id: 'professional',
      name: 'Professional',
      price: 39,
      interval: 'monthly' as const,
      features: [
        '250 Anfragen pro Monat',
        '50.000+ Rechtsquellen',
        'KI-Immobilienverwaltung (Mieter, Mahnwesen, Zähler)',
        'KI-Nebenkostenabrechnung (17 Kostenarten)',
        'KI-Renditerechner mit Cashflow-Prognose',
        'KI-Vertragsanalyse (Miet- & Kaufverträge)',
        'KI-Steuer-Optimierung & Spekulationsfrist',
        'KI-Baurecht-Assistent (VOB, Mängel)'
      ]
    },
    lawyer: {
      id: 'lawyer',
      name: 'Lawyer Pro',
      price: 69,
      interval: 'monthly' as const,
      features: [
        'Unbegrenzte Anfragen',
        '50.000+ Rechtsquellen-Datenbank',
        'KI-Mandanten-CRM mit Aktenführung',
        'KI-Fristenverwaltung & Wiedervorlagen',
        'KI-Schriftsatzgenerator (Klagen, Mahnungen)',
        'KI-Dokumentenmanagement & Suche',
        'KI-Fallanalyse (Erfolgsaussichten & Risiken)',
        'KI-Quellenfilter (Gesetze, Urteile, Literatur)',
        'KI-Vertragsanalyse mit Risikobewertung',
        'KI-Rechtsprechungsanalyse (BGH, OLG, LG)'
      ]
    }
  };

  const handleCheckout = (plan: typeof plans.basis) => {
    if (!isLoggedIn) {
      // Plan als URL-Parameter übergeben, um Bereichsauswahl zu überspringen
      router.push(`/auth/register?plan=${plan.id}`);
      return;
    }
    setSelectedPlan(plan);
    setShowCheckout(true);
  };

  const handleCheckoutConfirm = async (acceptedTerms: { agb: boolean; widerruf: boolean }) => {
    if (!selectedPlan || !isLoggedIn) return;

    try {
      const user = auth.currentUser;
      if (!user) {
        router.push('/auth/login');
        return;
      }

      const idToken = await user.getIdToken();

      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/stripe/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        },
        body: JSON.stringify({
          tier: selectedPlan.id,
          success_url: `${window.location.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: `${window.location.origin}/#pricing`
        })
      });

      if (!response.ok) {
        throw new Error('Checkout-Session konnte nicht erstellt werden');
      }

      const { checkout_url } = await response.json();
      window.location.href = checkout_url;
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Fehler beim Checkout. Bitte versuchen Sie es erneut.');
    } finally {
      setShowCheckout(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Skip-Link für Barrierefreiheit */}
      <a 
        href="#main-content" 
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-[#1e3a5f] focus:text-white focus:rounded-lg focus:outline-none focus:ring-2 focus:ring-[#b8860b]"
      >
        Zum Hauptinhalt springen
      </a>

      {/* Navigation - Premium & Seriös */}
      <header>
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100/50 shadow-sm" aria-label="Hauptnavigation">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-[106px]">
            <Logo size="sm" />
            {/* Desktop Navigation */}
            <ul className="hidden md:flex items-center gap-8" role="list">
              <li><Link href="/funktionen" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 rounded">Funktionen</Link></li>
              <li><a href="#zielgruppen" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 rounded">Für wen?</a></li>
              <li><Link href="/preise" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 rounded">Preise</Link></li>
              <li><Link href="/news" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 rounded">News</Link></li>
              <li><Link href="/faq" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-all duration-300 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 rounded">FAQ</Link></li>
              <li><Link href="/auth/login" className="group relative px-5 py-2.5 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] hover:from-[#2d4a6f] hover:to-[#1e3a5f] text-white rounded-xl font-medium transition-all duration-300 shadow-lg shadow-[#1e3a5f]/25 hover:shadow-xl hover:shadow-[#1e3a5f]/30 hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2">
                Anmelden
              </Link></li>
            </ul>
            {/* Mobile */}
            <Link href="/auth/login" className="md:hidden px-4 py-2 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] text-white rounded-xl font-medium text-sm shadow-lg shadow-[#1e3a5f]/25 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2">
              Anmelden
            </Link>
          </div>
        </div>
      </nav>
      </header>

      <main id="main-content">
      {/* Hero Section - Mit Gründer-Foto */}
      <section className="pt-32 pb-16 px-4 relative overflow-hidden" aria-labelledby="hero-heading">
        {/* Premium Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#fafaf8] via-white to-[#f0f4f8]"></div>
        <div className="absolute top-20 right-0 w-96 h-96 bg-[#b8860b]/5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-[#1e3a5f]/5 rounded-full blur-3xl"></div>
        
        <div className="max-w-7xl mx-auto relative">
          <div className="grid lg:grid-cols-[1fr_1.3fr] gap-8 items-center">
            {/* Text Content */}
            <div>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm border border-[#1e3a5f]/10 rounded-full mb-6 shadow-sm">
                <span className="w-2 h-2 bg-[#b8860b] rounded-full animate-pulse"></span>
                <span className="text-[#1e3a5f] text-sm font-medium">Für Juristen • Verwalter • Investoren • Eigentümer • Mieter</span>
              </div>
              
              <h1 id="hero-heading" className="text-4xl md:text-5xl lg:text-[3.25rem] font-bold text-[#1e3a5f] mb-6 leading-tight tracking-tight">
                Die KI-Rechtsplattform für <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#b8860b] to-[#d4a50f]">Immobilienrecht</span>
              </h1>

              {/* Mobile Image - zwischen Überschrift und Text */}
              <div className="lg:hidden flex justify-center mb-8">
                <div className="relative">
                  <div className="absolute -inset-4 bg-gradient-to-br from-[#1e3a5f]/20 to-[#b8860b]/20 rounded-2xl blur-2xl"></div>
                  <div className="relative bg-white p-2 rounded-xl shadow-xl">
                    <Image 
                      src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/gruender.jpeg?alt=media&token=9e773833-f0c2-4912-88dd-c1ecfd32e413"
                      alt="Konstantin Kranich, Gründer und Geschäftsführer von domulex.ai, im professionellen Porträt"
                      width={400}
                      height={500}
                      className="rounded-lg object-cover"
                      priority
                    />
                  </div>
                </div>
              </div>
              
              <p className="text-lg text-gray-600 mb-8 leading-relaxed">
                Entwickelt von Juristen und Immobilienprofis – für alle, die schnelle und verlässliche Antworten im Immobilienrecht suchen.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-10">
                <a 
                  href="/auth/register"
                  className="group relative px-8 py-4 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] hover:from-[#2d4a6f] hover:to-[#3d5a7f] text-white rounded-xl font-semibold text-center transition-all duration-300 shadow-xl shadow-[#1e3a5f]/30 hover:shadow-2xl hover:shadow-[#1e3a5f]/40 hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 overflow-hidden"
                >
                  <span className="relative z-10">Kostenlos registrieren</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-[#b8860b]/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </a>
                <Link 
                  href="/preise"
                  className="px-8 py-4 bg-white/80 backdrop-blur-sm border-2 border-[#1e3a5f]/20 text-[#1e3a5f] hover:border-[#1e3a5f]/40 hover:bg-white rounded-xl font-semibold text-center transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2"
                >
                  Preise ansehen
                </Link>
              </div>
            </div>

            {/* Gründer-Foto - nur Desktop */}
            <div className="hidden lg:flex justify-end">
              <div className="relative group">
                <div className="absolute -inset-8 bg-gradient-to-br from-[#1e3a5f]/30 to-[#b8860b]/30 rounded-3xl blur-3xl transition-all duration-500 group-hover:from-[#1e3a5f]/40 group-hover:to-[#b8860b]/40"></div>
                <div className="relative bg-white/90 backdrop-blur-sm p-4 rounded-2xl shadow-2xl ring-1 ring-black/5 transition-all duration-500 group-hover:shadow-3xl group-hover:-translate-y-1">
                  <Image 
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/gruender.jpeg?alt=media&token=9e773833-f0c2-4912-88dd-c1ecfd32e413"
                    alt="Konstantin Kranich, Gründer und Geschäftsführer von domulex.ai, im professionellen Porträt"
                    width={805}
                    height={1006}
                    className="rounded-xl object-cover"
                    style={{ width: '100%', maxWidth: '650px', height: 'auto' }}
                    priority
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Trust Indicators - zentriert unter dem Grid */}
          <div className="grid grid-cols-3 gap-8 pt-12 mt-8 border-t border-gray-200/50 max-w-3xl mx-auto">
            <div className="text-center group">
              <div className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] mb-2 transition-transform duration-300 group-hover:scale-105">50.000+</div>
              <div className="text-sm font-semibold text-gray-700 mb-1">Rechtsquellen</div>
              <div className="text-xs text-gray-500">Gesetze • Urteile • Literatur</div>
            </div>
            <div className="text-center group">
              <div className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] mb-2 transition-transform duration-300 group-hover:scale-105">100+</div>
              <div className="text-sm font-semibold text-gray-700 mb-1">Dokumentvorlagen</div>
              <div className="text-xs text-gray-500">Schriftsätze • Verträge • Klagen</div>
            </div>
            <div className="text-center group">
              <div className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] mb-2 transition-transform duration-300 group-hover:scale-105">24h</div>
              <div className="text-sm font-semibold text-gray-700 mb-1">Aktualisierung</div>
              <div className="text-xs text-gray-500">Täglich neue Urteile</div>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Bar */}
      <section className="py-8 bg-gradient-to-r from-white via-gray-50/50 to-white border-y border-gray-100/50 backdrop-blur-sm" aria-label="Vertrauensindikatoren">
        <div className="max-w-6xl mx-auto px-4">
          <ul className="flex flex-wrap items-center justify-center gap-8 md:gap-16" role="list">
            <li className="flex items-center gap-2.5 text-gray-600 transition-all duration-300 hover:text-gray-800 hover:scale-105">
              <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="font-medium">DSGVO-konform</span>
            </li>
            <li className="flex items-center gap-2.5 text-gray-600 transition-all duration-300 hover:text-gray-800 hover:scale-105">
              <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="font-medium">Google Cloud • ISO 27001</span>
            </li>
            <li className="flex items-center gap-2.5 text-gray-600 transition-all duration-300 hover:text-gray-800 hover:scale-105">
              <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="font-medium">Deutsche Rechtsquellen</span>
            </li>
            <li className="flex items-center gap-2.5 text-gray-600 transition-all duration-300 hover:text-gray-800 hover:scale-105">
              <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <span className="font-medium">Monatlich kündbar</span>
            </li>
          </ul>
        </div>
      </section>

      {/* NEU: Warum domulex statt ChatGPT? */}
      <section className="py-20 px-4 bg-gradient-to-b from-white via-gray-50/30 to-[#fafaf8] relative overflow-hidden" aria-labelledby="comparison-heading">
        <div className="absolute top-0 left-1/4 w-64 h-64 bg-red-100/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-64 h-64 bg-[#b8860b]/10 rounded-full blur-3xl"></div>
        <div className="max-w-6xl mx-auto relative">
          <div className="text-center mb-14">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-50 to-red-100 text-red-700 rounded-full text-sm font-medium mb-4 shadow-sm">
              <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse"></span>
              Wichtiger Unterschied
            </span>
            <h2 id="comparison-heading" className="text-3xl md:text-4xl lg:text-5xl font-bold text-[#1e3a5f] mb-4 tracking-tight">
              Warum nicht einfach ChatGPT nutzen?
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
              ChatGPT ist ein Allround-Assistent – aber für deutsches Recht gefährlich unzuverlässig
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {/* ChatGPT - Nachteile */}
            <div className="bg-gradient-to-br from-gray-50 to-gray-100/80 rounded-2xl p-8 border border-gray-200/50 shadow-lg hover:shadow-xl transition-all duration-300 backdrop-blur-sm">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-14 h-14 bg-gradient-to-br from-gray-200 to-gray-300 rounded-xl flex items-center justify-center shadow-inner">
                  <span className="text-2xl">🤖</span>
                </div>
                <div>
                  <h3 className="font-bold text-gray-700 text-lg">ChatGPT & Co.</h3>
                  <p className="text-sm text-gray-500">Allgemeine KI-Assistenten</p>
                </div>
              </div>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <span className="text-red-500 mt-0.5">✗</span>
                  <div>
                    <span className="font-medium text-gray-700">Keine Quellen</span>
                    <p className="text-sm text-gray-500">Keine Paragraphen, keine Aktenzeichen – woher wissen Sie, ob die Antwort stimmt?</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-500 mt-0.5">✗</span>
                  <div>
                    <span className="font-medium text-gray-700">Veraltetes Wissen</span>
                    <p className="text-sm text-gray-500">Trainingsstand oft 1-2 Jahre alt – neue Urteile fehlen komplett</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-500 mt-0.5">✗</span>
                  <div>
                    <span className="font-medium text-gray-700">"Halluziniert" Paragraphen</span>
                    <p className="text-sm text-gray-500">Erfindet Gesetze, die es nicht gibt – gefährlich bei Rechtsthemen!</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-red-500 mt-0.5">✗</span>
                  <div>
                    <span className="font-medium text-gray-700">USA-Server, kein Datenschutz</span>
                    <p className="text-sm text-gray-500">Ihre Vertragsdaten auf US-Servern – nicht DSGVO-konform</p>
                  </div>
                </li>
              </ul>
            </div>

            {/* domulex - Vorteile */}
            <div className="group bg-gradient-to-br from-[#1e3a5f] to-[#2d4a6f] rounded-2xl p-8 text-white relative overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-500 hover:-translate-y-1">
              <div className="absolute top-0 right-0 w-40 h-40 bg-[#b8860b]/20 rounded-full blur-3xl transition-all duration-500 group-hover:w-48 group-hover:h-48 group-hover:bg-[#b8860b]/30"></div>
              <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/5 rounded-full blur-2xl"></div>
              <div className="relative">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-14 h-14 bg-gradient-to-br from-[#b8860b] to-[#d4a50f] rounded-xl flex items-center justify-center shadow-lg shadow-[#b8860b]/30">
                    <span className="text-2xl">⚖️</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-lg">domulex.ai</h3>
                    <p className="text-sm text-blue-200">Spezialisiert auf Immobilienrecht</p>
                  </div>
                </div>
                <ul className="space-y-4">
                  <li className="flex items-start gap-3">
                    <span className="w-5 h-5 rounded-full bg-[#b8860b]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-[#b8860b] text-sm">✓</span>
                    </span>
                    <div>
                      <span className="font-medium">Immer mit Quellenangabe</span>
                      <p className="text-sm text-blue-200/80">Jede Antwort mit § und Aktenzeichen – verifizierbar</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-5 h-5 rounded-full bg-[#b8860b]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-[#b8860b] text-sm">✓</span>
                    </span>
                    <div>
                      <span className="font-medium">50.000+ aktuelle Rechtsquellen</span>
                      <p className="text-sm text-blue-200/80">Täglich aktualisierte BGH-Urteile, Gesetze, Kommentare</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-5 h-5 rounded-full bg-[#b8860b]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-[#b8860b] text-sm">✓</span>
                    </span>
                    <div>
                      <span className="font-medium">Keine Halluzinationen</span>
                      <p className="text-sm text-blue-200/80">RAG-Technologie: KI antwortet nur basierend auf echten Quellen</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="w-5 h-5 rounded-full bg-[#b8860b]/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-[#b8860b] text-sm">✓</span>
                    </span>
                    <div>
                      <span className="font-medium">DSGVO • Deutsche Server</span>
                      <p className="text-sm text-blue-200/80">Ihre Daten bleiben in der EU – ISO 27001 zertifiziert</p>
                    </div>
                  </li>
                </ul>
                <a href="/auth/register" className="mt-8 block w-full py-4 bg-gradient-to-r from-[#b8860b] to-[#d4a50f] hover:from-[#a07608] hover:to-[#b8860b] text-white rounded-xl font-semibold text-center transition-all duration-300 shadow-lg shadow-[#b8860b]/30 hover:shadow-xl hover:shadow-[#b8860b]/40 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-[#1e3a5f]">
                  Jetzt kostenlos testen →
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>



      {/* Produkt-Screenshots - Einblick in die Plattform */}
      <section className="py-24 px-4 bg-gradient-to-b from-[#fafaf8] via-white to-[#fafaf8] relative overflow-hidden" aria-labelledby="screenshots-heading">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#1e3a5f]/5 via-transparent to-transparent"></div>
        <div className="max-w-6xl mx-auto relative">
          <div className="text-center mb-16">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-[#1e3a5f]/5 border border-[#1e3a5f]/10 rounded-full text-sm font-medium text-[#1e3a5f] mb-4">
              <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full"></span>
              Produkteinblick
            </span>
            <h2 id="screenshots-heading" className="text-3xl md:text-4xl lg:text-5xl font-bold text-[#1e3a5f] mb-4 tracking-tight">
              Einblick in domulex.ai
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Entdecken Sie die Funktionen, die Ihre Arbeit mit Immobilienrecht revolutionieren
            </p>
          </div>

          {/* Screenshot Grid */}
          <div className="grid md:grid-cols-2 gap-10 mb-16">
            {/* Screenshot 1 - KI-Chat */}
            <div className="group relative">
              <div className="absolute -inset-3 bg-gradient-to-br from-[#1e3a5f]/30 to-[#b8860b]/30 rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
              <div 
                className="relative bg-white rounded-2xl shadow-xl ring-1 ring-black/5 overflow-hidden transition-all duration-500 group-hover:shadow-2xl group-hover:-translate-y-2 cursor-pointer"
                onClick={() => setLightboxImage({
                  src: "https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/ki-rechtsassistent.png?alt=media&token=7ecb3454-b398-43b5-8171-163c5ae0f568",
                  alt: "KI-Rechtsassistent - Rechtsfragen mit Quellenangaben",
                  title: "KI-Rechtsassistent"
                })}
              >
                <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] px-4 py-3 flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <span className="w-3 h-3 bg-red-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-yellow-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-green-400 rounded-full shadow-inner"></span>
                  </div>
                  <span className="text-white/90 text-sm font-medium ml-2">KI-Rechtsassistent</span>
                  <span className="ml-auto text-white/60 text-xs">🔍 Klicken zum Vergrößern</span>
                </div>
                <div className="aspect-[16/10] bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                  <Image
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/ki-rechtsassistent.png?alt=media&token=7ecb3454-b398-43b5-8171-163c5ae0f568"
                    alt="KI-Rechtsassistent - Rechtsfragen mit Quellenangaben"
                    width={800}
                    height={500}
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="mt-5 text-center">
                <h3 className="font-semibold text-[#1e3a5f] text-lg">KI-Rechtsassistent</h3>
                <p className="text-gray-600 text-sm mt-1">Stellen Sie Ihre Frage – erhalten Sie Antworten mit Quellenangaben</p>
              </div>
            </div>

            {/* Screenshot 2 - Vertragsanalyse */}
            <div className="group relative">
              <div className="absolute -inset-3 bg-gradient-to-br from-[#1e3a5f]/30 to-[#b8860b]/30 rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
              <div 
                className="relative bg-white rounded-2xl shadow-xl ring-1 ring-black/5 overflow-hidden transition-all duration-500 group-hover:shadow-2xl group-hover:-translate-y-2 cursor-pointer"
                onClick={() => setLightboxImage({
                  src: "https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/ki-vertragsanalyse.png?alt=media&token=36806e9b-9d0a-475d-9a16-bcabd574f866",
                  alt: "KI-Vertragsanalyse - Miet- und Kaufverträge prüfen",
                  title: "KI-Vertragsanalyse"
                })}
              >
                <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] px-4 py-3 flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <span className="w-3 h-3 bg-red-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-yellow-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-green-400 rounded-full shadow-inner"></span>
                  </div>
                  <span className="text-white/90 text-sm font-medium ml-2">Vertragsanalyse</span>
                  <span className="ml-auto text-white/60 text-xs">🔍 Klicken zum Vergrößern</span>
                </div>
                <div className="aspect-[16/10] bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                  <Image
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/ki-vertragsanalyse.png?alt=media&token=36806e9b-9d0a-475d-9a16-bcabd574f866"
                    alt="KI-Vertragsanalyse - Miet- und Kaufverträge prüfen"
                    width={800}
                    height={500}
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="mt-5 text-center">
                <h3 className="font-semibold text-[#1e3a5f] text-lg">KI-Vertragsanalyse</h3>
                <p className="text-gray-600 text-sm mt-1">Miet- und Kaufverträge prüfen, Risiken erkennen</p>
              </div>
            </div>

            {/* Screenshot 3 - Dashboard/Objekte */}
            <div className="group relative">
              <div className="absolute -inset-3 bg-gradient-to-br from-[#1e3a5f]/30 to-[#b8860b]/30 rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
              <div 
                className="relative bg-white rounded-2xl shadow-xl ring-1 ring-black/5 overflow-hidden transition-all duration-500 group-hover:shadow-2xl group-hover:-translate-y-2 cursor-pointer"
                onClick={() => setLightboxImage({
                  src: "https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/immobilienverwaltung_dashbourd.png?alt=media&token=97f0349b-c475-40c5-974d-ea04eac999da",
                  alt: "Immobilienverwaltung Dashboard - Objekte und Mieter verwalten",
                  title: "Immobilienverwaltung"
                })}
              >
                <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] px-4 py-3 flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <span className="w-3 h-3 bg-red-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-yellow-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-green-400 rounded-full shadow-inner"></span>
                  </div>
                  <span className="text-white/90 text-sm font-medium ml-2">Immobilienverwaltung</span>
                  <span className="ml-auto text-white/60 text-xs">🔍 Klicken zum Vergrößern</span>
                </div>
                <div className="aspect-[16/10] bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                  <Image
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/immobilienverwaltung_dashbourd.png?alt=media&token=97f0349b-c475-40c5-974d-ea04eac999da"
                    alt="Immobilienverwaltung Dashboard - Objekte und Mieter verwalten"
                    width={800}
                    height={500}
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="mt-5 text-center">
                <h3 className="font-semibold text-[#1e3a5f] text-lg">Immobilienverwaltung</h3>
                <p className="text-gray-600 text-sm mt-1">Objekte, Mieter, Nebenkosten – alles an einem Ort</p>
              </div>
            </div>

            {/* Screenshot 4 - Mandanten-CRM */}
            <div className="group relative">
              <div className="absolute -inset-3 bg-gradient-to-br from-[#1e3a5f]/30 to-[#b8860b]/30 rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
              <div 
                className="relative bg-white rounded-2xl shadow-xl ring-1 ring-black/5 overflow-hidden transition-all duration-500 group-hover:shadow-2xl group-hover:-translate-y-2 cursor-pointer"
                onClick={() => setLightboxImage({
                  src: "https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/crm%20mandanten.png?alt=media&token=1f7c44bc-5238-4d61-a703-abb52c5ec090",
                  alt: "Mandanten-CRM - Aktenführung und Fristen für Juristen",
                  title: "Mandanten-CRM"
                })}
              >
                <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] px-4 py-3 flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <span className="w-3 h-3 bg-red-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-yellow-400 rounded-full shadow-inner"></span>
                    <span className="w-3 h-3 bg-green-400 rounded-full shadow-inner"></span>
                  </div>
                  <span className="text-white/90 text-sm font-medium ml-2">Mandanten-CRM</span>
                  <span className="ml-auto text-white/60 text-xs">🔍 Klicken zum Vergrößern</span>
                </div>
                <div className="aspect-[16/10] bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
                  <Image
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/crm%20mandanten.png?alt=media&token=1f7c44bc-5238-4d61-a703-abb52c5ec090"
                    alt="Mandanten-CRM - Aktenführung und Fristen für Juristen"
                    width={800}
                    height={500}
                    className="w-full h-full object-cover"
                  />
                </div>
              </div>
              <div className="mt-5 text-center">
                <h3 className="font-semibold text-[#1e3a5f] text-lg">Mandanten-CRM</h3>
                <p className="text-gray-600 text-sm mt-1">Aktenführung, Fristen und Fallanalysen für Juristen</p>
              </div>
            </div>
          </div>

          {/* CTA unter Screenshots */}
          <div className="text-center">
            <a 
              href="/auth/register"
              className="group inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] hover:from-[#2d4a6f] hover:to-[#3d5a7f] text-white rounded-2xl font-semibold text-lg shadow-xl shadow-[#1e3a5f]/30 hover:shadow-2xl hover:shadow-[#1e3a5f]/40 transition-all duration-300 hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2"
            >
              <span>Jetzt selbst ausprobieren</span>
              <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </a>
            <p className="text-gray-500 text-sm mt-4">3 kostenlose Anfragen nach Registrierung</p>
          </div>
        </div>
      </section>

      {/* Zielgruppen - Für wen? */}
      <section id="zielgruppen" className="py-24 px-4 bg-gradient-to-b from-[#1e3a5f] to-[#152a45] relative overflow-hidden" aria-labelledby="zielgruppen-heading">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-[#b8860b]/10 via-transparent to-transparent"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-[#b8860b]/5 rounded-full blur-3xl"></div>
        <div className="max-w-6xl mx-auto relative">
          <div className="text-center mb-16">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-sm font-medium text-white mb-4">
              <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full"></span>
              Für jeden Anwendungsfall
            </span>
            <h2 id="zielgruppen-heading" className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 tracking-tight">
              Ein KI-Chat – maßgeschneidert für Ihre Bedürfnisse
            </h2>
            <p className="text-lg text-blue-200/80 max-w-2xl mx-auto leading-relaxed">
              Stellen Sie Ihre Rechtsfrage im Chat – plus spezialisierte Tools für Ihren Anwendungsfall
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: '⚖️',
                title: 'Juristen',
                subtitle: 'Mehr Fälle, weniger Recherche',
                mainFeature: '💬 Ihr Rechtsassistent – 24/7 abrufbereit',
                extras: ['+ Mandanten-CRM', '+ Dokumentenmanagement', '+ Schriftsatzgenerator'],
                highlight: 'Lawyer Pro'
              },
              {
                icon: '🏢',
                title: 'Immobilienverwalter',
                subtitle: 'Verwaltung ohne Papierkram',
                mainFeature: '💬 Ihr WEG- & Mietrecht-Assistent',
                extras: ['+ Objektverwaltung', '+ Nebenkostenabrechnung', '+ Mahnwesen & Zähler'],
                highlight: 'Professional'
              },
              {
                icon: '📈',
                title: 'Investoren & Vermieter',
                subtitle: 'Rendite maximieren, Risiken minimieren',
                mainFeature: '💬 Deals prüfen, Risiken erkennen',
                extras: ['+ Vertragsanalyse', '+ Renditerechner', '+ Steuer-Optimierung'],
                highlight: 'Professional'
              },
              {
                icon: '🏠',
                title: 'Mieter & Eigentümer',
                subtitle: 'Ihre Rechte kennen und durchsetzen',
                mainFeature: '💬 Endlich verstehen, was Ihnen zusteht',
                extras: ['+ Nebenkostenprüfung', '+ Musterbriefe', '+ Mängel-Vorlagen'],
                highlight: 'Basis'
              }
            ].map((group, idx) => (
              <div key={idx} className="group bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/20 hover:border-white/30 transition-all duration-500 hover:-translate-y-2 hover:shadow-2xl hover:shadow-black/20">
                <span className="text-4xl mb-4 block transition-transform duration-300 group-hover:scale-110">{group.icon}</span>
                <h3 className="text-xl font-semibold text-white mb-1">{group.title}</h3>
                <p className="text-blue-300/80 text-xs mb-5">{group.subtitle}</p>
                
                {/* Hauptfunktion hervorgehoben */}
                <div className="bg-gradient-to-r from-[#b8860b]/20 to-[#b8860b]/10 border border-[#b8860b]/30 rounded-xl p-3 mb-4 min-h-[56px] flex items-center backdrop-blur-sm">
                  <span className="text-white font-medium text-sm">{group.mainFeature}</span>
                </div>
                
                {/* Zusatztools */}
                <ul className="space-y-2 mb-5">
                  {group.extras.map((extra, i) => (
                    <li key={i} className="text-blue-200/80 text-xs flex items-start gap-2">
                      <span className="text-[#b8860b]">›</span>
                      {extra}
                    </li>
                  ))}
                </ul>
                <span className="inline-block px-4 py-1.5 bg-gradient-to-r from-[#b8860b] to-[#d4a50f] text-white text-xs font-semibold rounded-full shadow-lg shadow-[#b8860b]/30">
                  {group.highlight}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Preview - Kompakt mit Link zur Preisseite */}
      <section id="pricing" className="py-24 px-4 bg-gradient-to-b from-white via-gray-50/30 to-[#fafaf8] relative overflow-hidden" aria-labelledby="pricing-heading">
        <div className="absolute top-20 left-0 w-72 h-72 bg-blue-100/30 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-72 h-72 bg-[#b8860b]/10 rounded-full blur-3xl"></div>
        <div className="max-w-5xl mx-auto relative">
          <div className="text-center mb-14">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-[#1e3a5f]/5 border border-[#1e3a5f]/10 rounded-full text-sm font-medium text-[#1e3a5f] mb-4">
              <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full"></span>
              Transparente Preise
            </span>
            <h2 id="pricing-heading" className="text-3xl md:text-4xl lg:text-5xl font-bold text-[#1e3a5f] mb-4 tracking-tight">
              Passend für jeden Bedarf
            </h2>
            <p className="text-lg text-gray-600 leading-relaxed">
              Von privater Nutzung bis zur Kanzlei – monatlich kündbar
            </p>
          </div>

          {/* Kompakte Preis-Übersicht */}
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="group bg-white rounded-2xl p-8 border border-gray-200/50 text-center shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-2 ring-1 ring-black/5">
              <h3 className="text-xl font-bold text-[#1e3a5f] mb-2">Basis</h3>
              <p className="text-sm text-gray-500 mb-4">Für Mieter & Eigentümer</p>
              <div className="text-4xl font-bold text-[#1e3a5f]">19€<span className="text-lg font-normal text-gray-400">/Monat</span></div>
            </div>
            
            <div className="group bg-gradient-to-br from-blue-50 to-white rounded-2xl p-8 border-2 border-blue-400 text-center relative shadow-xl hover:shadow-2xl transition-all duration-500 hover:-translate-y-2">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-1.5 rounded-full text-xs font-bold text-white shadow-lg shadow-blue-500/30">
                BELIEBT
              </div>
              <h3 className="text-xl font-bold text-[#1e3a5f] mb-2">Professional</h3>
              <p className="text-sm text-gray-500 mb-4">Für Verwalter & Investoren</p>
              <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-blue-600">39€<span className="text-lg font-normal text-gray-400">/Monat</span></div>
            </div>
            
            <div className="group bg-gradient-to-br from-amber-50 to-white rounded-2xl p-8 border-2 border-[#b8860b] text-center relative shadow-xl hover:shadow-2xl transition-all duration-500 hover:-translate-y-2">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-[#b8860b] to-[#d4a50f] px-4 py-1.5 rounded-full text-xs font-bold text-white shadow-lg shadow-[#b8860b]/30">
                EMPFOHLEN
              </div>
              <h3 className="text-xl font-bold text-[#1e3a5f] mb-2">Lawyer Pro</h3>
              <p className="text-sm text-gray-500 mb-4">Für Juristen</p>
              <div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#b8860b] to-[#d4a50f]">69€<span className="text-lg font-normal text-gray-400">/Monat</span></div>
            </div>
          </div>

          {/* CTA zur Preisseite */}
          <div className="text-center">
            <Link 
              href="/preise"
              className="group inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] hover:from-[#2d4a6f] hover:to-[#3d5a7f] text-white rounded-2xl font-semibold text-lg shadow-xl shadow-[#1e3a5f]/30 hover:shadow-2xl hover:shadow-[#1e3a5f]/40 transition-all duration-300 hover:-translate-y-1"
            >
              <span>Alle Preise & Features vergleichen</span>
              <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
            <p className="text-gray-500 text-sm mt-5">Monatlich kündbar • 14 Tage Widerrufsrecht • Alle Preise inkl. MwSt.</p>
          </div>
        </div>
      </section>

      {/* Gründer-Zitat */}
      <section className="py-24 px-4 bg-gradient-to-b from-[#fafaf8] to-white">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-3xl p-8 md:p-12 shadow-xl ring-1 ring-black/5 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-40 h-40 bg-[#b8860b]/5 rounded-full blur-3xl"></div>
            <div className="flex flex-col md:flex-row items-center gap-10 relative">
              <div className="flex-shrink-0">
                <div className="relative group">
                  <div className="absolute -inset-2 bg-gradient-to-br from-[#1e3a5f]/20 to-[#b8860b]/20 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  <Image 
                    src="https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/gruender_buero.jpeg?alt=media&token=fe6bd50a-0eda-4963-90b3-609c039dfe8d"
                    alt="Konstantin Kranich"
                    width={200}
                    height={200}
                    className="rounded-full object-cover border-4 border-[#1e3a5f]/10 relative"
                  />
                </div>
              </div>
              <div>
                <svg className="w-12 h-12 text-[#b8860b]/20 mb-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
                </svg>
                <p className="text-xl text-gray-700 mb-6 leading-relaxed italic">
                  „Als Jurist und Immobilieninvestor mit langjähriger Erfahrung weiß ich, wie zeitaufwändig Rechtsrecherche sein kann. Deshalb haben wir domulex.ai entwickelt – ein Tool, das ich selbst jeden Tag nutze: präzise, schnell und auf echten deutschen Rechtsquellen basierend."
                </p>
                <div>
                  <div className="font-semibold text-[#1e3a5f]">Konstantin Kranich</div>
                  <div className="text-gray-500 text-sm">Gründer & Geschäftsführer, domulex.ai</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>



      {/* Final CTA */}
      <section className="py-24 px-4 bg-gradient-to-br from-[#1e3a5f] via-[#1e3a5f] to-[#152a45] relative overflow-hidden" aria-labelledby="cta-heading">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#b8860b]/10 via-transparent to-transparent"></div>
        <div className="absolute top-0 left-1/4 w-64 h-64 bg-[#b8860b]/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl"></div>
        <div className="max-w-4xl mx-auto text-center relative">
          <h2 id="cta-heading" className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 tracking-tight">
            Starten Sie jetzt mit domulex.ai
          </h2>
          <p className="text-xl text-blue-200/80 mb-10 leading-relaxed">
            Nach der Registrierung: 3 kostenlose Anfragen • Keine Kreditkarte erforderlich
          </p>
          <a 
            href="/auth/register"
            className="group inline-flex items-center gap-3 px-12 py-5 bg-gradient-to-r from-[#b8860b] to-[#d4a50f] hover:from-[#a07608] hover:to-[#b8860b] text-white rounded-2xl font-bold text-lg shadow-2xl shadow-[#b8860b]/40 hover:shadow-[#b8860b]/50 transition-all duration-300 hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-[#1e3a5f]"
          >
            Kostenlos registrieren
            <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </a>
        </div>
      </section>
      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-b from-[#0f1f2e] to-[#0a1520] py-16 px-4" role="contentinfo">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-10 mb-10">
            <div>
              <div className="flex items-center mb-4">
                <span className="text-xl font-semibold text-white">domulex<span className="text-[#b8860b]">.ai</span></span>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">
                KI-gestützte Rechtsplattform für Immobilienrecht.
              </p>
            </div>
            <nav aria-label="Produkt-Navigation">
              <h4 className="font-semibold text-white mb-5">Produkt</h4>
              <ul className="space-y-3 text-gray-400 text-sm" role="list">
                <li><Link href="/funktionen" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Funktionen</Link></li>
                <li><Link href="/preise" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Preise</Link></li>
                <li><Link href="/news" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">News</Link></li>
                <li><Link href="/auth/login" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Anmelden</Link></li>
              </ul>
            </nav>
            <nav aria-label="Rechtliche Navigation">
              <h4 className="font-semibold text-white mb-5">Rechtliches</h4>
              <ul className="space-y-3 text-gray-400 text-sm" role="list">
                <li><Link href="/impressum" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Impressum</Link></li>
                <li><Link href="/datenschutz" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Datenschutz</Link></li>
                <li><Link href="/agb" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">AGB</Link></li>
                <li><Link href="/avv" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">AVV (B2B)</Link></li>
                <li><Link href="/nda" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">NDA (B2B)</Link></li>
                <li><Link href="/redaktion" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Redaktion</Link></li>
              </ul>
            </nav>
            <nav aria-label="Support-Navigation">
              <h4 className="font-semibold text-white mb-5">Support</h4>
              <ul className="space-y-3 text-gray-400 text-sm" role="list">
                <li><Link href="/hilfe" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Hilfe</Link></li>
                <li><Link href="/faq" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">FAQ</Link></li>
                <li><Link href="/kuendigen" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Abo kündigen</Link></li>
                <li><a href="mailto:kontakt@domulex.ai" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">kontakt@domulex.ai</a></li>
              </ul>
            </nav>
          </div>
          <div className="border-t border-gray-800/50 pt-10 text-center text-gray-500 text-sm">
            <p className="mb-4">© 2026 Home Invest & Management GmbH. Alle Rechte vorbehalten.</p>
            <p className="text-xs text-gray-600 max-w-2xl mx-auto leading-relaxed">
              domulex.ai bietet KI-gestützte Rechtsanalysen auf Basis von 50.000+ Dokumenten. 
              Die Plattform ersetzt keine anwaltliche Beratung bei Gerichtsverfahren oder komplexen Rechtsstreitigkeiten.
            </p>
          </div>
        </div>
      </footer>

      {/* Checkout Modal */}
      {showCheckout && selectedPlan && (
        <CheckoutModal
          plan={selectedPlan}
          isOpen={showCheckout}
          onClose={() => setShowCheckout(false)}
          onConfirm={handleCheckoutConfirm}
        />
      )}

      {/* Screenshot Lightbox Modal */}
      {lightboxImage && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4"
          onClick={() => setLightboxImage(null)}
        >
          <button
            onClick={() => setLightboxImage(null)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors z-10"
            aria-label="Schließen"
          >
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div 
            className="relative max-w-7xl w-full max-h-[90vh] bg-white rounded-xl shadow-2xl overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d4a6f] px-4 py-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="flex gap-1.5">
                  <span className="w-3 h-3 bg-red-400 rounded-full shadow-inner"></span>
                  <span className="w-3 h-3 bg-yellow-400 rounded-full shadow-inner"></span>
                  <span className="w-3 h-3 bg-green-400 rounded-full shadow-inner"></span>
                </div>
                <span className="text-white font-medium ml-2">{lightboxImage.title}</span>
              </div>
              <span className="text-white/60 text-sm">ESC oder Klick zum Schließen</span>
            </div>
            <div className="overflow-auto max-h-[calc(90vh-48px)]">
              <Image
                src={lightboxImage.src}
                alt={lightboxImage.alt}
                width={1920}
                height={1200}
                className="w-full h-auto"
                priority
              />
            </div>
          </div>
        </div>
      )}

      {/* Cookie Consent Banner */}
      <CookieConsent />
    </div>
  );
}
