# ✅ AUTOMATISIERUNGS-IMPLEMENTIERUNG - NÄCHSTE SCHRITTE

## 🎉 BEREITS IMPLEMENTIERT

### ✅ Task 1 & 2: Firebase Auth + Email-Verifizierung
- `/src/lib/auth.ts` - Kompletter Auth-Service
- `/src/components/AuthModal.tsx` - Registrierung, Login, Passwort-Reset
- Email-Verifizierung automatisch beim Register
- ChatInterface integriert mit echtem Firebase Auth
- User-Profile in Firestore mit Query-Limits

### ✅ Task 3: Stripe Checkout (Teilweise)
- `/src/lib/stripe.ts` - Stripe Client SDK
- `/src/components/CheckoutModalV2.tsx` - Verbessertes Checkout
- @stripe/stripe-js installiert
- Stripe Redirect-Flow vorbereitet

---

## 🚀 NOCH ZU ERLEDIGEN

### Task 3: Stripe Backend + Webhooks
**Erforderlich für Production:**

1. **Backend Stripe Endpunkte** (in `/backend/main.py` oder neue `/backend/payments/stripe_handler.py`):
   ```python
   @app.post("/stripe/create-checkout-session")
   async def create_checkout_session(request: CheckoutRequest):
       stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
       
       session = stripe.checkout.Session.create(
           payment_method_types=['card', 'sepa_debit'],
           line_items=[{
               'price': request.price_id,
               'quantity': 1,
           }],
           mode='subscription',
           success_url=request.success_url,
           cancel_url=request.cancel_url,
           customer_email=request.customer_email,
           metadata={'user_id': request.user_id, 'plan_name': request.plan_name}
       )
       
       return {"session_id": session.id}
   
   @app.post("/stripe/webhook")
   async def stripe_webhook(request: Request):
       payload = await request.body()
       sig_header = request.headers.get('stripe-signature')
       
       event = stripe.Webhook.construct_event(
           payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
       )
       
       if event['type'] == 'checkout.session.completed':
           session = event['data']['object']
           # Update Firestore: User Plan + Subscription ID
           await update_user_subscription(
               user_id=session.metadata.user_id,
               plan=session.metadata.plan_name,
               stripe_customer_id=session.customer,
               stripe_subscription_id=session.subscription
           )
       
       elif event['type'] == 'customer.subscription.deleted':
           subscription = event['data']['object']
           # Downgrade User to Free
           await downgrade_user_to_free(subscription.metadata.user_id)
       
       return {"received": True}
   ```

2. **Stripe Dashboard Setup:**
   - Produkte erstellen (9€, 29€, 49€)
   - Price IDs in `.env` speichern:
     ```
     STRIPE_SECRET_KEY=sk_live_...
     STRIPE_WEBHOOK_SECRET=whsec_...
     NEXT_PUBLIC_STRIPE_PRICE_MIETER_PLUS=price_...
     NEXT_PUBLIC_STRIPE_PRICE_PROFESSIONAL=price_...
     NEXT_PUBLIC_STRIPE_PRICE_LAWYER=price_...
     ```
   - Webhook URL: `https://domulex-backend-841507936108.europe-west3.run.app/stripe/webhook`

### Task 4: Email-Templates
**Sendgrid/Mailgun Integration:**

1. **Willkommens-Email** (nach Registrierung):
   ```
   Betreff: Willkommen bei Domulex.ai! 🏛️
   - Email-Verifizierung Link
   - Erste Schritte
   - Free-Plan Features
   ```

2. **Bestellbestätigung** (nach erfolgreichem Checkout):
   ```
   Betreff: Ihre Bestellung bei Domulex.ai
   - Rechnung als PDF
   - Abo-Details
   - Widerrufsbelehrung (für Verbraucher)
   - Link zum Customer Portal
   ```

3. **Monatliche Rechnung** (via Stripe automatisch):
   ```
   Betreff: Ihre monatliche Rechnung
   - PDF-Anhang
   - Zahlungsdetails
   - Abo-Status
   ```

### Task 5: Monatliche Abrechnung
**Bereits durch Stripe Subscriptions gelöst:**
- Stripe charged automatisch jeden Monat
- Webhooks informieren über erfolgreiche/fehlgeschlagene Zahlungen
- Query-Counter Reset: Cloud Function schreiben:
  ```python
  # Firebase Cloud Function
  @scheduler('every day 00:00')
  def reset_monthly_queries():
      users = firestore.collection('users').where('queriesUsed', '>', 0).get()
      for user in users:
          user.reference.update({'queriesUsed': 0})
  ```

### Task 6: KI-Support System
**Chatbot für Support-Fragen:**

1. **Support-Chat in `/src/app/hilfe/page.tsx`**:
   - Separate ChatInterface-Instanz
   - Persona: "Support-Agent"
   - Fragen zu Registrierung, Abos, Kündigungen

2. **Email-Support-Ticket** (Fallback):
   - Formular sendet Email an support@domulex.ai
   - Auto-Reply mit Ticket-Nummer

### Task 7: User Dashboard
**Abo-Verwaltung in `/src/app/konto/page.tsx` erweitern:**

```tsx
// Stripe Customer Portal öffnen
const openCustomerPortal = async () => {
  const { url } = await createPortalSession(userProfile.stripeCustomerId);
  window.location.href = url;
};

// Features:
- Aktueller Plan anzeigen
- Nutzungsstatistik (Queries used/limit)
- "Plan ändern" Button → Customer Portal
- "Kündigen" Button → Customer Portal
- Rechnungshistorie (via Stripe)
```

---

## 📋 DEPLOYMENT CHECKLIST

### Environment Variables setzen:
```bash
# Firebase
firebase functions:config:set \
  stripe.secret_key="sk_live_..." \
  stripe.webhook_secret="whsec_..." \
  sendgrid.api_key="SG...."

# Next.js (.env.production)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_STRIPE_PRICE_MIETER_PLUS=price_...
NEXT_PUBLIC_STRIPE_PRICE_PROFESSIONAL=price_...
NEXT_PUBLIC_STRIPE_PRICE_LAWYER=price_...
```

### Build & Deploy:
```bash
npm run build
firebase deploy --only hosting
cd backend && gcloud run deploy domulex-backend --source .
```

### Testen:
1. Registrierung mit Test-Email
2. Email-Verifizierung Link klicken
3. 3 kostenlose Fragen stellen
4. Upgrade-Modal erscheint
5. Stripe Test-Checkout durchlaufen
6. Webhook Test: `stripe listen --forward-to localhost:8000/stripe/webhook`

---

## 🎯 PRIORITÄTEN FÜR MORGEN

**HIGHEST PRIORITY:**
1. Stripe Backend Endpoints implementieren
2. Webhook Handler fertigstellen
3. Stripe Dashboard Produkte erstellen
4. Production-Deploy testen

**MEDIUM PRIORITY:**
5. Email-Templates (Sendgrid)
6. Query Reset Cloud Function
7. User Dashboard erweitern

**LOW PRIORITY:**
8. KI-Support Chat
9. Analytics Integration
10. Invoice PDF Generation

---

## 📞 NÄCHSTE SCHRITTE MIT USER

Dem User zeigen:
1. ✅ Was bereits funktioniert (Auth, Checkout-UI)
2. ⏳ Was noch fehlt (Backend Stripe Integration)
3. 📝 Welche Keys/Zugänge benötigt werden
4. 🚀 Timeline für Fertigstellung (2-3 Tage)
