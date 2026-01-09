"""
User Model with Subscription Management
"""

from datetime import datetime, date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SubscriptionTier(Enum):
    """User subscription tiers."""
    FREE = "free"
    TENANT = "tenant"  # 9€/month - Tenant-focused features
    PRO = "pro"  # 29€/month - Full features
    LAWYER = "lawyer"  # 49€/month - Professional tools


class User(BaseModel):
    """User model with subscription tracking."""
    id: str
    email: str
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    queries_used_this_month: int = 0
    last_reset_date: date = Field(default_factory=date.today)
    created_at: datetime = Field(default_factory=datetime.now)
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    
    def get_quota_limit(self) -> int:
        """Get monthly query limit based on tier."""
        limits = {
            SubscriptionTier.FREE: 3,
            SubscriptionTier.TENANT: 25,      # Basis: 25 Anfragen/Monat
            SubscriptionTier.PRO: 250,        # Professional: 250 Anfragen/Monat
            SubscriptionTier.LAWYER: 999999,  # Lawyer Pro: Unbegrenzt
        }
        return limits.get(self.subscription_tier, 3)
    
    def reset_quota_if_needed(self):
        """Reset monthly quota if we're in a new month."""
        today = date.today()
        if today.month != self.last_reset_date.month or today.year != self.last_reset_date.year:
            self.queries_used_this_month = 0
            self.last_reset_date = today
    
    def has_quota(self) -> bool:
        """Check if user has remaining quota."""
        self.reset_quota_if_needed()
        return self.queries_used_this_month < self.get_quota_limit()
    
    def increment_usage(self):
        """Increment query counter."""
        self.reset_quota_if_needed()
        self.queries_used_this_month += 1
    
    def can_access_feature(self, feature: str) -> bool:
        """Check if user's tier grants access to a feature."""
        feature_gates = {
            "PDF_UPLOAD": [SubscriptionTier.PRO, SubscriptionTier.LAWYER],
            "INTERNATIONAL_SEARCH": [SubscriptionTier.PRO, SubscriptionTier.LAWYER],
            "API_ACCESS": [SubscriptionTier.LAWYER],
            "BULK_ANALYSIS": [SubscriptionTier.LAWYER],
            "CONTRACT_COMPARISON": [SubscriptionTier.PRO, SubscriptionTier.LAWYER],
            "DISPUTE_RESOLUTION": [SubscriptionTier.TENANT, SubscriptionTier.PRO, SubscriptionTier.LAWYER],
        }
        allowed_tiers = feature_gates.get(feature, [])
        return self.subscription_tier in allowed_tiers


# Tier pricing and features
TIER_DETAILS = {
    SubscriptionTier.FREE: {
        "name": "Test",
        "price": 0,
        "queries": 3,
        "features": [
            "✅ 3 Test-Anfragen insgesamt",
            "✅ Basis-Antworten",
            "✅ Nur Deutschland",
            "❌ Keine PDF-Uploads",
            "❌ Konto wird nach 6 Monaten gelöscht",
        ],
        "color": "amber",
    },
    SubscriptionTier.TENANT: {
        "name": "Basis",
        "price": 19,
        "queries": 50,
        "features": [
            "✅ 50 Fragen pro Monat",
            "✅ KI mit Rechtsquellen",
            "✅ Steuer-Basics (AfA, Werbungskosten)",
            "✅ Email-Support",
            "❌ Kein PDF-Upload",
        ],
        "color": "blue",
    },
    SubscriptionTier.PRO: {
        "name": "Professional",
        "price": 39,
        "queries": 250,
        "features": [
            "✅ 250 Fragen pro Monat",
            "✅ Alle Basis Features",
            "✅ Erweiterte Steuer-Analysen",
            "✅ PDF-Upload & Analyse",
            "✅ Vertragsanalyse",
            "✅ Priority Support",
        ],
        "color": "green",
        "recommended": True,
    },
    SubscriptionTier.LAWYER: {
        "name": "Lawyer Pro",
        "price": 69,
        "queries": 999999,
        "features": [
            "✅ Unbegrenzte Anfragen",
            "✅ Alle Professional Features",
            "✅ Mandanten-CRM",
            "✅ KI-Schriftsatzgenerierung",
            "✅ Fristenverwaltung",
            "✅ Premium-Support 24/7",
        ],
        "color": "purple",
    },
}
