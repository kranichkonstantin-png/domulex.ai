'use client';

import { useState } from 'react';
import { registerWithEmail, loginWithEmail, resetPassword } from '@/lib/auth';
import { useRouter } from 'next/navigation';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode?: 'register' | 'login' | 'reset';
  onSuccess?: () => void;
}

export default function AuthModal({ isOpen, onClose, mode = 'register', onSuccess }: AuthModalProps) {
  const [currentMode, setCurrentMode] = useState<'register' | 'login' | 'reset'>(mode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const router = useRouter();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      if (currentMode === 'register') {
        await registerWithEmail(email, password, displayName);
        setSuccess('Registrierung erfolgreich! Bitte bestätigen Sie Ihre E-Mail-Adresse.');
        setTimeout(() => {
          onSuccess?.();
          router.push('/app');
        }, 2000);
      } else if (currentMode === 'login') {
        await loginWithEmail(email, password);
        setSuccess('Login erfolgreich!');
        setTimeout(() => {
          onSuccess?.();
          router.push('/app');
        }, 1000);
      } else if (currentMode === 'reset') {
        await resetPassword(email);
        setSuccess('Passwort-Reset-Link wurde an Ihre E-Mail gesendet.');
        setTimeout(() => setCurrentMode('login'), 2000);
      }
    } catch (err: any) {
      setError(err.message || 'Ein Fehler ist aufgetreten');
    } finally {
      setLoading(false);
    }
  };

  const getModeConfig = () => {
    if (currentMode === 'register') {
      return {
        title: 'Kostenlos registrieren',
        subtitle: 'Erstellen Sie ein kostenloses Konto und erhalten Sie 3 Test-Anfragen.',
        buttonText: 'Jetzt registrieren',
        switchText: 'Bereits ein Konto?',
        switchAction: 'Anmelden',
      };
    } else if (currentMode === 'login') {
      return {
        title: 'Willkommen zurück!',
        subtitle: 'Melden Sie sich an, um fortzufahren.',
        buttonText: 'Anmelden',
        switchText: 'Noch kein Konto?',
        switchAction: 'Registrieren',
      };
    } else {
      return {
        title: 'Passwort zurücksetzen',
        subtitle: 'Geben Sie Ihre E-Mail-Adresse ein, um Ihr Passwort zurückzusetzen.',
        buttonText: 'Reset-Link senden',
        switchText: 'Zurück zur',
        switchAction: 'Anmeldung',
      };
    }
  };

  const config = getModeConfig();

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-md w-full border border-gray-200 overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-indigo-600">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white">{config.title}</h2>
              <p className="text-blue-100 mt-1 text-sm">{config.subtitle}</p>
            </div>
            <button
              onClick={onClose}
              className="text-white/80 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Error/Success Messages */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}
          {success && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
              {success}
            </div>
          )}

          {/* Name Field (nur bei Registrierung) */}
          {currentMode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Name (optional)
              </label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Ihr Name"
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
            </div>
          )}

          {/* Email Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              E-Mail
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="ihre@email.de"
              className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              required
            />
          </div>

          {/* Password Field (nicht bei Reset) */}
          {currentMode !== 'reset' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Passwort
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Mindestens 6 Zeichen"
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                required
                minLength={6}
              />
              {currentMode === 'login' && (
                <button
                  type="button"
                  onClick={() => setCurrentMode('reset')}
                  className="text-sm text-blue-600 hover:text-blue-700 mt-1"
                >
                  Passwort vergessen?
                </button>
              )}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Bitte warten...' : config.buttonText}
          </button>

          {/* Switch Mode */}
          <div className="text-center text-sm text-gray-600">
            {config.switchText}{' '}
            <button
              type="button"
              onClick={() => setCurrentMode(currentMode === 'register' ? 'login' : 'register')}
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              {config.switchAction}
            </button>
          </div>

          {/* Legal */}
          {currentMode === 'register' && (
            <p className="text-xs text-gray-500 text-center">
              Mit der Registrierung akzeptieren Sie unsere{' '}
              <a href="/agb" target="_blank" className="text-blue-600 hover:underline">
                AGB
              </a>{' '}
              und{' '}
              <a href="/datenschutz" target="_blank" className="text-blue-600 hover:underline">
                Datenschutzerklärung
              </a>
              .
            </p>
          )}
        </form>
      </div>
    </div>
  );
}
