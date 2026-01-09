'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { collection, getDocs, doc, updateDoc, deleteDoc, query, orderBy, addDoc, Timestamp, where } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import Logo from '@/components/Logo';

interface User {
  id: string;
  email: string;
  name: string;
  tier: string;
  dashboardType?: string; // 'basis' | 'professional' | 'lawyer'
  queriesUsed: number;
  queriesLimit: number;
  createdAt: string;
  lastActivityAt?: string;
  stripeCustomerId?: string;
  stripeSubscriptionId?: string;
  isAdmin?: boolean;
  isTestUser?: boolean;  // Test-Kunden sehen keine Upgrade-Buttons
  scheduledDeletionAt?: string;
}

interface DeleteRequest {
  id: string;
  userId: string;
  userEmail: string;
  userName: string;
  reason?: string;
  createdAt: any;
  status: 'pending' | 'completed';
}

// Backend URL
const BACKEND_URL = 'https://domulex-backend-lytuxcyyka-ey.a.run.app';

// 6 Monate in Millisekunden
const SIX_MONTHS_MS = 6 * 30 * 24 * 60 * 60 * 1000;

// Standard-Admins (als Fallback)
const DEFAULT_ADMIN_EMAILS = ['kontakt@domulex.ai', 'admin@domulex.ai'];

export default function AdminDashboard() {
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState({
    totalUsers: 0,
    freeUsers: 0,
    freeBasis: 0,
    freeProfessional: 0,
    freeLawyer: 0,
    premiumUsers: 0,
    totalQueries: 0,
    lawyerUsers: 0,
    lawyerQueries: 0,
    lawyerAboveLimit: 0, // Lawyer mit >2000 Anfragen
  });
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  const [activeTab, setActiveTab] = useState<'users' | 'messages' | 'inactive' | 'create' | 'delete-requests' | 'billing' | 'email' | 'usage'>('users');
  const [deleteRequests, setDeleteRequests] = useState<DeleteRequest[]>([]);
  
  // Query Edit Modal state
  const [editingQueryUser, setEditingQueryUser] = useState<User | null>(null);
  const [newQueryCount, setNewQueryCount] = useState<number>(0);
  
  // Billing state
  const [invoices, setInvoices] = useState<any[]>([]);
  const [creditNotes, setCreditNotes] = useState<any[]>([]);
  const [loadingBilling, setLoadingBilling] = useState(false);
  
  // Email config state
  const [emailConfig, setEmailConfig] = useState({
    smtp_host: 'smtp.strato.de',
    smtp_port: 465,
    smtp_user: '',
    smtp_password: '',
    from_email: 'info@domulex.ai',
    from_name: 'domulex.ai',
    use_ssl: true,
    configured: false,
  });
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailTestResult, setEmailTestResult] = useState<{success: boolean; message: string} | null>(null);
  const [testEmailAddress, setTestEmailAddress] = useState('');
  
  // Email inbox state
  const [emailTab, setEmailTab] = useState<'config' | 'inbox' | 'compose' | 'templates'>('inbox');
  const [emails, setEmails] = useState<any[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<any>(null);
  const [emailFolders, setEmailFolders] = useState<string[]>(['INBOX', 'SENT', 'DRAFTS', 'TRASH']);
  const [currentFolder, setCurrentFolder] = useState('INBOX');
  const [unreadCount, setUnreadCount] = useState(0);
  const [loadingEmails, setLoadingEmails] = useState(false);
  const [composeForm, setComposeForm] = useState({
    to: '',
    subject: '',
    body: '',
    html: true,
  });
  const [sendingEmail, setSendingEmail] = useState(false);
  
  // Email Templates state
  const [selectedTemplate, setSelectedTemplate] = useState<string>('welcome');
  const [templateRecipient, setTemplateRecipient] = useState('');
  const [templateParams, setTemplateParams] = useState({
    user_name: 'Max Mustermann',
    plan_name: 'Premium',
    plan_price: '49.00',
    subscription_id: 'sub_123456789',
    end_date: '31.01.2026',
    new_tier: 'Premium',
    queries_limit: '100',
    title: 'Wichtige Information',
    message: 'Dies ist eine Testnachricht.',
    company_name: 'Musterfirma GmbH',
  });
  const [sendingTemplate, setSendingTemplate] = useState(false);
  const [templateResult, setTemplateResult] = useState<{success: boolean; message: string} | null>(null);
  
  const [messageForm, setMessageForm] = useState({
    recipient: 'all', // 'all' | userId
    title: '',
    message: '',
    type: 'info' as 'info' | 'success' | 'warning' | 'admin',
    sendEmail: true,
  });
  const [sending, setSending] = useState(false);
  const [newUserForm, setNewUserForm] = useState({
    email: '',
    password: '',
    name: '',
    tier: 'free',
    isAdmin: false,
    accountType: 'test' as 'test' | 'paying', // test = kein Upgrade, paying = Stripe Checkout
  });
  const [creating, setCreating] = useState(false);
  const router = useRouter();

  // Prüft ob Benutzer Admin ist (Standard-Admin oder isAdmin Feld in Firestore)
  const checkIsAdmin = async (email: string, userId: string): Promise<boolean> => {
    // Standard-Admins immer erlauben (case-insensitive)
    const emailLower = email.toLowerCase();
    if (DEFAULT_ADMIN_EMAILS.some(e => e.toLowerCase() === emailLower)) {
      return true;
    }
    // Prüfe isAdmin Feld in Firestore
    try {
      const usersQuery = query(collection(db, 'users'));
      const snapshot = await getDocs(usersQuery);
      const userDoc = snapshot.docs.find(d => d.id === userId);
      return userDoc?.data()?.isAdmin === true;
    } catch {
      return false;
    }
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        router.push('/auth/login');
        return;
      }

      // Check if user is admin
      const adminStatus = await checkIsAdmin(user.email || '', user.uid);
      if (!adminStatus) {
        router.push('/dashboard');
        return;
      }

      setCurrentUser(user);
      setIsAdmin(true);
      await loadData();
    });

    return () => unsubscribe();
  }, [router]);

  // Helper function to display tier nicely
  const getTierDisplay = (tier: string, dashboardType?: string): { label: string; badge: string; color: string } => {
    if (tier === 'free_basis' || (tier === 'free' && dashboardType === 'basis')) {
      return { label: 'Free Basis', badge: '🏠', color: 'bg-gray-100 text-gray-700' };
    }
    if (tier === 'free_professional' || (tier === 'free' && dashboardType === 'professional')) {
      return { label: 'Free Professional', badge: '🏢', color: 'bg-gray-100 text-gray-700' };
    }
    if (tier === 'free_lawyer' || (tier === 'free' && dashboardType === 'lawyer')) {
      return { label: 'Free Lawyer Pro', badge: '⚖️', color: 'bg-gray-100 text-gray-700' };
    }
    if (tier === 'free') {
      return { label: 'Free (Unbekannt)', badge: '❓', color: 'bg-gray-100 text-gray-500' };
    }
    if (tier === 'basis') {
      return { label: 'Basis', badge: '🏠', color: 'bg-blue-100 text-blue-700' };
    }
    if (tier === 'professional') {
      return { label: 'Professional', badge: '🏢', color: 'bg-green-100 text-green-700' };
    }
    if (tier === 'lawyer') {
      return { label: 'Lawyer Pro', badge: '⚖️', color: 'bg-purple-100 text-purple-700' };
    }
    return { label: tier, badge: '', color: 'bg-gray-100 text-gray-700' };
  };

  const loadData = async () => {
    setLoading(true);
    try {
      const usersQuery = query(collection(db, 'users'), orderBy('createdAt', 'desc'));
      const usersSnapshot = await getDocs(usersQuery);
      
      const usersData: User[] = [];
      let totalQueries = 0;
      let freeCount = 0;
      let freeBasisCount = 0;
      let freeProfessionalCount = 0;
      let freeLawyerCount = 0;
      let premiumCount = 0;
      let lawyerCount = 0;
      let lawyerQueriesTotal = 0;
      let lawyerAboveLimitCount = 0;

      usersSnapshot.forEach((doc) => {
        const data = doc.data();
        usersData.push({
          id: doc.id,
          ...data,
        } as User);

        totalQueries += data.queriesUsed || 0;
        if (data.tier === 'free' || data.tier?.startsWith('free_')) {
          freeCount++;
          // Zähle nach Dashboard-Typ
          if (data.tier === 'free_basis' || data.dashboardType === 'basis') {
            freeBasisCount++;
          } else if (data.tier === 'free_professional' || data.dashboardType === 'professional') {
            freeProfessionalCount++;
          } else if (data.tier === 'free_lawyer' || data.dashboardType === 'lawyer') {
            freeLawyerCount++;
          } else {
            // Fallback: alte Free-Nutzer ohne spezifischen Typ
            freeBasisCount++;
          }
        } else if (data.tier === 'lawyer') {
          lawyerCount++;
          lawyerQueriesTotal += data.queriesUsed || 0;
          if ((data.queriesUsed || 0) > 2000) lawyerAboveLimitCount++;
        } else premiumCount++;
      });

      setUsers(usersData);
      setStats({
        totalUsers: usersData.length,
        freeUsers: freeCount,
        freeBasis: freeBasisCount,
        freeProfessional: freeProfessionalCount,
        freeLawyer: freeLawyerCount,
        premiumUsers: premiumCount,
        totalQueries,
        lawyerUsers: lawyerCount,
        lawyerQueries: lawyerQueriesTotal,
        lawyerAboveLimit: lawyerAboveLimitCount,
      });

      // Lade Löschanfragen
      const deleteRequestsQuery = query(collection(db, 'delete_requests'), orderBy('createdAt', 'desc'));
      const deleteRequestsSnapshot = await getDocs(deleteRequestsQuery);
      const deleteRequestsData: DeleteRequest[] = [];
      deleteRequestsSnapshot.forEach((doc) => {
        deleteRequestsData.push({ id: doc.id, ...doc.data() } as DeleteRequest);
      });
      setDeleteRequests(deleteRequestsData);

      // Lade E-Mail-Konfiguration
      try {
        const emailResponse = await fetch(`${BACKEND_URL}/admin/email/config`);
        if (emailResponse.ok) {
          const emailData = await emailResponse.json();
          setEmailConfig(prev => ({ ...prev, ...emailData }));
          // Lade auch die Inbox wenn konfiguriert
          if (emailData.configured) {
            loadEmails('INBOX');
          }
        }
      } catch (emailErr) {
        console.log('Email config not available');
      }
    } catch (err) {
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  // E-Mail Funktionen
  const loadEmails = async (folder: string = 'INBOX') => {
    setLoadingEmails(true);
    try {
      const response = await fetch(`${BACKEND_URL}/admin/email/inbox?folder=${folder}&limit=50`);
      if (response.ok) {
        const data = await response.json();
        setEmails(data.emails || []);
        setUnreadCount(data.unread || 0);
        setCurrentFolder(folder);
      }
    } catch (err) {
      console.error('Error loading emails:', err);
    } finally {
      setLoadingEmails(false);
    }
  };

  const loadEmailFolders = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/admin/email/folders`);
      if (response.ok) {
        const data = await response.json();
        setEmailFolders(data.folders || ['INBOX', 'SENT', 'DRAFTS', 'TRASH']);
      }
    } catch (err) {
      console.error('Error loading folders:', err);
    }
  };

  const openEmail = async (email: any) => {
    setSelectedEmail(email);
    // Als gelesen markieren wenn ungelesen
    if (!email.is_read) {
      try {
        await fetch(`${BACKEND_URL}/admin/email/message/${email.id}/read`, { method: 'POST' });
        setEmails(prev => prev.map(e => e.id === email.id ? { ...e, is_read: true } : e));
        setUnreadCount(prev => Math.max(0, prev - 1));
      } catch (err) {
        console.error('Error marking as read:', err);
      }
    }
  };

  const deleteEmail = async (emailId: string) => {
    if (!confirm('Diese E-Mail wirklich löschen?')) return;
    try {
      await fetch(`${BACKEND_URL}/admin/email/message/${emailId}`, { method: 'DELETE' });
      setEmails(prev => prev.filter(e => e.id !== emailId));
      setSelectedEmail(null);
    } catch (err) {
      console.error('Error deleting email:', err);
    }
  };

  const sendEmail = async () => {
    if (!composeForm.to || !composeForm.subject || !composeForm.body) {
      alert('Bitte alle Felder ausfüllen');
      return;
    }
    setSendingEmail(true);
    try {
      const formData = new URLSearchParams();
      formData.append('to', composeForm.to);
      formData.append('subject', composeForm.subject);
      formData.append('body', composeForm.body);
      formData.append('html', composeForm.html.toString());

      const response = await fetch(`${BACKEND_URL}/admin/email/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });

      if (response.ok) {
        alert('E-Mail gesendet!');
        setComposeForm({ to: '', subject: '', body: '', html: true });
        setEmailTab('inbox');
      } else {
        const data = await response.json();
        throw new Error(data.detail || 'Fehler beim Senden');
      }
    } catch (err: any) {
      alert('Fehler: ' + err.message);
    } finally {
      setSendingEmail(false);
    }
  };

  const replyToEmail = (email: any) => {
    setComposeForm({
      to: email.from_email || email.sender || '',
      subject: email.subject?.startsWith('Re:') ? email.subject : `Re: ${email.subject}`,
      body: `\n\n---\nAm ${email.date} schrieb ${email.from_name || email.sender}:\n${email.body_text || ''}`,
      html: false,
    });
    setSelectedEmail(null);
    setEmailTab('compose');
  };

  const handleDeleteUser = async (userId: string) => {
    const user = users.find(u => u.id === userId);
    const userName = user?.name || 'Unbekannt';
    const userEmail = user?.email || 'Unbekannt';
    
    // Erste Bestätigung
    if (!confirm(`⚠️ ACHTUNG: Benutzer löschen?\n\nName: ${userName}\nE-Mail: ${userEmail}\n\nDies löscht den Benutzer UNWIDERRUFLICH aus Firebase Auth UND Firestore!`)) return;
    
    // Zweite Bestätigung
    if (!confirm(`🚨 LETZTE WARNUNG!\n\nSind Sie WIRKLICH sicher, dass Sie "${userEmail}" löschen möchten?\n\nDiese Aktion kann NICHT rückgängig gemacht werden!`)) return;

    try {
      // Backend API aufrufen um User komplett zu löschen
      const response = await fetch(`${BACKEND_URL}/admin/delete-user/${userId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ admin_email: currentUser?.email || '' }),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Fehler beim Löschen');
      }
      await loadData();
    } catch (err: any) {
      console.error('Error deleting user:', err);
      alert('Fehler beim Löschen des Benutzers: ' + (err.message || err));
    }
  };

  const handleResetQueries = async (userId: string) => {
    try {
      await updateDoc(doc(db, 'users', userId), {
        queriesUsed: 0,
      });
      await loadData();
    } catch (err) {
      console.error('Error resetting queries:', err);
      alert('Fehler beim Zurücksetzen der Anfragen');
    }
  };

  const handleSetQueries = async (userId: string, newCount: number) => {
    try {
      await updateDoc(doc(db, 'users', userId), {
        queriesUsed: Math.max(0, newCount),
      });
      setEditingQueryUser(null);
      await loadData();
    } catch (err) {
      console.error('Error setting queries:', err);
      alert('Fehler beim Setzen der Anfragen');
    }
  };

  const openQueryEditor = (user: User) => {
    setEditingQueryUser(user);
    setNewQueryCount(user.queriesUsed);
  };

  const handleChangeTier = async (userId: string, newTier: string) => {
    const limits = {
      free: 3,
      basis: 50,            // Basis: 50 Anfragen/Monat
      professional: 250,    // Professional: 250 Anfragen/Monat
      lawyer: 999999,       // Lawyer Pro: Unbegrenzt
    };

    const tierNames: Record<string, string> = {
      free: 'Free',
      basis: 'Basis (19€/Monat)',
      professional: 'Professional (39€/Monat)',
      lawyer: 'Lawyer Pro (69€/Monat)',
    };

    const user = users.find(u => u.id === userId);
    if (!user) return;

    try {
      await updateDoc(doc(db, 'users', userId), {
        tier: newTier,
        queriesLimit: limits[newTier as keyof typeof limits],
      });

      // Automatische Benachrichtigung bei Tier-Änderung
      const title = newTier === 'free' ? 'Ihr Abo wurde beendet' : 'Ihr Abo wurde aktualisiert';
      const message = newTier === 'free' 
        ? `Ihr Abonnement wurde beendet. Sie nutzen jetzt den kostenlosen Tarif mit ${limits.free} Anfragen pro Monat.`
        : `Ihr Abonnement wurde auf ${tierNames[newTier]} aktualisiert. Sie haben jetzt ${limits[newTier as keyof typeof limits]} Anfragen pro Monat.`;

      // Firestore Notification
      await addDoc(collection(db, 'notifications'), {
        userId,
        title,
        message,
        type: 'success',
        read: false,
        createdAt: Timestamp.now(),
      });

      // E-Mail senden
      try {
        await fetch(`${BACKEND_URL}/email/send-tier-change`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            user_email: user.email,
            user_name: user.name,
            new_tier: tierNames[newTier],
            queries_limit: String(limits[newTier as keyof typeof limits]),
          }),
        });
      } catch (emailErr) {
        console.error('Email failed:', emailErr);
      }

      await loadData();
    } catch (err) {
      console.error('Error changing tier:', err);
      alert('Fehler beim Ändern des Tarifs');
    }
  };

  const handleToggleAdmin = async (userId: string, userEmail: string, currentIsAdmin: boolean) => {
    // Standard-Admins können nicht degradiert werden
    if (DEFAULT_ADMIN_EMAILS.includes(userEmail)) {
      alert('Standard-Admin-Rechte können nicht geändert werden.');
      return;
    }

    const action = currentIsAdmin ? 'ENTZIEHEN' : 'GEWÄHREN';
    const warning = currentIsAdmin 
      ? `⚠️ Admin-Rechte entziehen?\n\nBenutzer: ${userEmail}\n\nDieser Benutzer verliert den Zugriff auf das Admin-Dashboard!`
      : `👑 Admin-Rechte gewähren?\n\nBenutzer: ${userEmail}\n\nDieser Benutzer erhält vollen Zugriff auf das Admin-Dashboard und kann alle Benutzerdaten sehen und ändern!`;
    
    if (!confirm(warning)) return;

    try {
      await updateDoc(doc(db, 'users', userId), {
        isAdmin: !currentIsAdmin,
      });
      alert(`✅ Admin-Rechte wurden ${currentIsAdmin ? 'entzogen' : 'gewährt'}.`);
      await loadData();
    } catch (err) {
      console.error('Error toggling admin:', err);
      alert('Fehler beim Ändern der Admin-Rechte');
    }
  };

  // Notification & Email senden
  const sendNotification = async (userId: string, userEmail: string, userName: string) => {
    // Firestore Notification erstellen
    await addDoc(collection(db, 'notifications'), {
      userId,
      title: messageForm.title,
      message: messageForm.message,
      type: messageForm.type === 'admin' ? 'admin' : messageForm.type,
      read: false,
      createdAt: Timestamp.now(),
    });

    // E-Mail senden wenn aktiviert
    if (messageForm.sendEmail) {
      try {
        await fetch(`${BACKEND_URL}/email/send-admin-notification`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            user_email: userEmail,
            user_name: userName,
            title: messageForm.title,
            message: messageForm.message,
          }),
        });
      } catch (err) {
        console.error('Email failed:', err);
      }
    }
  };

  const handleSendMessage = async () => {
    if (!messageForm.title.trim() || !messageForm.message.trim()) {
      alert('Bitte Titel und Nachricht eingeben.');
      return;
    }

    setSending(true);
    try {
      if (messageForm.recipient === 'all') {
        // An alle Benutzer senden
        for (const user of users) {
          await sendNotification(user.id, user.email, user.name);
        }
        alert(`Nachricht an ${users.length} Benutzer gesendet!`);
      } else {
        // An einzelnen Benutzer senden
        const user = users.find(u => u.id === messageForm.recipient);
        if (user) {
          await sendNotification(user.id, user.email, user.name);
          alert(`Nachricht an ${user.email} gesendet!`);
        }
      }
      // Form zurücksetzen
      setMessageForm({ ...messageForm, title: '', message: '' });
    } catch (err) {
      console.error('Error sending message:', err);
      alert('Fehler beim Senden der Nachricht');
    } finally {
      setSending(false);
    }
  };

  // Neuen Benutzer erstellen (Firebase Auth + Firestore)
  const handleCreateUser = async () => {
    if (!newUserForm.email || !newUserForm.password || !newUserForm.name) {
      alert('Bitte alle Pflichtfelder ausfüllen');
      return;
    }

    if (newUserForm.password.length < 6) {
      alert('Passwort muss mindestens 6 Zeichen lang sein');
      return;
    }

    // Wenn zahlender Kunde und kein free-Tier, muss Stripe verwendet werden
    if (newUserForm.accountType === 'paying' && newUserForm.tier !== 'free') {
      // Zahlender Kunde: Erstelle User als free, dann Stripe Checkout Link generieren
      setCreating(true);
      try {
        // 1. User als Free erstellen
        const createResponse = await fetch(`${BACKEND_URL}/admin/create-user`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            email: newUserForm.email,
            password: newUserForm.password,
            name: newUserForm.name,
            tier: 'free',
            is_admin: newUserForm.isAdmin.toString(),
            admin_email: currentUser?.email || '',
            account_type: 'paying',
          }),
        });

        if (!createResponse.ok) {
          const err = await createResponse.json();
          throw new Error(err.detail || 'Fehler beim Erstellen');
        }

        const result = await createResponse.json();

        // 2. Checkout-Link für den gewünschten Tarif generieren
        const checkoutResponse = await fetch(`${BACKEND_URL}/admin/create-checkout-for-user`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: result.uid,
            user_email: newUserForm.email,
            tier: newUserForm.tier,
            admin_email: currentUser?.email || '',
          }),
        });

        if (!checkoutResponse.ok) {
          const err = await checkoutResponse.json();
          throw new Error(err.detail || 'Fehler beim Erstellen des Checkout-Links');
        }

        const checkoutResult = await checkoutResponse.json();
        
        alert(`✅ Benutzer ${newUserForm.email} erstellt!\n\n` +
              `📧 Checkout-Link wurde an ${newUserForm.email} gesendet.\n\n` +
              `💳 Der Kunde muss den Link öffnen und bezahlen, dann wird der ${newUserForm.tier}-Tarif aktiviert.\n\n` +
              `Link: ${checkoutResult.checkout_url}`);
        
        // Link in Zwischenablage kopieren
        navigator.clipboard?.writeText(checkoutResult.checkout_url);
        
        setNewUserForm({ email: '', password: '', name: '', tier: 'free', isAdmin: false, accountType: 'test' });
        await loadData();
        setActiveTab('users');
      } catch (err: any) {
        console.error('Error creating paying user:', err);
        alert(`Fehler: ${err.message}`);
      } finally {
        setCreating(false);
      }
      return;
    }

    // Test-Kunde: Direkt mit gewähltem Tier erstellen (kein Upgrade möglich)
    setCreating(true);
    try {
      const response = await fetch(`${BACKEND_URL}/admin/create-user`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          email: newUserForm.email,
          password: newUserForm.password,
          name: newUserForm.name,
          tier: newUserForm.tier,
          is_admin: newUserForm.isAdmin.toString(),
          admin_email: currentUser?.email || '',
          account_type: newUserForm.accountType,
        }),
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.detail || 'Fehler beim Erstellen');
      }

      const tierName = newUserForm.tier === 'free' ? 'Free' : 
                       newUserForm.tier === 'basis' ? 'Basis' :
                       newUserForm.tier === 'professional' ? 'Professional' : 'Lawyer Pro';
      
      alert(`✅ Test-Benutzer ${newUserForm.email} erfolgreich erstellt!\n\n` +
            `🎁 Tarif: ${tierName} (ohne Zahlung)\n` +
            `⚠️ Dieser Benutzer sieht KEINE Upgrade-Buttons.`);
      setNewUserForm({ email: '', password: '', name: '', tier: 'free', isAdmin: false, accountType: 'test' });
      await loadData();
      setActiveTab('users');
    } catch (err: any) {
      console.error('Error creating user:', err);
      alert(`Fehler: ${err.message}`);
    } finally {
      setCreating(false);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      router.push('/');
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  // Load billing data from Stripe
  const loadBillingData = async () => {
    setLoadingBilling(true);
    try {
      const [invoicesRes, creditNotesRes] = await Promise.all([
        fetch(`${BACKEND_URL}/admin/invoices?limit=50`),
        fetch(`${BACKEND_URL}/admin/credit-notes?limit=50`)
      ]);
      
      if (invoicesRes.ok) {
        const data = await invoicesRes.json();
        setInvoices(data.invoices || []);
      }
      
      if (creditNotesRes.ok) {
        const data = await creditNotesRes.json();
        setCreditNotes(data.credit_notes || []);
      }
    } catch (err) {
      console.error('Error loading billing data:', err);
    } finally {
      setLoadingBilling(false);
    }
  };

  // Handle invoice void/refund
  const handleVoidInvoice = async (invoiceId: string) => {
    if (!confirm('Möchten Sie diese Rechnung wirklich stornieren/gutschreiben?')) return;
    
    try {
      const response = await fetch(`${BACKEND_URL}/admin/invoices/${invoiceId}/void`, {
        method: 'POST'
      });
      const result = await response.json();
      
      if (result.success) {
        alert(`✅ ${result.message}`);
        await loadBillingData();
      } else {
        alert(`❌ ${result.message}`);
      }
    } catch (err: any) {
      alert(`Fehler: ${err.message}`);
    }
  };

  const handleRefundInvoice = async (invoiceId: string) => {
    if (!confirm('Möchten Sie diese Rechnung vollständig erstatten?')) return;
    
    try {
      const response = await fetch(`${BACKEND_URL}/admin/invoices/${invoiceId}/refund`, {
        method: 'POST'
      });
      const result = await response.json();
      
      if (result.success) {
        alert(`✅ ${result.message}`);
        await loadBillingData();
      } else {
        throw new Error(result.detail || 'Fehler bei Erstattung');
      }
    } catch (err: any) {
      alert(`Fehler: ${err.message}`);
    }
  };

  // Format date from Unix timestamp
  const formatUnixDate = (timestamp: number) => {
    if (!timestamp) return '-';
    return new Date(timestamp * 1000).toLocaleDateString('de-DE');
  };

  // Inaktive Free-User berechnen (6+ Monate keine Aktivität)
  const getInactiveUsers = () => {
    const now = Date.now();
    return users.filter(user => {
      // Nur Free-User prüfen
      if (!user.tier?.startsWith('free') && user.tier !== 'free') return false;
      
      const lastActivity = user.lastActivityAt ? new Date(user.lastActivityAt).getTime() : new Date(user.createdAt).getTime();
      const inactiveDays = Math.floor((now - lastActivity) / (24 * 60 * 60 * 1000));
      return inactiveDays >= 180; // 6 Monate
    });
  };

  // User zur Löschung vormerken (7 Tage Frist)
  const scheduleUserDeletion = async (userId: string, userEmail: string, userName: string) => {
    const deletionDate = new Date();
    deletionDate.setDate(deletionDate.getDate() + 7);
    
    try {
      await updateDoc(doc(db, 'users', userId), {
        scheduledDeletionAt: deletionDate.toISOString(),
      });

      // Warnung als Notification
      await addDoc(collection(db, 'notifications'), {
        userId,
        title: '⚠️ Ihr Konto wird in 7 Tagen gelöscht',
        message: `Aufgrund von 6 Monaten Inaktivität wird Ihr kostenloses Konto am ${deletionDate.toLocaleDateString('de-DE')} gelöscht. Melden Sie sich an, um Ihr Konto zu behalten.`,
        type: 'warning',
        read: false,
        createdAt: Timestamp.now(),
      });

      // E-Mail senden
      try {
        await fetch(`${BACKEND_URL}/email/send-account-deletion-reminder`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            user_email: userEmail,
            user_name: userName,
            deletion_date: deletionDate.toLocaleDateString('de-DE'),
          }),
        });
      } catch (err) {
        console.error('Email failed:', err);
      }

      await loadData();
      alert(`Löschung für ${userEmail} geplant am ${deletionDate.toLocaleDateString('de-DE')}`);
    } catch (err) {
      console.error('Error scheduling deletion:', err);
      alert('Fehler beim Planen der Löschung');
    }
  };

  // Sofortige Löschung des Users
  const deleteUserImmediately = async (userId: string) => {
    if (!confirm('Sind Sie sicher, dass Sie diesen Account SOFORT und unwiderruflich löschen möchten?')) return;
    
    try {
      // Lösche alle Notifications des Users
      const notifQuery = query(collection(db, 'notifications'), where('userId', '==', userId));
      const notifSnapshot = await getDocs(notifQuery);
      for (const notifDoc of notifSnapshot.docs) {
        await deleteDoc(notifDoc.ref);
      }
      
      // Lösche User-Dokument
      await deleteDoc(doc(db, 'users', userId));
      
      await loadData();
      alert('Account wurde gelöscht.');
    } catch (err) {
      console.error('Error deleting user:', err);
      alert('Fehler beim Löschen');
    }
  };

  // Löschung abbrechen
  const cancelDeletion = async (userId: string) => {
    try {
      await updateDoc(doc(db, 'users', userId), {
        scheduledDeletionAt: null,
      });
      await loadData();
      alert('Geplante Löschung wurde abgebrochen.');
    } catch (err) {
      console.error('Error canceling deletion:', err);
    }
  };

  const inactiveUsers = getInactiveUsers();
  const scheduledForDeletion = users.filter(u => u.scheduledDeletionAt);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Lädt Admin-Daten...</p>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex justify-between items-center h-[106px]">
            <div className="flex items-center gap-4">
              <Logo size="sm" />
              <span className="px-3 py-1 bg-red-100 text-red-700 text-xs font-bold rounded-full">
                ADMIN
              </span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600 hidden sm:inline">{currentUser?.email}</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm text-gray-700 hover:text-[#1e3a5f] whitespace-nowrap"
              >
                Abmelden
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="mt-1 text-gray-600">Benutzerverwaltung und Statistiken</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Gesamt Benutzer</h3>
            <p className="text-3xl font-bold text-gray-900">{stats.totalUsers}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Free Benutzer</h3>
            <p className="text-3xl font-bold text-gray-600">{stats.freeUsers}</p>
            <div className="mt-2 text-xs text-gray-500 space-y-1">
              <div className="flex justify-between">
                <span>🏠 Basis:</span>
                <span className="font-medium">{stats.freeBasis}</span>
              </div>
              <div className="flex justify-between">
                <span>🏢 Professional:</span>
                <span className="font-medium">{stats.freeProfessional}</span>
              </div>
              <div className="flex justify-between">
                <span>⚖️ Lawyer Pro:</span>
                <span className="font-medium">{stats.freeLawyer}</span>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Premium Benutzer</h3>
            <p className="text-3xl font-bold text-blue-600">{stats.premiumUsers}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Gesamt Anfragen</h3>
            <p className="text-3xl font-bold text-green-600">{stats.totalQueries}</p>
          </div>
        </div>
        
        {/* Lawyer Usage Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <h3 className="text-sm font-medium text-gray-600 mb-2">⚖️ Lawyer Pro Nutzer</h3>
            <p className="text-3xl font-bold text-purple-600">{stats.lawyerUsers}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <h3 className="text-sm font-medium text-gray-600 mb-2">⚖️ Lawyer Anfragen (gesamt)</h3>
            <p className="text-3xl font-bold text-purple-600">{stats.lawyerQueries}</p>
            <p className="text-xs text-gray-500 mt-1">Ø {stats.lawyerUsers > 0 ? Math.round(stats.lawyerQueries / stats.lawyerUsers) : 0} pro Nutzer</p>
          </div>
          <div className={`bg-white rounded-lg shadow p-6 border-l-4 ${stats.lawyerAboveLimit > 0 ? 'border-red-500' : 'border-green-500'}`}>
            <h3 className="text-sm font-medium text-gray-600 mb-2">⚠️ Fair-Use Überschreitung</h3>
            <p className={`text-3xl font-bold ${stats.lawyerAboveLimit > 0 ? 'text-red-600' : 'text-green-600'}`}>{stats.lawyerAboveLimit}</p>
            <p className="text-xs text-gray-500 mt-1">Lawyer mit &gt;2.000 Anfragen/Monat</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex overflow-x-auto gap-2 sm:gap-4 mb-6 pb-2 -mx-4 px-4 sm:mx-0 sm:px-0">
          <button
            onClick={() => setActiveTab('users')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'users'
                ? 'bg-[#1e3a5f] text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            👥 <span className="hidden sm:inline">Benutzerverwaltung</span><span className="sm:hidden">Nutzer</span>
          </button>
          <button
            onClick={() => setActiveTab('create')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'create'
                ? 'bg-[#1e3a5f] text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            ➕ <span className="hidden sm:inline">Neuer Benutzer</span><span className="sm:hidden">Neu</span>
          </button>
          <button
            onClick={() => setActiveTab('messages')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'messages'
                ? 'bg-[#1e3a5f] text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            ✉️ <span className="hidden sm:inline">Nachrichten</span><span className="sm:hidden">Msg</span>
          </button>
          <button
            onClick={() => setActiveTab('inactive')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'inactive'
                ? 'bg-[#1e3a5f] text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            ⚠️ <span className="hidden sm:inline">Inaktive</span> ({inactiveUsers.length})
          </button>
          <button
            onClick={() => setActiveTab('delete-requests')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'delete-requests'
                ? 'bg-red-600 text-white'
                : 'bg-white text-red-600 hover:bg-red-50 border border-red-200'
            }`}
          >
            🗑️ <span className="hidden sm:inline">Löschanfragen</span> ({deleteRequests.filter(r => r.status === 'pending').length})
          </button>
          <button
            onClick={() => setActiveTab('billing')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'billing'
                ? 'bg-green-600 text-white'
                : 'bg-white text-green-600 hover:bg-green-50 border border-green-200'
            }`}
          >
            📊 <span className="hidden sm:inline">Buchhaltung</span><span className="sm:hidden">$</span>
          </button>
          <button
            onClick={() => setActiveTab('email')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'email'
                ? 'bg-purple-600 text-white'
                : 'bg-white text-purple-600 hover:bg-purple-50 border border-purple-200'
            }`}
          >
            📧 <span className="hidden sm:inline">E-Mail</span>
          </button>
          <button
            onClick={() => setActiveTab('usage')}
            className={`flex-shrink-0 px-3 sm:px-6 py-2 sm:py-3 rounded-lg font-medium text-sm sm:text-base transition-colors ${
              activeTab === 'usage'
                ? 'bg-orange-600 text-white'
                : 'bg-white text-orange-600 hover:bg-orange-50 border border-orange-200'
            }`}
          >
            📈 <span className="hidden sm:inline">Nutzung</span> {stats.lawyerAboveLimit > 0 && <span className="ml-1 px-2 py-0.5 bg-red-500 text-white text-xs rounded-full">{stats.lawyerAboveLimit}</span>}
          </button>
        </div>

        {/* Create User Tab */}
        {activeTab === 'create' && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">➕ Neuen Benutzer anlegen</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">E-Mail *</label>
                <input
                  type="email"
                  value={newUserForm.email}
                  onChange={(e) => setNewUserForm({ ...newUserForm, email: e.target.value })}
                  placeholder="benutzer@example.de"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Passwort * (min. 6 Zeichen)</label>
                <input
                  type="text"
                  value={newUserForm.password}
                  onChange={(e) => setNewUserForm({ ...newUserForm, password: e.target.value })}
                  placeholder="Sicheres Passwort"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                <input
                  type="text"
                  value={newUserForm.name}
                  onChange={(e) => setNewUserForm({ ...newUserForm, name: e.target.value })}
                  placeholder="Vor- und Nachname"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tarif</label>
                <select
                  value={newUserForm.tier}
                  onChange={(e) => setNewUserForm({ ...newUserForm, tier: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="free">Free (3 Anfragen)</option>
                  <option value="basis">Basis (50 Anfragen) - 19€/Monat</option>
                  <option value="professional">Professional (250 Anfragen) - 39€/Monat</option>
                  <option value="lawyer">Lawyer Pro (Unbegrenzt) - 69€/Monat</option>
                </select>
              </div>
            </div>

            {/* Account-Typ Auswahl */}
            <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <label className="block text-sm font-medium text-gray-700 mb-3">🏷️ Account-Typ</label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => setNewUserForm({ ...newUserForm, accountType: 'test' })}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    newUserForm.accountType === 'test' 
                      ? 'border-purple-500 bg-purple-50' 
                      : 'border-gray-200 hover:border-purple-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xl">🧪</span>
                    <span className="font-semibold text-gray-900">Test-Kunde</span>
                    {newUserForm.accountType === 'test' && <span className="text-purple-600">✓</span>}
                  </div>
                  <p className="text-sm text-gray-600">
                    Erhält gewählten Tarif <strong>kostenlos</strong>. 
                    Sieht <strong>keine Upgrade-Buttons</strong>. 
                    Ideal für Beta-Tester, Partner.
                  </p>
                </button>
                
                <button
                  type="button"
                  onClick={() => setNewUserForm({ ...newUserForm, accountType: 'paying' })}
                  className={`p-4 rounded-lg border-2 text-left transition-all ${
                    newUserForm.accountType === 'paying' 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-gray-200 hover:border-green-300'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xl">💳</span>
                    <span className="font-semibold text-gray-900">Zahlender Kunde</span>
                    {newUserForm.accountType === 'paying' && <span className="text-green-600">✓</span>}
                  </div>
                  <p className="text-sm text-gray-600">
                    Erstellt User als Free, sendet <strong>Stripe Checkout-Link</strong> per E-Mail.
                    Standard-Zahlungsprozess.
                  </p>
                </button>
              </div>
              
              {newUserForm.accountType === 'paying' && newUserForm.tier !== 'free' && (
                <div className="mt-3 p-3 bg-green-100 border border-green-300 rounded-lg text-sm text-green-800">
                  <strong>💳 Info:</strong> Der Kunde erhält einen Checkout-Link für den {newUserForm.tier === 'basis' ? 'Basis (19€/Monat)' : newUserForm.tier === 'professional' ? 'Professional (39€/Monat)' : 'Lawyer Pro (69€/Monat)'} Tarif.
                  Nach Zahlung wird der Tarif automatisch aktiviert.
                </div>
              )}
            </div>
            
            <div className="mt-4 flex items-center gap-3">
              <input
                type="checkbox"
                id="newUserAdmin"
                checked={newUserForm.isAdmin}
                onChange={(e) => setNewUserForm({ ...newUserForm, isAdmin: e.target.checked })}
                className="rounded border-gray-300"
              />
              <label htmlFor="newUserAdmin" className="text-sm text-gray-700">
                👑 Als Admin anlegen (Zugriff auf Admin-Dashboard)
              </label>
            </div>
            
            <div className="mt-6 flex gap-3">
              <button
                onClick={handleCreateUser}
                disabled={creating || !newUserForm.email || !newUserForm.password || !newUserForm.name}
                className={`px-6 py-3 text-white rounded-lg font-medium transition-colors disabled:bg-gray-400 ${
                  newUserForm.accountType === 'paying' && newUserForm.tier !== 'free'
                    ? 'bg-green-600 hover:bg-green-700'
                    : 'bg-purple-600 hover:bg-purple-700'
                }`}
              >
                {creating ? '⏳ Wird erstellt...' : 
                  newUserForm.accountType === 'paying' && newUserForm.tier !== 'free'
                    ? '💳 User erstellen & Checkout-Link senden'
                    : '🧪 Test-Benutzer erstellen'
                }
              </button>
              <button
                onClick={() => setNewUserForm({ email: '', password: '', name: '', tier: 'free', isAdmin: false, accountType: 'test' })}
                className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
              >
                Formular leeren
              </button>
            </div>
            
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-700">
              <strong>ℹ️ Hinweis:</strong> Der Benutzer wird sowohl in Firebase Authentication 
              als auch in der Firestore-Datenbank erstellt und kann sich sofort anmelden.
              {newUserForm.accountType === 'test' && ' Test-Kunden sehen keine Upgrade-Optionen.'}
            </div>
          </div>
        )}

        {/* Messages Tab */}
        {activeTab === 'messages' && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">Nachricht an Benutzer senden</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Empfänger</label>
                <select
                  value={messageForm.recipient}
                  onChange={(e) => setMessageForm({ ...messageForm, recipient: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="all">📢 Alle Benutzer ({users.length})</option>
                  <optgroup label="Einzelne Benutzer">
                    {users.map(user => (
                      <option key={user.id} value={user.id}>{user.email} ({user.name})</option>
                    ))}
                  </optgroup>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Typ</label>
                <select
                  value={messageForm.type}
                  onChange={(e) => setMessageForm({ ...messageForm, type: e.target.value as any })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="info">ℹ️ Information</option>
                  <option value="success">✅ Erfolg</option>
                  <option value="warning">⚠️ Warnung</option>
                  <option value="admin">👑 Admin-Nachricht</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Titel</label>
                <input
                  type="text"
                  value={messageForm.title}
                  onChange={(e) => setMessageForm({ ...messageForm, title: e.target.value })}
                  placeholder="z.B. Wichtige Ankündigung"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nachricht</label>
                <textarea
                  value={messageForm.message}
                  onChange={(e) => setMessageForm({ ...messageForm, message: e.target.value })}
                  placeholder="Ihre Nachricht an die Benutzer..."
                  rows={5}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg resize-none"
                />
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="sendEmail"
                  checked={messageForm.sendEmail}
                  onChange={(e) => setMessageForm({ ...messageForm, sendEmail: e.target.checked })}
                  className="rounded border-gray-300"
                />
                <label htmlFor="sendEmail" className="text-sm text-gray-700">
                  Auch per E-Mail senden
                </label>
              </div>

              <button
                onClick={handleSendMessage}
                disabled={sending || !messageForm.title.trim() || !messageForm.message.trim()}
                className="w-full py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
              >
                {sending ? 'Wird gesendet...' : '📤 Nachricht senden'}
              </button>
            </div>
          </div>
        )}

        {/* Users Table */}
        {activeTab === 'users' && (
        <div className="space-y-6">
          {/* Filter/Controls */}
          <div className="bg-white rounded-lg shadow p-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Alle Benutzer ({users.length})</h2>
            <button
              onClick={loadData}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg"
            >
              🔄 Aktualisieren
            </button>
          </div>

          {/* Grouped by Category */}
          {[
            { key: 'lawyer', title: '⚖️ Lawyer Pro', filter: (u: User) => u.tier === 'lawyer' },
            { key: 'professional', title: '🏢 Professional', filter: (u: User) => u.tier === 'professional' },
            { key: 'basis', title: '🏠 Basis', filter: (u: User) => u.tier === 'basis' },
            { key: 'free_lawyer', title: '⚖️ Free Lawyer Pro', filter: (u: User) => u.tier === 'free_lawyer' || (u.tier === 'free' && u.dashboardType === 'lawyer') },
            { key: 'free_professional', title: '🏢 Free Professional', filter: (u: User) => u.tier === 'free_professional' || (u.tier === 'free' && u.dashboardType === 'professional') },
            { key: 'free_basis', title: '🏠 Free Basis', filter: (u: User) => u.tier === 'free_basis' || u.tier === 'free' && (!u.dashboardType || u.dashboardType === 'basis') },
          ].map(({ key, title, filter }) => {
            const categoryUsers = users.filter(filter);
            if (categoryUsers.length === 0) return null;
            
            return (
              <div key={key} className="bg-white rounded-lg shadow overflow-hidden">
                <div className="px-4 sm:px-6 py-3 bg-gray-50 border-b border-gray-200">
                  <h3 className="font-semibold text-gray-800">{title} ({categoryUsers.length})</h3>
                </div>
                
                {/* Mobile Card View */}
                <div className="block md:hidden divide-y divide-gray-200">
                  {categoryUsers.map((user) => {
                    const tierInfo = getTierDisplay(user.tier, user.dashboardType);
                    return (
                      <div key={user.id} className="p-4 space-y-3">
                        <div className="flex items-start justify-between">
                          <div className="flex-1 min-w-0">
                            <p className="font-medium text-gray-900 truncate">{user.name}</p>
                            <p className="text-sm text-gray-500 truncate">{user.email}</p>
                          </div>
                          {(user.isAdmin || DEFAULT_ADMIN_EMAILS.includes(user.email)) && (
                            <span className="ml-2 px-2 py-1 bg-red-100 text-red-700 text-xs rounded">👑</span>
                          )}
                        </div>
                        
                        <div className="flex flex-wrap gap-2 items-center">
                          <span className={`px-2 py-1 rounded text-xs font-medium ${tierInfo.color}`}>
                            {tierInfo.badge} {tierInfo.label}
                          </span>
                          <select
                            value={user.tier.startsWith('free') ? 'free' : user.tier}
                            onChange={(e) => handleChangeTier(user.id, e.target.value)}
                            className="text-xs border border-gray-300 rounded px-2 py-1"
                          >
                            <option value="free">Free</option>
                            <option value="basis">Basis</option>
                            <option value="professional">Professional</option>
                            <option value="lawyer">Lawyer Pro</option>
                          </select>
                        </div>
                        
                        <div 
                          className="cursor-pointer"
                          onClick={() => openQueryEditor(user)}
                        >
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Anfragen:</span>
                            <span className="font-medium text-blue-600">{user.queriesUsed} / {user.queriesLimit} ✏️</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${Math.min((user.queriesUsed / user.queriesLimit) * 100, 100)}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        <div className="flex justify-between items-center pt-2 border-t border-gray-100">
                          <span className="text-xs text-gray-500">
                            {new Date(user.createdAt).toLocaleDateString('de-DE')}
                          </span>
                          <div className="flex gap-3">
                            <button
                              onClick={() => openQueryEditor(user)}
                              className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                              title="Anfragen bearbeiten"
                            >
                              ✏️
                            </button>
                            <button
                              onClick={() => handleResetQueries(user.id)}
                              className="p-2 text-green-600 hover:bg-green-50 rounded"
                              title="Anfragen auf 0 zurücksetzen"
                            >
                              🔄
                            </button>
                            <button
                              onClick={() => handleToggleAdmin(user.id, user.email, user.isAdmin || false)}
                              className="p-2 text-yellow-600 hover:bg-yellow-50 rounded"
                              disabled={DEFAULT_ADMIN_EMAILS.includes(user.email)}
                              title="Admin-Status ändern"
                            >
                              👑
                            </button>
                            <button
                              onClick={() => handleDeleteUser(user.id)}
                              className="p-2 text-red-600 hover:bg-red-50 rounded"
                              title="Benutzer löschen"
                            >
                              🗑️
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
                
                {/* Desktop Table View */}
                <div className="hidden md:block overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Benutzer
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Tarif
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Admin
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Anfragen
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Erstellt am
                        </th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Aktionen
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {categoryUsers.map((user) => {
                        const tierInfo = getTierDisplay(user.tier, user.dashboardType);
                        return (
                          <tr key={user.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div>
                                <div className="text-sm font-medium text-gray-900">{user.name}</div>
                                <div className="text-sm text-gray-500">{user.email}</div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center gap-2">
                                <span className={`px-2 py-1 rounded text-xs font-medium ${tierInfo.color}`}>
                                  {tierInfo.badge} {tierInfo.label}
                                </span>
                                <select
                                  value={user.tier.startsWith('free') ? 'free' : user.tier}
                                  onChange={(e) => handleChangeTier(user.id, e.target.value)}
                                  className="text-xs border border-gray-300 rounded px-1 py-0.5"
                                >
                                  <option value="free">Free</option>
                                  <option value="basis">Basis</option>
                                  <option value="professional">Professional</option>
                                  <option value="lawyer">Lawyer Pro</option>
                                </select>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <button
                                onClick={() => handleToggleAdmin(user.id, user.email, user.isAdmin || false)}
                                className={`px-2 py-1 rounded text-xs font-medium ${
                                  user.isAdmin || DEFAULT_ADMIN_EMAILS.includes(user.email)
                                    ? 'bg-red-100 text-red-700'
                                    : 'bg-gray-100 text-gray-500'
                                }`}
                                disabled={DEFAULT_ADMIN_EMAILS.includes(user.email)}
                                title={DEFAULT_ADMIN_EMAILS.includes(user.email) ? 'Standard-Admin' : 'Admin-Status ändern'}
                              >
                                {user.isAdmin || DEFAULT_ADMIN_EMAILS.includes(user.email) ? '👑 Admin' : '—'}
                              </button>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div 
                                className="text-sm text-gray-900 cursor-pointer hover:text-blue-600"
                                onClick={() => openQueryEditor(user)}
                                title="Klicken zum Bearbeiten"
                              >
                                {user.queriesUsed} / {user.queriesLimit} ✏️
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                                <div
                                  className="bg-blue-600 h-1.5 rounded-full"
                                  style={{ width: `${Math.min((user.queriesUsed / user.queriesLimit) * 100, 100)}%` }}
                                ></div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {new Date(user.createdAt).toLocaleDateString('de-DE')}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                              <button
                                onClick={() => openQueryEditor(user)}
                                className="text-blue-600 hover:text-blue-900"
                                title="Anfragen bearbeiten"
                              >
                                ✏️
                              </button>
                              <button
                                onClick={() => handleResetQueries(user.id)}
                                className="text-green-600 hover:text-green-900"
                                title="Anfragen auf 0 zurücksetzen"
                              >
                                🔄
                              </button>
                              <button
                                onClick={() => handleDeleteUser(user.id)}
                                className="text-red-600 hover:text-red-900"
                                title="Benutzer löschen"
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
              </div>
            );
          })}
        </div>
        )}

        {/* Inactive Accounts Tab */}
        {activeTab === 'inactive' && (
          <div className="space-y-6">
            {/* Scheduled for Deletion */}
            {scheduledForDeletion.length > 0 && (
              <div className="bg-red-50 border border-red-200 rounded-lg shadow p-6">
                <h2 className="text-lg font-semibold text-red-800 mb-4">
                  🗑️ Zur Löschung vorgemerkt ({scheduledForDeletion.length})
                </h2>
                <div className="space-y-3">
                  {scheduledForDeletion.map(user => {
                    const deletionDate = new Date(user.scheduledDeletionAt!);
                    const daysLeft = Math.ceil((deletionDate.getTime() - Date.now()) / (24 * 60 * 60 * 1000));
                    return (
                      <div key={user.id} className="flex items-center justify-between bg-white p-4 rounded-lg">
                        <div>
                          <p className="font-medium text-gray-900">{user.email}</p>
                          <p className="text-sm text-red-600">
                            Löschung am {deletionDate.toLocaleDateString('de-DE')} ({daysLeft > 0 ? `noch ${daysLeft} Tage` : 'überfällig'})
                          </p>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => cancelDeletion(user.id)}
                            className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded"
                          >
                            ✓ Abbrechen
                          </button>
                          <button
                            onClick={() => deleteUserImmediately(user.id)}
                            className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded"
                          >
                            Jetzt löschen
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Inactive Free Users */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                ⚠️ Inaktive Free-Accounts (6+ Monate)
              </h2>
              <p className="text-sm text-gray-600 mb-4">
                Diese kostenlosen Accounts waren seit 6 oder mehr Monaten nicht aktiv.
              </p>
              
              {inactiveUsers.filter(u => !u.scheduledDeletionAt).length === 0 ? (
                <p className="text-gray-500 py-4 text-center">Keine inaktiven Accounts gefunden.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Benutzer</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Letzte Aktivität</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Inaktiv seit</th>
                        <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Aktionen</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {inactiveUsers.filter(u => !u.scheduledDeletionAt).map(user => {
                        const lastActivity = user.lastActivityAt ? new Date(user.lastActivityAt) : new Date(user.createdAt);
                        const inactiveDays = Math.floor((Date.now() - lastActivity.getTime()) / (24 * 60 * 60 * 1000));
                        return (
                          <tr key={user.id} className="hover:bg-gray-50">
                            <td className="px-4 py-3">
                              <p className="font-medium text-gray-900">{user.email}</p>
                              <p className="text-sm text-gray-500">{user.name || 'Kein Name'}</p>
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-600">
                              {lastActivity.toLocaleDateString('de-DE')}
                            </td>
                            <td className="px-4 py-3">
                              <span className="px-2 py-1 bg-orange-100 text-orange-700 text-sm rounded">
                                {inactiveDays} Tage
                              </span>
                            </td>
                            <td className="px-4 py-3 text-right space-x-2">
                              <button
                                onClick={() => scheduleUserDeletion(user.id, user.email, user.name || 'Nutzer')}
                                className="px-3 py-1 bg-orange-500 hover:bg-orange-600 text-white text-sm rounded"
                                title="7-Tage-Warnung senden und zur Löschung vormerken"
                              >
                                ⚠️ Vormerken
                              </button>
                              <button
                                onClick={() => deleteUserImmediately(user.id)}
                                className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded"
                                title="Sofort löschen"
                              >
                                🗑️ Löschen
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

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-800 mb-2">ℹ️ Löschungs-Workflow</h3>
              <ol className="text-sm text-blue-700 list-decimal list-inside space-y-1">
                <li>Klicken Sie &quot;Vormerken&quot; um eine 7-Tage-Warnung zu senden</li>
                <li>Der Benutzer erhält eine E-Mail und In-App-Benachrichtigung</li>
                <li>Nach 7 Tagen erscheint der Account in &quot;Zur Löschung vorgemerkt&quot;</li>
                <li>Führen Sie die finale Löschung manuell durch oder brechen Sie ab</li>
              </ol>
            </div>
          </div>
        )}

        {/* Delete Requests Tab */}
        {activeTab === 'delete-requests' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">🗑️ Account-Löschanfragen</h2>
            <p className="text-sm text-gray-600 mb-6">
              Hier sehen Sie alle Löschanfragen von Benutzern gemäß § 312k BGB.
            </p>
            
            {deleteRequests.length === 0 ? (
              <p className="text-gray-500 py-8 text-center">Keine Löschanfragen vorhanden.</p>
            ) : (
              <div className="space-y-4">
                {deleteRequests.map(request => {
                  const createdAt = request.createdAt?.toDate?.() || new Date(request.createdAt);
                  return (
                    <div 
                      key={request.id} 
                      className={`p-4 rounded-lg border ${
                        request.status === 'pending' 
                          ? 'bg-red-50 border-red-200' 
                          : 'bg-gray-50 border-gray-200'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-medium text-gray-900">{request.userEmail}</p>
                          <p className="text-sm text-gray-600">{request.userName}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            Anfrage vom {createdAt.toLocaleDateString('de-DE')} um {createdAt.toLocaleTimeString('de-DE')}
                          </p>
                          {request.reason && (
                            <p className="text-sm text-gray-700 mt-2 bg-white p-2 rounded">
                              <strong>Grund:</strong> {request.reason}
                            </p>
                          )}
                        </div>
                        <div className="flex flex-col gap-2">
                          {request.status === 'pending' ? (
                            <>
                              <span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded text-center">
                                Offen
                              </span>
                              <button
                                onClick={async () => {
                                  if (!confirm(`Account ${request.userEmail} wirklich löschen? Dies löscht auch den Firebase Auth User.`)) return;
                                  try {
                                    // Backend API aufrufen um User komplett zu löschen (Firestore + Auth)
                                    const response = await fetch(`${BACKEND_URL}/admin/delete-user/${request.userId}`, {
                                      method: 'DELETE',
                                      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                                      body: new URLSearchParams({ admin_email: currentUser?.email || '' }),
                                    });
                                    if (!response.ok) {
                                      const error = await response.json();
                                      throw new Error(error.detail || 'Fehler beim Löschen');
                                    }
                                    // Anfrage als erledigt markieren
                                    await updateDoc(doc(db, 'delete_requests', request.id), { status: 'completed' });
                                    await loadData();
                                    alert('Account komplett gelöscht (Firestore + Auth)!');
                                  } catch (err: any) {
                                    console.error(err);
                                    alert('Fehler beim Löschen: ' + (err.message || err));
                                  }
                                }}
                                className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-sm rounded"
                              >
                                Account löschen
                              </button>
                              <button
                                onClick={async () => {
                                  await updateDoc(doc(db, 'delete_requests', request.id), { status: 'completed' });
                                  await loadData();
                                }}
                                className="px-3 py-1 bg-gray-500 hover:bg-gray-600 text-white text-sm rounded"
                              >
                                Abschließen
                              </button>
                            </>
                          ) : (
                            <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded text-center">
                              Erledigt
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Billing Tab */}
        {activeTab === 'billing' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">📊 Vorbereitende Buchhaltung</h2>
              <button
                onClick={loadBillingData}
                disabled={loadingBilling}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium disabled:opacity-50"
              >
                {loadingBilling ? '⏳ Lädt...' : '🔄 Aktualisieren'}
              </button>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-lg shadow p-4">
                <p className="text-sm text-gray-600">Gesamt Rechnungen</p>
                <p className="text-2xl font-bold text-green-600">{invoices.length}</p>
              </div>
              <div className="bg-white rounded-lg shadow p-4">
                <p className="text-sm text-gray-600">Bezahlt</p>
                <p className="text-2xl font-bold text-blue-600">
                  {invoices.filter(i => i.status === 'paid').length}
                </p>
              </div>
              <div className="bg-white rounded-lg shadow p-4">
                <p className="text-sm text-gray-600">Offen</p>
                <p className="text-2xl font-bold text-amber-600">
                  {invoices.filter(i => i.status === 'open').length}
                </p>
              </div>
              <div className="bg-white rounded-lg shadow p-4">
                <p className="text-sm text-gray-600">Gutschriften</p>
                <p className="text-2xl font-bold text-purple-600">{creditNotes.length}</p>
              </div>
            </div>

            {/* Total Revenue */}
            <div className="bg-gradient-to-r from-green-600 to-green-700 rounded-lg shadow p-6 text-white">
              <p className="text-lg opacity-90">Gesamtumsatz (bezahlt)</p>
              <p className="text-4xl font-bold mt-1">
                {invoices.filter(i => i.status === 'paid')
                  .reduce((sum, i) => sum + i.amount_paid, 0)
                  .toFixed(2)} €
              </p>
            </div>

            {/* Invoices Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="p-4 border-b border-gray-200 bg-gray-50">
                <h3 className="font-semibold text-gray-900">📄 Rechnungen</h3>
              </div>
              
              {invoices.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  <p>Keine Rechnungen gefunden.</p>
                  <button
                    onClick={loadBillingData}
                    className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg"
                  >
                    Rechnungen laden
                  </button>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-100">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rechnung</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kunde</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Betrag</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Datum</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aktionen</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {invoices.map((invoice) => (
                        <tr key={invoice.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3">
                            <span className="font-mono text-sm">{invoice.number || invoice.id.slice(0, 12)}</span>
                          </td>
                          <td className="px-4 py-3">
                            <div>
                              <p className="text-sm font-medium">{invoice.customer_email}</p>
                              {invoice.customer_name && (
                                <p className="text-xs text-gray-500">{invoice.customer_name}</p>
                              )}
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <span className="font-medium">{invoice.amount_paid.toFixed(2)} €</span>
                          </td>
                          <td className="px-4 py-3">
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              invoice.status === 'paid' ? 'bg-green-100 text-green-700' :
                              invoice.status === 'open' ? 'bg-amber-100 text-amber-700' :
                              invoice.status === 'void' ? 'bg-gray-100 text-gray-700' :
                              'bg-red-100 text-red-700'
                            }`}>
                              {invoice.status === 'paid' ? '✅ Bezahlt' :
                               invoice.status === 'open' ? '⏳ Offen' :
                               invoice.status === 'void' ? '⛔ Storniert' :
                               invoice.status}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {formatUnixDate(invoice.created)}
                          </td>
                          <td className="px-4 py-3">
                            <div className="flex gap-2">
                              {invoice.invoice_pdf && (
                                <a
                                  href={invoice.invoice_pdf}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded hover:bg-blue-200"
                                >
                                  📄 PDF
                                </a>
                              )}
                              {invoice.status === 'paid' && (
                                <button
                                  onClick={() => handleRefundInvoice(invoice.id)}
                                  className="px-2 py-1 bg-amber-100 text-amber-700 text-xs rounded hover:bg-amber-200"
                                >
                                  ↩️ Erstatten
                                </button>
                              )}
                              {invoice.status === 'open' && (
                                <button
                                  onClick={() => handleVoidInvoice(invoice.id)}
                                  className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded hover:bg-red-200"
                                >
                                  ⛔ Stornieren
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Credit Notes */}
            {creditNotes.length > 0 && (
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <div className="p-4 border-b border-gray-200 bg-purple-50">
                  <h3 className="font-semibold text-purple-900">📋 Gutschriften / Stornos</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-100">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nr.</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kunde</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Betrag</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Grund</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Datum</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">PDF</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {creditNotes.map((cn) => (
                        <tr key={cn.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 font-mono text-sm">{cn.number || cn.id.slice(0, 12)}</td>
                          <td className="px-4 py-3 text-sm">{cn.customer_email}</td>
                          <td className="px-4 py-3 font-medium text-purple-600">-{cn.amount.toFixed(2)} €</td>
                          <td className="px-4 py-3 text-sm text-gray-600">{cn.memo || cn.reason || '-'}</td>
                          <td className="px-4 py-3 text-sm text-gray-600">{formatUnixDate(cn.created)}</td>
                          <td className="px-4 py-3">
                            {cn.pdf && (
                              <a
                                href={cn.pdf}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded hover:bg-purple-200"
                              >
                                📄 PDF
                              </a>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Info Box */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-800 mb-2">ℹ️ Automatische Buchhaltung</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Rechnungen werden automatisch von Stripe bei jeder Zahlung erstellt</li>
                <li>• Bei Widerruf: &quot;Erstatten&quot; erstellt automatisch eine Gutschrift</li>
                <li>• Alle PDFs können direkt heruntergeladen werden</li>
                <li>• E-Mails werden automatisch an Kunden versendet (Bestellung, Storno)</li>
              </ul>
            </div>
          </div>
        )}

        {/* Email Config Tab */}
        {activeTab === 'email' && (
          <div className="space-y-6">
            {/* Email Tab Navigation */}
            <div className="flex gap-2 border-b border-gray-200 pb-4">
              <button
                onClick={() => { setEmailTab('inbox'); loadEmails(currentFolder); }}
                className={`px-4 py-2 rounded-t-lg font-medium transition ${
                  emailTab === 'inbox' 
                    ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-600' 
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📥 Posteingang {unreadCount > 0 && <span className="ml-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">{unreadCount}</span>}
              </button>
              <button
                onClick={() => setEmailTab('compose')}
                className={`px-4 py-2 rounded-t-lg font-medium transition ${
                  emailTab === 'compose' 
                    ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-600' 
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                ✏️ Neue E-Mail
              </button>
              <button
                onClick={() => setEmailTab('templates')}
                className={`px-4 py-2 rounded-t-lg font-medium transition ${
                  emailTab === 'templates' 
                    ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-600' 
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📋 Vorlagen
              </button>
              <button
                onClick={() => setEmailTab('config')}
                className={`px-4 py-2 rounded-t-lg font-medium transition ${
                  emailTab === 'config' 
                    ? 'bg-purple-100 text-purple-700 border-b-2 border-purple-600' 
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                ⚙️ Einstellungen
              </button>
            </div>

            {/* INBOX Tab */}
            {emailTab === 'inbox' && (
              <div className="bg-white rounded-lg shadow">
                {/* Folder Bar */}
                <div className="flex items-center gap-2 p-3 border-b bg-gray-50">
                  {['INBOX', 'Sent', 'Drafts', 'Trash'].map((folder) => (
                    <button
                      key={folder}
                      onClick={() => loadEmails(folder.toUpperCase())}
                      className={`px-3 py-1.5 text-sm rounded-md transition ${
                        currentFolder === folder.toUpperCase()
                          ? 'bg-purple-600 text-white'
                          : 'bg-white border text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      {folder === 'INBOX' && '📥 '}
                      {folder === 'Sent' && '📤 '}
                      {folder === 'Drafts' && '📝 '}
                      {folder === 'Trash' && '🗑️ '}
                      {folder}
                    </button>
                  ))}
                  <button
                    onClick={() => loadEmails(currentFolder)}
                    className="ml-auto px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 rounded-md"
                    disabled={loadingEmails}
                  >
                    {loadingEmails ? '⏳' : '🔄'} Aktualisieren
                  </button>
                </div>

                {/* Email Detail View */}
                {selectedEmail ? (
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <button
                        onClick={() => setSelectedEmail(null)}
                        className="text-gray-600 hover:text-gray-800 flex items-center gap-1"
                      >
                        ← Zurück
                      </button>
                      <div className="flex gap-2">
                        <button
                          onClick={() => replyToEmail(selectedEmail)}
                          className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700"
                        >
                          ↩️ Antworten
                        </button>
                        <button
                          onClick={() => deleteEmail(selectedEmail.id)}
                          className="px-3 py-1.5 bg-red-600 text-white text-sm rounded-md hover:bg-red-700"
                        >
                          🗑️ Löschen
                        </button>
                      </div>
                    </div>
                    
                    <div className="border rounded-lg overflow-hidden">
                      <div className="bg-gray-50 p-4 border-b">
                        <h2 className="text-xl font-semibold text-gray-900 mb-2">{selectedEmail.subject || '(Kein Betreff)'}</h2>
                        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                          <span><strong>Von:</strong> {selectedEmail.from || selectedEmail.from_name || selectedEmail.sender || 'Unbekannt'}</span>
                          <span><strong>Datum:</strong> {selectedEmail.date || ''}</span>
                        </div>
                        {selectedEmail.to && (
                          <div className="text-sm text-gray-600 mt-1">
                            <strong>An:</strong> {Array.isArray(selectedEmail.to) ? selectedEmail.to.join(', ') : selectedEmail.to}
                          </div>
                        )}
                      </div>
                      <div className="p-4 bg-white max-h-[60vh] overflow-auto">
                        {selectedEmail.body_html ? (
                          <div 
                            className="prose max-w-none"
                            dangerouslySetInnerHTML={{ __html: selectedEmail.body_html }}
                          />
                        ) : (
                          <pre className="whitespace-pre-wrap font-sans text-gray-800">{selectedEmail.body_text || selectedEmail.body || 'Kein Inhalt'}</pre>
                        )}
                      </div>
                    </div>
                  </div>
                ) : (
                  /* Email List */
                  <div className="divide-y">
                    {loadingEmails ? (
                      <div className="p-8 text-center text-gray-500">
                        <div className="animate-spin text-4xl mb-2">⏳</div>
                        E-Mails werden geladen...
                      </div>
                    ) : emails.length === 0 ? (
                      <div className="p-8 text-center text-gray-500">
                        <div className="text-4xl mb-2">📭</div>
                        {emailConfig.configured ? 'Keine E-Mails im ' + currentFolder : 'E-Mail nicht konfiguriert'}
                      </div>
                    ) : (
                      emails.map((email) => (
                        <div
                          key={email.id}
                          onClick={() => openEmail(email)}
                          className={`p-4 cursor-pointer hover:bg-gray-50 transition ${
                            !email.is_read ? 'bg-blue-50 font-semibold' : ''
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2">
                                {!email.is_read && <span className="w-2 h-2 bg-blue-600 rounded-full"></span>}
                                <span className="text-gray-900 truncate">{email.from_name || email.sender}</span>
                              </div>
                              <p className={`text-gray-800 truncate ${!email.is_read ? 'font-semibold' : ''}`}>
                                {email.subject || '(Kein Betreff)'}
                              </p>
                              <p className="text-sm text-gray-500 truncate">
                                {(email.body_text || email.snippet || '').substring(0, 100)}...
                              </p>
                            </div>
                            <div className="ml-4 text-sm text-gray-500 whitespace-nowrap">
                              {email.date}
                            </div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>
            )}

            {/* COMPOSE Tab */}
            {emailTab === 'compose' && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                  ✏️ Neue E-Mail verfassen
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">An</label>
                    <input
                      type="email"
                      value={composeForm.to}
                      onChange={(e) => setComposeForm({ ...composeForm, to: e.target.value })}
                      placeholder="empfaenger@example.de"
                      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Betreff</label>
                    <input
                      type="text"
                      value={composeForm.subject}
                      onChange={(e) => setComposeForm({ ...composeForm, subject: e.target.value })}
                      placeholder="Betreff eingeben..."
                      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <label className="block text-sm font-medium text-gray-700">Nachricht</label>
                      <label className="flex items-center gap-2 text-sm text-gray-600">
                        <input
                          type="checkbox"
                          checked={composeForm.html}
                          onChange={(e) => setComposeForm({ ...composeForm, html: e.target.checked })}
                          className="rounded"
                        />
                        HTML-Template verwenden
                      </label>
                    </div>
                    <textarea
                      value={composeForm.body}
                      onChange={(e) => setComposeForm({ ...composeForm, body: e.target.value })}
                      placeholder="Ihre Nachricht..."
                      rows={12}
                      className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 font-mono text-sm"
                    />
                    {composeForm.html && (
                      <p className="mt-1 text-xs text-gray-500">
                        ✨ Ihre Nachricht wird automatisch in das domulex.ai Template eingefügt (Logo, Signatur, Footer)
                      </p>
                    )}
                  </div>
                  
                  <div className="flex gap-3 pt-4">
                    <button
                      onClick={sendEmail}
                      disabled={sendingEmail || !composeForm.to || !composeForm.subject}
                      className="px-6 py-2.5 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                    >
                      {sendingEmail ? '⏳ Wird gesendet...' : '📤 E-Mail senden'}
                    </button>
                    <button
                      onClick={() => setComposeForm({ to: '', subject: '', body: '', html: true })}
                      className="px-6 py-2.5 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                    >
                      🗑️ Verwerfen
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* TEMPLATES Tab */}
            {emailTab === 'templates' && (
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                  📋 E-Mail-Vorlagen versenden
                </h2>
                
                <p className="text-gray-600 mb-6">
                  Hier können Sie vordefinierte E-Mail-Vorlagen direkt versenden. Die Vorlagen enthalten das domulex.ai Branding mit Logo und Signatur.
                </p>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Template Selection */}
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Vorlage auswählen</label>
                      <select
                        value={selectedTemplate}
                        onChange={(e) => setSelectedTemplate(e.target.value)}
                        className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500 bg-white"
                      >
                        <option value="welcome">👋 Willkommens-E-Mail</option>
                        <option value="order_confirmation">✅ Bestellbestätigung</option>
                        <option value="payment_failed">⚠️ Zahlungsproblem</option>
                        <option value="subscription_cancelled">📝 Kündigungsbestätigung</option>
                        <option value="tier_change">🔄 Abo-Änderung</option>
                        <option value="deletion_reminder">⚠️ Löschwarnung (7 Tage)</option>
                        <option value="admin_notification">👑 Admin-Benachrichtigung</option>
                        <option value="order_confirmation_b2b">🏢 Bestellbestätigung (B2B)</option>
                        <option value="test">🧪 Test-E-Mail</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Empfänger *</label>
                      <input
                        type="email"
                        value={templateRecipient}
                        onChange={(e) => setTemplateRecipient(e.target.value)}
                        placeholder="empfaenger@example.de"
                        className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>

                    {/* Dynamic Parameters based on template */}
                    {selectedTemplate !== 'test' && (
                      <>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Name des Empfängers</label>
                          <input
                            type="text"
                            value={templateParams.user_name}
                            onChange={(e) => setTemplateParams({ ...templateParams, user_name: e.target.value })}
                            className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>

                        {(selectedTemplate === 'order_confirmation' || selectedTemplate === 'order_confirmation_b2b') && (
                          <>
                            <div className="grid grid-cols-2 gap-3">
                              <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Tarif</label>
                                <input
                                  type="text"
                                  value={templateParams.plan_name}
                                  onChange={(e) => setTemplateParams({ ...templateParams, plan_name: e.target.value })}
                                  className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                />
                              </div>
                              <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Preis (€)</label>
                                <input
                                  type="text"
                                  value={templateParams.plan_price}
                                  onChange={(e) => setTemplateParams({ ...templateParams, plan_price: e.target.value })}
                                  className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                />
                              </div>
                            </div>
                            {selectedTemplate === 'order_confirmation_b2b' && (
                              <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Firmenname</label>
                                <input
                                  type="text"
                                  value={templateParams.company_name}
                                  onChange={(e) => setTemplateParams({ ...templateParams, company_name: e.target.value })}
                                  className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                                />
                              </div>
                            )}
                          </>
                        )}

                        {selectedTemplate === 'subscription_cancelled' && (
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Enddatum</label>
                            <input
                              type="text"
                              value={templateParams.end_date}
                              onChange={(e) => setTemplateParams({ ...templateParams, end_date: e.target.value })}
                              placeholder="z.B. 31.01.2026"
                              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                            />
                          </div>
                        )}

                        {selectedTemplate === 'tier_change' && (
                          <div className="grid grid-cols-2 gap-3">
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-2">Neuer Tarif</label>
                              <input
                                type="text"
                                value={templateParams.new_tier}
                                onChange={(e) => setTemplateParams({ ...templateParams, new_tier: e.target.value })}
                                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-2">Anfragen/Monat</label>
                              <input
                                type="text"
                                value={templateParams.queries_limit}
                                onChange={(e) => setTemplateParams({ ...templateParams, queries_limit: e.target.value })}
                                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                              />
                            </div>
                          </div>
                        )}

                        {selectedTemplate === 'admin_notification' && (
                          <>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-2">Titel</label>
                              <input
                                type="text"
                                value={templateParams.title}
                                onChange={(e) => setTemplateParams({ ...templateParams, title: e.target.value })}
                                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-2">Nachricht</label>
                              <textarea
                                value={templateParams.message}
                                onChange={(e) => setTemplateParams({ ...templateParams, message: e.target.value })}
                                rows={4}
                                className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                              />
                            </div>
                          </>
                        )}

                        {selectedTemplate === 'deletion_reminder' && (
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Löschdatum</label>
                            <input
                              type="text"
                              value={templateParams.end_date}
                              onChange={(e) => setTemplateParams({ ...templateParams, end_date: e.target.value })}
                              placeholder="z.B. 11.01.2026"
                              className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-purple-500"
                            />
                          </div>
                        )}
                      </>
                    )}

                    {/* Send Button */}
                    <div className="pt-4">
                      <button
                        onClick={async () => {
                          if (!templateRecipient) {
                            setTemplateResult({ success: false, message: 'Bitte Empfänger eingeben' });
                            return;
                          }
                          setSendingTemplate(true);
                          setTemplateResult(null);
                          try {
                            const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/admin/email/send-template`, {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({
                                template_name: selectedTemplate,
                                to: templateRecipient,
                                params: templateParams,
                              }),
                            });
                            const data = await response.json();
                            if (response.ok) {
                              setTemplateResult({ success: true, message: data.message || 'E-Mail erfolgreich versendet!' });
                            } else {
                              setTemplateResult({ success: false, message: data.detail || 'Fehler beim Versenden' });
                            }
                          } catch (error: any) {
                            setTemplateResult({ success: false, message: error.message || 'Netzwerkfehler' });
                          }
                          setSendingTemplate(false);
                        }}
                        disabled={sendingTemplate || !templateRecipient}
                        className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                      >
                        {sendingTemplate ? '⏳ Wird gesendet...' : '📤 Vorlage versenden'}
                      </button>
                    </div>

                    {/* Result Message */}
                    {templateResult && (
                      <div className={`p-4 rounded-lg ${templateResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                        <p className={`font-medium ${templateResult.success ? 'text-green-800' : 'text-red-800'}`}>
                          {templateResult.success ? '✅' : '❌'} {templateResult.message}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Template Preview */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-3">Vorlagen-Info</h3>
                    <div className="space-y-4 text-sm text-gray-600">
                      {selectedTemplate === 'welcome' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">👋 Willkommens-E-Mail</p>
                          <p>Wird automatisch bei Registrierung gesendet. Enthält:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Begrüßung mit Namen</li>
                            <li>Info über Test-Tarif (3 Anfragen)</li>
                            <li>Link zur App</li>
                            <li>Hinweis auf Upgrade</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'order_confirmation' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">✅ Bestellbestätigung</p>
                          <p>Wird bei erfolgreicher Zahlung gesendet. Enthält:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Tarifname und Preis</li>
                            <li>Abo-ID</li>
                            <li>Widerrufsbelehrung</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'payment_failed' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">⚠️ Zahlungsproblem</p>
                          <p>Wird bei fehlgeschlagener Zahlung gesendet:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Warnung über Zahlungsproblem</li>
                            <li>Link zu Kontoeinstellungen</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'subscription_cancelled' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">📝 Kündigungsbestätigung</p>
                          <p>Wird bei Kündigung gesendet:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Enddatum des Abos</li>
                            <li>Info über Test-Tarif danach</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'test' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">🧪 Test-E-Mail</p>
                          <p>Einfache Test-E-Mail um die Konfiguration zu prüfen.</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Zeigt SMTP-Status</li>
                            <li>Listet automatische E-Mails</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'tier_change' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">🔄 Abo-Änderung</p>
                          <p>Wird bei Tarifwechsel gesendet:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Neuer Tarifname</li>
                            <li>Anfragen pro Monat</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'deletion_reminder' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">⚠️ Löschwarnung</p>
                          <p>Wird 7 Tage vor Kontolöschung gesendet:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Löschdatum</li>
                            <li>Anleitung zum Behalten</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'admin_notification' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">👑 Admin-Benachrichtigung</p>
                          <p>Individuelle Nachricht an Benutzer:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Freier Titel</li>
                            <li>Freie Nachricht</li>
                          </ul>
                        </div>
                      )}
                      {selectedTemplate === 'order_confirmation_b2b' && (
                        <div className="space-y-2">
                          <p className="font-medium text-gray-800">🏢 Bestellbestätigung (B2B)</p>
                          <p>Für Geschäftskunden:</p>
                          <ul className="list-disc list-inside ml-2">
                            <li>Firmenname</li>
                            <li>Netto-Preise mit MwSt.</li>
                            <li>Links zu AVV, NDA, AGB</li>
                          </ul>
                        </div>
                      )}

                      <div className="mt-4 p-3 bg-purple-50 rounded-lg">
                        <p className="text-purple-800 font-medium text-xs">
                          ✨ Alle E-Mails enthalten automatisch das domulex.ai Logo, Signatur und rechtliche Angaben.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* CONFIG Tab */}
            {emailTab === 'config' && (
              <>
                <div className="bg-white rounded-lg shadow p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
                    ⚙️ E-Mail-Konfiguration (Strato SMTP)
                  </h2>

                  {/* Status */}
                  <div className={`mb-6 p-4 rounded-lg ${emailConfig.configured ? 'bg-green-50 border border-green-200' : 'bg-yellow-50 border border-yellow-200'}`}>
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{emailConfig.configured ? '✅' : '⚠️'}</span>
                      <div>
                        <p className={`font-medium ${emailConfig.configured ? 'text-green-800' : 'text-yellow-800'}`}>
                          {emailConfig.configured ? 'E-Mail-Versand aktiv' : 'E-Mail nicht konfiguriert'}
                        </p>
                        {emailConfig.configured && (
                          <p className="text-sm text-green-600">
                            Server: {emailConfig.smtp_host}:{emailConfig.smtp_port} • Absender: {emailConfig.from_email}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Config Form */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">SMTP Server</label>
                      <input
                        type="text"
                        value={emailConfig.smtp_host}
                        onChange={(e) => setEmailConfig({ ...emailConfig, smtp_host: e.target.value })}
                        placeholder="smtp.strato.de"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">SMTP Port</label>
                      <select
                        value={emailConfig.smtp_port}
                        onChange={(e) => setEmailConfig({ 
                          ...emailConfig, 
                          smtp_port: parseInt(e.target.value),
                          use_ssl: parseInt(e.target.value) === 465
                        })}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value={465}>465 (SSL)</option>
                        <option value={587}>587 (STARTTLS)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Benutzername (E-Mail)</label>
                      <input
                        type="email"
                        value={emailConfig.smtp_user}
                        onChange={(e) => setEmailConfig({ ...emailConfig, smtp_user: e.target.value })}
                        placeholder="info@domulex.ai"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Passwort</label>
                      <input
                        type="password"
                        value={emailConfig.smtp_password}
                        onChange={(e) => setEmailConfig({ ...emailConfig, smtp_password: e.target.value })}
                        placeholder="••••••••"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Absender-E-Mail</label>
                      <input
                        type="email"
                        value={emailConfig.from_email}
                        onChange={(e) => setEmailConfig({ ...emailConfig, from_email: e.target.value })}
                        placeholder="info@domulex.ai"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Absender-Name</label>
                      <input
                        type="text"
                        value={emailConfig.from_name}
                        onChange={(e) => setEmailConfig({ ...emailConfig, from_name: e.target.value })}
                        placeholder="domulex.ai"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                  </div>

                  {/* Save Button */}
                  <div className="mt-6 flex gap-4">
                    <button
                      onClick={async () => {
                        setEmailLoading(true);
                        try {
                          const formData = new URLSearchParams();
                          formData.append('smtp_host', emailConfig.smtp_host);
                          formData.append('smtp_port', emailConfig.smtp_port.toString());
                          formData.append('smtp_user', emailConfig.smtp_user);
                          formData.append('smtp_password', emailConfig.smtp_password);
                          formData.append('from_email', emailConfig.from_email);
                          formData.append('from_name', emailConfig.from_name);
                          formData.append('use_ssl', emailConfig.use_ssl.toString());

                          const response = await fetch(`${BACKEND_URL}/admin/email/config`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: formData,
                          });
                          const data = await response.json();
                          if (data.success) {
                            setEmailConfig({ ...emailConfig, configured: true });
                            setEmailTestResult({ success: true, message: 'Konfiguration gespeichert!' });
                          } else {
                            throw new Error(data.detail || 'Fehler beim Speichern');
                          }
                        } catch (err: any) {
                          setEmailTestResult({ success: false, message: err.message });
                        } finally {
                          setEmailLoading(false);
                        }
                      }}
                      disabled={emailLoading || !emailConfig.smtp_user || !emailConfig.smtp_password}
                      className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {emailLoading ? '⏳ Speichern...' : '💾 Konfiguration speichern'}
                    </button>
                    <button
                      onClick={async () => {
                        setEmailLoading(true);
                        try {
                          const response = await fetch(`${BACKEND_URL}/admin/email/test-connection`, {
                            method: 'POST',
                          });
                          const data = await response.json();
                          setEmailTestResult(data);
                        } catch (err: any) {
                          setEmailTestResult({ success: false, message: err.message });
                        } finally {
                          setEmailLoading(false);
                        }
                      }}
                      disabled={emailLoading}
                      className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50"
                    >
                      🔌 Verbindung testen
                    </button>
                  </div>

                  {/* Test Result */}
                  {emailTestResult && (
                    <div className={`mt-4 p-4 rounded-lg ${emailTestResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                      <span className="mr-2">{emailTestResult.success ? '✅' : '❌'}</span>
                      {emailTestResult.message}
                    </div>
                  )}
                </div>

                {/* Test Email */}
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📨 Test-E-Mail senden</h3>
                  <div className="flex gap-4">
                    <input
                      type="email"
                      value={testEmailAddress}
                      onChange={(e) => setTestEmailAddress(e.target.value)}
                      placeholder="test@example.de"
                      className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <button
                      onClick={async () => {
                        if (!testEmailAddress) return;
                        setEmailLoading(true);
                        try {
                          const formData = new URLSearchParams();
                          formData.append('to_email', testEmailAddress);
                          const response = await fetch(`${BACKEND_URL}/admin/email/send-test`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: formData,
                          });
                          const data = await response.json();
                          if (response.ok) {
                            setEmailTestResult({ success: true, message: `Test-E-Mail an ${testEmailAddress} gesendet!` });
                          } else {
                            throw new Error(data.detail || 'Fehler beim Senden');
                          }
                        } catch (err: any) {
                          setEmailTestResult({ success: false, message: err.message });
                        } finally {
                          setEmailLoading(false);
                        }
                      }}
                      disabled={emailLoading || !testEmailAddress || !emailConfig.configured}
                      className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      📤 Test senden
                    </button>
                  </div>
                  {!emailConfig.configured && (
                    <p className="mt-2 text-sm text-yellow-600">⚠️ Zuerst die SMTP-Konfiguration speichern</p>
                  )}
                </div>

                {/* Info */}
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <h4 className="font-semibold text-purple-800 mb-2">📧 Strato SMTP-Einstellungen</h4>
                  <ul className="text-sm text-purple-700 space-y-1">
                    <li>• <strong>SMTP:</strong> smtp.strato.de (Port 465 SSL)</li>
                    <li>• <strong>IMAP:</strong> imap.strato.de (Port 993 SSL)</li>
                    <li>• <strong>Benutzername:</strong> Ihre vollständige E-Mail-Adresse</li>
                    <li>• Die Konfiguration wird verschlüsselt in Firestore gespeichert</li>
                  </ul>
                </div>

                {/* Automatic Emails Info */}
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-800 mb-2">📋 Automatische E-Mails mit Branding</h4>
                  <p className="text-sm text-gray-600 mb-3">Alle automatischen E-Mails enthalten: Logo, Unternehmensdaten, Signatur "Ihr domulex.ai Team"</p>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                    <div className="bg-white p-3 rounded border">
                      <span className="text-lg">👋</span>
                      <p className="font-medium">Willkommen</p>
                      <p className="text-gray-500 text-xs">Bei Registrierung</p>
                    </div>
                    <div className="bg-white p-3 rounded border">
                      <span className="text-lg">✅</span>
                      <p className="font-medium">Bestellbestätigung</p>
                      <p className="text-gray-500 text-xs">Nach Zahlung</p>
                    </div>
                    <div className="bg-white p-3 rounded border">
                      <span className="text-lg">⚠️</span>
                      <p className="font-medium">Zahlungsproblem</p>
                      <p className="text-gray-500 text-xs">Bei fehlgeschlagener Zahlung</p>
                    </div>
                    <div className="bg-white p-3 rounded border">
                      <span className="text-lg">📝</span>
                      <p className="font-medium">Kündigung</p>
                      <p className="text-gray-500 text-xs">Bestätigung</p>
                    </div>
                    <div className="bg-white p-3 rounded border">
                      <span className="text-lg">👑</span>
                      <p className="font-medium">Admin-Nachricht</p>
                      <p className="text-gray-500 text-xs">Benachrichtigungen</p>
                    </div>
                    <div className="bg-white p-3 rounded border">
                      <span className="text-lg">🏢</span>
                      <p className="font-medium">B2B-Bestellung</p>
                      <p className="text-gray-500 text-xs">Mit AVV/NDA</p>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {/* Usage Tab - Lawyer Nutzungskontrolle */}
        {activeTab === 'usage' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">📈 Nutzungsübersicht - Missbrauchskontrolle</h2>
            
            <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <p className="text-amber-800">
                <strong>Fair-Use-Limit:</strong> Lawyer Pro hat ein Fair-Use-Kontingent von 2.000 Anfragen pro Monat. 
                Überschreitungen können auf Account-Sharing hinweisen.
              </p>
            </div>
            
            {/* Lawyer Users Table */}
            <h3 className="font-semibold text-gray-800 mb-4">⚖️ Lawyer Pro Nutzer - Anfragenübersicht</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="text-left p-4 font-medium text-gray-700">Benutzer</th>
                    <th className="text-left p-4 font-medium text-gray-700">E-Mail</th>
                    <th className="text-right p-4 font-medium text-gray-700">Anfragen</th>
                    <th className="text-center p-4 font-medium text-gray-700">Status</th>
                    <th className="text-left p-4 font-medium text-gray-700">Letzte Aktivität</th>
                  </tr>
                </thead>
                <tbody>
                  {users
                    .filter(u => u.tier === 'lawyer')
                    .sort((a, b) => (b.queriesUsed || 0) - (a.queriesUsed || 0))
                    .map(user => (
                      <tr key={user.id} className={`border-t ${(user.queriesUsed || 0) > 2000 ? 'bg-red-50' : ''}`}>
                        <td className="p-4">
                          <p className="font-medium">{user.name || 'Kein Name'}</p>
                        </td>
                        <td className="p-4 text-gray-600">{user.email}</td>
                        <td className="p-4 text-right">
                          <span className={`font-bold ${(user.queriesUsed || 0) > 2000 ? 'text-red-600' : (user.queriesUsed || 0) > 1500 ? 'text-amber-600' : 'text-green-600'}`}>
                            {user.queriesUsed || 0}
                          </span>
                          <span className="text-gray-400"> / 2.000</span>
                        </td>
                        <td className="p-4 text-center">
                          {(user.queriesUsed || 0) > 2000 ? (
                            <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-sm">⚠️ Überschritten</span>
                          ) : (user.queriesUsed || 0) > 1500 ? (
                            <span className="px-2 py-1 bg-amber-100 text-amber-700 rounded-full text-sm">⚡ Hohe Nutzung</span>
                          ) : (
                            <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-sm">✅ Normal</span>
                          )}
                        </td>
                        <td className="p-4 text-gray-500 text-sm">
                          {user.lastActivityAt ? new Date(user.lastActivityAt).toLocaleDateString('de-DE') : 'Unbekannt'}
                        </td>
                      </tr>
                    ))}
                  {users.filter(u => u.tier === 'lawyer').length === 0 && (
                    <tr>
                      <td colSpan={5} className="p-8 text-center text-gray-500">
                        Keine Lawyer Pro Nutzer vorhanden
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            
            {/* Usage by Tier Summary */}
            <h3 className="font-semibold text-gray-800 mt-8 mb-4">📊 Nutzung nach Tarif</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {['free', 'basis', 'professional', 'lawyer'].map(tier => {
                const tierUsers = users.filter(u => u.tier === tier || (tier === 'free' && u.tier?.startsWith('free_')));
                const tierQueries = tierUsers.reduce((sum, u) => sum + (u.queriesUsed || 0), 0);
                const avgQueries = tierUsers.length > 0 ? Math.round(tierQueries / tierUsers.length) : 0;
                const limits: Record<string, number> = { free: 3, basis: 25, professional: 250, lawyer: 2000 };
                return (
                  <div key={tier} className="p-4 bg-gray-50 rounded-lg">
                    <p className="font-semibold text-gray-800 capitalize">{tier === 'free' ? 'Free' : tier}</p>
                    <p className="text-2xl font-bold text-gray-900">{tierUsers.length}</p>
                    <p className="text-sm text-gray-500">Nutzer</p>
                    <div className="mt-2 pt-2 border-t">
                      <p className="text-sm">Ø {avgQueries} / {limits[tier]} Anfragen</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Query Edit Modal */}
      {editingQueryUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              ✏️ Anfragen bearbeiten
            </h3>
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                <strong>Benutzer:</strong> {editingQueryUser.name} ({editingQueryUser.email})
              </p>
              <p className="text-sm text-gray-600">
                <strong>Aktuell:</strong> {editingQueryUser.queriesUsed} / {editingQueryUser.queriesLimit} Anfragen
              </p>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Neue Anzahl verbrauchter Anfragen:
              </label>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setNewQueryCount(Math.max(0, newQueryCount - 1))}
                  className="px-3 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-lg font-bold"
                >
                  −
                </button>
                <input
                  type="number"
                  value={newQueryCount}
                  onChange={(e) => setNewQueryCount(Math.max(0, parseInt(e.target.value) || 0))}
                  className="w-24 px-3 py-2 border border-gray-300 rounded-lg text-center text-lg"
                  min="0"
                />
                <button
                  onClick={() => setNewQueryCount(newQueryCount + 1)}
                  className="px-3 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-lg font-bold"
                >
                  +
                </button>
              </div>
            </div>
            
            <div className="flex gap-2 mb-4">
              <button
                onClick={() => setNewQueryCount(0)}
                className="flex-1 px-3 py-2 bg-green-100 hover:bg-green-200 text-green-700 rounded-lg text-sm"
              >
                Auf 0 setzen
              </button>
              <button
                onClick={() => setNewQueryCount(editingQueryUser.queriesLimit)}
                className="flex-1 px-3 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg text-sm"
              >
                Auf Limit setzen
              </button>
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={() => setEditingQueryUser(null)}
                className="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium"
              >
                Abbrechen
              </button>
              <button
                onClick={() => handleSetQueries(editingQueryUser.id, newQueryCount)}
                className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
              >
                Speichern
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
