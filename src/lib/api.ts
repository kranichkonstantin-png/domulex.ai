// API Client for DOMULEX Backend
import { getSessionHeaders, handleSessionConflict } from './session';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface QueryRequest {
  query: string;
  target_jurisdiction: 'DE' | 'ES' | 'US';
  user_role: string; // Flexible Rollen: INVESTOR, LANDLORD, TENANT, OWNER, MANAGER, MIETER, EIGENTUEMER, VERMIETER, ANWALT, VERWALTER
  user_language: 'de' | 'es' | 'en';
  sub_jurisdiction?: string;
  user_id?: string;  // Firebase UID for quota tracking
  user_tier?: string; // User's subscription tier
  source_filter?: string[];  // Filter by doc_type (e.g., ['GESETZ', 'URTEIL', 'LITERATUR'])
  gerichtsebene_filter?: string[];  // Filter by court level (e.g., ['BGH', 'OLG', 'LG', 'AG'])
  use_public_sources?: boolean;  // 🔑 Öffentliche Quellen nutzen (BGB, BGH, Literatur)
  uploaded_documents?: { document_id: string; text: string }[];  // User-uploaded documents for context
}

export interface LegalDocument {
  id: string;
  jurisdiction: string;
  title: string;
  content_original: string;
  source_url: string;
  publication_date: string;
  document_type: string;
  language: string;
}

export interface QueryResponse {
  answer: string;
  sources: LegalDocument[];
  jurisdiction_warning?: string;
  generated_at: string;
}

export interface ConflictRequest {
  party_a_statement: string;
  party_b_statement: string;
  jurisdiction: 'DE' | 'ES' | 'US';
  party_a_label?: string;
  party_b_label?: string;
  user_language?: string;
}

export interface ConflictAnalysis {
  party_label: string;
  legal_arguments: string;
  supporting_sources: LegalDocument[];
  strength_assessment: string;
}

export interface ConflictResponse {
  dispute_summary: string;
  party_a_analysis: ConflictAnalysis;
  party_b_analysis: ConflictAnalysis;
  neutral_assessment: string;
  success_probability_a: number;
  success_probability_b: number;
  settlement_likelihood: number;
  recommendation: string;
  jurisdiction: string;
  generated_at: string;
}

export interface ContractAnalysis {
  contract_name: string;
  analyzed_at: string;
  jurisdiction: string;
  user_role: string;
  clauses: ClauseAnalysis[];
  overall_risk: 'GREEN' | 'YELLOW' | 'RED';
  summary: string;
  total_clauses_analyzed: number;
  red_flags: number;
  yellow_flags: number;
  green_flags: number;
}

export interface ClauseAnalysis {
  clause_type: string;
  clause_text: string;
  risk_level: 'GREEN' | 'YELLOW' | 'RED';
  legal_standard: string;
  comparison: string;
  recommendation?: string;
  source_title?: string;
  source_url?: string;
}

// Custom error class for quota exceeded
export class QuotaExceededError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'QuotaExceededError';
  }
}

// Custom error class for session conflict
export class SessionConflictError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'SessionConflictError';
  }
}

/**
 * Handle API response and check for session conflicts
 */
async function handleResponse<T>(response: Response): Promise<T> {
  // Check for session conflict (409 with SESSION_EXPIRED_OTHER_DEVICE)
  if (response.status === 409) {
    const errorData = await response.json().catch(() => ({}));
    if (errorData.detail === 'SESSION_EXPIRED_OTHER_DEVICE') {
      // Handle session conflict - logout user
      await handleSessionConflict();
      throw new SessionConflictError('Sie wurden auf einem anderen Gerät angemeldet.');
    }
  }
  
  return response.json();
}

class APIClient {
  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        ...getSessionHeaders(),
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      // Handle session conflict
      if (response.status === 409) {
        const errorData = await response.json().catch(() => ({}));
        if (errorData.detail === 'SESSION_EXPIRED_OTHER_DEVICE') {
          await handleSessionConflict();
          throw new SessionConflictError('Sie wurden auf einem anderen Gerät angemeldet.');
        }
      }
      // Handle quota exceeded (429)
      if (response.status === 429) {
        const errorData = await response.json().catch(() => ({}));
        throw new QuotaExceededError(errorData.detail || 'Monatliches Anfrage-Limit erreicht');
      }
      throw new Error('Ihre Anfrage konnte nicht verarbeitet werden. Bitte stellen Sie nur themenbezogene Immobilienrechts-Fragen.');
    }

    return response.json();
  }

  async analyzeContract(
    file: File,
    jurisdiction: string,
    userRole: string
  ): Promise<ContractAnalysis> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('jurisdiction', jurisdiction);
    formData.append('user_role', userRole);

    const response = await fetch(`${API_BASE_URL}/analyze_contract`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Contract analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  async resolveConflict(request: ConflictRequest): Promise<ConflictResponse> {
    const response = await fetch(`${API_BASE_URL}/resolve_conflict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Conflict resolution failed: ${response.statusText}`);
    }

    return response.json();
  }

  async checkHealth(): Promise<{ status: string; qdrant: string; gemini: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  }

  async getStats(): Promise<{ total_documents: number; collection_name: string }> {
    const response = await fetch(`${API_BASE_URL}/stats`);
    return response.json();
  }

  async searchDocuments(query: string, documents: any[]): Promise<DocumentSearchResult[]> {
    const formData = new FormData();
    formData.append('query', query);
    formData.append('documents', JSON.stringify(documents));

    const response = await fetch(`${API_BASE_URL}/documents/search/rank`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Document search failed: ${response.statusText}`);
    }

    return response.json();
  }
}

export interface DocumentSearchResult {
  document_id: string;
  template_name: string;
  client_name?: string;
  case_number?: string;
  created_at: string;
  relevance_score: number;
  summary: string;
  matching_excerpt?: string;
}

export const apiClient = new APIClient();
