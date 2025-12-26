# Domulex.ai - Copilot Instructions

## Project Overview
Domulex.ai is a real estate AI platform built with Next.js and Firebase.

## Tech Stack
- **Frontend**: Next.js 14 with TypeScript
- **Backend**: Firebase Cloud Functions
- **Database**: Firestore
- **Authentication**: Firebase Auth
- **Hosting**: Firebase Hosting
- **Styling**: Tailwind CSS

## Project Structure
```
domulex.ai/
├── src/
│   ├── app/              # Next.js App Router
│   ├── components/       # React components
│   ├── lib/              # Utility functions
│   └── firebase/         # Firebase configuration
├── functions/            # Firebase Cloud Functions
├── public/               # Static assets
└── firebase.json         # Firebase configuration
```

## Development Guidelines
- Use TypeScript for all code
- Follow Next.js App Router conventions
- Use Firebase SDK v9+ modular syntax
- Implement proper error handling
- Write clean, maintainable code

## Firebase Services
- Firestore for database operations
- Firebase Auth for user authentication
- Cloud Functions for serverless backend
- Firebase Hosting for deployment

## Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `firebase deploy` - Deploy to Firebase
- `firebase emulators:start` - Start local emulators
