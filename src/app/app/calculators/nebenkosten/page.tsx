'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Logo from '@/components/Logo';
import UpgradeModal from '@/components/UpgradeModal';
import { hasTierAccess } from '@/lib/tierUtils';
import { onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import { useRouter } from 'next/navigation';

interface Nebenkosten {
  heizung: number;
  warmwasser: number;
  wasser: number;
  abwasser: number;
  muell: number;
  hausmeister: number;
  treppenhausreinigung: number;
  gartenpflege: number;
  aufzug: number;
  versicherung: number;
  grundsteuer: number;
  beleuchtung: number;
  schornsteinfeger: number;
  kabelanschluss: number;
  sonstige: number;
}

const initialNebenkosten: Nebenkosten = {
  heizung: 0,
  warmwasser: 0,
  wasser: 0,
  abwasser: 0,
  muell: 0,
  hausmeister: 0,
  treppenhausreinigung: 0,
  gartenpflege: 0,
  aufzug: 0,
  versicherung: 0,
  grundsteuer: 0,
  beleuchtung: 0,
  schornsteinfeger: 0,
  kabelanschluss: 0,
  sonstige: 0
};

const nebenkostenLabels: Record<keyof Nebenkosten, { label: string; icon: string; umlagefaehig: boolean }> = {
  heizung: { label: 'Heizkosten', icon: '🔥', umlagefaehig: true },
  warmwasser: { label: 'Warmwasser', icon: '🚿', umlagefaehig: true },
  wasser: { label: 'Kaltwasser', icon: '💧', umlagefaehig: true },
  abwasser: { label: 'Abwasser', icon: '🚰', umlagefaehig: true },
  muell: { label: 'Müllabfuhr', icon: '🗑️', umlagefaehig: true },
  hausmeister: { label: 'Hausmeister', icon: '🔧', umlagefaehig: true },
  treppenhausreinigung: { label: 'Treppenhausreinigung', icon: '🧹', umlagefaehig: true },
  gartenpflege: { label: 'Gartenpflege', icon: '🌳', umlagefaehig: true },
  aufzug: { label: 'Aufzug', icon: '🛗', umlagefaehig: true },
  versicherung: { label: 'Gebäudeversicherung', icon: '🏠', umlagefaehig: true },
  grundsteuer: { label: 'Grundsteuer', icon: '📋', umlagefaehig: true },
  beleuchtung: { label: 'Allgemeinbeleuchtung', icon: '💡', umlagefaehig: true },
  schornsteinfeger: { label: 'Schornsteinfeger', icon: '🎩', umlagefaehig: true },
  kabelanschluss: { label: 'Kabelanschluss', icon: '📺', umlagefaehig: true },
  sonstige: { label: 'Sonstige Kosten', icon: '📦', umlagefaehig: false }
};

export default function NebenkostenrechnerPage() {
  const router = useRouter();
  const [wohnflaeche, setWohnflaeche] = useState<number>(80);
  const [gesamtflaeche, setGesamtflaeche] = useState<number>(500);
  const [vorauszahlung, setVorauszahlung] = useState<number>(200);
  const [abrechnungszeitraum, setAbrechnungszeitraum] = useState<number>(12);
  const [nebenkosten, setNebenkosten] = useState<Nebenkosten>(initialNebenkosten);
  const [verteilschluessel, setVerteilschluessel] = useState<'wohnflaeche' | 'personenzahl' | 'einheiten'>('wohnflaeche');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const [loading, setLoading] = useState(true);

  // Check if user has access (Basis tier or higher)
  const hasAccess = hasTierAccess(userTier, 'basis');
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      if (userDoc.exists()) {
        const tier = userDoc.data().tier || userDoc.data().dashboardType || 'free';
        setUserTier(tier);
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, [router]);

  const updateNebenkosten = (key: keyof Nebenkosten, value: number) => {
    setNebenkosten(prev => ({ ...prev, [key]: value }));
  };

  // Berechnung des Anteils
  const anteil = wohnflaeche / gesamtflaeche;
  
  // Gesamte Nebenkosten
  const gesamtNebenkosten = Object.values(nebenkosten).reduce((sum, val) => sum + val, 0);
  
  // Umlagefähige Kosten
  const umlagefaehig = Object.entries(nebenkosten)
    .filter(([key]) => nebenkostenLabels[key as keyof Nebenkosten].umlagefaehig)
    .reduce((sum, [, val]) => sum + val, 0);
  
  // Anteil des Mieters
  const mieterAnteil = umlagefaehig * anteil;
  
  // Vorauszahlungen im Zeitraum
  const gezahlteVorauszahlungen = vorauszahlung * abrechnungszeitraum;
  
  // Nachzahlung/Guthaben
  const differenz = mieterAnteil - gezahlteVorauszahlungen;
  
  // Monatliche Kosten
  const monatlicheKosten = mieterAnteil / abrechnungszeitraum;
  
  // Kosten pro qm
  const kostenProQm = monatlicheKosten / wohnflaeche;

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-xl border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-gray-400 hover:text-white">
                ← Dashboard
              </Link>
              <Logo size="sm" />
            </div>
            <h1 className="text-lg font-semibold text-white">Nebenkostenrechner</h1>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Nebenkostenrechner</h1>
          <p className="text-gray-400 mt-2">Prüfen Sie Ihre Nebenkostenabrechnung oder berechnen Sie Ihren Anteil</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Eingabe */}
          <div className="lg:col-span-2 space-y-6">
            {/* Grunddaten */}
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">📊 Grunddaten</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Ihre Wohnfläche (m²)</label>
                  <input
                    type="number"
                    value={wohnflaeche}
                    onChange={(e) => setWohnflaeche(Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 text-white rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Gesamtfläche (m²)</label>
                  <input
                    type="number"
                    value={gesamtflaeche}
                    onChange={(e) => setGesamtflaeche(Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 text-white rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Vorauszahlung/Monat (€)</label>
                  <input
                    type="number"
                    value={vorauszahlung}
                    onChange={(e) => setVorauszahlung(Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 text-white rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Zeitraum (Monate)</label>
                  <input
                    type="number"
                    value={abrechnungszeitraum}
                    onChange={(e) => setAbrechnungszeitraum(Number(e.target.value))}
                    className="w-full p-2 bg-gray-800/50 border border-gray-700 text-white rounded-lg"
                  />
                </div>
              </div>
              <div className="mt-4">
                <label className="block text-sm text-gray-400 mb-1">Verteilungsschlüssel</label>
                <select
                  value={verteilschluessel}
                  onChange={(e) => setVerteilschluessel(e.target.value as 'wohnflaeche' | 'personenzahl' | 'einheiten')}
                  className="p-2 bg-gray-800/50 border border-gray-700 text-white rounded-lg"
                >
                  <option value="wohnflaeche">Nach Wohnfläche (Standard)</option>
                  <option value="personenzahl">Nach Personenzahl</option>
                  <option value="einheiten">Nach Wohneinheiten</option>
                </select>
              </div>
            </div>

            {/* Nebenkostenpositionen */}
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">💰 Nebenkostenpositionen (Gesamthaus/Jahr)</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {(Object.keys(nebenkosten) as (keyof Nebenkosten)[]).map((key) => (
                  <div key={key}>
                    <label className="flex items-center gap-2 text-sm text-gray-400 mb-1">
                      <span>{nebenkostenLabels[key].icon}</span>
                      <span>{nebenkostenLabels[key].label}</span>
                      {!nebenkostenLabels[key].umlagefaehig && (
                        <span className="text-xs text-red-400">(nicht umlagefähig)</span>
                      )}
                    </label>
                    <div className="relative">
                      <input
                        type="number"
                        value={nebenkosten[key] || ''}
                        onChange={(e) => updateNebenkosten(key, Number(e.target.value))}
                        placeholder="0"
                        className="w-full p-2 pr-8 bg-gray-800/50 border border-gray-700 text-white rounded-lg"
                      />
                      <span className="absolute right-3 top-2.5 text-gray-400">€</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Typische Werte */}
            <div className="bg-blue-900/30 border border-blue-700 rounded-xl p-4">
              <h3 className="font-medium text-white mb-2">📌 Typische Werte (Stand 2024)</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <p className="text-gray-400">Heizkosten</p>
                  <p className="font-medium text-white">1,00-1,50 €/m²/Monat</p>
                </div>
                <div>
                  <p className="text-gray-400">Warmwasser</p>
                  <p className="font-medium text-white">0,20-0,40 €/m²/Monat</p>
                </div>
                <div>
                  <p className="text-gray-400">Wasser/Abwasser</p>
                  <p className="font-medium text-white">0,30-0,50 €/m²/Monat</p>
                </div>
                <div>
                  <p className="text-gray-400">Gesamt (Durchschnitt)</p>
                  <p className="font-medium text-white">2,87 €/m²/Monat</p>
                </div>
              </div>
            </div>
          </div>

          {/* Ergebnis */}
          <div className="space-y-6">
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6 sticky top-4">
              <h2 className="text-lg font-semibold text-white mb-4">📋 Berechnung</h2>
              
              <div className="space-y-4">
                <div className="pb-4 border-b border-gray-700">
                  <p className="text-sm text-gray-500">Ihr Anteil</p>
                  <p className="text-2xl font-bold text-white">
                    {(anteil * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-400">{wohnflaeche} von {gesamtflaeche} m²</p>
                </div>

                <div className="pb-4 border-b border-gray-700">
                  <p className="text-sm text-gray-500">Gesamte umlagefähige Kosten</p>
                  <p className="text-xl font-bold text-white">{umlagefaehig.toFixed(2)} €</p>
                </div>

                <div className="pb-4 border-b border-gray-700">
                  <p className="text-sm text-gray-500">Ihr Anteil (jährlich)</p>
                  <p className="text-xl font-bold text-white">{mieterAnteil.toFixed(2)} €</p>
                </div>

                <div className="pb-4 border-b border-gray-700">
                  <p className="text-sm text-gray-500">Vorauszahlungen im Zeitraum</p>
                  <p className="text-xl font-bold text-gray-400">{gezahlteVorauszahlungen.toFixed(2)} €</p>
                </div>

                <div className={`p-4 rounded-lg ${differenz > 0 ? 'bg-red-900/30 border border-red-700' : 'bg-green-900/30 border border-green-700'}`}>
                  <p className="text-sm text-gray-500">
                    {differenz > 0 ? 'Nachzahlung' : 'Guthaben'}
                  </p>
                  <p className={`text-2xl font-bold ${differenz > 0 ? 'text-red-400' : 'text-green-400'}`}>
                    {Math.abs(differenz).toFixed(2)} €
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="bg-gray-700/50 p-3 rounded-lg text-center">
                    <p className="text-xs text-gray-500">pro Monat</p>
                    <p className="text-lg font-bold text-white">{monatlicheKosten.toFixed(2)} €</p>
                  </div>
                  <div className="bg-gray-700/50 p-3 rounded-lg text-center">
                    <p className="text-xs text-gray-500">pro m²/Monat</p>
                    <p className="text-lg font-bold text-white">{kostenProQm.toFixed(2)} €</p>
                  </div>
                </div>

                {kostenProQm > 3.50 && (
                  <div className="mt-4 p-3 bg-amber-900/30 border border-amber-700 rounded-lg text-sm text-amber-300">
                    ⚠️ <strong>Hinweis:</strong> Ihre Nebenkosten von {kostenProQm.toFixed(2)} €/m² liegen über dem Durchschnitt. Prüfen Sie die Abrechnung genau.
                  </div>
                )}
              </div>

              <div className="mt-6">
                <Link
                  href="/dashboard"
                  className="block w-full text-center py-3 bg-[#1e3a5f] text-white rounded-lg hover:bg-[#2d4a6f] transition-colors"
                >
                  🤖 Abrechnung prüfen lassen
                </Link>
              </div>
            </div>

            {/* Rechtliche Hinweise */}
            <div className="bg-amber-900/30 border border-amber-700 rounded-xl p-4 text-sm text-amber-300">
              <p className="font-medium mb-2">⚖️ Gut zu wissen</p>
              <ul className="space-y-1 text-xs">
                <li>• Abrechnung muss 12 Monate nach Ende des Abrechnungszeitraums vorliegen</li>
                <li>• Widerspruchsfrist: 12 Monate nach Erhalt</li>
                <li>• Sie haben Anspruch auf Belegeinsicht</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="basis"
        feature="Nebenkostenrechner"
      />
    </div>
  );
}
