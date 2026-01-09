"""
Firebase Authentication Middleware for DOMULEX Backend
"""

import logging
import uuid
from datetime import datetime
from typing import Optional
from functools import wraps

from fastapi import HTTPException, Security, Depends, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth, firestore

from config import get_settings


logger = logging.getLogger(__name__)
settings = get_settings()

# Security scheme
security = HTTPBearer()

# Initialize Firebase Admin (only if credentials available)
_firebase_initialized = False
_firestore_db = None


def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    global _firebase_initialized, _firestore_db
    
    if _firebase_initialized:
        return
    
    try:
        # Try to initialize Firebase - different methods depending on environment
        
        # Method 1: Try with explicit credentials from environment variables
        if settings.firebase_private_key and settings.firebase_client_email:
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": settings.firebase_project_id,
                "private_key_id": settings.firebase_private_key_id or "",
                "private_key": settings.firebase_private_key.replace('\\n', '\n'),
                "client_email": settings.firebase_client_email,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            })
            firebase_admin.initialize_app(cred)
            _firebase_initialized = True
            _firestore_db = firestore.client()
            logger.info("✅ Firebase Admin initialized with service account credentials")
            return
        
        # Method 2: Try with Application Default Credentials (works on Cloud Run)
        if settings.firebase_project_id:
            try:
                firebase_admin.initialize_app(options={
                    'projectId': settings.firebase_project_id
                })
                _firebase_initialized = True
                _firestore_db = firestore.client()
                logger.info("✅ Firebase Admin initialized with Application Default Credentials")
                return
            except Exception as e:
                logger.warning(f"ADC initialization failed: {e}")
        
        # Method 3: Try without any credentials (uses GOOGLE_APPLICATION_CREDENTIALS)
        try:
            firebase_admin.initialize_app()
            _firebase_initialized = True
            _firestore_db = firestore.client()
            logger.info("✅ Firebase Admin initialized with default credentials")
            return
        except Exception as e:
            logger.warning(f"Default initialization failed: {e}")
        
        logger.warning("🔓 Firebase Auth disabled - No valid credentials found")
    
    except Exception as e:
        logger.error(f"❌ Firebase initialization failed: {e}")


class FirebaseUser:
    """Authenticated Firebase user."""
    
    def __init__(self, uid: str, email: Optional[str] = None, claims: dict = None, session_id: str = None):
        self.uid = uid
        self.email = email
        self.claims = claims or {}
        self.session_id = session_id
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.claims.get('admin', False)
    
    @property
    def is_premium(self) -> bool:
        """Check if user has premium subscription."""
        return self.claims.get('premium', False)


def get_firestore_db():
    """Get Firestore database instance."""
    global _firestore_db
    if not _firestore_db and _firebase_initialized:
        _firestore_db = firestore.client()
    return _firestore_db


async def validate_session(uid: str, session_id: str) -> bool:
    """
    Validate that the session_id matches the active session for this user.
    Returns True if session is valid, False if user should be logged out.
    """
    if not session_id:
        return True  # No session enforcement for requests without session_id
    
    db = get_firestore_db()
    if not db:
        return True  # Skip validation if Firestore not available
    
    try:
        user_doc = db.collection('users').document(uid).get()
        if not user_doc.exists:
            return True  # New user, no session yet
        
        user_data = user_doc.to_dict()
        stored_session_id = user_data.get('activeSessionId')
        
        # If no stored session, this is the first session
        if not stored_session_id:
            return True
        
        # Check if session matches
        if stored_session_id != session_id:
            logger.warning(f"Session mismatch for user {uid}: expected {stored_session_id[:8]}..., got {session_id[:8]}...")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Session validation error: {e}")
        return True  # On error, allow access


async def register_session(uid: str, session_id: str, device_info: str = None) -> dict:
    """
    Register a new session for a user, invalidating any previous sessions.
    """
    db = get_firestore_db()
    if not db:
        return {"success": False, "error": "Database not available"}
    
    try:
        user_ref = db.collection('users').document(uid)
        user_ref.update({
            'activeSessionId': session_id,
            'lastSessionAt': datetime.utcnow().isoformat(),
            'lastDeviceInfo': device_info or 'Unknown',
        })
        logger.info(f"✅ Session registered for user {uid}: {session_id[:8]}...")
        return {"success": True, "session_id": session_id}
    except Exception as e:
        logger.error(f"Session registration error: {e}")
        return {"success": False, "error": str(e)}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
) -> FirebaseUser:
    """
    Verify Firebase ID token and return authenticated user.
    
    Usage:
    ```python
    @app.get("/protected")
    async def protected_route(user: FirebaseUser = Depends(get_current_user)):
        return {"user_id": user.uid, "email": user.email}
    ```
    """
    if not _firebase_initialized:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Firebase Authentication not configured"
        )
    
    token = credentials.credentials
    
    try:
        # Verify ID token
        decoded_token = auth.verify_id_token(token)
        
        uid = decoded_token['uid']
        
        # Validate session if session_id provided
        if x_session_id:
            session_valid = await validate_session(uid, x_session_id)
            if not session_valid:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="SESSION_EXPIRED_OTHER_DEVICE"
                )
        
        user = FirebaseUser(
            uid=uid,
            email=decoded_token.get('email'),
            claims=decoded_token,
            session_id=x_session_id,
        )
        
        return user
    
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked"
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(lambda: None)
) -> Optional[FirebaseUser]:
    """
    Get authenticated user if token provided, otherwise None.
    Useful for optional authentication.
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
    except HTTPException:
        return None


def require_admin(user: FirebaseUser):
    """Require admin role."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def require_premium(user: FirebaseUser):
    """Require premium subscription."""
    if not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Premium subscription required for this feature"
        )


# Admin E-Mails (müssen mit Frontend übereinstimmen)
ADMIN_EMAILS = ['kontakt@domulex.ai', 'admin@domulex.ai']


def is_admin_email(email: str) -> bool:
    """Prüft ob eine E-Mail Admin-Berechtigung hat."""
    return email.lower() in [e.lower() for e in ADMIN_EMAILS]


def create_firebase_user(email: str, password: str, display_name: str = None) -> dict:
    """
    Erstellt einen neuen Firebase Auth User.
    Gibt User-Info zurück mit uid.
    """
    if not _firebase_initialized:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Firebase nicht initialisiert"
        )
    
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name or email.split('@')[0],
            email_verified=False,
        )
        logger.info(f"✅ Firebase User erstellt: {email} (UID: {user.uid})")
        return {
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
        }
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-Mail bereits registriert"
        )
    except Exception as e:
        logger.error(f"❌ Fehler beim Erstellen des Users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Erstellen: {str(e)}"
        )


def delete_firebase_user(uid: str) -> bool:
    """
    Löscht einen Firebase Auth User.
    """
    if not _firebase_initialized:
        return False
    
    try:
        auth.delete_user(uid)
        logger.info(f"✅ Firebase User gelöscht: {uid}")
        return True
    except auth.UserNotFoundError:
        logger.warning(f"User nicht gefunden: {uid}")
        return True  # Schon gelöscht = OK
    except Exception as e:
        logger.error(f"❌ Fehler beim Löschen des Users: {e}")
        return False
