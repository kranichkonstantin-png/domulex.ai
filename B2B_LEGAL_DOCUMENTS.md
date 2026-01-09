# B2B Vertragsdokumente - AVV & NDA

## Übersicht

Für gewerbliche Kunden (B2B) werden bei Vertragsabschluss automatisch folgende Dokumente Bestandteil des Vertrags:

1. **AVV (Auftragsverarbeitungsvertrag)** - gemäß Art. 28 DSGVO
2. **NDA (Geheimhaltungsvereinbarung)** - für vertrauliche Geschäftsdaten

## Checkout-Prozess

### 1. Kundentyp-Auswahl

Im Checkout-Modal (`CheckoutModalV2.tsx`) wählt der Kunde:

- **Privat (Verbraucher)**: 14 Tage Widerrufsrecht, Widerrufsbelehrung akzeptieren
- **Geschäftlich (Unternehmer)**: Kein Widerrufsrecht, AVV + NDA werden angezeigt

### 2. B2B-Checkboxen

Bei Auswahl "Geschäftlich" erscheint:

```
Für gewerbliche Kunden gelten zusätzlich:
- 📋 Auftragsverarbeitungsvertrag (AVV) gemäß Art. 28 DSGVO
- 🔒 Geheimhaltungsvereinbarung (NDA) für vertrauliche Geschäftsdaten

Mit Ihrer Bestellung werden AVV und NDA automatisch Vertragsbestandteil.
```

### 3. E-Mail-Versand

Nach erfolgreicher Bestellung erhält der B2B-Kunde eine spezielle E-Mail mit:

- Bestellbestätigung
- Links zu: AGB, Datenschutz, AVV, NDA
- Rechnung (PDF-Link)
- Hinweis: Kein Widerrufsrecht für Unternehmer

## URLs

- **AVV**: https://domulex.ai/avv
- **NDA**: https://domulex.ai/nda
- **AGB**: https://domulex.ai/agb
- **Datenschutz**: https://domulex.ai/datenschutz

## E-Mail-Funktion

### B2B-Bestellbestätigung

```python
email_service.send_order_confirmation_b2b(
    user_email="firma@example.de",
    user_name="Max Mustermann",
    company_name="Musterfirma GmbH",
    plan_name="Lawyer Pro",
    plan_price=79.00,
    subscription_id="sub_xxx",
    invoice_url="https://stripe.com/invoice/xxx"
)
```

### Inhalt der E-Mail

1. ✅ Bestellbestätigung (B2B)
2. Firmenname + Ansprechpartner
3. Tarif + Preis (netto, zzgl. MwSt.)
4. **Vertragsbestandteile-Box**:
   - AGB
   - Datenschutzhinweise
   - AVV (Art. 28 DSGVO)
   - NDA
5. Rechnung (PDF)
6. Hinweise für B2B-Kunden
7. Sicherheitsinfos (Serverstandort, Verschlüsselung)

## AVV-Inhalte

### Struktur

1. § 1 Gegenstand und Dauer der Verarbeitung
2. § 2 Art und Zweck der Verarbeitung
3. § 3 Art der personenbezogenen Daten
4. § 4 Kategorien betroffener Personen
5. § 5 Pflichten des Auftragnehmers
6. § 6 Technische und organisatorische Maßnahmen (TOMs)
7. § 7 Unterauftragnehmer
8. § 8 Rechte der betroffenen Personen
9. § 9 Meldepflichten bei Datenschutzverletzungen
10. § 10 Kontrollrechte des Auftraggebers
11. § 11 Löschung und Rückgabe von Daten
12. § 12 Haftung
13. § 13 Schlussbestimmungen

### Unterauftragnehmer

| Unterauftragnehmer | Zweck | Standort |
|---|---|---|
| Google Cloud Platform | Hosting, Datenbank | Frankfurt, DE |
| Firebase (Google) | Authentifizierung, Firestore | Frankfurt, DE |
| Qdrant Cloud | Vektordatenbank für RAG | Frankfurt, DE |
| Google Gemini API | KI-Verarbeitung | EU (Zero Data Retention) |
| Stripe Inc. | Zahlungsabwicklung | Dublin, IE |
| Resend | E-Mail-Versand | EU |

## NDA-Inhalte

### Struktur

1. § 1 Vertragsparteien
2. § 2 Gegenstand der Vereinbarung
3. § 3 Definition vertraulicher Informationen
4. § 4 Ausnahmen von der Vertraulichkeit
5. § 5 Pflichten der Parteien
6. § 6 Zulässige Offenlegung
7. § 7 Technische Schutzmaßnahmen
8. § 8 Berufsgeheimnisträger (§ 203 StGB)
9. § 9 Rückgabe und Löschung
10. § 10 Dauer der Vereinbarung
11. § 11 Vertragsstrafe
12. § 12 Rechtsbehelfe
13. § 13 Meldepflicht bei Sicherheitsvorfällen
14. § 14 Schlussbestimmungen

### Geheimhaltungsdauer

- **Allgemeine Geschäftsinformationen**: 5 Jahre nach Vertragsende
- **Mandantengeheimnisse**: Unbefristet

### Vertragsstrafe

- Einfache Fahrlässigkeit: bis zu 10.000 €
- Grobe Fahrlässigkeit/Vorsatz: bis zu 50.000 €

## Integration

### Frontend-Dateien

- `/src/app/avv/page.tsx` - AVV-Seite
- `/src/app/nda/page.tsx` - NDA-Seite
- `/src/components/CheckoutModalV2.tsx` - Checkout mit B2B-Hinweisen

### Backend-Dateien

- `/backend/services/email_service.py` - `send_order_confirmation_b2b()`

### Footer-Links

Die AVV und NDA sind im Footer der Landing Page unter "Rechtliches" verlinkt (mit "(B2B)" Kennzeichnung).

## Rechtliche Grundlagen

- **AVV**: Art. 28 DSGVO - Auftragsverarbeitung
- **NDA**: Allgemeines Vertragsrecht (BGB)
- **§ 203 StGB**: Für Rechtsanwälte als Berufsgeheimnisträger
- **§ 312g Abs. 2 Nr. 1 BGB**: Kein Widerrufsrecht für Unternehmer

## Kontakt

- **Datenschutz**: datenschutz@domulex.ai
- **Rechtsabteilung**: legal@domulex.ai
- **Business**: business@domulex.ai
