'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { auth, db } from '@/lib/firebase';
import { onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc, updateDoc } from 'firebase/firestore';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';

/**
 * Kündigungsseite gemäß § 312k BGB
 * 
 * Anforderungen nach § 312k BGB:
 * 1. Leicht zugänglicher "Kündigungsbutton" auf der Website
 * 2. Einfacher Prozess ohne Hindernisse
 * 3. Bestätigungsseite mit Zusammenfassung
 * 4. Bestätigung per E-Mail (dauerhafter Datenträger)
 */

interface SubscriptionInfo {
  tier: string;
  price: number;
  subscriptionId: string | null;
  currentPeriodEnd: Date | null;
  status: string;
}

interface CancellationData {
  email: string;
  reason: string;
  confirmCancellation: boolean;
}

export default function KuendigenPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [subscription, setSubscription] = useState<SubscriptionInfo | null>(null);
  const [step, setStep] = useState<'start' | 'form' | 'confirm' | 'success' | 'error'>('start');
  const [formData, setFormData] = useState<CancellationData>({
    email: '',
    reason: '',
    confirmCancellation: false
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // User und Subscription laden
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      setUser(currentUser);
      setFormData(prev => ({ ...prev, email: currentUser.email || '' }));
      
      // Subscription-Daten aus Firestore laden
      try {
        const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          const tier = data.tier || data.subscription?.tier || 'free';
          const subscriptionId = data.stripeSubscriptionId || data.subscription?.stripeSubscriptionId || null;
          const periodEnd = data.subscription?.currentPeriodEnd;
          
          setSubscription({
            tier,
            price: tier === 'lawyer' ? 69 : tier === 'professional' ? 39 : tier === 'basis' ? 19 : 0,
            subscriptionId,
            currentPeriodEnd: periodEnd ? (periodEnd.toDate ? periodEnd.toDate() : new Date(periodEnd)) : null,
            status: data.subscription?.status || 'active'
          });
        }
      } catch (error) {
        console.error('Error loading subscription:', error);
      }
      
      setLoading(false);
    });
    return () => unsubscribe();
  }, [router]);

  const formatDate = (date: Date | null) => {
    if (!date) return 'N/A';
    return new Intl.DateTimeFormat('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(date);
  };

  const getTierName = (tier: string) => {
    switch (tier) {
      case 'lawyer': return 'Lawyer Pro';
      case 'professional': return 'Professional';
      case 'basis': return 'Basis';
      default: return 'Free';
    }
  };

  const handleStartCancellation = () => {
    setStep('form');
  };

  const handleSubmitForm = (e: React.FormEvent) => {
    e.preventDefault();
    setStep('confirm');
  };

  const handleConfirmCancellation = async () => {
    if (!subscription?.subscriptionId || !user) {
      setErrorMessage('Keine aktive Subscription gefunden.');
      setStep('error');
      return;
    }
    
    setIsProcessing(true);
    setErrorMessage('');
    
    try {
      // 1. Stripe-Kündigung an Backend senden
      const response = await fetch(`${API_URL}/stripe/cancel-subscription/${subscription.subscriptionId}?at_period_end=true`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Kündigung fehlgeschlagen');
      }
      
      const result = await response.json();
      
      // 2. Firestore aktualisieren
      await updateDoc(doc(db, 'users', user.uid), {
        'subscription.status': 'canceling',
        'subscription.cancelAtPeriodEnd': true,
        'subscription.cancelledAt': new Date().toISOString(),
        'subscription.cancellationReason': formData.reason
      });
      
      // 3. Bestätigungs-E-Mail senden (optional - Backend macht das auch über Webhook)
      try {
        await fetch(`${API_URL}/email/send-cancellation-confirmation`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            user_email: formData.email,
            user_name: user.displayName || 'Nutzer',
            tier: getTierName(subscription.tier),
            end_date: formatDate(subscription.currentPeriodEnd)
          })
        });
      } catch (emailError) {
        console.warn('Email notification failed, but cancellation succeeded:', emailError);
      }
      
      setStep('success');
      
    } catch (error) {
      console.error('Cancellation error:', error);
      setErrorMessage(error instanceof Error ? error.message : 'Ein Fehler ist aufgetreten');
      setStep('error');
    } finally {
      setIsProcessing(false);
    }
  };

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState('');
  const [deleteSuccess, setDeleteSuccess] = useState(false);

  const handleDeleteRequest = async () => {
    if (!user) return;
    
    setDeleteLoading(true);
    setDeleteError('');
    
    try {
      // Löschanfrage in Firestore speichern (Admin sieht das im Panel)
      const { collection, addDoc, serverTimestamp } = await import('firebase/firestore');
      await addDoc(collection(db, 'delete_requests'), {
        userId: user.uid,
        userEmail: user.email,
        userName: user.displayName || 'Nicht angegeben',
        createdAt: serverTimestamp(),
        status: 'pending'
      });
      
      // Bestätigung anzeigen
      alert('✅ Ihre Löschanfrage wurde erfolgreich eingereicht. Wir werden Ihren Account innerhalb von 24 Stunden löschen.');
      
      // User ausloggen
      const { signOut } = await import('firebase/auth');
      await signOut(auth);
      
      // Zur Hauptseite weiterleiten
      router.replace('/');
      
    } catch (error: any) {
      console.error('Delete request error:', error);
      setDeleteError('Fehler beim Senden der Anfrage. Bitte kontaktieren Sie support@domulex.ai');
      setDeleteLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="animate-spin text-4xl">⚙️</div>
      </div>
    );
  }

  // Keine aktive Subscription - Account löschen Option
  if (!subscription?.subscriptionId || subscription.tier === 'free' || subscription.tier?.startsWith('free')) {
    return (
      <div className="min-h-screen bg-[#fafaf8]">
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <div className="flex items-center justify-between h-16">
              <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">← Dashboard</Link>
              <Link href="/konto" className="text-gray-500 hover:text-[#1e3a5f]">Mein Konto</Link>
            </div>
          </div>
        </nav>
        <main className="max-w-2xl mx-auto px-4 pt-24 pb-12">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-8">
            <p className="text-5xl mb-4 text-center">ℹ️</p>
            <h1 className="text-2xl font-bold text-[#1e3a5f] mb-4 text-center">Kein aktives Abonnement</h1>
            <p className="text-gray-600 mb-8 text-center">
              Sie haben derzeit kein kostenpflichtiges Abonnement. Sie nutzen den kostenlosen Tarif.
            </p>
            
            {/* Account löschen Option */}
            <div className="border-t border-gray-200 pt-8 mt-8">
              <h2 className="text-lg font-semibold text-red-600 mb-4">Account löschen</h2>
              <p className="text-gray-600 mb-6 text-sm">
                Wenn Sie Ihren Account löschen, werden alle Ihre Daten unwiderruflich entfernt. 
                Diese Aktion kann nicht rückgängig gemacht werden.
              </p>
              
              {!showDeleteConfirm ? (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  className="w-full py-3 bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 transition-colors"
                >
                  Account löschen
                </button>
              ) : deleteSuccess ? (
                <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
                  <p className="text-4xl mb-3">✅</p>
                  <p className="text-green-700 font-medium mb-2">
                    Löschanfrage gesendet!
                  </p>
                  <p className="text-green-600 text-sm">
                    Wir haben Ihre Anfrage erhalten und werden Ihren Account innerhalb von 48 Stunden löschen.
                    Sie erhalten eine Bestätigung per E-Mail.
                  </p>
                </div>
              ) : (
                <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                  <p className="text-red-700 font-medium mb-4">
                    ⚠️ Möchten Sie wirklich Ihren Account löschen lassen?
                  </p>
                  <p className="text-gray-600 text-sm mb-4">
                    Nach Bestätigung wird Ihre Löschanfrage an unser Team gesendet. 
                    Die Löschung erfolgt innerhalb von 48 Stunden.
                  </p>
                  
                  {deleteError && (
                    <p className="text-red-600 text-sm mb-4 bg-red-100 p-3 rounded">{deleteError}</p>
                  )}
                  
                  <div className="flex gap-4">
                    <button
                      onClick={() => {
                        setShowDeleteConfirm(false);
                        setDeleteError('');
                      }}
                      className="flex-1 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
                      disabled={deleteLoading}
                    >
                      Abbrechen
                    </button>
                    <button
                      onClick={handleDeleteRequest}
                      className="flex-1 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
                      disabled={deleteLoading}
                    >
                      {deleteLoading ? 'Wird gesendet...' : 'Löschanfrage senden'}
                    </button>
                  </div>
                </div>
              )}
            </div>
            
            <div className="mt-8 text-center">
              <Link href="/konto" className="text-[#1e3a5f] hover:underline">
                Zurück zum Konto
              </Link>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">← Dashboard</Link>
            <Link href="/konto" className="text-gray-500 hover:text-[#1e3a5f] transition-colors">
              Mein Konto
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-2xl mx-auto px-4 pt-24 pb-12">
        {/* Step 1: Start - Kündigungsbutton gemäß § 312k BGB */}
        {step === 'start' && (
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-[#1e3a5f] mb-4">Vertrag kündigen</h1>
              <p className="text-gray-600">
                Sie können Ihr Abonnement hier jederzeit zum Ende der aktuellen Laufzeit kündigen.
              </p>
            </div>

            {/* Aktuelle Vertragsdaten */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
              <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">Ihre aktuellen Vertragsdaten</h2>
              <div className="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">Aktueller Tarif</p>
                  <p className="text-[#1e3a5f] font-medium">{getTierName(subscription.tier)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Monatlicher Preis</p>
                  <p className="text-[#1e3a5f] font-medium">{subscription.price.toFixed(2).replace('.', ',')} €</p>
                </div>
                <div>
                  <p className="text-gray-500">Status</p>
                  <p className="text-[#1e3a5f] font-medium capitalize">{subscription.status}</p>
                </div>
                <div>
                  <p className="text-gray-500">Laufzeit bis</p>
                  <p className="text-[#1e3a5f] font-medium">{formatDate(subscription.currentPeriodEnd)}</p>
                </div>
              </div>
            </div>

            {/* Kündigungsbutton - § 312k BGB konform */}
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 text-center">
              <p className="text-gray-600 mb-6">
                Wenn Sie Ihr Abonnement kündigen möchten, klicken Sie auf den folgenden Button. 
                Sie können die Kündigung im nächsten Schritt noch einmal bestätigen.
              </p>
              
              <button
                onClick={handleStartCancellation}
                className="px-8 py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-lg font-bold transition-colors"
              >
                Verträge hier kündigen
              </button>
            </div>

            {/* Alternativen */}
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">Bevor Sie kündigen...</h3>
              <p className="text-sm text-blue-700 mb-4">
                Gibt es ein Problem, bei dem wir Ihnen helfen können? Unser Support-Team steht 
                Ihnen gerne zur Verfügung.
              </p>
              <div className="flex flex-wrap gap-3">
                <Link
                  href="/hilfe"
                  className="px-4 py-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg text-sm font-medium transition-colors"
                >
                  Zum Hilfe-Center
                </Link>
                <a
                  href="mailto:kontakt@domulex.ai?subject=Frage%20zu%20meinem%20Abo"
                  className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-sm font-medium transition-colors"
                >
                  Support kontaktieren
                </a>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Kündigungsformular */}
        {step === 'form' && (
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-[#1e3a5f] mb-4">Kündigung eingeben</h1>
              <p className="text-gray-600">
                Bitte bestätigen Sie Ihre E-Mail-Adresse für die Kündigungsbestätigung.
              </p>
            </div>

            <form onSubmit={handleSubmitForm} className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-6">
              {/* E-Mail-Bestätigung */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  E-Mail-Adresse (für Bestätigung) *
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="ihre@email.de"
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 placeholder-gray-400 focus:outline-none focus:border-[#1e3a5f]"
                  required
                />
              </div>

              {/* Kündigungsgrund (optional) */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Kündigungsgrund (optional - hilft uns, besser zu werden)
                </label>
                <select
                  value={formData.reason}
                  onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:outline-none focus:border-[#1e3a5f]"
                >
                  <option value="">Bitte auswählen...</option>
                  <option value="too_expensive">Zu teuer</option>
                  <option value="not_needed">Benötige den Service nicht mehr</option>
                  <option value="missing_features">Fehlende Funktionen</option>
                  <option value="found_alternative">Nutze eine Alternative</option>
                  <option value="technical_issues">Technische Probleme</option>
                  <option value="other">Sonstiges</option>
                </select>
              </div>

              {/* Hinweise */}
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                <h4 className="font-medium text-amber-800 mb-2">Wichtige Hinweise zur Kündigung:</h4>
                <ul className="text-sm text-amber-700 space-y-2">
                  <li>• Die Kündigung wird zum Ende der aktuellen Abrechnungsperiode ({formatDate(subscription.currentPeriodEnd)}) wirksam.</li>
                  <li>• Sie können den Service bis dahin weiterhin uneingeschränkt nutzen.</li>
                  <li>• Sie erhalten eine Bestätigung per E-Mail an {formData.email}.</li>
                  <li>• Ihre Daten bleiben 30 Tage nach Vertragsende gespeichert.</li>
                </ul>
              </div>

              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setStep('start')}
                  className="flex-1 py-3 px-6 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
                >
                  Zurück
                </button>
                <button
                  type="submit"
                  className="flex-1 py-3 px-6 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
                >
                  Weiter zur Bestätigung
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Step 3: Bestätigung */}
        {step === 'confirm' && (
          <div className="space-y-8">
            <div className="text-center">
              <h1 className="text-3xl font-bold text-[#1e3a5f] mb-4">Kündigung bestätigen</h1>
              <p className="text-gray-600">
                Bitte überprüfen Sie Ihre Angaben und bestätigen Sie die Kündigung.
              </p>
            </div>

            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 space-y-6">
              {/* Zusammenfassung */}
              <div>
                <h3 className="text-lg font-semibold text-[#1e3a5f] mb-4">Zusammenfassung</h3>
                <div className="bg-gray-50 rounded-lg p-4 space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Gekündigter Tarif:</span>
                    <span className="text-[#1e3a5f] font-medium">{getTierName(subscription.tier)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Monatlicher Preis:</span>
                    <span className="text-[#1e3a5f] font-medium">{subscription.price.toFixed(2).replace('.', ',')} €</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Kündigungsdatum:</span>
                    <span className="text-[#1e3a5f] font-medium">{formatDate(new Date())}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Zugang bis:</span>
                    <span className="text-[#1e3a5f] font-medium">{formatDate(subscription.currentPeriodEnd)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Bestätigung an:</span>
                    <span className="text-[#1e3a5f] font-medium">{formData.email}</span>
                  </div>
                </div>
              </div>

              {/* Bestätigungs-Checkbox */}
              <div className="space-y-3">
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.confirmCancellation}
                    onChange={(e) => setFormData({ ...formData, confirmCancellation: e.target.checked })}
                    className="w-5 h-5 mt-0.5 text-red-600 rounded"
                  />
                  <span className="text-sm text-gray-600">
                    Ich bestätige, dass ich mein <strong className="text-[#1e3a5f]">{getTierName(subscription.tier)}</strong>-Abonnement 
                    zum Ende der Laufzeit ({formatDate(subscription.currentPeriodEnd)}) kündigen möchte. 
                    Die Kündigung wird automatisch an Stripe übermittelt.
                  </span>
                </label>
              </div>

              {/* Endgültig kündigen Button */}
              <div className="pt-4 border-t border-gray-100">
                <button
                  onClick={handleConfirmCancellation}
                  disabled={!formData.confirmCancellation || isProcessing}
                  className="w-full py-4 px-6 bg-red-600 hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg text-lg font-bold transition-colors"
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
                    'Jetzt endgültig kündigen'
                  )}
                </button>
                <p className="text-xs text-gray-500 text-center mt-2">
                  Die Kündigung wird sofort an Stripe übermittelt.
                </p>
              </div>

              <div className="flex justify-center">
                <button
                  onClick={() => setStep('form')}
                  className="text-gray-500 hover:text-[#1e3a5f] text-sm transition-colors"
                >
                  ← Zurück zum Formular
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Erfolg */}
        {step === 'success' && (
          <div className="space-y-8 text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            
            <div>
              <h1 className="text-3xl font-bold text-[#1e3a5f] mb-4">Kündigung erfolgreich</h1>
              <p className="text-gray-600">
                Ihre Kündigung wurde erfolgreich an Stripe übermittelt.
              </p>
            </div>

            <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6 text-left">
              <h3 className="text-lg font-semibold text-[#1e3a5f] mb-4">✅ Bestätigung</h3>
              <div className="space-y-3 text-sm">
                <p className="text-gray-600">
                  Ihr <strong className="text-[#1e3a5f]">{getTierName(subscription.tier)}</strong>-Abonnement wurde gekündigt.
                </p>
                <p className="text-gray-600">
                  Sie können den Service noch bis zum <strong className="text-[#1e3a5f]">{formatDate(subscription.currentPeriodEnd)}</strong> nutzen.
                </p>
                <p className="text-gray-600">
                  Eine Bestätigungs-E-Mail wird an <strong className="text-[#1e3a5f]">{formData.email}</strong> gesendet.
                </p>
                <p className="text-gray-600">
                  Danach wird Ihr Konto automatisch auf den kostenlosen Tarif umgestellt.
                </p>
              </div>
            </div>

            <Link
              href="/konto"
              className="inline-block px-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium transition-colors"
            >
              Zurück zum Konto
            </Link>
          </div>
        )}

        {/* Fehler */}
        {step === 'error' && (
          <div className="space-y-8 text-center">
            <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto">
              <span className="text-4xl">❌</span>
            </div>
            
            <div>
              <h1 className="text-3xl font-bold text-[#1e3a5f] mb-4">Fehler bei der Kündigung</h1>
              <p className="text-gray-600 mb-4">
                {errorMessage || 'Ein unerwarteter Fehler ist aufgetreten.'}
              </p>
            </div>

            <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
              <p className="text-amber-800 mb-4">
                Bitte versuchen Sie es erneut oder kontaktieren Sie unseren Support.
              </p>
              <div className="flex flex-wrap justify-center gap-3">
                <button
                  onClick={() => setStep('confirm')}
                  className="px-6 py-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium transition-colors"
                >
                  Erneut versuchen
                </button>
                <a
                  href="mailto:kontakt@domulex.ai?subject=Problem%20bei%20Kündigung"
                  className="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
                >
                  Support kontaktieren
                </a>
              </div>
            </div>

            <Link
              href="/konto"
              className="inline-block text-gray-500 hover:text-[#1e3a5f]"
            >
              Zurück zum Konto
            </Link>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-[#1e3a5f] py-6 mt-12">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Home Invest & Management GmbH • 
            <Link href="/impressum" className="text-gray-300 hover:text-white ml-2">Impressum</Link> • 
            <Link href="/datenschutz" className="text-gray-300 hover:text-white ml-2">Datenschutz</Link>
          </p>
        </div>
      </footer>
    </div>
  );
}
