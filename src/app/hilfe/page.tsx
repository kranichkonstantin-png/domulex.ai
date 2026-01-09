'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import PremiumHeader from '@/components/PremiumHeader';
import PremiumFooter from '@/components/PremiumFooter';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface FAQ {
  question: string;
  answer: string;
  keywords: string[];
}

// Häufig gestellte Fragen - KI-Agent beantwortet diese automatisch
const FAQ_DATABASE: FAQ[] = [
  // === ALLGEMEIN (Öffentlich) ===
  {
    question: "Was bietet domulex.ai?",
    answer: "domulex.ai ist Ihre KI-Plattform für deutsches Immobilienrecht. Wir analysieren Ihren individuellen Fall basierend auf über 50.000 Rechtsdokumenten zu Mietrecht, WEG-Recht, Baurecht, Maklerrecht und Immobiliensteuerrecht.",
    keywords: ["was ist domulex", "funktionen", "features", "was bietet", "was kann", "übersicht"]
  },
  {
    question: "Welche Tarife gibt es?",
    answer: "Wir bieten drei Tarife:\n\n• **Basis** (19€/Monat): 50 Anfragen, Mietrecht & WEG-Recht, Steuer-Basics, eigene Vorlagen erstellen\n• **Professional** (39€/Monat): 250 Anfragen, Vertragsanalyse, Renditerechner, Baurecht\n• **Lawyer Pro** (69€/Monat): Unbegrenzt, Mandanten-CRM, Fallanalyse, Rechtsprechungsanalyse\n\nNach der Registrierung erhalten Sie 3 kostenlose Test-Anfragen.",
    keywords: ["tarif", "preis", "kosten", "wieviel", "euro", "€", "preise"]
  },
  {
    question: "Wie kann ich mich registrieren?",
    answer: "Klicken Sie auf 'Kostenlos starten' auf unserer Startseite. Sie können sich mit E-Mail und Passwort registrieren. Nach der Registrierung erhalten Sie sofort 3 kostenlose Anfragen zum Testen.",
    keywords: ["registrieren", "anmelden", "account", "konto erstellen", "starten"]
  },
  {
    question: "Kann domulex.ai bei Steuerfragen helfen?",
    answer: "Ja! Unsere Datenbank enthält über 100 BFH-Urteile und BMF-Schreiben zum Immobiliensteuerrecht:\n\n• AfA-Berechnung (2%, 2.5%, 3%)\n• Spekulationsfrist (10 Jahre)\n• Grunderwerbsteuer (3.5-6.5% je nach Bundesland)\n• Werbungskosten bei Vermietung",
    keywords: ["steuer", "afa", "abschreibung", "spekulationsfrist", "grunderwerbsteuer", "werbungskosten", "finanzamt"]
  },
  {
    question: "Wie aktuell sind die Rechtsinformationen?",
    answer: "Unsere Rechtsdatenbank enthält:\n\n• **Gesetze:** Aktuelle Fassungen\n• **BGH-Urteile:** Laufend aktualisiert\n• **BFH-Entscheidungen:** Laufend ergänzt\n• **BMF-Schreiben:** Aktuelle Verwaltungsanweisungen\n\nDas Quelldatum wird bei jeder Antwort angezeigt.",
    keywords: ["aktuell", "aktualisierung", "update", "neu", "stand", "datum"]
  },
  {
    question: "Wie werden meine Daten geschützt?",
    answer: "Datenschutz hat für uns höchste Priorität:\n\n• **DSGVO-konform** - Serverstandort Deutschland\n• **Zero Data Retention** - Chat-Inhalte werden nicht dauerhaft gespeichert\n• **SSL-Verschlüsselung** - Alle Daten verschlüsselt übertragen\n• **Keine Weitergabe** an Dritte",
    keywords: ["datenschutz", "dsgvo", "daten", "sicherheit", "verschlüsselung", "privacy"]
  },
  {
    question: "Welche Zahlungsmethoden werden akzeptiert?",
    answer: "Wir akzeptieren:\n\n• **Kreditkarten:** Visa, Mastercard, American Express\n• **SEPA-Lastschrift**\n\nDie Zahlung wird sicher über unseren Partner Stripe abgewickelt.",
    keywords: ["zahlung", "bezahlen", "kreditkarte", "sepa", "lastschrift", "zahlungsmethode", "rechnung"]
  },
  {
    question: "Kann ich jederzeit kündigen?",
    answer: "Ja! Alle Abonnements sind monatlich kündbar. Sie haben 14 Tage Widerrufsrecht ab Vertragsabschluss – auch als gewerblicher Kunde. Die Kündigung wird zum Ende der aktuellen Abrechnungsperiode wirksam.",
    keywords: ["kündigen", "abo", "abonnement", "beenden", "stornieren", "widerruf"]
  },
  {
    question: "Funktioniert domulex.ai auch für Österreich oder die Schweiz?",
    answer: "Aktuell konzentriert sich domulex.ai auf **deutsches Immobilienrecht** (BGB, WEG, BauGB etc.). Österreichisches und Schweizer Recht sind derzeit nicht enthalten. Wir arbeiten an einer Erweiterung für DACH.",
    keywords: ["österreich", "schweiz", "international", "ausland", "welches recht"]
  },
  {
    question: "Gibt es eine App?",
    answer: "domulex.ai funktioniert vollständig im Browser auf allen Geräten (Desktop, Tablet, Smartphone). Eine native App ist aktuell nicht verfügbar, aber die Website ist mobil-optimiert.",
    keywords: ["app", "handy", "smartphone", "mobil", "tablet", "ios", "android"]
  },
  {
    question: "Wie kann ich den Support kontaktieren?",
    answer: "Sie erreichen uns per E-Mail:\n\n• **Allgemein:** kontakt@domulex.ai\n• **Technisch:** support@domulex.ai\n• **Datenschutz:** datenschutz@domulex.ai\n\nWir antworten in der Regel innerhalb von 24 Stunden.",
    keywords: ["support", "kontakt", "hilfe", "email", "erreichen", "problem"]
  }
];

// Einfacher KI-Agent für Support-Anfragen
function findAnswer(userMessage: string): { answer: string; confidence: 'high' | 'medium' | 'low' } {
  const normalizedMessage = userMessage.toLowerCase();
  
  // Prüfe auf FAQ-Matches
  for (const faq of FAQ_DATABASE) {
    const matchingKeywords = faq.keywords.filter(keyword => 
      normalizedMessage.includes(keyword.toLowerCase())
    );
    
    if (matchingKeywords.length >= 1) {
      return { answer: faq.answer, confidence: 'high' };
    }
  }
  
  // Allgemeine Begrüßung
  if (normalizedMessage.match(/^(hallo|hi|hey|guten tag|moin)/)) {
    return {
      answer: "Hallo! Willkommen beim domulex.ai Support. Wie kann ich Ihnen helfen? Sie können mir Fragen zu Ihrem Konto, Abonnement, Zahlungen oder zur Nutzung der Plattform stellen.",
      confidence: 'high'
    };
  }
  
  // Danke-Antwort
  if (normalizedMessage.match(/(danke|vielen dank|super|toll|perfekt)/)) {
    return {
      answer: "Gern geschehen! Gibt es noch etwas, wobei ich Ihnen helfen kann?",
      confidence: 'high'
    };
  }
  
  // Preis/Kosten-Fragen
  if (normalizedMessage.match(/(preis|kosten|wieviel|was kostet|euro|€)/)) {
    return {
      answer: "Unsere Preise finden Sie auf der Startseite unter 'Preise'. Wir bieten einen kostenlosen Test-Tarif (3 Anfragen) sowie Basis (19€/Monat mit eigenen Vorlagen), Professional (39€/Monat mit Vertragsanalyse) und Lawyer Pro (69€/Monat mit Fallanalyse & Rechtsprechungsanalyse). Nach 6 Monaten ohne Upgrade wird das Test-Konto automatisch gelöscht.",
      confidence: 'medium'
    };
  }
  
  // Technische Probleme
  if (normalizedMessage.match(/(fehler|problem|funktioniert nicht|bug|geht nicht|lädt nicht)/)) {
    return {
      answer: "Es tut mir leid, dass Sie auf ein Problem stoßen. Könnten Sie mir bitte mehr Details geben? Welcher Fehler tritt auf und auf welcher Seite? Haben Sie versucht, die Seite neu zu laden oder einen anderen Browser zu verwenden?",
      confidence: 'medium'
    };
  }
  
  // Keine passende Antwort gefunden
  return {
    answer: "",
    confidence: 'low'
  };
}

export default function HilfePage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hallo! 👋 Ich bin der domulex.ai Support-Assistent. Ich helfe Ihnen gerne bei Fragen zu Ihrem Konto, Abonnement, Zahlungen oder zur Nutzung der Plattform.\n\n**Tipp:** Falls ich Ihre Frage nicht beantworten kann, können Sie jederzeit auf "Mitarbeiter kontaktieren" klicken.',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showContactForm, setShowContactForm] = useState(false);
  const [contactEmail, setContactEmail] = useState('');
  const [contactMessage, setContactMessage] = useState('');
  const [contactName, setContactName] = useState('');
  const [contactSent, setContactSent] = useState(false);
  const [sendingContact, setSendingContact] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Auto-Scroll zur User-Frage wenn neue Antwort kommt
  const scrollToNewMessage = () => {
    if (messagesContainerRef.current && messages.length >= 2) {
      const container = messagesContainerRef.current;
      const userMessage = container.querySelector('[data-user-message="true"]');
      if (userMessage) {
        const rect = userMessage.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        const scrollOffset = rect.top - containerRect.top + container.scrollTop - 80;
        container.scrollTo({ top: scrollOffset, behavior: 'smooth' });
      }
    }
  };
  
  useEffect(() => {
    const timer = setTimeout(() => {
      scrollToNewMessage();
    }, 100);
    return () => clearTimeout(timer);
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Simuliere KI-Verarbeitungszeit
    await new Promise(resolve => setTimeout(resolve, 800));

    const { answer, confidence } = findAnswer(inputValue);

    let assistantContent = '';

    if (confidence === 'high') {
      assistantContent = answer;
    } else if (confidence === 'medium') {
      assistantContent = answer;
    } else {
      // Keine passende Antwort - an Support weiterleiten
      assistantContent = `Ich konnte leider keine passende Antwort auf Ihre Frage finden. 

Damit wir Ihnen bestmöglich helfen können, leite ich Ihre Anfrage an unser Support-Team weiter. Ein Mitarbeiter wird sich zeitnah bei Ihnen melden.

**Möchten Sie uns eine Nachricht hinterlassen?** Klicken Sie auf den Button unten, um das Kontaktformular zu öffnen.`;
      setShowContactForm(true);
    }

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: assistantContent,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, assistantMessage]);
    setIsLoading(false);
  };

  const handleContactSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!contactEmail || !contactMessage) return;

    setSendingContact(true);

    try {
      // Sende Support-Anfrage an Backend, welches E-Mail versendet
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';
      
      // Chat-Verlauf für Kontext sammeln
      const chatHistory = messages
        .filter(m => m.role !== 'system')
        .map(m => `[${m.role === 'user' ? 'Kunde' : 'KI'}] ${m.content}`)
        .join('\n\n');
      
      const response = await fetch(`${backendUrl}/support/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: contactEmail,
          name: contactName || 'Nicht angegeben',
          message: contactMessage,
          chat_history: chatHistory,
        }),
      });

      if (response.ok) {
        setContactSent(true);
        
        const systemMessage: Message = {
          id: Date.now().toString(),
          role: 'system',
          content: `✅ **Ihre Nachricht wurde erfolgreich übermittelt!**

Unser Support-Team wird sich schnellstmöglich bei Ihnen unter ${contactEmail} melden. In der Regel antworten wir innerhalb von 24 Stunden.

Vielen Dank für Ihre Geduld!`,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, systemMessage]);
        setShowContactForm(false);
        setContactEmail('');
        setContactName('');
        setContactMessage('');
      } else {
        const errorData = await response.json();
        alert('Fehler beim Senden: ' + (errorData.detail || 'Bitte versuchen Sie es später erneut oder schreiben Sie direkt an support@domulex.ai'));
      }
    } catch (error) {
      console.error('Contact form error:', error);
      alert('Netzwerkfehler. Bitte versuchen Sie es später erneut oder schreiben Sie direkt an support@domulex.ai');
    }

    setSendingContact(false);
  };

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      <PremiumHeader />

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 pt-32 pb-12">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          
          {/* Chat Header */}
          <div className="bg-[#1e3a5f]/5 p-4 border-b border-gray-100">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-[#1e3a5f] rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-lg font-semibold text-[#1e3a5f]">Hilfe</h1>
                <p className="text-sm text-gray-500">KI-Assistent • Typischerweise sofortige Antwort</p>
              </div>
            </div>
          </div>

          {/* Chat Messages */}
          <div ref={messagesContainerRef} className="h-[400px] overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((message, index) => (
              <div
                key={message.id}
                data-user-message={message.role === 'user' && index === messages.length - 2 ? "true" : undefined}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-[#1e3a5f] text-white'
                      : message.role === 'system'
                      ? 'bg-green-50 border border-green-200 text-green-800'
                      : 'bg-white border border-gray-200 text-gray-700'
                  }`}
                >
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content.split('\n').map((line, i) => (
                      <p key={i} className={i > 0 ? 'mt-2' : ''}>
                        {line.startsWith('**') && line.endsWith('**') 
                          ? <strong>{line.replace(/\*\*/g, '')}</strong>
                          : line}
                      </p>
                    ))}
                  </div>
                  <div className={`text-xs mt-2 ${
                    message.role === 'user' ? 'text-blue-200' : 'text-gray-400'
                  }`}>
                    {message.timestamp.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </div>

          {/* Contact Form (wenn angezeigt) */}
          {showContactForm && !contactSent && (
            <div className="p-4 border-t border-gray-100 bg-blue-50">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg">👤</span>
                <h3 className="font-medium text-[#1e3a5f]">Mitarbeiter kontaktieren</h3>
              </div>
              <form onSubmit={handleContactSubmit} className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Ihr Name
                    </label>
                    <input
                      type="text"
                      value={contactName}
                      onChange={(e) => setContactName(e.target.value)}
                      placeholder="Max Mustermann"
                      className="w-full px-4 py-2 bg-white border border-gray-200 rounded-lg text-gray-800 placeholder-gray-400 focus:outline-none focus:border-[#1e3a5f]"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Ihre E-Mail-Adresse *
                    </label>
                    <input
                      type="email"
                      value={contactEmail}
                      onChange={(e) => setContactEmail(e.target.value)}
                      placeholder="ihre@email.de"
                      className="w-full px-4 py-2 bg-white border border-gray-200 rounded-lg text-gray-800 placeholder-gray-400 focus:outline-none focus:border-[#1e3a5f]"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Ihre Nachricht an unser Team *
                  </label>
                  <textarea
                    value={contactMessage}
                    onChange={(e) => setContactMessage(e.target.value)}
                    placeholder="Beschreiben Sie Ihr Anliegen..."
                    rows={3}
                    className="w-full px-4 py-2 bg-white border border-gray-200 rounded-lg text-gray-800 placeholder-gray-400 focus:outline-none focus:border-[#1e3a5f] resize-none"
                    required
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    type="submit"
                    disabled={sendingContact}
                    className="flex-1 py-2 bg-[#1e3a5f] hover:bg-[#2d4a6f] disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors"
                  >
                    {sendingContact ? '⏳ Wird gesendet...' : '📧 Nachricht senden'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowContactForm(false)}
                    className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
                  >
                    Abbrechen
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Chat Input */}
          <div className="p-4 border-t border-gray-100">
            <form 
              onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}
              className="flex gap-2"
            >
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ihre Frage eingeben..."
                className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:border-[#1e3a5f]"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="px-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-xl font-medium transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </form>
            
            {/* Mitarbeiter kontaktieren Button - immer sichtbar */}
            {!showContactForm && (
              <button
                onClick={() => setShowContactForm(true)}
                className="mt-3 w-full py-2 text-sm text-gray-600 hover:text-[#1e3a5f] border border-gray-200 hover:border-[#1e3a5f] rounded-lg transition-colors flex items-center justify-center gap-2"
              >
                👤 Mitarbeiter kontaktieren
              </button>
            )}
          </div>
        </div>

        {/* Quick FAQ Buttons */}
        <div className="mt-8 bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-[#1e3a5f]">Häufige Themen</h2>
            <Link href="/faq" className="text-sm text-[#b8860b] hover:text-[#9a7209]">
              Alle FAQs anzeigen →
            </Link>
          </div>
          <div className="grid gap-3">
            {FAQ_DATABASE.slice(0, 6).map((faq, index) => (
              <button
                key={index}
                onClick={() => {
                  setInputValue(faq.question);
                }}
                className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-gray-600 hover:text-[#1e3a5f] transition-colors"
              >
                {faq.question}
              </button>
            ))}
          </div>
        </div>

        {/* Kontakt Info */}
        <div className="mt-8 grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-[#1e3a5f] mb-2">📧 E-Mail Support</h3>
            <p className="text-gray-500 text-sm mb-3">Für komplexere Anfragen</p>
            <a href="mailto:support@domulex.ai" className="text-[#b8860b] hover:text-[#9a7209]">
              support@domulex.ai
            </a>
          </div>
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-[#1e3a5f] mb-2">📚 FAQ</h3>
            <p className="text-gray-500 text-sm mb-3">Alle häufigen Fragen</p>
            <Link href="/faq" className="text-[#b8860b] hover:text-[#9a7209]">
              Zu den FAQs →
            </Link>
          </div>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
