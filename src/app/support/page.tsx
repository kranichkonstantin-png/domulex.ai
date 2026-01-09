'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

// Redirect /support zu /hilfe für einheitliche Navigation
export default function SupportPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/hilfe');
  }, [router]);

  return (
    <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#1e3a5f] mx-auto mb-4"></div>
        <p className="text-gray-600">Weiterleitung zur Hilfe-Seite...</p>
      </div>
    </div>
  );
}
