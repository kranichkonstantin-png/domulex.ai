'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { auth, db } from '@/lib/firebase';
import { doc, getDoc } from 'firebase/firestore';
import CheckoutModal from './CheckoutModal';

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  requiredTier: 'basis' | 'professional' | 'lawyer';
  feature: string;
}

const TIER_INFO = {
  basis: {
    name: 'Basis',
    price: '19',
    color: 'from-blue-500 to-blue-600',
    icon: '🏠',
    level: 1,
    benefits: [
      '25 Anfragen pro Monat',
      '5.000 Rechtsquellen',
      'KI-Mietrecht-Check & WEG-Berater',
      'KI-Steuer-Assistent (AfA, Werbungskosten)',
      'KI-Musterbriefe & eigene Vorlagen',
      'KI-Nebenkostenprüfung mit Fehleranalyse',
    ],
  },
  professional: {
    name: 'Professional',
    price: '39',
    color: 'from-purple-500 to-purple-600',
    icon: '📊',
    level: 2,
    benefits: [
      '250 Anfragen pro Monat',
      '50.000+ Rechtsquellen',
      'KI-Immobilienverwaltung (Mieter, Mahnwesen)',
      'KI-Nebenkostenabrechnung (17 Kostenarten)',
      'KI-Renditerechner mit Cashflow-Prognose',
      'KI-Vertragsanalyse (Miet- & Kaufverträge)',
    ],
  },
  lawyer: {
    name: 'Lawyer Pro',
    price: '69',
    color: 'from-amber-500 to-amber-600',
    icon: '⚖️',
    level: 3,
    benefits: [
      'Unbegrenzte Anfragen',
      '50.000+ Rechtsquellen-Datenbank',
      'KI-Mandanten-CRM mit Aktenführung',
      'KI-Fristenverwaltung & Wiedervorlagen',
      'KI-Schriftsatzgenerator (Klagen, Mahnungen)',
      'KI-Fallanalyse (Erfolgsaussichten & Risiken)',
      'KI-Rechtsprechungsanalyse (BGH, OLG, LG)',
    ],
  },
};

// Bestimme den richtigen Upgrade-Tarif
function getUpgradeTier(
  userTier: string | undefined,
  userDashboardType: string | undefined,
  requiredTier: 'basis' | 'professional' | 'lawyer'
): 'basis' | 'professional' | 'lawyer' {
  const normalizedTier = userTier === 'mieter_plus' ? 'basis' : userTier;
  const isFreeUser = !normalizedTier || normalizedTier === 'free' || normalizedTier.startsWith('free');
  
  if (isFreeUser) {
    // Free-Nutzer: Zeige den Tarif, für den er sich registriert hat
    const registeredTier = userDashboardType?.replace('free-', '') as 'basis' | 'professional' | 'lawyer';
    if (registeredTier && TIER_INFO[registeredTier]) {
      return registeredTier;
    }
    // Fallback: Das was das Feature erfordert
    return requiredTier;
  }
  
  // Bezahlter Nutzer: Zeige das nächsthöhere Abo
  const currentLevel = TIER_INFO[normalizedTier as keyof typeof TIER_INFO]?.level || 0;
  const requiredLevel = TIER_INFO[requiredTier]?.level || 1;
  
  if (currentLevel < requiredLevel) {
    return requiredTier;
  }
  
  // Nutzer hat bereits Zugang - sollte nicht passieren
  return requiredTier;
}

export default function UpgradeModal({ isOpen, onClose, requiredTier, feature }: UpgradeModalProps) {
  const [actualTier, setActualTier] = useState<'basis' | 'professional' | 'lawyer'>(requiredTier);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [showCheckoutModal, setShowCheckoutModal] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    
    const loadUserTier = async () => {
      setIsLoading(true);
      try {
        const currentUser = auth.currentUser;
        if (currentUser) {
          const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
          if (userDoc.exists()) {
            const data = userDoc.data();
            const upgradeTier = getUpgradeTier(data.tier, data.dashboardType, requiredTier);
            setActualTier(upgradeTier);
          }
        }
      } catch (err) {
        console.error('Error loading user tier:', err);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadUserTier();
  }, [isOpen, requiredTier]);

  if (!isOpen) return null;

  const tierInfo = TIER_INFO[actualTier];

  // Öffne CheckoutModal statt direkt zu Stripe
  const handleUpgradeClick = () => {
    setShowCheckoutModal(true);
  };

  // Wird aufgerufen wenn User im CheckoutModal bestätigt
  const handleCheckoutConfirm = async () => {
    setCheckoutLoading(true);
    setError(null);
    try {
      const currentUser = auth.currentUser;
      if (!currentUser) {
        setError('Bitte melden Sie sich erneut an.');
        return;
      }
      const token = await currentUser.getIdToken(true);

      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';
      console.log('Creating checkout session:', { tier: actualTier, backendUrl });

      const response = await fetch(`${backendUrl}/stripe/create-checkout-session`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({
          tier: actualTier,
          success_url: `${window.location.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: window.location.href
        })
      });

      const data = await response.json();
      
      if (!response.ok) {
        console.error('Checkout response error:', data);
        throw new Error(data.detail || 'Checkout-Session konnte nicht erstellt werden');
      }
      
      if (!data.checkout_url) {
        throw new Error('Keine Checkout-URL erhalten');
      }
      
      window.location.href = data.checkout_url;
    } catch (err: any) {
      console.error('Checkout error:', err);
      setError(err.message || 'Fehler beim Checkout. Bitte versuchen Sie es erneut.');
    } finally {
      setCheckoutLoading(false);
    }
  };

  // Plan-Objekt für CheckoutModal
  const checkoutPlan = {
    id: actualTier,
    name: tierInfo.name,
    price: parseInt(tierInfo.price),
    interval: 'monthly' as const,
    features: tierInfo.benefits,
  };

  // Zeige CheckoutModal wenn aktiviert
  if (showCheckoutModal) {
    return (
      <CheckoutModal
        plan={checkoutPlan}
        isOpen={true}
        onClose={() => {
          setShowCheckoutModal(false);
        }}
        onConfirm={handleCheckoutConfirm}
      />
    );
  }

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-gray-700 rounded-2xl max-w-md w-full overflow-hidden shadow-2xl animate-in fade-in zoom-in duration-200">
        {/* Header */}
        <div className={`bg-gradient-to-r ${tierInfo.color} p-6 text-white text-center`}>
          <span className="text-4xl mb-2 block">{tierInfo.icon}</span>
          <h2 className="text-2xl font-bold">Upgrade erforderlich</h2>
          <p className="text-white/80 mt-1 text-sm">
            {feature} ist Teil des {tierInfo.name}-Tarifs
          </p>
        </div>

        {/* Content */}
        <div className="p-6">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="w-8 h-8 border-2 border-gray-600 border-t-white rounded-full animate-spin"></div>
            </div>
          ) : (
            <>
              <div className="text-center mb-6">
                <p className="text-gray-300">
                  Um diese Funktion zu nutzen, benötigen Sie den
                </p>
                <p className="text-2xl font-bold text-white mt-2">
                  {tierInfo.name}-Tarif
                </p>
                <p className="text-gray-400 mt-1">
                  nur <span className="text-white font-semibold">{tierInfo.price} €</span> / Monat
                </p>
              </div>

              {/* Benefits */}
              <div className="bg-gray-800/50 rounded-xl p-4 mb-6">
                <p className="text-sm text-gray-400 mb-3">Inklusive:</p>
                <ul className="space-y-2">
                  {tierInfo.benefits.map((benefit, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm text-gray-300">
                      <span className="text-green-400">✓</span>
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Error */}
              {error && (
                <div className="bg-red-900/50 border border-red-700 text-red-300 p-3 rounded-lg mb-4 text-sm">
                  {error}
                </div>
              )}

              {/* Buttons */}
              <div className="space-y-3">
                <button
                  onClick={handleUpgradeClick}
                  disabled={checkoutLoading}
                  className={`w-full py-3 bg-gradient-to-r ${tierInfo.color} text-white rounded-xl font-semibold text-center hover:opacity-90 transition-opacity disabled:opacity-50`}
                >
                  {checkoutLoading ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                      Wird geladen...
                    </span>
                  ) : (
                    'Jetzt upgraden'
                  )}
                </button>
                <button
                  onClick={onClose}
                  className="w-full py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-xl font-medium transition-colors"
                >
                  Später
                </button>
              </div>

              <p className="text-xs text-gray-500 text-center mt-4">
                Jederzeit kündbar • Sichere Zahlung via Stripe
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// Inline Upgrade Banner für Seiten
export function UpgradeBanner({ 
  requiredTier, 
  feature,
  className = '' 
}: { 
  requiredTier: 'basis' | 'professional' | 'lawyer';
  feature: string;
  className?: string;
}) {
  const tierInfo = TIER_INFO[requiredTier];

  return (
    <div className={`bg-gradient-to-r ${tierInfo.color} rounded-xl p-4 ${className}`}>
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{tierInfo.icon}</span>
          <div>
            <p className="font-semibold text-white">{feature}</p>
            <p className="text-sm text-white/80">
              Verfügbar ab {tierInfo.name}-Tarif • {tierInfo.price} €/Monat
            </p>
          </div>
        </div>
        <Link
          href={`/konto?upgrade=${requiredTier}`}
          className="px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg font-medium transition-colors whitespace-nowrap"
        >
          Jetzt freischalten →
        </Link>
      </div>
    </div>
  );
}
