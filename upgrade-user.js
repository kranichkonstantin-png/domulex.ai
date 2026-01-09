const admin = require('firebase-admin');

// Initialize Firebase Admin with Application Default Credentials
admin.initializeApp({
  projectId: 'domulex-ai'
});

const db = admin.firestore();

async function upgradeFreeUser() {
  const userEmail = 'kranichkonstantin@gmail.com';
  
  try {
    // Find user by email
    const usersRef = db.collection('users');
    const snapshot = await usersRef.where('email', '==', userEmail).get();
    
    if (snapshot.empty) {
      console.log('❌ User nicht gefunden:', userEmail);
      process.exit(1);
    }
    
    const userDoc = snapshot.docs[0];
    const userId = userDoc.id;
    
    console.log('📋 Gefundener User:');
    console.log('   UID:', userId);
    console.log('   Aktueller Status:', userDoc.data());
    
    // Upgrade to Lawyer Pro
    const updateData = {
      plan: 'lawyer',
      tier: 'lawyer',
      queriesLimit: 999999, // Unbegrenzt
      queriesUsed: 0, // Reset
      subscriptionStatus: 'active',
      updatedAt: new Date().toISOString(),
      note: 'Manuell upgraded zu Lawyer Pro für Testing'
    };
    
    await usersRef.doc(userId).update(updateData);
    
    console.log('');
    console.log('✅ User erfolgreich upgraded:');
    console.log('   Email:', userEmail);
    console.log('   Neuer Plan: Lawyer Pro');
    console.log('   Neues Limit: Unbegrenzt (999999)');
    
  } catch (error) {
    console.error('❌ Fehler:', error);
  }
  
  process.exit(0);
}

upgradeFreeUser();
