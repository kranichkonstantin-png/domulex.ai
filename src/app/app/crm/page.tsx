'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, doc, getDoc, getDocs, addDoc, updateDoc, deleteDoc, query, orderBy, Timestamp } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import UpgradeModal from '@/components/UpgradeModal';
import { hasTierAccess } from '@/lib/tierUtils';

interface Client {
  id: string;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  notes?: string;
  status: 'aktiv' | 'inaktiv' | 'abgeschlossen';
  caseType?: string;
  createdAt: Date;
  updatedAt: Date;
  // NEU: Multi-Objekt-Verknüpfung
  objektIds?: string[];
  fristen?: Frist[];
}

// NEU: Frist Interface
interface Frist {
  id: string;
  bezeichnung: string;
  datum: string;
  typ: 'klage' | 'widerspruch' | 'frist' | 'termin' | 'sonstiges';
  erledigt: boolean;
}

// Eigentümerversammlungen entfernt - nicht relevant für Lawyer-CRM

// NEU: Dokument Interface (pro Objekt/Mandant)
interface Dokument {
  id: string;
  name: string;
  typ: 'vertrag' | 'protokoll' | 'rechnung' | 'bescheid' | 'korrespondenz' | 'sonstiges';
  datum: string;
  objektId?: string;
  mandantId?: string;
  notizen?: string;
}

// NEU: Objekt Interface (für Verknüpfung)
interface ObjektRef {
  id: string;
  adresse: string;
  ort: string;
}

interface CaseNote {
  id: string;
  content: string;
  createdAt: Date;
}

// ===== DEMO-DATEN FÜR FREE-NUTZER (sofort sichtbar) =====
const DEMO_MANDANTEN: Client[] = [
  {
    id: 'demo-1',
    name: 'Müller, Petra',
    email: 'p.mueller@email.de',
    phone: '030-12345678',
    address: 'Berliner Straße 42, 10115 Berlin',
    status: 'aktiv',
    caseType: 'Mietminderung wegen Schimmelbefall',
    notes: 'Mandantin klagt gegen Vermieter wegen Schimmel im Schlafzimmer. Sachverständigengutachten liegt vor.',
    createdAt: new Date('2025-11-15'),
    updatedAt: new Date('2026-01-05'),
    fristen: [
      { id: 'f1', bezeichnung: 'Klageerwiderung einreichen', datum: '2026-01-15', typ: 'frist', erledigt: false },
      { id: 'f2', bezeichnung: 'Gerichtstermin AG Berlin-Mitte', datum: '2026-02-20', typ: 'termin', erledigt: false },
    ]
  },
  {
    id: 'demo-2',
    name: 'Schmidt GmbH',
    email: 'recht@schmidt-immobilien.de',
    phone: '089-98765432',
    address: 'Maximilianstraße 15, 80539 München',
    status: 'aktiv',
    caseType: 'WEG-Beschlussanfechtung',
    notes: 'Anfechtung des Beschlusses zur Sonderumlage (85.000€). Formfehler bei Einladung.',
    createdAt: new Date('2025-12-01'),
    updatedAt: new Date('2026-01-06'),
    fristen: [
      { id: 'f3', bezeichnung: 'Anfechtungsklage einreichen', datum: '2026-01-10', typ: 'klage', erledigt: false },
    ]
  },
  {
    id: 'demo-3',
    name: 'Dr. Weber, Thomas',
    email: 't.weber@praxis-weber.de',
    phone: '040-55667788',
    address: 'Elbchaussee 120, 22763 Hamburg',
    status: 'aktiv',
    caseType: 'Gewerbemietkündigung',
    notes: 'Praxisräume gekündigt wegen Eigenbedarf. Mandant bestreitet Eigenbedarf.',
    createdAt: new Date('2025-10-20'),
    updatedAt: new Date('2026-01-03'),
    fristen: [
      { id: 'f4', bezeichnung: 'Widerspruch gegen Kündigung', datum: '2026-01-08', typ: 'widerspruch', erledigt: true },
      { id: 'f5', bezeichnung: 'Räumungsklage Erwiderung', datum: '2026-01-25', typ: 'frist', erledigt: false },
    ]
  },
  {
    id: 'demo-4',
    name: 'Fischer, Familie',
    email: 'familie.fischer@email.de',
    phone: '0221-33445566',
    address: 'Rheinufer 8, 50678 Köln',
    status: 'abgeschlossen',
    caseType: 'Kaufvertrag Immobilie',
    notes: 'Beratung beim Immobilienkauf. Kaufvertrag geprüft, Übergabe erfolgt.',
    createdAt: new Date('2025-08-10'),
    updatedAt: new Date('2025-12-15'),
    fristen: []
  },
  {
    id: 'demo-5',
    name: 'Bauer Hausverwaltung KG',
    email: 'info@bauer-hv.de',
    phone: '0711-22334455',
    address: 'Königstraße 50, 70173 Stuttgart',
    status: 'aktiv',
    caseType: 'Nebenkostenabrechnung Streit',
    notes: 'Mieter bestreitet Nebenkostenabrechnung 2024. Streitwert ca. 2.800€.',
    createdAt: new Date('2025-12-10'),
    updatedAt: new Date('2026-01-07'),
    fristen: [
      { id: 'f6', bezeichnung: 'Stellungnahme verfassen', datum: '2026-01-12', typ: 'frist', erledigt: false },
    ]
  },
];

const DEMO_DOKUMENTE: Dokument[] = [
  { id: 'doc1', name: 'Mietvertrag Müller', typ: 'vertrag', datum: '2022-03-01', mandantId: 'demo-1', notizen: 'Unbefristeter Mietvertrag' },
  { id: 'doc2', name: 'Sachverständigengutachten Schimmel', typ: 'sonstiges', datum: '2025-10-15', mandantId: 'demo-1', notizen: 'Ursache: baulicher Mangel' },
  { id: 'doc3', name: 'Protokoll ETV 2025', typ: 'protokoll', datum: '2025-06-15', mandantId: 'demo-2', notizen: 'Beschluss TOP 5 angefochten' },
  { id: 'doc4', name: 'Kündigungsschreiben', typ: 'korrespondenz', datum: '2025-09-30', mandantId: 'demo-3', notizen: 'Kündigung zum 31.03.2026' },
  { id: 'doc5', name: 'Nebenkostenabrechnung 2024', typ: 'rechnung', datum: '2025-11-01', mandantId: 'demo-5', notizen: 'Nachforderung 2.800€' },
];

export default function CRMPage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [clients, setClients] = useState<Client[]>([]);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [caseNotes, setCaseNotes] = useState<CaseNote[]>([]);
  const [newNote, setNewNote] = useState('');
  const [aiInsights, setAiInsights] = useState<any>(null);
  const [loadingInsights, setLoadingInsights] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  // NEU: Objekte für Verknüpfung
  const [verfuegbareObjekte, setVerfuegbareObjekte] = useState<ObjektRef[]>([]);
  const [showObjektVerknuepfung, setShowObjektVerknuepfung] = useState(false);
  const [showFristModal, setShowFristModal] = useState(false);
  const [newFrist, setNewFrist] = useState({
    bezeichnung: '',
    datum: '',
    typ: 'frist' as Frist['typ'],
  });
  // Dokumente (Versammlungen entfernt)
  const [dokumente, setDokumente] = useState<Dokument[]>([]);
  const [showDokumentModal, setShowDokumentModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'mandanten' | 'dokumente'>('mandanten');
  const [newDokument, setNewDokument] = useState({
    name: '',
    typ: 'vertrag' as Dokument['typ'],
    datum: new Date().toISOString().split('T')[0],
    objektId: '',
    mandantId: '',
    notizen: '',
  });
  const router = useRouter();

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    notes: '',
    status: 'aktiv' as Client['status'],
    caseType: '',
    objektIds: [] as string[],
  });
  
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

  // NEU: Alle fälligen Fristen berechnen
  const getFaelligeFristen = () => {
    const heute = new Date();
    const in7Tagen = new Date();
    in7Tagen.setDate(in7Tagen.getDate() + 7);
    
    const faellig: { client: Client; frist: Frist }[] = [];
    clients.forEach(client => {
      client.fristen?.filter(f => !f.erledigt).forEach(frist => {
        const datum = new Date(frist.datum);
        if (datum <= in7Tagen) {
          faellig.push({ client, frist });
        }
      });
    });
    return faellig.sort((a, b) => 
      new Date(a.frist.datum).getTime() - new Date(b.frist.datum).getTime()
    );
  };

  const faelligeFristen = getFaelligeFristen();

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
        
        // Load clients only for lawyers (others see demo data)
        if (hasTierAccess(tier, 'lawyer')) {
          await loadClients(currentUser.uid);
          await loadObjekte(currentUser.uid);
          await loadDokumente(currentUser.uid);
        } else {
          // Für FREE-Nutzer: Demo-Daten anzeigen
          setClients(DEMO_MANDANTEN);
          setDokumente(DEMO_DOKUMENTE);
        }
      }
      
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  // NEU: Objekte laden für Verknüpfung
  const loadObjekte = async (userId: string) => {
    try {
      const objekteRef = collection(db, 'users', userId, 'objekte');
      const snapshot = await getDocs(objekteRef);
      const objektList: ObjektRef[] = snapshot.docs.map(doc => ({
        id: doc.id,
        adresse: doc.data().adresse || '',
        ort: doc.data().ort || '',
      }));
      setVerfuegbareObjekte(objektList);
    } catch (error) {
      console.error('Error loading objekte:', error);
    }
  };

  // Dokumente laden
  const loadDokumente = async (userId: string) => {
    try {
      const dokumenteRef = collection(db, 'users', userId, 'dokumente');
      const q = query(dokumenteRef, orderBy('datum', 'desc'));
      const snapshot = await getDocs(q);
      const list: Dokument[] = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as Dokument[];
      setDokumente(list);
    } catch (error) {
      console.error('Error loading dokumente:', error);
    }
  };

  const loadClients = async (userId: string) => {
    try {
      const clientsRef = collection(db, 'users', userId, 'clients');
      const q = query(clientsRef, orderBy('createdAt', 'desc'));
      const snapshot = await getDocs(q);
      
      const clientList: Client[] = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
        createdAt: doc.data().createdAt?.toDate() || new Date(),
        updatedAt: doc.data().updatedAt?.toDate() || new Date()
      })) as Client[];
      
      setClients(clientList);
    } catch (error) {
      console.error('Error loading clients:', error);
    }
  };

  const loadCaseNotes = async (clientId: string) => {
    if (!user) return;
    try {
      const notesRef = collection(db, 'users', user.uid, 'clients', clientId, 'notes');
      const q = query(notesRef, orderBy('createdAt', 'desc'));
      const snapshot = await getDocs(q);
      
      const notes: CaseNote[] = snapshot.docs.map(doc => ({
        id: doc.id,
        content: doc.data().content,
        createdAt: doc.data().createdAt?.toDate() || new Date()
      }));
      
      setCaseNotes(notes);
    } catch (error) {
      console.error('Error loading notes:', error);
    }
  };

  const handleAddClient = async () => {
    if (!user || !formData.name || !formData.email) return;

    try {
      const clientsRef = collection(db, 'users', user.uid, 'clients');
      await addDoc(clientsRef, {
        ...formData,
        createdAt: Timestamp.now(),
        updatedAt: Timestamp.now()
      });

      await loadClients(user.uid);
      setShowAddModal(false);
      resetForm();
    } catch (error) {
      console.error('Error adding client:', error);
    }
  };

  const handleUpdateClient = async () => {
    if (!user || !selectedClient) return;

    try {
      const clientRef = doc(db, 'users', user.uid, 'clients', selectedClient.id);
      await updateDoc(clientRef, {
        ...formData,
        updatedAt: Timestamp.now()
      });

      await loadClients(user.uid);
      setShowEditModal(false);
      setSelectedClient(null);
      resetForm();
    } catch (error) {
      console.error('Error updating client:', error);
    }
  };

  const handleDeleteClient = async (clientId: string) => {
    if (!user || !confirm('Mandant wirklich löschen?')) return;

    try {
      await deleteDoc(doc(db, 'users', user.uid, 'clients', clientId));
      await loadClients(user.uid);
      if (selectedClient?.id === clientId) {
        setSelectedClient(null);
      }
    } catch (error) {
      console.error('Error deleting client:', error);
    }
  };

  const handleAddNote = async () => {
    if (!user || !selectedClient || !newNote.trim()) return;

    try {
      const notesRef = collection(db, 'users', user.uid, 'clients', selectedClient.id, 'notes');
      await addDoc(notesRef, {
        content: newNote,
        createdAt: Timestamp.now()
      });

      setNewNote('');
      await loadCaseNotes(selectedClient.id);
    } catch (error) {
      console.error('Error adding note:', error);
    }
  };

  // NEU: Frist hinzufügen
  const handleAddFrist = async () => {
    if (!user || !selectedClient || !newFrist.bezeichnung || !newFrist.datum) return;

    try {
      const fristId = `frist-${Date.now()}`;
      const neueFrist: Frist = {
        id: fristId,
        bezeichnung: newFrist.bezeichnung,
        datum: newFrist.datum,
        typ: newFrist.typ,
        erledigt: false,
      };
      
      const updatedFristen = [...(selectedClient.fristen || []), neueFrist];
      
      await updateDoc(doc(db, 'users', user.uid, 'clients', selectedClient.id), {
        fristen: updatedFristen,
        updatedAt: Timestamp.now()
      });

      setSelectedClient({ ...selectedClient, fristen: updatedFristen });
      setClients(prev => prev.map(c => 
        c.id === selectedClient.id ? { ...c, fristen: updatedFristen } : c
      ));
      
      setShowFristModal(false);
      setNewFrist({ bezeichnung: '', datum: '', typ: 'frist' });
    } catch (error) {
      console.error('Error adding frist:', error);
    }
  };

  // NEU: Frist als erledigt markieren
  const handleToggleFrist = async (fristId: string) => {
    if (!user || !selectedClient) return;

    const updatedFristen = selectedClient.fristen?.map(f => 
      f.id === fristId ? { ...f, erledigt: !f.erledigt } : f
    ) || [];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'clients', selectedClient.id), {
        fristen: updatedFristen,
        updatedAt: Timestamp.now()
      });

      setSelectedClient({ ...selectedClient, fristen: updatedFristen });
      setClients(prev => prev.map(c => 
        c.id === selectedClient.id ? { ...c, fristen: updatedFristen } : c
      ));
    } catch (error) {
      console.error('Error toggling frist:', error);
    }
  };

  // NEU: Objekt-Verknüpfung speichern
  const handleObjektVerknuepfung = async (objektId: string) => {
    if (!user || !selectedClient) return;

    const currentObjektIds = selectedClient.objektIds || [];
    const updatedObjektIds = currentObjektIds.includes(objektId)
      ? currentObjektIds.filter(id => id !== objektId)
      : [...currentObjektIds, objektId];

    try {
      await updateDoc(doc(db, 'users', user.uid, 'clients', selectedClient.id), {
        objektIds: updatedObjektIds,
        updatedAt: Timestamp.now()
      });

      setSelectedClient({ ...selectedClient, objektIds: updatedObjektIds });
      setClients(prev => prev.map(c => 
        c.id === selectedClient.id ? { ...c, objektIds: updatedObjektIds } : c
      ));
    } catch (error) {
      console.error('Error updating objekt verknuepfung:', error);
    }
  };

  // Dokument löschen
  const handleAddDokument = async () => {
    if (!user || !newDokument.name) return;

    try {
      const dokumentData = {
        ...newDokument,
        createdAt: Timestamp.now()
      };

      const docRef = await addDoc(collection(db, 'users', user.uid, 'dokumente'), dokumentData);
      
      setDokumente(prev => [{
        id: docRef.id,
        ...dokumentData
      } as Dokument, ...prev]);

      setNewDokument({
        name: '',
        typ: 'vertrag',
        datum: new Date().toISOString().split('T')[0],
        objektId: '',
        mandantId: '',
        notizen: ''
      });
      setShowDokumentModal(false);
    } catch (error) {
      console.error('Error adding dokument:', error);
    }
  };

  // NEU: Dokument löschen
  const handleDeleteDokument = async (dokumentId: string) => {
    if (!user || !confirm('Dokument wirklich löschen?')) return;

    try {
      await deleteDoc(doc(db, 'users', user.uid, 'dokumente', dokumentId));
      setDokumente(prev => prev.filter(d => d.id !== dokumentId));
    } catch (error) {
      console.error('Error deleting dokument:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      phone: '',
      address: '',
      notes: '',
      status: 'aktiv',
      caseType: '',
      objektIds: []
    });
  };

  const openEditModal = (client: Client) => {
    setSelectedClient(client);
    setFormData({
      name: client.name,
      email: client.email,
      phone: client.phone || '',
      address: client.address || '',
      notes: client.notes || '',
      status: client.status,
      caseType: client.caseType || '',
      objektIds: client.objektIds || []
    });
    setShowEditModal(true);
  };

  const selectClient = async (client: Client) => {
    setSelectedClient(client);
    await loadCaseNotes(client.id);
    setAiInsights(null); // Reset insights when switching clients
    setShowAnalysis(false);
  };

  const generateAIAnalysis = async () => {
    if (!selectedClient) return;

    setLoadingInsights(true);
    try {
      const formData = new FormData();
      formData.append('client_name', selectedClient.name);
      formData.append('case_type', selectedClient.caseType || 'Allgemein');
      formData.append('case_description', selectedClient.notes || 'Kein Fallbeschreibung');
      formData.append('case_notes', JSON.stringify(caseNotes.map(n => n.content)));

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/crm/case/analyze`, {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setAiInsights(data);
        setShowAnalysis(true);
      }
    } catch (error) {
      console.error('Failed to generate AI analysis:', error);
    } finally {
      setLoadingInsights(false);
    }
  };

  const filteredClients = clients.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || client.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const statusColors = {
    aktiv: 'bg-green-100 text-green-800',
    inaktiv: 'bg-gray-100 text-gray-800',
    abgeschlossen: 'bg-blue-100 text-blue-800'
  };

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
            <Link href="/dashboard" className="text-gray-400 hover:text-white">
              ← Dashboard
            </Link>
            <h1 className="text-lg font-semibold text-white">Mandanten-CRM</h1>
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
                <p className="text-gray-300 text-sm">Sie sehen Beispieldaten. Mit Lawyer Pro können Sie Ihre eigenen Mandanten verwalten.</p>
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

        {/* Toolbar */}
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 items-stretch sm:items-center justify-between mb-6">
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 items-stretch sm:items-center flex-1">
            <div className="relative flex-1">
              <input
                type="text"
                placeholder="Mandant suchen..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
            </div>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">Alle Status</option>
              <option value="aktiv">Aktiv</option>
              <option value="inaktiv">Inaktiv</option>
              <option value="abgeschlossen">Abgeschlossen</option>
            </select>
          </div>
          <button
            onClick={() => requireTier(() => setShowAddModal(true))}
            className="w-full sm:w-auto px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            + Neuer Mandant
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mb-6">
          <div className="bg-gray-800/50 rounded-xl p-3 sm:p-4 border border-gray-700">
            <p className="text-xs sm:text-sm text-gray-400">Gesamt</p>
            <p className="text-xl sm:text-2xl font-bold text-white">{clients.length}</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-3 sm:p-4 border border-gray-700">
            <p className="text-xs sm:text-sm text-gray-400">Aktiv</p>
            <p className="text-xl sm:text-2xl font-bold text-green-400">{clients.filter(c => c.status === 'aktiv').length}</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-3 sm:p-4 border border-gray-700">
            <p className="text-xs sm:text-sm text-gray-400">Inaktiv</p>
            <p className="text-xl sm:text-2xl font-bold text-gray-400">{clients.filter(c => c.status === 'inaktiv').length}</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-3 sm:p-4 border border-gray-700">
            <p className="text-xs sm:text-sm text-gray-400">Abgeschl.</p>
            <p className="text-xl sm:text-2xl font-bold text-blue-400">{clients.filter(c => c.status === 'abgeschlossen').length}</p>
          </div>
        </div>

        {/* NEU: Fristenwarnung */}
        {faelligeFristen.length > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 sm:p-4 mb-6">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="text-red-400 font-medium">Anstehende Fristen</p>
                <p className="text-red-300/70 text-sm">{faelligeFristen.length} Frist{faelligeFristen.length > 1 ? 'en' : ''} in den nächsten 7 Tagen</p>
              </div>
            </div>
            <div className="space-y-2">
              {faelligeFristen.map(({ client, frist }) => {
                const datum = new Date(frist.datum);
                const heute = new Date();
                const tage = Math.ceil((datum.getTime() - heute.getTime()) / (1000 * 60 * 60 * 24));
                const istUeberfaellig = tage < 0;
                
                return (
                  <div key={frist.id} className="flex flex-col sm:flex-row sm:items-center sm:justify-between bg-gray-800/50 rounded-lg p-2 text-sm gap-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={istUeberfaellig ? 'text-red-400' : tage <= 3 ? 'text-orange-400' : 'text-yellow-400'}>
                        {istUeberfaellig ? '🚨' : '⏰'}
                      </span>
                      <span className="text-white font-medium">{frist.bezeichnung}</span>
                      <span className="hidden sm:inline text-gray-500">•</span>
                      <span className="text-gray-400 text-xs sm:text-sm">{client.name}</span>
                    </div>
                    <div className="flex items-center gap-2 justify-between sm:justify-end">
                      <span className={`text-xs sm:text-sm ${istUeberfaellig ? 'text-red-400 font-bold' : tage <= 3 ? 'text-orange-400' : 'text-yellow-400'}`}>
                        {datum.toLocaleDateString('de-DE')} ({istUeberfaellig ? `${Math.abs(tage)}d überfällig!` : `in ${tage}d`})
                      </span>
                      <button
                        onClick={() => {
                          selectClient(client);
                          handleToggleFrist(frist.id);
                        }}
                        className="px-2 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-xs whitespace-nowrap"
                      >
                        ✓ Erledigt
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Tab-Navigation */}
        <div className="flex gap-2 mb-6 border-b border-gray-700 pb-4">
          <button
            onClick={() => setActiveTab('mandanten')}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              activeTab === 'mandanten'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800/50 text-gray-400 hover:text-white'
            }`}
          >
            👥 Mandanten ({clients.length})
          </button>
          <button
            onClick={() => setActiveTab('dokumente')}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              activeTab === 'dokumente'
                ? 'bg-green-600 text-white'
                : 'bg-gray-800/50 text-gray-400 hover:text-white'
            }`}
          >
            📄 Dokumente ({dokumente.length})
          </button>
        </div>

        {/* Mandanten Tab */}
        {activeTab === 'mandanten' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Client List */}
          <div className="lg:col-span-1 bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden">
            <div className="p-4 border-b border-gray-700">
              <h2 className="font-semibold text-white">Mandanten ({filteredClients.length})</h2>
            </div>
            <div className="divide-y divide-gray-700 max-h-[600px] overflow-y-auto">
              {filteredClients.length === 0 ? (
                <div className="p-8 text-center text-gray-400">
                  <p className="text-4xl mb-4">👥</p>
                  <p>Keine Mandanten gefunden</p>
                </div>
              ) : (
                filteredClients.map((client) => (
                  <button
                    key={client.id}
                    onClick={() => selectClient(client)}
                    className={`w-full p-4 text-left hover:bg-gray-700/50 transition-colors ${
                      selectedClient?.id === client.id ? 'bg-blue-900/30 border-l-4 border-blue-500' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-white">{client.name}</p>
                        <p className="text-sm text-gray-400">{client.email}</p>
                        {client.caseType && (
                          <p className="text-xs text-gray-500 mt-1">{client.caseType}</p>
                        )}
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full ${statusColors[client.status]}`}>
                        {client.status}
                      </span>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>

          {/* Client Detail */}
          <div className="lg:col-span-2 bg-gray-800/50 rounded-xl border border-gray-700">
            {selectedClient ? (
              <div>
                <div className="p-4 sm:p-6 border-b border-gray-700">
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-0">
                    <div>
                      <h2 className="text-lg sm:text-xl font-bold text-white">{selectedClient.name}</h2>
                      <p className="text-gray-400 text-sm sm:text-base truncate">{selectedClient.email}</p>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => openEditModal(selectedClient)}
                        className="px-3 sm:px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-700 transition-colors text-sm sm:text-base"
                      >
                        ✏️ <span className="hidden sm:inline">Bearbeiten</span>
                      </button>
                      <button
                        onClick={() => handleDeleteClient(selectedClient.id)}
                        className="px-4 py-2 border border-red-700 text-red-400 rounded-lg hover:bg-red-900/30 transition-colors"
                      >
                        🗑️ Löschen
                      </button>
                    </div>
                  </div>
                </div>

                <div className="p-4 sm:p-6 grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                  <div>
                    <h3 className="text-sm font-medium text-gray-400 mb-2">Kontaktdaten</h3>
                    <div className="space-y-2 text-gray-300">
                      <p><span className="text-gray-500">📧</span> {selectedClient.email}</p>
                      {selectedClient.phone && <p><span className="text-gray-500">📞</span> {selectedClient.phone}</p>}
                      {selectedClient.address && <p><span className="text-gray-500">📍</span> {selectedClient.address}</p>}
                    </div>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-400 mb-2">Fall-Details</h3>
                    <div className="space-y-2 text-gray-300">
                      <p><span className="text-gray-500">📋</span> Status: <span className={`px-2 py-0.5 rounded-full text-xs ${statusColors[selectedClient.status]}`}>{selectedClient.status}</span></p>
                      {selectedClient.caseType && <p><span className="text-gray-500">⚖️</span> Fallart: {selectedClient.caseType}</p>}
                      <p><span className="text-gray-500">📅</span> Angelegt: {selectedClient.createdAt.toLocaleDateString('de-DE')}</p>
                    </div>
                  </div>
                </div>

                {selectedClient.notes && (
                  <div className="px-6 pb-6">
                    <h3 className="text-sm font-medium text-gray-400 mb-2">Notizen</h3>
                    <p className="p-3 bg-gray-900/50 rounded-lg text-gray-300">{selectedClient.notes}</p>
                  </div>
                )}

                {/* NEU: Verknüpfte Objekte */}
                <div className="px-6 pb-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-medium text-gray-400">🏢 Verknüpfte Objekte</h3>
                    <button
                      onClick={() => setShowObjektVerknuepfung(true)}
                      className="text-xs text-blue-400 hover:text-blue-300"
                    >
                      + Objekt verknüpfen
                    </button>
                  </div>
                  {(!selectedClient.objektIds || selectedClient.objektIds.length === 0) ? (
                    <p className="text-gray-500 text-sm">Keine Objekte verknüpft</p>
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {selectedClient.objektIds.map(id => {
                        const objekt = verfuegbareObjekte.find(o => o.id === id);
                        return objekt ? (
                          <span key={id} className="px-3 py-1 bg-gray-800 rounded-lg text-sm text-gray-300 flex items-center gap-2">
                            🏠 {objekt.adresse}, {objekt.ort}
                            <button
                              onClick={() => handleObjektVerknuepfung(id)}
                              className="text-gray-500 hover:text-red-400"
                            >
                              ✕
                            </button>
                          </span>
                        ) : null;
                      })}
                    </div>
                  )}
                </div>

                {/* NEU: Fristen */}
                <div className="px-6 pb-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-medium text-gray-400">⏰ Fristen & Termine</h3>
                    <button
                      onClick={() => setShowFristModal(true)}
                      className="text-xs text-blue-400 hover:text-blue-300"
                    >
                      + Frist hinzufügen
                    </button>
                  </div>
                  {(!selectedClient.fristen || selectedClient.fristen.length === 0) ? (
                    <p className="text-gray-500 text-sm">Keine Fristen hinterlegt</p>
                  ) : (
                    <div className="space-y-2">
                      {selectedClient.fristen.map(frist => {
                        const datum = new Date(frist.datum);
                        const heute = new Date();
                        const tage = Math.ceil((datum.getTime() - heute.getTime()) / (1000 * 60 * 60 * 24));
                        const istUeberfaellig = tage < 0 && !frist.erledigt;
                        
                        return (
                          <div key={frist.id} className={`flex items-center justify-between p-2 rounded-lg ${
                            frist.erledigt ? 'bg-gray-800/30' : istUeberfaellig ? 'bg-red-900/30 border border-red-700/50' : tage <= 7 ? 'bg-yellow-900/20 border border-yellow-700/50' : 'bg-gray-800/50'
                          }`}>
                            <div className="flex items-center gap-2">
                              <span>{frist.erledigt ? '✅' : istUeberfaellig ? '🚨' : '⏰'}</span>
                              <span className={frist.erledigt ? 'text-gray-500 line-through' : 'text-white'}>{frist.bezeichnung}</span>
                              <span className="text-xs px-2 py-0.5 bg-gray-700 rounded text-gray-400">{frist.typ}</span>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className={`text-sm ${frist.erledigt ? 'text-gray-500' : istUeberfaellig ? 'text-red-400' : tage <= 7 ? 'text-yellow-400' : 'text-gray-400'}`}>
                                {datum.toLocaleDateString('de-DE')}
                                {!frist.erledigt && (istUeberfaellig ? ` (${Math.abs(tage)}d überfällig)` : ` (in ${tage}d)`)}
                              </span>
                              <button
                                onClick={() => handleToggleFrist(frist.id)}
                                className={`px-2 py-1 rounded text-xs ${frist.erledigt ? 'bg-gray-700 text-gray-400' : 'bg-green-600 text-white'}`}
                              >
                                {frist.erledigt ? 'Wiederherstellen' : '✓ Erledigt'}
                              </button>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Case Notes Section */}
                <div className="border-t border-gray-700 p-6">
                  <h3 className="font-semibold text-white mb-4">Aktennotizen</h3>
                  
                  {/* Add Note */}
                  <div className="flex gap-2 mb-4">
                    <input
                      type="text"
                      value={newNote}
                      onChange={(e) => setNewNote(e.target.value)}
                      placeholder="Neue Notiz hinzufügen..."
                      className="flex-1 px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                      onKeyPress={(e) => e.key === 'Enter' && handleAddNote()}
                    />
                    <button
                      onClick={handleAddNote}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Hinzufügen
                    </button>
                  </div>

                  {/* Notes List */}
                  <div className="space-y-3 max-h-[300px] overflow-y-auto">
                    {caseNotes.length === 0 ? (
                      <p className="text-gray-500 text-center py-4">Keine Notizen vorhanden</p>
                    ) : (
                      caseNotes.map((note) => (
                        <div key={note.id} className="p-3 bg-gray-900/50 rounded-lg">
                          <p className="text-gray-300">{note.content}</p>
                          <p className="text-xs text-gray-500 mt-2">
                            {note.createdAt.toLocaleDateString('de-DE')} um {note.createdAt.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="border-t border-gray-700 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-white">🤖 KI-Fallanalyse</h3>
                    <button
                      onClick={generateAIAnalysis}
                      disabled={loadingInsights}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
                    >
                      {loadingInsights ? '⏳ Analysiere...' : '✨ Analyse starten'}
                    </button>
                  </div>

                  {showAnalysis && aiInsights && (
                    <div className="space-y-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
                      {/* Analysis */}
                      {aiInsights.analysis && (
                        <div>
                          <h4 className="font-semibold text-[#1e3a5f] mb-2">📋 Fallanalyse</h4>
                          <p className="text-gray-700 text-sm">{aiInsights.analysis}</p>
                        </div>
                      )}

                      <div className="grid md:grid-cols-2 gap-4">
                        {/* Strengths */}
                        {aiInsights.strengths && aiInsights.strengths.length > 0 && (
                          <div className="bg-white rounded-lg p-4">
                            <h4 className="font-semibold text-green-700 mb-2 flex items-center gap-2">
                              <span>💪</span> Stärken
                            </h4>
                            <ul className="space-y-1 text-sm text-gray-700">
                              {aiInsights.strengths.map((item: string, idx: number) => (
                                <li key={idx} className="flex items-start gap-2">
                                  <span className="text-green-600 mt-0.5">✓</span>
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {/* Weaknesses */}
                        {aiInsights.weaknesses && aiInsights.weaknesses.length > 0 && (
                          <div className="bg-white rounded-lg p-4">
                            <h4 className="font-semibold text-amber-700 mb-2 flex items-center gap-2">
                              <span>⚠️</span> Risiken
                            </h4>
                            <ul className="space-y-1 text-sm text-gray-700">
                              {aiInsights.weaknesses.map((item: string, idx: number) => (
                                <li key={idx} className="flex items-start gap-2">
                                  <span className="text-amber-600 mt-0.5">!</span>
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>

                      {/* Recommendations */}
                      {aiInsights.recommendations && aiInsights.recommendations.length > 0 && (
                        <div className="bg-white rounded-lg p-4">
                          <h4 className="font-semibold text-[#1e3a5f] mb-2 flex items-center gap-2">
                            <span>🎯</span> Strategieempfehlung
                          </h4>
                          <ul className="space-y-2 text-sm text-gray-700">
                            {aiInsights.recommendations.map((item: string, idx: number) => (
                              <li key={idx} className="flex items-start gap-2">
                                <span className="text-[#b8860b] font-bold mt-0.5">{idx + 1}.</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Next Steps */}
                      {aiInsights.next_steps && aiInsights.next_steps.length > 0 && (
                        <div className="bg-white rounded-lg p-4">
                          <h4 className="font-semibold text-[#1e3a5f] mb-2 flex items-center gap-2">
                            <span>▶️</span> Nächste Schritte
                          </h4>
                          <ul className="space-y-2 text-sm text-gray-700">
                            {aiInsights.next_steps.map((item: string, idx: number) => (
                              <li key={idx} className="flex items-start gap-2">
                                <span className="text-blue-600 mt-0.5">→</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Quick Actions */}
                <div className="border-t border-gray-700 p-6">
                  <h3 className="font-semibold text-white mb-4">Schnellaktionen</h3>
                  <div className="flex flex-wrap gap-3">
                    <Link
                      href={`/app?prompt=Mein Mandant ${selectedClient.name} hat folgendes Problem: `}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      💬 KI-Beratung starten
                    </Link>
                    <Link
                      href="/app/documents/generate"
                      className="px-4 py-2 border border-blue-500 text-blue-400 rounded-lg hover:bg-blue-900/30 transition-colors"
                    >
                      📝 Schriftsatz erstellen
                    </Link>
                    <button
                      onClick={() => window.open(`mailto:${selectedClient.email}`, '_blank')}
                      className="px-4 py-2 border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-700 transition-colors"
                    >
                      ✉️ E-Mail senden
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-12 text-center text-gray-400">
                <p className="text-6xl mb-4">👈</p>
                <p className="text-lg">Wählen Sie einen Mandanten aus der Liste</p>
                <p className="text-sm mt-2">oder erstellen Sie einen neuen Mandanten</p>
              </div>
            )}
          </div>
        </div>
        )}

        {/* Dokumente Tab */}
        {activeTab === 'dokumente' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-white">📄 Dokumentenverwaltung</h2>
              <button
                onClick={() => requireTier(() => setShowDokumentModal(true))}
                className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
              >
                + Neues Dokument
              </button>
            </div>

            {/* Dokumente Filter */}
            <div className="flex gap-2 flex-wrap">
              {['alle', 'vertrag', 'protokoll', 'rechnung', 'bescheid', 'korrespondenz', 'sonstiges'].map(typ => (
                <button
                  key={typ}
                  className="px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-gray-400 hover:text-white hover:border-gray-600 transition-colors capitalize"
                >
                  {typ === 'alle' ? 'Alle' : typ}
                </button>
              ))}
            </div>

            {dokumente.length === 0 ? (
              <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-12 text-center">
                <span className="text-6xl block mb-4">📄</span>
                <p className="text-gray-400 text-lg mb-2">Keine Dokumente vorhanden</p>
                <p className="text-gray-500 text-sm">Laden Sie Ihr erstes Dokument hoch oder erstellen Sie einen Eintrag</p>
              </div>
            ) : (
              <div className="bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-900/50">
                    <tr>
                      <th className="text-left p-4 text-gray-400 font-medium">Dokument</th>
                      <th className="text-left p-4 text-gray-400 font-medium">Typ</th>
                      <th className="text-left p-4 text-gray-400 font-medium">Datum</th>
                      <th className="text-left p-4 text-gray-400 font-medium">Verknüpfung</th>
                      <th className="text-left p-4 text-gray-400 font-medium">Aktionen</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-700">
                    {dokumente.map(dok => {
                      const objekt = verfuegbareObjekte.find(o => o.id === dok.objektId);
                      const mandant = clients.find(c => c.id === dok.mandantId);
                      
                      return (
                        <tr key={dok.id} className="hover:bg-gray-700/30">
                          <td className="p-4">
                            <div className="flex items-center gap-3">
                              <span className="text-2xl">
                                {dok.typ === 'vertrag' ? '📝' :
                                 dok.typ === 'protokoll' ? '📋' :
                                 dok.typ === 'rechnung' ? '💰' :
                                 dok.typ === 'bescheid' ? '📨' :
                                 dok.typ === 'korrespondenz' ? '✉️' : '📄'}
                              </span>
                              <div>
                                <p className="text-white font-medium">{dok.name}</p>
                                {dok.notizen && <p className="text-gray-500 text-sm truncate max-w-xs">{dok.notizen}</p>}
                              </div>
                            </div>
                          </td>
                          <td className="p-4">
                            <span className="px-2 py-1 bg-gray-700 rounded text-gray-300 text-sm capitalize">{dok.typ}</span>
                          </td>
                          <td className="p-4 text-gray-300">
                            {new Date(dok.datum).toLocaleDateString('de-DE')}
                          </td>
                          <td className="p-4">
                            <div className="space-y-1">
                              {objekt && (
                                <span className="block text-blue-400 text-sm">🏠 {objekt.adresse}</span>
                              )}
                              {mandant && (
                                <span className="block text-purple-400 text-sm">👤 {mandant.name}</span>
                              )}
                              {!objekt && !mandant && (
                                <span className="text-gray-500 text-sm">-</span>
                              )}
                            </div>
                          </td>
                          <td className="p-4">
                            <button
                              onClick={() => handleDeleteDokument(dok.id)}
                              className="text-red-400 hover:text-red-300"
                            >
                              🗑️
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Add/Edit Modal */}
      {(showAddModal || showEditModal) && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-6">
              {showAddModal ? 'Neuen Mandanten anlegen' : 'Mandant bearbeiten'}
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                  placeholder="Max Mustermann"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">E-Mail *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                  placeholder="max@example.com"
                />
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Telefon</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                    placeholder="+49 123 456789"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value as Client['status'] })}
                    className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="aktiv">Aktiv</option>
                    <option value="inaktiv">Inaktiv</option>
                    <option value="abgeschlossen">Abgeschlossen</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Adresse</label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                  placeholder="Musterstraße 1, 12345 Berlin"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Fallart</label>
                <select
                  value={formData.caseType}
                  onChange={(e) => setFormData({ ...formData, caseType: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Bitte wählen...</option>
                  <option value="Mietrecht">Mietrecht</option>
                  <option value="WEG-Recht">WEG-Recht</option>
                  <option value="Kaufvertrag">Kaufvertrag</option>
                  <option value="Maklerrecht">Maklerrecht</option>
                  <option value="Baurecht">Baurecht</option>
                  <option value="Grundstücksrecht">Grundstücksrecht</option>
                  <option value="Steuerrecht">Steuerrecht</option>
                  <option value="Sonstiges">Sonstiges</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Notizen</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full px-4 py-2 bg-gray-700/50 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500"
                  rows={3}
                  placeholder="Weitere Informationen zum Mandanten..."
                />
              </div>
            </div>
            
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => {
                  setShowAddModal(false);
                  setShowEditModal(false);
                  resetForm();
                }}
                className="flex-1 py-3 border border-gray-600 text-gray-300 rounded-lg font-medium hover:bg-gray-700 transition-colors"
              >
                Abbrechen
              </button>
              <button
                onClick={showAddModal ? handleAddClient : handleUpdateClient}
                disabled={!formData.name || !formData.email}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
              >
                {showAddModal ? 'Mandant anlegen' : 'Speichern'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* NEU: Frist hinzufügen Modal */}
      {showFristModal && selectedClient && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-md w-full">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">⏰ Frist hinzufügen</h2>
                <button onClick={() => setShowFristModal(false)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Fristtyp</label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {[
                    { id: 'klage', label: 'Klage', icon: '⚖️' },
                    { id: 'widerspruch', label: 'Widerspruch', icon: '📝' },
                    { id: 'frist', label: 'Frist', icon: '⏰' },
                    { id: 'termin', label: 'Termin', icon: '📅' },
                    { id: 'sonstiges', label: 'Sonstiges', icon: '📋' },
                  ].map(typ => (
                    <button
                      key={typ.id}
                      onClick={() => setNewFrist({ ...newFrist, typ: typ.id as Frist['typ'] })}
                      className={`p-2 rounded-lg border text-center transition-colors ${
                        newFrist.typ === typ.id
                          ? 'border-blue-500 bg-blue-500/20 text-white'
                          : 'border-gray-700 bg-gray-800/50 text-gray-400 hover:border-gray-600'
                      }`}
                    >
                      <span className="text-lg block mb-1">{typ.icon}</span>
                      <span className="text-xs">{typ.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Bezeichnung *</label>
                <input
                  type="text"
                  value={newFrist.bezeichnung}
                  onChange={(e) => setNewFrist({ ...newFrist, bezeichnung: e.target.value })}
                  placeholder="z.B. Widerspruchsfrist Kündigung..."
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Datum *</label>
                <input
                  type="date"
                  value={newFrist.datum}
                  onChange={(e) => setNewFrist({ ...newFrist, datum: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-blue-500"
                />
              </div>
            </div>
            <div className="p-6 border-t border-gray-700 flex gap-3">
              <button
                onClick={() => setShowFristModal(false)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                Abbrechen
              </button>
              <button
                onClick={handleAddFrist}
                disabled={!newFrist.bezeichnung || !newFrist.datum}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
              >
                Frist speichern
              </button>
            </div>
          </div>
        </div>
      )}

      {/* NEU: Objekt-Verknüpfung Modal */}
      {showObjektVerknuepfung && selectedClient && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-md w-full">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">🏢 Objekte verknüpfen</h2>
                <button onClick={() => setShowObjektVerknuepfung(false)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            <div className="p-6">
              {verfuegbareObjekte.length === 0 ? (
                <div className="text-center py-8">
                  <span className="text-4xl block mb-4">🏠</span>
                  <p className="text-gray-400 mb-4">Keine Objekte vorhanden</p>
                  <Link
                    href="/app/objekte"
                    className="text-blue-400 hover:text-blue-300"
                  >
                    → Zur Objektverwaltung
                  </Link>
                </div>
              ) : (
                <div className="space-y-2 max-h-80 overflow-y-auto">
                  {verfuegbareObjekte.map(objekt => {
                    const isSelected = selectedClient.objektIds?.includes(objekt.id);
                    return (
                      <button
                        key={objekt.id}
                        onClick={() => handleObjektVerknuepfung(objekt.id)}
                        className={`w-full flex items-center justify-between p-3 rounded-lg border transition-colors ${
                          isSelected
                            ? 'border-blue-500 bg-blue-500/20 text-white'
                            : 'border-gray-700 bg-gray-800/50 text-gray-300 hover:border-gray-600'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">🏠</span>
                          <div className="text-left">
                            <p className="font-medium">{objekt.adresse}</p>
                            <p className="text-sm text-gray-400">{objekt.ort}</p>
                          </div>
                        </div>
                        {isSelected && <span className="text-blue-400">✓</span>}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
            <div className="p-6 border-t border-gray-700">
              <button
                onClick={() => setShowObjektVerknuepfung(false)}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
              >
                Fertig
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Dokument hinzufügen Modal */}
      {showDokumentModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 rounded-2xl border border-gray-700 max-w-lg w-full">
            <div className="p-6 border-b border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white">📄 Neues Dokument</h2>
                <button onClick={() => setShowDokumentModal(false)} className="text-gray-400 hover:text-white">✕</button>
              </div>
            </div>
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Bezeichnung *</label>
                <input
                  type="text"
                  value={newDokument.name}
                  onChange={(e) => setNewDokument({ ...newDokument, name: e.target.value })}
                  placeholder="z.B. Mietvertrag Müller, Protokoll EV 2024..."
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-green-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Dokumenttyp</label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { id: 'vertrag', label: 'Vertrag', icon: '📝' },
                    { id: 'protokoll', label: 'Protokoll', icon: '📋' },
                    { id: 'rechnung', label: 'Rechnung', icon: '💰' },
                    { id: 'bescheid', label: 'Bescheid', icon: '📨' },
                    { id: 'korrespondenz', label: 'Korrespondenz', icon: '✉️' },
                    { id: 'sonstiges', label: 'Sonstiges', icon: '📄' },
                  ].map(typ => (
                    <button
                      key={typ.id}
                      onClick={() => setNewDokument({ ...newDokument, typ: typ.id as Dokument['typ'] })}
                      className={`p-2 rounded-lg border text-center transition-colors ${
                        newDokument.typ === typ.id
                          ? 'border-green-500 bg-green-500/20 text-white'
                          : 'border-gray-700 bg-gray-800/50 text-gray-400 hover:border-gray-600'
                      }`}
                    >
                      <span className="text-lg block mb-1">{typ.icon}</span>
                      <span className="text-xs">{typ.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Datum</label>
                <input
                  type="date"
                  value={newDokument.datum}
                  onChange={(e) => setNewDokument({ ...newDokument, datum: e.target.value })}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-green-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Objekt verknüpfen</label>
                  <select
                    value={newDokument.objektId}
                    onChange={(e) => setNewDokument({ ...newDokument, objektId: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-green-500"
                  >
                    <option value="">Kein Objekt</option>
                    {verfuegbareObjekte.map(obj => (
                      <option key={obj.id} value={obj.id}>{obj.adresse}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Mandant verknüpfen</label>
                  <select
                    value={newDokument.mandantId}
                    onChange={(e) => setNewDokument({ ...newDokument, mandantId: e.target.value })}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:border-green-500"
                  >
                    <option value="">Kein Mandant</option>
                    {clients.map(c => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Notizen</label>
                <textarea
                  value={newDokument.notizen}
                  onChange={(e) => setNewDokument({ ...newDokument, notizen: e.target.value })}
                  placeholder="Optionale Beschreibung..."
                  rows={2}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-green-500"
                />
              </div>
            </div>
            <div className="p-6 border-t border-gray-700 flex gap-3">
              <button
                onClick={() => setShowDokumentModal(false)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
              >
                Abbrechen
              </button>
              <button
                onClick={handleAddDokument}
                disabled={!newDokument.name}
                className="flex-1 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
              >
                Dokument speichern
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
        feature="Mandanten-CRM"
      />
    </div>
  );
}
