'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Logo from '@/components/Logo';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

type DashboardType = 'basis' | 'professional' | 'lawyer';

// ============================================
// DASHBOARD-FUNKTIONEN WISSENSDATENBANK
// ============================================

interface Feature {
  name: string;
  description: string;
  howToUse: string;
  examples: string[];
  tips: string[];
  href: string;
}

const DASHBOARD_FEATURES: Record<DashboardType, Feature[]> = {
  basis: [
    {
      name: 'KI-Chat',
      description: 'Ihr persönlicher KI-Assistent für Fragen zum deutschen Immobilienrecht. Stellen Sie Fragen zu Mietrecht, WEG-Recht, Kündigungsschutz und mehr.',
      howToUse: 'Tippen Sie Ihre Frage in das Eingabefeld im Dashboard und drücken Sie Enter oder den Senden-Button. Die KI antwortet basierend auf über 50.000 Rechtsdokumenten.',
      examples: [
        'Was sind meine Rechte bei einer Mieterhöhung?',
        'Wie lange ist die Kündigungsfrist für meinen Mietvertrag?',
        'Welche Schönheitsreparaturen muss ich als Mieter durchführen?',
        'Was tun bei Schimmel in der Wohnung?'
      ],
      tips: [
        'Je konkreter Ihre Frage, desto besser die Antwort',
        'Wählen Sie Ihre Perspektive (Mieter/Eigentümer/Vermieter) für passendere Antworten',
        'Die Quellen werden unter jeder Antwort angezeigt'
      ],
      href: '/dashboard'
    },
    {
      name: 'KI-Steuer-Assistent',
      description: 'Erhalten Sie Antworten zu Immobilien-Steuerfragen: AfA, Werbungskosten, Spekulationsfrist und mehr.',
      howToUse: 'Stellen Sie Ihre Steuerfrage direkt im Chat. Der Assistent kennt BFH-Urteile, BMF-Schreiben und aktuelle Steuerregelungen.',
      examples: [
        'Wie berechne ich die AfA für meine vermietete Wohnung?',
        'Welche Werbungskosten kann ich als Vermieter absetzen?',
        'Wann endet die 10-Jahres-Spekulationsfrist?'
      ],
      tips: [
        'Unterscheiden Sie zwischen Anschaffungs- und Herstellungskosten',
        'Renovierungskosten können sofort oder über Jahre absetzbar sein',
        'Grunderwerbsteuer variiert je nach Bundesland (3,5-6,5%)'
      ],
      href: '/app?prompt=steuerliche%20Fragen'
    },
    {
      name: 'KI-Musterbriefe',
      description: 'Erstellen Sie rechtssichere Vorlagen für Mietminderung, Mängelanzeige, Kündigungswiderspruch und mehr.',
      howToUse: 'Öffnen Sie die Vorlagen-Seite und wählen Sie die gewünschte Vorlage. Füllen Sie die erforderlichen Felder aus und die KI generiert einen personalisierten Brief.',
      examples: [
        'Mängelanzeige bei defekter Heizung',
        'Widerspruch gegen Mieterhöhung',
        'Aufforderung zur Nebenkostenabrechnung'
      ],
      tips: [
        'Senden Sie wichtige Briefe per Einschreiben',
        'Setzen Sie angemessene Fristen (meist 14 Tage)',
        'Dokumentieren Sie Mängel mit Fotos und Datum'
      ],
      href: '/app/templates'
    },
    {
      name: 'Perspektive wechseln',
      description: 'Wählen Sie Ihre Rolle (Mieter, Eigentümer, Vermieter), damit die KI ihre Antworten an Ihre Perspektive anpasst.',
      howToUse: 'Klicken Sie im rechten Bereich unter "Ihre Perspektive" auf die gewünschte Rolle. Die aktive Rolle wird blau hervorgehoben.',
      examples: [
        'Als Mieter: Fokus auf Mieterrechte und Schutzvorschriften',
        'Als Eigentümer: WEG-Recht, Hausgeld, Eigentümerversammlungen',
        'Als Vermieter: Mieterhöhung, Kündigung, Vermieterpflichten'
      ],
      tips: [
        'Die Perspektive beeinflusst, welche Aspekte betont werden',
        'Sie können die Perspektive jederzeit wechseln',
        'Die Rechtsinfos bleiben objektiv, nur der Fokus ändert sich'
      ],
      href: '/dashboard'
    }
  ],
  professional: [
    {
      name: 'KI-Nebenkostenabrechnung erstellen',
      description: 'Erstellen Sie professionelle Nebenkostenabrechnungen für Ihre Mieter. Die KI hilft bei korrekter Verteilung und Formvorschriften.',
      howToUse: 'Öffnen Sie den Nebenkostenabrechnung-Generator. Geben Sie Objekt, Zeitraum, Gesamtkosten und Verteilerschlüssel ein. Die KI erstellt eine rechtskonforme Abrechnung.',
      examples: [
        'Jahresabrechnung für Mehrfamilienhaus mit 4 Parteien',
        'Heizkostenabrechnung mit 70/30 Verteilung',
        'Zwischenabrechnung bei Mieterwechsel'
      ],
      tips: [
        '12-Monats-Frist für Zustellung beachten',
        'Vorauszahlungen müssen klar erkennbar sein',
        'Grundsteuer nach Wohnfläche, Heizkosten mind. 50% nach Verbrauch'
      ],
      href: '/app/nebenkosten-abrechnung'
    },
    {
      name: 'KI-Renditerechner',
      description: 'Berechnen Sie die Rendite Ihrer Immobilieninvestments inklusive aller Kosten, Steuern und Finanzierung.',
      howToUse: 'Geben Sie Kaufpreis, Mieteinnahmen, Kaufnebenkosten und Finanzierungsdetails ein. Der Rechner zeigt Brutto- und Nettorendite, Cashflow und ROI.',
      examples: [
        'Rentabilität einer ETW zum Kauf prüfen',
        'Vergleich von 2 Anlageobjekten',
        'Einfluss der Zinsentwicklung auf die Rendite'
      ],
      tips: [
        'Bruttomietrendite = Jahresmiete / Kaufpreis',
        'Nettorendite berücksichtigt alle Kosten (Hausgeld, Instandhaltung, Leerstand)',
        'Leverage-Effekt bei Fremdfinanzierung beachten'
      ],
      href: '/app/calculators/rendite'
    },
    {
      name: 'KI-Vertragsanalyse',
      description: 'Analysieren Sie Miet- und Kaufverträge auf Risiken, unzulässige Klauseln und Optimierungspotenzial.',
      howToUse: 'Laden Sie Ihren Vertrag hoch oder kopieren Sie relevante Klauseln. Die KI prüft auf unwirksame Klauseln, fehlende Regelungen und Risiken.',
      examples: [
        'Prüfung von Schönheitsreparatur-Klauseln',
        'Analyse von Indexmietvereinbarungen',
        'Bewertung von Kaufvertrags-Entwürfen'
      ],
      tips: [
        'Unwirksame Klauseln können den gesamten Vertrag beeinflussen',
        'Standardformulare sind oft mieterfreundlicher als Individualverträge',
        'Bei Kaufverträgen: Notartermin erst nach Prüfung'
      ],
      href: '/app/contract-analysis'
    },
    {
      name: 'KI-Steuer-Optimierung',
      description: 'Optimieren Sie die Steuerlast Ihrer Immobilieninvestments durch AfA, Werbungskosten und steuerliche Gestaltung.',
      howToUse: 'Beschreiben Sie Ihre Immobiliensituation im Chat. Die KI zeigt Optimierungsmöglichkeiten basierend auf aktueller Rechtsprechung.',
      examples: [
        'AfA-Optimierung bei Denkmalimmobilien',
        'Steuerliche Behandlung von Modernisierungskosten',
        'Vermeidung der Spekulationssteuer'
      ],
      tips: [
        'Denkmal-AfA kann 100% der Sanierungskosten absetzbar machen',
        'Erhaltungsaufwand vs. Herstellungskosten unterscheiden',
        'Gewerblicher Grundstückshandel ab 4 Objekten in 5 Jahren'
      ],
      href: '/app?prompt=Steuer-Optimierung%20Immobilien'
    },
    {
      name: 'KI-Baurecht-Assistent',
      description: 'Hilfe bei Baumängeln, VOB-Fragen, Gewährleistung und Bauabnahme.',
      howToUse: 'Stellen Sie Ihre Baurecht-Frage im Chat. Der Assistent kennt BGB-Baurecht, VOB/B und aktuelle Rechtsprechung.',
      examples: [
        'Welche Gewährleistungsfristen gelten nach BGB?',
        'Wie dokumentiere ich Mängel bei der Bauabnahme?',
        'Was sind wesentliche Mängel?'
      ],
      tips: [
        'VOB/B gilt nur bei ausdrücklicher Vereinbarung',
        'Gewährleistung BGB: 5 Jahre, VOB: 4 Jahre',
        'Förmliche Abnahme schriftlich dokumentieren'
      ],
      href: '/app?prompt=Baurecht%20Baumängel'
    }
  ],
  lawyer: [
    {
      name: 'KI-Mandanten-CRM',
      description: 'Verwalten Sie Ihre Mandanten mit Kontaktdaten, Fallhistorie und Notizen. Schneller Zugriff auf alle relevanten Informationen.',
      howToUse: 'Öffnen Sie das CRM über die Werkzeugleiste. Legen Sie neue Mandanten an, ordnen Sie Fälle zu und pflegen Sie Notizen und Dokumente.',
      examples: [
        'Neuen Mandanten mit Kontaktdaten anlegen',
        'Fall mit Aktenzeichen und Fristen erstellen',
        'Schnellsuche nach Mandantenname'
      ],
      tips: [
        'Verknüpfen Sie Fälle mit Fristen für automatische Erinnerungen',
        'Nutzen Sie Tags für schnelle Filterung',
        'Exportieren Sie Mandantendaten für Ihre Kanzleisoftware'
      ],
      href: '/app/crm'
    },
    {
      name: 'KI-Fristenverwaltung',
      description: 'Überwachen Sie alle Fristen und Termine. Automatische Erinnerungen und Fristberechnung nach gesetzlichen Vorgaben.',
      howToUse: 'Tragen Sie Fristen mit Datum und Typ ein. Das System berechnet Vorfristen und sendet Erinnerungen per E-Mail oder Dashboard-Benachrichtigung.',
      examples: [
        'Berufungsfrist mit 1-Monat-Vorlauf',
        'Wiedereinsetzungsfrist automatisch berechnen',
        'Verhandlungstermin mit Mandantenerinnerung'
      ],
      tips: [
        'Unterscheiden Sie Notfristen von anderen Fristen',
        'Berücksichtigen Sie Feiertage und Wochenenden automatisch',
        'Setzen Sie mehrere Erinnerungen für wichtige Fristen'
      ],
      href: '/app/deadlines'
    },
    {
      name: 'KI-Schriftsatzgenerator',
      description: 'Erstellen Sie Klageschriften, Vertragsentwürfe, Mahnungen und Schriftsätze mit KI-Unterstützung.',
      howToUse: 'Wählen Sie den Dokumenttyp und geben Sie die Falldaten ein. Die KI generiert einen Entwurf basierend auf aktueller Rechtsprechung und Ihren Vorgaben.',
      examples: [
        'Klage auf Mietrückstand erstellen',
        'Räumungsklage mit Zahlungsverzug',
        'Anwaltsschreiben zur Abmahnung'
      ],
      tips: [
        'Prüfen Sie generierte Dokumente immer auf Mandantenbezug',
        'Passen Sie Formulierungen an Ihren Kanzleistil an',
        'Nutzen Sie die Vorlagen als Ausgangspunkt'
      ],
      href: '/app/templates'
    },
    {
      name: 'KI-Fallanalyse',
      description: 'Analysieren Sie Erfolgsaussichten, Risiken und strategische Optionen für Ihre Mandate.',
      howToUse: 'Beschreiben Sie den Sachverhalt und die Rechtsfrage. Die KI analysiert anhand von BGH-Urteilen und Fachliteratur.',
      examples: [
        'Erfolgsaussichten bei Mietminderungsklage',
        'Risikobewertung bei WEG-Beschlussanfechtung',
        'Strategieempfehlung bei Baumängelstreit'
      ],
      tips: [
        'Je detaillierter der Sachverhalt, desto präziser die Analyse',
        'Berücksichtigen Sie die Prozesskosten in der Strategie',
        'Vergleichsoptionen werden automatisch geprüft'
      ],
      href: '/app/fallanalyse'
    },
    {
      name: 'KI-Rechtsprechungsanalyse',
      description: 'Recherchieren Sie BGH-, OLG- und LG-Urteile zum Immobilienrecht. Finden Sie einschlägige Rechtsprechung für Ihren Fall.',
      howToUse: 'Geben Sie Stichwort, Aktenzeichen oder Rechtsfrage ein. Die KI findet relevante Urteile und zeigt Leitsätze und Fundstellen.',
      examples: [
        'Aktuelle BGH-Urteile zu Eigenbedarfskündigung',
        'Rechtsprechung zur Mietpreisbremse in Berlin',
        'OLG-Urteile zu WEG-Beschlussmängeln'
      ],
      tips: [
        'Kombinieren Sie Suche nach Rechtsbegriff und Sachverhalt',
        'Prüfen Sie, ob Urteile noch aktuell sind',
        'Nutzen Sie Fundstellen für Schriftsätze'
      ],
      href: '/app/rechtsprechung'
    },
    {
      name: 'KI-Dokumentenmanagement',
      description: 'Verwalten und durchsuchen Sie Ihre hochgeladenen Dokumente. Schnelle Volltextsuche und Kategorisierung.',
      howToUse: 'Laden Sie Dokumente hoch und versehen Sie sie mit Tags. Die Suche findet Inhalte auch in PDFs und Scans (OCR).',
      examples: [
        'Alle Mietverträge eines Mandanten finden',
        'Gerichtsbeschlüsse nach Datum filtern',
        'Volltext-Suche in Gutachten'
      ],
      tips: [
        'Einheitliche Benennung erleichtert die Suche',
        'Verknüpfen Sie Dokumente mit Mandanten und Fällen',
        'Nutzen Sie Tags wie "Dringend", "Entwurf", "Finalisiert"'
      ],
      href: '/app/documents'
    }
  ]
};

// Schnellstart-Anleitungen pro Dashboard-Typ
const QUICKSTART_GUIDES: Record<DashboardType, { title: string; steps: string[] }> = {
  basis: {
    title: 'Schnellstart für Basis-Nutzer',
    steps: [
      '👤 **Perspektive wählen**: Klicken Sie rechts auf Ihre Rolle (Mieter, Eigentümer oder Vermieter) – so passt die KI ihre Antworten an Ihre Situation an.',
      '💬 **Erste Frage stellen**: Tippen Sie Ihre Rechtsfrage in das Chat-Feld. Beispiel: "Was sind meine Rechte bei Schimmel in der Wohnung?"',
      '📚 **Quellen prüfen**: Unter jeder Antwort finden Sie die Rechtsquellen (§§, Urteile) – klicken Sie für Details.',
      '🔧 **Werkzeuge nutzen**: In der Seitenleiste finden Sie spezialisierte Tools wie Steuer-Assistent und Musterbriefe.',
      '✉️ **Vorlagen erstellen**: Mit "KI-Musterbriefe" erstellen Sie rechtssichere Schreiben an Vermieter oder Hausverwaltung.'
    ]
  },
  professional: {
    title: 'Schnellstart für Professional-Nutzer',
    steps: [
      '🏢 **Perspektive einstellen**: Wählen Sie Investor, Verwalter oder Vermieter für maßgeschneiderte Antworten.',
      '📊 **Rendite berechnen**: Nutzen Sie den KI-Renditerechner für Ihre Investmentanalyse.',
      '📄 **Verträge analysieren**: Laden Sie Miet- oder Kaufverträge zur Risikoprüfung hoch.',
      '💰 **Abrechnungen erstellen**: Der Nebenkostenabrechnung-Generator erstellt rechtskonforme Abrechnungen.',
      '⚖️ **Steuern optimieren**: Fragen Sie nach AfA, Werbungskosten und Spekulationsfristen für Ihre Objekte.'
    ]
  },
  lawyer: {
    title: 'Schnellstart für Juristen',
    steps: [
      '👥 **CRM einrichten**: Legen Sie Ihre ersten Mandanten und Fälle im Mandanten-CRM an.',
      '📅 **Fristen erfassen**: Tragen Sie wichtige Fristen ein – das System erinnert Sie automatisch.',
      '🔍 **Rechtsprechung recherchieren**: Nutzen Sie die Rechtsprechungsanalyse für BGH- und OLG-Urteile.',
      '📝 **Schriftsätze generieren**: Erstellen Sie Klageschriften und Mahnungen mit dem Schriftsatzgenerator.',
      '🎯 **Fälle analysieren**: Die KI-Fallanalyse bewertet Erfolgsaussichten und zeigt Risiken auf.'
    ]
  }
};

// KI-Antwortgenerierung
function generateAnswer(userMessage: string, dashboardType: DashboardType): string {
  const normalizedMessage = userMessage.toLowerCase();
  const features = DASHBOARD_FEATURES[dashboardType];
  const quickstart = QUICKSTART_GUIDES[dashboardType];
  
  // Begrüßung
  if (normalizedMessage.match(/^(hallo|hi|hey|guten tag|moin|servus)/)) {
    return `Hallo! 👋 Willkommen beim Schnellstart-Assistenten für Ihr ${dashboardType === 'basis' ? 'Basis' : dashboardType === 'professional' ? 'Professional' : 'Lawyer Pro'}-Dashboard.

Ich helfe Ihnen, alle Funktionen optimal zu nutzen. Fragen Sie mich zum Beispiel:
• "Wie starte ich?"
• "Was kann das Dashboard?"
• "Wie funktioniert [Funktion]?"

Oder wählen Sie unten eine Beispielfrage!`;
  }
  
  // Wie starte ich / Wie lege ich los
  if (normalizedMessage.match(/(wie starte|wie fange|wie lege ich los|erste schritte|anfangen|start|los)/)) {
    let response = `## ${quickstart.title}\n\n`;
    quickstart.steps.forEach((step, i) => {
      response += `${i + 1}. ${step}\n\n`;
    });
    response += `\n💡 **Tipp:** Fragen Sie mich zu einer konkreten Funktion für detaillierte Anleitungen!`;
    return response;
  }
  
  // Übersicht aller Funktionen
  if (normalizedMessage.match(/(was kann|funktionen|übersicht|features|alles|was gibt|möglichkeiten)/)) {
    let response = `## Ihre ${dashboardType === 'basis' ? 'Basis' : dashboardType === 'professional' ? 'Professional' : 'Lawyer Pro'}-Funktionen\n\n`;
    features.forEach(feature => {
      response += `### ${feature.name}\n${feature.description}\n\n`;
    });
    return response;
  }
  
  // Suche nach spezifischer Funktion
  for (const feature of features) {
    const featureKeywords = feature.name.toLowerCase().split(/[\s-]+/);
    if (featureKeywords.some(kw => normalizedMessage.includes(kw)) || 
        normalizedMessage.includes(feature.name.toLowerCase())) {
      let response = `## ${feature.name}\n\n`;
      response += `**Was ist das?**\n${feature.description}\n\n`;
      response += `**So nutzen Sie es:**\n${feature.howToUse}\n\n`;
      response += `**Beispiele:**\n`;
      feature.examples.forEach(ex => response += `• ${ex}\n`);
      response += `\n**Profi-Tipps:**\n`;
      feature.tips.forEach(tip => response += `• ${tip}\n`);
      response += `\n[→ Jetzt öffnen](${feature.href})`;
      return response;
    }
  }
  
  // Spezifische Themen
  if (normalizedMessage.match(/(nebenkosten|betriebskosten)/)) {
    const feature = features.find(f => f.name.toLowerCase().includes('nebenkosten'));
    if (feature) {
      return `## ${feature.name}\n\n${feature.description}\n\n**So geht's:** ${feature.howToUse}\n\n[→ Jetzt nutzen](${feature.href})`;
    }
  }
  
  if (normalizedMessage.match(/(steuer|afa|abschreibung|finanzamt)/)) {
    const feature = features.find(f => f.name.toLowerCase().includes('steuer'));
    if (feature) {
      return `## ${feature.name}\n\n${feature.description}\n\n**So geht's:** ${feature.howToUse}\n\n[→ Jetzt nutzen](${feature.href})`;
    }
  }
  
  if (normalizedMessage.match(/(vorlage|brief|muster|schreiben)/)) {
    const feature = features.find(f => f.name.toLowerCase().includes('vorlage') || f.name.toLowerCase().includes('muster') || f.name.toLowerCase().includes('schriftsatz'));
    if (feature) {
      return `## ${feature.name}\n\n${feature.description}\n\n**So geht's:** ${feature.howToUse}\n\n[→ Jetzt nutzen](${feature.href})`;
    }
  }
  
  if (normalizedMessage.match(/(vertrag|analyse|prüfen)/)) {
    const feature = features.find(f => f.name.toLowerCase().includes('vertrag'));
    if (feature) {
      return `## ${feature.name}\n\n${feature.description}\n\n**So geht's:** ${feature.howToUse}\n\n[→ Jetzt nutzen](${feature.href})`;
    }
  }
  
  if (normalizedMessage.match(/(chat|frage|ki|assistent)/)) {
    const feature = features.find(f => f.name.toLowerCase().includes('chat') || f.name.toLowerCase().includes('assistent'));
    if (feature) {
      return `## ${feature.name}\n\n${feature.description}\n\n**So geht's:** ${feature.howToUse}\n\n[→ Zurück zum Dashboard](/dashboard)`;
    }
  }
  
  if (normalizedMessage.match(/(perspektive|rolle|mieter|vermieter|eigentümer)/)) {
    return `## Perspektive wechseln

Die **Perspektive** beeinflusst, wie die KI Ihre Fragen beantwortet:

• **Mieter**: Fokus auf Mieterrechte, Kündigungsschutz, Mietminderung
• **Eigentümer**: WEG-Recht, Eigentümerversammlungen, Hausgeld
• **Vermieter**: Mieterhöhung, Kündigung, Vermieterpflichten

**So wechseln Sie:**
1. Schauen Sie im Dashboard auf den rechten Bereich "Ihre Perspektive"
2. Klicken Sie auf die gewünschte Rolle
3. Die aktive Rolle wird blau hervorgehoben

Die KI passt ihre Antworten automatisch an!`;
  }
  
  // Danke
  if (normalizedMessage.match(/(danke|vielen dank|super|toll|perfekt|klasse)/)) {
    return 'Gern geschehen! 🎉 Haben Sie noch eine Frage zu einer Funktion?';
  }
  
  // Fallback
  return `Ich bin Ihr Schnellstart-Assistent und kenne alle Funktionen Ihres Dashboards im Detail.

**Fragen Sie mich zum Beispiel:**
• "Wie starte ich?" – Schritt-für-Schritt Anleitung
• "Was kann das Dashboard?" – Übersicht aller Funktionen
• "Wie funktioniert der Steuer-Assistent?"
• "Wie erstelle ich Vorlagen?"

${dashboardType === 'lawyer' ? '• "Wie nutze ich das CRM?"\n• "Wie funktioniert die Rechtsprechungsanalyse?"' : ''}

Wählen Sie auch gerne eine Beispielfrage unten!`;
}

export default function SchnellstartPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [dashboardType, setDashboardType] = useState<DashboardType>('basis');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        router.push('/auth/login');
        return;
      }

      try {
        const userDoc = await getDoc(doc(db, 'users', user.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          const tier = data.tier || 'free';
          const dbType = data.dashboardType || 
            (tier === 'lawyer' ? 'lawyer' : tier === 'professional' ? 'professional' : 'basis');
          setDashboardType(dbType as DashboardType);
        }
      } catch (err) {
        console.error('Error loading user data:', err);
      }
      
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  // Initiale Begrüßung nach Laden
  useEffect(() => {
    if (!loading && messages.length === 0) {
      const welcome: Message = {
        id: '1',
        role: 'assistant',
        content: `# 🚀 Willkommen beim Schnellstart!

Ich bin Ihr persönlicher Assistent für das **${dashboardType === 'basis' ? 'Basis' : dashboardType === 'professional' ? 'Professional' : 'Lawyer Pro'}**-Dashboard.

Ich kenne jede Funktion im Detail und zeige Ihnen, wie Sie das Beste aus domulex.ai herausholen.

**Womit möchten Sie beginnen?**
• "Wie starte ich?" – Schritt-für-Schritt Anleitung
• "Was kann das Dashboard?" – Alle Funktionen im Überblick
• Oder fragen Sie zu einer bestimmten Funktion!`,
        timestamp: new Date()
      };
      setMessages([welcome]);
    }
  }, [loading, dashboardType, messages.length]);

  const scrollToNewMessage = () => {
    const container = document.querySelector('[data-chat-container]') as HTMLElement;
    if (container && messages.length >= 2) {
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

  const handleSend = async () => {
    if (!inputValue.trim() || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simuliere Tipp-Verzögerung
    await new Promise(r => setTimeout(r, 500 + Math.random() * 500));

    const answer = generateAnswer(inputValue, dashboardType);

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: answer,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, assistantMessage]);
    setIsTyping(false);
  };

  const handleExampleClick = (question: string) => {
    setInputValue(question);
    setTimeout(() => {
      handleSend();
    }, 100);
  };

  const exampleQuestions = dashboardType === 'lawyer' 
    ? ['Wie starte ich?', 'Wie nutze ich das CRM?', 'Wie funktioniert die Fristenverwaltung?', 'Wie erstelle ich Schriftsätze?']
    : dashboardType === 'professional'
    ? ['Wie starte ich?', 'Wie berechne ich Rendite?', 'Wie analysiere ich Verträge?', 'Wie erstelle ich Abrechnungen?']
    : ['Wie starte ich?', 'Wie funktioniert der Steuer-Assistent?', 'Wie erstelle ich Musterbriefe?', 'Welche Perspektive soll ich wählen?'];

  if (loading) {
    return (
      <div className="min-h-screen bg-[#fafaf8] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#1e3a5f]"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <Link 
                href="/dashboard"
                className="flex items-center gap-2 text-[#1e3a5f] hover:text-[#b8860b] transition-colors"
              >
                ← Dashboard
              </Link>
              <div className="h-6 w-px bg-gray-200" />
              <Logo size="sm" />
            </div>
            <span className="text-sm text-gray-500">Schnellstart</span>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 pt-24 pb-8">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-lg overflow-hidden">
          
          {/* Header */}
          <div className="bg-gradient-to-r from-[#1e3a5f] to-[#2d5a8f] p-4 sm:p-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🚀</span>
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-white">Schnellstart-Assistent</h1>
                <p className="text-white/80 text-sm">
                  Ihr Guide für das {dashboardType === 'basis' ? 'Basis' : dashboardType === 'professional' ? 'Professional' : 'Lawyer Pro'}-Dashboard
                </p>
              </div>
            </div>
          </div>

          {/* Chat Messages */}
          <div data-chat-container className="h-[400px] sm:h-[450px] overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((message, index) => (
              <div
                key={message.id}
                data-user-message={message.role === 'user' && index === messages.length - 2 ? "true" : undefined}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-[#1e3a5f] text-white'
                      : 'bg-white border border-gray-200 text-gray-700 shadow-sm'
                  }`}
                >
                  <div className="prose prose-sm max-w-none">
                    {message.content.split('\n').map((line, i) => {
                      // Überschriften
                      if (line.startsWith('# ')) {
                        return <h2 key={i} className={`text-lg font-bold mb-2 ${message.role === 'user' ? 'text-white' : 'text-[#1e3a5f]'}`}>{line.replace('# ', '')}</h2>;
                      }
                      if (line.startsWith('## ')) {
                        return <h3 key={i} className={`text-base font-bold mt-3 mb-2 ${message.role === 'user' ? 'text-white' : 'text-[#1e3a5f]'}`}>{line.replace('## ', '')}</h3>;
                      }
                      if (line.startsWith('### ')) {
                        return <h4 key={i} className={`font-semibold mt-2 mb-1 ${message.role === 'user' ? 'text-white' : 'text-[#1e3a5f]'}`}>{line.replace('### ', '')}</h4>;
                      }
                      // Liste
                      if (line.startsWith('• ') || line.startsWith('- ')) {
                        return <p key={i} className="ml-4 my-1">{line}</p>;
                      }
                      // Nummerierte Liste
                      if (line.match(/^\d+\./)) {
                        return <p key={i} className="my-2">{line.replace(/\*\*(.*?)\*\*/g, '$1')}</p>;
                      }
                      // Links
                      if (line.includes('[→')) {
                        const match = line.match(/\[(.+?)\]\((.+?)\)/);
                        if (match) {
                          return (
                            <Link key={i} href={match[2]} className="inline-block mt-3 px-4 py-2 bg-[#b8860b] text-white rounded-lg hover:bg-[#a07608] transition-colors">
                              {match[1]}
                            </Link>
                          );
                        }
                      }
                      // Bold
                      if (line.includes('**')) {
                        const parts = line.split(/\*\*(.*?)\*\*/g);
                        return (
                          <p key={i} className="my-1">
                            {parts.map((part, j) => j % 2 === 1 ? <strong key={j}>{part}</strong> : part)}
                          </p>
                        );
                      }
                      // Normal
                      return line ? <p key={i} className="my-1">{line}</p> : <br key={i} />;
                    })}
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Example Questions */}
          <div className="p-3 border-t border-gray-100 bg-white">
            <p className="text-xs text-gray-500 mb-2">Beispielfragen:</p>
            <div className="flex flex-wrap gap-2">
              {exampleQuestions.map((q, i) => (
                <button
                  key={i}
                  onClick={() => {
                    setInputValue(q);
                  }}
                  className="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-100 bg-white">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Fragen Sie zu einer Dashboard-Funktion..."
                className="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent outline-none"
                disabled={isTyping}
              />
              <button
                onClick={handleSend}
                disabled={!inputValue.trim() || isTyping}
                className="px-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Senden
              </button>
            </div>
          </div>
        </div>

        {/* Quick Access Card */}
        <div className="mt-6 bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-bold text-[#1e3a5f] mb-4">⚡ Schnellzugriff auf Ihre Werkzeuge</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {DASHBOARD_FEATURES[dashboardType].slice(0, 6).map((feature) => (
              <Link
                key={feature.name}
                href={feature.href}
                className="p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors text-center"
              >
                <p className="font-medium text-[#1e3a5f] text-sm">{feature.name}</p>
              </Link>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
