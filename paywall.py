"""
Paywall & Pricing UI Components
Visual quota counters, upgrade modals, and pricing tables.
"""

import streamlit as st
import requests
import os
from typing import Optional


# Backend API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
# Stripe publishable key (for frontend)
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "pk_live_...")


# Mock user state (in production: fetch from backend/database)
def init_user_state():
    """Initialize user session state."""
    if "user_tier" not in st.session_state:
        st.session_state.user_tier = "FREE"  # FREE, TENANT, PRO, LAWYER
    if "queries_used" not in st.session_state:
        st.session_state.queries_used = 0
    if "user_email" not in st.session_state:
        st.session_state.user_email = "user@example.com"  # Replace with actual auth


def get_quota_info(tier: str) -> dict:
    """Get quota limits for a tier."""
    quotas = {
        "FREE": {"limit": 3, "name": "Free", "price": 0},
        "TENANT": {"limit": 100, "name": "Mieter Plus", "price": 9},
        "PRO": {"limit": 500, "name": "Professional", "price": 29},
        "LAWYER": {"limit": 1000, "name": "Lawyer Pro", "price": 49},
    }
    return quotas.get(tier, quotas["FREE"])


def render_quota_counter():
    """Render usage counter in sidebar."""
    init_user_state()
    
    tier = st.session_state.user_tier
    used = st.session_state.queries_used
    quota_info = get_quota_info(tier)
    limit = quota_info["limit"]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Nutzung")
    
    # Tier badge
    tier_colors = {
        "FREE": "🆓",
        "TENANT": "🏠",
        "PRO": "⭐",
        "LAWYER": "⚖️",
    }
    icon = tier_colors.get(tier, "🆓")
    st.sidebar.markdown(f"**{icon} {quota_info['name']}**")
    
    # Progress bar
    percentage = min((used / limit) * 100, 100)
    st.sidebar.progress(percentage / 100)
    st.sidebar.caption(f"**{used} / {limit}** Fragen diesen Monat")
    
    # Warning if close to limit
    if used >= limit:
        st.sidebar.error("⚠️ **Limit erreicht!**")
        if st.sidebar.button("🚀 Jetzt upgraden", use_container_width=True, type="primary"):
            st.session_state.show_paywall = True
            st.rerun()
    elif used >= limit * 0.8:
        st.sidebar.warning(f"⚠️ Noch {limit - used} Fragen übrig")
    
    # Upgrade button for lower tiers
    if tier != "LAWYER":
        if st.sidebar.button("⬆️ Upgrade", use_container_width=True):
            st.session_state.show_paywall = True
            st.rerun()


def show_paywall_modal(reason: str = "quota", feature: Optional[str] = None):
    """
    Show paywall modal when user hits limit or locked feature.
    
    Args:
        reason: 'quota' or 'feature'
        feature: Name of locked feature (for feature gates)
    """
    st.markdown("---")
    
    if reason == "quota":
        st.error("### 🚫 Limit erreicht!")
        st.markdown("""
        Sie haben Ihr monatliches Frage-Limit erreicht.
        
        **Upgraden Sie jetzt** für unbegrenzten Zugriff auf alle Features!
        """)
    else:
        st.warning(f"### 🔒 Premium Feature: {feature}")
        st.markdown(f"""
        **{feature}** ist nur für zahlende Nutzer verfügbar.
        
        Schalten Sie diese und viele weitere Features mit einem Upgrade frei!
        """)
    
    # Show pricing table
    render_pricing_table_inline()
    
    st.markdown("---")
    if st.button("← Zurück ohne Upgrade", use_container_width=True):
        st.session_state.show_paywall = False
        st.rerun()


def render_pricing_table_inline():
    """Render compact pricing comparison table."""
    st.markdown("### 💎 Wählen Sie Ihren Plan")
    
    cols = st.columns(4)
    
    tiers = [
        {
            "name": "Free",
            "price": 0,
            "queries": 3,
            "features": ["3 Fragen/Monat", "Basis-Features", "Nur DE"],
            "tier_id": "FREE",
            "button": "Aktuell",
            "disabled": True,
        },
        {
            "name": "Mieter Plus",
            "price": 9,
            "queries": 100,
            "features": ["100 Fragen/Monat", "Alle Länder", "Streitschlichtung"],
            "tier_id": "TENANT",
            "button": "Wählen - 9€",
            "disabled": False,
        },
        {
            "name": "Professional",
            "price": 29,
            "queries": 500,
            "features": ["500 Fragen/Monat", "PDF-Upload", "Alle Rollen", "Priority Support"],
            "tier_id": "PRO",
            "button": "Wählen - 29€",
            "disabled": False,
            "recommended": True,
        },
        {
            "name": "Lawyer Pro",
            "price": 49,
            "queries": 1000,
            "features": ["1.000 Fragen/Monat", "API-Zugriff", "Bulk-Analyse", "24/7 Support"],
            "tier_id": "LAWYER",
            "button": "Wählen - 49€",
            "disabled": False,
        },
    ]
    
    for idx, tier in enumerate(tiers):
        with cols[idx]:
            if tier.get("recommended"):
                st.markdown("#### ⭐ EMPFOHLEN")
            st.markdown(f"### {tier['name']}")
            
            if tier["price"] == 0:
                st.markdown("## Kostenlos")
            else:
                st.markdown(f"## €{tier['price']}/Monat")
            
            st.markdown(f"**{tier['queries']} Fragen**")
            st.markdown("---")
            
            for feature in tier["features"]:
                st.markdown(f"✅ {feature}")
            
            st.markdown("---")
            
            button_type = "primary" if tier.get("recommended") else "secondary"
            if st.button(
                tier["button"],
                key=f"select_{tier['tier_id']}",
                disabled=tier["disabled"],
                use_container_width=True,
                type=button_type,
            ):
                # Mock upgrade (replace with Stripe later)
                mock_upgrade(tier["tier_id"])


def mock_upgrade(tier: str):
    """
    Create Stripe Checkout Session and redirect to payment.
    Replaces the old mock upgrade flow.
    """
    init_user_state()
    
    user_email = st.session_state.get("user_email", "user@example.com")
    
    # Get current URL for success/cancel redirects
    # In production, these would be your deployed URLs
    base_url = "https://domulex-frontend-841507936108.europe-west3.run.app"
    success_url = f"{base_url}?upgrade_success=true&tier={tier}"
    cancel_url = f"{base_url}?upgrade_cancelled=true"
    
    try:
        # Call backend to create Stripe Checkout Session
        response = requests.post(
            f"{API_BASE_URL}/stripe/create-checkout-session",
            data={
                "user_email": user_email,
                "tier": tier,
                "success_url": success_url,
                "cancel_url": cancel_url,
                "user_id": st.session_state.get("user_id", user_email),
            },
            timeout=10,
        )
        
        if response.status_code == 200:
            data = response.json()
            checkout_url = data.get("checkout_url")
            
            # Display success message and redirect button
            st.info(f"🔄 Weiterleitung zu Stripe Checkout für **{get_quota_info(tier)['name']}**...")
            
            st.markdown(f"""
            ### ✅ Checkout Session erstellt!
            
            Klicken Sie auf den Button unten, um zur sicheren Zahlungsseite von Stripe zu gelangen.
            
            **Was passiert als nächstes:**
            1. Sie werden zu Stripe weitergeleitet (sichere Zahlung)
            2. Geben Sie Ihre Zahlungsinformationen ein
            3. Nach erfolgreicher Zahlung werden Sie zurückgeleitet
            4. Ihr Account wird automatisch auf **{get_quota_info(tier)['name']}** upgraded
            """)
            
            # Create a link button to Stripe Checkout
            st.markdown(f"""
            <a href="{checkout_url}" target="_self">
                <button style="
                    background-color: #635BFF;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    width: 100%;
                    margin-top: 10px;
                ">
                    🔒 Zur Zahlung (Stripe Checkout)
                </button>
            </a>
            """, unsafe_allow_html=True)
            
            st.caption("🔐 Sichere Zahlung über Stripe • SSL-verschlüsselt • DSGVO-konform")
            
        else:
            st.error(f"❌ Fehler beim Erstellen der Checkout Session: {response.text}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Verbindungsfehler zum Backend: {e}")
        st.warning("Fallback: Mock-Upgrade aktiviert (nur für Entwicklung)")
        
        # Fallback to old mock behavior if backend is not available
        st.session_state.user_tier = tier
        st.session_state.queries_used = 0
        st.session_state.show_paywall = False
        st.success(f"🎉 Mock-Upgrade auf **{get_quota_info(tier)['name']}** (Entwicklungsmodus)")


def check_and_enforce_quota() -> bool:
    """
    Check quota before processing a query.
    Returns True if allowed, False if limit reached.
    Shows paywall modal if needed.
    """
    init_user_state()
    
    tier = st.session_state.user_tier
    used = st.session_state.queries_used
    limit = get_quota_info(tier)["limit"]
    
    if used >= limit:
        st.session_state.show_paywall = True
        show_paywall_modal(reason="quota")
        return False
    
    return True


def increment_query_count():
    """Increment query counter after successful query."""
    if "queries_used" in st.session_state:
        st.session_state.queries_used += 1


def check_feature_access(feature: str) -> bool:
    """
    Check if user can access a feature based on tier.
    Returns True if allowed, False if locked (shows paywall).
    """
    init_user_state()
    tier = st.session_state.user_tier
    
    feature_gates = {
        "PDF_UPLOAD": ["PRO", "LAWYER"],
        "INTERNATIONAL_SEARCH": ["TENANT", "PRO", "LAWYER"],
        "API_ACCESS": ["LAWYER"],
        "CONTRACT_COMPARISON": ["PRO", "LAWYER"],
    }
    
    allowed_tiers = feature_gates.get(feature, [])
    
    if tier not in allowed_tiers:
        st.session_state.show_paywall = True
        show_paywall_modal(reason="feature", feature=feature)
        return False
    
    return True
