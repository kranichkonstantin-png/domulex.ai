'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { signOut, onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc, updateDoc } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import ChatInterface from '@/components/ChatInterface';
import Logo from '@/components/Logo';
import UpgradeModal from '@/components/UpgradeModal';
import CheckoutModal from '@/components/CheckoutModal';

type Role = 'MIETER' | 'EIGENTUEMER' | 'VERMIETER' | 'INVESTOR' | 'VERWALTER' | 'ANWALT';

interface UserData {
  email: string;
  name: string;
  tier: string;
  dashboardType?: string;
  queriesUsed: number;
  queriesLimit: number;
  stripeCustomerId?: string;
  stripeSubscriptionId?: string;
  isAdmin?: boolean;
  isTestUser?: boolean;  // Test-Kunden sehen keine Upgrade-Buttons
  role?: string;
}

function UpgradeSuccessBanner({ onDismiss }: { onDismiss: () => void }) {
  return (
    <div className="bg-green-500 text-white p-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <span className="text-2xl">✅</span>
        <div>
          <p className="font-semibold">Upgrade erfolgreich!</p>
          <p className="text-sm opacity-90">Ihr Konto wurde aktualisiert. Alle Premium-Funktionen sind jetzt freigeschaltet.</p>
        </div>
      </div>
      <button onClick={onDismiss} className="hover:bg-green-600 p-2 rounded-full transition-colors">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  );
}

// (EmbeddedChat component removed - replaced by ChatInterface below)

function DashboardContent() {
  const [user, setUser] = useState<any>(null);
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedRole, setSelectedRole] = useState<Role>('MIETER');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [showUpgradeSuccess, setShowUpgradeSuccess] = useState(false);
  const [showCheckoutModal, setShowCheckoutModal] = useState(false);
  const [checkoutPlan, setCheckoutPlan] = useState<{ id: string; name: string; price: number; interval: 'monthly'; features: string[] } | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  // Plan-Definitionen für CheckoutModal
  const PLAN_DEFINITIONS = {
    basis: {
      id: 'basis',
      name: 'Basis',
      price: 19,
      interval: 'monthly' as const,
      features: ['25 Anfragen pro Monat', '5.000 Rechtsquellen', 'KI-Mietrecht-Check & WEG-Berater', 'KI-Steuer-Assistent', 'KI-Musterbriefe', 'KI-Nebenkostenprüfung']
    },
    professional: {
      id: 'professional',
      name: 'Professional',
      price: 39,
      interval: 'monthly' as const,
      features: ['250 Anfragen pro Monat', '50.000+ Rechtsquellen', 'KI-Immobilienverwaltung', 'KI-Nebenkostenabrechnung', 'KI-Renditerechner', 'KI-Vertragsanalyse']
    },
    lawyer: {
      id: 'lawyer',
      name: 'Lawyer Pro',
      price: 69,
      interval: 'monthly' as const,
      features: ['Unbegrenzte Anfragen', '50.000+ Rechtsquellen', 'KI-Mandanten-CRM', 'KI-Fristenverwaltung', 'KI-Schriftsatzgenerator', 'KI-Fallanalyse']
    }
  };

  // Sofortiger Auth-Check beim Mount - nur User setzen, NICHT loading beenden
  // Loading wird erst beendet, wenn Firestore-Daten geladen sind
  useEffect(() => {
    if (auth.currentUser) {
      setUser(auth.currentUser);
      // NICHT setLoading(false) hier - Firestore-Daten müssen erst geladen werden
    }
  }, []);

  // Normalisiere tier (legacy support für mieter_plus)
  const normalizedTier = userData?.tier === 'mieter_plus' ? 'basis' : userData?.tier;

  // Free User = tier startet mit 'free' ODER ist 'free' ODER nicht gesetzt
  const isFreeUser = normalizedTier?.startsWith('free') || normalizedTier === 'free' || !normalizedTier;
  
  // Test-User sehen KEINE Upgrade-Buttons (vom Admin ohne Zahlung erstellt)
  const isTestUser = userData?.isTestUser === true;
  
  // Upgrade-Buttons nur anzeigen wenn: Free-User UND kein Test-User
  const showUpgradeOptions = isFreeUser && !isTestUser;

  const getDashboardType = () => {
    if (userData?.dashboardType) return userData.dashboardType;
    if (normalizedTier === 'free_basis' || normalizedTier === 'basis') return 'basis';
    if (normalizedTier === 'free_professional' || normalizedTier === 'professional') return 'professional';
    if (normalizedTier === 'free_lawyer' || normalizedTier === 'lawyer') return 'lawyer';
    return 'basis';
  };

  const showUpgrade = () => {
    // Test-User sehen keine Upgrades
    if (isTestUser) return;
    setShowUpgradeModal(true);
  };

  // Checkout Parameter aus URL prüfen (nach Registrierung mit Plan)
  useEffect(() => {
    const checkoutParam = searchParams.get('checkout');
    if (checkoutParam && ['basis', 'professional', 'lawyer'].includes(checkoutParam)) {
      // URL bereinigen
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('checkout');
      window.history.replaceState({}, '', newUrl.toString());
      
      // CheckoutModal mit dem gewählten Plan öffnen
      const plan = PLAN_DEFINITIONS[checkoutParam as keyof typeof PLAN_DEFINITIONS];
      if (plan) {
        setCheckoutPlan(plan);
        setShowCheckoutModal(true);
      }
    }
  }, [searchParams]);

  // Checkout bestätigen - zu Stripe weiterleiten
  const handleCheckoutConfirm = async () => {
    if (!checkoutPlan) return;
    
    try {
      const currentUser = auth.currentUser;
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      
      const idToken = await currentUser.getIdToken();
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';
      
      const response = await fetch(`${backendUrl}/stripe/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`
        },
        body: JSON.stringify({
          tier: checkoutPlan.id,
          success_url: `${window.location.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: `${window.location.origin}/dashboard`
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
      setShowCheckoutModal(false);
    }
  };

  // Session ID aus URL prüfen (nach erfolgreichem Checkout)
  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    if (sessionId) {
      // URL bereinigen (session_id entfernen)
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.delete('session_id');
      window.history.replaceState({}, '', newUrl.toString());
      
      // Session bei Stripe verifizieren, bevor Erfolgsmeldung angezeigt wird
      const verifySession = async () => {
        try {
          const currentUser = auth.currentUser;
          if (!currentUser) return;
          
          const token = await currentUser.getIdToken(true);
          const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';
          
          const response = await fetch(`${backendUrl}/stripe/verify-session/${sessionId}`, {
            method: 'GET',
            headers: { 
              'Authorization': `Bearer ${token}` 
            }
          });
          
          if (response.ok) {
            const data = await response.json();
            if (data.success) {
              // Zahlung erfolgreich - Erfolgsmeldung anzeigen
              setShowUpgradeSuccess(true);
              
              // Profil nach kurzer Verzögerung neu laden (Webhook braucht Zeit)
              setTimeout(async () => {
                try {
                  const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
                  if (userDoc.exists()) {
                    setUserData(userDoc.data() as UserData);
                  }
                } catch (err) {
                  console.error('Error reloading user data:', err);
                }
              }, 2000);
            }
            // Bei fehlgeschlagener Zahlung: keine Erfolgsmeldung anzeigen
          }
        } catch (err) {
          console.error('Error verifying checkout session:', err);
        }
      };
      
      verifySession();
    }
  }, [searchParams]);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.replace('/auth/login');
        return;
      }

      setUser(currentUser);

      try {
        const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
        if (userDoc.exists()) {
          const data = userDoc.data() as UserData;
          setUserData(data);
          
          if (data.tier === 'lawyer') {
            setSelectedRole('ANWALT');
          } else if (data.tier === 'professional') {
            setSelectedRole('INVESTOR');
          } else {
            setSelectedRole((data.role as Role) || 'MIETER');
          }
        }
      } catch (err) {
        console.error('Error loading user data:', err);
      } finally {
        // Loading erst beenden, wenn User-Daten geladen sind
        // Verhindert Flash des falschen Dashboards
        setLoading(false);
      }
    });

    return () => unsubscribe();
  }, [router]);

  const handleRoleChange = async (role: Role) => {
    setSelectedRole(role);
    if (user) {
      try {
        await updateDoc(doc(db, 'users', user.uid), { role });
      } catch (err) {
        console.error('Error updating role:', err);
      }
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      router.push('/');
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
        {/* Skeleton Header */}
        <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-xl border-b border-gray-800">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <div className="flex justify-between items-center h-16">
              <div className="w-24 h-8 bg-gray-700 rounded animate-pulse"></div>
              <div className="flex gap-4">
                <div className="w-20 h-8 bg-gray-700 rounded animate-pulse"></div>
                <div className="w-20 h-8 bg-gray-700 rounded animate-pulse"></div>
              </div>
            </div>
          </div>
        </nav>
        
        <div className="max-w-6xl mx-auto px-4 sm:px-6 pt-24">
          {/* Skeleton Welcome */}
          <div className="mb-8">
            <div className="w-64 h-8 bg-gray-700 rounded animate-pulse mb-2"></div>
            <div className="w-48 h-4 bg-gray-800 rounded animate-pulse"></div>
          </div>
          
          {/* Skeleton Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1,2,3,4,5,6].map(i => (
              <div key={i} className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
                <div className="w-12 h-12 bg-gray-700 rounded-lg animate-pulse mb-4"></div>
                <div className="w-32 h-5 bg-gray-700 rounded animate-pulse mb-2"></div>
                <div className="w-24 h-4 bg-gray-800 rounded animate-pulse"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const dashboardType = getDashboardType();
  const getUpgradeTier = () => {
    if (dashboardType === 'basis') return 'basis';
    if (dashboardType === 'professional') return 'professional';
    return 'lawyer';
  };

  const roleOptions = {
    basis: [
      { id: 'MIETER', name: 'Mieter', icon: '👤', desc: 'Mietrecht, Kündigungsschutz' },
      { id: 'EIGENTUEMER', name: 'Eigentümer', icon: '🔑', desc: 'WEG-Recht, Hausgeld' },
      { id: 'VERMIETER', name: 'Vermieter', icon: '🏠', desc: 'Vermietung, Mieterhöhung' }
    ],
    professional: [
      { id: 'INVESTOR', name: 'Investor', icon: '🏢', desc: 'Investments, Rendite' },
      { id: 'VERWALTER', name: 'Verwalter', icon: '⚙️', desc: 'WEG-Verwaltung' },
      { id: 'VERMIETER', name: 'Vermieter', icon: '🏠', desc: 'Vermietung, Mieterhöhung' }
    ],
    lawyer: [
      { id: 'ANWALT', name: 'Jurist', icon: '⚖️', desc: 'Vollzugriff auf alle Bereiche' }
    ]
  };

  // Tarif-spezifische Features
  const tierFeatures = {
    basis: [
      { icon: '📊', name: 'KI-Nebenkostenprüfung', desc: 'Abrechnung prüfen', href: '/app/nebenkosten-pruefung', locked: false, isTool: true },
      { icon: '✉️', name: 'KI-Musterbriefe', desc: 'Vorlagen für Mieter', href: '/app/templates', locked: false },
      { icon: '💰', name: 'KI-Steuer-Assistent', desc: 'AfA & Werbungskosten', href: '/app?prompt=Welche%20steuerlichen%20Abzüge%20kann%20ich%20geltend%20machen?', locked: false, usesQuery: true },
      { icon: '📋', name: 'KI-Mietrecht-Check', desc: 'Rechte & Pflichten', href: '/app?prompt=Was%20sind%20meine%20Rechte%20als%20Mieter?', locked: false, usesQuery: true },
      { icon: '🏠', name: 'KI-WEG-Berater', desc: 'Eigentümer-Fragen', href: '/app?prompt=WEG%20Beschluss%20anfechten', locked: false, usesQuery: true },
    ],
    professional: [
      // Haupttool für Immobilienverwalter
      { icon: '\u{1F3E2}', name: 'KI-Immobilienverwaltung', desc: 'Objekte, Mieter, Zähler, Mahnwesen, Beschlüsse, Handwerker', href: '/app/objekte', locked: false, isTool: true },
      // Abrechnungstools
      { icon: '\u{1F4CA}', name: 'KI-Nebenkostenabrechnung', desc: 'Abrechnungen erstellen & prüfen', href: '/app/nebenkosten-abrechnung', locked: false, isTool: true },
      { icon: '\u{1F4C8}', name: 'KI-Renditerechner', desc: 'Investment-Analyse & Prognose', href: '/app/calculators/rendite', locked: false, isTool: true },
      // Vertrags- & Dokumententools
      { icon: '\u{1F50D}', name: 'KI-Vertragsanalyse', desc: 'Miet- & Kaufverträge prüfen', href: '/app/contract-analysis', locked: false },
      { icon: '\u{2709}\u{FE0F}', name: 'KI-Profi-Vorlagen', desc: 'Mieterhöhung, Kündigung, Mahnung', href: '/app/templates', locked: false },
      // Beratungstools
      { icon: '\u{1F4B0}', name: 'KI-Steuer-Optimierung', desc: 'AfA, Spekulationsfrist, Abschreibung', href: '/app?prompt=Wie%20optimiere%20ich%20die%20Steuerlast%20meiner%20Immobilien?', locked: false, usesQuery: true },
      { icon: '\u{1F3D7}\u{FE0F}', name: 'KI-Baurecht-Assistent', desc: 'Mängel, VOB, Gewährleistung', href: '/app?prompt=Baumängel%20Gewährleistung', locked: false, usesQuery: true },
    ],
    lawyer: [
      { icon: '\u{1F465}', name: 'KI-Mandanten-CRM', desc: 'Mandantenverwaltung', href: '/app/crm', locked: false, isTool: true },
      { icon: '\u{1F4C5}', name: 'KI-Fristenverwaltung', desc: 'Termine & Fristen', href: '/app/deadlines', locked: false, isTool: true },
      { icon: '\u{1F4C2}', name: 'KI-Dokumentenmanagement', desc: 'Suche & Analyse', href: '/app/documents', locked: false, isTool: true },
      { icon: '\u{1F4DC}', name: 'KI-Schriftsatzgenerator', desc: 'Klagen, Verträge, Mahnungen', href: '/app/templates', locked: false },
      { icon: '\u{1F4C4}', name: 'KI-Vertragsanalyse', desc: 'Risikobewertung', href: '/app/contract-analysis', locked: false },
      { icon: '\u{1F3AF}', name: 'KI-Fallanalyse', desc: 'Erfolgsaussichten & Risiken', href: '/app/fallanalyse', locked: false },
      { icon: '\u{2696}\u{FE0F}', name: 'KI-Rechtsprechungsanalyse', desc: 'BGH & Landgerichte', href: '/app/rechtsprechung', locked: false },
    ]
  };

  const currentRoles = roleOptions[dashboardType as keyof typeof roleOptions] || roleOptions.basis;

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      <UpgradeModal 
        isOpen={showUpgradeModal} 
        onClose={() => setShowUpgradeModal(false)} 
        requiredTier="basis"
        feature="Dashboard-Funktionen"
      />

      {/* Upgrade Success Banner */}
      {showUpgradeSuccess && (
        <UpgradeSuccessBanner onDismiss={() => setShowUpgradeSuccess(false)} />
      )}

      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-[106px]">
            <Logo size="sm" />
            <div className="flex items-center gap-2 sm:gap-4">
              <Link href="/app/schnellstart" className="flex items-center gap-1 px-3 py-1.5 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-full text-sm font-medium transition-colors">
                🚀 <span className="hidden sm:inline">Schnellstart</span>
              </Link>
              <Link href="/konto" className="text-sm text-gray-600 hover:text-[#1e3a5f] whitespace-nowrap">Mein Bereich</Link>
              <button onClick={handleLogout} className="px-3 sm:px-4 py-2 text-sm text-gray-700 hover:text-[#1e3a5f] whitespace-nowrap">Abmelden</button>
            </div>
          </div>
        </div>
      </nav>

      {/* Free User Banner - unter der Navigation */}
      {showUpgradeOptions && !showUpgradeSuccess && (
        <div className="fixed top-[106px] left-0 right-0 z-40 bg-gradient-to-r from-[#b8860b] to-[#d4a012] text-white py-2 px-4 text-center text-sm">
          <span className="mr-2">🔓</span>
          Sie nutzen den <strong>Test-Tarif</strong> mit 3 kostenlosen Anfragen. 
          <button onClick={() => showUpgrade()} className="ml-2 underline font-medium hover:no-underline">
            Jetzt upgraden für Vollzugriff →
          </button>
        </div>
      )}
      
      {/* Test-User Info Banner - unter der Navigation */}
      {isTestUser && (
        <div className="fixed top-[106px] left-0 right-0 z-40 bg-purple-600 text-white py-2 px-4 text-center text-sm">
          <span className="mr-2">🧪</span>
          Sie nutzen einen <strong>Test-Account</strong> mit vollem Zugang zum {getDashboardType() === 'basis' ? 'Basis' : getDashboardType() === 'professional' ? 'Professional' : 'Lawyer Pro'}-Tarif.
        </div>
      )}

      {/* Main Content - mit extra padding wenn Banner sichtbar */}
      <div className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8 ${(showUpgradeOptions && !showUpgradeSuccess) || isTestUser ? 'pt-40' : 'pt-32'}`}>
        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold text-[#1e3a5f]">
              Willkommen, {userData?.name ? userData.name.split(' ')[0] : 'Nutzer'}! 👋
            </h1>
            <p className="text-gray-600 text-sm">
              {dashboardType === 'lawyer' && 'Juristen-Dashboard für Immobilienrecht'}
              {dashboardType === 'professional' && 'Professional-Dashboard für Immobilienprofis'}
              {dashboardType === 'basis' && 'Ihr persönliches Immobilienrecht-Dashboard'}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {/* Status Badge - nur für zahlende User oder Test-User (1x pro Typ) */}
            {(!isFreeUser || isTestUser) && dashboardType === 'lawyer' && (
              <span className="px-4 py-2 bg-[#b8860b] text-white rounded-full text-sm font-medium">
                ⚖️ Lawyer Pro {isTestUser && '(Test)'}
              </span>
            )}
            {(!isFreeUser || isTestUser) && dashboardType !== 'lawyer' && (
              <span className="px-4 py-2 bg-[#1e3a5f] text-white rounded-full text-sm font-medium">
                {dashboardType === 'professional' ? '🏢 Professional' : '🏠 Basis'} {isTestUser && '(Test)'}
              </span>
            )}
            {/* Upgrade Button - für ALLE Free-User (inkl. Free-Lawyer) die NICHT Test-User sind */}
            {showUpgradeOptions && (
              <button
                onClick={() => showUpgrade()}
                className="px-4 py-2 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-full text-sm font-medium transition-colors flex items-center gap-1"
              >
                ⬆️ <span className="hidden sm:inline">Jetzt upgraden</span>
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Advanced Chat with Source Filters */}
          <div className="lg:col-span-2">
            <ChatInterface 
              role={selectedRole}
              jurisdiction="DE"
              subJurisdiction="Bundesweit"
              language="de"
            />
          </div>

          {/* Right Column - Controls & Features */}
          <div className="space-y-6">
            {/* Role Selection */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-[#1e3a5f]">Ihre Perspektive</h3>
              </div>
              <p className="text-xs text-gray-500 mb-3">Die KI passt ihre Antworten an Ihre Rolle an.</p>
              <div className="space-y-2">
                {currentRoles.map((role) => (
                  <button
                    key={role.id}
                    onClick={() => handleRoleChange(role.id as Role)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all ${
                      selectedRole === role.id 
                        ? 'bg-[#1e3a5f] text-white' 
                        : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                    }`}
                  >
                    <span className="text-xl">{role.icon}</span>
                    <div className="text-left">
                      <p className="font-medium">{role.name}</p>
                      <p className={`text-xs ${selectedRole === role.id ? 'text-white/70' : 'text-gray-500'}`}>{role.desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Quick Actions - Tarif-spezifisch */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <h3 className="font-semibold text-[#1e3a5f] mb-3">Ihre Werkzeuge</h3>
              <div className="space-y-2">
                {/* FREE-User sehen alle Features ihres dashboardType und können alle Seiten besuchen */}
                {/* Die Sperrung (KI, Upload, Anlegen) passiert auf den einzelnen Seiten */}
                {(() => {
                  // Zeige Features basierend auf dashboardType
                  return tierFeatures[dashboardType as keyof typeof tierFeatures] || tierFeatures.basis;
                })().map((feature) => {
                  // Alle Features sind anklickbar - Sperrung erfolgt auf den jeweiligen Seiten
                  const isLocked = false;
                  
                  if (isLocked) {
                    return (
                      <button
                        key={feature.name}
                        onClick={() => showUpgrade()}
                        className="w-full flex items-center gap-3 p-3 rounded-lg bg-gray-100/50 hover:bg-gray-100 transition-all text-left border border-dashed border-gray-300"
                      >
                        <span className="text-xl grayscale opacity-60">{feature.icon}</span>
                        <div className="flex-1">
                          <p className="font-medium text-gray-500">{feature.name}</p>
                          <p className="text-xs text-gray-400">{feature.desc}</p>
                        </div>
                        <span className="text-xs bg-[#b8860b]/20 text-[#b8860b] px-2 py-1 rounded-full whitespace-nowrap">
                          🔒 {(feature as any).tier || 'Pro'}
                        </span>
                      </button>
                    );
                  }
                  
                  return (
                    <Link
                      key={feature.name}
                      href={feature.href}
                      className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
                    >
                      <span className="text-xl">{feature.icon}</span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <p className="font-medium text-[#1e3a5f]">{feature.name}</p>
                          {feature.isTool && (
                            <span className="text-[10px] bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded font-medium">Tool</span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500">{feature.desc}</p>
                        {(feature as any).usesQuery && (
                          <p className="text-[10px] text-orange-500 mt-0.5">verbraucht 1 Anfrage</p>
                        )}
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>

            {/* Usage Stats - nur für Basis/Professional Nutzer */}
            {!(userData?.tier === 'lawyer' && !isFreeUser) && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <h3 className="font-semibold text-[#1e3a5f] mb-3">Ihr Kontingent</h3>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-500">Verwendet</span>
                    <span className="font-medium">{userData?.queriesUsed || 0} / {userData?.queriesLimit || 0}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all ${
                        (userData?.queriesUsed || 0) >= (userData?.queriesLimit || 1) ? 'bg-red-500' : 'bg-[#1e3a5f]'
                      }`}
                      style={{ width: `${Math.min(((userData?.queriesUsed || 0) / (userData?.queriesLimit || 1)) * 100, 100)}%` }}
                    ></div>
                  </div>
                  <p className="text-center mt-3">
                    <span className={`text-2xl font-bold ${
                      (userData?.queriesLimit || 0) - (userData?.queriesUsed || 0) <= 0 ? 'text-red-500' : 'text-[#1e3a5f]'
                    }`}>{Math.max(0, (userData?.queriesLimit || 0) - (userData?.queriesUsed || 0))}</span>
                    <span className="text-sm text-gray-500 ml-2">verbleibend</span>
                  </p>
                  {isFreeUser && (
                    <button
                      onClick={() => showUpgrade()}
                      className="mt-4 w-full py-2 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-lg text-sm font-medium transition-colors"
                    >
                      Jetzt upgraden
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-[#1e3a5f] py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap gap-6 justify-center text-gray-300 text-sm">
          <Link href="/impressum" className="hover:text-white">Impressum</Link>
          <Link href="/datenschutz" className="hover:text-white">Datenschutz</Link>
          <Link href="/agb" className="hover:text-white">AGB</Link>
          <Link href="/hilfe" className="hover:text-white">Hilfe</Link>
        </div>
      </footer>

      {/* CheckoutModal für Registrierung mit Plan */}
      {checkoutPlan && (
        <CheckoutModal
          plan={checkoutPlan}
          isOpen={showCheckoutModal}
          onClose={() => {
            setShowCheckoutModal(false);
            setCheckoutPlan(null);
          }}
          onConfirm={handleCheckoutConfirm}
        />
      )}
    </div>
  );
}

// Export mit Suspense für useSearchParams
export default function DashboardPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1e3a5f] mx-auto mb-4"></div>
          <p className="text-gray-600">Lädt...</p>
        </div>
      </div>
    }>
      <DashboardContent />
    </Suspense>
  );
}
