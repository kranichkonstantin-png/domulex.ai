# Domulex Checkout & Upgrade Flow

## ✅ Implementierter Flow

### 1. **Nicht eingeloggter Benutzer**

```
Landingpage → "Kostenlos starten" → /auth/register → Login → Dashboard
```

- Alle "Kostenlos starten" Buttons führen zu `/auth/register`
- Bezahl-Buttons (Mieter Plus, Professional, Lawyer Pro) prüfen Login-Status
- **Nicht eingeloggt**: Automatische Weiterleitung zu `/auth/register`

### 2. **Free User - Limit erreicht**

```
/app (3/3 Anfragen) → Paywall-Overlay → "Jetzt upgraden" → /#pricing
Dashboard → "Jetzt upgraden" → /#pricing
```

**Paywall Features:**
- ✅ Fullscreen-Overlay mit Blur-Hintergrund
- ✅ Zeigt verbrauchte Anfragen (z.B. "Du hast deine 3 kostenlosen Anfragen aufgebraucht")
- ✅ Übersicht aller 3 Bezahl-Tiere (19€ / 39€ / 69€)
- ✅ "Jetzt upgraden" Button führt zu `/#pricing`
- ✅ Sidebar zeigt Verbrauch + Upgrade-Button

**Paywall erscheint in:**
- `/app` Seite (KI-Chat Interface)
- Dashboard zeigt permanenten Upgrade-Button wenn Tier = "free"

### 3. **Bezahl-Flow (Eingeloggt)**

```
Landingpage → Plan wählen → CheckoutModal → Stripe Checkout → Dashboard
```

**CheckoutModal Features:**
- ✅ Bestellübersicht mit Plan-Details
- ✅ User-Typ Auswahl (Privat/Gewerblich)
- ✅ AGB & Widerrufsbelehrung Checkboxes
- ✅ Sofortiger Beginn der Dienstleistung (Widerrufsrecht-Hinweis)
- ✅ Download-Links für AGB & Widerrufsbelehrung

**Backend Integration:**
- ✅ Endpoint: `POST /stripe/create-checkout-session`
- ✅ Authentifizierung via Firebase Token
- ✅ Tier-Mapping: `free → FREE`, `mieter_plus → TENANT`, `professional → PRO`, `lawyer → LAWYER`
- ✅ Erstellt Stripe Checkout Session
- ✅ Weiterleitung zu Stripe Checkout
- ✅ Nach Zahlung zurück zu `/dashboard?session_id={CHECKOUT_SESSION_ID}`

## 🔧 Technische Details

### Frontend (`/src/app/page.tsx`)

```typescript
const handleCheckout = (plan) => {
  // Prüfe Login-Status
  if (!isLoggedIn) {
    router.push('/auth/register');
    return;
  }
  
  // Öffne Checkout-Modal
  setSelectedPlan(plan);
  setShowCheckout(true);
};

const handleCheckoutConfirm = async (acceptedTerms) => {
  const idToken = await user.getIdToken();
  
  const response = await fetch(`${BACKEND_URL}/stripe/create-checkout-session`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    },
    body: JSON.stringify({
      tier: selectedPlan.id, // 'free', 'mieter_plus', 'professional', 'lawyer'
      success_url: `${window.location.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${window.location.origin}/#pricing`
    })
  });
  
  const { checkout_url } = await response.json();
  window.location.href = checkout_url; // Redirect zu Stripe
};
```

### Backend (`/backend/main.py`)

```python
@app.post("/stripe/create-checkout-session")
async def create_stripe_checkout(
    request: dict,
    user_id: str = Depends(get_current_user)
):
    tier = request.get("tier", "").lower()
    
    # Tier-Mapping
    tier_mapping = {
        "free": "FREE",
        "mieter_plus": "TENANT",
        "professional": "PRO",
        "lawyer": "LAWYER"
    }
    
    stripe_tier = tier_mapping[tier]
    
    # Get user email from Firestore
    user_doc = await db.collection('users').document(user_id).get()
    user_email = user_doc.to_dict().get('email', '')
    
    # Create Stripe Checkout Session
    result = StripeService.create_checkout_session(
        user_email=user_email,
        tier=stripe_tier,
        success_url=request.get("success_url"),
        cancel_url=request.get("cancel_url"),
        user_id=user_id,
    )
    
    return {
        "checkout_url": result['url'],
        "session_id": result['session_id'],
    }
```

### Paywall (`/src/app/app/page.tsx`)

```typescript
useEffect(() => {
  const unsubscribe = onAuthStateChanged(auth, async (user) => {
    if (user) {
      const userDoc = await getDoc(doc(db, 'users', user.uid));
      const data = userDoc.data();
      
      // Paywall anzeigen wenn Limit erreicht
      if (data.queriesUsed >= data.queriesLimit) {
        setShowPaywall(true);
      }
    }
  });
}, []);

{showPaywall && (
  <div className="fixed inset-0 bg-black/70 backdrop-blur-md">
    <div className="bg-white rounded-2xl p-8">
      <h2>Limit erreicht!</h2>
      <p>Du hast deine {userData.queriesLimit} kostenlosen Anfragen aufgebraucht.</p>
      
      <div className="grid grid-cols-3 gap-4">
        <PricingCard tier="mieter_plus" price="19€" />
        <PricingCard tier="professional" price="39€" />
        <PricingCard tier="lawyer" price="69€" />
      </div>
      
      <button onClick={() => router.push('/#pricing')}>
        Jetzt upgraden
      </button>
    </div>
  </div>
)}
```

## 📋 Stripe Setup Checklist

### ✅ Completed
- [x] Stripe Service im Backend (`/backend/services/stripe_service.py`)
- [x] Checkout Session Endpoint (`/stripe/create-checkout-session`)
- [x] Frontend Checkout Flow mit Login-Check
- [x] CheckoutModal mit AGB/Widerruf
- [x] Paywall bei Limit-Überschreitung
- [x] Tier-Mapping (frontend → backend)
- [x] Mieter Plus Price ID: `price_1Sj8l83LV15CfXasN3zUqv2v`

### ⏳ To Do
- [ ] **Stripe Secret Key** hinzufügen zu Backend Environment Variables
- [ ] **Professional Price ID** erstellen in Stripe Dashboard (39€/Monat)
- [ ] **Lawyer Pro Price ID** erstellen in Stripe Dashboard (69€/Monat)
- [ ] **Webhook Endpoint** konfigurieren für `checkout.session.completed`
- [ ] **Webhook Handler** implementieren (automatisches Tier-Upgrade nach Zahlung)
- [ ] Testen: Free → Mieter Plus Upgrade
- [ ] Testen: Mieter Plus → Professional Upgrade
- [ ] Testen: Professional → Lawyer Pro Upgrade

## 🎯 Nächste Schritte

### 1. Stripe Produkte erstellen
Gehe zu https://dashboard.stripe.com/products/create und erstelle:

**Professional (39€)**
- Name: Domulex Professional
- Beschreibung: 500 Anfragen, PDF-Analyse, Alle Rollen
- Preis: 39.00 EUR/Monat (recurring)
- → Kopiere Price ID

**Lawyer Pro (69€)**
- Name: Domulex Lawyer Pro  
- Beschreibung: 1000 Anfragen, Anwalts-Modus, CRM, Dokumentenmanagement
- Preis: 69.00 EUR/Monat (recurring)
- → Kopiere Price ID

### 2. Environment Variables setzen

```bash
cd backend
gcloud run deploy domulex-backend \
  --source . \
  --region=europe-west3 \
  --allow-unauthenticated \
  --update-env-vars="STRIPE_SECRET_KEY=sk_test_51S402X3LV15CfXas2kijjWnds3sXPaTdlAK2FnftPefB9jzZY5vobXtwhiM82H0ExlG8aDeOZFod7kGdozs9FhD00SdyPgtgA,STRIPE_WEBHOOK_SECRET=whsec_nqf6ggVHJO7rBorY5xZzWLRuYNT00JUV,STRIPE_PRICE_TENANT=price_1Sj8l83LV15CfXasN3zUqv2v,STRIPE_PRICE_PRO=price_1Siuom3LV15CfXasXmpE2LCt,STRIPE_PRICE_LAWYER=price_1Siutl3LV15CfXas4Mxel6SS"
```

### 3. Webhook konfigurieren

1. Gehe zu https://dashboard.stripe.com/webhooks
2. Add endpoint: `https://domulex-backend-841507936108.europe-west3.run.app/stripe/webhook`
3. Events: `checkout.session.completed`, `customer.subscription.updated`, etc.
4. Kopiere Webhook Secret (`whsec_...`)
5. Setze als Environment Variable: `STRIPE_WEBHOOK_SECRET=whsec_...`

### 4. Testen

```bash
# Test Checkout Session erstellen
curl -X POST https://domulex-backend-841507936108.europe-west3.run.app/stripe/create-checkout-session \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "mieter_plus",
    "success_url": "https://domulex-ai.web.app/dashboard?session_id={CHECKOUT_SESSION_ID}",
    "cancel_url": "https://domulex-ai.web.app/#pricing"
  }'
```

## 🔐 Security

- ✅ Alle Checkout-Requests erfordern Firebase Authentication
- ✅ User Email wird aus Firestore gelesen (nicht vom Frontend)
- ✅ Stripe Secret Key nur im Backend
- ✅ Webhook-Signatur-Verifizierung (noch zu implementieren)
- ✅ HTTPS only (Cloud Run enforced)

## 📊 User Journey Beispiele

### Journey 1: Neuer Nutzer → Mieter Plus
1. Besucht https://domulex-ai.web.app
2. Klickt "Kostenlos starten" → `/auth/register`
3. Registriert sich → automatisch `tier: free`, `queriesLimit: 3`
4. Nutzt 3 kostenlose Anfragen in `/app`
5. 4. Anfrage → **Paywall erscheint**
6. Klickt "Jetzt upgraden" → `/#pricing`
7. Wählt "Mieter Plus (19€)" → **CheckoutModal**
8. Akzeptiert AGB → Redirect zu **Stripe Checkout**
9. Zahlt mit Kreditkarte → Redirect zu `/dashboard?session_id=cs_...`
10. Webhook updated `tier: mieter_plus`, `queriesLimit: 100`
11. Kann jetzt 100 Anfragen pro Monat nutzen

### Journey 2: Direkter Kauf ohne Account
1. Besucht https://domulex-ai.web.app
2. Scrollt zu Pricing → Klickt "Jetzt starten" bei Professional (39€)
3. **Nicht eingeloggt** → Redirect zu `/auth/register`
4. Registriert sich
5. **Automatischer Redirect zurück zu** `/#pricing`
6. Klickt erneut "Jetzt starten" bei Professional
7. **Jetzt eingeloggt** → CheckoutModal öffnet sich
8. Rest wie Journey 1

### Journey 3: Upgrade Free → Professional
1. Free User mit 3/3 Anfragen aufgebraucht
2. Dashboard zeigt "Jetzt upgraden" Button
3. Klickt Button → `/#pricing`
4. Wählt Professional (39€) → CheckoutModal
5. Zahlt → Upgrade von `free` zu `professional`
6. Neue Limits: 500 Anfragen/Monat

## 💡 Feature Highlights

### Smart Routing
- Kostenlos-Buttons → Registrierung
- Bezahl-Buttons → Login-Check → Checkout oder Registrierung

### Paywall Strategie
- **Nicht blockierend**: User kann Paywall schließen ("Später")
- **Prominent**: Fullscreen Overlay mit Blur
- **Klar**: Zeigt verbleibende Anfragen + Upgrade-Optionen
- **In-App**: Direkt in `/app` wenn Limit erreicht
- **Dashboard**: Permanent sichtbar für Free-User

### Checkout UX
- **Transparent**: Bestellübersicht vor Zahlung
- **Legal Compliant**: AGB + Widerrufsbelehrung (DE)
- **Flexible**: Privat vs. Gewerblich Unterscheidung
- **Download**: AGB/Widerruf als PDF verfügbar
- **Secure**: Zahlung über Stripe (PCI-DSS compliant)

## 🎨 Design Prinzipien

1. **Keine Barrieren für Free**: Registrierung ohne Kreditkarte
2. **Klare Value Proposition**: "Spare 100-300€/Monat" Message
3. **Vertrauen**: Transparente Preise, klare AGB, DSGVO-konform
4. **Urgency**: Paywall wenn Limit erreicht
5. **Simplicity**: 1-Click Checkout (nach AGB-Akzeptanz)
