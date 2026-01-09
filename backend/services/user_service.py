"""
User Service for Firestore User Management
Handles subscription updates, query counting, and user profile management.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from firebase_admin import firestore

logger = logging.getLogger(__name__)

# Plan limits for each tier
PLAN_LIMITS = {
    'free': 3,
    'basis': 25,            # Basis: 25 Anfragen/Monat
    'professional': 250,    # Professional: 250 Anfragen/Monat
    'lawyer': 999999,       # Lawyer Pro: Unbegrenzt
}

# Map Stripe tier names to Firestore plan names
STRIPE_TO_FIRESTORE_TIER = {
    'TENANT': 'basis',
    'PRO': 'professional',
    'LAWYER': 'lawyer',
    'basis': 'basis',
    'mieter_plus': 'basis',  # Legacy mapping
    'professional': 'professional',
    'lawyer': 'lawyer',
}


class UserService:
    """Service for managing user data in Firestore."""
    
    def __init__(self):
        """Initialize the UserService with Firestore client."""
        try:
            self.db = firestore.client()
            self._initialized = True
            logger.info("✅ UserService initialized with Firestore")
        except Exception as e:
            logger.error(f"❌ UserService initialization failed: {e}")
            self._initialized = False
            self.db = None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user data from Firestore.
        
        Args:
            user_id: Firebase Auth UID
            
        Returns:
            User data dict or None if not found
        """
        if not self._initialized:
            return None
            
        try:
            doc = self.db.collection('users').document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user data by email.
        
        Args:
            email: User email address
            
        Returns:
            Tuple of (user_id, user_data) or (None, None) if not found
        """
        if not self._initialized:
            return None
            
        try:
            docs = self.db.collection('users').where('email', '==', email).limit(1).stream()
            for doc in docs:
                return {'id': doc.id, **doc.to_dict()}
            return None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    def update_subscription(
        self,
        user_id: str,
        tier: str,
        stripe_customer_id: Optional[str] = None,
        stripe_subscription_id: Optional[str] = None,
        subscription_status: str = 'active'
    ) -> bool:
        """
        Update user subscription in Firestore after successful payment.
        
        Args:
            user_id: Firebase Auth UID
            tier: New subscription tier (from Stripe: TENANT, PRO, LAWYER)
            stripe_customer_id: Stripe customer ID
            stripe_subscription_id: Stripe subscription ID
            subscription_status: Subscription status (active, canceled, etc.)
            
        Returns:
            True if update successful, False otherwise
        """
        if not self._initialized:
            logger.error("UserService not initialized")
            return False
            
        try:
            # Map Stripe tier to Firestore plan name
            plan = STRIPE_TO_FIRESTORE_TIER.get(tier, tier.lower() if tier else 'free')
            queries_limit = PLAN_LIMITS.get(plan, 3)
            
            update_data = {
                'plan': plan,
                'tier': plan,  # Also update tier for backwards compatibility
                'queriesLimit': queries_limit,
                'subscriptionStatus': subscription_status,
                'updatedAt': firestore.SERVER_TIMESTAMP,
            }
            
            if stripe_customer_id:
                update_data['stripeCustomerId'] = stripe_customer_id
            
            if stripe_subscription_id:
                update_data['stripeSubscriptionId'] = stripe_subscription_id
            
            self.db.collection('users').document(user_id).update(update_data)
            
            logger.info(f"✅ Updated subscription for user {user_id}: plan={plan}, limit={queries_limit}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating subscription for user {user_id}: {e}")
            return False
    
    def cancel_subscription(self, user_id: str) -> bool:
        """
        Cancel user subscription (downgrade to free).
        
        Args:
            user_id: Firebase Auth UID
            
        Returns:
            True if cancellation successful, False otherwise
        """
        if not self._initialized:
            return False
            
        try:
            self.db.collection('users').document(user_id).update({
                'plan': 'free',
                'tier': 'free',
                'queriesLimit': PLAN_LIMITS['free'],
                'subscriptionStatus': 'canceled',
                'updatedAt': firestore.SERVER_TIMESTAMP,
            })
            
            logger.info(f"✅ Cancelled subscription for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cancelling subscription for user {user_id}: {e}")
            return False
    
    def increment_query_count(self, user_id: str) -> Optional[int]:
        """
        Increment user's query count and return new count.
        
        Args:
            user_id: Firebase Auth UID
            
        Returns:
            New query count or None on error
        """
        if not self._initialized:
            return None
            
        try:
            user_ref = self.db.collection('users').document(user_id)
            
            # Use transaction for atomic increment
            @firestore.transactional
            def update_in_transaction(transaction):
                snapshot = user_ref.get(transaction=transaction)
                if not snapshot.exists:
                    return None
                
                current = snapshot.get('queriesUsed') or 0
                new_count = current + 1
                
                transaction.update(user_ref, {
                    'queriesUsed': new_count,
                    'lastQueryAt': firestore.SERVER_TIMESTAMP,
                })
                
                return new_count
            
            transaction = self.db.transaction()
            new_count = update_in_transaction(transaction)
            
            if new_count is not None:
                logger.debug(f"Incremented query count for user {user_id}: {new_count}")
            
            return new_count
            
        except Exception as e:
            logger.error(f"Error incrementing query count for user {user_id}: {e}")
            return None
    
    def check_query_limit(self, user_id: str) -> tuple[bool, int, int]:
        """
        Check if user has remaining queries.
        
        Args:
            user_id: Firebase Auth UID
            
        Returns:
            Tuple of (can_query, queries_used, queries_limit)
        """
        if not self._initialized:
            return False, 0, 0
            
        try:
            user = self.get_user(user_id)
            if not user:
                return False, 0, 0
            
            queries_used = user.get('queriesUsed', 0)
            queries_limit = user.get('queriesLimit', PLAN_LIMITS['free'])
            
            can_query = queries_used < queries_limit
            
            return can_query, queries_used, queries_limit
            
        except Exception as e:
            logger.error(f"Error checking query limit for user {user_id}: {e}")
            return False, 0, 0
    
    def reset_monthly_queries(self, user_id: str) -> bool:
        """
        Reset user's monthly query count (called at billing cycle start).
        
        Args:
            user_id: Firebase Auth UID
            
        Returns:
            True if reset successful, False otherwise
        """
        if not self._initialized:
            return False
            
        try:
            self.db.collection('users').document(user_id).update({
                'queriesUsed': 0,
                'lastResetAt': firestore.SERVER_TIMESTAMP,
                'updatedAt': firestore.SERVER_TIMESTAMP,
            })
            
            logger.info(f"✅ Reset monthly queries for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error resetting queries for user {user_id}: {e}")
            return False
    
    def add_query_pack(self, user_id: str, queries: int) -> bool:
        """
        Add purchased query pack to user's limit.
        
        Args:
            user_id: Firebase Auth UID
            queries: Number of queries to add
            
        Returns:
            True if update successful, False otherwise
        """
        if not self._initialized:
            return False
            
        try:
            user_ref = self.db.collection('users').document(user_id)
            
            # Use transaction to atomically add queries
            @firestore.transactional
            def add_queries_in_transaction(transaction):
                snapshot = user_ref.get(transaction=transaction)
                if not snapshot.exists:
                    return False
                
                current_limit = snapshot.get('queriesLimit') or 0
                new_limit = current_limit + queries
                
                transaction.update(user_ref, {
                    'queriesLimit': new_limit,
                    'lastQueryPackAt': firestore.SERVER_TIMESTAMP,
                    'updatedAt': firestore.SERVER_TIMESTAMP,
                })
                
                return True
            
            transaction = self.db.transaction()
            success = add_queries_in_transaction(transaction)
            
            if success:
                logger.info(f"✅ Added {queries} queries to user {user_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error adding query pack for user {user_id}: {e}")
            return False


# Singleton instance
_user_service: Optional[UserService] = None


def get_user_service() -> UserService:
    """Get or create UserService singleton."""
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service
