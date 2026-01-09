# Tier-basierte Zugriffskontrolle

## ✅ Implementierte Beschränkungen

### Backend Endpoints

#### `/query` - Rechtsfragen-Endpoint
**Alle Tiers haben Zugriff**, aber mit unterschiedlichen Limits:

| Tier | Anfragen/Monat | Preis |
|------|----------------|-------|
| Free | 3 | 0€ |
| Mieter Plus | 100 | 9€ |
| Professional | 500 | 29€ |
| Lawyer | 1.000 | 49€ |

**Request-Parameter:**
```json
{
  "query": "Ihre Rechtsfrage",
  "target_jurisdiction": "DE",
  "user_role": "TENANT",
  "user_language": "de",
  "user_id": "firebase_uid",
  "user_tier": "free"
}
```

**Quota-Tracking:**
- `user_id` und `user_tier` werden geloggt
- TODO: Firestore-Integration für Quota-Enforcement

#### `/analyze_contract` - PDF-Vertragsanalyse
**NUR Professional & Lawyer Tier**

**Tier-Check implementiert:**
```python
if user_tier.lower() not in ['professional', 'lawyer']:
    raise HTTPException(
        status_code=403,
        detail="PDF-Vertragsanalyse ist nur im Professional- oder Lawyer-Tarif verfügbar."
    )
```

**Request-Parameter:**
```bash
curl -X POST https://domulex-backend-841507936108.europe-west3.run.app/analyze_contract \
  -F "file=@vertrag.pdf" \
  -F "jurisdiction=DE" \
  -F "user_role=TENANT" \
  -F "user_tier=professional"
```

**Fehler bei Free/Mieter Plus:**
```json
{
  "detail": "PDF-Vertragsanalyse ist nur im Professional- oder Lawyer-Tarif verfügbar. Bitte upgraden Sie Ihren Tarif."
}
```

## 📋 Feature-Matrix

| Feature | Free | Mieter Plus | Professional | Lawyer |
|---------|------|-------------|--------------|--------|
| **Anfragen/Monat** | 3 | 100 | 500 | 1.000 |
| **Deutsches Immobilienrecht** | ✅ | ✅ | ✅ | ✅ |
| **Konfliktlösung mit Musterbriefen** | ❌ | ✅ | ✅ | ✅ |
| **PDF-Upload & Vertragsanalyse** | ❌ | ❌ | ✅ | ✅ |
| **Risikobewertung Klauseln** | ❌ | ❌ | ✅ | ✅ |
| **Mehrfach-PDF-Analyse** | ❌ | ❌ | ❌ | ✅ |
| **Prioritäts-Support** | ❌ | ❌ | ✅ | ❌ |
| **24/7 Premium Support** | ❌ | ❌ | ❌ | ✅ |

## 🚫 Entfernte Features (nicht implementiert)

- ~~API-Zugang~~ - Nicht implementiert
- ~~Bulk-Analyse~~ - Nicht implementiert  
- ~~DE, ES, US Rechtssysteme~~ - Nur Deutschland verfügbar
- ~~Alle Rollen & Jurisdiktionen~~ - Nur Deutschland

## 🔄 TODO: Vollständige Quota-Enforcement

Derzeit wird `user_tier` nur geloggt. Für vollständige Enforcement:

1. **Firestore-Integration in `/query`:**
```python
# Check user quota in Firestore
user_doc = db.collection('users').document(request.user_id).get()
if user_doc.exists:
    user_data = user_doc.to_dict()
    if user_data['queriesUsed'] >= user_data['queriesLimit']:
        raise HTTPException(
            status_code=429,
            detail="Monatliches Anfrage-Limit erreicht. Bitte upgraden Sie Ihren Tarif."
        )
    # Increment counter
    db.collection('users').document(request.user_id).update({
        'queriesUsed': firestore.Increment(1)
    })
```

2. **Frontend ChatInterface:**
- `user_tier` aus Firestore User-Dokument lesen
- Bei `/query` Request mitschicken
- Bei 403/429 Error → Upgrade-Modal anzeigen

## 🎯 Admin-Bereich

**Admin-Benutzer:**
- Email: `kontakt@domulex.ai`
- UID: `Up9nWC381Sdf4TCMmubtiYtru4N2`
- Tier: `lawyer` (10.000 Anfragen)
- Rolle: `admin`

**Weitere Admin-Emails:**
- `kranichkonstantin@gmail.com`
- `admin@domulex.ai`
- `kontakt@domulex.ai`

**Firestore Rules:**
```javascript
allow read, write: if request.auth != null && 
  request.auth.token.email in [
    'kranichkonstantin@gmail.com', 
    'admin@domulex.ai', 
    'kontakt@domulex.ai'
  ];
```

## 📊 Deployment Status

- ✅ Frontend deployed: https://domulex-ai.web.app
- 🔄 Backend deploying: Mit Tier-Checks für PDF-Analyse
- ✅ Firestore Rules deployed: Admin-Zugriff konfiguriert
- ✅ Firebase Auth: Email/Password + Google OAuth
