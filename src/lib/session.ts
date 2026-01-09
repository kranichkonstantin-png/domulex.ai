/**
 * Session Management for Single-Device Authentication
 * 
 * This module ensures that a user can only be logged in on ONE device at a time.
 * When a user logs in on a new device, all other sessions are invalidated.
 */

import { auth } from './firebase';

const SESSION_STORAGE_KEY = 'domulex_session_id';
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';

/**
 * Generate a unique session ID
 */
export function generateSessionId(): string {
  const timestamp = Date.now().toString(36);
  const randomPart = Math.random().toString(36).substring(2, 15);
  const browserFingerprint = getBrowserFingerprint();
  return `${timestamp}-${randomPart}-${browserFingerprint}`;
}

/**
 * Get a simple browser fingerprint for device identification
 */
function getBrowserFingerprint(): string {
  if (typeof window === 'undefined') return 'server';
  
  const components = [
    navigator.userAgent,
    navigator.language,
    screen.width,
    screen.height,
    new Date().getTimezoneOffset(),
  ];
  
  // Simple hash
  const str = components.join('|');
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash).toString(36);
}

/**
 * Get device info string for logging
 */
export function getDeviceInfo(): string {
  if (typeof window === 'undefined') return 'Server';
  
  const ua = navigator.userAgent;
  let device = 'Unknown';
  
  if (/iPhone|iPad|iPod/.test(ua)) {
    device = 'iOS';
  } else if (/Android/.test(ua)) {
    device = 'Android';
  } else if (/Windows/.test(ua)) {
    device = 'Windows';
  } else if (/Mac/.test(ua)) {
    device = 'Mac';
  } else if (/Linux/.test(ua)) {
    device = 'Linux';
  }
  
  const browser = /Chrome/.test(ua) ? 'Chrome' : 
                  /Firefox/.test(ua) ? 'Firefox' : 
                  /Safari/.test(ua) ? 'Safari' : 
                  /Edge/.test(ua) ? 'Edge' : 'Other';
  
  return `${device} - ${browser}`;
}

/**
 * Get current session ID from localStorage
 */
export function getSessionId(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(SESSION_STORAGE_KEY);
}

/**
 * Store session ID in localStorage
 */
export function setSessionId(sessionId: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
}

/**
 * Clear session ID from localStorage
 */
export function clearSessionId(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(SESSION_STORAGE_KEY);
}

/**
 * Register a new session with the backend
 * This invalidates all other sessions for this user
 */
export async function registerSession(): Promise<{ success: boolean; sessionId?: string; error?: string }> {
  try {
    const currentUser = auth.currentUser;
    if (!currentUser) {
      return { success: false, error: 'Not authenticated' };
    }
    
    const sessionId = generateSessionId();
    const deviceInfo = getDeviceInfo();
    const token = await currentUser.getIdToken();
    
    const response = await fetch(`${BACKEND_URL}/auth/register-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        session_id: sessionId,
        device_info: deviceInfo,
      }),
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return { success: false, error: error.detail || 'Failed to register session' };
    }
    
    // Store session ID locally
    setSessionId(sessionId);
    
    return { success: true, sessionId };
  } catch (error: any) {
    console.error('Session registration error:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Get headers with session ID for API calls
 */
export function getSessionHeaders(): Record<string, string> {
  const sessionId = getSessionId();
  if (sessionId) {
    return { 'X-Session-ID': sessionId };
  }
  return {};
}

/**
 * Handle session conflict (user logged in on another device)
 * This function should be called when API returns SESSION_EXPIRED_OTHER_DEVICE
 */
export async function handleSessionConflict(): Promise<void> {
  clearSessionId();
  
  // Sign out the user
  try {
    await auth.signOut();
  } catch (error) {
    console.error('Error signing out:', error);
  }
  
  // Show notification and redirect
  if (typeof window !== 'undefined') {
    alert('Sie wurden abgemeldet, da Ihr Konto auf einem anderen Gerät verwendet wird. Gemäß unserer AGB ist die gleichzeitige Nutzung auf mehreren Geräten nicht gestattet.');
    window.location.href = '/auth/login?reason=other_device';
  }
}

/**
 * Initialize session on login
 * Call this after successful Firebase authentication
 */
export async function initializeSession(): Promise<boolean> {
  const result = await registerSession();
  
  if (!result.success) {
    console.error('Failed to initialize session:', result.error);
    return false;
  }
  
  console.log('Session initialized:', result.sessionId);
  return true;
}
