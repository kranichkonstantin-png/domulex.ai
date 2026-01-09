# ================================================
# DOMULEX STRIPE SETUP GUIDE
# ================================================

## 🚀 Quick Start

You've provided the Stripe publishable key, but we need a few more pieces to complete the integration:

### 1. Get Your Stripe SECRET Key

The key you provided (`stpk_live_51S402X...`) appears to be a PUBLISHABLE key (used in frontend).

**You also need the SECRET key (used in backend):**

1. Go to: https://dashboard.stripe.com/apikeys
2. Find the **Secret key** section
3. Copy the key that starts with `sk_live_...` 
4. Add it to `.env.production`:
   ```
   STRIPE_SECRET_KEY=sk_live_YOUR_ACTUAL_SECRET_KEY
   ```

⚠️ **IMPORTANT:** Never commit the secret key to Git or expose it in frontend code!

---

### 2. Create Products in Stripe Dashboard

Create 3 subscription products for your tiers:

#### **Mieter Plus (TENANT) - 19€/month**
✅ **COMPLETED**
- Price ID: `price_1Sj8l83LV15CfXasN3zUqv2v`
- Name: "Domulex Mieter Plus"
- Description: "100 Fragen pro Monat, Erweiterte Mieter-Perspektive, Musterbriefe"
- Pricing: Recurring, Monthly, 19.00 EUR (inkl. 19% MwSt.)

#### **Professional (PRO) - 39€/month**
⏳ **TO CREATE**
1. Go to: https://dashboard.stripe.com/products/create
2. Name: "Domulex Professional"
3. Description: "500 Fragen, PDF-Vertragsanalyse, Alle Rollen (Mieter/Vermieter/Eigentümer/Investor)"
4. Pricing: Recurring, Monthly, 39.00 EUR (inkl. 19% MwSt.)
5. Copy Price ID and provide it

#### **Lawyer Pro (LAWYER) - 69€/month**
⏳ **TO CREATE**
1. Go to: https://dashboard.stripe.com/products/create
2. Name: "Domulex Lawyer Pro"
3. Description: "1000 Fragen, Anwalts-Modus, Schriftsatz-Generierung, CRM & Dokumentenmanagement, KI-Aktenanalyse"
4. Pricing: Recurring, Monthly, 69.00 EUR (inkl. 19% MwSt.)
5. Copy Price ID and provide it

---

### 3. Set Up Webhooks

Webhooks notify your backend when payments succeed, subscriptions are created/cancelled, etc.

1. Go to: https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. Endpoint URL: `https://domulex-backend-841507936108.europe-west3.run.app/stripe/webhook`
4. Description: "Domulex subscription events"
5. Select events to listen for:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
6. Click "Add endpoint"
7. Copy the **Signing secret** (starts with `whsec_...`)
8. Add to `.env.production`:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET
   ```

---

### 4. Configure Payment Methods

Enable payment methods for the German market:

1. Go to: https://dashboard.stripe.com/settings/payment_methods
2. Enable:
   - ✅ Cards (Visa, Mastercard, Amex)
   - ✅ SEPA Direct Debit (popular in Germany)
   - ✅ giropay (German bank transfers)
   - ✅ Sofort (optional, popular in DE/AT)

---

### 5. Update Environment Variables

After completing steps 1-3, your `.env.production` should look like:

```env
# Stripe Keys (PRODUCTION - AKTIV)
# ⚠️ NIEMALS echte Keys committen! Hole sie aus Google Cloud Secret Manager
STRIPE_SECRET_KEY=sk_test_YOUR_STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET

# Stripe Price IDs (PRODUCTION - AKTIV)
STRIPE_PRICE_TENANT=price_1Sj8l83LV15CfXasN3zUqv2v
STRIPE_PRICE_PRO=price_1Siuom3LV15CfXasXmpE2LCt
STRIPE_PRICE_LAWYER=price_1Siutl3LV15CfXas4Mxel6SS
```

---

### 6. Deploy to Google Cloud Run

Once environment variables are configured:

```bash
# Backend deployment with Stripe env vars
cd /Users/konstantinkranich/domulex.ai/backend
# Verwende Google Cloud Secret Manager für sensible Daten:
gcloud run deploy domulex-backend \
  --source . \
  --region europe-west3 \
  --set-secrets "STRIPE_SECRET_KEY=stripe-secret-key:latest,STRIPE_WEBHOOK_SECRET=stripe-webhook-secret:latest" \
  --set-env-vars "STRIPE_PRICE_TENANT=price_1Sj8l83LV15CfXasN3zUqv2v,STRIPE_PRICE_PRO=price_1Siuom3LV15CfXasXmpE2LCt,STRIPE_PRICE_LAWYER=price_1Siutl3LV15CfXas4Mxel6SS" \
  --quiet

# Frontend deployment
cd /Users/konstantinkranich/domulex.ai
firebase deploy --only hosting
```

**Or** use Cloud Run web console:
1. Go to: https://console.cloud.google.com/run
2. Select `domulex-backend`
3. Click "Edit & Deploy New Revision"
4. Go to "Variables & Secrets" tab
5. Add environment variables
6. Deploy

---

### 7. Test Payment Flow

1. Visit: https://domulex-frontend-841507936108.europe-west3.run.app
2. Click "Jetzt kostenlos starten"
3. Click "Upgrade" in the pricing table
4. You'll be redirected to Stripe Checkout
5. Use test card: `4242 4242 4242 4242`
6. Any future date, any CVC
7. Complete checkout
8. You should be redirected back with success message

---

## 📝 Additional Notes

### Test Mode vs Live Mode

- Your key appears to be a **LIVE** key (`pk_live_...`)
- For testing, use **TEST** keys instead (`pk_test_...` and `sk_test_...`)
- Switch to test mode in Stripe Dashboard (top-left toggle)

### Security Checklist

- ✅ Secret key stored only in backend environment (never in code)
- ✅ Webhook signature verification enabled
- ✅ HTTPS enforced on all endpoints
- ✅ CORS configured for your frontend domain
- ✅ No sensitive keys in frontend code or Git

### Customer Portal

Users can manage their subscriptions at:
```
https://domulex-frontend-841507936108.europe-west3.run.app/subscription_settings
```

This redirects to Stripe Customer Portal where they can:
- Update payment method
- Download invoices
- Cancel subscription
- View billing history

---

## 🆘 Troubleshooting

### "No such price: price_..."
- Price IDs are wrong or not created in Stripe Dashboard
- Make sure you're in the correct mode (test vs live)

### Webhook not receiving events
- Check webhook URL is publicly accessible
- Verify signing secret is correct
- Check Cloud Run logs for errors

### Payment succeeds but subscription not activated
- Check webhook handler in backend logs
- Verify database update logic
- Check Stripe webhook dashboard for delivery status

---

## 📚 Resources

- Stripe Dashboard: https://dashboard.stripe.com
- Stripe Docs: https://stripe.com/docs/billing/subscriptions/build-subscriptions
- Test Cards: https://stripe.com/docs/testing

---

Need help? Check the Stripe Dashboard logs or backend Cloud Run logs for detailed error messages.
