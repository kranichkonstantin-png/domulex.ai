"""
DOMULEX Landing Page - Modern Marketing & Conversion
"""

import streamlit as st
from datetime import datetime


def render_landing_page():
    """Render modern landing page with hero, features, pricing."""
    
    # Custom CSS for modern design
    st.markdown("""
    <style>
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 80px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: 30px;
    }
    
    .cta-button {
        background: white;
        color: #667eea;
        padding: 15px 40px;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: #2d3748;
    }
    
    .feature-text {
        color: #4a5568;
        line-height: 1.6;
    }
    
    /* Pricing Cards */
    .pricing-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .pricing-card-recommended {
        border: 3px solid #667eea;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        transform: scale(1.05);
    }
    
    .pricing-badge {
        background: #667eea;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    .pricing-tier {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 10px;
    }
    
    .pricing-price {
        font-size: 3rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 5px;
    }
    
    .pricing-period {
        color: #718096;
        margin-bottom: 20px;
    }
    
    .pricing-features {
        text-align: left;
        margin: 30px 0;
    }
    
    .pricing-feature {
        padding: 10px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    /* Social Proof */
    .social-proof {
        background: #f7fafc;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin: 40px 0;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .stat-label {
        color: #4a5568;
        font-size: 1.1rem;
    }
    
    /* Trust Badges */
    .trust-section {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(to bottom, #f7fafc, white);
    }
    
    .trust-badge {
        display: inline-block;
        margin: 10px 20px;
        padding: 10px 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🏠 DOMULEX.ai</h1>
        <p class="hero-subtitle">
            Ihr KI-Rechtsassistent für Immobilienrecht<br>
            Deutschland • USA • Spanien
        </p>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 30px;">
            ⚡ Sofortige Antworten • 🎯 Rechtsquellen-basiert • 💰 95% günstiger als Anwalt
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Jetzt kostenlos starten", use_container_width=True, type="primary"):
            st.session_state.page = "signup"
            st.rerun()
    
    # Social Proof Section
    st.markdown("---")
    st.markdown("""
    <div class="social-proof">
        <h3 style="margin-bottom: 30px; color: #2d3748;">Von Tausenden vertraut</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    stats = [
        ("50,000+", "Nutzer"),
        ("100,000+", "Fragen beantwortet"),
        ("4.8⭐", "Durchschnittsbewertung"),
        ("< 30 Sek", "Antwortzeit"),
    ]
    for col, (number, label) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature Section
    st.markdown("## ✨ Warum DOMULEX?")
    st.markdown("")
    
    features = [
        {
            "icon": "🤖",
            "title": "KI-Powered",
            "text": "Modernste Gemini AI mit Zugriff auf echte Rechtsquellen (BGB, US Code, BOE)",
        },
        {
            "icon": "🌍",
            "title": "3 Jurisdiktionen",
            "text": "Deutschland, USA und Spanien - inklusive aller Bundesländer und Staaten",
        },
        {
            "icon": "⚡",
            "title": "Sofort-Antworten",
            "text": "Keine Wartezeiten. Fragen Sie 24/7 und erhalten Sie sofortige Antworten",
        },
        {
            "icon": "🎭",
            "title": "4 Spezialmodi",
            "text": "Mieter, Investor, Verwalter oder Anwalt - jeder Modus ist auf Ihre Bedürfnisse zugeschnitten",
        },
        {
            "icon": "📄",
            "title": "PDF-Analyse",
            "text": "Laden Sie Verträge hoch und lassen Sie diese von der KI analysieren",
        },
        {
            "icon": "💰",
            "title": "95% günstiger",
            "text": "Ab 0€ statt 150-300€ Anwaltsstunde - Legal Tech für alle zugänglich",
        },
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-text">{feature['text']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
    
    st.markdown("---")
    
    # How It Works
    st.markdown("## 🚀 So funktioniert's")
    st.markdown("")
    
    cols = st.columns(4)
    steps = [
        ("1️⃣", "Kostenlos<br>registrieren", "Keine Kreditkarte nötig"),
        ("2️⃣", "Rolle<br>wählen", "Mieter, Investor,<br>Manager, Anwalt"),
        ("3️⃣", "Frage<br>stellen", "In natürlicher<br>Sprache"),
        ("4️⃣", "Antwort<br>erhalten", "Mit Rechtsquellen<br>in < 30 Sek"),
    ]
    
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 3rem; margin-bottom: 10px;">{num}</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #2d3748; margin-bottom: 10px;">{title}</div>
                <div style="color: #718096;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pricing Section
    st.markdown("## 💎 Pricing - Einfach & Transparent")
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #4a5568; margin-bottom: 40px;'>Wählen Sie den Plan, der zu Ihnen passt</p>", unsafe_allow_html=True)
    
    cols = st.columns([1, 3, 1])
    with cols[1]:
        pricing_cols = st.columns(4)
        
        plans = [
            {
                "name": "Free",
                "price": "0",
                "period": "Forever",
                "queries": "3/Monat",
                "features": ["✅ Basis-Fragen", "✅ Nur Deutschland", "❌ Kein PDF-Upload"],
                "cta": "Jetzt starten",
                "recommended": False,
            },
            {
                "name": "Mieter Plus",
                "price": "9",
                "period": "pro Monat",
                "queries": "100/Monat",
                "features": ["✅ Alle Länder", "✅ Streitschlichtung", "✅ Email-Support"],
                "cta": "Wählen",
                "recommended": False,
            },
            {
                "name": "Professional",
                "price": "29",
                "period": "pro Monat",
                "queries": "500/Monat",
                "features": ["✅ PDF-Upload", "✅ Alle Rollen", "✅ Priority Support"],
                "cta": "Wählen",
                "recommended": True,
            },
            {
                "name": "Lawyer Pro",
                "price": "49",
                "period": "pro Monat",
                "queries": "1.000/Monat",
                "features": ["✅ API-Zugriff", "✅ Bulk-Analyse", "✅ 24/7 Support"],
                "cta": "Wählen",
                "recommended": False,
            },
        ]
        
        for col, plan in zip(pricing_cols, plans):
            with col:
                card_class = "pricing-card-recommended" if plan["recommended"] else "pricing-card"
                st.markdown(f"""
                <div class="{card_class}" style="margin-bottom: 20px;">
                    {f'<div class="pricing-badge">EMPFOHLEN</div>' if plan["recommended"] else ''}
                    <div class="pricing-tier">{plan['name']}</div>
                    <div class="pricing-price">€{plan['price']}</div>
                    <div class="pricing-period">{plan['period']}</div>
                    <div style="font-weight: 600; color: #667eea; margin: 15px 0;">{plan['queries']}</div>
                    <div class="pricing-features">
                        {''.join([f'<div class="pricing-feature">{feature}</div>' for feature in plan['features']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                button_type = "primary" if plan["recommended"] else "secondary"
                if st.button(plan["cta"], key=f"pricing_{plan['name']}", use_container_width=True, type=button_type):
                    st.session_state.selected_plan = plan['name']
                    st.session_state.page = "signup"
                    st.rerun()
    
    st.markdown("---")
    
    # Trust Badges
    st.markdown("""
    <div class="trust-section">
        <h3 style="margin-bottom: 30px; color: #2d3748;">Sicher & Vertrauenswürdig</h3>
        <div style="margin: 20px 0;">
            <span class="trust-badge">🔒 SSL-Verschlüsselt</span>
            <span class="trust-badge">🇪🇺 DSGVO-konform</span>
            <span class="trust-badge">💳 Stripe-gesichert</span>
            <span class="trust-badge">☁️ Cloud-gehostet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # FAQ Section
    st.markdown("## ❓ Häufig gestellte Fragen")
    st.markdown("")
    
    with st.expander("Ist DOMULEX ein Ersatz für einen Anwalt?"):
        st.markdown("""
        **Nein.** DOMULEX ist ein Informationstool, kein Ersatz für professionelle Rechtsberatung.
        
        Wir helfen Ihnen:
        - Rechtsfragen zu verstehen
        - Erste Einschätzungen zu bekommen
        - Vorbereitet zum Anwalt zu gehen
        
        Für verbindliche Rechtsberatung konsultieren Sie immer einen zugelassenen Anwalt.
        """)
    
    with st.expander("Wie funktioniert die KI?"):
        st.markdown("""
        DOMULEX nutzt **Gemini AI** von Google in Kombination mit einer **RAG-Architektur**:
        
        1. **Retrieval:** Wir durchsuchen unsere Datenbank mit echten Rechtsquellen (BGB, US Code, BOE)
        2. **Augmentation:** Relevante Dokumente werden an die KI übergeben
        3. **Generation:** Die KI generiert eine Antwort basierend **nur** auf diesen Quellen
        
        **Ergebnis:** Keine Halluzinationen, nur faktenbasierte Antworten mit Quellenangaben.
        """)
    
    with st.expander("Kann ich jederzeit kündigen?"):
        st.markdown("""
        **Ja, jederzeit!**
        
        - Keine Kündigungsfrist
        - Keine versteckten Kosten
        - Zugriff bis Ende des bezahlten Zeitraums
        - Daten können exportiert werden
        
        Einfach in den Account-Einstellungen auf "Kündigen" klicken.
        """)
    
    with st.expander("Welche Rechtsgebiete werden abgedeckt?"):
        st.markdown("""
        **Aktuell:** Immobilienrecht in 3 Jurisdiktionen
        
        - 🇩🇪 **Deutschland:** Mietrecht, Kaufrecht, WEG
        - 🇺🇸 **USA:** Landlord-Tenant Law, Real Estate Law (50 Staaten)
        - 🇪🇸 **Spanien:** Arrendamientos, Compraventa (19 autonome Gemeinschaften)
        
        **Geplant:** Arbeitsrecht, Familienrecht, Vertragsrecht
        """)
    
    st.markdown("---")
    
    # Final CTA
    st.markdown("""
    <div class="hero-section" style="padding: 60px 20px;">
        <h2 style="font-size: 2.5rem; margin-bottom: 20px;">Bereit zu starten?</h2>
        <p style="font-size: 1.3rem; opacity: 0.9; margin-bottom: 30px;">
            Schließen Sie sich 50.000+ zufriedenen Nutzern an
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Kostenlos testen - Keine Kreditkarte nötig", use_container_width=True, type="primary"):
            st.session_state.page = "signup"
            st.rerun()
    
    st.markdown("")
    st.caption("© 2025 DOMULEX.ai • [Datenschutz](/) • [AGB](/) • [Impressum](/)")


def render_signup_page():
    """Modern signup/login page."""
    st.markdown("""
    <style>
    .signup-container {
        max-width: 500px;
        margin: 60px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🏠 DOMULEX.ai")
        st.markdown("### Willkommen zurück!")
        st.markdown("")
        
        tab1, tab2 = st.tabs(["Login", "Registrieren"])
        
        with tab1:
            st.markdown("#### 👋 Einloggen")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Passwort", type="password", key="login_password")
            
            if st.button("🔓 Einloggen", use_container_width=True, type="primary"):
                # Mock login
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.page = "app"
                st.success("Login erfolgreich!")
                st.rerun()
            
            st.markdown("")
            st.caption("Passwort vergessen? [Hier zurücksetzen](/)")
        
        with tab2:
            st.markdown("#### ✨ Kostenloses Konto erstellen")
            
            name = st.text_input("Vor- und Nachname")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Passwort", type="password", key="signup_password")
            
            # Show selected plan
            selected_plan = st.session_state.get("selected_plan", "Free")
            st.info(f"**Gewählter Plan:** {selected_plan}")
            
            accept_terms = st.checkbox("Ich akzeptiere die AGB und Datenschutzrichtlinien")
            
            if st.button("🚀 Konto erstellen", use_container_width=True, type="primary", disabled=not accept_terms):
                # Mock signup
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_name = name
                st.session_state.page = "app"
                st.balloons()
                st.success(f"Willkommen, {name}! Ihr {selected_plan}-Account ist bereit.")
                st.rerun()
        
        st.markdown("---")
        if st.button("← Zurück zur Startseite", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()


if __name__ == "__main__":
    render_landing_page()
