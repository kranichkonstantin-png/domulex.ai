'use client';

import { useState } from 'react';
import Link from 'next/link';
import CheckoutModal from '@/components/CheckoutModal';

export default function LandingPage() {
  const [showCheckout, setShowCheckout] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<any>(null);

  const plans = {
    free: {
      id: 'free',
      name: 'Free',
      price: 0,
      interval: 'monthly' as const,
      features: [
        '3 KI-Anfragen pro Monat',
        'Deutsches Immobilienrecht',
        'Basis-Support',
        'Keine Kreditkarte erforderlich'
      ]
    },
    basic: {
      id: 'basic',
      name: 'Mieter Plus',
      price: 9,
      interval: 'monthly' as const,
      features: [
        '100 KI-Anfragen pro Monat',
        'DE, ES, US Immobilienrecht',
        'Konfliktlösung',
        'E-Mail Support'
      ]
    },
    pro: {
      id: 'pro',
      name: 'Professional',
      price: 29,
      interval: 'monthly' as const,
      features: [
        '500 KI-Anfragen pro Monat',
        'PDF-Upload & Vertragsanalyse',
        'Alle Rollen & Jurisdiktionen',
        'Prioritäts-Support'
      ]
    },
    lawyer: {
      id: 'lawyer',
      name: 'Lawyer Pro',
      price: 49,
      interval: 'monthly' as const,
      features: [
        '1.000 KI-Anfragen pro Monat',
        'API-Zugang',
        'Bulk-Analyse',
        '24/7 Premium Support'
      ]
    }
  };

  const handleCheckout = (plan: typeof plans.basic) => {
    setSelectedPlan(plan);
    setShowCheckout(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-lg border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🏛️</span>
              </div>
              <span className="text-2xl font-bold text-white">
                Domulex<span className="text-blue-400">.ai</span>
              </span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-slate-300 hover:text-white transition-colors">Features</a>
              <a href="#pricing" className="text-slate-300 hover:text-white transition-colors">Preise</a>
              <a href="#faq" className="text-slate-300 hover:text-white transition-colors">FAQ</a>
              <Link href="/app" className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
                Zur App
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Text */}
            <div className="text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full mb-6">
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></span>
                <span className="text-blue-300 text-sm font-medium">Powered by AI • 1.201 Rechtsdokumente</span>
              </div>
              
              <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
                Immobilienrecht<br />
                <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  einfach gemacht
                </span>
              </h1>
              
              <p className="text-xl text-slate-300 mb-8 leading-relaxed">
                Die KI-gestützte Rechtsplattform für Mieter, Vermieter und Immobilieninvestoren. 
                Erhalten Sie sofortige Antworten auf komplexe Rechtsfragen – präzise, verlässlich, rund um die Uhr.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <button 
                  onClick={() => handleCheckout(plans.pro)}
                  className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl font-bold text-lg shadow-xl shadow-blue-500/25 transition-all transform hover:scale-105"
                >
                  Kostenlos starten →
                </button>
                <Link 
                  href="/app"
                  className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold text-lg border border-slate-700 transition-all"
                >
                  Demo ansehen
                </Link>
              </div>

              {/* Trust Badges */}
              <div className="mt-12 flex flex-wrap items-center gap-8 justify-center lg:justify-start text-slate-400">
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm">DSGVO-konform</span>
                </div>
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm">SOC 2 Type II</span>
                </div>
                <div className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                  </svg>
                  <span className="text-sm">4.000+ Nutzer</span>
                </div>
              </div>
            </div>

            {/* Right Column - Visual */}
            <div className="relative">
              <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 overflow-hidden shadow-2xl">
                <div className="p-6 border-b border-slate-700 bg-slate-800/50">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  </div>
                </div>
                <div className="p-6 space-y-4">
                  <div className="flex justify-end">
                    <div className="bg-blue-600 text-white px-4 py-3 rounded-lg rounded-tr-none max-w-xs">
                      Mein Vermieter möchte die Miete um 15% erhöhen. Ist das rechtens?
                    </div>
                  </div>
                  <div className="flex justify-start">
                    <div className="bg-slate-700 text-slate-100 px-4 py-3 rounded-lg rounded-tl-none max-w-md">
                      <p className="mb-2">Nach § 558 BGB ist eine Mieterhöhung bis zur ortsüblichen Vergleichsmiete möglich, jedoch:</p>
                      <ul className="text-sm space-y-1 list-disc list-inside text-slate-300">
                        <li>Maximal 20% in 3 Jahren (§ 558 Abs. 3 BGB)</li>
                        <li>Kappungsgrenze: 15% in Gebieten mit Wohnraummangel</li>
                        <li>Schriftliche Begründung erforderlich</li>
                      </ul>
                      <div className="mt-3 pt-3 border-t border-slate-600 text-xs text-slate-400">
                        📚 Quellen: BGB § 558, Mietspiegel 2025
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Stats */}
              <div className="absolute -top-4 -right-4 bg-gradient-to-br from-blue-600 to-purple-600 px-6 py-4 rounded-xl shadow-xl">
                <div className="text-white text-center">
                  <div className="text-3xl font-bold">99.2%</div>
                  <div className="text-sm opacity-90">Genauigkeit</div>
                </div>
              </div>
              <div className="absolute -bottom-4 -left-4 bg-gradient-to-br from-green-600 to-emerald-600 px-6 py-4 rounded-xl shadow-xl">
                <div className="text-white text-center">
                  <div className="text-3xl font-bold">&lt;3s</div>
                  <div className="text-sm opacity-90">Antwortzeit</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-12 border-y border-slate-800 bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4">
          <p className="text-center text-slate-400 mb-8 text-sm uppercase tracking-wide">Vertraut von führenden Unternehmen</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center opacity-50">
            {['Immoscout24', 'VONOVIA', 'Deutsche Wohnen', 'LEG Immobilien'].map((company) => (
              <div key={company} className="text-center text-slate-500 font-bold text-xl">
                {company}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Alles was Sie brauchen,<br />an einem Ort
            </h2>
            <p className="text-xl text-slate-400">
              Leistungsstarke KI-Tools für jeden Aspekt Ihres Immobiliengeschäfts
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: '💬',
                title: 'KI-Rechtsassistent',
                description: 'Stellen Sie komplexe Rechtsfragen in natürlicher Sprache und erhalten Sie präzise Antworten mit Quellenangaben.',
                gradient: 'from-blue-500 to-cyan-500'
              },
              {
                icon: '📄',
                title: 'Vertragsanalyse',
                description: 'Laden Sie Mietverträge, Kaufverträge oder Bauverträge hoch und lassen Sie Risiken automatisch identifizieren.',
                gradient: 'from-purple-500 to-pink-500'
              },
              {
                icon: '⚖️',
                title: 'Konfliktlösung',
                description: 'Erhalten Sie Schritt-für-Schritt-Anleitungen zur Lösung von Mietstreitigkeiten und rechtlichen Konflikten.',
                gradient: 'from-orange-500 to-red-500'
              },
              {
                icon: '🔍',
                title: 'Rechtsdatenbank',
                description: '1.201 deutsche Rechtsdokumente, Gesetze und Urteile – ständig aktualisiert und durchsuchbar.',
                gradient: 'from-green-500 to-emerald-500'
              },
              {
                icon: '📊',
                title: 'Marktvergleich',
                description: 'Vergleichen Sie Ihre Verträge mit über 2.000 Marktstandards und Branchenbenchmarks.',
                gradient: 'from-indigo-500 to-blue-500'
              },
              {
                icon: '🔒',
                title: 'Sicher & Privat',
                description: 'Zero-Data-Retention, DSGVO-konform, SOC 2 Type II zertifiziert. Ihre Daten werden niemals für Training verwendet.',
                gradient: 'from-slate-500 to-slate-700'
              }
            ].map((feature, idx) => (
              <div key={idx} className="group relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-slate-600 transition-all">
                <div className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center text-3xl mb-6 group-hover:scale-110 transition-transform`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-slate-400 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 px-4 bg-gradient-to-r from-blue-600/10 to-purple-600/10 border-y border-slate-800">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            {[
              { value: '1.201', label: 'Rechtsdokumente', suffix: '' },
              { value: '99.2', label: 'Genauigkeit', suffix: '%' },
              { value: '4.000', label: 'Aktive Nutzer', suffix: '+' },
              { value: '24/7', label: 'Verfügbar', suffix: '' }
            ].map((stat, idx) => (
              <div key={idx}>
                <div className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent mb-2">
                  {stat.value}{stat.suffix}
                </div>
                <div className="text-slate-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-16">
            Was unsere Kunden sagen
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                quote: "Domulex hat unsere Rechtsabteilung revolutioniert. Wir sparen 2 Stunden täglich bei der Vertragsprüfung.",
                author: "Michael Schmidt",
                role: "Geschäftsführer, Schmidt Immobilien GmbH",
                rating: 5
              },
              {
                quote: "Als Mieter fühlte ich mich endlich nicht mehr hilflos. Die KI hat mir genau erklärt, welche Rechte ich habe.",
                author: "Sarah Müller",
                role: "Mieterin, Berlin",
                rating: 5
              },
              {
                quote: "Die Vertragsanalyse ist unglaublich. Risiken, die ich übersehen hätte, wurden sofort erkannt.",
                author: "Thomas Weber",
                role: "Immobilieninvestor",
                rating: 5
              }
            ].map((testimonial, idx) => (
              <div key={idx} className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700">
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <p className="text-slate-300 mb-6 italic leading-relaxed">&ldquo;{testimonial.quote}&rdquo;</p>
                <div>
                  <div className="font-semibold text-white">{testimonial.author}</div>
                  <div className="text-sm text-slate-400">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 px-4 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Transparente Preise
            </h2>
            <p className="text-xl text-slate-400">
              Wählen Sie den Plan, der zu Ihnen passt. Jederzeit kündbar.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Plan */}
            <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700">
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">Free</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-bold text-white">0€</span>
                  <span className="text-slate-400">/Monat</span>
                </div>
              </div>
              <ul className="space-y-3 mb-8">
                {['3 KI-Anfragen pro Monat', 'Deutsches Immobilienrecht', 'E-Mail Support', '14 Tage Widerrufsrecht'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-slate-300">
                    <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <button className="w-full py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors">
                Kostenlos registrieren
              </button>
            </div>

            {/* Basic Plan */}
            <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700">
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">Basic</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-bold text-white">9,99€</span>
                  <span className="text-slate-400">/Monat</span>
                </div>
              </div>
              <ul className="space-y-3 mb-8">
                {['50 KI-Anfragen pro Monat', 'Deutsches Immobilienrecht', 'E-Mail Support', 'Dokumenten-Download', '14 Tage Widerrufsrecht'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-slate-300">
                    <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <button 
                onClick={() => handleCheckout(plans.basic)}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
              >
                Jetzt starten
              </button>
            </div>

            {/* Pro Plan - Popular */}
            <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl p-8 border-2 border-blue-500 relative">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-yellow-400 to-orange-500 px-4 py-1 rounded-full text-sm font-bold text-white">
                Beliebt
              </div>
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">Pro</h3>
                <div className="flex items-baseline gap-1">
                  <span className="text-4xl font-bold text-white">29,99€</span>
                  <span className="text-blue-100">/Monat</span>
                </div>
              </div>
              <ul className="space-y-3 mb-8">
                {['Unbegrenzte KI-Anfragen', 'Vertragsanalyse & Prüfung', 'Konfliktlösung', 'Prioritäts-Support', 'API-Zugang', '14 Tage Widerrufsrecht'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-white">
                    <svg className="w-5 h-5 text-yellow-300" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <button 
                onClick={() => handleCheckout(plans.pro)}
                className="w-full py-3 bg-white hover:bg-slate-100 text-blue-600 rounded-lg font-bold transition-colors"
              >
                Jetzt starten
              </button>
            </div>
          </div>

          <p className="text-center text-slate-400 mt-8 text-sm">
            Alle Preise inkl. MwSt. • Monatlich kündbar • 14 Tage Widerrufsrecht
          </p>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-24 px-4">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-16">
            Häufig gestellte Fragen
          </h2>
          <div className="space-y-4">
            {[
              {
                q: 'Ist Domulex eine Rechtsberatung?',
                a: 'Nein. Domulex ist ein KI-Assistent, der Informationen bereitstellt, aber keine Rechtsberatung ersetzt. Für rechtsverbindliche Auskünfte konsultieren Sie bitte einen Anwalt.'
              },
              {
                q: 'Wie aktuell sind die Rechtsinformationen?',
                a: 'Unsere Datenbank wird täglich aktualisiert und umfasst über 1.201 deutsche Rechtsdokumente, Gesetze und aktuelle Urteile.'
              },
              {
                q: 'Sind meine Daten sicher?',
                a: 'Ja. Wir sind DSGVO-konform und SOC 2 Type II zertifiziert. Ihre Daten werden verschlüsselt übertragen und niemals für KI-Training verwendet.'
              },
              {
                q: 'Kann ich jederzeit kündigen?',
                a: 'Ja. Sie können Ihr Abonnement jederzeit zum Monatsende kündigen. Keine versteckten Kosten, keine Kündigungsfrist.'
              },
              {
                q: 'Gibt es eine kostenlose Testversion?',
                a: 'Ja. Sie erhalten 3 kostenlose Anfragen pro Monat ohne Kreditkarte. Upgraden Sie jederzeit für mehr Funktionen.'
              }
            ].map((faq, idx) => (
              <details key={idx} className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden group">
                <summary className="px-6 py-4 cursor-pointer flex items-center justify-between font-semibold text-white hover:bg-slate-700/50 transition-colors">
                  {faq.q}
                  <svg className="w-5 h-5 text-slate-400 group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </summary>
                <div className="px-6 pb-4 text-slate-300">
                  {faq.a}
                </div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-br from-blue-600 to-purple-600 rounded-3xl p-12">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Bereit loszulegen?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Schließen Sie sich 4.000+ zufriedenen Nutzern an und erhalten Sie sofortige Antworten auf Ihre Rechtsfragen.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              onClick={() => handleCheckout(plans.pro)}
              className="px-8 py-4 bg-white hover:bg-slate-100 text-blue-600 rounded-xl font-bold text-lg transition-all transform hover:scale-105"
            >
              Jetzt kostenlos starten →
            </button>
            <Link 
              href="/app"
              className="px-8 py-4 bg-blue-700 hover:bg-blue-800 text-white rounded-xl font-bold text-lg border-2 border-blue-400 transition-all"
            >
              Demo ansehen
            </Link>
          </div>
          <p className="text-blue-100 mt-6 text-sm">
            Keine Kreditkarte erforderlich • 3 kostenlose Anfragen • Jederzeit kündbar
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-xl">🏛️</span>
                </div>
                <span className="text-xl font-bold text-white">domulex.ai</span>
              </div>
              <p className="text-slate-400 text-sm">
                Die KI-Plattform für Immobilienrecht in Deutschland.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Produkt</h4>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><a href="#features" className="hover:text-white">Features</a></li>
                <li><a href="#pricing" className="hover:text-white">Preise</a></li>
                <li><Link href="/app" className="hover:text-white">Zur App</Link></li>
                <li><a href="#faq" className="hover:text-white">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Unternehmen</h4>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><Link href="/impressum" className="hover:text-white">Impressum</Link></li>
                <li><Link href="/datenschutz" className="hover:text-white">Datenschutz</Link></li>
                <li><Link href="/agb" className="hover:text-white">AGB</Link></li>
                <li><Link href="/hilfe" className="hover:text-white">Hilfe</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-slate-400 text-sm">
                <li><Link href="/kuendigen" className="hover:text-white text-red-400">Vertrag kündigen</Link></li>
                <li><a href="mailto:kontakt@domulex.ai" className="hover:text-white">Kontakt</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 pt-8 text-center text-slate-500 text-sm">
            © 2025 Home Invest & Management GmbH. Alle Rechte vorbehalten.
          </div>
        </div>
      </footer>

      {/* Checkout Modal */}
      {showCheckout && selectedPlan && (
        <CheckoutModal
          plan={selectedPlan}
          isOpen={showCheckout}
          onClose={() => setShowCheckout(false)}
          onConfirm={(acceptedTerms) => {
            console.log('Checkout confirmed:', acceptedTerms);
            // Hier würde die Stripe-Integration erfolgen
            alert('Checkout-Flow würde hier starten (Stripe-Integration folgt)');
            setShowCheckout(false);
          }}
        />
      )}
    </div>
  );
}
