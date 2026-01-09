// Stripe Client-Side Integration
import { loadStripe, Stripe } from '@stripe/stripe-js';

// Lade Stripe
let stripePromise: Promise<Stripe | null>;
export const getStripe = () => {
  if (!stripePromise) {
    stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);
  }
  return stripePromise;
};

export interface CheckoutSessionParams {
  priceId: string; // Deprecated, nicht mehr verwendet
  customerEmail?: string;
  userId?: string;
  planName: string; // TENANT, PRO, oder LAWYER
  successUrl?: string;
  cancelUrl?: string;
}

/**
 * Erstelle Stripe Checkout Session
 */
export async function createCheckoutSession(params: CheckoutSessionParams): Promise<{ sessionId: string; checkoutUrl: string }> {
  try {
    // Form-Data erstellen (Backend erwartet Form-Data)
    const formData = new FormData();
    formData.append('user_email', params.customerEmail || '');
    formData.append('tier', params.planName.toUpperCase());
    formData.append('success_url', params.successUrl || `${window.location.origin}/konto?session_id={CHECKOUT_SESSION_ID}`);
    formData.append('cancel_url', params.cancelUrl || `${window.location.origin}/#pricing`);
    if (params.userId) {
      formData.append('user_id', params.userId);
    }

    const response = await fetch('https://domulex-backend-lytuxcyyka-ey.a.run.app/stripe/create-checkout-session', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create checkout session');
    }

    const data = await response.json();
    return { 
      sessionId: data.session_id,
      checkoutUrl: data.checkout_url 
    };
  } catch (error) {
    console.error('Checkout session error:', error);
    throw error;
  }
}

/**
 * Redirect zu Stripe Checkout
 */
export async function redirectToCheckout(params: CheckoutSessionParams): Promise<void> {
  try {
    const { checkoutUrl } = await createCheckoutSession(params);
    
    // Direkt zur Checkout URL redirecten (Stripe hostet die Seite)
    window.location.href = checkoutUrl;
  } catch (error) {
    console.error('Redirect to checkout error:', error);
    throw error;
  }
}

/**
 * Erstelle Customer Portal Session (für Abo-Verwaltung)
 */
export async function createPortalSession(customerId: string): Promise<{ url: string }> {
  try {
    const formData = new FormData();
    formData.append('customer_id', customerId);
    formData.append('return_url', `${window.location.origin}/konto`);

    const response = await fetch('https://domulex-backend-lytuxcyyka-ey.a.run.app/stripe/create-portal-session', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create portal session');
    }

    const data = await response.json();
    return { url: data.portal_url };
  } catch (error) {
    console.error('Portal session error:', error);
    throw error;
  }
}

// Plan Price IDs (aus ENV oder hardcoded)
export const STRIPE_PRICES = {
  mieter_plus: process.env.NEXT_PUBLIC_STRIPE_PRICE_MIETER_PLUS || 'price_mieter_plus',
  professional: process.env.NEXT_PUBLIC_STRIPE_PRICE_PROFESSIONAL || 'price_professional',
  lawyer: process.env.NEXT_PUBLIC_STRIPE_PRICE_LAWYER || 'price_lawyer',
};
