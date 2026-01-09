'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/firebase';
import { onAuthStateChanged } from 'firebase/auth';
import CheckoutModal from '@/components/CheckoutModal';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';

export default function PreisePage() {
  const router = useRouter();
  const [showCheckout, setShowCheckout] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<any>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setIsLoggedIn(!!user);
    });
    return () => unsubscribe();
  }, []);

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
          cancel_url: `${window.location.origin}/preise`
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
      <PremiumHeader activePage="preise" />

      {/* Premium Hero Section */}
      <section className="pt-36 pb-16 bg-gradient-to-br from-[#1e3a5f] via-[#1e3a5f] to-[#152a45] relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-[#b8860b]/10 via-transparent to-transparent"></div>
        <div className="absolute top-20 left-1/4 w-72 h-72 bg-[#b8860b]/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-10 right-1/3 w-48 h-48 bg-white/5 rounded-full blur-3xl"></div>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 text-center relative">
          <span className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full text-sm font-medium text-white mb-6">
            <span className="w-1.5 h-1.5 bg-[#b8860b] rounded-full animate-pulse"></span>
            Faire Preise
          </span>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 tracking-tight">
            Transparente <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#b8860b] to-[#d4a50f]">Preise</span>
          </h1>
          <p className="text-xl text-blue-100/80 max-w-2xl mx-auto leading-relaxed">
            Monatlich kündbar • 14 Tage Widerrufsrecht (auch gewerblich) • Alle Preise inkl. MwSt.
          </p>
        </div>
      </section>

      <main className="py-16 px-4">
        <div className="max-w-6xl mx-auto">

          {/* Pricing Cards */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {/* Basis */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-6">
                <span className="inline-block px-3 py-1 bg-gray-100 text-gray-600 text-xs font-semibold rounded-full mb-4">
                  FÜR PRIVATE
                </span>
                <h3 className="text-2xl font-bold text-[#1e3a5f] mb-2">Basis</h3>
                <p className="text-gray-500 text-sm">Für Mieter & Eigentümer</p>
              </div>
              <div className="flex items-baseline mb-6">
                <span className="text-5xl font-bold text-[#1e3a5f]">19€</span>
                <span className="text-gray-500 ml-2">/Monat</span>
              </div>
              <button 
                onClick={() => handleCheckout(plans.basis)} 
                className="w-full py-4 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-xl font-semibold transition-colors mb-8"
              >
                Jetzt starten
              </button>
              <ul className="space-y-4">
                {plans.basis.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-3 text-gray-600">
                    <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            {/* Professional */}
            <div className="bg-white rounded-2xl p-8 border-2 border-blue-500 shadow-xl relative transform md:-translate-y-4">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-blue-600 px-6 py-2 rounded-full text-sm font-bold text-white">
                BELIEBT
              </div>
              <div className="mb-6">
                <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full mb-4">
                  FÜR GEWERBLICHE
                </span>
                <h3 className="text-2xl font-bold text-[#1e3a5f] mb-2">Professional</h3>
                <p className="text-gray-500 text-sm">Für Verwalter & Investoren</p>
              </div>
              <div className="flex items-baseline mb-6">
                <span className="text-5xl font-bold text-blue-600">39€</span>
                <span className="text-gray-500 ml-2">/Monat</span>
              </div>
              <button 
                onClick={() => handleCheckout(plans.professional)} 
                className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold transition-colors mb-8"
              >
                Jetzt starten
              </button>
              <ul className="space-y-4">
                {plans.professional.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-3 text-gray-600">
                    <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>

            {/* Lawyer Pro */}
            <div className="bg-white rounded-2xl p-8 border-2 border-[#b8860b] shadow-xl relative">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-[#b8860b] px-6 py-2 rounded-full text-sm font-bold text-white">
                EMPFOHLEN
              </div>
              <div className="mb-6">
                <span className="inline-block px-3 py-1 bg-amber-100 text-amber-700 text-xs font-semibold rounded-full mb-4">
                  FÜR JURISTEN
                </span>
                <h3 className="text-2xl font-bold text-[#1e3a5f] mb-2">Lawyer Pro</h3>
                <p className="text-gray-500 text-sm">Für Kanzleien & Rechtsabteilungen</p>
              </div>
              <div className="flex items-baseline mb-6">
                <span className="text-5xl font-bold text-[#b8860b]">69€</span>
                <span className="text-gray-500 ml-2">/Monat</span>
              </div>
              <button 
                onClick={() => handleCheckout(plans.lawyer)} 
                className="w-full py-4 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-xl font-bold transition-colors mb-8"
              >
                Jetzt starten
              </button>
              <ul className="space-y-4">
                {plans.lawyer.features.slice(0, 8).map((feature, i) => (
                  <li key={i} className="flex items-start gap-3 text-gray-600">
                    <svg className="w-5 h-5 text-[#b8860b] flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Kostenlos testen */}
          <div className="bg-[#1e3a5f] rounded-2xl p-8 md:p-12 text-center">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Noch unsicher? Testen Sie kostenlos!
            </h2>
            <p className="text-blue-200 mb-8 max-w-2xl mx-auto">
              Nach der Registrierung erhalten Sie 3 kostenlose Anfragen – keine Kreditkarte erforderlich. 
              Überzeugen Sie sich selbst von der Qualität unserer KI-Rechtsanalysen.
            </p>
            <Link 
              href="/auth/register"
              className="inline-block px-10 py-4 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-xl font-bold text-lg shadow-lg transition-colors"
            >
              Kostenlos registrieren →
            </Link>
          </div>
        </div>
      </main>

      <PremiumFooter />

      {/* Checkout Modal */}
      {showCheckout && selectedPlan && (
        <CheckoutModal
          plan={selectedPlan}
          isOpen={showCheckout}
          onClose={() => setShowCheckout(false)}
          onConfirm={handleCheckoutConfirm}
        />
      )}
    </div>
  );
}
