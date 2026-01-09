"""
DOMULEX - Subscription & Billing Module
Single subscription with role switching
"""

from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
import streamlit as st


class SubscriptionTier(Enum):
    """Subscription tiers."""
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"


class SubscriptionStatus(Enum):
    """Subscription status."""
    ACTIVE = "active"
    TRIAL = "trial"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


# Pricing (Monthly in EUR)
PRICING = {
    SubscriptionTier.FREE: {
        "price": 0,
        "queries_per_month": 10,
        "features": [
            "✅ 10 Fragen pro Monat",
            "✅ Basis-KI-Antworten",
            "✅ 1 Jurisdiktion",
            "❌ Keine Dokumenten-Uploads",
            "❌ Kein Experten-Support",
        ],
    },
    SubscriptionTier.PRO: {
        "price": 29,
        "queries_per_month": 500,
        "features": [
            "✅ 500 Fragen pro Monat",
            "✅ KI mit Rechtsquellen (RAG)",
            "✅ Alle 3 Jurisdiktionen (DE/US/ES)",
            "✅ PDF-Upload & Analyse",
            "✅ Alle 4 Rollen wechselbar",
            "✅ Streitschlichtungs-Assistent",
            "✅ Email-Support (48h)",
            "✅ Export als PDF",
        ],
    },
    SubscriptionTier.BUSINESS: {
        "price": 99,
        "queries_per_month": 2500,
        "features": [
            "✅ 2.500 Fragen pro Monat",
            "✅ Alle PRO Features",
            "✅ API-Zugriff (REST)",
            "✅ Team-Accounts (bis 5 User)",
            "✅ Priority Support (24h)",
            "✅ Bulk-PDF-Analyse",
            "✅ Custom Branding",
            "✅ Dedicated Account Manager",
        ],
    },
}


def get_user_subscription() -> dict:
    """
    Get user's subscription status.
    In production: Fetch from Firebase/Firestore.
    For demo: Use session state.
    """
    if "subscription" not in st.session_state:
        # Default: Free trial for 7 days
        st.session_state.subscription = {
            "tier": SubscriptionTier.PRO,  # Trial of PRO
            "status": SubscriptionStatus.TRIAL,
            "queries_used": 0,
            "queries_limit": PRICING[SubscriptionTier.PRO]["queries_per_month"],
            "trial_end": datetime.now() + timedelta(days=7),
            "next_billing_date": None,
        }
    return st.session_state.subscription


def check_query_quota() -> tuple[bool, str]:
    """
    Check if user has quota for a query.
    Returns: (allowed, message)
    """
    sub = get_user_subscription()
    
    # Check trial expiry
    if sub["status"] == SubscriptionStatus.TRIAL:
        if datetime.now() > sub["trial_end"]:
            sub["status"] = SubscriptionStatus.EXPIRED
            return False, "⚠️ Ihre Testphase ist abgelaufen. Bitte upgraden Sie."
    
    # Check quota
    if sub["queries_used"] >= sub["queries_limit"]:
        return False, f"⚠️ Monatliches Limit erreicht ({sub['queries_limit']} Fragen). Upgraden Sie für mehr."
    
    return True, ""


def increment_query_count():
    """Increment query counter."""
    if "subscription" in st.session_state:
        st.session_state.subscription["queries_used"] += 1


def render_subscription_widget():
    """Render subscription status widget in sidebar."""
    sub = get_user_subscription()
    tier = sub["tier"]
    status = sub["status"]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💳 Abonnement")
    
    # Status badge
    if status == SubscriptionStatus.TRIAL:
        days_left = (sub["trial_end"] - datetime.now()).days
        st.sidebar.info(f"🎁 **TRIAL** - {days_left} Tage verbleibend")
    elif status == SubscriptionStatus.ACTIVE:
        st.sidebar.success(f"✅ **{tier.value.upper()}** aktiv")
    elif status == SubscriptionStatus.EXPIRED:
        st.sidebar.error("⚠️ **ABGELAUFEN**")
    
    # Usage bar
    used = sub["queries_used"]
    limit = sub["queries_limit"]
    percentage = (used / limit) * 100 if limit > 0 else 100
    
    st.sidebar.markdown(f"**Nutzung:** {used} / {limit} Fragen")
    st.sidebar.progress(min(percentage / 100, 1.0))
    
    # Upgrade button
    if tier != SubscriptionTier.BUSINESS:
        if st.sidebar.button("⬆️ Upgrade", use_container_width=True):
            st.session_state.show_pricing = True
            st.rerun()


def render_pricing_page():
    """Render pricing comparison page."""
    st.markdown("# 💎 DOMULEX Preise")
    st.markdown("**Ein Abo, alle Rollen** - Wechseln Sie frei zwischen Mieter, Investor, Verwalter und Anwalt")
    st.markdown("---")
    
    cols = st.columns(3)
    
    for idx, (tier, details) in enumerate(PRICING.items()):
        with cols[idx]:
            # Card styling
            if tier == SubscriptionTier.PRO:
                st.markdown("### 🌟 PRO (EMPFOHLEN)")
            else:
                st.markdown(f"### {tier.value.upper()}")
            
            # Price
            price = details["price"]
            if price == 0:
                st.markdown("## KOSTENLOS")
            else:
                st.markdown(f"## €{price}/Monat")
            
            # Features
            for feature in details["features"]:
                st.markdown(feature)
            
            # CTA button
            if tier == SubscriptionTier.FREE:
                st.button("Aktueller Plan", disabled=True, key=f"btn_{tier.value}")
            else:
                if st.button(f"Wählen - €{price}/Monat", key=f"btn_{tier.value}", type="primary" if tier == SubscriptionTier.PRO else "secondary"):
                    st.session_state.selected_tier = tier
                    st.session_state.show_checkout = True
                    st.rerun()
    
    # FAQ
    st.markdown("---")
    st.markdown("### ❓ Häufig gestellte Fragen")
    
    with st.expander("Kann ich zwischen Rollen wechseln?"):
        st.markdown("""
        **Ja!** Mit einem Abonnement können Sie frei zwischen allen 4 Rollen wechseln:
        - 👤 Mieter-Modus
        - 💼 Investor-Modus
        - 🏢 Verwalter-Modus
        - ⚖️ Anwalt-Modus
        
        Keine Extrakosten, keine Einschränkungen.
        """)
    
    with st.expander("Welche Zahlungsmethoden akzeptieren Sie?"):
        st.markdown("""
        - 💳 Kreditkarte (Visa, Mastercard, Amex)
        - 🏦 SEPA-Lastschrift
        - 💰 PayPal
        
        Alle Zahlungen werden sicher über Stripe abgewickelt.
        """)
    
    with st.expander("Kann ich jederzeit kündigen?"):
        st.markdown("""
        **Ja, jederzeit!** 
        
        - Keine Kündigungsfrist
        - Keine versteckten Gebühren
        - Zugriff bis Ende des bezahlten Zeitraums
        """)
    
    with st.expander("Gibt es eine Testphase?"):
        st.markdown("""
        **7 Tage kostenlos** für PRO-Funktionen!
        
        - Keine Kreditkarte erforderlich
        - Voller Zugriff auf alle Features
        - Automatische Umstellung auf FREE nach Ablauf (wenn nicht upgraded)
        """)


def render_checkout_page():
    """Render checkout/payment page."""
    tier = st.session_state.get("selected_tier", SubscriptionTier.PRO)
    details = PRICING[tier]
    
    st.markdown(f"# 💳 Checkout: {tier.value.upper()}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Zahlungsinformationen")
        
        # Payment form (mock)
        payment_method = st.radio(
            "Zahlungsmethode",
            ["💳 Kreditkarte", "🏦 SEPA-Lastschrift", "💰 PayPal"],
        )
        
        if payment_method == "💳 Kreditkarte":
            st.text_input("Kartennummer", placeholder="1234 5678 9012 3456")
            col_a, col_b = st.columns(2)
            with col_a:
                st.text_input("Ablaufdatum", placeholder="MM/YY")
            with col_b:
                st.text_input("CVV", placeholder="123")
        
        elif payment_method == "🏦 SEPA-Lastschrift":
            st.text_input("IBAN", placeholder="DE89 3704 0044 0532 0130 00")
            st.text_input("Kontoinhaber")
        
        st.text_input("Email", placeholder="ihre.email@beispiel.de")
        
        st.checkbox("Ich akzeptiere die AGB und Datenschutzrichtlinien", value=False)
        
        if st.button("✅ Abonnement abschließen - €{}/Monat".format(details["price"]), type="primary", use_container_width=True):
            # In production: Create Stripe subscription
            st.success("🎉 Zahlung erfolgreich! Ihr Abonnement wurde aktiviert.")
            st.session_state.subscription = {
                "tier": tier,
                "status": SubscriptionStatus.ACTIVE,
                "queries_used": 0,
                "queries_limit": details["queries_per_month"],
                "next_billing_date": datetime.now() + timedelta(days=30),
            }
            st.balloons()
            st.session_state.show_checkout = False
            st.rerun()
    
    with col2:
        st.markdown("### 📋 Bestellübersicht")
        st.markdown(f"**Plan:** {tier.value.upper()}")
        st.markdown(f"**Preis:** €{details['price']}/Monat")
        st.markdown(f"**Fragen/Monat:** {details['queries_per_month']}")
        
        st.markdown("---")
        st.markdown("### ✅ Inklusive:")
        for feature in details["features"][:5]:
            st.markdown(feature)
        
        st.markdown("---")
        st.markdown(f"### 💰 Gesamt: €{details['price']}/Monat")
        st.caption("Wird monatlich abgerechnet. Jederzeit kündbar.")
