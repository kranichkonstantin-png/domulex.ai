'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '@/lib/firebase';
import Link from 'next/link';

const ADMIN_EMAILS = ['kontakt@domulex.ai', 'admin@domulex.ai'];

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);
  const router = useRouter();

  // Sofort prüfen ob bereits eingeloggt
  useEffect(() => {
    // Prefetch für schnelleren Übergang
    router.prefetch('/dashboard');
    router.prefetch('/admin');
    
    // Bereits eingeloggt? Sofort weiterleiten!
    if (auth.currentUser) {
      const emailLower = auth.currentUser.email?.toLowerCase() || '';
      if (ADMIN_EMAILS.some(e => e.toLowerCase() === emailLower)) {
        router.replace('/admin');
      } else {
        router.replace('/dashboard');
      }
      return;
    }
    setCheckingAuth(false);
  }, [router]);

  const checkAdminAndRedirect = (userEmail: string) => {
    const emailLower = userEmail.toLowerCase();
    // Prüfe Standard-Admin - sofort weiterleiten ohne Firestore
    if (ADMIN_EMAILS.some(e => e.toLowerCase() === emailLower)) {
      router.replace('/admin');
      return;
    }
    // Normale User direkt zum Dashboard
    router.replace('/dashboard');
  };

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      checkAdminAndRedirect(result.user.email || '');
    } catch (err: any) {
      setError(err.message || 'Login fehlgeschlagen');
      setLoading(false);
    }
  };

  // Während Auth-Check läuft, zeige nichts (verhindert Flackern)
  if (checkingAuth) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="animate-pulse text-[#1e3a5f] text-xl">Laden...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h1 className="text-3xl font-bold text-[#1e3a5f]">
              domulex<span className="text-[#b8860b]">.ai</span>
            </h1>
          </Link>
          <p className="mt-2 text-gray-600">
            Willkommen zurück
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <h2 className="text-2xl font-bold text-[#1e3a5f] mb-6">Anmelden</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleEmailLogin} className="space-y-4">
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
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                placeholder="••••••••"
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-[#1e3a5f] focus:ring-[#1e3a5f]" />
                <span className="ml-2 text-sm text-gray-600">Angemeldet bleiben</span>
              </label>
              <Link href="/auth/reset-password" className="text-sm text-[#1e3a5f] hover:text-[#2d4a6f]">
                Passwort vergessen?
              </Link>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
            >
              {loading ? 'Wird angemeldet...' : 'Anmelden'}
            </button>
          </form>

          <p className="mt-6 text-center text-gray-600 text-sm">
            Noch kein Konto?{' '}
            <Link href="/auth/register" className="text-[#1e3a5f] hover:text-[#2d4a6f] font-medium">
              Jetzt registrieren
            </Link>
          </p>
        </div>

        <p className="mt-6 text-center text-gray-500 text-xs">
          Mit der Anmeldung akzeptieren Sie unsere{' '}
          <Link href="/agb" className="underline hover:text-[#1e3a5f]">AGB</Link>
          {' '}und{' '}
          <Link href="/datenschutz" className="underline hover:text-[#1e3a5f]">Datenschutzerklärung</Link>
        </p>
      </div>
    </div>
  );
}
