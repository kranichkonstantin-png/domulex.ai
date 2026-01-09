/**
 * Zentrale Tier-Verwaltung für Domulex.ai
 * 
 * Tier-Hierarchie:
 * - free (0): Nur Chat mit 3 Anfragen
 * - basis / mieter_plus (1): + Nebenkostenprüfung, Musterbriefe, Nebenkostenrechner
 * - professional (2): + Objektverwaltung, Nebenkostenabrechnung, Renditerechner, Vertragsanalyse, Steuer, Baurecht
 * - lawyer (3): + CRM, Fristen, Dokumentenmanagement, Fallanalyse, Rechtsprechung, Schriftsätze
 */

export type TierLevel = 'free' | 'basis' | 'mieter_plus' | 'professional' | 'lawyer';

// Tier-Level-Nummern für Vergleiche
const TIER_LEVELS: Record<string, number> = {
  'free': 0,
  'basis': 1,
  'mieter_plus': 1,  // Alias für basis
  'professional': 2,
  'lawyer': 3,
};

/**
 * Normalisiert verschiedene Tier-Bezeichnungen
 */
export function normalizeTier(tier?: string | null): TierLevel {
  if (!tier) return 'free';
  
  const lowerTier = tier.toLowerCase();
  
  // Entferne "free_" Präfix (z.B. free_professional -> professional)
  if (lowerTier.startsWith('free_')) {
    return 'free';  // free_xxx bedeutet: registriert aber nicht bezahlt
  }
  
  if (lowerTier === 'mieter_plus') return 'basis';
  if (lowerTier === 'basis') return 'basis';
  if (lowerTier === 'professional') return 'professional';
  if (lowerTier === 'lawyer') return 'lawyer';
  
  return 'free';
}

/**
 * Prüft, ob ein Benutzer mindestens den erforderlichen Tier hat
 */
export function hasTierAccess(userTier: string | undefined, requiredTier: TierLevel): boolean {
  const normalizedUserTier = normalizeTier(userTier);
  const userLevel = TIER_LEVELS[normalizedUserTier] ?? 0;
  const requiredLevel = TIER_LEVELS[requiredTier] ?? 0;
  
  return userLevel >= requiredLevel;
}

/**
 * Feature-spezifische Zugriffsprüfungen
 */
export const FEATURE_REQUIREMENTS: Record<string, TierLevel> = {
  // Basis-Features (Tier 1)
  'nebenkosten-pruefung': 'basis',
  'nebenkosten-rechner': 'basis',
  'musterbriefe': 'basis',
  
  // Professional-Features (Tier 2)
  'objekte': 'professional',
  'nebenkosten-abrechnung': 'professional',
  'renditerechner': 'professional',
  'contract-analysis': 'professional',
  'steuer': 'professional',
  'baurecht': 'professional',
  'profi-vorlagen': 'professional',
  
  // Lawyer-Features (Tier 3)
  'crm': 'lawyer',
  'deadlines': 'lawyer',
  'documents': 'lawyer',
  'fallanalyse': 'lawyer',
  'rechtsprechung': 'lawyer',
  'schriftsatz': 'lawyer',
  'templates-lawyer': 'lawyer',
};

/**
 * Prüft, ob der Benutzer Zugang zu einem bestimmten Feature hat
 */
export function hasFeatureAccess(userTier: string | undefined, featureId: string): boolean {
  const requiredTier = FEATURE_REQUIREMENTS[featureId];
  if (!requiredTier) return true;  // Unbekannte Features sind offen
  
  return hasTierAccess(userTier, requiredTier);
}

/**
 * Gibt den erforderlichen Tier für ein Feature zurück
 */
export function getRequiredTierForFeature(featureId: string): TierLevel | null {
  return FEATURE_REQUIREMENTS[featureId] || null;
}

/**
 * Gibt den deutschen Namen für einen Tier zurück
 */
export function getTierDisplayName(tier: string | undefined): string {
  const normalizedTier = normalizeTier(tier);
  
  switch (normalizedTier) {
    case 'free': return 'Kostenlos';
    case 'basis': return 'Basis';
    case 'professional': return 'Professional';
    case 'lawyer': return 'Anwalt Pro';
    default: return 'Unbekannt';
  }
}
