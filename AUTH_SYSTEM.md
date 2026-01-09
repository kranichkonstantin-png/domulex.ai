# Firebase Authentication System - Domulex.ai

## Übersicht

Das Domulex.ai Auth-System basiert auf **Firebase Authentication** und **Firestore** für Benutzerverwaltung.

## Features

### 1. Benutzer-Registrierung

**Wege zur Registrierung:**
- ✅ E-Mail & Passwort
- ✅ Google OAuth

**Automatischer Prozess:**
1. Firebase Auth Konto wird erstellt
2. Firestore `/users/{userId}` Dokument wird angelegt mit:
   ```json
   {
     "email": "user@example.com",
     "name": "Max Mustermann",
     "tier": "free",
     "queriesUsed": 0,
     "queriesLimit": 3,
     "createdAt": "2025-12-28T...",
     "updatedAt": "2025-12-28T..."
   }
   ```
3. Willkommens-E-Mail wird versendet (optional)
4. Redirect zu `/dashboard`

**Implementierung:**
- Frontend: `/src/app/auth/register/page.tsx`
- Firestore Funktion: `createUserDocument()`

### 2. Benutzer-Login

**Login-Optionen:**
- E-Mail & Passwort
- Google OAuth
- "Angemeldet bleiben" Option

**Implementierung:**
- Frontend: `/src/app/auth/login/page.tsx`
- Firebase Auth: `signInWithEmailAndPassword`, `signInWithPopup`

### 3. Passwort-Reset

**Ablauf:**
1. Benutzer gibt E-Mail ein
2. Firebase sendet Password-Reset-E-Mail
3. Benutzer klickt auf Link in E-Mail
4. Benutzer setzt neues Passwort

**Implementierung:**
- Frontend: `/src/app/auth/reset-password/page.tsx`
- Firebase Auth: `sendPasswordResetEmail`

### 4. User Dashboard

**URL:** `/dashboard`

**Zugriff:** Nur für angemeldete Benutzer

**Features:**
- Tarifanzeige mit Badge (Free, Mieter Plus, Professional, Lawyer Pro)
- Verbrauchsanzeige:
  - Fortschrittsbalken
  - Verwendet / Limit
  - Verbleibende Anfragen
- Schnellzugriff:
  - Neue Anfrage stellen
  - Support kontaktieren
- Account-Details:
  - Name, E-Mail, Tarif
- Hilfreiche Links:
  - AGB, Datenschutz, Widerruf, Support

**Implementierung:**
- Frontend: `/src/app/dashboard/page.tsx`
- Auth Guard: `onAuthStateChanged` redirect

### 5. Admin Dashboard

**URL:** `/admin`

**Zugriff:** Nur für Admins
- `kranichkonstantin@gmail.com`
- `admin@domulex.ai`

**Features:**
- **Statistiken**:
  - Gesamt Benutzer
  - Free vs. Premium Benutzer
  - Gesamt Anfragen
- **Benutzerverwaltung**:
  - Alle Benutzer anzeigen (sortiert nach Erstellungsdatum)
  - Tarif ändern (Dropdown mit Free, Mieter Plus, Professional, Lawyer Pro)
  - Anfragen zurücksetzen (Reset zu 0)
  - Benutzer löschen
  - Fortschrittsbalken pro Benutzer
- **Live-Updates**: Aktualisieren-Button

**Implementierung:**
- Frontend: `/src/app/admin/page.tsx`
- Admin Check: `ADMIN_EMAILS.includes(user.email)`

## Firestore Datenmodell

### Users Collection (`/users/{userId}`)

```typescript
interface User {
  email: string;                    // Benutzer E-Mail
  name: string;                     // Anzeigename
  tier: 'free' | 'mieter_plus' | 'professional' | 'lawyer';  // Tarif
  queriesUsed: number;              // Verwendete Anfragen
  queriesLimit: number;             // Anfragen-Limit
  createdAt: string;                // ISO Timestamp
  updatedAt: string;                // ISO Timestamp
  stripeCustomerId?: string;        // Stripe Customer ID (optional)
  stripeSubscriptionId?: string;    // Stripe Subscription ID (optional)
}
```

### Tarif-Limits

| Tarif          | Queries/Monat | Preis    |
|---------------|---------------|----------|
| Free          | 3             | 0€       |
| Mieter Plus   | 100           | 9€       |
| Professional  | 500           | 29€      |
| Lawyer Pro    | 1.000         | 49€      |

## Firestore Security Rules

```javascript
// Users können nur ihre eigenen Daten lesen/schreiben
match /users/{userId} {
  allow read: if request.auth.uid == userId;
  allow create: if request.auth.uid == userId;
  allow update: if request.auth.uid == userId
                && !affectedKeys().hasAny(['tier', 'queriesLimit', ...]);
  
  // Admins haben vollen Zugriff
  allow read, write: if request.auth.token.email in [
    'kranichkonstantin@gmail.com', 
    'admin@domulex.ai'
  ];
}
```

## Auth Guards

### Protected Routes

**User Dashboard** (`/dashboard`):
```typescript
onAuthStateChanged(auth, (user) => {
  if (!user) router.push('/auth/login');
});
```

**Admin Dashboard** (`/admin`):
```typescript
onAuthStateChanged(auth, (user) => {
  if (!user) router.push('/auth/login');
  if (!ADMIN_EMAILS.includes(user.email)) router.push('/dashboard');
});
```

## Integration mit Backend

### Willkommens-E-Mail

Nach Registrierung wird automatisch eine Willkommens-E-Mail versendet:

```typescript
await fetch('https://domulex-backend-841507936108.europe-west3.run.app/email/send-welcome', {
  method: 'POST',
  body: new URLSearchParams({
    user_email: email,
    user_name: name,
  }),
});
```

**Backend Endpoint:** `POST /email/send-welcome`
**Service:** Resend API

## Deployment

### Firestore Rules deployen:
```bash
firebase deploy --only firestore:rules
```

### Frontend deployen:
```bash
npm run build
firebase deploy --only hosting
```

## Umgebungsvariablen

**Frontend** (`.env.local`):
```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=domulex-ai.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=domulex-ai
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=domulex-ai.firebasestorage.app
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

**Backend** (Cloud Run Environment Variables):
```env
GEMINI_API_KEY=your_gemini_key
RESEND_API_KEY=your_resend_key
FROM_EMAIL=noreply@domulex.ai
FROM_NAME=Domulex.ai
```

## Admin-Zugriff

Um Admin-Rechte zu erhalten, muss die E-Mail-Adresse in beiden Stellen eingetragen werden:

1. **Frontend** (`/src/app/admin/page.tsx`):
```typescript
const ADMIN_EMAILS = ['kranichkonstantin@gmail.com', 'admin@domulex.ai'];
```

2. **Firestore Rules** (`firestore.rules`):
```javascript
allow read, write: if request.auth.token.email in [
  'kranichkonstantin@gmail.com', 
  'admin@domulex.ai'
];
```

## Sicherheit

✅ **Passwort-Anforderungen**: Mindestens 6 Zeichen
✅ **Firestore Rules**: Benutzer können nur eigene Daten ändern
✅ **Admin Check**: Zweifache Validierung (Frontend + Firestore)
✅ **Tier Protection**: Benutzer können `tier` und `queriesLimit` nicht selbst ändern
✅ **Email Verification**: Optional aktivierbar in Firebase Console

## Testing

### Test-Benutzer erstellen:
1. Gehe zu https://domulex-ai.web.app/auth/register
2. Registriere mit E-Mail & Passwort
3. Dashboard öffnet sich automatisch

### Admin testen:
1. Mit Admin-E-Mail anmelden
2. `/admin` aufrufen
3. Benutzer verwalten

## Troubleshooting

**Problem**: "Firestore permission denied"
**Lösung**: Firestore Rules deployen: `firebase deploy --only firestore:rules`

**Problem**: "User not found in database"
**Lösung**: Firestore Dokument wurde nicht erstellt. Manuell anlegen oder neu registrieren.

**Problem**: "Admin access denied"
**Lösung**: E-Mail in `ADMIN_EMAILS` und Firestore Rules eintragen.

## Next Steps

- [ ] E-Mail Verification aktivieren
- [ ] Custom Claims für Admin-Rolle (sicherer)
- [ ] Zwei-Faktor-Authentifizierung
- [ ] Audit Log für Admin-Aktionen
- [ ] Rate Limiting für Registrierung
