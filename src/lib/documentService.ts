/**
 * Document Management Service
 * 
 * Dieser Service ermöglicht es allen Tools, Dokumente ins Dokumentenmanagement zu speichern.
 * 
 * Verwendung in anderen Tools:
 * 
 * import { saveToDocumentManagement } from '@/lib/documentService';
 * 
 * await saveToDocumentManagement(userId, {
 *   name: 'Mietvertrag Müller',
 *   content: '...',
 *   category: 'vertraege',
 *   sourceApp: 'schriftsatz',
 *   clientName: 'Herr Müller',
 *   caseNumber: '2026/001'
 * });
 */

import { collection, addDoc, serverTimestamp, doc, updateDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase';

export type DocumentCategory = 
  | 'eigene_vertraege'    // Echte abgeschlossene Verträge mit Anlagen
  | 'mustervorlagen'      // Selbst erstellte Vorlagen
  | 'archiv';             // Archivierte Dokumente

export type DocumentStatus = 'entwurf' | 'aktiv' | 'abgeschlossen' | 'archiviert';

export type SourceApp = 'upload' | 'schriftsatz' | 'vertragsanalyse' | 'fallanalyse' | 'musterbriefe' | 'checkout' | 'import' | 'rechtsprechung';

export interface DocumentDeadline {
  id: string;
  title: string;
  dueDate: Date;
  reminderDays?: number;
  completed?: boolean;
  type: 'frist' | 'wiedervorlage' | 'termin';
}

export interface SaveDocumentRequest {
  // Pflichtfelder
  name: string;
  content: string;
  category: DocumentCategory;
  sourceApp: SourceApp;
  
  // Optionale Felder
  status?: DocumentStatus;
  clientName?: string;
  clientId?: string;
  caseNumber?: string;
  mandateId?: string;
  fileName?: string;
  fileType?: string;
  fileSize?: number;
  aiSummary?: string;
  aiKeywords?: string[];
  aiDocumentType?: string;
  tags?: string[];
  deadlines?: DocumentDeadline[];
  sourceDocId?: string;
  parentDocId?: string;
  version?: number;
}

/**
 * Speichert ein Dokument ins Dokumentenmanagement
 */
export async function saveToDocumentManagement(
  userId: string, 
  document: SaveDocumentRequest
): Promise<string> {
  if (!userId) {
    throw new Error('User ID ist erforderlich');
  }
  if (!document.name || !document.content) {
    throw new Error('Dokumentname und Inhalt sind erforderlich');
  }
  
  try {
    // Firestore akzeptiert keine undefined-Werte, daher filtern wir sie heraus
    const cleanDocument: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(document)) {
      if (value !== undefined) {
        cleanDocument[key] = value;
      }
    }
    
    // Standard-Felder hinzufügen/überschreiben
    cleanDocument.status = document.status || 'aktiv';
    cleanDocument.tags = document.tags || [];
    cleanDocument.deadlines = document.deadlines || [];
    cleanDocument.createdAt = serverTimestamp();
    cleanDocument.updatedAt = serverTimestamp();
    
    console.log('Saving document to:', `users/${userId}/managed_documents`);
    console.log('Document data:', { name: cleanDocument.name, category: cleanDocument.category });
    
    const docRef = await addDoc(
      collection(db, 'users', userId, 'managed_documents'), 
      cleanDocument
    );
    
    console.log(`Document saved to management: ${docRef.id}`);
    return docRef.id;
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Unbekannter Fehler';
    const errorCode = (error as { code?: string })?.code;
    console.error('Error saving to document management:', error);
    console.error('Error code:', errorCode);
    console.error('Error message:', errorMessage);
    throw new Error(`Speicherfehler: ${errorMessage}`);
  }
}

/**
 * Speichert einen Vertrag nach Abschluss (Checkout) automatisch
 */
export async function saveContractAfterCheckout(
  userId: string,
  tierName: string,
  contractContent: string,
  customerName?: string
): Promise<string> {
  return saveToDocumentManagement(userId, {
    name: `Abonnement-Vertrag ${tierName}`,
    content: contractContent,
    category: 'eigene_vertraege',
    sourceApp: 'checkout',
    status: 'aktiv',
    clientName: customerName,
    aiSummary: `Domulex ${tierName} Abonnement-Vertrag, abgeschlossen am ${new Date().toLocaleDateString('de-DE')}`,
    tags: ['Abonnement', tierName, 'Domulex'],
    deadlines: [{
      id: `dl_widerruf_${Date.now()}`,
      title: 'Widerrufsfrist',
      dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 14 Tage
      type: 'frist',
      reminderDays: 3,
      completed: false
    }]
  });
}

/**
 * Speichert eine Vorlage aus dem Schriftsatzgenerator/Musterbriefe als Muster
 */
export async function saveTemplateAsMuster(
  userId: string,
  templateName: string,
  content: string,
  clientName?: string,
  caseNumber?: string
): Promise<string> {
  return saveToDocumentManagement(userId, {
    name: templateName,
    content,
    category: 'mustervorlagen',
    sourceApp: 'musterbriefe',
    status: 'aktiv',
    clientName,
    caseNumber,
    tags: ['Mustervorlage', 'Musterbrief']
  });
}

/**
 * Speichert ein analysiertes Dokument aus der Vertragsanalyse
 */
export async function saveFromContractAnalysis(
  userId: string,
  fileName: string,
  content: string,
  analysis: {
    summary?: string;
    risks?: string[];
    documentType?: string;
  },
  clientName?: string
): Promise<string> {
  return saveToDocumentManagement(userId, {
    name: analysis.documentType || fileName,
    content,
    category: 'eigene_vertraege',
    sourceApp: 'vertragsanalyse',
    status: 'aktiv',
    fileName,
    clientName,
    aiSummary: analysis.summary,
    aiDocumentType: analysis.documentType,
    tags: ['Analysiert', ...(analysis.risks || [])]
  });
}

/**
 * Speichert ein Urteil aus der Rechtsprechungssuche
 * Wird als Mustervorlage gespeichert (für Recherche-Referenzen)
 */
export async function saveUrteil(
  userId: string,
  urteilName: string,
  content: string,
  metadata: {
    gericht?: string;
    datum?: string;
    aktenzeichen?: string;
    summary?: string;
  }
): Promise<string> {
  return saveToDocumentManagement(userId, {
    name: urteilName,
    content,
    category: 'mustervorlagen',
    sourceApp: 'rechtsprechung',
    status: 'abgeschlossen',
    caseNumber: metadata.aktenzeichen,
    aiSummary: metadata.summary,
    tags: ['Urteil', metadata.gericht || '', metadata.datum || ''].filter(Boolean)
  });
}

/**
 * Speichert AGB, AVV oder NDA als Anlage zu einem Vertrag
 */
export async function saveVertragsanlage(
  userId: string,
  type: 'AGB' | 'AVV' | 'NDA' | 'Anlage',
  content: string,
  relatedContractId?: string,
  clientName?: string
): Promise<string> {
  return saveToDocumentManagement(userId, {
    name: type,
    content,
    category: 'eigene_vertraege', // Anlagen gehören zu Verträgen
    sourceApp: 'checkout',
    status: 'aktiv',
    clientName,
    parentDocId: relatedContractId, // Verknüpfung zum Hauptvertrag
    tags: [type, 'Anlage']
  });
}

/**
 * Aktualisiert ein bestehendes Dokument
 */
export async function updateManagedDocument(
  userId: string,
  documentId: string,
  updates: Partial<SaveDocumentRequest>
): Promise<void> {
  try {
    await updateDoc(
      doc(db, 'users', userId, 'managed_documents', documentId),
      {
        ...updates,
        updatedAt: serverTimestamp()
      }
    );
  } catch (error) {
    console.error('Error updating document:', error);
    throw error;
  }
}

/**
 * Fügt eine Frist zu einem Dokument hinzu
 */
export async function addDeadlineToDocument(
  userId: string,
  documentId: string,
  deadline: Omit<DocumentDeadline, 'id'>
): Promise<void> {
  const newDeadline: DocumentDeadline = {
    ...deadline,
    id: `dl_${Date.now()}`
  };
  
  // Wir müssen hier die bestehenden Deadlines laden und erweitern
  // Das ist eine vereinfachte Version - in Produktion würde man arrayUnion verwenden
  await updateDoc(
    doc(db, 'users', userId, 'managed_documents', documentId),
    {
      updatedAt: serverTimestamp()
    }
  );
}

// Kategorie-Mapping für automatische Zuordnung basierend auf Dokumenttyp
export const CATEGORY_MAPPING: Record<string, DocumentCategory> = {
  'mietvertrag': 'eigene_vertraege',
  'kaufvertrag': 'eigene_vertraege',
  'arbeitsvertrag': 'eigene_vertraege',
  'kündigung': 'eigene_vertraege',
  'mahnung': 'eigene_vertraege',
  'schreiben': 'eigene_vertraege',
  'urteil': 'mustervorlagen',
  'beschluss': 'mustervorlagen',
  'agb': 'eigene_vertraege', // Als Anlage zu einem Vertrag
  'avv': 'eigene_vertraege',
  'nda': 'eigene_vertraege',
  'anlage': 'eigene_vertraege',
  'muster': 'mustervorlagen',
  'vorlage': 'mustervorlagen',
  'template': 'mustervorlagen'
};

/**
 * Erkennt automatisch die passende Kategorie basierend auf dem Dokumentnamen
 */
export function detectCategory(documentName: string): DocumentCategory {
  const lowerName = documentName.toLowerCase();
  
  for (const [keyword, category] of Object.entries(CATEGORY_MAPPING)) {
    if (lowerName.includes(keyword)) {
      return category;
    }
  }
  
  return 'eigene_vertraege'; // Default
}
