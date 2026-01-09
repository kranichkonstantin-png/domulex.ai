const admin = require('firebase-admin');

// Initialize Firebase Admin
admin.initializeApp({
  credential: admin.credential.applicationDefault(),
  projectId: 'domulex-ai'
});

const db = admin.firestore();

async function setupAdmin() {
  const adminUid = 'Up9nWC381Sdf4TCMmubtiYtru4N2';
  const adminEmail = 'kontakt@domulex.ai';
  
  const adminData = {
    email: adminEmail,
    name: 'Konstantin Kranich',
    tier: 'lawyer', // Höchster Tier für Admin
    queriesUsed: 0,
    queriesLimit: 10000, // Unbegrenzt für Admin
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    role: 'admin' // Admin-Rolle
  };

  try {
    await db.collection('users').doc(adminUid).set(adminData);
    console.log('✅ Admin-Benutzer erfolgreich angelegt:');
    console.log('   UID:', adminUid);
    console.log('   Email:', adminEmail);
    console.log('   Tier:', adminData.tier);
    console.log('   Limit:', adminData.queriesLimit);
  } catch (error) {
    console.error('❌ Fehler beim Anlegen:', error);
  }
  
  process.exit(0);
}

setupAdmin();
