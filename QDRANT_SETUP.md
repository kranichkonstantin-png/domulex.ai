# DOMULEX.ai - Qdrant Setup Guide

## Option 1: Qdrant Cloud (Empfohlen für Produktion)

### Schritte:
1. Gehe zu https://cloud.qdrant.io/
2. Erstelle kostenlosen Account
3. Erstelle neuen Cluster (Free Tier: 1GB)
4. Kopiere:
   - **Cluster URL:** z.B. `https://xyz-abc.eu-central.aws.cloud.qdrant.io:6333`
   - **API Key:** (Optional, aber empfohlen)

5. Update Backend Environment Variables:
```bash
QDRANT_HOST=<your-cluster-url>
QDRANT_API_KEY=<your-api-key>  # Optional
```

## Option 2: Cloud Run Qdrant (Aktuell deployed)

**Status:** ✅ Deployed aber nicht erreichbar von anderen Cloud Run Services
**URL:** https://domulex-qdrant-841507936108.europe-west3.run.app
**Problem:** Cloud Run Services können sich nicht direkt verbinden ohne VPC

**Lösung:** VPC Connector einrichten oder Qdrant Cloud verwenden

## Option 3: Lokales Development

```bash
docker-compose -f qdrant-docker-compose.yml up -d
```

Dann Backend mit:
```bash
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_USE_HTTPS=false
```

---

## Aktueller Status

- ✅ Qdrant Container auf Cloud Run deployed
- ⚠️ Backend kann sich nicht verbinden (VPC benötigt)
- 💡 **Empfehlung:** Qdrant Cloud verwenden (kostenlos + einfacher)

---

## Nächste Schritte

1. Qdrant Cloud Account erstellen
2. Cluster URL + API Key in Backend konfigurieren
3. Backend neu deployen
4. Legal Documents ingesten
