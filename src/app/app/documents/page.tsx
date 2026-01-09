'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, query, orderBy, getDocs, deleteDoc, doc, updateDoc, getDoc, addDoc, serverTimestamp } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import { apiClient, DocumentSearchResult } from '@/lib/api';
import UpgradeModal from '@/components/UpgradeModal';
import { useDropzone } from 'react-dropzone';
import { hasTierAccess } from '@/lib/tierUtils';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';

// =========================================================================
// TYPEN & KONSTANTEN
// =========================================================================

interface ManagedDocument {
  id: string;
  name: string;
  content: string;
  category: DocumentCategory;
  status: DocumentStatus;
  clientId?: string;
  clientName?: string;
  caseNumber?: string;
  mandateId?: string;
  fileName?: string;
  fileType?: string;
  fileSize?: number;
  aiSummary?: string;
  aiKeywords?: string[];
  aiDocumentType?: string;
  deadlines?: DocumentDeadline[];
  sourceApp?: 'upload' | 'schriftsatz' | 'vertragsanalyse' | 'fallanalyse' | 'musterbriefe' | 'checkout' | 'import';
  sourceDocId?: string;
  createdAt: Date;
  updatedAt?: Date;
  version?: number;
  parentDocId?: string;
  tags?: string[];
}

interface DocumentDeadline {
  id: string;
  title: string;
  dueDate: Date;
  reminderDays?: number;
  completed?: boolean;
  type: 'frist' | 'wiedervorlage' | 'termin';
}

// Neue vereinfachte Kategorien: Zwei Welten
type DocumentCategory = 
  | 'eigene_vertraege'    // Echte abgeschlossene Verträge mit Anlagen
  | 'mustervorlagen'      // Selbst erstellte Vorlagen
  | 'archiv';             // Archivierte Dokumente

type DocumentStatus = 'entwurf' | 'aktiv' | 'abgeschlossen' | 'archiviert';

// Hauptkategorien (die zwei Welten)
const MAIN_CATEGORIES: { id: DocumentCategory; label: string; icon: string; description: string }[] = [
  { id: 'eigene_vertraege', label: 'Meine Verträge', icon: '📄', description: 'Echte abgeschlossene Verträge mit Anlagen • KI-Fristenerkennung' },
  { id: 'mustervorlagen', label: 'Meine Vorlagen', icon: '📋', description: 'Selbst erstellte Mustervorlagen' },
  { id: 'archiv', label: 'Archiv', icon: '🗄️', description: 'Archivierte Dokumente' },
];

const STATUS_OPTIONS: { id: DocumentStatus; label: string; color: string }[] = [
  { id: 'entwurf', label: 'Entwurf', color: 'bg-gray-600 text-gray-200' },
  { id: 'aktiv', label: 'Aktiv', color: 'bg-green-600 text-green-100' },
  { id: 'abgeschlossen', label: 'Abgeschlossen', color: 'bg-blue-600 text-blue-100' },
  { id: 'archiviert', label: 'Archiviert', color: 'bg-amber-600 text-amber-100' }
];

// ===== DEMO-DATEN FÜR FREE-NUTZER (sofort sichtbar) =====
const DEMO_DOKUMENTE: ManagedDocument[] = [
  {
    id: 'demo-doc1',
    name: 'Mietvertrag Müller - Berliner Str. 42',
    content: 'Mietvertrag zwischen Petra Müller (Mieterin) und Großstadt Immobilien GmbH (Vermieterin)...',
    category: 'eigene_vertraege',
    status: 'aktiv',
    clientName: 'Müller, Petra',
    caseNumber: 'Az. 67 C 2345/25',
    aiSummary: 'Unbefristeter Wohnungsmietvertrag mit 3-monatiger Kündigungsfrist. Schönheitsreparaturen auf Mieter übertragen (möglicherweise unwirksam nach BGH-Rechtsprechung).',
    aiKeywords: ['Mietvertrag', 'Wohnungsmiete', 'Schönheitsreparaturen', 'Kündigungsfrist'],
    aiDocumentType: 'Mietvertrag',
    deadlines: [
      { id: 'd1', title: 'Kündigungsfrist prüfen', dueDate: new Date('2026-03-01'), type: 'wiedervorlage', completed: false }
    ],
    sourceApp: 'upload',
    createdAt: new Date('2025-11-15'),
    updatedAt: new Date('2025-12-20'),
    tags: ['Schimmel', 'Mietminderung']
  },
  {
    id: 'demo-doc2',
    name: 'Sachverständigengutachten Schimmel',
    content: 'Gutachten zur Feststellung der Schimmelursache in der Mietwohnung Berliner Str. 42...',
    category: 'eigene_vertraege',
    status: 'aktiv',
    clientName: 'Müller, Petra',
    caseNumber: 'Az. 67 C 2345/25',
    aiSummary: 'Gutachten bestätigt baulichen Mangel als Ursache des Schimmelbefalls. Empfohlene Mietminderung: 20-25%.',
    aiKeywords: ['Gutachten', 'Schimmel', 'Baumangel', 'Mietminderung'],
    aiDocumentType: 'Sachverständigengutachten',
    sourceApp: 'upload',
    createdAt: new Date('2025-10-20'),
    tags: ['Beweismittel', 'Schimmel']
  },
  {
    id: 'demo-doc3',
    name: 'Klageerwiderung Mietminderung',
    content: 'In dem Rechtsstreit Großstadt Immobilien GmbH ./. Müller wird namens und in Vollmacht der Beklagten vorgetragen...',
    category: 'eigene_vertraege',
    status: 'entwurf',
    clientName: 'Müller, Petra',
    caseNumber: 'Az. 67 C 2345/25',
    aiSummary: 'Entwurf der Klageerwiderung. Kernargument: Mietminderung gem. § 536 BGB berechtigt, da Schimmelbefall baulich bedingt.',
    aiKeywords: ['Klageerwiderung', 'Mietminderung', '§ 536 BGB'],
    aiDocumentType: 'Schriftsatz',
    deadlines: [
      { id: 'd2', title: 'Einreichungsfrist AG Berlin-Mitte', dueDate: new Date('2026-01-15'), type: 'frist', completed: false }
    ],
    sourceApp: 'schriftsatz',
    createdAt: new Date('2026-01-03'),
    tags: ['Frist kritisch']
  },
  {
    id: 'demo-doc4',
    name: 'WEG-Protokoll ETV 2025',
    content: 'Protokoll der ordentlichen Eigentümerversammlung vom 15.06.2025...',
    category: 'eigene_vertraege',
    status: 'aktiv',
    clientName: 'Schmidt GmbH',
    caseNumber: 'Noch nicht vergeben',
    aiSummary: 'Beschluss TOP 5 (Sonderumlage 85.000€) anfechtbar wegen Formfehler bei Einladung (Frist nicht eingehalten).',
    aiKeywords: ['WEG', 'Eigentümerversammlung', 'Sonderumlage', 'Beschlussanfechtung'],
    aiDocumentType: 'Versammlungsprotokoll',
    deadlines: [
      { id: 'd3', title: 'Anfechtungsfrist 1 Monat', dueDate: new Date('2026-01-10'), type: 'frist', completed: false }
    ],
    sourceApp: 'upload',
    createdAt: new Date('2025-12-01'),
    tags: ['Anfechtung']
  },
  {
    id: 'demo-doc5',
    name: 'Vorlage: Mieterhöhungsverlangen',
    content: 'Sehr geehrte/r [Mieter],\n\nhiermit verlange ich gem. § 558 BGB eine Erhöhung der Miete...',
    category: 'mustervorlagen',
    status: 'aktiv',
    aiSummary: 'Mustervorlage für Mieterhöhung nach Mietspiegel gem. § 558 BGB.',
    aiKeywords: ['Mieterhöhung', '§ 558 BGB', 'Mietspiegel'],
    aiDocumentType: 'Vorlage',
    sourceApp: 'musterbriefe',
    createdAt: new Date('2025-09-10'),
    tags: ['Vermieter']
  },
  {
    id: 'demo-doc6',
    name: 'Vorlage: Mahnung Hausgeld',
    content: 'Mahnung\n\nSehr geehrte/r [Eigentümer],\n\nleider mussten wir feststellen, dass folgende Hausgelder noch ausstehen...',
    category: 'mustervorlagen',
    status: 'aktiv',
    aiSummary: 'Mustervorlage für Hausgeld-Mahnung an säumige WEG-Eigentümer.',
    aiKeywords: ['Mahnung', 'Hausgeld', 'WEG'],
    aiDocumentType: 'Vorlage',
    sourceApp: 'musterbriefe',
    createdAt: new Date('2025-08-20'),
    tags: ['WEG', 'Mahnung']
  },
];

// =========================================================================
// HAUPTKOMPONENTE
// =========================================================================

export default function DocumentsPage() {
  const router = useRouter();
  
  const [user, setUser] = useState<any>(null);
  const [userTier, setUserTier] = useState<string>('free');
  const [loading, setLoading] = useState(true);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  
  const [documents, setDocuments] = useState<ManagedDocument[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<DocumentCategory | 'all'>('all');
  const [selectedDoc, setSelectedDoc] = useState<ManagedDocument | null>(null);
  const [filterStatus, setFilterStatus] = useState<DocumentStatus | 'all'>('all');
  
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<DocumentSearchResult[]>([]);
  const [useAISearch, setUseAISearch] = useState(false);
  
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [pendingFile, setPendingFile] = useState<{ name: string; content: string; type: string } | null>(null);
  const [aiAnalysis, setAiAnalysis] = useState<any>(null);
  
  const [upcomingDeadlines, setUpcomingDeadlines] = useState<{doc: ManagedDocument; deadline: DocumentDeadline}[]>([]);
  
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<string | null>(null);
  const [showMoveModal, setShowMoveModal] = useState<ManagedDocument | null>(null);
  const [showDeadlineModal, setShowDeadlineModal] = useState<ManagedDocument | null>(null);
  const [showAddAttachmentModal, setShowAddAttachmentModal] = useState<ManagedDocument | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [attachmentFile, setAttachmentFile] = useState<{ name: string; content: string; type: string } | null>(null);

  // Check if user has access (Lawyer only)
  const hasAccess = hasTierAccess(userTier, 'lawyer');
  
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  // =========================================================================
  // AUTH & LOAD
  // =========================================================================

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      if (userDoc.exists()) {
        const userData = userDoc.data();
        const tier = userData.tier || userData.dashboardType || 'free';
        setUserTier(tier);
        
        if (hasTierAccess(tier, 'lawyer')) {
          await loadDocuments(currentUser.uid);
        } else {
          // Für FREE-Nutzer: Demo-Daten anzeigen
          setDocuments(DEMO_DOKUMENTE);
          // Berechne Demo-Fristen
          const now = new Date();
          const in14Days = new Date(now.getTime() + 14 * 24 * 60 * 60 * 1000);
          const deadlines: {doc: ManagedDocument; deadline: DocumentDeadline}[] = [];
          DEMO_DOKUMENTE.forEach(d => {
            d.deadlines?.forEach(deadline => {
              if (!deadline.completed && deadline.dueDate <= in14Days) {
                deadlines.push({ doc: d, deadline });
              }
            });
          });
          deadlines.sort((a, b) => a.deadline.dueDate.getTime() - b.deadline.dueDate.getTime());
          setUpcomingDeadlines(deadlines);
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
      
      setUser(currentUser);
    });

    return () => unsubscribe();
  }, [router]);

  const loadDocuments = async (userId: string) => {
    setLoading(true);
    try {
      const q = query(
        collection(db, 'users', userId, 'managed_documents'),
        orderBy('createdAt', 'desc')
      );
      const snapshot = await getDocs(q);
      const docs = snapshot.docs.map(docSnap => ({
        id: docSnap.id,
        ...docSnap.data(),
        createdAt: docSnap.data().createdAt?.toDate() || new Date(),
        updatedAt: docSnap.data().updatedAt?.toDate(),
        deadlines: docSnap.data().deadlines?.map((d: any) => ({
          ...d,
          dueDate: d.dueDate?.toDate() || new Date()
        })) || []
      })) as ManagedDocument[];
      
      setDocuments(docs);
      
      // Berechne anstehende Fristen
      const now = new Date();
      const in14Days = new Date(now.getTime() + 14 * 24 * 60 * 60 * 1000);
      const deadlines: {doc: ManagedDocument; deadline: DocumentDeadline}[] = [];
      
      docs.forEach(d => {
        d.deadlines?.forEach(deadline => {
          if (!deadline.completed && deadline.dueDate <= in14Days) {
            deadlines.push({ doc: d, deadline });
          }
        });
      });
      
      deadlines.sort((a, b) => a.deadline.dueDate.getTime() - b.deadline.dueDate.getTime());
      setUpcomingDeadlines(deadlines);
      
      // Migration: Alte Dokumente importieren
      await migrateOldDocuments(userId, docs.length);
      
    } catch (error) {
      console.error('Error loading documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const migrateOldDocuments = async (userId: string, existingCount: number) => {
    if (existingCount > 0) return;
    
    try {
      const oldQ = query(
        collection(db, 'users', userId, 'generated_documents'),
        orderBy('createdAt', 'desc')
      );
      const oldSnapshot = await getDocs(oldQ);
      
      if (oldSnapshot.empty) return;
      
      for (const oldDoc of oldSnapshot.docs) {
        const data = oldDoc.data();
        const newDoc: Partial<ManagedDocument> = {
          name: data.templateName || 'Dokument',
          content: data.content,
          category: data.sourceApp === 'musterbriefe' ? 'mustervorlagen' : 'eigene_vertraege',
          status: data.status === 'archiviert' ? 'archiviert' : 'aktiv',
          clientName: data.clientName,
          caseNumber: data.caseNumber,
          aiSummary: data.aiSummary,
          sourceApp: data.sourceApp || 'import',
          sourceDocId: oldDoc.id,
          tags: []
        };
        
        await addDoc(collection(db, 'users', userId, 'managed_documents'), {
          ...newDoc,
          createdAt: serverTimestamp(),
          updatedAt: serverTimestamp()
        });
      }
      
      await loadDocuments(userId);
    } catch (error) {
      console.error('Migration error:', error);
    }
  };

  // =========================================================================
  // UPLOAD & KI-ANALYSE
  // =========================================================================

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0 || !user) return;
    
    const file = acceptedFiles[0];
    setUploading(true);
    setUploadProgress('Datei wird gelesen...');
    
    try {
      const content = await readFileContent(file);
      setPendingFile({ name: file.name, content, type: file.type });
      
      setUploadProgress('KI analysiert Dokument...');
      const token = await user.getIdToken();
      
      const response = await fetch(`${BACKEND_URL}/documents/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          content: content.substring(0, 10000),
          fileName: file.name
        })
      });
      
      if (response.ok) {
        const analysis = await response.json();
        setAiAnalysis(analysis);
      } else {
        setAiAnalysis({
          documentType: 'Dokument',
          summary: 'Automatische Analyse nicht verfügbar'
        });
      }
      
      setShowUploadModal(true);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Fehler beim Hochladen');
    } finally {
      setUploading(false);
      setUploadProgress('');
    }
  }, [user]);
  
  const readFileContent = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target?.result as string || '');
      reader.onerror = reject;
      
      // Binäre Formate als Base64 lesen (für Backend-Verarbeitung)
      const binaryTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image/jpeg',
        'image/png',
        'image/webp',
        'image/tiff',
        'message/rfc822'
      ];
      
      if (binaryTypes.includes(file.type) || file.type.startsWith('image/')) {
        reader.readAsDataURL(file);
      } else {
        reader.readAsText(file);
      }
    });
  };
  
  const saveUploadedDocument = async (
    clientName: string, 
    caseNumber: string, 
    category: DocumentCategory,
    tags: string[]
  ) => {
    if (!user || !pendingFile) return;
    
    try {
      const docData: Partial<ManagedDocument> = {
        name: aiAnalysis?.documentType || pendingFile.name,
        content: pendingFile.content,
        category,
        status: 'aktiv',
        clientName: clientName || aiAnalysis?.suggestedClient,
        caseNumber: caseNumber || aiAnalysis?.suggestedCase,
        fileName: pendingFile.name,
        fileType: pendingFile.type,
        aiSummary: aiAnalysis?.summary,
        aiKeywords: aiAnalysis?.keywords,
        aiDocumentType: aiAnalysis?.documentType,
        sourceApp: 'upload',
        tags,
        deadlines: []
      };
      
      const docRef = await addDoc(collection(db, 'users', user.uid, 'managed_documents'), {
        ...docData,
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp()
      });
      
      setDocuments(prev => [{
        id: docRef.id,
        ...docData,
        createdAt: new Date(),
        updatedAt: new Date()
      } as ManagedDocument, ...prev]);
      
      setShowUploadModal(false);
      setPendingFile(null);
      setAiAnalysis(null);
    } catch (error) {
      console.error('Error saving document:', error);
      alert('Fehler beim Speichern');
    }
  };
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      // Dokumente
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/rtf': ['.rtf'],
      'application/rtf': ['.rtf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      // Excel
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      // Bilder (für OCR/Scans)
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/webp': ['.webp'],
      'image/tiff': ['.tiff', '.tif'],
      // E-Mail
      'message/rfc822': ['.eml'],
      // Weitere
      'application/xml': ['.xml'],
      'text/html': ['.html', '.htm']
    },
    maxFiles: 1,
    disabled: uploading
  });

  // =========================================================================
  // DOKUMENT-AKTIONEN
  // =========================================================================

  const updateDocument = async (docId: string, updates: Partial<ManagedDocument>) => {
    if (!user) return;
    try {
      await updateDoc(doc(db, 'users', user.uid, 'managed_documents', docId), {
        ...updates,
        updatedAt: serverTimestamp()
      });
      setDocuments(prev => prev.map(d => 
        d.id === docId ? { ...d, ...updates, updatedAt: new Date() } : d
      ));
      if (selectedDoc?.id === docId) {
        setSelectedDoc(prev => prev ? { ...prev, ...updates } : null);
      }
    } catch (error) {
      console.error('Error updating document:', error);
    }
  };

  const deleteDocument = async (docId: string) => {
    if (!user) return;
    try {
      await deleteDoc(doc(db, 'users', user.uid, 'managed_documents', docId));
      setDocuments(prev => prev.filter(d => d.id !== docId));
      setShowDeleteConfirm(null);
      if (selectedDoc?.id === docId) setSelectedDoc(null);
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  const moveToCategory = async (docId: string, newCategory: DocumentCategory) => {
    await updateDocument(docId, { category: newCategory });
    setShowMoveModal(null);
  };

  const addDeadline = async (docId: string, deadline: Omit<DocumentDeadline, 'id'>) => {
    const docToUpdate = documents.find(d => d.id === docId);
    if (!docToUpdate) return;
    
    const newDeadline: DocumentDeadline = {
      ...deadline,
      id: `dl_${Date.now()}`
    };
    
    const updatedDeadlines = [...(docToUpdate.deadlines || []), newDeadline];
    await updateDocument(docId, { deadlines: updatedDeadlines });
    setShowDeadlineModal(null);
  };

  const toggleDeadlineComplete = async (docId: string, deadlineId: string) => {
    const docToUpdate = documents.find(d => d.id === docId);
    if (!docToUpdate) return;
    
    const updatedDeadlines = docToUpdate.deadlines?.map(d => 
      d.id === deadlineId ? { ...d, completed: !d.completed } : d
    ) || [];
    
    await updateDocument(docId, { deadlines: updatedDeadlines });
  };

  // =========================================================================
  // SUCHE & FILTER
  // =========================================================================

  const performAISearch = async (searchQuery: string) => {
    if (!searchQuery.trim() || documents.length === 0) {
      setSearchResults([]);
      setUseAISearch(false);
      return;
    }

    setIsSearching(true);
    try {
      const docsForSearch = documents.map(d => ({
        id: d.id,
        templateName: d.name,
        content: d.content,
        clientName: d.clientName || '',
        caseNumber: d.caseNumber || '',
        createdAt: d.createdAt.toISOString(),
        status: d.status
      }));

      const results = await apiClient.searchDocuments(searchQuery, docsForSearch);
      setSearchResults(results);
      setUseAISearch(true);
    } catch (error) {
      console.error('AI search failed:', error);
      setUseAISearch(false);
    } finally {
      setIsSearching(false);
    }
  };

  useEffect(() => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      setUseAISearch(false);
      return;
    }
    const timeoutId = setTimeout(() => performAISearch(searchTerm), 800);
    return () => clearTimeout(timeoutId);
  }, [searchTerm, documents]);

  const filteredDocuments = documents.filter(d => {
    // Zeige nur Hauptdokumente (keine Anlagen), außer bei archiv-Filter
    const isMainDoc = !d.parentDocId;
    const matchesCategory = selectedCategory === 'all' || 
      d.category === selectedCategory || 
      (selectedCategory === 'archiv' && d.status === 'archiviert');
    const matchesStatus = filterStatus === 'all' || d.status === filterStatus;
    const matchesSearch = !searchTerm || 
      d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.clientName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.caseNumber?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.tags?.some(t => t.toLowerCase().includes(searchTerm.toLowerCase()));
    return isMainDoc && matchesCategory && matchesStatus && matchesSearch;
  });

  const displayDocuments = useAISearch && searchResults.length > 0
    ? documents
        .filter(d => !d.parentDocId && searchResults.some(r => r.document_id === d.id))
        .sort((a, b) => {
          const scoreA = searchResults.find(r => r.document_id === a.id)?.relevance_score || 0;
          const scoreB = searchResults.find(r => r.document_id === b.id)?.relevance_score || 0;
          return scoreB - scoreA;
        })
    : filteredDocuments;

  // =========================================================================
  // HELPER
  // =========================================================================

  const formatDate = (date: Date) => date.toLocaleDateString('de-DE', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  });

  const formatDateTime = (date: Date) => date.toLocaleDateString('de-DE', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  const getStatusStyle = (status: DocumentStatus) => 
    STATUS_OPTIONS.find(s => s.id === status)?.color || 'bg-gray-600 text-gray-200';

  const getCategoryInfo = (cat: DocumentCategory) => 
    MAIN_CATEGORIES.find(c => c.id === cat) || MAIN_CATEGORIES[0];

  // Hole Anlagen eines Vertrags
  const getAttachments = (parentId: string) => 
    documents.filter(d => d.parentDocId === parentId);

  // Hole nur Hauptdokumente (keine Anlagen)
  const getMainDocuments = () =>
    documents.filter(d => !d.parentDocId);

  const downloadDocument = (d: ManagedDocument) => {
    const blob = new Blob([d.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = window.document.createElement('a');
    a.href = url;
    a.download = `${d.name.replace(/\s+/g, '_')}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = (content: string) => {
    navigator.clipboard.writeText(content);
    alert('In Zwischenablage kopiert!');
  };

  // =========================================================================
  // RENDER
  // =========================================================================

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Dokumentenmanagement wird geladen...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-xl border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              {/* Mobile Menu Button */}
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <Link href="/dashboard" className="text-gray-400 hover:text-white">
                ← Dashboard
              </Link>
            </div>
            <h1 className="text-lg font-semibold text-white">📁 Dokumentenmanagement</h1>
          </div>
        </div>
      </nav>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <div className="flex pt-16">
        {/* Sidebar */}
        <aside className={`w-64 fixed left-0 top-16 bottom-0 bg-gray-900 border-r border-gray-800 overflow-y-auto z-40 transform transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
          <div className="p-4">
            {/* Mobile Close Button */}
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden absolute top-2 right-2 p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            {/* Upload Button */}
            <div
              {...getRootProps()}
              onClick={(e) => {
                if (!hasAccess) {
                  e.stopPropagation();
                  setShowUpgradeModal(true);
                  return;
                }
                getRootProps().onClick?.(e);
              }}
              className={`mb-6 p-4 border-2 border-dashed rounded-lg text-center cursor-pointer transition-all ${
                isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-gray-700 hover:border-blue-400'
              } ${uploading ? 'opacity-50' : ''}`}
            >
              <input {...getInputProps()} />
              {uploading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                  <span className="text-gray-400 text-sm">{uploadProgress}</span>
                </div>
              ) : (
                <>
                  <span className="text-2xl block mb-1">📤</span>
                  <span className="text-gray-300 text-sm">Dokument hochladen</span>
                </>
              )}
            </div>

            {/* Kategorien - Die zwei Welten */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Dokumentenverwaltung</h3>
              <button
                onClick={() => setSelectedCategory('all')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1 ${
                  selectedCategory === 'all' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                📂 Alle Dokumente
                <span className="float-right text-gray-500">{getMainDocuments().length}</span>
              </button>
              
              {/* Eigene Verträge - mit Anlagen-Zählung */}
              <button
                onClick={() => setSelectedCategory('eigene_vertraege')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1 ${
                  selectedCategory === 'eigene_vertraege' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>📄 Meine Verträge</span>
                  <span className="text-gray-500">{documents.filter(d => d.category === 'eigene_vertraege' && !d.parentDocId).length}</span>
                </div>
                <p className="text-xs text-gray-500 mt-0.5">Mit Anlagen • KI-Fristen</p>
              </button>
              
              {/* Mustervorlagen */}
              <button
                onClick={() => setSelectedCategory('mustervorlagen')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1 ${
                  selectedCategory === 'mustervorlagen' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>📋 Meine Vorlagen</span>
                  <span className="text-gray-500">{documents.filter(d => d.category === 'mustervorlagen' && !d.parentDocId).length}</span>
                </div>
                <p className="text-xs text-gray-500 mt-0.5">Selbst erstellte Vorlagen</p>
              </button>
              
              {/* Archiv */}
              <button
                onClick={() => setSelectedCategory('archiv')}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1 ${
                  selectedCategory === 'archiv' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>🗄️ Archiv</span>
                  <span className="text-gray-500">{documents.filter(d => d.category === 'archiv' || d.status === 'archiviert').length}</span>
                </div>
              </button>
            </div>

            {/* Anstehende Fristen */}
            {upcomingDeadlines.length > 0 && (
              <div className="mb-6">
                <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">⏰ Anstehende Fristen</h3>
                <div className="space-y-2">
                  {upcomingDeadlines.slice(0, 5).map(({ doc: d, deadline }) => {
                    const daysLeft = Math.ceil((deadline.dueDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
                    const isUrgent = daysLeft <= 3;
                    return (
                      <div 
                        key={deadline.id}
                        onClick={() => setSelectedDoc(d)}
                        className={`p-2 rounded-lg cursor-pointer text-xs ${
                          isUrgent ? 'bg-red-900/30 border border-red-700' : 'bg-gray-800'
                        }`}
                      >
                        <p className={`font-medium ${isUrgent ? 'text-red-400' : 'text-gray-300'}`}>
                          {deadline.title}
                        </p>
                        <p className="text-gray-500">
                          {formatDate(deadline.dueDate)} • {daysLeft > 0 ? `${daysLeft} Tage` : 'Heute!'}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Quick Stats */}
            <div className="border-t border-gray-800 pt-4">
              <h3 className="text-xs font-semibold text-gray-500 uppercase mb-2">Statistik</h3>
              <div className="grid grid-cols-2 gap-2 text-center">
                <div className="bg-gray-800 rounded p-2">
                  <p className="text-xl font-bold text-white">{documents.length}</p>
                  <p className="text-xs text-gray-500">Gesamt</p>
                </div>
                <div className="bg-gray-800 rounded p-2">
                  <p className="text-xl font-bold text-green-400">{documents.filter(d => d.status === 'aktiv').length}</p>
                  <p className="text-xs text-gray-500">Aktiv</p>
                </div>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 lg:ml-64 p-4 lg:p-6">
          {/* FREE User Banner */}
          {!hasAccess && (
            <div className="mb-6 p-4 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-500/50 rounded-xl">
              <div className="flex flex-col sm:flex-row items-center gap-4">
                <span className="text-4xl">🔒</span>
                <div className="flex-1 text-center sm:text-left">
                  <p className="text-white font-bold text-lg">Demo-Ansicht - Volle Funktionen mit Lawyer Pro</p>
                  <p className="text-gray-300 text-sm">Sie sehen Beispieldaten. Mit Lawyer Pro können Sie Ihre eigenen Dokumente verwalten.</p>
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

          {/* Search & Filter */}
          <div className="mb-6">
            <div className="flex flex-wrap gap-4 items-center">
              <div className="flex-1 min-w-[300px]">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="🤖 KI-Suche: Nach Inhalt, Mandant, Aktenzeichen suchen..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none"
                  />
                  <span className="absolute left-3 top-3.5 text-gray-400">
                    {isSearching ? '⏳' : '🔍'}
                  </span>
                  {useAISearch && searchResults.length > 0 && (
                    <span className="absolute right-3 top-3.5 text-xs text-green-500 font-medium">
                      ✨ {searchResults.length} KI-Treffer
                    </span>
                  )}
                </div>
              </div>
              <div className="flex gap-2">
                {STATUS_OPTIONS.map(s => (
                  <button
                    key={s.id}
                    onClick={() => setFilterStatus(filterStatus === s.id ? 'all' : s.id)}
                    className={`px-3 py-2 rounded-lg text-sm ${
                      filterStatus === s.id ? s.color : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                    }`}
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Documents Grid/List */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Document List */}
            <div className={selectedDoc ? 'lg:col-span-1' : 'lg:col-span-3'}>
              {displayDocuments.length === 0 ? (
                <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-12 text-center">
                  <span className="text-5xl block mb-4">📂</span>
                  <p className="text-lg text-gray-300">Keine Dokumente gefunden</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Laden Sie Dokumente hoch oder importieren Sie aus anderen Tools
                  </p>
                </div>
              ) : (
                <div className="bg-gray-800/50 rounded-xl border border-gray-700 divide-y divide-gray-700 max-h-[calc(100vh-200px)] overflow-y-auto">
                  {displayDocuments.map(d => {
                    const catInfo = getCategoryInfo(d.category);
                    const aiResult = searchResults.find(r => r.document_id === d.id);
                    const hasDeadlines = d.deadlines && d.deadlines.filter(dl => !dl.completed).length > 0;
                    const attachments = getAttachments(d.id);
                    
                    return (
                      <div key={d.id}>
                        {/* Hauptdokument */}
                        <div
                          onClick={() => setSelectedDoc(d)}
                          className={`p-4 cursor-pointer hover:bg-gray-700/50 transition-colors ${
                            selectedDoc?.id === d.id ? 'bg-blue-900/30 border-l-4 border-blue-500' : ''
                          }`}
                        >
                          <div className="flex items-start gap-3">
                            <span className="text-2xl">{catInfo.icon}</span>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <p className="font-medium text-white truncate">{d.name}</p>
                                {hasDeadlines && <span className="text-amber-500">⏰</span>}
                                {attachments.length > 0 && (
                                  <span className="text-xs bg-gray-700 text-gray-300 px-1.5 py-0.5 rounded">
                                    📎 {attachments.length} Anlage{attachments.length !== 1 ? 'n' : ''}
                                  </span>
                                )}
                              </div>
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className={`text-xs px-2 py-0.5 rounded ${getStatusStyle(d.status)}`}>
                                  {STATUS_OPTIONS.find(s => s.id === d.status)?.label}
                                </span>
                                <span className="text-xs text-gray-500">{catInfo.label}</span>
                                {aiResult && (
                                  <span className="text-xs px-2 py-0.5 bg-green-900/50 text-green-400 rounded">
                                    ✨ {Math.round(aiResult.relevance_score * 100)}%
                                  </span>
                                )}
                              </div>
                              {d.clientName && (
                                <p className="text-sm text-gray-400 mt-1">👤 {d.clientName}</p>
                              )}
                              {d.aiSummary && (
                                <p className="text-xs text-gray-500 mt-1 line-clamp-2">{d.aiSummary}</p>
                              )}
                              <p className="text-xs text-gray-600 mt-2">{formatDate(d.createdAt)}</p>
                            </div>
                          </div>
                        </div>
                        
                        {/* Anlagen (eingerückt) */}
                        {attachments.length > 0 && (
                          <div className="bg-gray-900/30 border-l-4 border-gray-600 ml-6">
                            {attachments.map(att => (
                              <div
                                key={att.id}
                                onClick={() => setSelectedDoc(att)}
                                className={`p-3 cursor-pointer hover:bg-gray-700/30 transition-colors flex items-center gap-2 ${
                                  selectedDoc?.id === att.id ? 'bg-blue-900/20' : ''
                                }`}
                              >
                                <span className="text-lg">📎</span>
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm text-gray-300 truncate">{att.name}</p>
                                  <p className="text-xs text-gray-500">{att.aiDocumentType || 'Anlage'}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Document Detail */}
            {selectedDoc && (
              <div className="lg:col-span-2">
                <div className="bg-gray-800/50 rounded-xl border border-gray-700 sticky top-24">
                  {/* Header */}
                  <div className="p-4 border-b border-gray-700 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{getCategoryInfo(selectedDoc.category).icon}</span>
                      <div>
                        <h2 className="font-semibold text-white">{selectedDoc.name}</h2>
                        <p className="text-sm text-gray-400">
                          {getCategoryInfo(selectedDoc.category).label}
                          {selectedDoc.clientName && ` • ${selectedDoc.clientName}`}
                        </p>
                      </div>
                    </div>
                    <button onClick={() => setSelectedDoc(null)} className="text-gray-400 hover:text-white text-xl">✕</button>
                  </div>

                  {/* KI-Zusammenfassung */}
                  {selectedDoc.aiSummary && (
                    <div className="p-4 bg-blue-900/20 border-b border-gray-700">
                      <p className="text-sm text-blue-300 font-medium mb-1">🤖 KI-Zusammenfassung</p>
                      <p className="text-gray-300 text-sm">{selectedDoc.aiSummary}</p>
                      {selectedDoc.aiKeywords && selectedDoc.aiKeywords.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {selectedDoc.aiKeywords.map((kw, i) => (
                            <span key={i} className="px-2 py-0.5 bg-gray-700 text-gray-300 rounded text-xs">{kw}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Status & Kategorie ändern */}
                  <div className="p-4 border-b border-gray-700 flex flex-wrap gap-4">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Status</p>
                      <div className="flex gap-1">
                        {STATUS_OPTIONS.map(s => (
                          <button
                            key={s.id}
                            onClick={() => updateDocument(selectedDoc.id, { status: s.id })}
                            className={`px-2 py-1 rounded text-xs ${
                              selectedDoc.status === s.id ? s.color : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                            }`}
                          >
                            {s.label}
                          </button>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Kategorie</p>
                      <button
                        onClick={() => setShowMoveModal(selectedDoc)}
                        className="px-3 py-1 bg-gray-700 text-gray-300 rounded text-xs hover:bg-gray-600"
                      >
                        📁 Verschieben
                      </button>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Fristen</p>
                      <button
                        onClick={() => setShowDeadlineModal(selectedDoc)}
                        className="px-3 py-1 bg-gray-700 text-gray-300 rounded text-xs hover:bg-gray-600"
                      >
                        ⏰ Frist hinzufügen
                      </button>
                    </div>
                  </div>

                  {/* Fristen des Dokuments */}
                  {selectedDoc.deadlines && selectedDoc.deadlines.length > 0 && (
                    <div className="p-4 border-b border-gray-700">
                      <p className="text-xs text-gray-500 mb-2">📅 Fristen & Termine</p>
                      <div className="space-y-2">
                        {selectedDoc.deadlines.map(dl => (
                          <div 
                            key={dl.id} 
                            className={`flex items-center justify-between p-2 rounded ${
                              dl.completed ? 'bg-gray-700/50' : 'bg-amber-900/20'
                            }`}
                          >
                            <div className="flex items-center gap-2">
                              <input
                                type="checkbox"
                                checked={dl.completed}
                                onChange={() => toggleDeadlineComplete(selectedDoc.id, dl.id)}
                                className="w-4 h-4"
                              />
                              <span className={`text-sm ${dl.completed ? 'text-gray-500 line-through' : 'text-gray-300'}`}>
                                {dl.title}
                              </span>
                            </div>
                            <span className="text-xs text-gray-500">{formatDate(dl.dueDate)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Anlagen des Dokuments */}
                  {!selectedDoc.parentDocId && (
                    <div className="p-4 border-b border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <p className="text-xs text-gray-500">📎 Anlagen</p>
                        <button
                          onClick={() => setShowAddAttachmentModal(selectedDoc)}
                          className="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded hover:bg-gray-600"
                        >
                          + Anlage hinzufügen
                        </button>
                      </div>
                      {getAttachments(selectedDoc.id).length > 0 ? (
                        <div className="space-y-2">
                          {getAttachments(selectedDoc.id).map(att => (
                            <div 
                              key={att.id}
                              onClick={() => setSelectedDoc(att)}
                              className="flex items-center justify-between p-2 bg-gray-700/50 rounded cursor-pointer hover:bg-gray-600/50"
                            >
                              <div className="flex items-center gap-2">
                                <span>📎</span>
                                <span className="text-sm text-gray-300">{att.name}</span>
                              </div>
                              <span className="text-xs text-gray-500">{att.aiDocumentType || 'Anlage'}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-xs text-gray-600 italic">Keine Anlagen vorhanden</p>
                      )}
                    </div>
                  )}

                  {/* Angehängt an (wenn dies eine Anlage ist) */}
                  {selectedDoc.parentDocId && (
                    <div className="p-4 border-b border-gray-700 bg-gray-900/30">
                      <p className="text-xs text-gray-500 mb-2">📄 Gehört zu Vertrag:</p>
                      {documents.find(d => d.id === selectedDoc.parentDocId) && (
                        <button
                          onClick={() => setSelectedDoc(documents.find(d => d.id === selectedDoc.parentDocId)!)}
                          className="text-sm text-blue-400 hover:text-blue-300"
                        >
                          ← {documents.find(d => d.id === selectedDoc.parentDocId)?.name}
                        </button>
                      )}
                    </div>
                  )}

                  {/* Inhalt */}
                  <div className="p-4">
                    <pre className="whitespace-pre-wrap font-mono text-sm text-gray-300 bg-gray-900/50 p-4 rounded-lg max-h-[300px] overflow-y-auto">
                      {selectedDoc.content.substring(0, 5000)}
                      {selectedDoc.content.length > 5000 && '\n\n[... weiterer Inhalt ...]'}
                    </pre>
                  </div>

                  {/* Meta */}
                  <div className="p-4 border-t border-gray-700 bg-gray-900/50 text-xs text-gray-500">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p>Erstellt: {formatDateTime(selectedDoc.createdAt)}</p>
                        {selectedDoc.updatedAt && <p>Aktualisiert: {formatDateTime(selectedDoc.updatedAt)}</p>}
                      </div>
                      <div>
                        {selectedDoc.caseNumber && <p>Aktenzeichen: {selectedDoc.caseNumber}</p>}
                        {selectedDoc.sourceApp && <p>Quelle: {selectedDoc.sourceApp}</p>}
                      </div>
                    </div>
                  </div>

                  {/* Aktionen */}
                  <div className="p-4 border-t border-gray-700 flex flex-wrap gap-2">
                    <button onClick={() => copyToClipboard(selectedDoc.content)} className="px-3 py-2 bg-gray-700 text-gray-300 rounded text-sm hover:bg-gray-600">
                      📋 Kopieren
                    </button>
                    <button onClick={() => downloadDocument(selectedDoc)} className="px-3 py-2 bg-gray-700 text-gray-300 rounded text-sm hover:bg-gray-600">
                      ⬇️ Download
                    </button>
                    <button onClick={() => setShowDeleteConfirm(selectedDoc.id)} className="px-3 py-2 bg-red-900/50 text-red-400 rounded text-sm hover:bg-red-900">
                      🗑️ Löschen
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Modals */}
      
      {/* Delete Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-xl max-w-md w-full p-6 border border-gray-700">
            <div className="text-center">
              <span className="text-4xl block mb-4">🗑️</span>
              <h3 className="text-xl font-bold text-white mb-2">Dokument löschen?</h3>
              <p className="text-gray-400 mb-6">Diese Aktion kann nicht rückgängig gemacht werden.</p>
              <div className="flex gap-3">
                <button onClick={() => setShowDeleteConfirm(null)} className="flex-1 py-3 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
                  Abbrechen
                </button>
                <button onClick={() => deleteDocument(showDeleteConfirm)} className="flex-1 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700">
                  Löschen
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Move Modal */}
      {showMoveModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-xl max-w-md w-full p-6 border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-4">📁 Dokument verschieben</h3>
            <p className="text-gray-400 mb-4">Wählen Sie die neue Kategorie:</p>
            <div className="space-y-2 max-h-[300px] overflow-y-auto">
              {MAIN_CATEGORIES.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => moveToCategory(showMoveModal.id, cat.id)}
                  className={`w-full text-left p-3 rounded-lg ${
                    showMoveModal.category === cat.id 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  <span className="mr-2">{cat.icon}</span>
                  {cat.label}
                  <span className="block text-xs text-gray-500 mt-0.5">{cat.description}</span>
                </button>
              ))}
            </div>
            <button onClick={() => setShowMoveModal(null)} className="w-full mt-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
              Abbrechen
            </button>
          </div>
        </div>
      )}

      {/* Deadline Modal */}
      {showDeadlineModal && (
        <DeadlineModal
          onSave={(deadline) => addDeadline(showDeadlineModal.id, deadline)}
          onClose={() => setShowDeadlineModal(null)}
        />
      )}

      {/* Upload Modal */}
      {showUploadModal && pendingFile && (
        <UploadModal
          fileName={pendingFile.name}
          aiAnalysis={aiAnalysis}
          onSave={saveUploadedDocument}
          onCancel={() => {
            setShowUploadModal(false);
            setPendingFile(null);
            setAiAnalysis(null);
          }}
        />
      )}

      {/* Anlage Hinzufügen Modal */}
      {showAddAttachmentModal && (
        <AddAttachmentModal
          parentDoc={showAddAttachmentModal}
          onSave={async (file, name) => {
            if (!user) return;
            try {
              const content = await readFileContent(file);
              const docData: Partial<ManagedDocument> = {
                name: name || file.name,
                content,
                category: showAddAttachmentModal.category,
                status: 'aktiv',
                fileName: file.name,
                fileType: file.type,
                sourceApp: 'upload',
                parentDocId: showAddAttachmentModal.id, // Verknüpfung zum Hauptvertrag
                tags: ['Anlage'],
              };
              
              const docRef = await addDoc(collection(db, 'users', user.uid, 'managed_documents'), {
                ...docData,
                createdAt: serverTimestamp(),
                updatedAt: serverTimestamp()
              });
              
              setDocuments(prev => [{
                id: docRef.id,
                ...docData,
                createdAt: new Date(),
                updatedAt: new Date()
              } as ManagedDocument, ...prev]);
              
              setShowAddAttachmentModal(null);
              alert('✅ Anlage hinzugefügt!');
            } catch (error) {
              console.error('Error adding attachment:', error);
              alert('Fehler beim Hinzufügen der Anlage');
            }
          }}
          onCancel={() => setShowAddAttachmentModal(null)}
        />
      )}

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="lawyer"
        feature="Dokumentenmanagement"
      />
    </div>
  );
}

// =========================================================================
// SUB-KOMPONENTEN
// =========================================================================

function DeadlineModal({ onSave, onClose }: { 
  onSave: (deadline: Omit<DocumentDeadline, 'id'>) => void; 
  onClose: () => void;
}) {
  const [title, setTitle] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [type, setType] = useState<'frist' | 'wiedervorlage' | 'termin'>('frist');
  const [reminderDays, setReminderDays] = useState(3);

  const handleSave = () => {
    if (!title || !dueDate) return;
    onSave({
      title,
      dueDate: new Date(dueDate),
      type,
      reminderDays,
      completed: false
    });
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-md w-full p-6 border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-4">⏰ Frist hinzufügen</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Bezeichnung</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="z.B. Widerrufsfrist, Klagefrist"
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
            />
          </div>
          
          <div>
            <label className="block text-sm text-gray-400 mb-1">Datum</label>
            <input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
            />
          </div>
          
          <div>
            <label className="block text-sm text-gray-400 mb-1">Typ</label>
            <div className="flex gap-2">
              {[
                { id: 'frist', label: '⚠️ Frist' },
                { id: 'wiedervorlage', label: '📋 Wiedervorlage' },
                { id: 'termin', label: '📅 Termin' }
              ].map(t => (
                <button
                  key={t.id}
                  onClick={() => setType(t.id as any)}
                  className={`flex-1 py-2 rounded-lg text-sm ${
                    type === t.id ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm text-gray-400 mb-1">Erinnerung (Tage vorher)</label>
            <input
              type="number"
              value={reminderDays}
              onChange={(e) => setReminderDays(parseInt(e.target.value))}
              min={0}
              max={30}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
            />
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button onClick={onClose} className="flex-1 py-3 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
            Abbrechen
          </button>
          <button onClick={handleSave} disabled={!title || !dueDate} className="flex-1 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
            Speichern
          </button>
        </div>
      </div>
    </div>
  );
}

function UploadModal({ fileName, aiAnalysis, onSave, onCancel }: {
  fileName: string;
  aiAnalysis: any;
  onSave: (clientName: string, caseNumber: string, category: DocumentCategory, tags: string[]) => void;
  onCancel: () => void;
}) {
  const [clientName, setClientName] = useState(aiAnalysis?.suggestedClient || '');
  const [caseNumber, setCaseNumber] = useState(aiAnalysis?.suggestedCase || '');
  const [category, setCategory] = useState<DocumentCategory>('eigene_vertraege');
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState<string[]>([]);

  const addTag = () => {
    if (tagInput.trim() && !tags.includes(tagInput.trim())) {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-lg w-full p-6 border border-gray-700 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center gap-3 mb-6">
          <span className="text-3xl">🤖</span>
          <div>
            <h3 className="text-xl font-bold text-white">KI-Analyse abgeschlossen</h3>
            <p className="text-gray-400 text-sm">{fileName}</p>
          </div>
        </div>

        {aiAnalysis?.summary && (
          <div className="bg-blue-900/30 border border-blue-700/50 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-300 font-medium mb-1">📝 KI-Zusammenfassung</p>
            <p className="text-gray-300 text-sm">{aiAnalysis.summary}</p>
            {aiAnalysis?.detectedDeadlines && aiAnalysis.detectedDeadlines.length > 0 && (
              <div className="mt-3 pt-3 border-t border-blue-700/50">
                <p className="text-sm text-amber-400 font-medium mb-1">⏰ Erkannte Fristen:</p>
                {aiAnalysis.detectedDeadlines.map((d: any, i: number) => (
                  <p key={i} className="text-gray-300 text-sm">• {d.title}: {d.date}</p>
                ))}
              </div>
            )}
          </div>
        )}

        {aiAnalysis?.documentType && (
          <div className="mb-4">
            <p className="text-sm text-gray-400 mb-1">Erkannter Dokumenttyp</p>
            <p className="text-white font-medium">{aiAnalysis.documentType}</p>
          </div>
        )}

        <div className="space-y-4">
          {/* Kategorie - vereinfacht auf die zwei Welten */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Speichern unter</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setCategory('eigene_vertraege')}
                className={`p-3 rounded-lg border text-left ${
                  category === 'eigene_vertraege' 
                    ? 'border-blue-500 bg-blue-900/30' 
                    : 'border-gray-600 hover:border-gray-500'
                }`}
              >
                <span className="text-xl block mb-1">📄</span>
                <p className="text-white font-medium text-sm">Meine Verträge</p>
                <p className="text-gray-500 text-xs">Echte abgeschlossene Verträge</p>
              </button>
              <button
                onClick={() => setCategory('mustervorlagen')}
                className={`p-3 rounded-lg border text-left ${
                  category === 'mustervorlagen' 
                    ? 'border-blue-500 bg-blue-900/30' 
                    : 'border-gray-600 hover:border-gray-500'
                }`}
              >
                <span className="text-xl block mb-1">📋</span>
                <p className="text-white font-medium text-sm">Meine Vorlagen</p>
                <p className="text-gray-500 text-xs">Selbst erstellte Muster</p>
              </button>
            </div>
          </div>

          {/* Mandant */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">
              Mandant/Vertragspartner {aiAnalysis?.suggestedClient && <span className="text-green-400">(KI-Vorschlag)</span>}
            </label>
            <input
              type="text"
              value={clientName}
              onChange={(e) => setClientName(e.target.value)}
              placeholder="z.B. Müller GmbH"
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
            />
          </div>

          {/* Aktenzeichen */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Aktenzeichen/Referenz</label>
            <input
              type="text"
              value={caseNumber}
              onChange={(e) => setCaseNumber(e.target.value)}
              placeholder="z.B. 2026/001"
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm text-gray-400 mb-1">Tags</label>
            <div className="flex gap-2">
              <input
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && addTag()}
                placeholder="Tag hinzufügen"
                className="flex-1 px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
              />
              <button onClick={addTag} className="px-4 py-2 bg-gray-700 text-white rounded-lg">+</button>
            </div>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {tags.map((t, i) => (
                  <span key={i} className="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs flex items-center gap-1">
                    {t}
                    <button onClick={() => setTags(tags.filter((_, j) => j !== i))} className="text-gray-500 hover:text-white">×</button>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button onClick={onCancel} className="flex-1 py-3 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
            Abbrechen
          </button>
          <button onClick={() => onSave(clientName, caseNumber, category, tags)} className="flex-1 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            💾 Speichern
          </button>
        </div>
      </div>
    </div>
  );
}

function AddAttachmentModal({ parentDoc, onSave, onCancel }: {
  parentDoc: ManagedDocument;
  onSave: (file: File, name: string) => void;
  onCancel: () => void;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [name, setName] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setFile(f);
      if (!name) setName(f.name.replace(/\.[^/.]+$/, ''));
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-xl max-w-md w-full p-6 border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-2">📎 Anlage hinzufügen</h3>
        <p className="text-gray-400 text-sm mb-4">
          Zu: <span className="text-white">{parentDoc.name}</span>
        </p>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Datei auswählen</label>
            <input
              type="file"
              accept=".pdf,.doc,.docx,.txt,.rtf,.xls,.xlsx,.csv,.jpg,.jpeg,.png,.webp,.tiff,.tif,.eml,.xml,.html,.htm"
              onChange={handleFileChange}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-gray-700 file:text-white"
            />
            <p className="text-xs text-gray-500 mt-1">PDF, Word, Excel, Bilder, CSV & mehr</p>
          </div>
          
          <div>
            <label className="block text-sm text-gray-400 mb-1">Bezeichnung</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="z.B. AGB, Anlage 1, Vollmacht"
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white"
            />
          </div>
        </div>
        
        <div className="flex gap-3 mt-6">
          <button onClick={onCancel} className="flex-1 py-3 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600">
            Abbrechen
          </button>
          <button 
            onClick={() => file && onSave(file, name)}
            disabled={!file}
            className="flex-1 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            📎 Hinzufügen
          </button>
        </div>
      </div>
    </div>
  );
}

// Type export für andere Module
export type { ManagedDocument, DocumentCategory, DocumentDeadline, DocumentStatus };
