# Email Setup - SendGrid für Domulex.ai

## 1. SendGrid Account & API Key

### Account erstellen
1. Gehe zu https://sendgrid.com
2. Registriere dich oder logge dich ein
3. Free Plan: 100 E-Mails/Tag kostenlos

### API Key erstellen
1. Settings → API Keys
2. "Create API Key"
3. Name: `domulex-backend`
4. Permissions: **Full Access**
5. Key kopieren und sicher speichern (wird nur einmal angezeigt!)

### Environment Variable setzen
```bash
# Backend (.env oder Cloud Run)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@domulex.ai
FROM_NAME=Domulex.ai
```

---

## 2. Domain-Authentifizierung (KRITISCH!)

### Warum notwendig?
- Ohne Domain-Verifizierung landen E-Mails im Spam
- SPF/DKIM verhindert Phishing-Warnungen
- Höhere Zustellrate (>95% statt ~30%)

### Domain verifizieren
1. SendGrid → Settings → **Sender Authentication**
2. **Domain Authentication** → "Authenticate Your Domain"
3. DNS-Provider: **Andere** (oder dein Provider)
4. Domain eingeben: `domulex.ai`
5. Subdomain für Links: `em8125.domulex.ai` (SendGrid schlägt vor)

### DNS-Records hinzufügen
SendGrid zeigt dir **3 DNS-Records**, die du bei deinem Domain-Provider (z.B. Google Domains, Cloudflare, etc.) hinzufügen musst:

#### Record 1: CNAME für DKIM (Signatur)
```
Type: CNAME
Host: s1._domainkey.domulex.ai
Value: s1.domainkey.u12345678.wl125.sendgrid.net
TTL: 3600
```

#### Record 2: CNAME für DKIM (Signatur 2)
```
Type: CNAME
Host: s2._domainkey.domulex.ai
Value: s2.domainkey.u12345678.wl125.sendgrid.net
TTL: 3600
```

#### Record 3: CNAME für Tracking
```
Type: CNAME
Host: em8125.domulex.ai
Value: u12345678.wl125.sendgrid.net
TTL: 3600
```

**Hinweis:** Die genauen Werte (`u12345678.wl125`) zeigt dir SendGrid an - kopiere sie genau!

### Verifizierung prüfen
1. DNS-Records hinzufügen (kann bis zu 48h dauern, meist <1h)
2. Zurück zu SendGrid → "Verify" klicken
3. ✅ Status sollte "Verified" zeigen

---

## 3. Single Sender Verification (Alternative für Test)

Falls du **noch keine Domain** verifizieren kannst:

1. Settings → **Sender Authentication**
2. **Single Sender Verification**
3. E-Mail eingeben: z.B. `info@domulex.ai` oder deine persönliche E-Mail
4. Bestätigungs-Link in E-Mail klicken
5. ⚠️ Nur für Tests! Production braucht Domain-Auth

---

## 4. Backend Deployment mit Email-Service

### Lokaler Test (optional)
```bash
cd backend

# .env erstellen
cat > .env << EOF
SENDGRID_API_KEY=SG.xxxxxxxxx
FROM_EMAIL=noreply@domulex.ai
FROM_NAME=Domulex.ai
EOF

# Email-Service testen
python -c "
from services.email_service import email_service
result = email_service.send_welcome_email('deine@email.de', 'Test User')
print('Email sent!' if result else 'Failed!')
"
```

### Cloud Run Deployment
```bash
# Environment Variables in Cloud Run setzen
gcloud run services update domulex-backend \
  --region=europe-west3 \
  --update-env-vars=SENDGRID_API_KEY=SG.xxxxxxxxx,FROM_EMAIL=noreply@domulex.ai,FROM_NAME=Domulex.ai

# Backend neu deployen mit Email-Service
cd backend
gcloud run deploy domulex-backend \
  --source . \
  --region=europe-west3 \
  --allow-unauthenticated
```

---

## 5. Firebase Cloud Functions Deployment

### Functions deployen
```bash
cd /Users/konstantinkranich/domulex.ai

# Dependencies installieren (lokal testen)
cd functions
pip install -r requirements.txt

# Alle Functions deployen
firebase deploy --only functions

# Oder einzelne Function:
firebase deploy --only functions:on_user_created
firebase deploy --only functions:send_order_confirmation
firebase deploy --only functions:reset_monthly_queries
```

### Functions testen
```bash
# Welcome Email testen (triggert automatisch bei User-Registrierung)
# → Einfach neuen User in Firebase Auth erstellen

# Order Confirmation testen
curl -X POST https://us-central1-domulex-ai.cloudfunctions.net/send_order_confirmation \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "test@example.com",
    "user_name": "Test User",
    "plan_name": "Mieter Plus",
    "plan_price": "9.00",
    "subscription_id": "sub_test123"
  }'
```

---

## 6. Email-Vorlagen übersicht

### Automatische E-Mails (via Webhooks/Functions)

| Trigger | Email-Type | Versandt durch |
|---------|-----------|----------------|
| User registriert sich | **Willkommens-Email** | Firebase Function `on_user_created` |
| Firebase Auth | **Email-Verifizierung** | Firebase Auth (automatisch) |
| Passwort vergessen | **Passwort-Reset** | Firebase Auth (automatisch) |
| Stripe Checkout erfolgreich | **Bestellbestätigung** | Stripe Webhook → Backend |
| Zahlung fehlgeschlagen | **Payment Failed** | Stripe Webhook → Backend |
| Abo gekündigt | **Kündigungs-Bestätigung** | Stripe Webhook → Backend |
| 1. des Monats | **Monatliche Rechnung** | Stripe automatisch |

### E-Mail Inhalte

#### Willkommens-Email
- ✅ Features des Free Plans
- ✅ "Jetzt loslegen" CTA-Button
- ✅ Nächste Schritte
- ✅ Links: Datenschutz, AGB, Impressum

#### Bestellbestätigung
- ✅ Rechnungsdetails (Plan, Preis, Subscription-ID)
- ✅ Link zur Rechnung (Stripe Invoice)
- ✅ **Widerrufsbelehrung** (§ 312j/k BGB)
- ✅ Widerrufsformular-Link
- ✅ AGB & Datenschutz-Links
- ✅ Kundenkonto-Link

#### Payment Failed
- ✅ Freundliche Benachrichtigung
- ✅ "Zahlungsmethode aktualisieren" Button
- ✅ Support-Kontakt

#### Kündigungs-Bestätigung
- ✅ Ende der Laufzeit
- ✅ Dankeschön-Nachricht
- ✅ Feedback-Möglichkeit

---

## 7. Monitoring & Testing

### SendGrid Dashboard
- **Activity**: Zeigt alle versendeten E-Mails
- **Statistics**: Zustellrate, Bounces, Spam-Reports
- **Alerts**: Bei hoher Bounce-Rate

### Test-Checkliste
```bash
# 1. Neue Registrierung → Welcome Email
# Browser: https://domulex-ai.web.app → Registrieren
# ✅ Check: E-Mail erhalten?

# 2. Checkout → Order Confirmation
# Browser: https://domulex-ai.web.app → Upgrade → Zahlen
# ✅ Check: Bestellbestätigung mit Widerruf erhalten?

# 3. Payment Failed (Test in Stripe)
# Stripe Dashboard → Subscriptions → Simulate failed payment
# ✅ Check: Payment-Failed E-Mail erhalten?

# 4. Kündigung → Cancellation Email
# Browser: https://domulex-ai.web.app/konto → Abo verwalten → Kündigen
# ✅ Check: Kündigungs-Email erhalten?
```

---

## 8. DSGVO-Konformität

### In allen E-Mails enthalten:
- ✅ Firmenadresse (Home Invest & Management GmbH)
- ✅ Link zur Datenschutzerklärung
- ✅ Link zu AGB
- ✅ Link zum Impressum
- ✅ Abmeldemöglichkeit (bei Marketing-E-Mails)

### E-Mail-Aufbewahrung
- **Transaktions-E-Mails**: 10 Jahre (steuerlich)
- **Marketing-E-Mails**: Nur mit Einwilligung
- **Logs**: SendGrid löscht nach 30 Tagen

### Opt-Out
- Transaktions-E-Mails (Bestellbestätigungen): **Pflicht**, kein Opt-Out
- Marketing-E-Mails: Unsubscribe-Link erforderlich (TODO wenn Newsletter)

---

## 9. Kosten-Übersicht

### SendGrid Pricing
- **Free**: 100 E-Mails/Tag (3.000/Monat) - ✅ Für Start ausreichend
- **Essentials**: $15/Monat - 50.000 E-Mails
- **Pro**: $90/Monat - 1.5M E-Mails

### Geschätzte Nutzung (Monat 1)
- Registrierungen: ~100 → 100 Welcome-E-Mails
- Conversions (5%): ~5 → 5 Bestellbestätigungen
- Payment Failed (1%): ~0.05 → 1 E-Mail
- **Total**: ~106 E-Mails/Monat → **Free Plan reicht!**

---

## 10. Nächste Schritte

### Sofort:
1. ✅ SendGrid Account erstellen
2. ✅ API Key generieren
3. ✅ Domain `domulex.ai` authentifizieren (DNS-Records)
4. ⏳ Backend mit ENV vars deployen
5. ⏳ Firebase Functions deployen
6. ⏳ Test-Registrierung durchführen

### Optional (später):
- [ ] Custom Email-Templates in SendGrid Editor
- [ ] Monatlicher Newsletter (mit Opt-In)
- [ ] Email-Analytics Dashboard
- [ ] A/B Testing für E-Mail-Betreffzeilen
- [ ] Transactional Email-Tracking (Öffnungsrate etc.)

---

## Support & Troubleshooting

### E-Mail kommt nicht an?
1. **Spam-Ordner prüfen**
2. SendGrid Activity Log prüfen: Wurde E-Mail versendet?
3. Bounce-Reason prüfen: Hard bounce = ungültige Adresse
4. Domain-Authentifizierung prüfen: Status "Verified"?

### "API key permissions invalid"
- API Key braucht **Full Access** oder mindestens **Mail Send**
- Neuen Key erstellen wenn unsicher

### DNS-Records nicht erkannt?
- DNS-Änderungen brauchen 1-48h (meist <1h)
- `dig CNAME s1._domainkey.domulex.ai` zum Testen
- TTL auf 3600 setzen

### Fragen?
- SendGrid Docs: https://docs.sendgrid.com
- Support: support@sendgrid.com
- Domulex Backend Logs: `gcloud run logs read domulex-backend`

---

**Status:** ⏳ Pending - Domain-Authentifizierung erforderlich
**Priority:** 🔴 HIGH - Ohne E-Mails kein kompletter Automatismus
**Zeitaufwand:** 30 Minuten (Setup) + 1h (DNS-Propagation)
