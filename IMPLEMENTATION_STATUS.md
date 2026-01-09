# Domulex.ai - Aktuelle Implementation (Status Update)

## ✅ Abgeschlossene Aufgaben

### 1. Gemini API Integration
- **Neuer API-Key**: `AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls`
- **Modell-Namen korrigiert**: 
  - Von `gemini-1.5-flash-latest` zu `gemini-1.5-flash`
  - Von `gemini-1.5-pro-latest` zu `gemini-1.5-pro`
- **Cloud Run Umgebungsvariable** aktualisiert
- **Backend Deployment**: In Arbeit (Build läuft)

### 2. Firebase Authentication System
Vollständig implementiert und deployed:

#### Login-Seite (`/auth/login`)
- Email/Password Login
- Google OAuth Integration
- "Angemeldet bleiben" Funktion
- Fehlerbehandlung und Validierung

#### Registrierungs-Seite (`/auth/register`)
- Email/Password Registrierung
- **Automatische Firestore-Dokument-Erstellung**:
  ```typescript
  {
    email: string,
    name: string,
    tier: 'free',
    queriesUsed: 0,
    queriesLimit: 3,
    createdAt: timestamp,
    updatedAt: timestamp
  }
  ```
- Weiterleitung zum Dashboard nach erfolgreicher Registrierung
- Willkommens-Email-Trigger

#### Passwort-Reset (`/auth/reset-password`)
- Email-basierte Passwort-Wiederherstellung
- Firebase Password Reset Flow
- Erfolgs-/Fehler-Anzeigen

#### User Dashboard (`/dashboard`)
- **Tier-Anzeige**: Free, Mieter Plus, Professional, Lawyer
- **Nutzungsstatistik**: 
  - Verbrauchte Anfragen
  - Verfügbare Anfragen (Query-Limit)
  - Fortschrittsbalken
- **Account-Informationen**:
  - Name und Email
  - Mitglied seit
  - Aktiver Tarif
- **Quick Actions**: 
  - Neue Anfrage stellen
  - Tarif upgraden
  - Profil bearbeiten
  - Logout

#### Admin Dashboard (`/admin`)
- **Zugriffskontrolle**: Nur für Admin-Emails
  - `kranichkonstantin@gmail.com`
  - `admin@domulex.ai`
- **Benutzer-Verwaltung**:
  - Alle Benutzer anzeigen
  - Tier-Änderungen
  - Query-Counter zurücksetzen
  - Benutzer löschen
- **Statistiken**:
  - Gesamtanzahl Benutzer
  - Benutzer pro Tier
  - Gesamte Anfragen

### 3. Firestore Security Rules
Deployed und aktiv:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Admin-Funktion
    function isAdmin() {
      return request.auth != null && 
        (request.auth.token.email == 'kranichkonstantin@gmail.com' ||
         request.auth.token.email == 'admin@domulex.ai');
    }
    
    // User kann nur eigene Daten lesen/schreiben
    match /users/{userId} {
      allow read: if request.auth != null && 
        (request.auth.uid == userId || isAdmin());
      
      allow write: if request.auth != null && 
        (request.auth.uid == userId || isAdmin()) &&
        // Verhindert Manipulation von tier, queriesLimit, Stripe-Feldern
        (!request.resource.data.diff(resource.data).affectedKeys()
          .hasAny(['tier', 'queriesLimit', 'stripeCustomerId', 'stripeSubscriptionId'])
         || isAdmin());
    }
  }
}
```

### 4. Frontend Deployment
- **Status**: ✅ Erfolgreich deployed
- **URL**: https://domulex-ai.web.app
- **Build**: 168 Dateien, kompiliert in 1434.7ms
- **Features aktiv**:
  - Login/Registrierung
  - User Dashboard
  - Admin Dashboard
  - Passwort-Reset

### 5. Backend Deployment
- **Status**: ⏳ In Arbeit (Container wird gebaut)
- **URL**: https://domulex-backend-841507936108.europe-west3.run.app
- **Änderungen**:
  - Gemini API Key aktualisiert
  - Modell-Namen korrigiert (ohne `-latest`)
- **Build-ID**: `b99f2c23-4671-480b-83c9-44929f3b2de7`

## 📋 Firestore Daten-Schema

### User-Dokument (`/users/{userId}`)
```typescript
{
  email: string,              // User's email
  name: string,               // Full name
  tier: 'free' | 'mieter_plus' | 'professional' | 'lawyer',
  queriesUsed: number,        // Anzahl verwendeter Anfragen
  queriesLimit: number,       // Maximale Anfragen pro Monat
  createdAt: string,          // ISO timestamp
  updatedAt: string,          // ISO timestamp
  stripeCustomerId?: string,  // Nur durch Admin änderbar
  stripeSubscriptionId?: string  // Nur durch Admin änderbar
}
```

### Tier-Limits
- **Free**: 3 Anfragen/Monat
- **Mieter Plus**: 100 Anfragen/Monat
- **Professional**: 500 Anfragen/Monat
- **Lawyer**: 1000 Anfragen/Monat

## 🔄 Nächste Schritte

### Nach Backend-Deployment:
1. **Support Endpoint testen**:
   ```bash
   curl -X POST https://domulex-backend-841507936108.europe-west3.run.app/support \
     -H "Content-Type: application/json" \
     -d '{"query": "Wie kündige ich mein Abo?", "user_language": "de"}' | jq
   ```

2. **Auth-Flow testen**:
   - Gehe zu https://domulex-ai.web.app/auth/register
   - Erstelle Test-Account
   - Prüfe Firestore-Dokument
   - Teste Dashboard-Zugriff

3. **Admin-Dashboard testen**:
   - Login mit `kranichkonstantin@gmail.com`
   - Navigiere zu `/admin`
   - Teste Benutzer-Verwaltung

## 📖 Dokumentation
Siehe [AUTH_SYSTEM.md](./AUTH_SYSTEM.md) für vollständige Details zum Authentication System.

## 🔑 Wichtige Zugangsdaten
- **Admin Emails**: 
  - kranichkonstantin@gmail.com
  - admin@domulex.ai
- **Firebase Project**: domulex-ai
- **Cloud Run Region**: europe-west3
- **Gemini API Key**: AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls
