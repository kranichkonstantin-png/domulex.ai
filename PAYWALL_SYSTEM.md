# 💰 DOMULEX Paywall & Pricing System

## Übersicht

Vollständiges Freemium-Modell mit Quota-Management, Feature-Gates und Upgrade-Flow.

---

## 🎯 Pricing-Tiers

| Tier | Preis | Fragen/Monat | Hauptfeatures |
|------|-------|--------------|---------------|
| **FREE** | 0€ | 3 | Basis-Features, Mieter-Perspektive |
| **Mieter Plus** | 19€ | 100 | Erweiterte Mieter-Perspektive, Musterbriefe |
| **Professional** | 39€ | 500 | PDF-Vertragsanalyse, alle Rollen |
| **Lawyer Pro** | 69€ | 1.000 | Schriftsatz-Generierung, CRM, Dokumentenmanagement |

**Alle Preise inkl. 19% MwSt.**

---

## 🔧 Implementierung

### 1. Backend: User Model & Quota Management

**Datei:** `backend/models/user.py`

```python
class User(BaseModel):
    subscription_tier: SubscriptionTier
    queries_used_this_month: int
    last_reset_date: date
    
    def has_quota(self) -> bool:
        """Check if user has remaining quota."""
        
    def can_access_feature(self, feature: str) -> bool:
        """Check if tier grants access to feature."""
```

**Features:**
- ✅ Automatische monatliche Quota-Resets
- ✅ Tier-basierte Limits
- ✅ Feature-Gates (PDF_UPLOAD, INTERNATIONAL_SEARCH, API_ACCESS)

---

### 2. Backend: Security Middleware

**Datei:** `backend/core/security.py`

```python
def enforce_limits(user: User, request_type: str):
    """
    Main enforcement function.
    Raises QuotaExceededException or UpgradeRequiredException.
    """
```

**Exceptions:**
- `QuotaExceededException` (402): Monatliches Limit erreicht
- `UpgradeRequiredException` (402): Feature für Tier gesperrt

**Request Types:**
- `QUERY` - Standard-Frage
- `PDF_UPLOAD` - PDF-Analyse
- `INTERNATIONAL_SEARCH` - Nicht-DE-Jurisdiktionen
- `API_REQUEST` - API-Zugriff
- `CONTRACT_COMPARISON` - Vertragsvergleich

---

### 3. Frontend: Paywall UI Components

**Datei:** `paywall.py`

#### A. Quota Counter (Sidebar)
```python
render_quota_counter()
```
- Zeigt aktuellen Tier
- Progress Bar mit Nutzung
- Warnung bei 80% Limit
- Upgrade-Button

#### B. Paywall Modal
```python
show_paywall_modal(reason="quota"|"feature")
```
- Erscheint bei Limit-Überschreitung
- Zeigt Pricing-Vergleichstabelle
- Call-to-Action für Upgrade

#### C. Feature Gates
```python
if not check_feature_access("PDF_UPLOAD"):
    # Feature gesperrt - Paywall zeigen
```

---

### 4. Integration in Frontend

**Datei:** `frontend_app.py`

```python
# 1. Init user state
init_user_state()

# 2. Check quota before query
if not check_and_enforce_quota():
    return  # Paywall shown

# 3. Increment counter after query
increment_paywall_query()

# 4. Feature-specific gates
if jurisdiction != "DE" and tier == "FREE":
    check_feature_access("INTERNATIONAL_SEARCH")
```

---

## 🚀 Mock Payment Flow

**Aktuell:** Simulated Upgrade (keine echte Zahlung)

```python
def mock_upgrade(tier: str):
    st.session_state.user_tier = tier
    st.session_state.queries_used = 0
    st.success("Upgrade erfolgreich!")
```

**Für Produktion:** Ersetze mit Stripe Checkout

---

## 💳 Stripe Integration (Next Step)

### Setup:
```bash
pip install stripe
```

### Backend Endpoint:
```python
@app.post("/create-checkout-session")
async def create_checkout(tier: str, user_id: str):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': STRIPE_PRICE_IDS[tier],
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://domulex.ai/success',
        cancel_url='https://domulex.ai/cancel',
        client_reference_id=user_id,
    )
    return {"checkout_url": session.url}
```

### Frontend Update:
```python
def real_upgrade(tier: str):
    response = requests.post(
        f"{API_BASE_URL}/create-checkout-session",
        json={"tier": tier, "user_id": st.session_state.user_id}
    )
    checkout_url = response.json()["checkout_url"]
    st.markdown(f"[Zur Zahlung →]({checkout_url})")
```

### Webhook:
```python
@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    event = stripe.Webhook.construct_event(
        payload=await request.body(),
        sig_header=request.headers.get('stripe-signature'),
        secret=STRIPE_WEBHOOK_SECRET
    )
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['client_reference_id']
        # Update user tier in database
        update_user_tier(user_id, tier)
```

---

## 📊 Feature Gates Matrix

| Feature | FREE | Mieter Plus | Pro | Lawyer |
|---------|------|-------------|-----|--------|
| **Basis-Fragen** | ✅ (3) | ✅ (100) | ✅ (500) | ✅ (1000) |
| **Deutschland** | ✅ | ✅ | ✅ | ✅ |
| **USA/Spanien** | ❌ | ✅ | ✅ | ✅ |
| **PDF-Upload** | ❌ | ❌ | ✅ | ✅ |
| **Alle Rollen** | ❌ | ❌ | ✅ | ✅ |
| **Streitschlichtung** | ❌ | ✅ | ✅ | ✅ |
| **Vertragsvergleich** | ❌ | ❌ | ✅ | ✅ |
| **API-Zugriff** | ❌ | ❌ | ❌ | ✅ |
| **Bulk-Analyse** | ❌ | ❌ | ❌ | ✅ |

---

## 🧪 Testing

### Test FREE Tier (3 Queries):
1. Starte App
2. Stelle 3 Fragen
3. Bei 4. Frage: Paywall erscheint
4. Klick "Upgrade" → Pricing Table
5. Mock-Upgrade zu "Mieter Plus"
6. Quota resettet, weiter nutzbar

### Test Feature Gate (International Search):
1. Als FREE User
2. Wähle USA als Jurisdiction
3. Stelle Frage
4. Paywall: "International Search requires upgrade"

### Test PDF Upload (wenn implementiert):
1. Als TENANT User
2. Klick auf "PDF Upload"
3. Paywall: "PDF Upload nur für Pro/Lawyer"

---

## 📈 Analytics Tracking (Recommended)

```python
# Track paywall impressions
if show_paywall:
    analytics.track('paywall_shown', {
        'reason': reason,
        'current_tier': user.tier,
        'queries_used': user.queries_used
    })

# Track upgrades
if upgrade_success:
    analytics.track('subscription_upgraded', {
        'from_tier': old_tier,
        'to_tier': new_tier,
        'price': tier_price
    })
```

---

## 🎯 Conversion Optimization

### Best Practices:
1. **Clear Value Proposition**
   - Zeige gesperrte Features visuell
   - "Unlock 97 more questions" statt "Limit reached"

2. **Social Proof**
   - "500+ Nutzer haben upgraded"
   - "4.8★ auf Trustpilot"

3. **Urgency**
   - "Nur noch 2 Fragen heute im Free Tier"
   - "Upgrade jetzt: 20% Launch-Rabatt"

4. **Frictionless Upgrade**
   - 1-Click Stripe Checkout
   - Keine Formular-Orgie
   - Instant Access nach Zahlung

---

## 🔒 Security

### User Authentication (Required for Production):
```python
# Add to backend
from fastapi import Depends
from auth import get_current_user

@app.post("/query")
async def query(
    request: QueryRequest,
    user: User = Depends(get_current_user)
):
    enforce_limits(user, "QUERY")
    # Process query
```

### Rate Limiting:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_user_id)

@app.post("/query")
@limiter.limit("10/minute")  # Additional protection
async def query(...):
    ...
```

---

## 📦 Deployment Checklist

- [x] User model mit Subscription-Feldern
- [x] Quota-Check Middleware
- [x] Frontend Paywall UI
- [x] Mock Upgrade Flow
- [ ] Firebase Auth Integration
- [ ] Stripe Checkout Setup
- [ ] Webhook Handling
- [ ] Database Persistence
- [ ] Email Notifications
- [ ] Analytics Tracking

---

## 🚀 Live Status

**Deployed:** ✅ https://domulex-frontend-841507936108.europe-west3.run.app

**Current Mode:** Mock Payment (no credit card required)

**Test Credentials:**
- Default: FREE tier
- Mock upgrade via button in paywall

---

## 💡 Next Steps

1. **Firebase Authentication**
   - User Login/Signup
   - Persistent user data

2. **Stripe Production Setup**
   - Create Products & Prices
   - Configure Webhooks
   - Test mode → Live mode

3. **Database Integration**
   - Store user tier in Firestore
   - Track usage history
   - Billing history

4. **Email Automation**
   - Welcome emails
   - Payment confirmations
   - Usage alerts (80% quota)
   - Upgrade reminders
