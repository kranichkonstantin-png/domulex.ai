"""
DOMULEX Paywall System - Quick Reference
Pricing Tiers & Feature Gates
"""

# ==================== PRICING STRUCTURE ====================

TIERS = {
    "FREE": {
        "price": 0,
        "queries": 3,
        "jurisdictions": ["DE"],
        "features": ["basic_search"],
    },
    "TENANT": {
        "price": 9,
        "queries": 100,
        "jurisdictions": ["DE", "US", "ES"],
        "features": ["basic_search", "dispute_resolution", "all_jurisdictions"],
    },
    "PRO": {
        "price": 29,
        "queries": 500,
        "jurisdictions": ["DE", "US", "ES"],
        "features": [
            "basic_search",
            "dispute_resolution",
            "all_jurisdictions",
            "pdf_upload",
            "contract_comparison",
            "all_roles",
        ],
    },
    "LAWYER": {
        "price": 49,
        "queries": 1000,
        "jurisdictions": ["DE", "US", "ES"],
        "features": [
            "basic_search",
            "dispute_resolution",
            "all_jurisdictions",
            "pdf_upload",
            "contract_comparison",
            "all_roles",
            "api_access",
            "bulk_analysis",
            "priority_support",
        ],
    },
}

# ==================== FEATURE GATES ====================

FEATURE_REQUIREMENTS = {
    # Feature: Minimum required tier
    "PDF_UPLOAD": "PRO",
    "INTERNATIONAL_SEARCH": "TENANT",  # US/ES searches
    "CONTRACT_COMPARISON": "PRO",
    "API_ACCESS": "LAWYER",
    "BULK_ANALYSIS": "LAWYER",
    "DISPUTE_RESOLUTION": "TENANT",
    "ALL_ROLES": "PRO",  # Switch between Tenant/Investor/Manager/Lawyer
}

# ==================== USAGE EXAMPLES ====================

"""
# Backend Usage:
from core.security import enforce_limits, get_mock_user

user = get_mock_user(tier=SubscriptionTier.FREE)

# Check quota before query
enforce_limits(user, "QUERY")

# Check feature access
enforce_limits(user, "PDF_UPLOAD")  # Raises UpgradeRequiredException if FREE


# Frontend Usage:
from paywall import check_and_enforce_quota, check_feature_access

# Before processing query
if not check_and_enforce_quota():
    return  # Paywall modal shown automatically

# Before showing PDF upload button
if check_feature_access("PDF_UPLOAD"):
    st.file_uploader("Upload PDF")
else:
    st.info("PDF Upload is a Pro feature - Upgrade to unlock!")
"""

# ==================== CONVERSION TRACKING ====================

CONVERSION_EVENTS = {
    "paywall_shown": ["quota_exceeded", "feature_locked"],
    "pricing_table_viewed": ["from_paywall", "from_sidebar"],
    "upgrade_clicked": ["tier_selected"],
    "upgrade_completed": ["payment_success"],
    "upgrade_cancelled": ["payment_cancelled"],
}

# ==================== RECOMMENDED COPY ====================

PAYWALL_MESSAGES = {
    "quota_exceeded": {
        "title": "🚫 Limit erreicht!",
        "message": "Sie haben Ihre {limit} kostenlosen Fragen diesen Monat aufgebraucht.",
        "cta": "Upgraden für unbegrenzte Fragen",
    },
    "pdf_upload_locked": {
        "title": "🔒 Premium Feature",
        "message": "PDF-Upload ist nur für Professional und Lawyer Pro verfügbar.",
        "cta": "Jetzt upgraden - ab 29€/Monat",
    },
    "international_search_locked": {
        "title": "🌍 Multi-Jurisdictions freischalten",
        "message": "Suchen Sie in US & spanischem Recht mit Mieter Plus.",
        "cta": "Upgraden für nur 9€/Monat",
    },
}
