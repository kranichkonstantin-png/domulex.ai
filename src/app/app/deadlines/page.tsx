'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, doc, getDoc, getDocs, addDoc, updateDoc, deleteDoc, query, orderBy, where, Timestamp } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import UpgradeModal from '@/components/UpgradeModal';
import { hasTierAccess } from '@/lib/tierUtils';

interface Deadline {
  id: string;
  title: string;
  description?: string;
  dueDate: Date;
  clientName?: string;
  clientId?: string;
  caseNumber?: string;
  priority: 'niedrig' | 'mittel' | 'hoch' | 'kritisch';
  status: 'offen' | 'erledigt' | 'überfällig';
  reminderDays: number;
  createdAt: Date;
}

const PRIORITY_COLORS = {
  niedrig: 'bg-gray-100 text-gray-700',
  mittel: 'bg-blue-100 text-blue-700',
  hoch: 'bg-orange-100 text-orange-700',
  kritisch: 'bg-red-100 text-red-700'
};

const STATUS_COLORS = {
  offen: 'bg-yellow-100 text-yellow-700',
  erledigt: 'bg-green-100 text-green-700',
  überfällig: 'bg-red-100 text-red-700'
};

// ===== DEMO-DATEN FÜR FREE-NUTZER (sofort sichtbar) =====
const DEMO_FRISTEN: Deadline[] = [
  {
    id: 'demo-f1',
    title: 'Klageerwiderung Mietminderung Müller',
    description: 'Erwiderung auf Klage des Vermieters wegen einbehaltener Miete bei Schimmelbefall.',
    dueDate: new Date('2026-01-15'),
    clientName: 'Müller, Petra',
    caseNumber: 'Az. 67 C 2345/25',
    priority: 'kritisch',
    status: 'offen',
    reminderDays: 5,
    createdAt: new Date('2025-12-20')
  },
  {
    id: 'demo-f2',
    title: 'WEG-Anfechtungsklage einreichen',
    description: 'Anfechtung des Beschlusses zur Sonderumlage wegen Formfehler bei Einladung.',
    dueDate: new Date('2026-01-10'),
    clientName: 'Schmidt GmbH',
    caseNumber: 'Noch nicht vergeben',
    priority: 'kritisch',
    status: 'offen',
    reminderDays: 3,
    createdAt: new Date('2025-12-28')
  },
  {
    id: 'demo-f3',
    title: 'Gerichtstermin AG Berlin-Mitte',
    description: 'Mündliche Verhandlung im Schimmelprozess. Mandantin und Sachverständiger geladen.',
    dueDate: new Date('2026-02-20'),
    clientName: 'Müller, Petra',
    caseNumber: 'Az. 67 C 2345/25',
    priority: 'hoch',
    status: 'offen',
    reminderDays: 7,
    createdAt: new Date('2025-12-15')
  },
  {
    id: 'demo-f4',
    title: 'Räumungsklage Erwiderung',
    description: 'Erwiderung auf Räumungsklage des Vermieters wegen angeblichem Eigenbedarf.',
    dueDate: new Date('2026-01-25'),
    clientName: 'Dr. Weber, Thomas',
    caseNumber: 'Az. 102 O 4567/25',
    priority: 'hoch',
    status: 'offen',
    reminderDays: 5,
    createdAt: new Date('2026-01-02')
  },
  {
    id: 'demo-f5',
    title: 'Stellungnahme Nebenkostenstreit',
    description: 'Stellungnahme zur bestrittenen Nebenkostenabrechnung 2024.',
    dueDate: new Date('2026-01-12'),
    clientName: 'Bauer Hausverwaltung KG',
    caseNumber: 'Vorgerichtlich',
    priority: 'mittel',
    status: 'offen',
    reminderDays: 3,
    createdAt: new Date('2026-01-03')
  },
  {
    id: 'demo-f6',
    title: 'Widerspruch gegen Kündigung',
    description: 'Widerspruch gegen Kündigung wegen Eigenbedarf eingereicht.',
    dueDate: new Date('2026-01-08'),
    clientName: 'Dr. Weber, Thomas',
    caseNumber: 'Vorgerichtlich',
    priority: 'kritisch',
    status: 'erledigt',
    reminderDays: 3,
    createdAt: new Date('2025-12-01')
  },
  {
    id: 'demo-f7',
    title: 'Berufungsfrist LG München',
    description: 'Berufung gegen Urteil in WEG-Sache prüfen.',
    dueDate: new Date('2026-03-01'),
    clientName: 'Schmidt GmbH',
    caseNumber: 'Az. 36 T 8901/25',
    priority: 'niedrig',
    status: 'offen',
    reminderDays: 14,
    createdAt: new Date('2026-01-05')
  },
];

export default function DeadlinesPage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const router = useRouter();

  // Check if user has access (Lawyer only)
  const hasAccess = hasTierAccess(userTier, 'lawyer');
  
  // Wrapper for actions that require tier
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    dueDate: '',
    clientName: '',
    caseNumber: '',
    priority: 'mittel' as Deadline['priority'],
    reminderDays: 3
  });

  // KI-States
  const [kiSuggestion, setKiSuggestion] = useState<string>('');
  const [isLoadingKi, setIsLoadingKi] = useState(false);
  
  // Kalender-States
  const [viewMode, setViewMode] = useState<'liste' | 'kalender'>('liste');
  const [currentMonth, setCurrentMonth] = useState(new Date());

  // Outlook/iCal Export Funktion
  const exportToICS = (deadline: Deadline) => {
    const formatDateForICS = (date: Date) => {
      return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    };
    
    const startDate = deadline.dueDate;
    const endDate = new Date(startDate.getTime() + 60 * 60 * 1000); // 1 Stunde
    const reminderDate = new Date(startDate.getTime() - deadline.reminderDays * 24 * 60 * 60 * 1000);
    
    const icsContent = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Domulex AI//Fristenverwaltung//DE
BEGIN:VEVENT
UID:${deadline.id}@domulex.ai
DTSTART:${formatDateForICS(startDate)}
DTEND:${formatDateForICS(endDate)}
SUMMARY:${deadline.title}
DESCRIPTION:${deadline.description || ''}${deadline.clientName ? '\\nMandant: ' + deadline.clientName : ''}${deadline.caseNumber ? '\\nAz: ' + deadline.caseNumber : ''}\\nPriorität: ${deadline.priority}
CATEGORIES:${deadline.priority.toUpperCase()}
PRIORITY:${deadline.priority === 'kritisch' ? 1 : deadline.priority === 'hoch' ? 3 : deadline.priority === 'mittel' ? 5 : 9}
BEGIN:VALARM
TRIGGER:-P${deadline.reminderDays}D
ACTION:DISPLAY
DESCRIPTION:Erinnerung: ${deadline.title}
END:VALARM
END:VEVENT
END:VCALENDAR`;

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `frist-${deadline.id}.ics`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Alle Fristen exportieren
  const exportAllToICS = () => {
    const openDeadlines = deadlines.filter(d => d.status !== 'erledigt');
    
    const formatDateForICS = (date: Date) => {
      return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    };
    
    let icsContent = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Domulex AI//Fristenverwaltung//DE
X-WR-CALNAME:Domulex Fristen
`;

    openDeadlines.forEach(deadline => {
      const startDate = deadline.dueDate;
      const endDate = new Date(startDate.getTime() + 60 * 60 * 1000);
      
      icsContent += `BEGIN:VEVENT
UID:${deadline.id}@domulex.ai
DTSTART:${formatDateForICS(startDate)}
DTEND:${formatDateForICS(endDate)}
SUMMARY:${deadline.title}
DESCRIPTION:${deadline.description || ''}${deadline.clientName ? '\\nMandant: ' + deadline.clientName : ''}${deadline.caseNumber ? '\\nAz: ' + deadline.caseNumber : ''}
CATEGORIES:${deadline.priority.toUpperCase()}
PRIORITY:${deadline.priority === 'kritisch' ? 1 : deadline.priority === 'hoch' ? 3 : 5}
BEGIN:VALARM
TRIGGER:-P${deadline.reminderDays}D
ACTION:DISPLAY
DESCRIPTION:Erinnerung: ${deadline.title}
END:VALARM
END:VEVENT
`;
    });

    icsContent += 'END:VCALENDAR';

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'domulex-fristen.ics';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Kalender-Hilfsfunktionen
  const getMonthDays = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const days: Date[] = [];
    
    // Vorherige Monatstage auffüllen
    const startPadding = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
    for (let i = startPadding; i > 0; i--) {
      days.push(new Date(year, month, 1 - i));
    }
    
    // Aktueller Monat
    for (let i = 1; i <= lastDay.getDate(); i++) {
      days.push(new Date(year, month, i));
    }
    
    // Nächster Monat auffüllen
    const endPadding = 42 - days.length;
    for (let i = 1; i <= endPadding; i++) {
      days.push(new Date(year, month + 1, i));
    }
    
    return days;
  };

  const getDeadlinesForDay = (date: Date) => {
    return deadlines.filter(d => {
      const dDate = d.dueDate;
      return dDate.getDate() === date.getDate() && 
             dDate.getMonth() === date.getMonth() && 
             dDate.getFullYear() === date.getFullYear();
    });
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }

      setUser(currentUser);

      // Check tier - set tier for soft-lock instead of redirect
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      if (userDoc.exists()) {
        const userData = userDoc.data();
        const tier = userData.tier || userData.dashboardType || 'free';
        setUserTier(tier);
        
        // Load deadlines only for lawyers (others see demo data)
        if (hasTierAccess(tier, 'lawyer')) {
          await loadDeadlines(currentUser.uid);
        } else {
          // Für FREE-Nutzer: Demo-Daten anzeigen
          setDeadlines(DEMO_FRISTEN);
        }
      }
      
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  const loadDeadlines = async (userId: string) => {
    try {
      const deadlinesRef = collection(db, 'users', userId, 'deadlines');
      const q = query(deadlinesRef, orderBy('dueDate', 'asc'));
      const snapshot = await getDocs(q);
      
      const now = new Date();
      const deadlineList: Deadline[] = snapshot.docs.map(doc => {
        const data = doc.data();
        const dueDate = data.dueDate?.toDate() || new Date();
        let status = data.status || 'offen';
        
        // Automatisch überfällig markieren
        if (status === 'offen' && dueDate < now) {
          status = 'überfällig';
        }
        
        return {
          id: doc.id,
          ...data,
          dueDate,
          status,
          createdAt: data.createdAt?.toDate() || new Date()
        };
      }) as Deadline[];
      
      setDeadlines(deadlineList);
    } catch (error) {
      console.error('Error loading deadlines:', error);
    }
  };

  const handleAddDeadline = async () => {
    if (!user || !formData.title || !formData.dueDate) return;

    try {
      const deadlinesRef = collection(db, 'users', user.uid, 'deadlines');
      await addDoc(deadlinesRef, {
        ...formData,
        dueDate: Timestamp.fromDate(new Date(formData.dueDate)),
        status: 'offen',
        createdAt: Timestamp.now()
      });

      await loadDeadlines(user.uid);
      setShowAddModal(false);
      resetForm();
    } catch (error) {
      console.error('Error adding deadline:', error);
    }
  };

  const toggleDeadlineStatus = async (deadline: Deadline) => {
    if (!user) return;
    const newStatus = deadline.status === 'erledigt' ? 'offen' : 'erledigt';
    
    try {
      await updateDoc(doc(db, 'users', user.uid, 'deadlines', deadline.id), {
        status: newStatus
      });
      await loadDeadlines(user.uid);
    } catch (error) {
      console.error('Error updating deadline:', error);
    }
  };

  const deleteDeadline = async (id: string) => {
    if (!user || !confirm('Frist wirklich löschen?')) return;
    
    try {
      await deleteDoc(doc(db, 'users', user.uid, 'deadlines', id));
      await loadDeadlines(user.uid);
    } catch (error) {
      console.error('Error deleting deadline:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      dueDate: '',
      clientName: '',
      caseNumber: '',
      priority: 'mittel',
      reminderDays: 3
    });
    setKiSuggestion('');
  };

  // KI-Fristvorschlag anfordern
  const requestKiFristvorschlag = async () => {
    if (!formData.title) return;
    setIsLoadingKi(true);
    try {
      const prompt = `Als Rechtsanwalt für Immobilienrecht, analysiere diese Frist und gib Empfehlungen:

**Frist:** ${formData.title}
**Beschreibung:** ${formData.description || 'Keine'}
**Mandant:** ${formData.clientName || 'Nicht angegeben'}
**Aktenzeichen:** ${formData.caseNumber || 'Nicht angegeben'}
**Geplantes Datum:** ${formData.dueDate || 'Noch nicht festgelegt'}

Bitte beantworte kurz:
1. Welche gesetzlichen Fristen sind zu beachten (z.B. § 556 BGB, ZPO)?
2. Gibt es Verjährungsfristen zu beachten?
3. Empfohlene Pufferzeit vor der Frist?
4. Welche Folgen drohen bei Fristversäumnis?
5. Wichtige Checkliste für diese Frist?

Antworte prägnant und praxisorientiert.`;

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app'}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: prompt,
          target_jurisdiction: 'DE'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setKiSuggestion(data.answer || data.response || 'Keine Empfehlung verfügbar.');
      }
    } catch (error) {
      console.error('KI-Fehler:', error);
      setKiSuggestion('KI-Analyse nicht verfügbar.');
    } finally {
      setIsLoadingKi(false);
    }
  };

  const getDaysUntilDue = (dueDate: Date) => {
    const now = new Date();
    const diff = dueDate.getTime() - now.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('de-DE', {
      weekday: 'short',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const filteredDeadlines = deadlines.filter(d => {
    const matchesStatus = filterStatus === 'all' || d.status === filterStatus;
    const matchesPriority = filterPriority === 'all' || d.priority === filterPriority;
    return matchesStatus && matchesPriority;
  });

  // Statistiken
  const stats = {
    total: deadlines.length,
    offen: deadlines.filter(d => d.status === 'offen').length,
    überfällig: deadlines.filter(d => d.status === 'überfällig').length,
    erledigt: deadlines.filter(d => d.status === 'erledigt').length,
    kritisch: deadlines.filter(d => d.priority === 'kritisch' && d.status !== 'erledigt').length
  };

  // Nächste 7 Tage
  const upcomingDeadlines = deadlines.filter(d => {
    const days = getDaysUntilDue(d.dueDate);
    return days >= 0 && days <= 7 && d.status !== 'erledigt';
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Fristen werden geladen...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-xl border-b border-gray-800">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-16">
            <Link href="/dashboard" className="text-gray-400 hover:text-white">← Dashboard</Link>
            <div className="flex items-center gap-4">
              <Link href="/app/crm" className="text-sm text-gray-400 hover:text-white">CRM</Link>
              <h1 className="text-lg font-semibold text-white">Fristenverwaltung</h1>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        {/* FREE User Banner */}
        {!hasAccess && (
          <div className="mb-6 p-4 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/50 rounded-xl">
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <span className="text-4xl">🔒</span>
              <div className="flex-1 text-center sm:text-left">
                <p className="text-white font-bold text-lg">Demo-Ansicht - Volle Funktionen mit Lawyer Pro</p>
                <p className="text-gray-300 text-sm">Sie sehen Beispieldaten. Mit Lawyer Pro können Sie Ihre eigenen Fristen verwalten.</p>
              </div>
              <button
                onClick={() => setShowUpgradeModal(true)}
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-medium whitespace-nowrap shadow-lg"
              >
                ⬆️ Jetzt upgraden
              </button>
            </div>
          </div>
        )}

        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Fristenverwaltung</h1>
            <p className="text-gray-400 mt-1">Behalten Sie alle wichtigen Termine im Blick</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => requireTier(() => exportAllToICS())}
              className="px-4 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 font-medium flex items-center gap-2"
              title="Alle Fristen für Outlook/Kalender exportieren"
            >
              <span>📅</span> Outlook Export
            </button>
            <button
              onClick={() => requireTier(() => setShowAddModal(true))}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium flex items-center gap-2"
            >
              <span>➕</span> Neue Frist
            </button>
          </div>
        </div>

        {/* Ansichts-Toggle */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setViewMode('liste')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              viewMode === 'liste' ? 'bg-blue-600 text-white' : 'bg-gray-800/50 text-gray-400 hover:text-white'
            }`}
          >
            📋 Liste
          </button>
          <button
            onClick={() => setViewMode('kalender')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              viewMode === 'kalender' ? 'bg-blue-600 text-white' : 'bg-gray-800/50 text-gray-400 hover:text-white'
            }`}
          >
            📅 Kalender
          </button>
        </div>

        {/* Warnungen */}
        {stats.überfällig > 0 && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-3">
            <span className="text-2xl">⚠️</span>
            <div>
              <p className="font-semibold text-red-800">{stats.überfällig} überfällige Frist{stats.überfällig > 1 ? 'en' : ''}!</p>
              <p className="text-sm text-red-600">Bitte umgehend bearbeiten.</p>
            </div>
          </div>
        )}

        {/* Statistik-Karten */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4">
            <p className="text-3xl font-bold text-white">{stats.total}</p>
            <p className="text-sm text-gray-400">Gesamt</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4">
            <p className="text-3xl font-bold text-yellow-400">{stats.offen}</p>
            <p className="text-sm text-gray-400">Offen</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4">
            <p className="text-3xl font-bold text-red-400">{stats.überfällig}</p>
            <p className="text-sm text-gray-400">Überfällig</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4">
            <p className="text-3xl font-bold text-green-400">{stats.erledigt}</p>
            <p className="text-sm text-gray-400">Erledigt</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4">
            <p className="text-3xl font-bold text-red-500">{stats.kritisch}</p>
            <p className="text-sm text-gray-400">Kritisch</p>
          </div>
        </div>

        {/* Nächste 7 Tage */}
        {upcomingDeadlines.length > 0 && (
          <div className="mb-8 bg-amber-900/30 rounded-xl border border-amber-700/50 p-4">
            <h3 className="font-semibold text-amber-400 mb-3">📅 Nächste 7 Tage ({upcomingDeadlines.length})</h3>
            <div className="space-y-2">
              {upcomingDeadlines.slice(0, 5).map(d => (
                <div key={d.id} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3">
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-1 text-xs rounded-full ${PRIORITY_COLORS[d.priority]}`}>
                      {d.priority}
                    </span>
                    <span className="font-medium text-white">{d.title}</span>
                    {d.clientName && <span className="text-sm text-gray-400">• {d.clientName}</span>}
                  </div>
                  <div className="text-sm">
                    <span className={getDaysUntilDue(d.dueDate) <= 1 ? 'text-red-400 font-bold' : 'text-gray-400'}>
                      {getDaysUntilDue(d.dueDate) === 0 ? 'Heute!' : 
                       getDaysUntilDue(d.dueDate) === 1 ? 'Morgen' : 
                       `In ${getDaysUntilDue(d.dueDate)} Tagen`}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Filter */}
        <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-4 mb-6">
          <div className="flex flex-wrap gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Status</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="all">Alle</option>
                <option value="offen">Offen</option>
                <option value="überfällig">Überfällig</option>
                <option value="erledigt">Erledigt</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Priorität</label>
              <select
                value={filterPriority}
                onChange={(e) => setFilterPriority(e.target.value)}
                className="bg-gray-800/50 border border-gray-700 rounded-lg px-3 py-2 text-white"
              >
                <option value="all">Alle</option>
                <option value="kritisch">Kritisch</option>
                <option value="hoch">Hoch</option>
                <option value="mittel">Mittel</option>
                <option value="niedrig">Niedrig</option>
              </select>
            </div>
          </div>
        </div>

        {/* Kalender-Ansicht */}
        {viewMode === 'kalender' && (
          <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6 mb-6">
            {/* Kalender-Header */}
            <div className="flex items-center justify-between mb-6">
              <button
                onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
                className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white"
              >
                ←
              </button>
              <h3 className="text-xl font-semibold text-white">
                {currentMonth.toLocaleDateString('de-DE', { month: 'long', year: 'numeric' })}
              </h3>
              <button
                onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
                className="p-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white"
              >
                →
              </button>
            </div>

            {/* Wochentage */}
            <div className="grid grid-cols-7 gap-1 mb-2">
              {['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'].map(day => (
                <div key={day} className="text-center text-sm font-medium text-gray-400 py-2">
                  {day}
                </div>
              ))}
            </div>

            {/* Kalender-Tage */}
            <div className="grid grid-cols-7 gap-1">
              {getMonthDays(currentMonth).map((day, idx) => {
                const dayDeadlines = getDeadlinesForDay(day);
                const isCurrentMonth = day.getMonth() === currentMonth.getMonth();
                const isToday = day.toDateString() === new Date().toDateString();
                const hasCritical = dayDeadlines.some(d => d.priority === 'kritisch' && d.status !== 'erledigt');
                const hasOverdue = dayDeadlines.some(d => d.status === 'überfällig');
                
                return (
                  <div
                    key={idx}
                    className={`min-h-[80px] p-1 rounded-lg border transition-colors ${
                      !isCurrentMonth ? 'bg-gray-900/30 border-gray-800 text-gray-600' :
                      isToday ? 'bg-blue-900/30 border-blue-500' :
                      hasOverdue ? 'bg-red-900/30 border-red-700' :
                      hasCritical ? 'bg-orange-900/30 border-orange-700' :
                      dayDeadlines.length > 0 ? 'bg-gray-700/30 border-gray-600' :
                      'bg-gray-800/30 border-gray-700'
                    }`}
                  >
                    <div className={`text-right text-sm font-medium mb-1 ${isToday ? 'text-blue-400' : isCurrentMonth ? 'text-white' : 'text-gray-600'}`}>
                      {day.getDate()}
                    </div>
                    <div className="space-y-0.5">
                      {dayDeadlines.slice(0, 3).map(d => (
                        <div
                          key={d.id}
                          onClick={() => exportToICS(d)}
                          className={`text-xs px-1 py-0.5 rounded truncate cursor-pointer hover:opacity-80 ${
                            d.status === 'erledigt' ? 'bg-green-900/50 text-green-300 line-through' :
                            d.status === 'überfällig' ? 'bg-red-600 text-white' :
                            d.priority === 'kritisch' ? 'bg-red-500 text-white' :
                            d.priority === 'hoch' ? 'bg-orange-500 text-white' :
                            'bg-blue-600 text-white'
                          }`}
                          title={`${d.title}${d.clientName ? ' - ' + d.clientName : ''} (Klick für Outlook-Export)`}
                        >
                          {d.title}
                        </div>
                      ))}
                      {dayDeadlines.length > 3 && (
                        <div className="text-xs text-gray-400 text-center">
                          +{dayDeadlines.length - 3} mehr
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Legende */}
            <div className="flex flex-wrap gap-4 mt-4 pt-4 border-t border-gray-700">
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <div className="w-3 h-3 bg-red-600 rounded"></div>
                Überfällig
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <div className="w-3 h-3 bg-red-500 rounded"></div>
                Kritisch
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <div className="w-3 h-3 bg-orange-500 rounded"></div>
                Hoch
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <div className="w-3 h-3 bg-blue-600 rounded"></div>
                Normal
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <div className="w-3 h-3 bg-green-600 rounded"></div>
                Erledigt
              </div>
            </div>

            <p className="text-xs text-gray-500 mt-3">💡 Tipp: Klicken Sie auf eine Frist, um sie in Outlook/Kalender zu exportieren</p>
          </div>
        )}

        {/* Fristen-Liste */}
        {viewMode === 'liste' && (
        <div className="bg-gray-800/50 rounded-xl border border-gray-700">
          {filteredDeadlines.length === 0 ? (
            <div className="p-12 text-center">
              <p className="text-4xl mb-4">📋</p>
              <p className="text-lg text-gray-400">Keine Fristen gefunden</p>
              <p className="text-sm text-gray-500 mt-2">Erstellen Sie Ihre erste Frist</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-700">
              {filteredDeadlines.map((deadline) => {
                const daysLeft = getDaysUntilDue(deadline.dueDate);
                return (
                  <div key={deadline.id} className={`p-4 hover:bg-gray-700/30 ${deadline.status === 'erledigt' ? 'opacity-60' : ''}`}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <button
                          onClick={() => toggleDeadlineStatus(deadline)}
                          className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                            deadline.status === 'erledigt' 
                              ? 'bg-green-500 border-green-500 text-white' 
                              : 'border-gray-600 hover:border-green-500'
                          }`}
                        >
                          {deadline.status === 'erledigt' && '✓'}
                        </button>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className={`text-lg font-medium ${deadline.status === 'erledigt' ? 'line-through text-gray-500' : 'text-white'}`}>
                              {deadline.title}
                            </span>
                            <span className={`px-2 py-0.5 text-xs rounded-full ${PRIORITY_COLORS[deadline.priority]}`}>
                              {deadline.priority}
                            </span>
                            <span className={`px-2 py-0.5 text-xs rounded-full ${STATUS_COLORS[deadline.status]}`}>
                              {deadline.status}
                            </span>
                          </div>
                          <div className="text-sm text-gray-400 mt-1">
                            {deadline.clientName && <span>👤 {deadline.clientName}</span>}
                            {deadline.caseNumber && <span className="ml-3">Az: {deadline.caseNumber}</span>}
                            {deadline.description && <span className="ml-3">• {deadline.description}</span>}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <p className="font-medium text-white">{formatDate(deadline.dueDate)}</p>
                          <p className={`text-sm ${
                            deadline.status === 'erledigt' ? 'text-gray-500' :
                            daysLeft < 0 ? 'text-red-400 font-bold' :
                            daysLeft <= 3 ? 'text-orange-400' :
                            'text-gray-400'
                          }`}>
                            {deadline.status === 'erledigt' ? 'Erledigt' :
                             daysLeft < 0 ? `${Math.abs(daysLeft)} Tage überfällig!` :
                             daysLeft === 0 ? 'Heute fällig!' :
                             daysLeft === 1 ? 'Morgen fällig' :
                             `In ${daysLeft} Tagen`}
                          </p>
                        </div>
                        <button
                          onClick={() => exportToICS(deadline)}
                          className="text-gray-500 hover:text-blue-400"
                          title="In Outlook/Kalender exportieren"
                        >
                          📅
                        </button>
                        <button
                          onClick={() => deleteDeadline(deadline.id)}
                          className="text-gray-500 hover:text-red-400"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
        )}
      </div>

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-xl max-w-lg w-full p-6 shadow-2xl border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-4">Neue Frist anlegen</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Titel *</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="z.B. Klagebeantwortung einreichen"
                  className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500"
                />
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Fällig am *</label>
                  <input
                    type="date"
                    value={formData.dueDate}
                    onChange={(e) => setFormData(prev => ({ ...prev, dueDate: e.target.value }))}
                    className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Priorität</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value as Deadline['priority'] }))}
                    className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white"
                  >
                    <option value="niedrig">Niedrig</option>
                    <option value="mittel">Mittel</option>
                    <option value="hoch">Hoch</option>
                    <option value="kritisch">Kritisch</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Mandant</label>
                  <input
                    type="text"
                    value={formData.clientName}
                    onChange={(e) => setFormData(prev => ({ ...prev, clientName: e.target.value }))}
                    placeholder="Name des Mandanten"
                    className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Aktenzeichen</label>
                  <input
                    type="text"
                    value={formData.caseNumber}
                    onChange={(e) => setFormData(prev => ({ ...prev, caseNumber: e.target.value }))}
                    placeholder="Az: 123/25"
                    className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Beschreibung</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  rows={2}
                  placeholder="Zusätzliche Notizen..."
                  className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Erinnerung (Tage vorher)</label>
                <input
                  type="number"
                  value={formData.reminderDays}
                  onChange={(e) => setFormData(prev => ({ ...prev, reminderDays: Number(e.target.value) }))}
                  min={0}
                  max={30}
                  className="w-full p-3 bg-gray-700/50 border border-gray-600 rounded-lg text-white"
                />
              </div>

              {/* KI-Vorschlag Button */}
              <button
                onClick={requestKiFristvorschlag}
                disabled={!formData.title || isLoadingKi}
                className="w-full py-2 bg-purple-900/50 text-purple-300 rounded-lg font-medium hover:bg-purple-800/50 disabled:opacity-50 flex items-center justify-center gap-2 text-sm border border-purple-700"
              >
                {isLoadingKi ? (
                  <>
                    <span className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></span>
                    KI analysiert Frist...
                  </>
                ) : (
                  <>🤖 KI-Fristanalyse anfordern</>
                )}
              </button>

              {/* KI-Empfehlung anzeigen */}
              {kiSuggestion && (
                <div className="p-3 bg-purple-900/30 border border-purple-700 rounded-lg">
                  <p className="text-xs font-medium text-purple-300 mb-1">🤖 KI-Empfehlung:</p>
                  <p className="text-xs text-purple-200 whitespace-pre-wrap">{kiSuggestion}</p>
                </div>
              )}
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => { setShowAddModal(false); resetForm(); }}
                className="flex-1 py-3 border border-gray-600 text-gray-300 rounded-lg font-medium hover:bg-gray-700"
              >
                Abbrechen
              </button>
              <button
                onClick={handleAddDeadline}
                disabled={!formData.title || !formData.dueDate}
                className="flex-1 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                Frist anlegen
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="lawyer"
        feature="Fristenverwaltung"
      />
    </div>
  );
}
