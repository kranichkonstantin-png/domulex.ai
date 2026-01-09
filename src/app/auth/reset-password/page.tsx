'use client';

import { useState } from 'react';
import { sendPasswordResetEmail } from 'firebase/auth';
import { auth } from '@/lib/firebase';
import Link from 'next/link';

export default function ResetPasswordPage() {
  const [email, setEmail] = useState('');
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setLoading(true);

    try {
      await sendPasswordResetEmail(auth, email);
      setSuccess(true);
    } catch (err: any) {
      if (err.code === 'auth/user-not-found') {
        setError('Es gibt kein Konto mit dieser E-Mail-Adresse');
      } else {
        setError(err.message || 'Fehler beim Zurücksetzen des Passworts');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h1 className="text-4xl font-bold text-[#1e3a5f]">
              domulex<span className="text-[#b8860b]">.ai</span>
            </h1>
          </Link>
          <p className="mt-2 text-gray-600">
            Passwort zurücksetzen
          </p>
        </div>

        {/* Reset Card */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
          <h2 className="text-2xl font-bold text-[#1e3a5f] mb-6">Passwort vergessen?</h2>

          {success ? (
            <div className="space-y-4">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-700 text-sm">
                  ✅ Wir haben Ihnen eine E-Mail mit einem Link zum Zurücksetzen Ihres Passworts gesendet.
                </p>
              </div>
              <p className="text-sm text-gray-600">
                Bitte überprüfen Sie Ihr E-Mail-Postfach und folgen Sie den Anweisungen in der E-Mail.
              </p>
              <Link
                href="/auth/login"
                className="block w-full py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium text-center transition-colors"
              >
                Zurück zur Anmeldung
              </Link>
            </div>
          ) : (
            <>
              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              <p className="text-gray-600 mb-6 text-sm">
                Geben Sie Ihre E-Mail-Adresse ein und wir senden Ihnen einen Link zum Zurücksetzen Ihres Passworts.
              </p>

              <form onSubmit={handleResetPassword} className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-[#1e3a5f] mb-1">
                    E-Mail
                  </label>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#b8860b] focus:border-[#b8860b] text-[#1e3a5f]"
                    placeholder="ihre@email.de"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
                >
                  {loading ? 'Wird gesendet...' : 'Passwort zurücksetzen'}
                </button>
              </form>

              <div className="mt-6 text-center">
                <Link href="/auth/login" className="text-sm text-[#b8860b] hover:text-[#9a7209]">
                  ← Zurück zur Anmeldung
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
