"""
Professional Email Templates for Domulex.ai
With company branding, logo, and automatic signature
"""

# Company Information
COMPANY_NAME = "Home Invest & Management GmbH"
COMPANY_STREET = "Zur Maate 19"
COMPANY_CITY = "31515 Wunstorf"
COMPANY_COUNTRY = "Deutschland"
COMPANY_EMAIL = "kontakt@domulex.ai"
COMPANY_WEBSITE = "https://domulex.ai"
COMPANY_PHONE = "+49 (0) 5031 123456"

# Logo URL (Firebase Storage)
LOGO_URL = "https://firebasestorage.googleapis.com/v0/b/domulex-ai.firebasestorage.app/o/logo_domulex.ai.jpeg?alt=media&token=09549d86-118a-4dd6-a187-85e951b57fbf"

# Brand Colors
PRIMARY_COLOR = "#1e3a5f"  # Dark blue
SECONDARY_COLOR = "#2563eb"  # Bright blue
ACCENT_COLOR = "#10b981"  # Green
WARNING_COLOR = "#f59e0b"  # Orange
ERROR_COLOR = "#ef4444"  # Red


def get_base_template(content: str, title: str = "") -> str:
    """Base HTML email template with header, footer, and signature"""
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            margin: 0;
            padding: 0;
            background-color: #f4f4f5;
        }}
        .wrapper {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .email-container {{
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, #2d4a6f 100%);
            padding: 30px;
            text-align: center;
        }}
        .header img {{
            height: 50px;
            margin-bottom: 10px;
        }}
        .header h1 {{
            color: #ffffff;
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .content {{
            padding: 30px;
        }}
        .content h2 {{
            color: {PRIMARY_COLOR};
            margin-top: 0;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, #4f46e5 100%);
            color: #ffffff !important;
            padding: 14px 32px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 20px 0;
        }}
        .button:hover {{
            opacity: 0.9;
        }}
        .info-box {{
            background-color: #f0f9ff;
            border-left: 4px solid {SECONDARY_COLOR};
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        .warning-box {{
            background-color: #fffbeb;
            border-left: 4px solid {WARNING_COLOR};
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        .success-box {{
            background-color: #f0fdf4;
            border-left: 4px solid {ACCENT_COLOR};
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        .signature {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
        .signature p {{
            margin: 5px 0;
            color: #6b7280;
        }}
        .signature .team {{
            font-weight: 600;
            color: {PRIMARY_COLOR};
            font-size: 16px;
        }}
        .footer {{
            background-color: #f9fafb;
            padding: 25px 30px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }}
        .footer img {{
            height: 35px;
            margin-bottom: 15px;
            opacity: 0.8;
        }}
        .footer p {{
            margin: 5px 0;
            font-size: 12px;
            color: #6b7280;
        }}
        .footer a {{
            color: {SECONDARY_COLOR};
            text-decoration: none;
        }}
        .social-links {{
            margin: 15px 0;
        }}
        .social-links a {{
            display: inline-block;
            margin: 0 8px;
            color: #6b7280;
            text-decoration: none;
        }}
        .legal {{
            font-size: 11px;
            color: #9ca3af;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="email-container">
            <div class="header" style="background-color: #1e3a5f; padding: 30px; text-align: center;">
                <h1 style="font-size: 28px; margin: 0; color: #ffffff;"><span style="color: #ffffff;">domulex</span><span style="color: #b8860b;">.ai</span></h1>
                <p style="color: #ffffff; opacity: 0.9; margin: 8px 0 0 0; font-size: 14px;">KI-Rechtsassistenz für Immobilien</p>
            </div>
            
            <div class="content">
                {content}
                
                <div class="signature">
                    <p class="team">Ihr domulex.ai Team</p>
                    <p>KI-Rechtsassistenz für Immobilien</p>
                    <p style="font-size: 13px;">
                        📧 <a href="mailto:{COMPANY_EMAIL}">{COMPANY_EMAIL}</a> | 
                        🌐 <a href="{COMPANY_WEBSITE}">domulex.ai</a>
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p style="font-size: 18px; font-weight: 600; color: {PRIMARY_COLOR}; margin-bottom: 10px;">domulex<span style="color: #b8860b;">.ai</span></p>
                <p><strong>{COMPANY_NAME}</strong></p>
                <p>{COMPANY_STREET} • {COMPANY_CITY}</p>
                <p>
                    <a href="{COMPANY_WEBSITE}/datenschutz">Datenschutz</a> • 
                    <a href="{COMPANY_WEBSITE}/agb">AGB</a> • 
                    <a href="{COMPANY_WEBSITE}/impressum">Impressum</a>
                </p>
                <p class="legal">
                    Diese E-Mail wurde automatisch generiert. 
                    Bei Fragen antworten Sie einfach auf diese E-Mail.
                </p>
            </div>
        </div>
    </div>
</body>
</html>'''


def get_welcome_email(user_name: str) -> dict:
    """Welcome email for new users"""
    content = f'''
        <h2>Willkommen bei domulex.ai! 👋</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <p>vielen Dank für Ihre Registrierung bei domulex.ai – Ihrer KI-Rechtsassistenz für Immobilien.</p>
        
        <div class="success-box">
            <strong>✅ Ihr Test-Tarif ist aktiviert</strong>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>3 kostenlose Test-Anfragen</li>
                <li>Zugang zu deutschem Immobilienrecht</li>
                <li>Über 50.000 aktuelle Rechtsdokumente</li>
                <li>DSGVO-konform & Zero Data Retention</li>
            </ul>
        </div>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/app" class="button">🚀 Jetzt loslegen</a>
        </p>
        
        <p><strong>So nutzen Sie domulex.ai optimal:</strong></p>
        <ol>
            <li>Stellen Sie Ihre erste Rechtsfrage zur Immobilie</li>
            <li>Erhalten Sie eine fundierte Antwort mit Quellenangaben</li>
            <li>Upgraden Sie für unbegrenzte Nutzung</li>
        </ol>
        
        <div class="warning-box">
            <strong>📌 Hinweis:</strong> Test-Konten werden nach 6 Monaten Inaktivität automatisch gelöscht. 
            <a href="{COMPANY_WEBSITE}/preise">Jetzt upgraden</a> für dauerhaften Zugang.
        </div>
    '''
    
    return {
        "subject": "Willkommen bei domulex.ai! ✅",
        "html": get_base_template(content, "Willkommen bei domulex.ai"),
        "text": f"""Willkommen bei domulex.ai!

Hallo {user_name},

vielen Dank für Ihre Registrierung bei domulex.ai – Ihrer KI-Rechtsassistenz für Immobilien.

Ihr Test-Tarif ist aktiviert:
• 3 kostenlose Test-Anfragen
• Zugang zu deutschem Immobilienrecht
• Über 50.000 aktuelle Rechtsdokumente
• DSGVO-konform & Zero Data Retention

Jetzt loslegen: {COMPANY_WEBSITE}/app

Ihr domulex.ai Team
{COMPANY_NAME}
{COMPANY_STREET}, {COMPANY_CITY}
"""
    }


def get_order_confirmation_email(user_name: str, plan_name: str, plan_price: float, subscription_id: str, invoice_url: str = None) -> dict:
    """Order confirmation email"""
    invoice_section = f'<p><a href="{invoice_url}">📄 Rechnung als PDF herunterladen</a></p>' if invoice_url else ''
    
    content = f'''
        <h2>Bestellung erfolgreich! ✅</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <p>vielen Dank für Ihre Bestellung. Ihr Upgrade wurde sofort aktiviert.</p>
        
        <div class="success-box" style="text-align: center;">
            <p style="margin: 0; font-size: 14px; color: #059669;">IHR TARIF</p>
            <p style="margin: 10px 0 5px 0; font-size: 28px; font-weight: bold; color: {PRIMARY_COLOR};">{plan_name}</p>
            <p style="margin: 0; font-size: 24px; color: {ACCENT_COLOR}; font-weight: bold;">{plan_price:.2f} €/Monat</p>
            <p style="margin: 10px 0 0 0; font-size: 12px; color: #6b7280;">Abo-ID: {subscription_id[:20]}...</p>
        </div>
        
        {invoice_section}
        
        <p><strong>Was Sie jetzt nutzen können:</strong></p>
        <ul>
            <li>Unbegrenzte Rechtsfragen</li>
            <li>Alle Premium-Features</li>
            <li>Prioritäts-Support</li>
            <li>Automatische monatliche Abrechnung</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/app" class="button">Zur App →</a>
        </p>
        
        <div class="info-box">
            <strong>ℹ️ Widerrufsrecht (Verbraucher)</strong><br>
            Sie haben das Recht, binnen 14 Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen.
            <a href="{COMPANY_WEBSITE}/agb#widerruf">Mehr erfahren</a>
        </div>
    '''
    
    return {
        "subject": f"Bestellbestätigung – {plan_name}",
        "html": get_base_template(content, "Bestellbestätigung"),
        "text": f"""Bestellung erfolgreich!

Hallo {user_name},

vielen Dank für Ihre Bestellung. Ihr Upgrade wurde sofort aktiviert.

Ihr Tarif: {plan_name}
Preis: {plan_price:.2f} €/Monat
Abo-ID: {subscription_id}

Zur App: {COMPANY_WEBSITE}/app

Ihr domulex.ai Team
{COMPANY_NAME}
"""
    }


def get_payment_failed_email(user_name: str) -> dict:
    """Payment failed notification"""
    content = f'''
        <h2>Zahlungsproblem ⚠️</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <p>leider konnten wir Ihre letzte Zahlung nicht verarbeiten.</p>
        
        <div class="warning-box">
            <strong>Was bedeutet das?</strong><br>
            Ihr Abonnement bleibt zunächst aktiv. Wir werden die Zahlung in den nächsten Tagen 
            erneut versuchen. Bitte stellen Sie sicher, dass Ihre Zahlungsmethode aktuell ist.
        </div>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/konto" class="button">💳 Zahlungsmethode aktualisieren</a>
        </p>
        
        <p>Falls Sie Fragen haben, kontaktieren Sie uns jederzeit unter 
        <a href="mailto:{COMPANY_EMAIL}">{COMPANY_EMAIL}</a>.</p>
    '''
    
    return {
        "subject": "⚠️ Zahlungsproblem bei Ihrem domulex.ai Abonnement",
        "html": get_base_template(content, "Zahlungsproblem"),
        "text": f"""Zahlungsproblem

Hallo {user_name},

leider konnten wir Ihre letzte Zahlung nicht verarbeiten.

Bitte aktualisieren Sie Ihre Zahlungsmethode: {COMPANY_WEBSITE}/konto

Ihr domulex.ai Team
"""
    }


def get_subscription_cancelled_email(user_name: str, end_date: str) -> dict:
    """Subscription cancellation confirmation"""
    content = f'''
        <h2>Kündigungsbestätigung</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <p>wir bestätigen die Kündigung Ihres Abonnements.</p>
        
        <div class="info-box">
            <strong>📅 Wichtig:</strong><br>
            Ihr Zugang bleibt bis zum <strong>{end_date}</strong> vollständig aktiv.<br>
            Sie können Domulex.ai bis dahin wie gewohnt nutzen.
        </div>
        
        <p><strong>Nach Ablauf Ihres Abonnements:</strong></p>
        <ul>
            <li>Automatische Herabstufung auf Test-Tarif</li>
            <li>3 Anfragen pro Monat verfügbar</li>
            <li>Ihre Daten bleiben 6 Monate gespeichert</li>
        </ul>
        
        <p>Wir würden uns freuen, Sie bald wiederzusehen!</p>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/preise" class="button">Tarife ansehen</a>
        </p>
    '''
    
    return {
        "subject": "Kündigungsbestätigung – domulex.ai",
        "html": get_base_template(content, "Kündigungsbestätigung"),
        "text": f"""Kündigungsbestätigung

Hallo {user_name},

wir bestätigen die Kündigung Ihres Abonnements.

Ihr Zugang bleibt bis zum {end_date} aktiv.

Ihr domulex.ai Team
"""
    }


def get_admin_notification_email(user_name: str, title: str, message: str) -> dict:
    """Admin notification to user"""
    content = f'''
        <h2>👑 {title}</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <div class="info-box" style="background-color: #faf5ff; border-left-color: #9333ea;">
            <p style="white-space: pre-wrap; margin: 0;">{message}</p>
        </div>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/app/notifications" class="button">Alle Benachrichtigungen anzeigen</a>
        </p>
    '''
    
    return {
        "subject": f"Nachricht von domulex.ai: {title}",
        "html": get_base_template(content, title),
        "text": f"""{title}

Hallo {user_name},

{message}

Ihr domulex.ai Team
"""
    }


def get_tier_change_email(user_name: str, new_tier: str, queries_limit: int) -> dict:
    """Tier change notification"""
    content = f'''
        <h2>Ihr Abo wurde aktualisiert ✅</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <p>Ihr Abonnement bei domulex.ai wurde erfolgreich aktualisiert.</p>
        
        <div class="success-box" style="text-align: center;">
            <p style="margin: 0; font-size: 14px; color: #059669;">IHR NEUER TARIF</p>
            <p style="margin: 10px 0; font-size: 28px; font-weight: bold; color: {PRIMARY_COLOR};">{new_tier}</p>
            <p style="margin: 0; color: #6b7280;">{queries_limit} Anfragen pro Monat</p>
        </div>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/app" class="button">Jetzt nutzen →</a>
        </p>
    '''
    
    return {
        "subject": "Ihr Abo wurde aktualisiert – domulex.ai",
        "html": get_base_template(content, "Abo aktualisiert"),
        "text": f"""Ihr Abo wurde aktualisiert

Hallo {user_name},

Ihr neuer Tarif: {new_tier}
Anfragen pro Monat: {queries_limit}

Ihr domulex.ai Team
"""
    }


def get_deletion_reminder_email(user_name: str, deletion_date: str) -> dict:
    """Account deletion reminder (7 days before)"""
    content = f'''
        <h2>⚠️ Wichtige Mitteilung</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <div class="warning-box" style="background-color: #fef2f2; border-left-color: {ERROR_COLOR};">
            <strong>Ihr Konto wird am {deletion_date} gelöscht.</strong>
            <p style="margin: 10px 0 0 0;">
                Da Ihr Test-Tarif seit 6 Monaten inaktiv ist, wird Ihr Konto 
                gemäß unserer Datenschutzrichtlinie in 7 Tagen automatisch gelöscht.
            </p>
        </div>
        
        <p><strong>So behalten Sie Ihr Konto:</strong></p>
        <ul>
            <li>Melden Sie sich einfach bei domulex.ai an</li>
            <li>Oder upgraden Sie auf einen kostenpflichtigen Tarif</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/auth/login" class="button">Jetzt anmelden</a>
        </p>
    '''
    
    return {
        "subject": "⚠️ Ihr Konto wird in 7 Tagen gelöscht – domulex.ai",
        "html": get_base_template(content, "Kontolöschung"),
        "text": f"""Wichtige Mitteilung

Hallo {user_name},

Ihr Konto wird am {deletion_date} gelöscht.

Melden Sie sich an, um Ihr Konto zu behalten: {COMPANY_WEBSITE}/auth/login

Ihr domulex.ai Team
"""
    }


def get_order_confirmation_b2b_email(user_name: str, company_name: str, plan_name: str, plan_price: float, subscription_id: str, invoice_url: str = None) -> dict:
    """B2B order confirmation with AVV/NDA references"""
    invoice_section = f'<p><a href="{invoice_url}">📄 Rechnung als PDF herunterladen</a></p>' if invoice_url else ''
    
    content = f'''
        <h2>Bestellung erfolgreich (B2B) ✅</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        <p style="color: #6b7280; margin-top: -10px;">{company_name}</p>
        
        <p>vielen Dank für Ihre Bestellung als Geschäftskunde.</p>
        
        <div class="success-box" style="text-align: center;">
            <p style="margin: 0; font-size: 14px; color: #059669;">BUSINESS-TARIF</p>
            <p style="margin: 10px 0 5px 0; font-size: 28px; font-weight: bold; color: {PRIMARY_COLOR};">{plan_name}</p>
            <p style="margin: 0; font-size: 24px; color: {ACCENT_COLOR}; font-weight: bold;">{plan_price:.2f} €/Monat (netto)</p>
            <p style="margin: 5px 0 0 0; font-size: 12px; color: #6b7280;">zzgl. 19% MwSt.</p>
        </div>
        
        {invoice_section}
        
        <div class="info-box" style="background-color: #f0fdf4; border-left-color: #22c55e;">
            <strong>🏢 Enterprise-Lösungen für Ihr Unternehmen</strong>
            <p style="margin: 10px 0 0 0;">Benötigen Sie <strong>mehrere Arbeitsplätze</strong> für Ihre Mitarbeiter oder eine <strong>unternehmensinterne Plattform</strong> mit gemeinsamer Wissensdatenbank?</p>
            <p style="margin: 10px 0 0 0;">Wir bieten maßgeschneiderte Lösungen:</p>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li><strong>Multi-User-Lizenzen:</strong> Mehrere Zugänge für Ihr Team</li>
                <li><strong>Team-Datenbank:</strong> Gemeinsame Dokumenten- und Wissensverwaltung</li>
                <li><strong>API-Anbindungen:</strong> Integration in Ihre bestehenden Systeme</li>
                <li><strong>Schnittstellen:</strong> CRM, DMS, ERP und weitere Anbindungen</li>
                <li><strong>White-Label-Lösungen:</strong> domulex.ai im eigenen Branding</li>
            </ul>
            <p style="margin: 15px 0 0 0; font-weight: bold; color: #059669;">
                ✉️ Antworten Sie einfach auf diese E-Mail mit Ihren Anforderungen:
            </p>
            <ul style="margin: 5px 0 0 0; padding-left: 20px; font-size: 14px;">
                <li>Anzahl gewünschter Arbeitsplätze/Lizenzen</li>
                <li>Gewünschte Schnittstellen oder API-Anbindungen</li>
                <li>Weitere Anforderungen</li>
            </ul>
            <p style="margin: 10px 0 0 0; font-size: 13px; color: #6b7280;">Wir erstellen Ihnen gerne ein individuelles Angebot.</p>
        </div>
        
        <div class="warning-box">
            <strong>📋 Vertragsbestandteile (B2B)</strong>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li><a href="{COMPANY_WEBSITE}/agb">Allgemeine Geschäftsbedingungen (AGB)</a></li>
                <li><a href="{COMPANY_WEBSITE}/avv">Auftragsverarbeitungsvertrag (AVV)</a> gemäß Art. 28 DSGVO</li>
                <li><a href="{COMPANY_WEBSITE}/nda">Geheimhaltungsvereinbarung (NDA)</a></li>
            </ul>
            <p style="font-size: 12px; margin: 10px 0 0 0; color: #6b7280;">
                Diese Dokumente gelten mit Ihrer Bestellung als akzeptiert.
            </p>
        </div>
        
        <p><strong>Als Geschäftskunde:</strong></p>
        <ul>
            <li>Kein Widerrufsrecht (§ 312g Abs. 2 Nr. 1 BGB)</li>
            <li>Rechnungsstellung mit ausgewiesener MwSt.</li>
            <li>DSGVO-konforme Datenverarbeitung mit AVV</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/app" class="button">Zur App →</a>
        </p>
    '''
    
    return {
        "subject": f"Bestellbestätigung (B2B) – {plan_name}",
        "html": get_base_template(content, "Bestellbestätigung B2B"),
        "text": f"""Bestellbestätigung (B2B)

Hallo {user_name},
{company_name}

Ihr Tarif: {plan_name}
Preis: {plan_price:.2f} €/Monat (netto)

--- ENTERPRISE-LÖSUNGEN ---

Benötigen Sie mehrere Arbeitsplätze oder eine Unternehmensplattform?

Wir bieten:
- Multi-User-Lizenzen für Ihr Team
- Gemeinsame Team-Datenbank
- API-Anbindungen und Schnittstellen
- White-Label-Lösungen

Antworten Sie einfach auf diese E-Mail mit:
- Anzahl gewünschter Arbeitsplätze
- Gewünschte Schnittstellen
- Weitere Anforderungen

Ihr domulex.ai Team
"""
    }


def get_test_email() -> dict:
    """Test email to verify configuration"""
    content = f'''
        <h2>E-Mail-Test erfolgreich! ✅</h2>
        
        <p>Ihre E-Mail-Konfiguration funktioniert einwandfrei.</p>
        
        <div class="success-box">
            <strong>Konfiguration:</strong>
            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                <li>SMTP-Server: smtp.strato.de</li>
                <li>Verbindung: SSL/TLS (Port 465)</li>
                <li>Status: Aktiv ✓</li>
            </ul>
        </div>
        
        <p><strong>Automatische E-Mails werden jetzt versendet für:</strong></p>
        <ul>
            <li>👋 Willkommens-E-Mails bei Registrierung</li>
            <li>✅ Bestellbestätigungen</li>
            <li>⚠️ Zahlungserinnerungen</li>
            <li>📝 Kündigungsbestätigungen</li>
            <li>👑 Admin-Benachrichtigungen</li>
        </ul>
    '''
    
    return {
        "subject": "✅ domulex.ai – E-Mail-Test erfolgreich",
        "html": get_base_template(content, "E-Mail-Test"),
        "text": f"""E-Mail-Test erfolgreich!

Ihre E-Mail-Konfiguration funktioniert einwandfrei.

Ihr domulex.ai Team
"""
    }


def get_support_contact_confirmation_email(user_name: str, user_message: str) -> dict:
    """Confirmation email sent to user when they submit a support request"""
    content = f'''
        <h2>Wir haben Ihre Anfrage erhalten 📬</h2>
        
        <p>Hallo <strong>{user_name}</strong>,</p>
        
        <p>vielen Dank für Ihre Nachricht! Unser Support-Team hat Ihre Anfrage erhalten und wird sich so schnell wie möglich bei Ihnen melden.</p>
        
        <div class="info-box">
            <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 13px;">📝 Ihre Nachricht:</p>
            <p style="margin: 0; white-space: pre-wrap;">{user_message}</p>
        </div>
        
        <div class="success-box">
            <strong>⏱️ Bearbeitungszeit:</strong>
            <p style="margin: 10px 0 0 0;">In der Regel antworten wir innerhalb von 24 Stunden (werktags).</p>
        </div>
        
        <p>In der Zwischenzeit können Sie gerne unseren FAQ-Bereich besuchen:</p>
        
        <p style="text-align: center;">
            <a href="{COMPANY_WEBSITE}/faq" class="button">FAQ besuchen →</a>
        </p>
    '''
    
    return {
        "subject": "✅ Ihre Anfrage bei domulex.ai wurde empfangen",
        "html": get_base_template(content, "Anfrage empfangen"),
        "text": f"""Wir haben Ihre Anfrage erhalten

Hallo {user_name},

vielen Dank für Ihre Nachricht! Unser Support-Team hat Ihre Anfrage erhalten und wird sich so schnell wie möglich bei Ihnen melden.

Ihre Nachricht:
{user_message}

Bearbeitungszeit: In der Regel antworten wir innerhalb von 24 Stunden (werktags).

FAQ besuchen: {COMPANY_WEBSITE}/faq

Ihr domulex.ai Team
{COMPANY_NAME}
{COMPANY_STREET}, {COMPANY_CITY}
"""
    }


def get_support_contact_internal_email(user_name: str, user_email: str, user_message: str, chat_history: str = "") -> dict:
    """Internal email sent to support team when user submits a request"""
    chat_section = ""
    if chat_history:
        chat_section = f'''
        <div class="warning-box" style="background-color: #f3f4f6; border-left-color: #6b7280;">
            <strong>💬 Chat-Verlauf mit KI-Assistent:</strong>
            <pre style="white-space: pre-wrap; font-family: inherit; margin: 10px 0 0 0; font-size: 13px; color: #4b5563; background: white; padding: 10px; border-radius: 4px;">{chat_history}</pre>
        </div>
        '''
    
    content = f'''
        <h2>📧 Neue Support-Anfrage</h2>
        
        <div class="info-box">
            <p style="margin: 0 0 5px 0; color: #6b7280; font-size: 13px;">Absender:</p>
            <p style="margin: 0; font-size: 18px; font-weight: bold; color: {PRIMARY_COLOR};">{user_name}</p>
            <p style="margin: 5px 0 0 0;"><a href="mailto:{user_email}" style="color: {SECONDARY_COLOR};">{user_email}</a></p>
        </div>
        
        <div class="info-box" style="background-color: #fefce8; border-left-color: #eab308;">
            <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 13px;">📝 Nachricht:</p>
            <p style="margin: 0; white-space: pre-wrap; font-size: 15px;">{user_message}</p>
        </div>
        
        {chat_section}
        
        <p style="text-align: center;">
            <a href="mailto:{user_email}?subject=Re: Ihre Anfrage bei domulex.ai" class="button">↩️ Antworten</a>
        </p>
    '''
    
    return {
        "subject": f"📧 Support-Anfrage von {user_name} ({user_email})",
        "html": get_base_template(content, "Support-Anfrage"),
        "text": f"""Neue Support-Anfrage

Von: {user_name}
E-Mail: {user_email}

Nachricht:
{user_message}

---
Chat-Verlauf:
{chat_history or 'Kein Chat-Verlauf verfügbar'}

---
Antworten: mailto:{user_email}
"""
    }
