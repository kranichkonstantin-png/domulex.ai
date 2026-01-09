"""
Email Client Service for sending and receiving emails
Uses SMTP for sending and IMAP for receiving
"""
import os
import smtplib
import ssl
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

# Try to import Firebase for config storage
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False


class EmailClient:
    """Full email client for sending and receiving via SMTP/IMAP"""
    
    def __init__(self):
        # SMTP config (sending) - Gmail uses STARTTLS on port 587
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        # IMAP config (receiving)
        self.imap_host = "imap.gmail.com"
        self.imap_port = 993
        # Credentials
        self.email_user = ""
        self.email_password = ""
        self.from_name = "domulex.ai"
        
        # Load config
        self._load_config()
        self.configured = bool(self.email_user and self.email_password)
    
    def _load_config(self):
        """Load config from Firestore"""
        if not FIRESTORE_AVAILABLE:
            return
        
        try:
            db = firestore.Client()
            config_doc = db.collection('settings').document('email_config').get()
            
            if config_doc.exists:
                config = config_doc.to_dict()
                self.smtp_host = config.get('smtp_host', self.smtp_host)
                self.smtp_port = int(config.get('smtp_port', self.smtp_port))
                self.email_user = config.get('smtp_user', '')
                self.email_password = config.get('smtp_password', '')
                self.from_name = config.get('from_name', self.from_name)
                logger.info(f"Email client loaded config for {self.email_user}")
        except Exception as e:
            logger.warning(f"Could not load email config: {e}")
    
    def reload_config(self):
        """Reload configuration"""
        self._load_config()
        self.configured = bool(self.email_user and self.email_password)
        return self.configured
    
    def _decode_header_value(self, value: str) -> str:
        """Decode email header value"""
        if not value:
            return ""
        decoded_parts = []
        for part, encoding in decode_header(value):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
            else:
                decoded_parts.append(part)
        return ''.join(decoded_parts)
    
    def _extract_email_address(self, header: str) -> str:
        """Extract email address from header like 'Name <email@example.com>'"""
        if not header:
            return ""
        match = re.search(r'<([^>]+)>', header)
        if match:
            return match.group(1)
        return header.strip()
    
    def _get_email_body(self, msg) -> Dict[str, str]:
        """Extract text and html body from email"""
        text_body = ""
        html_body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                if "attachment" in content_disposition:
                    continue
                
                try:
                    body = part.get_payload(decode=True)
                    if body:
                        charset = part.get_content_charset() or 'utf-8'
                        body_text = body.decode(charset, errors='replace')
                        
                        if content_type == "text/plain":
                            text_body = body_text
                        elif content_type == "text/html":
                            html_body = body_text
                except Exception as e:
                    logger.warning(f"Error decoding email part: {e}")
        else:
            content_type = msg.get_content_type()
            try:
                body = msg.get_payload(decode=True)
                if body:
                    charset = msg.get_content_charset() or 'utf-8'
                    body_text = body.decode(charset, errors='replace')
                    if content_type == "text/html":
                        html_body = body_text
                    else:
                        text_body = body_text
            except Exception as e:
                logger.warning(f"Error decoding email body: {e}")
        
        return {"text": text_body, "html": html_body}
    
    def fetch_emails(self, folder: str = "INBOX", limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch emails from IMAP server"""
        if not self.configured:
            return []
        
        emails = []
        
        try:
            # Connect to IMAP
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                imap.select(folder)
                
                # Search for all emails
                status, messages = imap.search(None, "ALL")
                if status != "OK":
                    return []
                
                message_ids = messages[0].split()
                # Get latest emails first
                message_ids = list(reversed(message_ids))[:limit]
                
                for msg_id in message_ids:
                    try:
                        status, msg_data = imap.fetch(msg_id, "(RFC822 FLAGS)")
                        if status != "OK":
                            continue
                        
                        raw_email = msg_data[0][1]
                        msg = email.message_from_bytes(raw_email)
                        
                        # Parse flags
                        flags_data = msg_data[0][0].decode() if msg_data[0][0] else ""
                        is_read = "\\Seen" in flags_data
                        
                        # Parse date
                        date_str = msg.get("Date", "")
                        try:
                            parsed_date = email.utils.parsedate_to_datetime(date_str)
                            date_formatted = parsed_date.strftime("%d.%m.%Y %H:%M")
                        except:
                            date_formatted = date_str[:20] if date_str else ""
                        
                        # Get body
                        body = self._get_email_body(msg)
                        
                        emails.append({
                            "id": msg_id.decode(),
                            "from": self._decode_header_value(msg.get("From", "")),
                            "from_email": self._extract_email_address(msg.get("From", "")),
                            "to": self._decode_header_value(msg.get("To", "")),
                            "subject": self._decode_header_value(msg.get("Subject", "(Kein Betreff)")),
                            "date": date_formatted,
                            "is_read": is_read,
                            "body_text": body["text"][:500] if body["text"] else "",
                            "body_html": body["html"],
                            "has_attachments": any(
                                part.get("Content-Disposition", "").startswith("attachment")
                                for part in msg.walk() if msg.is_multipart()
                            ),
                        })
                    except Exception as e:
                        logger.warning(f"Error parsing email {msg_id}: {e}")
                        continue
                
                imap.logout()
        
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP error: {e}")
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
        
        return emails
    
    def get_email(self, email_id: str, folder: str = "INBOX") -> Optional[Dict[str, Any]]:
        """Get a single email with full content"""
        if not self.configured:
            return None
        
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                imap.select(folder)
                
                # Mark as read
                imap.store(email_id.encode(), '+FLAGS', '\\Seen')
                
                status, msg_data = imap.fetch(email_id.encode(), "(RFC822)")
                if status != "OK":
                    return None
                
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                body = self._get_email_body(msg)
                
                # Parse date
                date_str = msg.get("Date", "")
                try:
                    parsed_date = email.utils.parsedate_to_datetime(date_str)
                    date_formatted = parsed_date.strftime("%d.%m.%Y %H:%M:%S")
                except:
                    date_formatted = date_str
                
                # Get attachments info
                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        content_disposition = str(part.get("Content-Disposition", ""))
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                attachments.append({
                                    "filename": self._decode_header_value(filename),
                                    "content_type": part.get_content_type(),
                                    "size": len(part.get_payload(decode=True) or b""),
                                })
                
                imap.logout()
                
                return {
                    "id": email_id,
                    "from": self._decode_header_value(msg.get("From", "")),
                    "from_email": self._extract_email_address(msg.get("From", "")),
                    "to": self._decode_header_value(msg.get("To", "")),
                    "cc": self._decode_header_value(msg.get("Cc", "")),
                    "subject": self._decode_header_value(msg.get("Subject", "(Kein Betreff)")),
                    "date": date_formatted,
                    "body_text": body["text"],
                    "body_html": body["html"],
                    "attachments": attachments,
                }
        
        except Exception as e:
            logger.error(f"Error getting email {email_id}: {e}")
            return None
    
    def get_folders(self) -> List[str]:
        """Get list of email folders"""
        if not self.configured:
            return []
        
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                
                status, folders = imap.list()
                if status != "OK":
                    return ["INBOX"]
                
                folder_list = []
                for folder in folders:
                    # Parse folder name
                    match = re.search(r'"([^"]*)" "?([^"]*)"?$', folder.decode())
                    if match:
                        folder_name = match.group(2)
                        folder_list.append(folder_name)
                
                imap.logout()
                return folder_list if folder_list else ["INBOX"]
        
        except Exception as e:
            logger.error(f"Error getting folders: {e}")
            return ["INBOX"]
    
    def send_email(
        self,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send an email"""
        if not self.configured:
            return {"success": False, "error": "E-Mail nicht konfiguriert"}
        
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.email_user}>"
            msg["To"] = to
            if cc:
                msg["Cc"] = cc
            if reply_to:
                msg["Reply-To"] = reply_to
            
            # Add body
            msg.attach(MIMEText(body_text, "plain", "utf-8"))
            if body_html:
                msg.attach(MIMEText(body_html, "html", "utf-8"))
            
            # Build recipient list
            recipients = [to]
            if cc:
                recipients.extend([addr.strip() for addr in cc.split(",")])
            if bcc:
                recipients.extend([addr.strip() for addr in bcc.split(",")])
            
            # Send via SMTP - Gmail uses STARTTLS on port 587
            context = ssl.create_default_context()
            
            # Check if using SSL port (465) or STARTTLS port (587)
            if self.smtp_port == 465:
                # SSL connection
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context) as server:
                    server.login(self.email_user, self.email_password)
                    server.sendmail(self.email_user, recipients, msg.as_string())
            else:
                # STARTTLS connection (Gmail port 587)
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.email_user, self.email_password)
                    server.sendmail(self.email_user, recipients, msg.as_string())
            
            logger.info(f"Email sent to {to}: {subject}")
            return {"success": True, "message": f"E-Mail an {to} gesendet"}
        
        except smtplib.SMTPAuthenticationError:
            return {"success": False, "error": "Authentifizierung fehlgeschlagen"}
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_email(self, email_id: str, folder: str = "INBOX") -> Dict[str, Any]:
        """Delete an email (move to trash)"""
        if not self.configured:
            return {"success": False, "error": "E-Mail nicht konfiguriert"}
        
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                imap.select(folder)
                
                # Mark as deleted
                imap.store(email_id.encode(), '+FLAGS', '\\Deleted')
                imap.expunge()
                
                imap.logout()
            
            return {"success": True, "message": "E-Mail gelöscht"}
        
        except Exception as e:
            logger.error(f"Error deleting email: {e}")
            return {"success": False, "error": str(e)}
    
    def mark_as_read(self, email_id: str, folder: str = "INBOX") -> Dict[str, Any]:
        """Mark email as read"""
        if not self.configured:
            return {"success": False, "error": "E-Mail nicht konfiguriert"}
        
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                # Read-write mode (default)
                imap.select(folder)
                # Use UID or message sequence number as bytes
                msg_id = email_id.encode() if isinstance(email_id, str) else email_id
                status, response = imap.store(msg_id, '+FLAGS', '(\\Seen)')
                logger.info(f"Mark as read: email_id={email_id}, status={status}, response={response}")
                imap.logout()
            
            return {"success": status == "OK"}
        except Exception as e:
            logger.error(f"Error marking email as read: {e}")
            return {"success": False, "error": str(e)}
    
    def mark_as_unread(self, email_id: str, folder: str = "INBOX") -> Dict[str, Any]:
        """Mark email as unread"""
        if not self.configured:
            return {"success": False, "error": "E-Mail nicht konfiguriert"}
        
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                imap.select(folder)
                msg_id = email_id.encode() if isinstance(email_id, str) else email_id
                status, response = imap.store(msg_id, '-FLAGS', '(\\Seen)')
                logger.info(f"Mark as unread: email_id={email_id}, status={status}, response={response}")
                imap.logout()
            
            return {"success": status == "OK"}
        except Exception as e:
            logger.error(f"Error marking email as unread: {e}")
            return {"success": False, "error": str(e)}
    
    def get_unread_count(self, folder: str = "INBOX") -> int:
        """Get count of unread emails"""
        if not self.configured:
            return 0
        
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_host, self.imap_port, ssl_context=context) as imap:
                imap.login(self.email_user, self.email_password)
                imap.select(folder)
                
                status, messages = imap.search(None, "UNSEEN")
                if status != "OK":
                    return 0
                
                count = len(messages[0].split()) if messages[0] else 0
                imap.logout()
                return count
        
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            return 0
    
    def send_with_template(
        self,
        to: str,
        subject: str,
        body_text: str,
        use_template: bool = True,
    ) -> Dict[str, Any]:
        """Send email with Domulex.ai branding template"""
        if not self.configured:
            return {"success": False, "error": "E-Mail nicht konfiguriert"}
        
        html_body = None
        
        if use_template:
            # Import template
            try:
                from services.email_templates import get_base_template
                
                # Convert newlines to <br> for HTML
                html_content = body_text.replace('\n', '<br>')
                html_body = get_base_template(f"<p>{html_content}</p>", subject)
            except Exception as e:
                logger.warning(f"Could not use template: {e}")
        
        return self.send_email(to, subject, body_text, html_body)


# Global instance
email_client = EmailClient()