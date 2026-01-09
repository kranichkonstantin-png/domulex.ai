# Domulex.ai Cloud Functions
# Firebase Cloud Functions for automation

from firebase_functions import https_fn, scheduler_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app, firestore
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
initialize_app()

# Backend URL
BACKEND_URL = "https://domulex-backend-841507936108.europe-west3.run.app"

# Cost control
set_global_options(max_instances=10)


@https_fn.on_call()
def send_order_confirmation(req: https_fn.CallableRequest) -> dict:
    """
    Callable function to send order confirmation emails.
    Called by Stripe webhooks or checkout success page.
    """
    try:
        data = req.data
        
        user_email = data.get('user_email')
        user_name = data.get('user_name')
        plan_name = data.get('plan_name')
        plan_price = data.get('plan_price')
        subscription_id = data.get('subscription_id')
        
        if not all([user_email, user_name, plan_name, plan_price, subscription_id]):
            return {'success': False, 'error': 'Missing required fields'}
        
        # Forward to backend email service
        response = requests.post(
            f"{BACKEND_URL}/email/send-order-confirmation",
            data={
                'user_email': user_email,
                'user_name': user_name,
                'plan_name': plan_name,
                'plan_price': plan_price,
                'subscription_id': subscription_id,
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return {'success': True, 'message': f'Order confirmation sent to {user_email}'}
        else:
            return {'success': False, 'error': 'Failed to send email'}
            
    except Exception as e:
        logger.error(f"Error sending order confirmation: {e}")
        return {'success': False, 'error': str(e)}


@scheduler_fn.on_schedule(schedule="0 0 1 * *", timezone="Europe/Berlin")
def reset_monthly_queries(event: scheduler_fn.ScheduledEvent) -> None:
    """
    Scheduled function to reset monthly query counters.
    Runs on the 1st of every month at 00:00 Berlin time.
    """
    try:
        db = firestore.client()
        
        # Get all users with queries > 0
        users_ref = db.collection('users').where('queriesUsed', '>', 0)
        users = users_ref.get()
        
        count = 0
        for user in users:
            user.reference.update({'queriesUsed': 0})
            count += 1
        
        logger.info(f"Reset query counters for {count} users")
        
    except Exception as e:
        logger.error(f"Error resetting queries: {e}")