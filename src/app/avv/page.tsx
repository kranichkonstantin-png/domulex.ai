'use client';

import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';

export default function AVVPage() {
  return (
    <div className="min-h-screen bg-[#fafaf8]">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-[106px]">
            <Logo size="sm" />
            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-8">
              <Link href="/#vorteile" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">Vorteile</Link>
              <Link href="/#zielgruppen" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">Für wen?</Link>
              <Link href="/#pricing" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">Preise</Link>
              <Link href="/news" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">News</Link>
              <Link href="/faq" className="text-gray-600 hover:text-[#1e3a5f] font-medium transition-colors">FAQ</Link>
              <Link href="/auth/login" className="px-5 py-2.5 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-lg font-medium transition-colors">
                Anmelden
              </Link>
            </div>
            {/* Mobile */}
            <Link href="/auth/login" className="md:hidden px-4 py-2 bg-[#1e3a5f] text-white rounded-lg font-medium text-sm">
              Anmelden
            </Link>
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-4xl mx-auto px-4 pt-28 pb-16">
        <div className="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm">
          <h1 className="text-3xl font-bold text-[#1e3a5f] mb-2">Auftragsverarbeitungsvertrag (AVV)</h1>
          <p className="text-gray-500 mb-8">gemäß Art. 28 DSGVO</p>
          
          <div className="prose prose-gray max-w-none">
            <p className="text-sm text-gray-500 mb-6">Stand: Januar 2026</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 1 Gegenstand und Dauer der Verarbeitung</h2>
            <p><strong>(1)</strong> Dieser Auftragsverarbeitungsvertrag (nachfolgend &quot;AVV&quot;) konkretisiert die datenschutzrechtlichen Rechte und Pflichten der Vertragsparteien im Zusammenhang mit der Nutzung der Plattform domulex.ai.</p>
            <p><strong>(2)</strong> Der Auftragnehmer (Home Invest &amp; Management GmbH, nachfolgend &quot;domulex.ai&quot;) verarbeitet personenbezogene Daten im Auftrag des Auftraggebers (nachfolgend &quot;Kunde&quot;) ausschließlich im Rahmen der vereinbarten Leistungen.</p>
            <p><strong>(3)</strong> Die Laufzeit dieses AVV entspricht der Laufzeit des Hauptvertrags (Nutzungsvertrag domulex.ai). Der AVV endet automatisch mit Beendigung des Hauptvertrags.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 2 Art und Zweck der Verarbeitung</h2>
            <p><strong>(1)</strong> Art der Verarbeitung:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Speicherung und Verarbeitung von Nutzerdaten zur Bereitstellung der Plattform</li>
              <li>Analyse von hochgeladenen Dokumenten (Vertragsanalyse)</li>
              <li>Verarbeitung von Anfragen im Rechts-Chat</li>
              <li>Speicherung von Mandantendaten im CRM (Lawyer Pro)</li>
              <li>Generierung von Dokumenten und Schriftsätzen</li>
            </ul>
            <p className="mt-4"><strong>(2)</strong> Zweck der Verarbeitung:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Erbringung der vertraglich vereinbarten KI-gestützten Rechtsanalyse-Dienstleistungen</li>
              <li>Mandantenverwaltung für Rechtsanwälte (Lawyer Pro Tarif)</li>
              <li>Dokumentenmanagement und -generierung</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 3 Art der personenbezogenen Daten</h2>
            <p>Folgende Kategorien personenbezogener Daten werden verarbeitet:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li><strong>Bestandsdaten:</strong> Name, E-Mail-Adresse, Firmenname, Anschrift</li>
              <li><strong>Nutzungsdaten:</strong> Anfragen, Suchanfragen, Zeitstempel</li>
              <li><strong>Vertragsdaten:</strong> Miet-/Kaufverträge, die zur Analyse hochgeladen werden</li>
              <li><strong>Mandantendaten (Lawyer Pro):</strong> Namen, Kontaktdaten, Aktenzeichen, Schriftsätze</li>
              <li><strong>Zahlungsdaten:</strong> Werden direkt bei Stripe verarbeitet (nicht bei domulex.ai)</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 4 Kategorien betroffener Personen</h2>
            <ul className="list-disc pl-6 space-y-1">
              <li>Mitarbeiter des Auftraggebers</li>
              <li>Mandanten des Auftraggebers (bei Lawyer Pro)</li>
              <li>Vertragsparteien in hochgeladenen Dokumenten</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 5 Pflichten des Auftragnehmers</h2>
            <p><strong>(1)</strong> Der Auftragnehmer verpflichtet sich:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Personenbezogene Daten nur auf dokumentierte Weisung des Auftraggebers zu verarbeiten</li>
              <li>Die Vertraulichkeit gemäß Art. 28 Abs. 3 lit. b DSGVO zu gewährleisten</li>
              <li>Alle erforderlichen technischen und organisatorischen Maßnahmen gemäß Art. 32 DSGVO zu ergreifen</li>
              <li>Unterauftragnehmer nur mit vorheriger Zustimmung des Auftraggebers einzusetzen</li>
              <li>Den Auftraggeber bei der Erfüllung von Betroffenenrechten zu unterstützen</li>
              <li>Nach Beendigung der Auftragsverarbeitung alle Daten zu löschen oder zurückzugeben</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Der Auftragnehmer stellt sicher, dass die zur Verarbeitung befugten Personen zur Vertraulichkeit verpflichtet sind.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 6 Technische und organisatorische Maßnahmen (TOMs)</h2>
            <p>Der Auftragnehmer hat folgende Maßnahmen implementiert:</p>
            
            <p className="mt-4"><strong>Zutrittskontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Serverstandort: Google Cloud Platform, Region europe-west3 (Frankfurt)</li>
              <li>ISO 27001 zertifiziertes Rechenzentrum</li>
            </ul>

            <p className="mt-4"><strong>Zugangskontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Authentifizierung über Firebase Authentication</li>
              <li>Passwort-Richtlinien (Mindestlänge, Komplexität)</li>
              <li>Optionale Zwei-Faktor-Authentifizierung</li>
            </ul>

            <p className="mt-4"><strong>Zugriffskontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Rollenbasiertes Berechtigungskonzept</li>
              <li>Strikte Mandantentrennung</li>
              <li>Protokollierung von Zugriffen</li>
            </ul>

            <p className="mt-4"><strong>Weitergabekontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>TLS 1.3 Verschlüsselung aller Datenübertragungen</li>
              <li>Verschlüsselung ruhender Daten (AES-256)</li>
            </ul>

            <p className="mt-4"><strong>Eingabekontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Vollständige Protokollierung aller Eingaben</li>
              <li>Audit-Logs mit Zeitstempeln</li>
            </ul>

            <p className="mt-4"><strong>Auftragskontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Verarbeitung nur gemäß Vertrag und Weisung</li>
              <li>Regelmäßige Compliance-Prüfungen</li>
            </ul>

            <p className="mt-4"><strong>Verfügbarkeitskontrolle:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Redundante Systemauslegung</li>
              <li>Regelmäßige Backups</li>
              <li>Disaster Recovery Plan</li>
            </ul>

            <p className="mt-4"><strong>Trennungsgebot:</strong></p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Logische Mandantentrennung</li>
              <li>Separate Datenbanken pro Mandant (bei Enterprise)</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 7 Unterauftragnehmer</h2>
            <p><strong>(1)</strong> Folgende Unterauftragnehmer sind zum Zeitpunkt des Vertragsschlusses genehmigt:</p>
            
            <div className="overflow-x-auto mt-4">
              <table className="min-w-full border border-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Unterauftragnehmer</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Zweck</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Standort</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr>
                    <td className="px-4 py-2 text-sm">Google Cloud Platform</td>
                    <td className="px-4 py-2 text-sm">Hosting, Datenbank</td>
                    <td className="px-4 py-2 text-sm">Frankfurt, DE</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">Firebase (Google)</td>
                    <td className="px-4 py-2 text-sm">Authentifizierung, Firestore</td>
                    <td className="px-4 py-2 text-sm">Frankfurt, DE</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">Qdrant Cloud</td>
                    <td className="px-4 py-2 text-sm">Vektordatenbank für RAG</td>
                    <td className="px-4 py-2 text-sm">Frankfurt, DE</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">Google Gemini API</td>
                    <td className="px-4 py-2 text-sm">KI-Verarbeitung</td>
                    <td className="px-4 py-2 text-sm">EU (Zero Data Retention)</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">Stripe Inc.</td>
                    <td className="px-4 py-2 text-sm">Zahlungsabwicklung</td>
                    <td className="px-4 py-2 text-sm">Dublin, IE</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 text-sm">Resend</td>
                    <td className="px-4 py-2 text-sm">E-Mail-Versand</td>
                    <td className="px-4 py-2 text-sm">EU</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p className="mt-4"><strong>(2)</strong> Änderungen bei Unterauftragnehmern werden dem Auftraggeber mindestens 14 Tage vor Wirksamwerden mitgeteilt. Der Auftraggeber kann innerhalb von 7 Tagen widersprechen.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 8 Rechte der betroffenen Personen</h2>
            <p><strong>(1)</strong> Der Auftragnehmer unterstützt den Auftraggeber bei der Erfüllung der Rechte betroffener Personen:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Auskunftsrecht (Art. 15 DSGVO)</li>
              <li>Recht auf Berichtigung (Art. 16 DSGVO)</li>
              <li>Recht auf Löschung (Art. 17 DSGVO)</li>
              <li>Recht auf Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
              <li>Recht auf Datenübertragbarkeit (Art. 20 DSGVO)</li>
              <li>Widerspruchsrecht (Art. 21 DSGVO)</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Anfragen betroffener Personen leitet der Auftragnehmer unverzüglich an den Auftraggeber weiter.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 9 Meldepflichten bei Datenschutzverletzungen</h2>
            <p><strong>(1)</strong> Der Auftragnehmer informiert den Auftraggeber unverzüglich, spätestens jedoch innerhalb von 24 Stunden, über Verletzungen des Schutzes personenbezogener Daten.</p>
            <p><strong>(2)</strong> Die Meldung enthält mindestens:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Art der Verletzung</li>
              <li>Betroffene Datenkategorien und ungefähre Anzahl betroffener Personen</li>
              <li>Wahrscheinliche Folgen</li>
              <li>Ergriffene oder vorgeschlagene Maßnahmen</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 10 Kontrollrechte des Auftraggebers</h2>
            <p><strong>(1)</strong> Der Auftraggeber ist berechtigt, die Einhaltung der Datenschutzvorschriften und der Weisungen zu überprüfen.</p>
            <p><strong>(2)</strong> Der Auftragnehmer stellt alle erforderlichen Informationen zum Nachweis der Einhaltung der Pflichten zur Verfügung.</p>
            <p><strong>(3)</strong> Vor-Ort-Audits sind nach Abstimmung und unter Wahrung der Vertraulichkeit möglich.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 11 Löschung und Rückgabe von Daten</h2>
            <p><strong>(1)</strong> Nach Beendigung des Hauptvertrags löscht der Auftragnehmer alle personenbezogenen Daten, sofern keine gesetzliche Aufbewahrungspflicht besteht.</p>
            <p><strong>(2)</strong> Auf Wunsch des Auftraggebers erfolgt vor Löschung eine Datenrückgabe in einem gängigen Format (JSON, CSV).</p>
            <p><strong>(3)</strong> Die Löschung wird dem Auftraggeber schriftlich bestätigt.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 12 Haftung</h2>
            <p>Die Haftung richtet sich nach den Bestimmungen des Hauptvertrags (AGB) sowie den gesetzlichen Regelungen der DSGVO, insbesondere Art. 82 DSGVO.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 13 Schlussbestimmungen</h2>
            <p><strong>(1)</strong> Änderungen und Ergänzungen dieses AVV bedürfen der Schriftform.</p>
            <p><strong>(2)</strong> Sollten einzelne Bestimmungen unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.</p>
            <p><strong>(3)</strong> Es gilt deutsches Recht. Gerichtsstand ist Frankfurt am Main.</p>

            <div className="mt-12 p-6 bg-gray-50 rounded-xl">
              <h3 className="font-semibold text-[#1e3a5f] mb-4">Kontakt für Datenschutzanfragen</h3>
              <p className="text-gray-600">
                Home Invest &amp; Management GmbH<br />
                Datenschutzbeauftragter<br />
                E-Mail: <a href="mailto:datenschutz@domulex.ai" className="text-[#b8860b]">datenschutz@domulex.ai</a>
              </p>
            </div>
          </div>
        </div>

        {/* Download Button */}
        <div className="mt-8 text-center">
          <a 
            href="/downloads/avv.pdf" 
            className="inline-flex items-center gap-2 px-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-xl font-medium transition-colors"
          >
            📄 AVV als PDF herunterladen
          </a>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
