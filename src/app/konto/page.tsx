'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { doc, getDoc, updateDoc, increment } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Logo from '@/components/Logo';

interface UserDocument {
  id: string;
  name: string;
  description: string;
  type: 'agb' | 'widerruf' | 'datenschutz' | 'rechnung';
  date: Date;
  downloadUrl: string;
}

// Vertragsdokumente
const getContractDocuments = (tier: string): UserDocument[] => {
  const baseDocs = [
    {
      id: '1',
      name: 'Allgemeine Geschäftsbedingungen',
      description: 'AGB zum Zeitpunkt Ihres Vertragsabschlusses (Dezember 2025)',
      type: 'agb' as const,
      date: new Date('2025-12-27'),
      downloadUrl: '/agb'
    },
    {
      id: '2',
      name: 'Widerrufsbelehrung',
      description: 'Widerrufsbelehrung inkl. Muster-Widerrufsformular',
      type: 'widerruf' as const,
      date: new Date('2025-12-27'),
      downloadUrl: '/downloads/widerrufsbelehrung.html'
    },
    {
      id: '3',
      name: 'Datenschutzerklärung',
      description: 'Aktuelle Datenschutzerklärung',
      type: 'datenschutz' as const,
      date: new Date('2025-12-27'),
      downloadUrl: '/datenschutz'
    }
  ];
  
  // Für Professional und Lawyer zusätzliche Dokumente
  if (tier === 'professional' || tier === 'lawyer') {
    baseDocs.push({
      id: '4',
      name: 'Auftragsverarbeitungsvertrag (AVV)',
      description: 'AVV gemäß Art. 28 DSGVO für geschäftliche Nutzung',
      type: 'agb' as const,
      date: new Date('2025-12-27'),
      downloadUrl: '/avv'
    });
  }
  
  // Für Lawyer zusätzlich NDA
  if (tier === 'lawyer') {
    baseDocs.push({
      id: '5',
      name: 'Geheimhaltungsvereinbarung (NDA)',
      description: 'Vertraulichkeitsvereinbarung für Anwälte',
      type: 'agb' as const,
      date: new Date('2025-12-27'),
      downloadUrl: '/nda'
    });
  }
  
  return baseDocs;
};

export default function KontoPage() {
  const router = useRouter();
  const [activeSection, setActiveSection] = useState<'overview' | 'documents' | 'subscription' | 'settings' | 'data'>('overview');
  const [user, setUser] = useState<any>(null);
  const [userData, setUserData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [userInvoices, setUserInvoices] = useState<any[]>([]);
  const [loadingInvoices, setLoadingInvoices] = useState(false);
  const [showQueryPackModal, setShowQueryPackModal] = useState(false);
  const [purchasingPack, setPurchasingPack] = useState(false);
  
  // Data Export/Import State
  const [exporting, setExporting] = useState(false);
  const [importing, setImporting] = useState(false);
  const [exportFormat, setExportFormat] = useState<'json' | 'csv' | 'excel'>('json');
  const [importResult, setImportResult] = useState<{success: boolean; message: string} | null>(null);
  
  const BACKEND_URL = 'https://domulex-backend-841507936108.europe-west3.run.app';
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    company: '',
    address: '',
    zipCode: '',
    city: '',
    country: 'Deutschland'
  });

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        setUser(firebaseUser);
        // Lade User-Daten aus Firestore
        try {
          const userDoc = await getDoc(doc(db, 'users', firebaseUser.uid));
          if (userDoc.exists()) {
            const data = userDoc.data();
            setUserData(data);
            // Initialisiere Formulardaten
            setFormData({
              name: data.name || '',
              phone: data.phone || '',
              company: data.company || '',
              address: data.address || '',
              zipCode: data.zipCode || '',
              city: data.city || '',
              country: data.country || 'Deutschland'
            });
          }
        } catch (error) {
          console.error('Fehler beim Laden der Userdaten:', error);
        }
      } else {
        router.push('/auth/login');
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, [router]);

  // Load user invoices
  const loadUserInvoices = async () => {
    if (!user) return;
    
    setLoadingInvoices(true);
    try {
      const token = await user.getIdToken();
      const response = await fetch(`${BACKEND_URL}/user/invoices`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUserInvoices(data.invoices || []);
      }
    } catch (err) {
      console.error('Error loading invoices:', err);
    } finally {
      setLoadingInvoices(false);
    }
  };

  // Format Unix timestamp
  const formatUnixDate = (timestamp: number) => {
    if (!timestamp) return '-';
    return new Date(timestamp * 1000).toLocaleDateString('de-DE');
  };

  const handleSaveSettings = async () => {
    if (!user) return;
    
    setSaving(true);
    setSaveSuccess(false);
    try {
      await updateDoc(doc(db, 'users', user.uid), {
        name: formData.name,
        phone: formData.phone,
        company: formData.company,
        address: formData.address,
        zipCode: formData.zipCode,
        city: formData.city,
        country: formData.country,
        updatedAt: new Date()
      });
      
      // Update local state
      setUserData({ ...userData, ...formData });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      console.error('Fehler beim Speichern:', error);
      alert('Fehler beim Speichern der Daten');
    } finally {
      setSaving(false);
    }
  };

  const handleStripePortal = async () => {
    if (!user || !userData?.stripeCustomerId) {
      alert('Kein aktives Stripe-Abonnement gefunden');
      return;
    }

    try {
      const token = await user.getIdToken();
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';
      
      // Backend erwartet Form-Daten
      const formData = new URLSearchParams();
      formData.append('customer_id', userData.stripeCustomerId);
      formData.append('return_url', window.location.href);
      
      const response = await fetch(`${backendUrl}/stripe/create-portal-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();
      if (data.portal_url) {
        window.location.href = data.portal_url;
      } else {
        throw new Error('Keine Portal-URL erhalten');
      }
    } catch (error) {
      console.error('Fehler beim Öffnen des Stripe-Portals:', error);
      alert('Fehler beim Öffnen der Abo-Verwaltung');
    }
  };

  // Data Export
  const handleExport = async (exportType: 'mandanten' | 'objekte' | 'all') => {
    if (!user) return;
    
    setExporting(true);
    try {
      const token = await user.getIdToken();
      
      const response = await fetch(`${BACKEND_URL}/data/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          export_type: exportType,
          format: exportFormat
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Export fehlgeschlagen');
      }

      const result = await response.json();
      
      // Download erstellen
      let blob: Blob;
      let fileExtension: string;
      
      if (exportFormat === 'excel') {
        // Excel kommt als Base64
        const binaryString = atob(result.data);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        blob = new Blob([bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        fileExtension = 'xlsx';
      } else if (exportFormat === 'json') {
        blob = new Blob([JSON.stringify(result.data, null, 2)], { type: 'application/json' });
        fileExtension = 'json';
      } else {
        blob = new Blob([result.data], { type: 'text/csv' });
        fileExtension = 'csv';
      }
      
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `domulex_export_${exportType}_${new Date().toISOString().split('T')[0]}.${fileExtension}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
    } catch (error: any) {
      console.error('Export error:', error);
      alert(error.message || 'Fehler beim Export');
    } finally {
      setExporting(false);
    }
  };

  // Data Import
  const handleImport = async (event: React.ChangeEvent<HTMLInputElement>, importType: 'mandanten' | 'objekte') => {
    const file = event.target.files?.[0];
    if (!file || !user) return;
    
    setImporting(true);
    setImportResult(null);
    
    try {
      let importData: any[];
      
      if (file.name.endsWith('.json')) {
        const content = await file.text();
        const parsed = JSON.parse(content);
        importData = parsed[importType] || parsed.data || parsed;
        if (!Array.isArray(importData)) {
          importData = [importData];
        }
      } else if (file.name.endsWith('.csv')) {
        const content = await file.text();
        // Simple CSV parsing
        const lines = content.split('\n').filter(l => l.trim());
        if (lines.length < 2) throw new Error('CSV-Datei muss mindestens Header und eine Datenzeile enthalten');
        
        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
        importData = lines.slice(1).map(line => {
          const values = line.split(',').map(v => v.trim().replace(/"/g, ''));
          const obj: any = {};
          headers.forEach((h, i) => { obj[h] = values[i] || ''; });
          return obj;
        });
      } else if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
        // Excel Import - read as ArrayBuffer and parse
        const arrayBuffer = await file.arrayBuffer();
        const bytes = new Uint8Array(arrayBuffer);
        
        // Send to backend for parsing
        const token = await user.getIdToken();
        const formData = new FormData();
        formData.append('file', file);
        formData.append('import_type', importType);
        
        const response = await fetch(`${BACKEND_URL}/data/import-excel`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || 'Excel-Import fehlgeschlagen');
        }

        const result = await response.json();
        setImportResult({
          success: true,
          message: `✅ Import erfolgreich: ${result.imported} importiert, ${result.skipped} übersprungen`
        });
        setImporting(false);
        event.target.value = '';
        return;
      } else {
        throw new Error('Nur JSON, CSV und Excel (.xlsx) Dateien werden unterstützt');
      }

      const token = await user.getIdToken();
      
      const response = await fetch(`${BACKEND_URL}/data/import`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          import_type: importType,
          data: importData,
          merge_strategy: 'skip'
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Import fehlgeschlagen');
      }

      const result = await response.json();
      setImportResult({
        success: true,
        message: `✅ Import erfolgreich: ${result.imported} importiert, ${result.skipped} übersprungen`
      });
      
    } catch (error: any) {
      console.error('Import error:', error);
      setImportResult({
        success: false,
        message: `❌ Fehler: ${error.message}`
      });
    } finally {
      setImporting(false);
      // Reset file input
      event.target.value = '';
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      router.push('/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  // Anfragen-Paket kaufen
  const handlePurchaseQueryPack = async () => {
    if (!user) return;
    
    setPurchasingPack(true);
    try {
      const token = await user.getIdToken();
      const packType = normalizedTier === 'basis' ? 'basis' : 'professional';
      
      const response = await fetch(`${BACKEND_URL}/stripe/create-query-pack-checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          pack_type: packType,
          success_url: `${window.location.origin}/konto?pack_success=true`,
          cancel_url: window.location.href
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Checkout konnte nicht erstellt werden');
      }

      const { checkout_url } = await response.json();
      window.location.href = checkout_url;
    } catch (error) {
      console.error('Query pack checkout error:', error);
      alert('Fehler beim Checkout. Bitte versuchen Sie es erneut.');
    } finally {
      setPurchasingPack(false);
    }
  };

  // Normalisiere tier (legacy support für mieter_plus)
  const normalizedTier = userData?.tier === 'mieter_plus' ? 'basis' : userData?.tier;

  // Helper to safely parse dates from Firestore
  const parseDate = (value: any): Date | null => {
    if (!value) return null;
    // Firestore Timestamp
    if (value.toDate && typeof value.toDate === 'function') {
      return value.toDate();
    }
    // String or number
    const parsed = new Date(value);
    return isNaN(parsed.getTime()) ? null : parsed;
  };

  // Subscription basierend auf userData
  const subscription = {
    plan: normalizedTier === 'lawyer' ? 'Lawyer Pro 69€' : 
          normalizedTier === 'professional' ? 'Professional 39€' : 
          normalizedTier === 'basis' ? 'Basis 19€' : 'Kostenlos',
    status: normalizedTier && normalizedTier !== 'free' ? 'active' : 'inactive',
    price: normalizedTier === 'lawyer' ? 69 : 
           normalizedTier === 'professional' ? 39 : 
           normalizedTier === 'basis' ? 19 : 0,
    nextBilling: parseDate(userData?.subscriptionEnd),
    startDate: parseDate(userData?.subscriptionStart) || new Date(),
  };

  const formatDate = (date: Date | null | undefined) => {
    if (!date || isNaN(date.getTime())) {
      return '-';
    }
    try {
      return new Intl.DateTimeFormat('de-DE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }).format(date);
    } catch {
      return '-';
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR'
    }).format(price);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1e3a5f]"></div>
      </div>
    );
  }

  const displayName = userData?.name || user?.displayName || user?.email?.split('@')[0] || 'Nutzer';
  const displayEmail = user?.email || '';

  // Query Pack Modal
  const QueryPackModal = () => {
    if (!showQueryPackModal) return null;
    
    const isBasic = normalizedTier === 'basis';
    const packQueries = isBasic ? 20 : 50;
    const packPrice = isBasic ? 5 : 10;
    const pricePerQuery = (packPrice / packQueries).toFixed(2);
    
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
          <div className="text-center">
            <div className="w-16 h-16 bg-[#b8860b]/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🔋</span>
            </div>
            <h3 className="text-xl font-bold text-[#1e3a5f] mb-2">Anfragen nachkaufen</h3>
            <p className="text-gray-600 mb-4">
              Erweitern Sie Ihr Kontingent mit zusätzlichen KI-Anfragen.
            </p>
            
            <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d5a8f] rounded-xl p-6 text-white mb-6">
              <div className="text-4xl font-bold mb-1">{packQueries} Anfragen</div>
              <div className="text-2xl font-semibold mb-2">{packPrice},00 € <span className="text-sm font-normal opacity-80">inkl. MwSt.</span></div>
              <div className="text-sm opacity-80">nur {pricePerQuery} € pro Anfrage</div>
            </div>
            
            <div className="text-left bg-gray-50 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-600 mb-2">✓ Sofort verfügbar nach Zahlung</p>
              <p className="text-sm text-gray-600 mb-2">✓ Keine Laufzeit - niemals ablaufend</p>
              <p className="text-sm text-gray-600">✓ Sichere Zahlung via Stripe</p>
            </div>
            
            <div className="flex gap-3">
              <button 
                onClick={() => setShowQueryPackModal(false)} 
                className="flex-1 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
              >
                Abbrechen
              </button>
              <button 
                onClick={handlePurchaseQueryPack} 
                disabled={purchasingPack}
                className="flex-1 py-3 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-lg font-medium transition-colors disabled:opacity-50"
              >
                {purchasingPack ? 'Wird geladen...' : 'Jetzt kaufen'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Query Pack Modal */}
      <QueryPackModal />
      
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-[106px]">
            <div className="flex items-center gap-6">
              <Logo size="sm" />
              <Link 
                href="/dashboard" 
                className="text-gray-600 hover:text-[#1e3a5f] transition-colors"
              >
                ← Zum Dashboard
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-gray-600 hidden md:inline text-sm">{displayEmail}</span>
              <button 
                onClick={handleLogout}
                className="px-3 py-1.5 text-sm text-gray-600 hover:text-white hover:bg-[#1e3a5f] border border-gray-300 hover:border-[#1e3a5f] rounded-lg transition-colors"
              >
                Abmelden
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 pt-32 pb-8">
        {/* Mobile Navigation - Tab Bar */}
        <nav className="md:hidden mb-6">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-2">
            <div className="flex overflow-x-auto gap-1 -mx-1 px-1 scrollbar-hide">
              <button
                onClick={() => setActiveSection('overview')}
                className={`flex-shrink-0 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeSection === 'overview'
                    ? 'bg-[#1e3a5f] text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📊 Übersicht
              </button>
              <button
                onClick={() => setActiveSection('documents')}
                className={`flex-shrink-0 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeSection === 'documents'
                    ? 'bg-[#1e3a5f] text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📄 Dokumente
              </button>
              <button
                onClick={() => setActiveSection('subscription')}
                className={`flex-shrink-0 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeSection === 'subscription'
                    ? 'bg-[#1e3a5f] text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                💳 Abo
              </button>
              <button
                onClick={() => setActiveSection('settings')}
                className={`flex-shrink-0 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeSection === 'settings'
                    ? 'bg-[#1e3a5f] text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                ⚙️ Einstellungen
              </button>
              {(normalizedTier === 'professional' || normalizedTier === 'lawyer') && (
                <button
                  onClick={() => setActiveSection('data')}
                  className={`flex-shrink-0 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    activeSection === 'data'
                      ? 'bg-[#1e3a5f] text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📥 Daten
                </button>
              )}
            </div>
          </div>
        </nav>

        <div className="flex gap-8">
        {/* Desktop Sidebar Navigation */}
        <nav className="hidden md:block w-64 flex-shrink-0">
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
            <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">Mein Bereich</h2>
            <ul className="space-y-1">
              <li>
                <button
                  onClick={() => setActiveSection('overview')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    activeSection === 'overview'
                      ? 'bg-[#1e3a5f] text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📊 Übersicht
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection('documents')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    activeSection === 'documents'
                      ? 'bg-[#1e3a5f] text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📄 Dokumente
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection('subscription')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    activeSection === 'subscription'
                      ? 'bg-[#1e3a5f] text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  💳 Abonnement
                </button>
              </li>
              <li>
                <button
                  onClick={() => setActiveSection('settings')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    activeSection === 'settings'
                      ? 'bg-[#1e3a5f] text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  ⚙️ Einstellungen
                </button>
              </li>
              {(normalizedTier === 'professional' || normalizedTier === 'lawyer') && (
                <li>
                  <button
                    onClick={() => setActiveSection('data')}
                    className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                      activeSection === 'data'
                        ? 'bg-[#1e3a5f] text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    📥 Daten Import/Export
                  </button>
                </li>
              )}
            </ul>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1">
          {/* Overview Section */}
          {activeSection === 'overview' && (
            <div className="space-y-6">
              <h1 className="text-2xl font-bold text-[#1e3a5f]">Hallo, {displayName}!</h1>
              
              {/* User Info */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">Ihre Daten</h2>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-gray-500 text-sm">Name</p>
                    <p className="text-[#1e3a5f] font-medium">{displayName || '-'}</p>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">E-Mail</p>
                    <p className="text-[#1e3a5f] font-medium">{displayEmail}</p>
                  </div>
                  {formData.phone && (
                    <div>
                      <p className="text-gray-500 text-sm">Telefon</p>
                      <p className="text-[#1e3a5f] font-medium">{formData.phone}</p>
                    </div>
                  )}
                  {formData.company && (
                    <div>
                      <p className="text-gray-500 text-sm">Unternehmen</p>
                      <p className="text-[#1e3a5f] font-medium">{formData.company}</p>
                    </div>
                  )}
                  {formData.address && (
                    <div className="md:col-span-2">
                      <p className="text-gray-500 text-sm">Adresse</p>
                      <p className="text-[#1e3a5f] font-medium">
                        {formData.address}
                        {formData.zipCode || formData.city ? (
                          <>, {formData.zipCode} {formData.city}</>
                        ) : null}
                        {formData.country && formData.country !== 'Deutschland' && (
                          <>, {formData.country}</>
                        )}
                      </p>
                    </div>
                  )}
                </div>
                {(!formData.name || !formData.address) && (
                  <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg flex items-start gap-2">
                    <span className="text-amber-600">⚠️</span>
                    <div className="text-sm text-amber-700">
                      <p className="font-medium">Profil unvollständig</p>
                      <p>Bitte vervollständigen Sie Ihre Daten in den <button onClick={() => setActiveSection('settings')} className="underline hover:no-underline">Einstellungen</button>.</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Stats */}
              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <p className="text-gray-500 text-sm">Aktiver Tarif</p>
                  <p className="text-2xl font-bold text-[#1e3a5f] mt-1">{subscription.plan}</p>
                </div>
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <p className="text-gray-500 text-sm">Nächste Abrechnung</p>
                  <p className="text-2xl font-bold text-[#1e3a5f] mt-1">
                    {subscription.nextBilling ? formatDate(subscription.nextBilling) : '-'}
                  </p>
                </div>
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                  <p className="text-gray-500 text-sm">Verbleibende Anfragen</p>
                  <p className="text-2xl font-bold text-[#1e3a5f] mt-1">
                    {normalizedTier === 'lawyer' ? '∞ Unbegrenzt' :
                     `${Math.max(0, (userData?.queriesLimit || 3) - (userData?.queriesUsed || 0))} / ${userData?.queriesLimit || 3}`}
                  </p>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">Schnellzugriff</h2>
                <div className="grid md:grid-cols-2 gap-4">
                  <button
                    onClick={() => setActiveSection('documents')}
                    className="p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors text-left"
                  >
                    <p className="font-medium text-[#1e3a5f]">📄 Vertragsdokumente</p>
                    <p className="text-sm text-gray-500 mt-1">AGB & Widerrufsbelehrung herunterladen</p>
                  </button>
                  <button
                    onClick={() => setActiveSection('subscription')}
                    className="p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors text-left"
                  >
                    <p className="font-medium text-[#1e3a5f]">💳 Abonnement</p>
                    <p className="text-sm text-gray-500 mt-1">Tarif und Zahlungen verwalten</p>
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Documents Section */}
          {activeSection === 'documents' && (
            <div className="space-y-6">
              <h1 className="text-2xl font-bold text-[#1e3a5f]">Meine Dokumente</h1>
              
              <p className="text-gray-600">
                Hier finden Sie alle Vertragsdokumente zum Download. Die Dokumente entsprechen 
                dem Stand bei Ihrem Vertragsabschluss.
              </p>

              {/* Vertragsdokumente */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                <div className="p-4 border-b border-gray-100 bg-gray-50">
                  <h2 className="text-lg font-semibold text-[#1e3a5f]">Vertragsdokumente</h2>
                </div>
                <div className="divide-y divide-gray-100">
                  {getContractDocuments(normalizedTier || 'free').map((doc) => (
                    <div key={doc.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between hover:bg-gray-50 transition-colors gap-3">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-[#1e3a5f]/10 rounded-lg flex items-center justify-center">
                          {doc.type === 'agb' && <span className="text-lg">📋</span>}
                          {doc.type === 'widerruf' && <span className="text-lg">↩️</span>}
                          {doc.type === 'datenschutz' && <span className="text-lg">🔒</span>}
                          {doc.type === 'rechnung' && <span className="text-lg">🧾</span>}
                        </div>
                        <div>
                          <p className="font-medium text-[#1e3a5f]">{doc.name}</p>
                          <p className="text-sm text-gray-500">{doc.description}</p>
                          <p className="text-xs text-gray-400 mt-1">Stand: {formatDate(doc.date)}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 flex-shrink-0 mt-2 sm:mt-0">
                        {doc.type === 'agb' && (
                          <Link
                            href="/agb"
                            target="_blank"
                            className="px-3 py-2 text-sm text-gray-500 hover:text-[#1e3a5f] transition-colors hidden sm:inline"
                          >
                            Ansehen
                          </Link>
                        )}
                        {doc.type === 'widerruf' && (
                          <Link
                            href="/agb#widerruf"
                            target="_blank"
                            className="px-3 py-2 text-sm text-gray-500 hover:text-[#1e3a5f] transition-colors hidden sm:inline"
                          >
                            Ansehen
                          </Link>
                        )}
                        {doc.type === 'datenschutz' && (
                          <Link
                            href="/datenschutz"
                            target="_blank"
                            className="px-3 py-2 text-sm text-gray-500 hover:text-[#1e3a5f] transition-colors hidden sm:inline"
                          >
                            Ansehen
                          </Link>
                        )}
                        <a
                          href={doc.downloadUrl}
                          target="_blank"
                          className="flex items-center gap-2 px-4 py-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg text-sm font-medium transition-colors"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                          Herunterladen
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Widerrufsformular */}
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-amber-800 mb-2">Widerruf erklären</h3>
                <p className="text-sm text-amber-700 mb-4">
                  Sie können Ihren Vertrag innerhalb von 14 Tagen nach Vertragsabschluss 
                  ohne Angabe von Gründen widerrufen. Dies gilt für private und gewerbliche Nutzer.
                  Nutzen Sie das Muster-Widerrufsformular oder 
                  senden Sie eine formlose Erklärung an kontakt@domulex.ai.
                </p>
                <div className="flex flex-col sm:flex-row gap-3">
                  <a
                    href="/downloads/widerrufsformular.html"
                    target="_blank"
                    className="flex items-center justify-center gap-2 px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-sm font-medium transition-colors"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Widerrufsformular öffnen
                  </a>
                  <a
                    href="mailto:kontakt@domulex.ai?subject=Widerruf%20meines%20Vertrages"
                    className="flex items-center justify-center gap-2 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    ✉️ Per E-Mail widerrufen
                  </a>
                </div>
              </div>
            </div>
          )}

          {/* Subscription Section */}
          {activeSection === 'subscription' && (
            <div className="space-y-6">
              <h1 className="text-2xl font-bold text-[#1e3a5f]">Mein Abonnement</h1>
              
              {/* Current Plan */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <p className="text-gray-500 text-sm">Aktueller Tarif</p>
                    <p className="text-2xl font-bold text-[#1e3a5f] mt-1">{subscription.plan}</p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                    subscription.status === 'active' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-gray-100 text-gray-700'
                  }`}>
                    {subscription.status === 'active' ? '✓ Aktiv' : 'Kostenlos'}
                  </div>
                </div>
                
                <div className="grid md:grid-cols-2 gap-4 mb-6">
                  <div>
                    <p className="text-gray-500 text-sm">Monatlicher Preis</p>
                    <p className="text-[#1e3a5f] font-medium">{subscription.price > 0 ? formatPrice(subscription.price) : 'Kostenlos'}</p>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">Nächste Abrechnung</p>
                    <p className="text-[#1e3a5f] font-medium">
                      {subscription.nextBilling ? formatDate(subscription.nextBilling) : '-'}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">Mitglied seit</p>
                    <p className="text-[#1e3a5f] font-medium">{formatDate(parseDate(userData?.createdAt) || subscription.startDate)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500 text-sm">Zahlungsintervall</p>
                    <p className="text-[#1e3a5f] font-medium">Monatlich</p>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3 pt-4 border-t border-gray-100">
                  {userData?.stripeCustomerId && subscription.status === 'active' && (
                    <button
                      onClick={handleStripePortal}
                      className="px-4 py-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg text-sm font-medium transition-colors"
                    >
                      Abo verwalten (Stripe)
                    </button>
                  )}
                </div>
              </div>

              {/* Anfragen nachkaufen - nur für Basis und Professional */}
              {(normalizedTier === 'basis' || normalizedTier === 'professional') && (
                <div className="bg-gradient-to-r from-[#1e3a5f]/5 to-[#b8860b]/5 rounded-xl border border-[#b8860b]/20 p-6">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                      <h3 className="text-lg font-semibold text-[#1e3a5f] flex items-center gap-2">
                        🔋 Anfragen nachkaufen
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">
                        Ihr aktuelles Guthaben: <strong>{Math.max(0, (userData?.queriesLimit || 0) - (userData?.queriesUsed || 0))} Anfragen</strong> übrig
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {normalizedTier === 'basis' 
                          ? '20 zusätzliche Anfragen für nur 5 € inkl. MwSt. (0,25 €/Anfrage)' 
                          : '50 zusätzliche Anfragen für nur 10 € inkl. MwSt. (0,20 €/Anfrage)'}
                      </p>
                    </div>
                    <button
                      onClick={() => setShowQueryPackModal(true)}
                      className="px-6 py-3 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-lg font-bold transition-colors whitespace-nowrap flex items-center gap-2"
                    >
                      <span>⚡</span>
                      Anfragen kaufen
                    </button>
                  </div>
                </div>
              )}

              {/* Kündigungsbutton gemäß § 312k BGB */}
              <div className="bg-white rounded-xl border border-red-200 p-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-semibold text-[#1e3a5f]">Vertrag kündigen</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      Sie können Ihr Abonnement jederzeit zum Ende der Laufzeit kündigen.
                    </p>
                  </div>
                  <Link
                    href="/kuendigen"
                    className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-bold transition-colors whitespace-nowrap text-center"
                  >
                    Verträge hier kündigen
                  </Link>
                </div>
              </div>

              {/* Billing History */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                <div className="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                  <h2 className="text-lg font-semibold text-[#1e3a5f]">Rechnungshistorie</h2>
                  <button
                    onClick={loadUserInvoices}
                    disabled={loadingInvoices}
                    className="px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 rounded text-gray-700"
                  >
                    {loadingInvoices ? '⏳' : '🔄'} Laden
                  </button>
                </div>
                <div className="p-4">
                  {userInvoices.length === 0 ? (
                    <p className="text-gray-500 text-sm">
                      {loadingInvoices ? 'Rechnungen werden geladen...' : 'Keine Rechnungen vorhanden. Klicken Sie auf "Laden" um Ihre Rechnungen abzurufen.'}
                    </p>
                  ) : (
                    <div className="space-y-3">
                      {userInvoices.map((invoice) => (
                        <div key={invoice.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div>
                            <p className="font-medium text-gray-900">
                              {invoice.number || `Rechnung vom ${formatUnixDate(invoice.created)}`}
                            </p>
                            <p className="text-sm text-gray-500">
                              {formatUnixDate(invoice.created)} • {invoice.amount.toFixed(2)} €
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className={`px-2 py-1 text-xs rounded ${
                              invoice.status === 'paid' ? 'bg-green-100 text-green-700' :
                              invoice.status === 'open' ? 'bg-amber-100 text-amber-700' :
                              'bg-gray-100 text-gray-600'
                            }`}>
                              {invoice.status === 'paid' ? '✅ Bezahlt' : invoice.status === 'open' ? '⏳ Offen' : invoice.status}
                            </span>
                            {invoice.invoice_pdf && (
                              <a
                                href={invoice.invoice_pdf}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-3 py-1 bg-[#1e3a5f] text-white text-sm rounded hover:bg-[#2d4a6f]"
                              >
                                📄 PDF
                              </a>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Settings Section */}
          {activeSection === 'settings' && (
            <div className="space-y-6">
              <h1 className="text-2xl font-bold text-[#1e3a5f]">Einstellungen</h1>
              
              {saveSuccess && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
                  ✓ Änderungen erfolgreich gespeichert
                </div>
              )}
              
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">Persönliche Daten</h2>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-500 mb-1">E-Mail</label>
                    <input
                      type="email"
                      value={displayEmail}
                      disabled
                      className="w-full px-4 py-2 bg-gray-100 border border-gray-200 rounded-lg text-gray-600 cursor-not-allowed"
                    />
                    <p className="text-xs text-gray-400 mt-1">E-Mail kann nicht geändert werden</p>
                  </div>
                  <div>
                    <label className="block text-sm text-gray-500 mb-1">Name *</label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-500 mb-1">Telefon</label>
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      placeholder="+49 123 456789"
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-500 mb-1">Firma (optional)</label>
                    <input
                      type="text"
                      value={formData.company}
                      onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                      placeholder="Firma oder Kanzlei"
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">Adresse</h2>
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-sm text-gray-500 mb-1">Straße und Hausnummer</label>
                    <input
                      type="text"
                      value={formData.address}
                      onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                      placeholder="Musterstraße 123"
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-500 mb-1">PLZ</label>
                    <input
                      type="text"
                      value={formData.zipCode}
                      onChange={(e) => setFormData({ ...formData, zipCode: e.target.value })}
                      placeholder="10115"
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-500 mb-1">Stadt</label>
                    <input
                      type="text"
                      value={formData.city}
                      onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                      placeholder="Berlin"
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm text-gray-500 mb-1">Land</label>
                    <input
                      type="text"
                      value={formData.country}
                      onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                      className="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 focus:border-[#1e3a5f] focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-end">
                <button
                  onClick={handleSaveSettings}
                  disabled={saving}
                  className="px-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {saving ? 'Wird gespeichert...' : 'Änderungen speichern'}
                </button>
              </div>
            </div>
          )}

          {/* Data Import/Export Section */}
          {activeSection === 'data' && (normalizedTier === 'professional' || normalizedTier === 'lawyer') && (
            <div className="space-y-6">
              <h1 className="text-2xl font-bold text-[#1e3a5f]">Daten Import & Export</h1>
              <p className="text-gray-600">
                Exportieren Sie Ihre Daten als Backup oder importieren Sie bestehende Daten.
              </p>

              {/* Export Section */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">📤 Daten exportieren</h2>
                
                {/* Format Selection */}
                <div className="mb-4">
                  <label className="block text-sm text-gray-500 mb-2">Export-Format</label>
                  <div className="flex gap-4 flex-wrap">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="exportFormat"
                        value="json"
                        checked={exportFormat === 'json'}
                        onChange={() => setExportFormat('json')}
                        className="text-[#1e3a5f]"
                      />
                      <span className="text-gray-700">JSON</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="exportFormat"
                        value="csv"
                        checked={exportFormat === 'csv'}
                        onChange={() => setExportFormat('csv')}
                        className="text-[#1e3a5f]"
                      />
                      <span className="text-gray-700">CSV</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="exportFormat"
                        value="excel"
                        checked={exportFormat === 'excel'}
                        onChange={() => setExportFormat('excel')}
                        className="text-[#1e3a5f]"
                      />
                      <span className="text-gray-700">Excel (.xlsx)</span>
                    </label>
                  </div>
                </div>

                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <button
                    onClick={() => handleExport('objekte')}
                    disabled={exporting}
                    className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left disabled:opacity-50"
                  >
                    <div className="text-2xl mb-2">🏠</div>
                    <div className="font-medium text-[#1e3a5f]">Objekte exportieren</div>
                    <div className="text-sm text-gray-500">Alle Immobilien & Mieter</div>
                  </button>

                  {normalizedTier === 'lawyer' && (
                    <button
                      onClick={() => handleExport('mandanten')}
                      disabled={exporting}
                      className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left disabled:opacity-50"
                    >
                      <div className="text-2xl mb-2">👥</div>
                      <div className="font-medium text-[#1e3a5f]">Mandanten exportieren</div>
                      <div className="text-sm text-gray-500">CRM-Daten & Fristen</div>
                    </button>
                  )}

                  <button
                    onClick={() => handleExport('all')}
                    disabled={exporting}
                    className="p-4 border border-[#1e3a5f] bg-[#1e3a5f]/5 rounded-lg hover:bg-[#1e3a5f]/10 transition-colors text-left disabled:opacity-50"
                  >
                    <div className="text-2xl mb-2">📦</div>
                    <div className="font-medium text-[#1e3a5f]">Alles exportieren</div>
                    <div className="text-sm text-gray-500">Komplettes Backup</div>
                  </button>
                </div>

                {exporting && (
                  <div className="mt-4 text-center text-gray-600">
                    <div className="inline-block animate-spin mr-2">⏳</div>
                    Export wird erstellt...
                  </div>
                )}
              </div>

              {/* Import Section */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                <h2 className="text-lg font-semibold text-[#1e3a5f] mb-4">📥 Daten importieren</h2>
                <p className="text-sm text-gray-500 mb-4">
                  Laden Sie eine JSON, CSV oder Excel-Datei hoch. Existierende Einträge werden übersprungen.
                </p>

                <div className="grid sm:grid-cols-2 gap-4">
                  <div className="relative">
                    <input
                      type="file"
                      accept=".json,.csv,.xlsx,.xls"
                      onChange={(e) => handleImport(e, 'objekte')}
                      disabled={importing}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <div className="p-4 border-2 border-dashed border-gray-200 rounded-lg hover:border-[#1e3a5f] transition-colors text-center">
                      <div className="text-2xl mb-2">🏠</div>
                      <div className="font-medium text-[#1e3a5f]">Objekte importieren</div>
                      <div className="text-sm text-gray-500">JSON, CSV oder Excel</div>
                    </div>
                  </div>

                  {normalizedTier === 'lawyer' && (
                    <div className="relative">
                      <input
                        type="file"
                        accept=".json,.csv,.xlsx,.xls"
                        onChange={(e) => handleImport(e, 'mandanten')}
                        disabled={importing}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      />
                      <div className="p-4 border-2 border-dashed border-gray-200 rounded-lg hover:border-[#1e3a5f] transition-colors text-center">
                        <div className="text-2xl mb-2">👥</div>
                        <div className="font-medium text-[#1e3a5f]">Mandanten importieren</div>
                        <div className="text-sm text-gray-500">JSON, CSV oder Excel</div>
                      </div>
                    </div>
                  )}
                </div>

                {importing && (
                  <div className="mt-4 text-center text-gray-600">
                    <div className="inline-block animate-spin mr-2">⏳</div>
                    Import wird verarbeitet...
                  </div>
                )}

                {importResult && (
                  <div className={`mt-4 p-4 rounded-lg ${importResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                    {importResult.message}
                  </div>
                )}
              </div>

              {/* Info Section */}
              <div className="bg-blue-50 rounded-xl p-6">
                <h3 className="font-medium text-[#1e3a5f] mb-2">💡 Hinweise zum Import/Export</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• <strong>JSON</strong>: Vollständiger Datenexport mit allen Feldern</li>
                  <li>• <strong>CSV</strong>: Tabellenformat (wichtigste Felder)</li>
                  <li>• <strong>Excel (.xlsx)</strong>: Formatiert mit Spaltenüberschriften, ideal für Bearbeitung</li>
                  <li>• Beim Import werden existierende Einträge mit gleicher ID übersprungen</li>
                  <li>• Zeitstempel werden automatisch beim Import generiert</li>
                </ul>
              </div>
            </div>
          )}
        </main>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-[#1e3a5f] py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 flex flex-wrap gap-6 justify-center text-gray-300 text-sm">
          <Link href="/impressum" className="hover:text-white">Impressum</Link>
          <Link href="/datenschutz" className="hover:text-white">Datenschutz</Link>
          <Link href="/agb" className="hover:text-white">AGB</Link>
        </div>
      </footer>
    </div>
  );
}
