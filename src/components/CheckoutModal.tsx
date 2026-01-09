'use client';

import { useState } from 'react';
import Link from 'next/link';

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
  onConfirm: (acceptedTerms: { agb: boolean; widerruf: boolean }) => void;
}

export default function CheckoutModal({ plan, isOpen, onClose, onConfirm }: CheckoutModalProps) {
  const [acceptAGB, setAcceptAGB] = useState(false);
  const [acceptWiderruf, setAcceptWiderruf] = useState(false);
  const [acceptDatenschutz, setAcceptDatenschutz] = useState(false);
  const [acceptNDA, setAcceptNDA] = useState(false);
  const [acceptAVV, setAcceptAVV] = useState(false);
  const [isBusinessUser, setIsBusinessUser] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showAGBPreview, setShowAGBPreview] = useState(false);
  const [showWiderrufPreview, setShowWiderrufPreview] = useState(false);

  if (!isOpen) return null;

  // Alle Nutzer brauchen AGB, Widerruf und Datenschutz
  // Gewerbliche brauchen zusätzlich NDA und AVV
  const canProceed = acceptAGB && acceptWiderruf && acceptDatenschutz && (!isBusinessUser || (acceptNDA && acceptAVV));

  const handleConfirm = async () => {
    if (!canProceed) return;
    
    setIsProcessing(true);
    await onConfirm({ agb: acceptAGB, widerruf: acceptWiderruf });
    setIsProcessing(false);
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR'
    }).format(price);
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-slate-800 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-slate-700">
        {/* Header */}
        <div className="p-6 border-b border-slate-700">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white">Bestellung abschließen</h2>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Order Summary */}
        <div className="p-6 border-b border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Bestellübersicht</h3>
          <div className="bg-slate-700/50 rounded-lg p-4">
            <div className="flex justify-between items-center mb-3">
              <span className="text-white font-medium">{plan.name}</span>
              <span className="text-blue-400 font-bold">{formatPrice(plan.price)}</span>
            </div>
            <p className="text-sm text-slate-400">
              {plan.interval === 'monthly' ? 'Monatliches Abonnement' : 'Jährliches Abonnement'}
            </p>
            <ul className="mt-3 space-y-1">
              {plan.features.map((feature, idx) => (
                <li key={idx} className="text-sm text-slate-300 flex items-center gap-2">
                  <span className="text-green-400">✓</span> {feature}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* User Type Selection */}
        <div className="p-6 border-b border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Art der Nutzung</h3>
          <div className="space-y-3">
            <label className="flex items-center gap-3 p-3 bg-slate-700/30 rounded-lg cursor-pointer hover:bg-slate-700/50 transition-colors">
              <input
                type="radio"
                name="userType"
                checked={!isBusinessUser}
                onChange={() => setIsBusinessUser(false)}
                className="w-4 h-4 text-blue-600"
              />
              <div>
                <span className="text-white font-medium">Privat (Verbraucher)</span>
                <p className="text-sm text-slate-400">Ich handle als Privatperson gemäß § 13 BGB</p>
              </div>
            </label>
            <label className="flex items-center gap-3 p-3 bg-slate-700/30 rounded-lg cursor-pointer hover:bg-slate-700/50 transition-colors">
              <input
                type="radio"
                name="userType"
                checked={isBusinessUser}
                onChange={() => setIsBusinessUser(true)}
                className="w-4 h-4 text-blue-600"
              />
              <div>
                <span className="text-white font-medium">Gewerblich (Unternehmer)</span>
                <p className="text-sm text-slate-400">Ich handle als Unternehmer gemäß § 14 BGB</p>
              </div>
            </label>
          </div>
        </div>

        {/* Terms Acceptance */}
        <div className="p-6 border-b border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">Rechtliche Hinweise</h3>
          
          {/* AGB Checkbox */}
          <div className="mb-4">
            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={acceptAGB}
                onChange={(e) => setAcceptAGB(e.target.checked)}
                className="w-5 h-5 mt-0.5 text-blue-600 rounded"
              />
              <div className="text-sm text-slate-300">
                <span>Ich habe die </span>
                <button
                  type="button"
                  onClick={() => setShowAGBPreview(!showAGBPreview)}
                  className="text-blue-400 hover:text-blue-300 underline"
                >
                  Allgemeinen Geschäftsbedingungen (AGB)
                </button>
                <span> gelesen und akzeptiere diese. *</span>
              </div>
            </label>
            
            {showAGBPreview && (
              <div className="mt-3 p-4 bg-slate-700/50 rounded-lg border border-slate-600 max-h-48 overflow-y-auto">
                <p className="text-sm text-slate-300 mb-2">
                  <strong className="text-white">Auszug aus den AGB:</strong>
                </p>
                <p className="text-sm text-slate-400">
                  § 1 Geltungsbereich: Diese AGB gelten für die Nutzung der Plattform domulex.ai, 
                  betrieben von Home Invest & Management GmbH...
                </p>
                <Link 
                  href="/agb" 
                  target="_blank" 
                  className="text-blue-400 hover:text-blue-300 text-sm mt-2 inline-block"
                >
                  Vollständige AGB lesen →
                </Link>
              </div>
            )}
          </div>

          {/* Datenschutzerklärung Checkbox */}
          <div className="mb-4">
            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={acceptDatenschutz}
                onChange={(e) => setAcceptDatenschutz(e.target.checked)}
                className="w-5 h-5 mt-0.5 text-blue-600 rounded"
              />
              <div className="text-sm text-slate-300">
                <span>Ich habe die </span>
                <Link href="/datenschutz" target="_blank" className="text-blue-400 hover:text-blue-300 underline">
                  Datenschutzerklärung
                </Link>
                <span> zur Kenntnis genommen. *</span>
              </div>
            </label>
          </div>

          {/* Widerrufsbelehrung Checkbox (für alle Nutzer) */}
          <div className="mb-4">
            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={acceptWiderruf}
                onChange={(e) => setAcceptWiderruf(e.target.checked)}
                className="w-5 h-5 mt-0.5 text-blue-600 rounded"
              />
              <div className="text-sm text-slate-300">
                <span>Ich habe die </span>
                <button
                  type="button"
                  onClick={() => setShowWiderrufPreview(!showWiderrufPreview)}
                  className="text-blue-400 hover:text-blue-300 underline"
                >
                  Widerrufsbelehrung
                </button>
                <span> zur Kenntnis genommen. *</span>
              </div>
            </label>
            
            {showWiderrufPreview && (
              <div className="mt-3 p-4 bg-slate-700/50 rounded-lg border border-slate-600 max-h-48 overflow-y-auto">
                <p className="text-sm text-slate-300 mb-2">
                  <strong className="text-white">Widerrufsbelehrung:</strong>
                </p>
                <p className="text-sm text-slate-400">
                  Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag 
                  zu widerrufen. Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsschlusses.
                </p>
                <Link 
                  href="/agb#widerruf" 
                  target="_blank" 
                  className="text-blue-400 hover:text-blue-300 text-sm mt-2 inline-block"
                >
                  Vollständige Widerrufsbelehrung lesen →
                </Link>
              </div>
            )}
            
            {/* Sofortiger Beginn der Dienstleistung */}
            <div className="mt-4 p-4 bg-amber-900/20 border border-amber-700 rounded-lg">
              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  defaultChecked
                  className="w-5 h-5 mt-0.5 text-amber-600 rounded"
                />
                <div className="text-sm text-amber-200">
                  Ich stimme ausdrücklich zu, dass mit der Ausführung der Dienstleistung vor 
                  Ablauf der Widerrufsfrist begonnen wird. Mir ist bekannt, dass ich dadurch 
                  mein Widerrufsrecht bei vollständiger Vertragserfüllung verliere.
                </div>
              </label>
            </div>
          </div>

          {isBusinessUser && (
            <div className="p-4 bg-blue-900/20 border border-blue-700 rounded-lg">
              <p className="text-sm text-blue-200 mb-4">
                <strong>Hinweis für gewerbliche Nutzer:</strong> Auch als Unternehmer gewähren wir 
                Ihnen freiwillig ein 14-tägiges Widerrufsrecht zu den gleichen Bedingungen wie für Verbraucher.
              </p>
              
              {/* NDA Checkbox */}
              <div className="mb-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={acceptNDA}
                    onChange={(e) => setAcceptNDA(e.target.checked)}
                    className="w-5 h-5 mt-0.5 text-blue-600 rounded"
                  />
                  <div className="text-sm text-blue-100">
                    <span>Ich akzeptiere die </span>
                    <Link href="/nda" target="_blank" className="text-blue-400 hover:text-blue-300 underline">
                      Vertraulichkeitsvereinbarung (NDA)
                    </Link>
                    <span> *</span>
                  </div>
                </label>
              </div>
              
              {/* AVV Checkbox */}
              <div>
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={acceptAVV}
                    onChange={(e) => setAcceptAVV(e.target.checked)}
                    className="w-5 h-5 mt-0.5 text-blue-600 rounded"
                  />
                  <div className="text-sm text-blue-100">
                    <span>Ich akzeptiere den </span>
                    <Link href="/avv" target="_blank" className="text-blue-400 hover:text-blue-300 underline">
                      Auftragsverarbeitungsvertrag (AVV)
                    </Link>
                    <span> gemäß Art. 28 DSGVO *</span>
                  </div>
                </label>
              </div>
            </div>
          )}

          <p className="text-xs text-slate-500 mt-4">* Pflichtfeld</p>
        </div>

        {/* Download Links */}
        <div className="p-6 border-b border-slate-700 bg-slate-700/20">
          <h3 className="text-sm font-semibold text-white mb-3">Dokumente zum Download</h3>
          <div className="flex flex-wrap gap-3">
            <a
              href="/downloads/agb.html"
              target="_blank"
              className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-slate-300 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              AGB herunterladen
            </a>
            <a
              href="/downloads/widerrufsbelehrung.html"
              target="_blank"
              className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-slate-300 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Widerrufsbelehrung herunterladen
            </a>
            <a
              href="/datenschutz"
              target="_blank"
              className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-slate-300 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Datenschutzerklärung
            </a>
            {isBusinessUser && (
              <>
                <a
                  href="/nda"
                  target="_blank"
                  className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-slate-300 transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  NDA
                </a>
                <a
                  href="/avv"
                  target="_blank"
                  className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-slate-300 transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  AVV (DSGVO)
                </a>
              </>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="p-6 flex gap-4">
          <button
            onClick={onClose}
            className="flex-1 py-3 px-6 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors"
          >
            Abbrechen
          </button>
          <button
            onClick={handleConfirm}
            disabled={!canProceed || isProcessing}
            className="flex-1 py-3 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
          >
            {isProcessing ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Wird bearbeitet...
              </span>
            ) : (
              `Zahlungspflichtig bestellen (${formatPrice(plan.price)})`
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
