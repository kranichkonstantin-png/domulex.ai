# Domulex.ai

A real estate AI platform built with Next.js and Firebase.

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript
- **Backend**: Firebase Cloud Functions (Python)
- **Database**: Firestore
- **Authentication**: Firebase Auth
- **Hosting**: Firebase Hosting
- **Styling**: Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+ 
- Firebase CLI
- Python 3.13+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kranichkonstantin-png/domulex.ai.git
cd domulex.ai
```

2. Install dependencies:
```bash
npm install
```

3. Set up Firebase configuration:
   - Copy `.env.local.example` to `.env.local`
   - Add your Firebase credentials from the Firebase Console

4. Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

## Firebase Setup

### Get Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/project/domulex-ai)
2. Navigate to Project Settings > General
3. Under "Your apps", select the web app or create one
4. Copy the configuration values to `.env.local`

### Deploy to Firebase

```bash
# Build the app
npm run build

# Deploy to Firebase Hosting
firebase deploy --only hosting

# Deploy Cloud Functions
firebase deploy --only functions
```

## Project Structure

```
domulex.ai/
├── src/
│   ├── app/              # Next.js App Router pages
│   ├── components/       # React components
│   ├── lib/              # Utility functions & Firebase config
│   └── firebase/         # Firebase SDK initialization
├── functions/            # Firebase Cloud Functions (Python)
├── public/               # Static assets
├── firestore.rules       # Firestore security rules
├── firestore.indexes.json # Firestore indexes
└── firebase.json         # Firebase configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `firebase emulators:start` - Start Firebase emulators locally
- `firebase deploy` - Deploy to Firebase

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
