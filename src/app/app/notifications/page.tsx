'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, query, where, orderBy, getDocs, updateDoc, doc, deleteDoc, Timestamp } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import Logo from '@/components/Logo';

interface Notification {
  id: string;
  userId: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'admin' | 'system';
  read: boolean;
  createdAt: Timestamp;
  link?: string;
}

export default function NotificationsPage() {
  const [user, setUser] = useState<any>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }
      setUser(currentUser);
      await loadNotifications(currentUser.uid);
    });

    return () => unsubscribe();
  }, [router]);

  const loadNotifications = async (userId: string) => {
    setLoading(true);
    try {
      const notificationsRef = collection(db, 'notifications');
      const q = query(
        notificationsRef,
        where('userId', '==', userId),
        orderBy('createdAt', 'desc')
      );
      const snapshot = await getDocs(q);
      const notifs: Notification[] = [];
      snapshot.forEach((doc) => {
        notifs.push({ id: doc.id, ...doc.data() } as Notification);
      });
      setNotifications(notifs);
    } catch (err) {
      console.error('Error loading notifications:', err);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (notificationId: string) => {
    try {
      await updateDoc(doc(db, 'notifications', notificationId), { read: true });
      setNotifications(prev => 
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      );
    } catch (err) {
      console.error('Error marking as read:', err);
    }
  };

  const markAllAsRead = async () => {
    for (const notif of notifications.filter(n => !n.read)) {
      await markAsRead(notif.id);
    }
  };

  const deleteNotification = async (notificationId: string) => {
    try {
      await deleteDoc(doc(db, 'notifications', notificationId));
      setNotifications(prev => prev.filter(n => n.id !== notificationId));
    } catch (err) {
      console.error('Error deleting notification:', err);
    }
  };

  const getTypeIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success': return '✅';
      case 'warning': return '⚠️';
      case 'admin': return '👑';
      case 'system': return '🔔';
      default: return 'ℹ️';
    }
  };

  const getTypeLabel = (type: Notification['type']) => {
    switch (type) {
      case 'success': return 'Erfolg';
      case 'warning': return 'Warnung';
      case 'admin': return 'Admin';
      case 'system': return 'System';
      default: return 'Info';
    }
  };

  const formatDate = (timestamp: Timestamp) => {
    if (!timestamp) return '';
    const date = timestamp.toDate();
    return date.toLocaleDateString('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredNotifications = filter === 'unread' 
    ? notifications.filter(n => !n.read)
    : notifications;

  const unreadCount = notifications.filter(n => !n.read).length;

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1e3a5f] mx-auto mb-4"></div>
          <p className="text-gray-600">Lädt Benachrichtigungen...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-sm text-gray-600 hover:text-[#1e3a5f]">
                ← Dashboard
              </Link>
              <div className="h-6 w-px bg-gray-200" />
              <Logo size="sm" />
            </div>
            <span className="text-sm text-gray-500">Benachrichtigungen</span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 pt-32 pb-12">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-[#1e3a5f]">Benachrichtigungen</h1>
            <p className="text-gray-600 mt-1">
              {unreadCount > 0 ? `${unreadCount} ungelesen` : 'Alle gelesen'}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as 'all' | 'unread')}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="all">Alle ({notifications.length})</option>
              <option value="unread">Ungelesen ({unreadCount})</option>
            </select>
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="px-4 py-2 bg-[#1e3a5f] text-white rounded-lg text-sm hover:bg-[#2d4a6f]"
              >
                Alle als gelesen markieren
              </button>
            )}
          </div>
        </div>

        {filteredNotifications.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center">
            <div className="text-6xl mb-4">📭</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Keine Benachrichtigungen</h2>
            <p className="text-gray-600">
              {filter === 'unread' ? 'Alle Benachrichtigungen wurden gelesen.' : 'Sie haben noch keine Benachrichtigungen erhalten.'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredNotifications.map((notif) => (
              <div
                key={notif.id}
                className={`bg-white rounded-xl shadow-lg p-6 transition-all ${
                  !notif.read ? 'border-l-4 border-[#1e3a5f]' : ''
                }`}
              >
                <div className="flex items-start gap-4">
                  <span className="text-3xl">{getTypeIcon(notif.type)}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <h3 className={`font-semibold text-gray-900 ${!notif.read ? 'font-bold' : ''}`}>
                          {notif.title}
                        </h3>
                        <span className={`px-2 py-0.5 text-xs rounded-full ${
                          notif.type === 'admin' ? 'bg-purple-100 text-purple-700' :
                          notif.type === 'success' ? 'bg-green-100 text-green-700' :
                          notif.type === 'warning' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-blue-100 text-blue-700'
                        }`}>
                          {getTypeLabel(notif.type)}
                        </span>
                        {!notif.read && (
                          <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                        )}
                      </div>
                      <span className="text-sm text-gray-400">{formatDate(notif.createdAt)}</span>
                    </div>
                    <p className="text-gray-600 whitespace-pre-wrap">{notif.message}</p>
                    {notif.link && (
                      <Link href={notif.link} className="text-[#1e3a5f] hover:underline text-sm mt-2 inline-block">
                        Mehr erfahren →
                      </Link>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    {!notif.read && (
                      <button
                        onClick={() => markAsRead(notif.id)}
                        className="p-2 text-gray-400 hover:text-[#1e3a5f]"
                        title="Als gelesen markieren"
                      >
                        ✓
                      </button>
                    )}
                    <button
                      onClick={() => deleteNotification(notif.id)}
                      className="p-2 text-gray-400 hover:text-red-500"
                      title="Löschen"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
