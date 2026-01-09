import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut, 
  sendPasswordResetEmail,
  sendEmailVerification,
  User,
  updateProfile,
  onAuthStateChanged
} from 'firebase/auth';
import { doc, setDoc, getDoc, updateDoc, serverTimestamp } from 'firebase/firestore';
import { auth, db } from './firebase';
import { initializeSession, clearSessionId } from './session';

export interface UserProfile {
  uid: string;
  email: string;
  displayName?: string;
  plan: 'free' | 'mieter_plus' | 'professional' | 'lawyer';
  tier?: 'free' | 'basis' | 'professional' | 'lawyer'; // Neues Feld (hat Vorrang vor plan)
  queriesUsed: number;
  queriesLimit: number;
  stripeCustomerId?: string;
  stripeSubscriptionId?: string;
  subscriptionStatus?: 'active' | 'canceled' | 'past_due' | 'trialing';
  createdAt: any;
  updatedAt: any;
  emailVerified: boolean;
  lastActivityAt?: string; // Aktivitäts-Tracking für Inaktivitäts-Löschung
}

// Plan Limits
const PLAN_LIMITS = {
  free: 3,
  mieter_plus: 50,      // Basis: 50 Anfragen/Monat
  professional: 250,    // Professional: 250 Anfragen/Monat
  lawyer: 999999,       // Lawyer Pro: Unbegrenzt
};

/**
 * Registrierung mit Email & Passwort
 */
export async function registerWithEmail(
  email: string, 
  password: string,
  displayName?: string
): Promise<{ user: User; profile: UserProfile }> {
  try {
    // Firebase Auth User erstellen
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // DisplayName setzen
    if (displayName) {
      await updateProfile(user, { displayName });
    }

    // Email-Verifizierung senden
    await sendEmailVerification(user, {
      url: `${window.location.origin}/app?verified=true`,
      handleCodeInApp: false,
    });

    // User-Profil in Firestore erstellen
    const userProfile: UserProfile = {
      uid: user.uid,
      email: user.email!,
      displayName: displayName || user.email!.split('@')[0],
      plan: 'free',
      queriesUsed: 0,
      queriesLimit: PLAN_LIMITS.free,
      emailVerified: false,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
    };

    await setDoc(doc(db, 'users', user.uid), userProfile);

    // Welcome Email senden (über Backend)
    try {
      const formData = new FormData();
      formData.append('user_email', user.email!);
      formData.append('user_name', displayName || user.email!.split('@')[0]);
      
      await fetch('https://domulex-backend-lytuxcyyka-ey.a.run.app/email/send-welcome', {
        method: 'POST',
        body: formData,
      });
    } catch (emailError) {
      // Email-Fehler nicht nach oben werfen, Registrierung soll trotzdem funktionieren
      console.warn('Failed to send welcome email:', emailError);
    }

    return { user, profile: userProfile };
  } catch (error: any) {
    console.error('Registration error:', error);
    throw new Error(getAuthErrorMessage(error.code));
  }
}

/**
 * Login mit Email & Passwort
 */
export async function loginWithEmail(email: string, password: string): Promise<User> {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    
    // Register session for single-device enforcement
    await initializeSession();
    
    return userCredential.user;
  } catch (error: any) {
    console.error('Login error:', error);
    throw new Error(getAuthErrorMessage(error.code));
  }
}

/**
 * Logout
 */
export async function logout(): Promise<void> {
  try {
    // Clear local session
    clearSessionId();
    await signOut(auth);
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
}

/**
 * Passwort zurücksetzen
 */
export async function resetPassword(email: string): Promise<void> {
  try {
    await sendPasswordResetEmail(auth, email, {
      url: `${window.location.origin}/login?reset=success`,
      handleCodeInApp: false,
    });
  } catch (error: any) {
    console.error('Password reset error:', error);
    throw new Error(getAuthErrorMessage(error.code));
  }
}

/**
 * User-Profil aus Firestore laden
 */
export async function getUserProfile(uid: string): Promise<UserProfile | null> {
  try {
    const docRef = doc(db, 'users', uid);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      return docSnap.data() as UserProfile;
    }
    return null;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    return null;
  }
}

/**
 * User-Profil aktualisieren
 */
export async function updateUserProfile(
  uid: string, 
  updates: Partial<UserProfile>
): Promise<void> {
  try {
    const docRef = doc(db, 'users', uid);
    await updateDoc(docRef, {
      ...updates,
      updatedAt: serverTimestamp(),
    });
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
}

/**
 * Query-Counter inkrementieren und lastActivityAt aktualisieren
 */
export async function incrementUserQueries(uid: string): Promise<void> {
  try {
    const profile = await getUserProfile(uid);
    if (!profile) throw new Error('User profile not found');

    await updateUserProfile(uid, {
      queriesUsed: profile.queriesUsed + 1,
      lastActivityAt: new Date().toISOString(), // Aktivitäts-Tracking für Inaktivitäts-Löschung
    });
  } catch (error) {
    console.error('Error incrementing queries:', error);
    throw error;
  }
}

/**
 * Monatlichen Query-Reset durchführen
 */
export async function resetMonthlyQueries(uid: string): Promise<void> {
  try {
    await updateUserProfile(uid, {
      queriesUsed: 0,
    });
  } catch (error) {
    console.error('Error resetting queries:', error);
    throw error;
  }
}

/**
 * Auth-State-Listener
 */
export function onAuthChange(callback: (user: User | null) => void) {
  return onAuthStateChanged(auth, callback);
}

/**
 * Fehler-Messages übersetzen
 */
function getAuthErrorMessage(errorCode: string): string {
  const messages: Record<string, string> = {
    'auth/email-already-in-use': 'Diese E-Mail-Adresse wird bereits verwendet.',
    'auth/invalid-email': 'Ungültige E-Mail-Adresse.',
    'auth/operation-not-allowed': 'Operation nicht erlaubt.',
    'auth/weak-password': 'Passwort ist zu schwach. Mindestens 6 Zeichen erforderlich.',
    'auth/user-disabled': 'Dieses Konto wurde deaktiviert.',
    'auth/user-not-found': 'Kein Konto mit dieser E-Mail-Adresse gefunden.',
    'auth/wrong-password': 'Falsches Passwort.',
    'auth/too-many-requests': 'Zu viele Anfragen. Bitte versuchen Sie es später erneut.',
    'auth/network-request-failed': 'Netzwerkfehler. Bitte prüfen Sie Ihre Internetverbindung.',
  };

  return messages[errorCode] || 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.';
}
