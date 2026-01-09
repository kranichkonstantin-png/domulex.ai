'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter } from 'next/navigation';
import { onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc, collection, addDoc, getDocs, query, orderBy, Timestamp } from 'firebase/firestore';
import { auth, db } from '@/lib/firebase';
import Link from 'next/link';
import Logo from '@/components/Logo';
import UpgradeModal from '@/components/UpgradeModal';

interface DocumentTemplate {
  id: string;
  name: string;
  category: string;
  description: string;
  icon: string;
  fields: TemplateField[];
  template: string;
}

interface TemplateField {
  id: string;
  label: string;
  type: 'text' | 'textarea' | 'date' | 'select' | 'number';
  placeholder?: string;
  required?: boolean;
  options?: string[];
}

interface GeneratedDocument {
  id: string;
  templateId: string;
  templateName: string;
  content: string;
  createdAt: Date;
}

const DOCUMENT_TEMPLATES: DocumentTemplate[] = [
  {
    id: 'mietminderung',
    name: 'Mietminderungsschreiben',
    category: 'Mietrecht',
    description: 'Professionelle Mietminderung wegen Mängeln',
    icon: '🏠',
    fields: [
      { id: 'vermieter_name', label: 'Name des Vermieters', type: 'text', required: true, placeholder: 'Max Mustermann' },
      { id: 'vermieter_adresse', label: 'Adresse des Vermieters', type: 'textarea', required: true, placeholder: 'Musterstraße 1, 12345 Berlin' },
      { id: 'mandant_name', label: 'Name des Mandanten', type: 'text', required: true },
      { id: 'mandant_adresse', label: 'Adresse der Mietsache', type: 'textarea', required: true },
      { id: 'mangel_beschreibung', label: 'Beschreibung des Mangels', type: 'textarea', required: true, placeholder: 'Detaillierte Beschreibung des Mangels...' },
      { id: 'mangel_datum', label: 'Datum der Mängelanzeige', type: 'date', required: true },
      { id: 'minderung_prozent', label: 'Minderungsquote (%)', type: 'number', required: true, placeholder: '20' },
      { id: 'kaltmiete', label: 'Kaltmiete (€)', type: 'number', required: true },
    ],
    template: `[RECHTSANWALTSKANZLEI BRIEFKOPF]

{datum}

An
{vermieter_name}
{vermieter_adresse}

Betreff: Mietminderung gem. § 536 BGB für die Wohnung {mandant_adresse}
Mandant: {mandant_name}

Sehr geehrte/r {vermieter_name},

namens und in Vollmacht unseres Mandanten {mandant_name} zeigen wir die anwaltliche Vertretung an.

Unser Mandant bewohnt die oben bezeichnete Wohnung aufgrund des mit Ihnen bestehenden Mietverhältnisses.

Mit Schreiben vom {mangel_datum} wurde Ihnen folgender Mangel angezeigt:

{mangel_beschreibung}

Trotz Aufforderung zur Mängelbeseitigung ist der Mangel bis heute nicht behoben worden.

Gemäß § 536 Abs. 1 BGB ist die Miete kraft Gesetzes gemindert, solange ein Mangel besteht, der die Tauglichkeit der Mietsache zum vertragsgemäßen Gebrauch aufhebt oder mindert.

Unter Berücksichtigung der Rechtsprechung zu vergleichbaren Mängeln halten wir eine Minderungsquote von {minderung_prozent}% für angemessen.

Bei einer Kaltmiete von {kaltmiete},- € entspricht dies einem monatlichen Minderungsbetrag von {minderung_betrag},- €.

Wir fordern Sie daher auf:

1. Die Minderung in vorgenannter Höhe anzuerkennen
2. Den Mangel unverzüglich, spätestens bis zum {frist_datum} zu beseitigen
3. Die zu viel gezahlte Miete seit Mängelanzeige in Höhe von {rueckzahlung_betrag},- € an unseren Mandanten zurückzuzahlen

Sollten wir bis zum genannten Datum keine positive Rückmeldung erhalten, behalten wir uns vor, die Ansprüche unseres Mandanten gerichtlich durchzusetzen.

Mit freundlichen Grüßen

[Unterschrift]
Rechtsanwalt/Rechtsanwältin`
  },
  {
    id: 'kuendigung_mieter',
    name: 'Kündigungsschreiben (Vermieter)',
    category: 'Mietrecht',
    description: 'Ordentliche Kündigung des Mietverhältnisses',
    icon: '📋',
    fields: [
      { id: 'mieter_name', label: 'Name des Mieters', type: 'text', required: true },
      { id: 'mieter_adresse', label: 'Adresse des Mieters', type: 'textarea', required: true },
      { id: 'mandant_name', label: 'Name des Mandanten (Vermieter)', type: 'text', required: true },
      { id: 'objekt_adresse', label: 'Adresse des Mietobjekts', type: 'textarea', required: true },
      { id: 'kuendigung_grund', label: 'Kündigungsgrund', type: 'select', required: true, options: ['Eigenbedarf', 'Wirtschaftliche Verwertung', 'Vertragsverletzung', 'Zahlungsverzug'] },
      { id: 'kuendigung_begruendung', label: 'Detaillierte Begründung', type: 'textarea', required: true },
      { id: 'mietverhaeltnis_beginn', label: 'Beginn Mietverhältnis', type: 'date', required: true },
    ],
    template: `[RECHTSANWALTSKANZLEI BRIEFKOPF]

{datum}

Per Einschreiben mit Rückschein

An
{mieter_name}
{mieter_adresse}

Betreff: Ordentliche Kündigung des Mietverhältnisses über die Wohnung {objekt_adresse}
Mandantschaft: {mandant_name}

Sehr geehrte/r {mieter_name},

namens und in Vollmacht unseres Mandanten {mandant_name} kündigen wir hiermit das zwischen Ihnen bestehende Mietverhältnis über die oben bezeichnete Wohnung ordentlich.

Das Mietverhältnis begann am {mietverhaeltnis_beginn} und besteht somit seit {mietdauer}. Die gesetzliche Kündigungsfrist beträgt daher {kuendigungsfrist} Monate.

Die Kündigung erfolgt zum nächstmöglichen Termin, das ist der {kuendigungstermin}.

Kündigungsgrund nach § 573 BGB: {kuendigung_grund}

Begründung:
{kuendigung_begruendung}

Wir weisen darauf hin, dass Sie gemäß § 574 BGB der Kündigung widersprechen können, wenn die Beendigung des Mietverhältnisses für Sie, Ihre Familie oder einen anderen Angehörigen Ihres Haushalts eine Härte bedeuten würde, die auch unter Würdigung der berechtigten Interessen des Vermieters nicht zu rechtfertigen ist.

Der Widerspruch muss schriftlich erfolgen und unserem Mandanten spätestens zwei Monate vor Beendigung des Mietverhältnisses zugehen.

Sollte die Wohnung nicht fristgerecht geräumt übergeben werden, behalten wir uns vor, Räumungsklage zu erheben.

Mit freundlichen Grüßen

[Unterschrift]
Rechtsanwalt/Rechtsanwältin`
  },
  {
    id: 'weg_anfechtung',
    name: 'WEG-Beschlussanfechtung',
    category: 'WEG-Recht',
    description: 'Anfechtungsklage gegen WEG-Beschluss',
    icon: '⚖️',
    fields: [
      { id: 'mandant_name', label: 'Name des Mandanten', type: 'text', required: true },
      { id: 'weg_name', label: 'Name der WEG', type: 'text', required: true, placeholder: 'WEG Musterstraße 1-5' },
      { id: 'verwalter_name', label: 'Name des Verwalters', type: 'text', required: true },
      { id: 'verwalter_adresse', label: 'Adresse des Verwalters', type: 'textarea', required: true },
      { id: 'versammlung_datum', label: 'Datum der Eigentümerversammlung', type: 'date', required: true },
      { id: 'beschluss_top', label: 'TOP-Nummer des Beschlusses', type: 'text', required: true, placeholder: 'TOP 5' },
      { id: 'beschluss_inhalt', label: 'Inhalt des Beschlusses', type: 'textarea', required: true },
      { id: 'anfechtung_gruende', label: 'Anfechtungsgründe', type: 'textarea', required: true },
    ],
    template: `An das
Amtsgericht {zustaendiges_gericht}
- Wohnungseigentumsgericht -

{datum}

Klage

des/der {mandant_name}, wohnhaft {mandant_adresse}
- Kläger/in -

Prozessbevollmächtigte: [Kanzlei]

gegen

die übrigen Wohnungseigentümer der {weg_name}, 
vertreten durch den Verwalter {verwalter_name}, {verwalter_adresse}
- Beklagte -

wegen: Anfechtung eines Beschlusses der Eigentümerversammlung

Streitwert: {streitwert},- €

Namens und in Vollmacht des Klägers/der Klägerin erhebe ich Klage und beantrage:

1. Der in der Eigentümerversammlung vom {versammlung_datum} unter {beschluss_top} gefasste Beschluss mit folgendem Inhalt:

"{beschluss_inhalt}"

wird für ungültig erklärt.

2. Die Beklagten tragen die Kosten des Rechtsstreits.

Begründung:

I. Sachverhalt

Der Kläger/Die Klägerin ist Mitglied der beklagten Wohnungseigentümergemeinschaft. In der Eigentümerversammlung vom {versammlung_datum} wurde unter {beschluss_top} der streitgegenständliche Beschluss gefasst.

II. Rechtliche Würdigung

Der angegriffene Beschluss ist gem. § 23 Abs. 4 WEG für ungültig zu erklären.

{anfechtung_gruende}

Die Anfechtungsklage ist binnen der Monatsfrist des § 46 Abs. 1 WEG erhoben worden und damit zulässig.

III. Streitwert

Der Streitwert wird nach § 49a GKG auf {streitwert},- € geschätzt.

Beweis: wird angetreten durch Vorlage der Einladung und des Protokolls zur Eigentümerversammlung

Mit freundlichen Grüßen

[Unterschrift]
Rechtsanwalt/Rechtsanwältin`
  },
  {
    id: 'abmahnung',
    name: 'Abmahnung wegen Vertragsverletzung',
    category: 'Mietrecht',
    description: 'Abmahnung vor Kündigung',
    icon: '⚠️',
    fields: [
      { id: 'mieter_name', label: 'Name des Mieters', type: 'text', required: true },
      { id: 'mieter_adresse', label: 'Adresse des Mieters', type: 'textarea', required: true },
      { id: 'mandant_name', label: 'Name des Mandanten (Vermieter)', type: 'text', required: true },
      { id: 'objekt_adresse', label: 'Adresse des Mietobjekts', type: 'textarea', required: true },
      { id: 'verstoss_art', label: 'Art des Verstoßes', type: 'select', required: true, options: ['Ruhestörung', 'Unerlaubte Tierhaltung', 'Unerlaubte Untervermietung', 'Beschädigung der Mietsache', 'Verstoß gegen Hausordnung', 'Sonstiges'] },
      { id: 'verstoss_beschreibung', label: 'Beschreibung des Verstoßes', type: 'textarea', required: true },
      { id: 'verstoss_datum', label: 'Datum des Verstoßes', type: 'date', required: true },
    ],
    template: `[RECHTSANWALTSKANZLEI BRIEFKOPF]

{datum}

Per Einschreiben mit Rückschein

An
{mieter_name}
{mieter_adresse}

Betreff: Abmahnung wegen Vertragsverletzung - Mietobjekt {objekt_adresse}
Mandantschaft: {mandant_name}

Sehr geehrte/r {mieter_name},

namens und in Vollmacht unseres Mandanten {mandant_name} müssen wir Sie hiermit wegen Verletzung Ihrer mietvertraglichen Pflichten abmahnen.

Art des Verstoßes: {verstoss_art}

Am {verstoss_datum} ist folgender Vorfall eingetreten:

{verstoss_beschreibung}

Dieses Verhalten stellt eine erhebliche Verletzung Ihrer Pflichten aus dem Mietvertrag dar und ist für unseren Mandanten sowie die übrigen Hausbewohner nicht hinnehmbar.

Wir fordern Sie auf, das beanstandete Verhalten ab sofort und dauerhaft zu unterlassen.

Sollte es zu einem weiteren gleichartigen oder vergleichbaren Verstoß kommen, ist unser Mandant berechtigt, das Mietverhältnis fristlos, hilfsweise fristgerecht zu kündigen.

Wir gehen davon aus, dass Sie diese Abmahnung ernst nehmen und künftig Ihre vertraglichen Pflichten ordnungsgemäß erfüllen werden.

Mit freundlichen Grüßen

[Unterschrift]
Rechtsanwalt/Rechtsanwältin`
  },
  {
    id: 'kaufvertrag_pruefung',
    name: 'Stellungnahme Kaufvertragsentwurf',
    category: 'Immobilienkauf',
    description: 'Juristische Prüfung eines Kaufvertragsentwurfs',
    icon: '🏢',
    fields: [
      { id: 'mandant_name', label: 'Name des Mandanten', type: 'text', required: true },
      { id: 'objekt_beschreibung', label: 'Beschreibung des Objekts', type: 'textarea', required: true },
      { id: 'kaufpreis', label: 'Kaufpreis (€)', type: 'number', required: true },
      { id: 'verkaeufer_name', label: 'Name des Verkäufers', type: 'text', required: true },
      { id: 'notar_name', label: 'Beurkundender Notar', type: 'text', required: true },
      { id: 'pruefung_ergebnis', label: 'Ergebnis der Prüfung', type: 'textarea', required: true },
      { id: 'aenderung_vorschlaege', label: 'Änderungsvorschläge', type: 'textarea', required: true },
    ],
    template: `[RECHTSANWALTSKANZLEI BRIEFKOPF]

{datum}

Vertraulich

An
{mandant_name}
{mandant_adresse}

Betreff: Stellungnahme zum Kaufvertragsentwurf
Objekt: {objekt_beschreibung}
Kaufpreis: {kaufpreis},- €

Sehr geehrte/r {mandant_name},

wie beauftragt haben wir den von Notar {notar_name} übersandten Kaufvertragsentwurf rechtlich geprüft und nehmen wie folgt Stellung:

I. Zusammenfassung des Vertragsentwurfs

Gegenstand des Vertrages ist der Erwerb des oben bezeichneten Objekts vom Verkäufer {verkaeufer_name} zu einem Kaufpreis von {kaufpreis},- €.

II. Rechtliche Würdigung

{pruefung_ergebnis}

III. Empfohlene Änderungen

Nach unserer Prüfung empfehlen wir folgende Änderungen am Vertragsentwurf:

{aenderung_vorschlaege}

IV. Weitere Empfehlungen

1. Vor Vertragsschluss sollte eine aktuelle Grundbucheinsicht erfolgen
2. Die Lastenfreistellung ist vor Kaufpreiszahlung sicherzustellen
3. Eine Besichtigung des Objekts unmittelbar vor Beurkundung wird empfohlen

V. Weiteres Vorgehen

Bitte teilen Sie uns mit, ob wir die empfohlenen Änderungen gegenüber dem beurkundenden Notar kommunizieren sollen.

Für Rückfragen stehen wir Ihnen selbstverständlich gerne zur Verfügung.

Mit freundlichen Grüßen

[Unterschrift]
Rechtsanwalt/Rechtsanwältin`
  }
];

export default function DocumentGeneratorPage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState<DocumentTemplate | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [generatedContent, setGeneratedContent] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [savedDocuments, setSavedDocuments] = useState<GeneratedDocument[]>([]);
  const [showSaved, setShowSaved] = useState(false);
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [userTier, setUserTier] = useState<string>('free');
  const router = useRouter();

  // Check if user has access
  const hasAccess = userTier === 'lawyer';
  
  // Wrapper for actions that require tier
  const requireTier = (action: () => void) => {
    if (!hasAccess) {
      setShowUpgradeModal(true);
      return;
    }
    action();
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (!currentUser) {
        router.push('/auth/login');
        return;
      }

      setUser(currentUser);

      // Check tier - set tier for soft-lock instead of redirect
      const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
      if (userDoc.exists()) {
        const userData = userDoc.data();
        const tier = userData.tier || userData.dashboardType || 'free';
        setUserTier(tier);
        
        // Load saved documents only for lawyers (others see demo/empty state)
        if (tier === 'lawyer') {
          await loadSavedDocuments(currentUser.uid);
        }
      }
      
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  const loadSavedDocuments = async (userId: string) => {
    try {
      const docsRef = collection(db, 'users', userId, 'generated_documents');
      const q = query(docsRef, orderBy('createdAt', 'desc'));
      const snapshot = await getDocs(q);
      
      const docs: GeneratedDocument[] = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
        createdAt: doc.data().createdAt?.toDate() || new Date()
      })) as GeneratedDocument[];
      
      setSavedDocuments(docs);
    } catch (error) {
      console.error('Error loading documents:', error);
    }
  };

  const selectTemplate = (template: DocumentTemplate) => {
    setSelectedTemplate(template);
    setFormData({});
    setGeneratedContent('');
  };

  const handleFieldChange = (fieldId: string, value: string) => {
    setFormData(prev => ({ ...prev, [fieldId]: value }));
  };

  const generateDocument = () => {
    if (!selectedTemplate) return;

    setIsGenerating(true);

    // Simulate AI generation (in production, this would call the backend)
    setTimeout(() => {
      let content = selectedTemplate.template;

      // Replace placeholders with form data
      Object.entries(formData).forEach(([key, value]) => {
        content = content.replace(new RegExp(`{${key}}`, 'g'), value);
      });

      // Add calculated fields
      const today = new Date();
      content = content.replace(/{datum}/g, today.toLocaleDateString('de-DE', { day: '2-digit', month: 'long', year: 'numeric' }));
      
      // Calculate derived values
      if (formData.minderung_prozent && formData.kaltmiete) {
        const minderungBetrag = (parseFloat(formData.kaltmiete) * parseFloat(formData.minderung_prozent) / 100).toFixed(2);
        content = content.replace(/{minderung_betrag}/g, minderungBetrag);
        
        // Frist: 2 Wochen
        const frist = new Date(today);
        frist.setDate(frist.getDate() + 14);
        content = content.replace(/{frist_datum}/g, frist.toLocaleDateString('de-DE'));
        
        // Rückzahlung (vereinfacht: 1 Monat)
        content = content.replace(/{rueckzahlung_betrag}/g, minderungBetrag);
      }

      // Kündigungsfristen berechnen
      if (formData.mietverhaeltnis_beginn) {
        const beginn = new Date(formData.mietverhaeltnis_beginn);
        const monate = Math.floor((today.getTime() - beginn.getTime()) / (1000 * 60 * 60 * 24 * 30));
        const jahre = Math.floor(monate / 12);
        content = content.replace(/{mietdauer}/g, `${jahre} Jahren und ${monate % 12} Monaten`);
        
        let kuendigungsfrist = 3;
        if (monate >= 60) kuendigungsfrist = 6;
        else if (monate >= 96) kuendigungsfrist = 9;
        content = content.replace(/{kuendigungsfrist}/g, kuendigungsfrist.toString());
        
        const kuendigungstermin = new Date(today);
        kuendigungstermin.setMonth(kuendigungstermin.getMonth() + kuendigungsfrist + 1);
        kuendigungstermin.setDate(0); // Letzter Tag des Monats
        content = content.replace(/{kuendigungstermin}/g, kuendigungstermin.toLocaleDateString('de-DE'));
      }

      // Platzhalter für nicht ausgefüllte Felder markieren
      content = content.replace(/{[^}]+}/g, '[BITTE ERGÄNZEN]');

      setGeneratedContent(content);
      setIsGenerating(false);
    }, 1500);
  };

  const saveDocument = async () => {
    if (!user || !selectedTemplate || !generatedContent) return;

    try {
      // Generate AI summary
      let aiSummary = '';
      try {
        const summaryResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/documents/generate-summary`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: generatedContent,
            template_name: selectedTemplate.name
          })
        });
        
        if (summaryResponse.ok) {
          const summaryData = await summaryResponse.json();
          aiSummary = summaryData.summary || '';
        }
      } catch (e) {
        console.warn('Failed to generate summary:', e);
      }

      const docsRef = collection(db, 'users', user.uid, 'generated_documents');
      await addDoc(docsRef, {
        templateId: selectedTemplate.id,
        templateName: selectedTemplate.name,
        content: generatedContent,
        aiSummary: aiSummary,
        createdAt: Timestamp.now()
      });

      await loadSavedDocuments(user.uid);
      alert('Dokument gespeichert!');
    } catch (error) {
      console.error('Error saving document:', error);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedContent);
    alert('In Zwischenablage kopiert!');
  };

  const downloadAsText = () => {
    const blob = new Blob([generatedContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selectedTemplate?.name || 'dokument'}_${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const categories = [...new Set(DOCUMENT_TEMPLATES.map(t => t.category))];
  const filteredTemplates = filterCategory === 'all' 
    ? DOCUMENT_TEMPLATES 
    : DOCUMENT_TEMPLATES.filter(t => t.category === filterCategory);

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
          <div className="flex justify-between items-center h-[106px]">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-gray-500 hover:text-[#1e3a5f]">
                ← Dashboard
              </Link>
              <Logo size="sm" />
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowSaved(!showSaved)}
                className={`px-4 py-2 rounded-lg transition-colors ${showSaved ? 'bg-[#1e3a5f] text-white' : 'border border-gray-300 hover:bg-gray-50'}`}
              >
                📁 Gespeicherte ({savedDocuments.length})
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-[#1e3a5f]">Schriftsatz-Generator</h1>
          <p className="text-gray-600 mt-2">Erstellen Sie professionelle Rechtsdokumente mit KI-Unterstützung</p>
        </div>

        {showSaved ? (
          /* Saved Documents View */
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
            <div className="p-6 border-b border-gray-100">
              <h2 className="font-semibold text-[#1e3a5f]">Gespeicherte Dokumente</h2>
            </div>
            <div className="divide-y divide-gray-100">
              {savedDocuments.length === 0 ? (
                <div className="p-12 text-center text-gray-500">
                  <p className="text-4xl mb-4">📄</p>
                  <p>Keine gespeicherten Dokumente</p>
                </div>
              ) : (
                savedDocuments.map((doc) => (
                  <div key={doc.id} className="p-4 hover:bg-gray-50 cursor-pointer" onClick={() => {
                    setGeneratedContent(doc.content);
                    setShowSaved(false);
                  }}>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-[#1e3a5f]">{doc.templateName}</p>
                        <p className="text-sm text-gray-500">{doc.createdAt.toLocaleDateString('de-DE')}</p>
                      </div>
                      <span className="text-gray-400">→</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Template Selection */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                <div className="p-4 border-b border-gray-100">
                  <h2 className="font-semibold text-[#1e3a5f] mb-3">Vorlagen</h2>
                  <select
                    value={filterCategory}
                    onChange={(e) => setFilterCategory(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  >
                    <option value="all">Alle Kategorien</option>
                    {categories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
                <div className="divide-y divide-gray-100 max-h-[500px] overflow-y-auto">
                  {filteredTemplates.map((template) => (
                    <button
                      key={template.id}
                      onClick={() => selectTemplate(template)}
                      className={`w-full p-4 text-left hover:bg-gray-50 transition-colors ${
                        selectedTemplate?.id === template.id ? 'bg-[#1e3a5f]/5 border-l-4 border-[#1e3a5f]' : ''
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{template.icon}</span>
                        <div>
                          <p className="font-medium text-[#1e3a5f]">{template.name}</p>
                          <p className="text-xs text-gray-500">{template.category}</p>
                          <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Form & Preview */}
            <div className="lg:col-span-2">
              {selectedTemplate ? (
                <div className="space-y-6">
                  {/* Form */}
                  <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
                    <h2 className="font-semibold text-[#1e3a5f] mb-4">
                      {selectedTemplate.icon} {selectedTemplate.name}
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {selectedTemplate.fields.map((field) => (
                        <div key={field.id} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            {field.label} {field.required && <span className="text-red-500">*</span>}
                          </label>
                          
                          {field.type === 'textarea' ? (
                            <textarea
                              value={formData[field.id] || ''}
                              onChange={(e) => handleFieldChange(field.id, e.target.value)}
                              placeholder={field.placeholder}
                              rows={3}
                              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                            />
                          ) : field.type === 'select' ? (
                            <select
                              value={formData[field.id] || ''}
                              onChange={(e) => handleFieldChange(field.id, e.target.value)}
                              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                            >
                              <option value="">Bitte wählen...</option>
                              {field.options?.map(opt => (
                                <option key={opt} value={opt}>{opt}</option>
                              ))}
                            </select>
                          ) : (
                            <input
                              type={field.type}
                              value={formData[field.id] || ''}
                              onChange={(e) => handleFieldChange(field.id, e.target.value)}
                              placeholder={field.placeholder}
                              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f]"
                            />
                          )}
                        </div>
                      ))}
                    </div>

                    <button
                      onClick={generateDocument}
                      disabled={isGenerating}
                      className="mt-6 w-full py-3 bg-[#b8860b] hover:bg-[#a07608] text-white rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                      {isGenerating ? '⏳ Wird generiert...' : '🪄 Dokument generieren'}
                    </button>
                  </div>

                  {/* Preview */}
                  {generatedContent && (
                    <div className="bg-white rounded-xl border border-gray-100 shadow-sm">
                      <div className="p-4 border-b border-gray-100 flex items-center justify-between">
                        <h2 className="font-semibold text-[#1e3a5f]">Generiertes Dokument</h2>
                        <div className="flex gap-2">
                          <button
                            onClick={copyToClipboard}
                            className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50"
                          >
                            📋 Kopieren
                          </button>
                          <button
                            onClick={downloadAsText}
                            className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50"
                          >
                            ⬇️ Download
                          </button>
                          <button
                            onClick={saveDocument}
                            className="px-3 py-1 text-sm bg-[#1e3a5f] text-white rounded hover:bg-[#2d4a6f]"
                          >
                            💾 Speichern
                          </button>
                        </div>
                      </div>
                      <div className="p-6">
                        <pre className="whitespace-pre-wrap font-mono text-sm text-gray-700 bg-gray-50 p-4 rounded-lg max-h-[600px] overflow-y-auto">
                          {generatedContent}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-12 text-center">
                  <p className="text-6xl mb-4">📝</p>
                  <p className="text-lg text-gray-600">Wählen Sie eine Vorlage aus der Liste</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Professionelle Schriftsätze für Mietrecht, WEG-Recht und mehr
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        requiredTier="lawyer"
        feature="Dokumentenerstellung"
      />
    </div>
  );
}
