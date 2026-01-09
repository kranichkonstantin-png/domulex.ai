"""
DOMULEX User Dashboard - Tier-specific features and analytics
"""

import streamlit as st
from datetime import datetime, timedelta
import random


def render_user_dashboard():
    """Render tier-specific user dashboard."""
    
    # Get user info
    tier = st.session_state.get("user_tier", "FREE")
    email = st.session_state.get("user_email", "demo@domulex.ai")
    name = st.session_state.get("user_name", "Demo User")
    queries_used = st.session_state.get("queries_used", 0)
    
    # Tier info
    tier_info = {
        "FREE": {"limit": 3, "name": "Free", "color": "#gray"},
        "TENANT": {"limit": 100, "name": "Mieter Plus", "color": "#3b82f6"},
        "PRO": {"limit": 500, "name": "Professional", "color": "#10b981"},
        "LAWYER": {"limit": 1000, "name": "Lawyer Pro", "color": "#8b5cf6"},
    }
    
    info = tier_info.get(tier, tier_info["FREE"])
    
    # Dashboard CSS
    st.markdown("""
    <style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    
    .stat-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2d3748;
    }
    
    .stat-label {
        color: #718096;
        font-size: 1rem;
        margin-top: 5px;
    }
    
    .quick-action {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        cursor: pointer;
        transition: all 0.3s;
        text-align: center;
    }
    
    .quick-action:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .activity-item {
        padding: 15px;
        border-left: 3px solid #e2e8f0;
        margin-bottom: 10px;
        background: #f7fafc;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>👋 Willkommen zurück, {name}!</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Ihr {info['name']} Account</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Overview
    st.markdown("### 📊 Übersicht")
    
    cols = st.columns(4)
    
    # Calculate some stats
    remaining = max(0, info['limit'] - queries_used)
    usage_percent = (queries_used / info['limit']) * 100 if info['limit'] > 0 else 0
    days_left = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - datetime.now()
    
    stats = [
        (f"{queries_used}", "Genutzte Fragen", "📝"),
        (f"{remaining}", "Verbleibend", "✨"),
        (f"{usage_percent:.0f}%", "Nutzung", "📈"),
        (f"{days_left.days}", "Tage bis Reset", "🔄"),
    ]
    
    for col, (number, label, icon) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Schnellzugriff")
    
    quick_cols = st.columns(4)
    
    actions = [
        ("💬", "Neue Frage", "app"),
        ("📄", "PDF Analyse", "pdf" if tier in ["PRO", "LAWYER"] else "locked"),
        ("📊", "Statistiken", "stats"),
        ("⚙️", "Einstellungen", "settings"),
    ]
    
    for col, (icon, label, action) in zip(quick_cols, actions):
        with col:
            st.markdown(f"""
            <div class="quick-action">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
                <div style="font-weight: 600;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if action == "locked":
                st.caption("🔒 Pro Feature")
            elif st.button("Öffnen", key=f"qa_{action}", use_container_width=True):
                if action == "app":
                    st.session_state.page = "app"
                    st.rerun()
                elif action == "locked":
                    st.session_state.show_paywall = True
                    st.rerun()
    
    st.markdown("---")
    
    # Tier-specific content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Letzte Aktivitäten")
        
        # Mock activity feed
        activities = [
            ("Heute, 14:23", "🇩🇪", "Frage zu Mietminderung gestellt"),
            ("Gestern, 16:45", "🇺🇸", "PDF hochgeladen: lease_agreement.pdf" if tier in ["PRO", "LAWYER"] else "Frage zu Security Deposit"),
            ("23. Dez, 10:12", "🇪🇸", "Frage zu Desahucio"),
            ("21. Dez, 09:30", "🇩🇪", "Frage zu Eigenbedarfskündigung"),
        ]
        
        for time, flag, text in activities[:4]:
            st.markdown(f"""
            <div class="activity-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2rem; margin-right: 10px;">{flag}</span>
                        <span style="font-weight: 500;">{text}</span>
                    </div>
                    <div style="color: #718096; font-size: 0.85rem;">{time}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📜 Alle Aktivitäten anzeigen", use_container_width=True):
            st.session_state.show_history = True
    
    with col2:
        st.markdown("### 💎 Ihr Plan")
        
        st.markdown(f"""
        <div style="background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">
                    {'🆓' if tier == 'FREE' else '🏠' if tier == 'TENANT' else '⭐' if tier == 'PRO' else '⚖️'}
                </div>
                <h3 style="color: #2d3748; margin-bottom: 5px;">{info['name']}</h3>
                <p style="color: #718096; margin-bottom: 20px;">{info['limit']} Fragen/Monat</p>
                
                <div style="background: #f7fafc; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <div style="font-weight: 600; margin-bottom: 10px;">Nutzung</div>
                    <div style="height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden;">
                        <div style="height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); width: {usage_percent}%;"></div>
                    </div>
                    <div style="margin-top: 8px; font-size: 0.9rem; color: #718096;">
                        {queries_used} / {info['limit']} Fragen
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        if tier != "LAWYER":
            if st.button("⬆️ Upgrade", use_container_width=True, type="primary"):
                st.session_state.show_paywall = True
                st.rerun()
        
        if tier != "FREE":
            if st.button("⚙️ Abo verwalten", use_container_width=True):
                st.session_state.page = "subscription_settings"
                st.rerun()
    
    st.markdown("---")
    
    # Tier-specific features showcase
    if tier in ["PRO", "LAWYER"]:
        st.markdown("### 🎯 Premium Features")
        
        feat_cols = st.columns(3)
        
        premium_features = [
            ("📄", "PDF-Analyse", "Laden Sie Verträge hoch und lassen Sie diese analysieren"),
            ("🔄", "Vertragsvergleich", "Vergleichen Sie zwei Verträge automatisch"),
            ("🎭", "Alle Rollen", "Wechseln Sie frei zwischen allen 4 Modi"),
        ]
        
        if tier == "LAWYER":
            premium_features.append(("🔌", "API-Zugriff", "Integrieren Sie DOMULEX in Ihre Software"))
        
        for col, (icon, title, desc) in zip(feat_cols, premium_features):
            with col:
                st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); height: 100%;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                    <div style="font-weight: 600; margin-bottom: 8px; color: #2d3748;">{title}</div>
                    <div style="color: #718096; font-size: 0.9rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Recommendations based on tier
    if tier == "FREE":
        st.markdown("---")
        st.info("""
        **💡 Tipp:** Mit Mieter Plus (9€/Monat) erhalten Sie:
        - 100 statt 3 Fragen pro Monat
        - Zugriff auf USA & Spanien
        - Streitschlichtungs-Tool
        """)
        if st.button("Jetzt upgraden", key="upgrade_cta"):
            st.session_state.show_paywall = True
            st.rerun()


def render_subscription_settings():
    """Subscription management page."""
    tier = st.session_state.get("user_tier", "FREE")
    
    st.markdown("## ⚙️ Abo-Verwaltung")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Aktueller Plan")
        
        tier_names = {
            "FREE": "Free",
            "TENANT": "Mieter Plus - 9€/Monat",
            "PRO": "Professional - 29€/Monat",
            "LAWYER": "Lawyer Pro - 49€/Monat",
        }
        
        st.success(f"✅ Aktiv: **{tier_names.get(tier, 'Free')}**")
        
        if tier != "FREE":
            st.markdown(f"""
            **Nächste Abrechnung:** {(datetime.now() + timedelta(days=15)).strftime('%d. %B %Y')}
            
            **Zahlungsmethode:** •••• •••• •••• 4242 (Visa)
            """)
            
            st.markdown("---")
            
            if st.button("💳 Zahlungsmethode ändern"):
                st.info("Stripe Checkout wird geöffnet...")
            
            if st.button("⬇️ Downgrade"):
                st.warning("Möchten Sie wirklich downgraden?")
            
            if st.button("❌ Abo kündigen"):
                if st.checkbox("Ja, ich möchte wirklich kündigen"):
                    st.error("Abo zum Ende der Laufzeit gekündigt.")
        else:
            st.info("Sie nutzen den kostenlosen Plan.")
            if st.button("⬆️ Jetzt upgraden"):
                st.session_state.show_paywall = True
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Rechnungen")
        
        if tier != "FREE":
            invoices = [
                ("Dez 2025", "29,00 €"),
                ("Nov 2025", "29,00 €"),
                ("Okt 2025", "29,00 €"),
            ]
            
            for month, amount in invoices:
                cols = st.columns([2, 1])
                cols[0].markdown(f"**{month}**")
                cols[1].markdown(amount)
                if st.button("📥 PDF", key=f"invoice_{month}"):
                    st.info(f"Rechnung_{month}.pdf wird heruntergeladen...")
        else:
            st.info("Keine Rechnungen vorhanden")
    
    st.markdown("---")
    
    if st.button("← Zurück zum Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


if __name__ == "__main__":
    render_user_dashboard()
