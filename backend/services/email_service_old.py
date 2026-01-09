"""
Email service for sending transactional emails
Uses Resend for reliable email delivery
"""
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Try to import Resend
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logger.warning("Resend not available - install with: pip install resend")

class EmailService:
    """Service for sending emails via Resend"""
    
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY", "")
        self.from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
        self.from_name = os.getenv("FROM_NAME", "Domulex.ai")
        
        if RESEND_AVAILABLE and self.api_key:
            resend.api_key = self.api_key
            self.client = resend
        else:
            self.client = None
            logger.warning("Resend not configured")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, str]]] = None
    ) -> bool:
        """Send an email via Resend"""
        if not self.client:
            logger.error("Resend client not available")
            return False
        
        try:
            # Prepare email params
            email_params = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }
            
            # Add plain text if provided
            if plain_content:
                email_params["text"] = plain_content
            
            # Send email
            response = resend.Emails.send(email_params)
            
            logger.info(f"Email sent to {to_email}: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_welcome_email(self, user_email: str, user_name: Optional[str] = None) -> bool:
        """Send welcome email after registration"""
        name = user_name or user_email.split('@')[0]
        
        subject = "Willkommen bei Domulex.ai! 🏛️"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
        .features {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .feature {{ margin: 15px 0; padding-left: 30px; position: relative; }}
        .feature:before {{ content: "✓"; position: absolute; left: 0; color: #10b981; font-weight: bold; font-size: 20px; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ Willkommen bei Domulex.ai</h1>
        </div>
        
        <div class="content">
            <h2>Hallo {name}!</h2>
            
            <p>Vielen Dank für Ihre Registrierung bei Domulex.ai - Ihrer KI-Rechtsassistenz für Immobilien.</p>
            
            <p><strong>Ihr Test-Tarif:</strong></p>
            
            <div class="features">
                <div class="feature">3 Test-Anfragen zum Ausprobieren</div>
                <div class="feature">Zugang zu deutschem Immobilienrecht</div>
                <div class="feature">1.201 aktuelle Rechtsdokumente</div>
                <div class="feature">Täglich aktualisierte Datenbank</div>
                <div class="feature">DSGVO-konform & Zero Data Retention</div>
            </div>
            
            <div style="background: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="margin: 0; color: #92400e;"><strong>Hinweis:</strong> Nach 6 Monaten ohne Upgrade wird Ihr Test-Konto automatisch gelöscht. Upgraden Sie auf einen unserer Tarife, um alle Funktionen dauerhaft zu nutzen!</p>
            </div>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/app" class="button">Jetzt loslegen →</a>
            </p>
            
            <p><strong>Nächste Schritte:</strong></p>
            <ol>
                <li>Bestätigen Sie Ihre E-Mail-Adresse</li>
                <li>Stellen Sie Ihre erste Rechtsfrage</li>
                <li>Entdecken Sie unsere Premium-Funktionen</li>
            </ol>
            
            <p>Bei Fragen sind wir jederzeit für Sie da unter <a href="mailto:support@domulex.ai">support@domulex.ai</a></p>
            
            <p>Viel Erfolg!</p>
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
        
        <div class="footer">
            <img src="https://domulex.ai/logo.png" alt="Domulex.ai" style="height: 40px; margin-bottom: 15px;">
            <p>Home Invest & Management GmbH<br>
            Zur Maate 19, 31515 Wunstorf<br>
            <a href="https://domulex.ai/datenschutz">Datenschutz</a> | 
            <a href="https://domulex.ai/agb">AGB</a> | 
            <a href="https://domulex.ai/impressum">Impressum</a></p>
        </div>
    </div>
</body>
</html>
        """
        
        plain_content = f"""
Willkommen bei Domulex.ai!

Hallo {name},

Vielen Dank für Ihre Registrierung bei Domulex.ai - Ihrer KI-Rechtsassistenz für Immobilien.

Ihr Test-Tarif:
- 3 Test-Anfragen zum Ausprobieren
- Zugang zu deutschem Immobilienrecht
- 1.201 aktuelle Rechtsdokumente
- Täglich aktualisierte Datenbank
- DSGVO-konform & Zero Data Retention

Hinweis: Nach 6 Monaten ohne Upgrade wird Ihr Test-Konto automatisch gelöscht.

Jetzt loslegen: https://domulex.ai/app

Nächste Schritte:
1. Bestätigen Sie Ihre E-Mail-Adresse
2. Stellen Sie Ihre erste Rechtsfrage
3. Entdecken Sie unsere Premium-Funktionen

Bei Fragen: support@domulex.ai

Viel Erfolg!
Ihr Domulex.ai Team
        """
        
        return self.send_email(user_email, subject, html_content, plain_content)
    
    def send_order_confirmation(
        self,
        user_email: str,
        user_name: str,
        plan_name: str,
        plan_price: float,
        subscription_id: str,
        invoice_url: Optional[str] = None
    ) -> bool:
        """Send order confirmation after successful payment"""
        
        subject = f"Bestellbestätigung - {plan_name}"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .order-box {{ background: white; border: 2px solid #10b981; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .price {{ font-size: 32px; font-weight: bold; color: #10b981; }}
        .button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 10px 5px; }}
        .info-box {{ background: #e0f2fe; border-left: 4px solid #0284c7; padding: 15px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Bestellung erfolgreich!</h1>
        </div>
        
        <div class="content">
            <h2>Vielen Dank, {user_name}!</h2>
            
            <p>Ihre Bestellung wurde erfolgreich abgeschlossen.</p>
            
            <div class="order-box">
                <h3 style="margin-top: 0;">{plan_name}</h3>
                <p class="price">{plan_price:.2f} €/Monat</p>
                <p style="color: #6b7280;">Abonnement-ID: {subscription_id}</p>
            </div>
            
            <div class="info-box">
                <strong>📄 Ihre Rechnung</strong><br>
                {f'<a href="{invoice_url}">Rechnung als PDF herunterladen</a>' if invoice_url else 'Ihre Rechnung wird Ihnen in Kürze per E-Mail zugesendet.'}
            </div>
            
            <p><strong>Was passiert jetzt?</strong></p>
            <ul>
                <li>Ihr Upgrade wurde sofort aktiviert</li>
                <li>Sie haben jetzt Zugriff auf alle Premium-Features</li>
                <li>Die monatliche Abrechnung erfolgt automatisch</li>
                <li>Sie können jederzeit kündigen</li>
            </ul>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/app" class="button">Zur App →</a>
                <a href="https://domulex.ai/konto" class="button" style="background: #6b7280;">Mein Bereich</a>
            </p>
            
            <div class="info-box" style="background: #fef3c7; border-left-color: #f59e0b;">
                <strong>ℹ️ Widerrufsrecht (für Verbraucher)</strong><br>
                Sie haben das Recht, binnen 14 Tagen ohne Angabe von Gründen diesen Vertrag zu widerrufen.
                <a href="https://domulex.ai/agb#widerruf">Mehr erfahren</a>
            </div>
            
            <p>Bei Fragen kontaktieren Sie uns unter <a href="mailto:support@domulex.ai">support@domulex.ai</a></p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
        
        <div class="footer">
            <img src="https://domulex.ai/logo.png" alt="Domulex.ai" style="height: 40px; margin-bottom: 15px;">
            <p>Home Invest & Management GmbH<br>
            Zur Maate 19, 31515 Wunstorf<br>
            <a href="https://domulex.ai/konto">Abo verwalten</a> | 
            <a href="https://domulex.ai/kuendigen">Kündigen</a></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_payment_failed(self, user_email: str, user_name: str) -> bool:
        """Send notification when payment fails"""
        subject = "⚠️ Zahlungsproblem bei Ihrem Domulex.ai Abonnement"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .button {{ display: inline-block; background: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
        .warning-box {{ background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚠️ Zahlungsproblem</h1>
        </div>
        
        <div class="content">
            <h2>Hallo {user_name},</h2>
            
            <p>leider konnten wir Ihre letzte Zahlung nicht verarbeiten.</p>
            
            <div class="warning-box">
                <strong>Was bedeutet das?</strong><br>
                Ihr Abonnement bleibt zunächst aktiv, aber wir benötigen eine aktualisierte Zahlungsmethode.
            </div>
            
            <p><strong>Nächste Schritte:</strong></p>
            <ol>
                <li>Öffnen Sie Ihr Kundenkonto</li>
                <li>Aktualisieren Sie Ihre Zahlungsmethode</li>
                <li>Die Zahlung wird automatisch wiederholt</li>
            </ol>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/konto" class="button">Zahlungsmethode aktualisieren →</a>
            </p>
            
            <p>Bei Fragen helfen wir gerne: <a href="mailto:support@domulex.ai">support@domulex.ai</a></p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_subscription_cancelled(self, user_email: str, user_name: str, end_date: str) -> bool:
        """Send confirmation when subscription is cancelled"""
        subject = "Kündigungsbestätigung - Domulex.ai"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .info-box {{ background: #e0f2fe; border-left: 4px solid #0284c7; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Kündigungsbestätigung</h1>
        </div>
        
        <div class="content">
            <h2>Hallo {user_name},</h2>
            
            <p>wir bestätigen die Kündigung Ihres Abonnements.</p>
            
            <div class="info-box">
                <strong>Wichtig:</strong><br>
                Ihr Zugang bleibt bis zum <strong>{end_date}</strong> aktiv.<br>
                Sie können Domulex.ai bis dahin weiterhin nutzen.
            </div>
            
            <p>Nach Ablauf Ihres Abonnements werden Sie automatisch auf den Test-Tarif herabgestuft.</p>
            
            <p><strong>Test-Tarif Hinweis:</strong></p>
            <ul>
                <li>3 Anfragen insgesamt (falls noch nicht verbraucht)</li>
                <li>Deutsches Immobilienrecht</li>
                <li>Nach 6 Monaten ohne erneutes Upgrade wird das Konto gelöscht</li>
            </ul>
            
            <p>Wir würden uns freuen, Sie bald wiederzusehen!</p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)

    def send_admin_notification(self, user_email: str, user_name: str, title: str, message: str) -> bool:
        """Send admin notification email to user"""
        subject = f"Nachricht von Domulex.ai: {title}"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .message-box {{ background: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
        .button {{ display: inline-block; background: #1e3a5f; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👑 {title}</h1>
        </div>
        
        <div class="content">
            <h2>Hallo {user_name},</h2>
            
            <div class="message-box">
                <p style="white-space: pre-wrap;">{message}</p>
            </div>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/app/notifications" class="button">Alle Benachrichtigungen anzeigen →</a>
            </p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
        
        <div class="footer">
            <p>Diese E-Mail wurde automatisch gesendet. Bei Fragen antworten Sie einfach auf diese E-Mail.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)

    def send_tier_change(self, user_email: str, user_name: str, new_tier: str, queries_limit: int) -> bool:
        """Send notification when user tier is changed"""
        subject = "Ihr Abo wurde aktualisiert - Domulex.ai"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .tier-box {{ background: #d1fae5; border: 2px solid #10b981; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center; }}
        .button {{ display: inline-block; background: #1e3a5f; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Abo aktualisiert</h1>
        </div>
        
        <div class="content">
            <h2>Hallo {user_name},</h2>
            
            <p>Ihr Abonnement bei Domulex.ai wurde aktualisiert.</p>
            
            <div class="tier-box">
                <h3 style="margin: 0 0 10px 0; color: #059669;">Ihr neuer Tarif:</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 0; color: #1e3a5f;">{new_tier}</p>
                <p style="margin: 10px 0 0 0; color: #6b7280;">{queries_limit} Anfragen pro Monat</p>
            </div>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/app" class="button">Jetzt nutzen →</a>
            </p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)

    def send_account_deletion_reminder(self, user_email: str, user_name: str, deletion_date: str) -> bool:
        """Send reminder 7 days before account deletion"""
        subject = "⚠️ Ihr Konto wird in 7 Tagen gelöscht - Domulex.ai"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .warning-box {{ background: #fef3c7; border: 2px solid #f59e0b; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .button {{ display: inline-block; background: #1e3a5f; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚠️ Wichtige Mitteilung</h1>
        </div>
        
        <div class="content">
            <h2>Hallo {user_name},</h2>
            
            <div class="warning-box">
                <strong>Ihr Konto wird am {deletion_date} gelöscht.</strong>
                <p>Da Ihr Test-Tarif seit 6 Monaten inaktiv ist, wird Ihr Konto in 7 Tagen automatisch gelöscht.</p>
            </div>
            
            <p><strong>Was Sie tun können:</strong></p>
            <ul>
                <li>Melden Sie sich an und nutzen Sie Domulex.ai</li>
                <li>Oder upgraden Sie auf einen kostenpflichtigen Tarif</li>
            </ul>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/auth/login" class="button">Jetzt anmelden →</a>
            </p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)

        return self.send_email(user_email, subject, html_content)

    def send_order_confirmation_b2b(
        self,
        user_email: str,
        user_name: str,
        company_name: str,
        plan_name: str,
        plan_price: float,
        subscription_id: str,
        invoice_url: Optional[str] = None
    ) -> bool:
        """Send order confirmation for B2B customers including AVV and NDA"""
        
        subject = f"Bestellbestätigung (B2B) - {plan_name} | AVV & NDA"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; }}
        .order-box {{ background: white; border: 2px solid #1e3a5f; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .price {{ font-size: 32px; font-weight: bold; color: #1e3a5f; }}
        .button {{ display: inline-block; background: #1e3a5f; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 10px 5px; }}
        .document-box {{ background: #fef3c7; border: 2px solid #f59e0b; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .legal-box {{ background: #e0f2fe; border-left: 4px solid #0284c7; padding: 15px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Bestellung erfolgreich (B2B)</h1>
        </div>
        
        <div class="content">
            <h2>Vielen Dank, {user_name}!</h2>
            <p style="color: #6b7280; margin-top: -10px;">{company_name}</p>
            
            <p>Ihre Bestellung wurde erfolgreich abgeschlossen.</p>
            
            <div class="order-box">
                <h3 style="margin-top: 0;">{plan_name}</h3>
                <p class="price">{plan_price:.2f} €/Monat (netto)</p>
                <p style="color: #6b7280;">Abonnement-ID: {subscription_id}</p>
                <p style="color: #6b7280; font-size: 14px;">zzgl. MwSt.</p>
            </div>
            
            <div class="document-box">
                <h3 style="margin-top: 0;">📋 Vertragsbestandteile (B2B)</h3>
                <p>Als gewerblicher Kunde sind folgende Dokumente Bestandteil Ihres Vertrags:</p>
                <ul>
                    <li><a href="https://domulex.ai/agb">Allgemeine Geschäftsbedingungen (AGB)</a></li>
                    <li><a href="https://domulex.ai/datenschutz">Datenschutzhinweise</a></li>
                    <li><strong><a href="https://domulex.ai/avv">Auftragsverarbeitungsvertrag (AVV)</a></strong> gemäß Art. 28 DSGVO</li>
                    <li><strong><a href="https://domulex.ai/nda">Geheimhaltungsvereinbarung (NDA)</a></strong></li>
                </ul>
                <p style="font-size: 12px; color: #6b7280; margin-bottom: 0;">
                    Diese Dokumente gelten mit Ihrer Bestellung als akzeptiert. Bitte speichern Sie diese für Ihre Unterlagen.
                </p>
            </div>
            
            <div class="legal-box">
                <strong>📄 Rechnung</strong><br>
                {f'<a href="{invoice_url}">Rechnung als PDF herunterladen</a>' if invoice_url else 'Ihre Rechnung wird Ihnen in Kürze per E-Mail zugesendet.'}
            </div>
            
            <p><strong>Als Geschäftskunde haben Sie:</strong></p>
            <ul>
                <li>Kein Widerrufsrecht (§ 312g Abs. 2 Nr. 1 BGB)</li>
                <li>Sofortigen Zugang zu allen Funktionen</li>
                <li>Rechnungsstellung mit ausgewiesener MwSt.</li>
                <li>DSGVO-konforme Datenverarbeitung mit AVV</li>
                <li>Vertraglich gesicherte Vertraulichkeit durch NDA</li>
            </ul>
            
            <p style="text-align: center;">
                <a href="https://domulex.ai/app" class="button">Zur App →</a>
                <a href="https://domulex.ai/konto" class="button" style="background: #6b7280;">Mein Bereich</a>
            </p>
            
            <h3>🔒 Ihre Daten sind sicher</h3>
            <ul>
                <li>Serverstandort: Frankfurt am Main, Deutschland</li>
                <li>Verschlüsselung: TLS 1.3 + AES-256</li>
                <li>Zero Data Retention bei KI-Verarbeitung</li>
                <li>ISO 27001 zertifizierte Infrastruktur</li>
            </ul>
            
            <p>Bei Fragen kontaktieren Sie uns unter <a href="mailto:business@domulex.ai">business@domulex.ai</a></p>
            
            <p><strong>Ihr Domulex.ai Team</strong></p>
        </div>
        
        <div class="footer">
            <img src="https://domulex.ai/logo.png" alt="Domulex.ai" style="height: 40px; margin-bottom: 15px;">
            <p>Home Invest & Management GmbH<br>
            Zur Maate 19, 31515 Wunstorf<br>
            <a href="https://domulex.ai/agb">AGB</a> | 
            <a href="https://domulex.ai/datenschutz">Datenschutz</a> | 
            <a href="https://domulex.ai/avv">AVV</a> | 
            <a href="https://domulex.ai/nda">NDA</a></p>
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, html_content)

# Global instance
email_service = EmailService()
