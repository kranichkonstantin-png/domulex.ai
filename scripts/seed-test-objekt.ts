/**
 * Seed-Script: Erstellt ein Test-MFH mit 6 Mietparteien
 * 
 * Ausführen:
 * npx ts-node --project tsconfig.json scripts/seed-test-objekt.ts
 */

import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc, getDocs, query, where } from 'firebase/firestore';

// Firebase Config (aus .env oder direkt)
const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Test-Objekt: Mehrfamilienhaus mit 6 Parteien
const testObjekt = {
  adresse: 'Musterstraße 42',
  plz: '10115',
  ort: 'Berlin',
  gesamtflaeche: 480, // 6 Wohnungen à ca. 80m²
  gesamteinheiten: 6,
  baujahr: 1985,
  heizungstyp: 'gas',
  energieausweis: 'E',
  typ: 'mfh',
  notizen: 'Test-MFH für Nebenkostenabrechnung',
  mieter: [
    {
      id: 'mieter-1',
      name: 'Familie Müller',
      einheit: 'EG links',
      flaeche: 75,
      personenanzahl: 3,
      einzugsdatum: '2020-04-01',
      email: 'mueller@example.com',
      telefon: '030-12345671',
      vorauszahlung: 250
    },
    {
      id: 'mieter-2',
      name: 'Herr Schmidt',
      einheit: 'EG rechts',
      flaeche: 65,
      personenanzahl: 1,
      einzugsdatum: '2019-07-15',
      email: 'schmidt@example.com',
      telefon: '030-12345672',
      vorauszahlung: 180
    },
    {
      id: 'mieter-3',
      name: 'Frau Weber',
      einheit: '1. OG links',
      flaeche: 85,
      personenanzahl: 2,
      einzugsdatum: '2021-01-01',
      email: 'weber@example.com',
      telefon: '030-12345673',
      vorauszahlung: 280
    },
    {
      id: 'mieter-4',
      name: 'WG Hoffmann',
      einheit: '1. OG rechts',
      flaeche: 95,
      personenanzahl: 4,
      einzugsdatum: '2022-10-01',
      email: 'wg-hoffmann@example.com',
      telefon: '030-12345674',
      vorauszahlung: 320
    },
    {
      id: 'mieter-5',
      name: 'Familie Yilmaz',
      einheit: '2. OG links',
      flaeche: 80,
      personenanzahl: 4,
      einzugsdatum: '2018-03-01',
      email: 'yilmaz@example.com',
      telefon: '030-12345675',
      vorauszahlung: 270
    },
    {
      id: 'mieter-6',
      name: 'Dr. Braun',
      einheit: '2. OG rechts',
      flaeche: 80,
      personenanzahl: 2,
      einzugsdatum: '2023-06-01',
      email: 'braun@example.com',
      telefon: '030-12345676',
      vorauszahlung: 260
    }
  ],
  createdAt: new Date()
};

async function seedTestObjekt(userId: string) {
  console.log('🏢 Erstelle Test-MFH für User:', userId);
  
  try {
    const docRef = await addDoc(collection(db, 'users', userId, 'objekte'), testObjekt);
    console.log('✅ Test-Objekt erstellt mit ID:', docRef.id);
    console.log('');
    console.log('📋 Objektdaten:');
    console.log(`   Adresse: ${testObjekt.adresse}, ${testObjekt.plz} ${testObjekt.ort}`);
    console.log(`   Typ: Mehrfamilienhaus`);
    console.log(`   Gesamtfläche: ${testObjekt.gesamtflaeche} m²`);
    console.log(`   Einheiten: ${testObjekt.gesamteinheiten}`);
    console.log(`   Heizung: Erdgas`);
    console.log('');
    console.log('👥 Mieter:');
    testObjekt.mieter.forEach(m => {
      console.log(`   - ${m.name} (${m.einheit}): ${m.flaeche}m², ${m.personenanzahl} Personen, ${m.vorauszahlung}€/Monat`);
    });
    
    return docRef.id;
  } catch (error) {
    console.error('❌ Fehler:', error);
    throw error;
  }
}

// User-ID muss als Argument übergeben werden
const userId = process.argv[2];
if (!userId) {
  console.log('Usage: npx ts-node scripts/seed-test-objekt.ts <USER_ID>');
  console.log('');
  console.log('Die User-ID findest du in der Firebase Console unter Authentication.');
  process.exit(1);
}

seedTestObjekt(userId).then(() => {
  console.log('');
  console.log('🎉 Fertig! Öffne jetzt domulex.ai/app/objekte um das Objekt zu sehen.');
  process.exit(0);
}).catch(() => process.exit(1));
