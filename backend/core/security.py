"""
Security & Quota Management
Middleware for enforcing subscription limits and feature gates.
"""

from fastapi import HTTPException, status
from models.user import User, SubscriptionTier


class QuotaExceededException(HTTPException):
    """Raised when user exceeds monthly quota."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "quota_exceeded",
                "message": "Sie haben Ihr monatliches Limit erreicht.",
                "action": "upgrade",
            }
        )


class UpgradeRequiredException(HTTPException):
    """Raised when user tries to access a premium feature."""
    def __init__(self, feature: str, required_tier: str):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "feature_locked",
                "message": f"'{feature}' ist nur für {required_tier}-Nutzer verfügbar.",
                "feature": feature,
                "required_tier": required_tier,
                "action": "upgrade",
            }
        )


def check_quota(user: User) -> None:
    """
    Check if user has quota available.
    Raises QuotaExceededException if limit reached.
    """
    if not user.has_quota():
        raise QuotaExceededException()


def check_feature_access(user: User, feature: str) -> None:
    """
    Check if user's tier grants access to a feature.
    Raises UpgradeRequiredException if not allowed.
    """
    if not user.can_access_feature(feature):
        # Determine required tier
        if feature in ["API_ACCESS", "BULK_ANALYSIS"]:
            required = "Lawyer Pro"
        elif feature in ["PDF_UPLOAD", "CONTRACT_COMPARISON"]:
            required = "Professional"
        else:
            required = "Mieter Plus"
        
        raise UpgradeRequiredException(feature, required)


def enforce_limits(user: User, request_type: str = "QUERY") -> None:
    """
    Main enforcement function - checks both quota and feature access.
    
    Args:
        user: Current user
        request_type: Type of request (QUERY, PDF_UPLOAD, INTERNATIONAL_SEARCH, etc.)
    """
    # Always check quota first
    check_quota(user)
    
    # Feature-specific gates
    if request_type == "PDF_UPLOAD":
        check_feature_access(user, "PDF_UPLOAD")
    
    elif request_type == "INTERNATIONAL_SEARCH":
        # Free users can only search Germany
        if user.subscription_tier == SubscriptionTier.FREE:
            check_feature_access(user, "INTERNATIONAL_SEARCH")
    
    elif request_type == "API_REQUEST":
        check_feature_access(user, "API_ACCESS")
    
    elif request_type == "BULK_ANALYSIS":
        check_feature_access(user, "BULK_ANALYSIS")
    
    elif request_type == "CONTRACT_COMPARISON":
        check_feature_access(user, "CONTRACT_COMPARISON")
    
    # Increment usage counter
    user.increment_usage()


def get_mock_user(tier: SubscriptionTier = SubscriptionTier.FREE) -> User:
    """
    Get a mock user for testing.
    In production, this would fetch from database.
    """
    return User(
        id="mock_user_123",
        email="demo@domulex.ai",
        subscription_tier=tier,
        queries_used_this_month=0,
    )
