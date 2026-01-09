'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';

// Dashboard-Typ Optionen
type DashboardType = 'basis' | 'professional' | 'lawyer';

const DASHBOARD_OPTIONS = [
  { 
    id: 'basis' as DashboardType, 
    name: 'Basis', 
    icon: '🏠', 
    desc: 'Für Mieter, Eigentümer & Vermieter',
    roles: ['Mieter', 'Eigentümer', 'Vermieter'],
    upgrade: 'Basis (19€/Monat)'
  },
  { 
    id: 'professional' as DashboardType, 
    name: 'Professional', 
    icon: '🏢', 
    desc: 'Für Investoren & Verwalter',
    roles: ['Immobilien-Investor', 'Immobilienverwalter'],
    upgrade: 'Professional (39€/Monat)'
  },
  { 
    id: 'lawyer' as DashboardType, 
    name: 'Jurist', 
    icon: '⚖️', 
    desc: 'Für Juristen',
    roles: ['Rechtsanwalt', 'Jurist'],
    upgrade: 'Lawyer Pro (69€/Monat)'
  },
];

// Wrapper-Komponente für Suspense
export default function RegisterPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#1e3a5f]"></div>
      </div>
    }>
      <RegisterContent />
    </Suspense>
  );
}

function RegisterContent() {
  const searchParams = useSearchParams();
  const planFromUrl = searchParams.get('plan') as DashboardType | null;
  
  // Wenn Plan von URL kommt, direkt zu Step 2 springen
  const [step, setStep] = useState<1 | 2>(planFromUrl ? 2 : 1);
  const [selectedDashboard, setSelectedDashboard] = useState<DashboardType>(planFromUrl || 'basis');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // Plan von URL übernehmen
  useEffect(() => {
    if (planFromUrl && ['basis', 'professional', 'lawyer'].includes(planFromUrl)) {
      setSelectedDashboard(planFromUrl);
      setStep(2); // Direkt zum Formular
    }
  }, [planFromUrl]);

  const createUserDocument = async (userId: string, userEmail: string, userName?: string) => {
    try {
      // Bestimme Standard-Rolle basierend auf Dashboard-Typ
      const defaultRole = selectedDashboard === 'basis' ? 'MIETER' 
        : selectedDashboard === 'professional' ? 'INVESTOR' 
        : 'ANWALT';

      // Free-Tier basierend auf Dashboard-Typ
      const freeTier = `free_${selectedDashboard}`;

      await setDoc(doc(db, 'users', userId), {
        email: userEmail,
        name: userName || userEmail.split('@')[0],
        tier: freeTier, // z.B. free_basis, free_professional, free_lawyer
        dashboardType: selectedDashboard,
        role: defaultRole,
        queriesUsed: 0,
        queriesLimit: 3,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        lastActivityAt: new Date().toISOString(), // Für Inaktivitäts-Tracking
      });
    } catch (err) {
      console.error('Error creating user document:', err);
      throw err;
    }
  };

  const handleEmailRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validierung
    if (password !== confirmPassword) {
      setError('Passwörter stimmen nicht überein');
      return;
    }

    if (password.length < 6) {
      setError('Passwort muss mindestens 6 Zeichen lang sein');
      return;
    }

    if (!agreedToTerms) {
      setError('Bitte akzeptieren Sie die AGB');
      return;
    }

    setLoading(true);

    try {
      // Firebase Auth Konto erstellen
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      // Firestore Dokument erstellen
      await createUserDocument(userCredential.user.uid, email, name);
      
      // Willkommens-E-Mail senden (optional)
      try {
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';
        await fetch(`${backendUrl}/email/send-welcome`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            user_email: email,
            user_name: name || email.split('@')[0],
          }),
        });
      } catch (emailErr) {
        console.error('Welcome email failed:', emailErr);
        // Nicht kritisch - weiter
      }

      // Wenn Plan von URL kommt → zum Dashboard mit checkout Parameter
      if (planFromUrl && ['basis', 'professional', 'lawyer'].includes(planFromUrl)) {
        // Zum Dashboard weiterleiten mit checkout Parameter
        // Dort wird das CheckoutModal mit AGB, Widerruf, Datenschutz angezeigt
        router.push(`/dashboard?checkout=${planFromUrl}`);
        return;
      }
      
      router.push('/dashboard');
    } catch (err: any) {
      if (err.code === 'auth/email-already-in-use') {
        setError('Diese E-Mail-Adresse wird bereits verwendet');
      } else if (err.code === 'auth/weak-password') {
        setError('Passwort ist zu schwach');
      } else {
        setError(err.message || 'Registrierung fehlgeschlagen');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h1 className="text-3xl font-bold text-[#1e3a5f]">
              domulex<span className="text-[#b8860b]">.ai</span>
            </h1>
          </Link>
          <p className="mt-2 text-gray-600">
            Erstellen Sie Ihr kostenloses Konto
          </p>
        </div>

        {/* Step Indicator */}
        <div className="flex items-center justify-center gap-4 mb-6">
          <div className={`flex items-center gap-2 ${step === 1 ? 'text-[#1e3a5f]' : 'text-gray-400'}`}>
            <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${step === 1 ? 'bg-[#1e3a5f] text-white' : 'bg-gray-200'}`}>1</span>
            <span className="text-sm font-medium">Bereich wählen</span>
          </div>
          <div className="w-8 h-0.5 bg-gray-300"></div>
          <div className={`flex items-center gap-2 ${step === 2 ? 'text-[#1e3a5f]' : 'text-gray-400'}`}>
            <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${step === 2 ? 'bg-[#1e3a5f] text-white' : 'bg-gray-200'}`}>2</span>
            <span className="text-sm font-medium">Registrieren</span>
          </div>
        </div>

        {/* Step 1: Dashboard-Auswahl */}
        {step === 1 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-2xl font-bold text-[#1e3a5f] mb-2">Wählen Sie Ihren Bereich</h2>
            <p className="text-gray-600 text-sm mb-6">Sie können alle Funktionen testen. Für Vollzugriff upgraden Sie später.</p>

            <div className="space-y-3">
              {DASHBOARD_OPTIONS.map((option) => (
                <button
                  key={option.id}
                  onClick={() => setSelectedDashboard(option.id)}
                  className={`w-full p-4 rounded-xl border-2 text-left transition-all ${
                    selectedDashboard === option.id 
                      ? 'border-[#1e3a5f] bg-[#1e3a5f]/5' 
                      : 'border-gray-200 hover:border-[#1e3a5f]/50'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div className="text-3xl">{option.icon}</div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-[#1e3a5f]">{option.name}</h3>
                        {selectedDashboard === option.id && (
                          <div className="w-5 h-5 bg-[#1e3a5f] rounded-full flex items-center justify-center">
                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                      </div>
                      <p className="text-sm text-gray-500">{option.desc}</p>
                      <div className="flex flex-wrap gap-1 mt-2">
                        {option.roles.map((role) => (
                          <span key={role} className="text-xs bg-[#1e3a5f]/10 text-[#1e3a5f] px-2 py-0.5 rounded">
                            {role}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>

            <button
              onClick={() => setStep(2)}
              className="w-full mt-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium transition-colors"
            >
              Weiter →
            </button>

            <p className="mt-4 text-center text-gray-600 text-sm">
              Haben Sie schon ein Konto?{' '}
              <Link href="/auth/login" className="text-[#1e3a5f] hover:text-[#2d4a6f] font-medium">
                Jetzt anmelden
              </Link>
            </p>
          </div>
        )}

        {/* Step 2: Register Card */}
        {step === 2 && (
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-[#1e3a5f]">Registrieren</h2>
            <button onClick={() => setStep(1)} className="text-sm text-gray-500 hover:text-[#1e3a5f]">
              ← Zurück
            </button>
          </div>

          {/* Gewählter Bereich */}
          <div className="mb-4 p-3 bg-[#1e3a5f]/5 border border-[#1e3a5f]/20 rounded-lg flex items-center gap-3">
            <span className="text-xl">{DASHBOARD_OPTIONS.find(o => o.id === selectedDashboard)?.icon}</span>
            <div>
              <span className="font-medium text-[#1e3a5f]">{DASHBOARD_OPTIONS.find(o => o.id === selectedDashboard)?.name}</span>
              <span className="text-sm text-gray-500 ml-2">Dashboard</span>
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleEmailRegister} className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                Name
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                placeholder="Max Mustermann"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                E-Mail
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                placeholder="ihre@email.de"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Passwort
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                placeholder="••••••••"
              />
              <p className="mt-1 text-xs text-gray-500">Mindestens 6 Zeichen</p>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                Passwort bestätigen
              </label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                placeholder="••••••••"
              />
            </div>

            <label className="flex items-start gap-2">
              <input
                type="checkbox"
                checked={agreedToTerms}
                onChange={(e) => setAgreedToTerms(e.target.checked)}
                className="mt-0.5 rounded border-gray-300 text-[#1e3a5f] focus:ring-[#1e3a5f]"
              />
              <span className="text-sm text-gray-600">
                Ich akzeptiere die{' '}
                <Link href="/agb" target="_blank" className="text-[#1e3a5f] hover:underline">
                  AGB
                </Link>{' '}
                und die{' '}
                <Link href="/datenschutz" target="_blank" className="text-[#1e3a5f] hover:underline">
                  Datenschutzerklärung
                </Link>
              </span>
            </label>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
            >
              {loading ? 'Wird registriert...' : 'Kostenlos registrieren'}
            </button>
          </form>

          <p className="mt-6 text-center text-gray-600 text-sm">
            Haben Sie schon ein Konto?{' '}
            <Link href="/auth/login" className="text-[#1e3a5f] hover:text-[#2d4a6f] font-medium">
              Jetzt anmelden
            </Link>
          </p>
          
          {/* E-Mail Hinweis */}
          <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
            <p className="text-xs text-amber-800">
              📧 <strong>Wichtig:</strong> Unsere E-Mails können im Spam-Ordner landen. 
              Bitte prüfen Sie auch dort und markieren Sie E-Mails von @domulex.ai als &quot;Kein Spam&quot;.
            </p>
          </div>
        </div>
        )}

        {/* Info Box - nur bei Step 1 */}
        {step === 1 && (
        <div className="mt-6 bg-[#1e3a5f]/5 border border-[#1e3a5f]/10 rounded-lg p-4">
          <h3 className="font-semibold text-[#1e3a5f] mb-2">✨ Ihr Free-Tarif beinhaltet:</h3>
          <ul className="space-y-1 text-sm text-[#1e3a5f]/80">
            <li>✓ 3 kostenlose Anfragen pro Monat</li>
            <li>✓ Zugriff auf Ihr gewähltes Dashboard</li>
            <li>✓ Alle Funktionen testen (nur Ansicht)</li>
            <li>✓ Jederzeit upgraden für Vollzugriff</li>
          </ul>
        </div>
        )}
      </div>
    </div>
  );
}
