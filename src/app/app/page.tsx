'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { auth, db } from '@/lib/firebase';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import Link from 'next/link';
import ChatInterface from '@/components/ChatInterface';
import NotificationBell from '@/components/NotificationBell';
import UpgradeModal from '@/components/UpgradeModal';

interface UserData {
  email?: string;
  tier: string;
  dashboardType?: string;
  role?: string;
  queriesUsed: number;
  queriesLimit: number;
}

function AppContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [user, setUser] = useState<any>(null);
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }

      setUser(currentUser);

      try {
        const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
        if (userDoc.exists()) {
          const data = userDoc.data() as UserData;
          setUserData(data);
        }
      } catch (err) {
        console.error('Error loading user data:', err);
      } finally {
        setLoading(false);
      }
    });

    return () => unsubscribe();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1e3a5f] mx-auto mb-4"></div>
          <p className="text-gray-600">Lädt...</p>
        </div>
      </div>
    );
  }

  const queriesRemaining = (userData?.queriesLimit || 0) - (userData?.queriesUsed || 0);
  const isLimitReached = queriesRemaining <= 0;
  const isFreeUser = userData?.tier?.startsWith('free') || userData?.tier === 'free';

  // Rolle aus URL oder User-Daten
  const roleFromUrl = searchParams.get('role');
  const currentRole = roleFromUrl || userData?.role || 'MIETER';

  // Rolle-Label für Anzeige
  const getRoleLabel = (role: string) => {
    const labels: Record<string, string> = {
      'MIETER': 'Mieter',
      'EIGENTUEMER': 'Eigentümer',
      'VERMIETER': 'Vermieter',
      'INVESTOR': 'Investor',
      'VERWALTER': 'Verwalter',
      'ANWALT': 'Jurist',
    };
    return labels[role] || role;
  };

  return (
    <div className="min-h-screen bg-[#fafaf8] flex flex-col">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            {/* Links: Dashboard zurück */}
            <Link
              href="/dashboard"
              className="text-sm text-gray-600 hover:text-[#1e3a5f] transition-colors whitespace-nowrap"
            >
              ← Dashboard
            </Link>
          
            <div className="flex items-center gap-2 sm:gap-4">
              {/* Rolle anzeigen */}
              <span className="hidden lg:inline-flex items-center gap-1 px-3 py-1 bg-[#1e3a5f]/10 text-[#1e3a5f] rounded-full text-sm">
                👤 {getRoleLabel(currentRole)}
              </span>
            
            {/* Anfragen-Counter */}
            <div className={`flex items-center gap-2 px-2 sm:px-3 py-1 rounded-full text-sm ${
              isLimitReached ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
            }`}>
              <span className="font-medium">{queriesRemaining}</span>
              <span className="hidden sm:inline">übrig</span>
            </div>
            
            {/* Notification Bell */}
            {user && <NotificationBell userId={user.uid} />}
            
            {/* Schnellstart Button */}
            <Link
              href="/app/schnellstart"
              className="flex items-center gap-1 px-3 py-1.5 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-full text-sm font-medium transition-colors"
            >
              🚀 <span className="hidden sm:inline">Schnellstart</span>
            </Link>
            
            {/* Mein Bereich Link */}
            <Link
              href="/konto"
              className="text-sm text-gray-600 hover:text-[#1e3a5f] whitespace-nowrap hidden sm:inline"
            >
              Mein Bereich
            </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Upgrade Modal */}
      <UpgradeModal 
        isOpen={showUpgradeModal} 
        onClose={() => setShowUpgradeModal(false)} 
        requiredTier="basis"
        feature="KI-Assistenten"
      />

      {/* Limit-Warnung - fixed unter Navigation */}
      {isLimitReached && (
        <div className="fixed top-16 left-0 right-0 z-40 bg-red-500 text-white py-3 px-4 text-center">
          <span className="mr-2">🚫</span>
          Ihr Anfragen-Limit ist erreicht. 
          <button onClick={() => setShowUpgradeModal(true)} className="ml-2 underline font-medium">
            Jetzt upgraden →
          </button>
        </div>
      )}

      {/* Free-User Banner - fixed unter Navigation */}
      {isFreeUser && !isLimitReached && (
        <div className="fixed top-16 left-0 right-0 z-40 bg-[#1e3a5f] text-white py-2 px-4 text-center text-sm">
          <span className="mr-2">💡</span>
          Test-Tarif: {queriesRemaining} von 3 Anfragen verbleibend
          <button onClick={() => setShowUpgradeModal(true)} className="ml-2 text-[#b8860b] font-medium hover:underline">
            Upgraden für mehr
          </button>
        </div>
      )}

      {/* Chat-Bereich - mit extra padding wenn Banner sichtbar */}
      <main className={`flex-1 max-w-4xl mx-auto w-full ${isLimitReached || (isFreeUser && !isLimitReached) ? 'pt-28' : 'pt-20'}`}>
        <ChatInterface
          jurisdiction="DE"
          role={currentRole}
          language="de"
          initialMessage={searchParams.get('prompt') || undefined}
        />
      </main>

      {/* Footer */}
      <footer className="bg-[#1e3a5f] py-4 mt-auto">
        <div className="max-w-5xl mx-auto px-4 flex flex-wrap gap-4 justify-center text-gray-300 text-xs">
          <Link href="/impressum" className="hover:text-white">Impressum</Link>
          <Link href="/datenschutz" className="hover:text-white">Datenschutz</Link>
          <Link href="/agb" className="hover:text-white">AGB</Link>
          <Link href="/hilfe" className="hover:text-white">Hilfe & Unterstützung</Link>
        </div>
        <div className="text-center text-gray-400 text-xs mt-2">
          © 2026 Home Invest & Management GmbH. Alle Rechte vorbehalten.
        </div>
      </footer>
    </div>
  );
}

export default function AppPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1e3a5f] mx-auto mb-4"></div>
          <p className="text-gray-600">Lädt...</p>
        </div>
      </div>
    }>
      <AppContent />
    </Suspense>
  );
}
