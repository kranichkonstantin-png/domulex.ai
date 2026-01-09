'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface CookiePreferences {
  necessary: boolean;
  analytics: boolean;
  marketing: boolean;
}

const COOKIE_CONSENT_KEY = 'domulex_cookie_consent';
const COOKIE_PREFERENCES_KEY = 'domulex_cookie_preferences';

export default function CookieConsent() {
  const [showBanner, setShowBanner] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [preferences, setPreferences] = useState<CookiePreferences>({
    necessary: true, // Immer erforderlich
    analytics: false,
    marketing: false,
  });

  useEffect(() => {
    // Prüfen ob bereits Zustimmung erteilt wurde
    const consent = localStorage.getItem(COOKIE_CONSENT_KEY);
    if (!consent) {
      setShowBanner(true);
    }
  }, []);

  const saveConsent = (allAccepted: boolean) => {
    const finalPreferences = allAccepted
      ? { necessary: true, analytics: true, marketing: true }
      : preferences;

    localStorage.setItem(COOKIE_CONSENT_KEY, 'true');
    localStorage.setItem(COOKIE_PREFERENCES_KEY, JSON.stringify(finalPreferences));
    
    // Hier können Sie Analytics aktivieren wenn zugestimmt
    if (finalPreferences.analytics) {
      // Google Analytics oder ähnliches aktivieren
      console.log('Analytics cookies enabled');
    }
    
    setShowBanner(false);
  };

  const handleAcceptAll = () => {
    saveConsent(true);
  };

  const handleAcceptSelected = () => {
    saveConsent(false);
  };

  const handleRejectAll = () => {
    setPreferences({ necessary: true, analytics: false, marketing: false });
    saveConsent(false);
  };

  if (!showBanner) return null;

  return (
    <>
      {/* Overlay der die Seite blockiert */}
      <div 
        className="fixed inset-0 z-[99] bg-black/50 backdrop-blur-sm"
        aria-hidden="true"
      />
      
      {/* Cookie Banner */}
      <div className="fixed bottom-0 left-0 right-0 z-[100] bg-white border-t border-gray-200 shadow-2xl">
      <div className="max-w-6xl mx-auto px-4 py-4 sm:py-6">
        {/* Kompakte Ansicht */}
        {!showDetails && (
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <div className="flex-1">
              <p className="text-sm text-gray-700">
                <span className="font-medium">🍪 Cookie-Einstellungen:</span>{' '}
                Wir verwenden Cookies, um Ihnen die bestmögliche Erfahrung zu bieten. 
                Einige Cookies sind für den Betrieb der Website notwendig, während andere 
                uns helfen, die Website zu verbessern.{' '}
                <Link href="/datenschutz" className="text-[#1e3a5f] underline hover:no-underline">
                  Mehr erfahren
                </Link>
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setShowDetails(true)}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Einstellungen
              </button>
              <button
                onClick={handleRejectAll}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Nur Notwendige
              </button>
              <button
                onClick={handleAcceptAll}
                className="px-4 py-2 text-sm text-white bg-[#1e3a5f] hover:bg-[#2d4a6f] rounded-lg transition-colors"
              >
                Alle akzeptieren
              </button>
            </div>
          </div>
        )}

        {/* Detailansicht mit Auswahlmöglichkeiten */}
        {showDetails && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Cookie-Einstellungen</h3>
              <button
                onClick={() => setShowDetails(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>

            <p className="text-sm text-gray-600">
              Hier können Sie Ihre Cookie-Präferenzen verwalten. Notwendige Cookies können nicht 
              deaktiviert werden, da sie für den Betrieb der Website erforderlich sind.
            </p>

            <div className="space-y-3">
              {/* Notwendige Cookies */}
              <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                <input
                  type="checkbox"
                  checked={true}
                  disabled
                  className="mt-1 rounded border-gray-300"
                />
                <div className="flex-1">
                  <p className="font-medium text-gray-900">Notwendige Cookies</p>
                  <p className="text-sm text-gray-600">
                    Diese Cookies sind für die Grundfunktionen der Website erforderlich, 
                    wie z.B. Anmeldung, Sicherheit und Speicherung Ihrer Einstellungen. 
                    Sie können nicht deaktiviert werden.
                  </p>
                </div>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                  Immer aktiv
                </span>
              </div>

              {/* Analyse Cookies */}
              <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                <input
                  type="checkbox"
                  checked={preferences.analytics}
                  onChange={(e) => setPreferences({ ...preferences, analytics: e.target.checked })}
                  className="mt-1 rounded border-gray-300 text-[#1e3a5f] focus:ring-[#1e3a5f]"
                />
                <div className="flex-1">
                  <p className="font-medium text-gray-900">Analyse-Cookies</p>
                  <p className="text-sm text-gray-600">
                    Diese Cookies helfen uns zu verstehen, wie Besucher mit unserer Website 
                    interagieren, indem anonyme Informationen gesammelt werden. Dies hilft 
                    uns, die Website zu verbessern.
                  </p>
                </div>
              </div>

              {/* Marketing Cookies */}
              <div className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                <input
                  type="checkbox"
                  checked={preferences.marketing}
                  onChange={(e) => setPreferences({ ...preferences, marketing: e.target.checked })}
                  className="mt-1 rounded border-gray-300 text-[#1e3a5f] focus:ring-[#1e3a5f]"
                />
                <div className="flex-1">
                  <p className="font-medium text-gray-900">Marketing-Cookies</p>
                  <p className="text-sm text-gray-600">
                    Diese Cookies werden verwendet, um relevantere Werbung anzuzeigen. 
                    Sie können auch dazu dienen, die Effektivität von Werbekampagnen zu messen.
                  </p>
                </div>
              </div>
            </div>

            {/* Rechtliche Hinweise */}
            <div className="text-xs text-gray-500 border-t pt-3">
              <p>
                <strong>Rechtsgrundlage:</strong> Die Verarbeitung erfolgt gemäß Art. 6 Abs. 1 lit. a DSGVO 
                (Einwilligung) für optionale Cookies und Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse) 
                für notwendige Cookies. Sie können Ihre Einwilligung jederzeit widerrufen.{' '}
                <Link href="/datenschutz" className="text-[#1e3a5f] underline">
                  Datenschutzerklärung
                </Link>{' '}
                |{' '}
                <Link href="/impressum" className="text-[#1e3a5f] underline">
                  Impressum
                </Link>
              </p>
            </div>

            {/* Aktionsbuttons */}
            <div className="flex flex-wrap gap-2 pt-2">
              <button
                onClick={handleRejectAll}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Alle ablehnen
              </button>
              <button
                onClick={handleAcceptSelected}
                className="px-4 py-2 text-sm text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Auswahl speichern
              </button>
              <button
                onClick={handleAcceptAll}
                className="px-4 py-2 text-sm text-white bg-[#1e3a5f] hover:bg-[#2d4a6f] rounded-lg transition-colors"
              >
                Alle akzeptieren
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
    </>
  );
}

// Hook um Cookie-Präferenzen abzurufen
export function useCookiePreferences(): CookiePreferences | null {
  const [preferences, setPreferences] = useState<CookiePreferences | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem(COOKIE_PREFERENCES_KEY);
    if (stored) {
      try {
        setPreferences(JSON.parse(stored));
      } catch {
        setPreferences(null);
      }
    }
  }, []);

  return preferences;
}
