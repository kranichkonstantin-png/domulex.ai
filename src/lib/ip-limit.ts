// IP-Hash Utility für anonymes Tracking
export async function getAnonymousId(): Promise<string> {
  // Browser Fingerprint (vereinfacht - für Production besser machen)
  const userAgent = navigator.userAgent;
  const language = navigator.language;
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const screen = `${window.screen.width}x${window.screen.height}`;
  
  const fingerprint = `${userAgent}|${language}|${timezone}|${screen}`;
  
  // Hash erstellen
  const msgUint8 = new TextEncoder().encode(fingerprint);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  
  return hashHex.substring(0, 16); // Erste 16 Zeichen
}

// Prüfe Queries für anonyme Nutzer
export function checkAnonymousQueryLimit(): { queriesUsed: number; canQuery: boolean } {
  const stored = localStorage.getItem('domulex_anonymous_queries');
  
  if (!stored) {
    return { queriesUsed: 0, canQuery: true };
  }
  
  const data = JSON.parse(stored);
  const queriesUsed = data.count || 0;
  const timestamp = new Date(data.timestamp).getTime();
  const now = Date.now();
  const twentyFourHours = 24 * 60 * 60 * 1000;
  
  // Reset nach 24h
  if (now - timestamp > twentyFourHours) {
    localStorage.removeItem('domulex_anonymous_queries');
    return { queriesUsed: 0, canQuery: true };
  }
  
  return {
    queriesUsed,
    canQuery: queriesUsed < 3
  };
}

// Inkrement anonym
export function incrementAnonymousQuery(): boolean {
  const { queriesUsed, canQuery } = checkAnonymousQueryLimit();
  
  if (!canQuery) {
    return false;
  }
  
  localStorage.setItem('domulex_anonymous_queries', JSON.stringify({
    count: queriesUsed + 1,
    timestamp: new Date().toISOString()
  }));
  
  return true;
}
