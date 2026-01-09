'use client';

import { useState } from 'react';
import Link from 'next/link';
import { redirectToCheckout, STRIPE_PRICES } from '@/lib/stripe';

interface Plan {
  id: string;
  name: string;
  price: number;
  interval: 'monthly' | 'yearly';
  features: string[];
}

interface CheckoutModalProps {
  plan: Plan;
  isOpen: boolean;
  onClose: () => void;
  userEmail?: string;
  userId?: string;
}

export default function CheckoutModalV2({ plan, isOpen, onClose, userEmail, userId }: CheckoutModalProps) {
  const [acceptAGB, setAcceptAGB] = useState(false);
  const [acceptWiderruf, setAcceptWiderruf] = useState(false);
  const [isBusinessUser, setIsBusinessUser] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const canProceed = acceptAGB && (isBusinessUser || acceptWiderruf);

  const getPlanTier = (planId: string): string => {
    // Map plan IDs zu Backend Tier Namen
    const tierMap: Record<string, string> = {
      'basis': 'TENANT',
      'mieter_plus': 'TENANT',  // Legacy
      'professional': 'PRO',
      'lawyer': 'LAWYER',
    };
    return tierMap[planId] || 'TENANT';
  };

  const handleConfirm = async () => {
    if (!canProceed) return;
    
    setIsProcessing(true);
    setError(null);

    try {
      // Redirect zu Stripe Checkout
      await redirectToCheckout({
        priceId: '', // Nicht mehr benötigt - Backend nutzt Tier
        customerEmail: userEmail,
        userId: userId,
        planName: getPlanTier(plan.id),
        successUrl: `${window.location.origin}/konto?session_id={CHECKOUT_SESSION_ID}`,
        cancelUrl: `${window.location.origin}/#pricing`,
      });
    } catch (err: any) {
      console.error('Checkout error:', err);
      setError('Fehler beim Starten des Zahlungsvorgangs. Bitte versuchen Sie es erneut.');
      setIsProcessing(false);
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR'
    }).format(price);
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-200 shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-indigo-600">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white">Bestellung abschließen</h2>
              <p className="text-blue-100 text-sm mt-1">Sichere Zahlung via Stripe</p>
            </div>
            <button
              onClick={onClose}
              disabled={isProcessing}
              className="text-white/80 hover:text-white transition-colors disabled:opacity-50"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 m-6 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Order Summary */}
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Bestellübersicht</h3>
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
            <div className="flex justify-between items-center mb-3">
              <span className="text-gray-900 font-semibold">{plan.name}</span>
              <span className="text-blue-600 font-bold text-xl">{formatPrice(plan.price)}</span>
            </div>
            <p className="text-sm text-gray-600 mb-3">
              {plan.interval === 'monthly' ? 'Monatliches Abonnement' : 'Jährliches Abonnement'} • Jederzeit kündbar
            </p>
            <div className="border-t border-blue-200 pt-3">
              <ul className="space-y-2">
                {plan.features.map((feature, idx) => (
                  <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                    <svg className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* User Type Selection */}
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Art der Nutzung</h3>
          <div className="space-y-3">
            <label className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors border-2 border-transparent data-[checked=true]:border-blue-500">
              <input
                type="radio"
                name="userType"
                checked={!isBusinessUser}
                onChange={() => setIsBusinessUser(false)}
                className="w-5 h-5 text-blue-600 mt-0.5"
              />
              <div>
                <span className="text-gray-900 font-medium block">Privat (Verbraucher)</span>
                <span className="text-sm text-gray-600">14 Tage Widerrufsrecht</span>
              </div>
            </label>
            <label className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors border-2 border-transparent data-[checked=true]:border-blue-500">
              <input
                type="radio"
                name="userType"
                checked={isBusinessUser}
                onChange={() => setIsBusinessUser(true)}
                className="w-5 h-5 text-blue-600 mt-0.5"
              />
              <div>
                <span className="text-gray-900 font-medium block">Geschäftlich (Unternehmer)</span>
                <span className="text-sm text-gray-600">Kein Widerrufsrecht, sofortiger Zugang</span>
              </div>
            </label>
          </div>
        </div>

        {/* Legal Checkboxes */}
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Rechtliche Hinweise</h3>
          <div className="space-y-4">
            {/* AGB */}
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={acceptAGB}
                onChange={(e) => setAcceptAGB(e.target.checked)}
                className="w-5 h-5 text-blue-600 mt-0.5"
                required
              />
              <span className="text-sm text-gray-700">
                Ich habe die{' '}
                <Link href="/agb" target="_blank" className="text-blue-600 hover:underline font-medium">
                  Allgemeinen Geschäftsbedingungen (AGB)
                </Link>{' '}
                und die{' '}
                <Link href="/datenschutz" target="_blank" className="text-blue-600 hover:underline font-medium">
                  Datenschutzhinweise
                </Link>{' '}
                gelesen und akzeptiere diese. *
              </span>
            </label>

            {/* Widerruf (nur für Verbraucher) */}
            {!isBusinessUser && (
              <label className="flex items-start gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={acceptWiderruf}
                  onChange={(e) => setAcceptWiderruf(e.target.checked)}
                  className="w-5 h-5 text-blue-600 mt-0.5"
                  required
                />
                <span className="text-sm text-gray-700">
                  Ich habe die{' '}
                  <Link href="/agb#widerruf" target="_blank" className="text-blue-600 hover:underline font-medium">
                    Widerrufsbelehrung
                  </Link>{' '}
                  zur Kenntnis genommen und akzeptiere den sofortigen Beginn der Leistung vor Ablauf der Widerrufsfrist. *
                </span>
              </label>
            )}

            {/* AVV und NDA (nur für Geschäftskunden) */}
            {isBusinessUser && (
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                <p className="text-sm text-gray-800 mb-3">
                  <strong>Für gewerbliche Kunden gelten zusätzlich:</strong>
                </p>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li className="flex items-start gap-2">
                    <span className="text-amber-600">📋</span>
                    <span>
                      <Link href="/avv" target="_blank" className="text-blue-600 hover:underline font-medium">
                        Auftragsverarbeitungsvertrag (AVV)
                      </Link>{' '}
                      gemäß Art. 28 DSGVO
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-amber-600">🔒</span>
                    <span>
                      <Link href="/nda" target="_blank" className="text-blue-600 hover:underline font-medium">
                        Geheimhaltungsvereinbarung (NDA)
                      </Link>{' '}
                      für vertrauliche Geschäftsdaten
                    </span>
                  </li>
                </ul>
                <p className="text-xs text-gray-600 mt-3">
                  Mit Ihrer Bestellung werden AVV und NDA automatisch Vertragsbestandteil. 
                  Die Dokumente werden Ihnen mit der Bestellbestätigung per E-Mail zugesendet.
                </p>
              </div>
            )}

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <p className="text-xs text-gray-600">
                * Pflichtfelder • Datenschutz: Ihre Zahlungsdaten werden sicher verschlüsselt und von Stripe verarbeitet. 
                Wir speichern keine Kreditkartendaten.
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="p-6 space-y-3">
          <button
            onClick={handleConfirm}
            disabled={!canProceed || isProcessing}
            className="w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-lg font-bold text-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
          >
            {isProcessing ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Wird geladen...
              </span>
            ) : (
              `Zahlungspflichtig bestellen (${formatPrice(plan.price)})`
            )}
          </button>

          <button
            onClick={onClose}
            disabled={isProcessing}
            className="w-full py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium transition-colors disabled:opacity-50"
          >
            Abbrechen
          </button>

          <div className="flex items-center justify-center gap-4 pt-2">
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              Sichere Zahlung
            </div>
            <div className="text-xs text-gray-400">•</div>
            <div className="text-xs text-gray-500">256-Bit SSL Verschlüsselung</div>
          </div>
        </div>
      </div>
    </div>
  );
}
