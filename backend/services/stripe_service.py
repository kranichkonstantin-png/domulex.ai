"""
Stripe payment service for subscription management
"""
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

# Setup basic logging
logger = logging.getLogger(__name__)

# Try to import Stripe
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

# Initialize Stripe with secret key (only if available)
if STRIPE_AVAILABLE and os.getenv("STRIPE_SECRET_KEY"):
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


def get_stripe_price_ids():
    """Get Stripe Price IDs from environment variables."""
    return {
        "TENANT": os.getenv("STRIPE_PRICE_TENANT", ""),
        "BASIS": os.getenv("STRIPE_PRICE_TENANT", ""),  # Alias for frontend
        "PRO": os.getenv("STRIPE_PRICE_PRO", ""),
        "PROFESSIONAL": os.getenv("STRIPE_PRICE_PRO", ""),  # Alias for frontend
        "LAWYER": os.getenv("STRIPE_PRICE_LAWYER", ""),
    }


class StripeService:
    """Service for handling Stripe payment operations"""
    
    @staticmethod
    def create_checkout_session(
        user_email: str,
        tier: str,  # Tier as string: "TENANT", "PRO", "LAWYER"
        success_url: str,
        cancel_url: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout Session for subscription
        
        Args:
            user_email: User's email address
            tier: Subscription tier to purchase (TENANT, PRO, LAWYER)
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if payment is cancelled
            user_id: Optional user ID to track in metadata
            
        Returns:
            Dict with session URL and session ID
        """
        if not STRIPE_AVAILABLE:
            raise RuntimeError("Stripe module not available")
        
        try:
            tier_upper = tier.upper() if isinstance(tier, str) else str(tier).upper()
            
            if tier_upper == "FREE":
                raise ValueError("Cannot create checkout for FREE tier")
            
            price_ids = get_stripe_price_ids()
            price_id = price_ids.get(tier_upper, "")
            
            if not price_id:
                raise ValueError(f"No Stripe Price ID configured for tier: {tier}")
            
            # Create Checkout Session
            # Note: Frontend already adds session_id to success_url, so use as-is
            session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user_id or user_email,
                    'tier': tier_upper,
                    'timestamp': datetime.utcnow().isoformat(),
                },
                subscription_data={
                    'metadata': {
                        'user_id': user_id or user_email,
                        'tier': tier_upper,
                    }
                },
                billing_address_collection='required',
                allow_promotion_codes=True,
                # Custom fields for company name and usage type
                custom_fields=[
                    {
                        'key': 'company_name',
                        'label': {'type': 'custom', 'custom': 'Firmenname (optional)'},
                        'type': 'text',
                        'optional': True,
                    },
                    {
                        'key': 'usage_type',
                        'label': {'type': 'custom', 'custom': 'Nutzungsart'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Privat', 'value': 'private'},
                                {'label': 'Gewerblich', 'value': 'commercial'},
                            ],
                        },
                    },
                ],
            )
            
            logger.info(f"Created Stripe Checkout Session: {session.id} for {user_email} - {tier_upper}")
            
            return {
                'url': session.url,
                'session_id': session.id,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout session: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            raise
    
    @staticmethod
    def create_query_pack_checkout(
        user_email: str,
        pack_type: str,  # "basis" or "professional"
        success_url: str,
        cancel_url: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Checkout Session for one-time query pack purchase
        
        Args:
            user_email: User's email address
            pack_type: Pack type - "basis" (20 queries for 5€) or "professional" (50 queries for 10€)
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect if payment is cancelled
            user_id: Optional user ID to track in metadata
            
        Returns:
            Dict with session URL and session ID
        """
        if not STRIPE_AVAILABLE:
            raise RuntimeError("Stripe module not available")
        
        try:
            # Define pack details
            pack_details = {
                "basis": {
                    "name": "Basis Anfragen-Paket",
                    "description": "20 zusätzliche KI-Anfragen",
                    "queries": 20,
                    "amount": 500,  # 5.00 EUR in cents
                },
                "professional": {
                    "name": "Professional Anfragen-Paket",
                    "description": "50 zusätzliche KI-Anfragen",
                    "queries": 50,
                    "amount": 1000,  # 10.00 EUR in cents
                },
            }
            
            pack = pack_details.get(pack_type.lower())
            if not pack:
                raise ValueError(f"Invalid pack type: {pack_type}")
            
            # Create Checkout Session for one-time payment
            session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': pack['name'],
                            'description': pack['description'],
                        },
                        'unit_amount': pack['amount'],
                    },
                    'quantity': 1,
                }],
                mode='payment',  # One-time payment, not subscription
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user_id or user_email,
                    'pack_type': pack_type.lower(),
                    'queries': pack['queries'],
                    'type': 'query_pack',
                    'timestamp': datetime.utcnow().isoformat(),
                },
            )
            
            logger.info(f"Created Query Pack Checkout Session: {session.id} for {user_email} - {pack_type}")
            
            return {
                'url': session.url,
                'session_id': session.id,
                'queries': pack['queries'],
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating query pack checkout: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating query pack checkout: {e}")
            raise
    
    @staticmethod
    def create_customer_portal_session(
        customer_id: str,
        return_url: str
    ) -> Dict[str, Any]:
        """
        Create a Stripe Customer Portal session for managing subscription
        
        Args:
            customer_id: Stripe customer ID
            return_url: URL to return to after portal session
            
        Returns:
            Dict with portal URL
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            logger.info(f"Created Stripe Portal Session for customer: {customer_id}")
            
            return {
                'url': session.url,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating portal session: {e}")
            raise
    
    @staticmethod
    def handle_webhook_event(
        payload: bytes,
        signature: str,
        webhook_secret: str
    ) -> Optional[Dict[str, Any]]:
        """
        Handle Stripe webhook events
        
        Args:
            payload: Raw request body
            signature: Stripe signature header
            webhook_secret: Webhook signing secret
            
        Returns:
            Dict with event data if processed, None otherwise
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            logger.info(f"Received Stripe webhook: {event['type']}")
            
            # Handle different event types
            if event['type'] == 'checkout.session.completed':
                return StripeService._handle_checkout_completed(event['data']['object'])
            
            elif event['type'] == 'customer.subscription.created':
                return StripeService._handle_subscription_created(event['data']['object'])
            
            elif event['type'] == 'customer.subscription.updated':
                return StripeService._handle_subscription_updated(event['data']['object'])
            
            elif event['type'] == 'customer.subscription.deleted':
                return StripeService._handle_subscription_deleted(event['data']['object'])
            
            elif event['type'] == 'invoice.payment_succeeded':
                return StripeService._handle_payment_succeeded(event['data']['object'])
            
            elif event['type'] == 'invoice.payment_failed':
                return StripeService._handle_payment_failed(event['data']['object'])
            
            return None
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {e}")
            raise
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            raise
    
    @staticmethod
    def _handle_checkout_completed(session: Dict[str, Any]) -> Dict[str, Any]:
        """Handle checkout.session.completed event"""
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        customer_id = session.get('customer')
        
        # Check if this is a query pack purchase
        if metadata.get('type') == 'query_pack':
            queries = int(metadata.get('queries', 0))
            pack_type = metadata.get('pack_type')
            
            logger.info(f"Query pack checkout completed: user={user_id}, pack={pack_type}, queries={queries}")
            
            return {
                'event': 'query_pack_purchased',
                'user_id': user_id,
                'queries': queries,
                'pack_type': pack_type,
                'customer_id': customer_id,
            }
        
        # Regular subscription checkout
        tier_value = metadata.get('tier')
        subscription_id = session.get('subscription')
        
        logger.info(f"Checkout completed: user={user_id}, tier={tier_value}, customer={customer_id}")
        
        return {
            'event': 'checkout_completed',
            'user_id': user_id,
            'tier': tier_value,
            'customer_id': customer_id,
            'subscription_id': subscription_id,
        }
    
    @staticmethod
    def _handle_subscription_created(subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer.subscription.created event"""
        user_id = subscription.get('metadata', {}).get('user_id')
        tier_value = subscription.get('metadata', {}).get('tier')
        status = subscription.get('status')
        
        logger.info(f"Subscription created: user={user_id}, tier={tier_value}, status={status}")
        
        return {
            'event': 'subscription_created',
            'user_id': user_id,
            'tier': tier_value,
            'status': status,
            'subscription_id': subscription.get('id'),
        }
    
    @staticmethod
    def _handle_subscription_updated(subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer.subscription.updated event"""
        user_id = subscription.get('metadata', {}).get('user_id')
        status = subscription.get('status')
        
        logger.info(f"Subscription updated: user={user_id}, status={status}")
        
        return {
            'event': 'subscription_updated',
            'user_id': user_id,
            'status': status,
            'subscription_id': subscription.get('id'),
        }
    
    @staticmethod
    def _handle_subscription_deleted(subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer.subscription.deleted event"""
        user_id = subscription.get('metadata', {}).get('user_id')
        
        logger.info(f"Subscription deleted: user={user_id}")
        
        return {
            'event': 'subscription_deleted',
            'user_id': user_id,
            'subscription_id': subscription.get('id'),
        }
    
    @staticmethod
    def _handle_payment_succeeded(invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle invoice.payment_succeeded event"""
        subscription_id = invoice.get('subscription')
        customer_id = invoice.get('customer')
        
        logger.info(f"Payment succeeded: customer={customer_id}, subscription={subscription_id}")
        
        return {
            'event': 'payment_succeeded',
            'customer_id': customer_id,
            'subscription_id': subscription_id,
            'amount': invoice.get('amount_paid'),
        }
    
    @staticmethod
    def _handle_payment_failed(invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle invoice.payment_failed event"""
        subscription_id = invoice.get('subscription')
        customer_id = invoice.get('customer')
        
        logger.warning(f"Payment failed: customer={customer_id}, subscription={subscription_id}")
        
        return {
            'event': 'payment_failed',
            'customer_id': customer_id,
            'subscription_id': subscription_id,
        }
    
    @staticmethod
    def get_subscription_status(subscription_id: str) -> Dict[str, Any]:
        """
        Get current subscription status from Stripe
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Dict with subscription details
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            
            return {
                'status': subscription.status,
                'current_period_end': datetime.fromtimestamp(subscription.current_period_end),
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'customer_id': subscription.customer,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving subscription: {e}")
            raise
    
    @staticmethod
    def cancel_subscription(subscription_id: str, at_period_end: bool = True) -> Dict[str, Any]:
        """
        Cancel a subscription
        
        Args:
            subscription_id: Stripe subscription ID
            at_period_end: If True, cancel at end of billing period; if False, cancel immediately
            
        Returns:
            Dict with cancellation details
        """
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)
            
            logger.info(f"Cancelled subscription: {subscription_id}, at_period_end={at_period_end}")
            
            return {
                'cancelled': True,
                'at_period_end': at_period_end,
                'status': subscription.status,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error cancelling subscription: {e}")
            raise
