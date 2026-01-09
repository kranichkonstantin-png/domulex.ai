"""
Email service for sending transactional emails
Uses SMTP (Strato/custom server) for reliable email delivery
"""
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

# Import professional templates
from services.email_templates import (
    get_welcome_email,
    get_order_confirmation_email,
    get_payment_failed_email,
    get_subscription_cancelled_email,
    get_admin_notification_email,
    get_tier_change_email,
    get_deletion_reminder_email,
    get_order_confirmation_b2b_email,
    get_test_email,
)

logger = logging.getLogger(__name__)

# Try to import Firebase for config storage
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False
    logger.warning("Firestore not available for email config")


class EmailService:
    """Service for sending emails via SMTP (Strato or custom SMTP server)"""
    
    def __init__(self):
        # Default config from environment
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.strato.de")
        self.smtp_port = int(os.getenv("SMTP_PORT", "465"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "info@domulex.ai")
        self.from_name = os.getenv("FROM_NAME", "domulex.ai")
        self.use_ssl = os.getenv("SMTP_USE_SSL", "true").lower() == "true"
        
        # Try to load config from Firestore
        self._load_config_from_firestore()
        
        # Check if configured
        self.configured = bool(self.smtp_user and self.smtp_password)
        
        if not self.configured:
            logger.warning("SMTP not configured - emails will not be sent")
        else:
            logger.info(f"SMTP configured: {self.smtp_host}:{self.smtp_port} as {self.smtp_user}")
    
    def _load_config_from_firestore(self):
        """Load SMTP config from Firestore if available"""
        if not FIRESTORE_AVAILABLE:
            return
        
        try:
            db = firestore.Client()
            config_doc = db.collection('settings').document('email_config').get()
            
            if config_doc.exists:
                config = config_doc.to_dict()
                self.smtp_host = config.get('smtp_host', self.smtp_host)
                self.smtp_port = int(config.get('smtp_port', self.smtp_port))
                self.smtp_user = config.get('smtp_user', self.smtp_user)
                self.smtp_password = config.get('smtp_password', self.smtp_password)
                self.from_email = config.get('from_email', self.from_email)
                self.from_name = config.get('from_name', self.from_name)
                self.use_ssl = config.get('use_ssl', self.use_ssl)
                logger.info("Loaded SMTP config from Firestore")
        except Exception as e:
            logger.warning(f"Could not load SMTP config from Firestore: {e}")
    
    def reload_config(self):
        """Reload configuration from Firestore"""
        self._load_config_from_firestore()
        self.configured = bool(self.smtp_user and self.smtp_password)
        return self.configured
    
    def get_config_status(self) -> Dict[str, Any]:
        """Get current config status (without password)"""
        return {
            "configured": self.configured,
            "smtp_host": self.smtp_host,
            "smtp_port": self.smtp_port,
            "smtp_user": self.smtp_user,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "use_ssl": self.use_ssl,
        }
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None,
        attachments: Optional[List[Dict[str, str]]] = None
    ) -> bool:
        """Send an email via SMTP"""
        if not self.configured:
            logger.error("SMTP not configured - cannot send email")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email
            msg["Reply-To"] = self.from_email
            msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0100")
            msg["Message-ID"] = f"<{datetime.now().strftime('%Y%m%d%H%M%S')}.{id(msg)}@domulex.ai>"
            msg["X-Mailer"] = "domulex.ai"
            msg["MIME-Version"] = "1.0"
            
            # Add plain text if provided
            if plain_content:
                part1 = MIMEText(plain_content, "plain", "utf-8")
                msg.attach(part1)
            
            # Add HTML content
            part2 = MIMEText(html_content, "html", "utf-8")
            msg.attach(part2)
            
            # Send email - Port 587 always uses STARTTLS, Port 465 always uses SSL
            if self.smtp_port == 465:
                # SSL connection (port 465)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context) as server:
                    server.login(self.smtp_user, self.smtp_password)
                    server.sendmail(self.from_email, to_email, msg.as_string())
            else:
                # STARTTLS connection (port 587 or other)
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_user, self.smtp_password)
                    server.sendmail(self.from_email, to_email, msg.as_string())
            
            logger.info(f"Email sent successfully to {to_email}: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending to {to_email}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def test_connection(self) -> Dict[str, Any]:
        """Test SMTP connection without sending email"""
        if not self.configured:
            return {"success": False, "error": "SMTP nicht konfiguriert"}
        
        try:
            # Port 587 always uses STARTTLS, Port 465 always uses SSL
            if self.smtp_port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=10) as server:
                    server.login(self.smtp_user, self.smtp_password)
            else:
                # Port 587 or other - use STARTTLS
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_user, self.smtp_password)
            
            return {"success": True, "message": f"Verbindung zu {self.smtp_host}:{self.smtp_port} erfolgreich"}
        except smtplib.SMTPAuthenticationError:
            return {"success": False, "error": "Authentifizierung fehlgeschlagen - Benutzername oder Passwort falsch"}
        except smtplib.SMTPConnectError:
            return {"success": False, "error": f"Verbindung zu {self.smtp_host}:{self.smtp_port} fehlgeschlagen"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_test_email(self, to_email: str) -> Dict[str, Any]:
        """Send a test email to verify configuration"""
        template = get_test_email()
        
        success = self.send_email(to_email, template["subject"], template["html"], template["text"])
        
        if success:
            return {"success": True, "message": f"Test-E-Mail an {to_email} gesendet"}
        else:
            return {"success": False, "error": "E-Mail konnte nicht gesendet werden"}
    
    def send_welcome_email(self, user_email: str, user_name: Optional[str] = None) -> bool:
        """Send welcome email after registration"""
        name = user_name or user_email.split('@')[0]
        template = get_welcome_email(name)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
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
        template = get_order_confirmation_email(user_name, plan_name, plan_price, subscription_id, invoice_url)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
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
        """Send B2B order confirmation with AVV/NDA references"""
        template = get_order_confirmation_b2b_email(user_name, company_name, plan_name, plan_price, subscription_id, invoice_url)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
    def send_payment_failed(self, user_email: str, user_name: str) -> bool:
        """Send notification when payment fails"""
        template = get_payment_failed_email(user_name)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
    def send_subscription_cancelled(self, user_email: str, user_name: str, end_date: str) -> bool:
        """Send subscription cancellation confirmation"""
        template = get_subscription_cancelled_email(user_name, end_date)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
    def send_admin_notification(self, user_email: str, user_name: str, title: str, message: str) -> bool:
        """Send admin notification to user"""
        template = get_admin_notification_email(user_name, title, message)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
    def send_tier_change(self, user_email: str, user_name: str, new_tier: str, queries_limit: int) -> bool:
        """Send tier change notification"""
        template = get_tier_change_email(user_name, new_tier, queries_limit)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])
    
    def send_deletion_reminder(self, user_email: str, user_name: str, deletion_date: str) -> bool:
        """Send account deletion reminder"""
        template = get_deletion_reminder_email(user_name, deletion_date)
        return self.send_email(user_email, template["subject"], template["html"], template["text"])


# Global instance
email_service = EmailService()
