'use client';

import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';

export default function DatenschutzPage() {
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
      <main className="max-w-4xl mx-auto px-4 pt-32 pb-12">
        <div className="bg-white rounded-2xl p-8 border border-gray-100 shadow-sm">
          <h1 className="text-3xl font-bold text-[#1e3a5f] mb-8">Datenschutzerklärung</h1>
          
          <div className="prose max-w-none space-y-6 text-gray-600">
            
            {/* 1. Verantwortlicher */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">1. Verantwortlicher</h2>
              <p>
                Verantwortlicher im Sinne der Datenschutz-Grundverordnung (DSGVO) ist:
              </p>
              <p className="mt-2">
                <strong className="text-[#1e3a5f]">Home Invest & Management GmbH</strong><br />
                Zur Maate 19<br />
                31515 Wunstorf<br />
                Deutschland
              </p>
              <p className="mt-2">
                E-Mail: <a href="mailto:datenschutz@domulex.ai" className="text-[#b8860b] hover:text-[#9a7209]">datenschutz@domulex.ai</a>
              </p>
            </section>

            {/* 2. Überblick */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">2. Überblick der Verarbeitungen</h2>
              <p>
                Die nachfolgende Übersicht fasst die Arten der verarbeiteten Daten und die Zwecke ihrer 
                Verarbeitung zusammen und verweist auf die betroffenen Personen.
              </p>
              <h3 className="text-lg font-medium text-[#1e3a5f] mt-4 mb-2">Arten der verarbeiteten Daten</h3>
              <ul className="list-disc list-inside space-y-1">
                <li>Bestandsdaten (z.B. Namen, Adressen)</li>
                <li>Kontaktdaten (z.B. E-Mail, Telefonnummern)</li>
                <li>Inhaltsdaten (z.B. Eingaben in der KI-Chat-Funktion)</li>
                <li>Nutzungsdaten (z.B. besuchte Seiten, Interesse an Inhalten)</li>
                <li>Meta-/Kommunikationsdaten (z.B. Geräte-Informationen, IP-Adressen)</li>
                <li>Vertragsdaten (z.B. Vertragsgegenstand, Laufzeit, Abonnement-Status)</li>
                <li>Zahlungsdaten (z.B. Bankverbindungen, Zahlungshistorie via Stripe)</li>
                <li>Objektverwaltungsdaten (z.B. Immobiliendaten, Mieter, Zählerstände, Handwerker-Kontakte)</li>
              </ul>
              
              <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h4 className="font-semibold text-blue-800 mb-2">📊 Objektverwaltung (Professional-Tarif)</h4>
                <p className="text-sm text-blue-700 mb-2">
                  Im Rahmen der Objektverwaltung können Sie folgende Daten erfassen:
                </p>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• <strong>Mahnwesen:</strong> Offene Forderungen, Mahnstufen, Zahlungseingänge</li>
                  <li>• <strong>Zählerstände:</strong> Strom, Gas, Wasser, Heizung, Allgemeinzähler</li>
                  <li>• <strong>WEG-Beschlüsse:</strong> Protokolle, Beschlusstexte, Umsetzungsstatus</li>
                  <li>• <strong>Handwerker-Kontakte:</strong> Firmenname, Ansprechpartner, Kontaktdaten</li>
                  <li>• <strong>Mieterhöhungen:</strong> Aktuelle Miete, Index/Mietspiegel-Berechnungen</li>
                </ul>
                <p className="text-sm text-blue-700 mt-2">
                  Diese Daten werden ausschließlich in Ihrem Firebase-Konto (Firestore) gespeichert und 
                  sind nur für Sie zugänglich. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung).
                </p>
              </div>
            </section>

            {/* 3. Rechtsgrundlagen */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">3. Rechtsgrundlagen der Verarbeitung</h2>
              <p>
                Im Folgenden erhalten Sie eine Übersicht der Rechtsgrundlagen der DSGVO, auf deren Basis 
                wir personenbezogene Daten verarbeiten:
              </p>
              <ul className="list-disc list-inside space-y-2 mt-3">
                <li><strong className="text-[#1e3a5f]">Einwilligung (Art. 6 Abs. 1 lit. a DSGVO)</strong> – Die betroffene Person hat ihre Einwilligung in die Verarbeitung gegeben.</li>
                <li><strong className="text-[#1e3a5f]">Vertragserfüllung (Art. 6 Abs. 1 lit. b DSGVO)</strong> – Die Verarbeitung ist für die Erfüllung des Nutzungsvertrags erforderlich.</li>
                <li><strong className="text-[#1e3a5f]">Rechtliche Verpflichtung (Art. 6 Abs. 1 lit. c DSGVO)</strong> – Die Verarbeitung ist zur Erfüllung einer rechtlichen Verpflichtung erforderlich.</li>
                <li><strong className="text-[#1e3a5f]">Berechtigte Interessen (Art. 6 Abs. 1 lit. f DSGVO)</strong> – Die Verarbeitung ist zur Wahrung unserer berechtigten Interessen erforderlich.</li>
              </ul>
            </section>

            {/* 4. Datenübermittlung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">4. Datenübermittlung in Drittländer</h2>
              <p>
                Im Rahmen unserer Datenverarbeitung werden Daten auch an Dienste in Drittländern 
                (Länder außerhalb der EU/EWR) übermittelt. Dies geschieht auf Grundlage folgender 
                Garantien:
              </p>
              
              <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <h3 className="text-lg font-medium text-[#1e3a5f] mb-3">Dienste und Drittland-Übermittlungen</h3>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-300">
                      <th className="text-left py-2 text-[#1e3a5f]">Dienst</th>
                      <th className="text-left py-2 text-[#1e3a5f]">Anbieter</th>
                      <th className="text-left py-2 text-[#1e3a5f]">Land</th>
                      <th className="text-left py-2 text-[#1e3a5f]">Garantie</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    <tr>
                      <td className="py-2">Firebase/Google Cloud</td>
                      <td className="py-2">Google LLC</td>
                      <td className="py-2">USA</td>
                      <td className="py-2">EU-U.S. DPF</td>
                    </tr>
                    <tr>
                      <td className="py-2">Google Gemini API</td>
                      <td className="py-2">Google LLC</td>
                      <td className="py-2">USA</td>
                      <td className="py-2">EU-U.S. DPF</td>
                    </tr>
                    <tr>
                      <td className="py-2">Stripe</td>
                      <td className="py-2">Stripe, Inc.</td>
                      <td className="py-2">USA</td>
                      <td className="py-2">EU-U.S. DPF</td>
                    </tr>
                    <tr>
                      <td className="py-2">Qdrant Cloud</td>
                      <td className="py-2">Qdrant Solutions GmbH</td>
                      <td className="py-2">Deutschland</td>
                      <td className="py-2">EU (kein Drittland)</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <p className="mt-4">
                <strong className="text-[#1e3a5f]">EU-U.S. Data Privacy Framework (DPF):</strong> Die US-Anbieter sind 
                unter dem EU-U.S. Data Privacy Framework zertifiziert, welches ein angemessenes Datenschutzniveau 
                gemäß Art. 45 DSGVO gewährleistet.
              </p>
            </section>

            {/* 5. Hosting */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">5. Hosting und Serverinfrastruktur</h2>
              <p>
                Wir nutzen die folgenden Hosting-Dienste zur Bereitstellung unserer Plattform:
              </p>
              
              <h3 className="text-lg font-medium text-[#1e3a5f] mt-4 mb-2">Firebase Hosting & Cloud Functions</h3>
              <p>
                <strong className="text-[#1e3a5f]">Anbieter:</strong> Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland<br />
                <strong className="text-[#1e3a5f]">Zweck:</strong> Hosting der Website und Bereitstellung der Backend-Funktionen<br />
                <strong className="text-[#1e3a5f]">Datenschutz:</strong> <a href="https://firebase.google.com/support/privacy" target="_blank" rel="noopener noreferrer" className="text-[#b8860b] hover:text-[#9a7209]">https://firebase.google.com/support/privacy</a>
              </p>
              
              <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
                <h4 className="font-semibold text-green-800 mb-2">🔒 Google Cloud Zertifizierungen</h4>
                <p className="text-sm text-green-700 mb-3">
                  Unsere Infrastruktur läuft auf Google Cloud / Firebase – einer der sichersten Cloud-Plattformen weltweit mit folgenden Zertifizierungen:
                </p>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>✓ <strong>ISO 27001</strong> – Informationssicherheits-Management</li>
                  <li>✓ <strong>ISO 27017</strong> – Cloud-spezifische Sicherheitskontrollen</li>
                  <li>✓ <strong>ISO 27018</strong> – Schutz personenbezogener Daten in der Cloud</li>
                  <li>✓ <strong>SOC 1, SOC 2, SOC 3</strong> – Unabhängige Audit-Berichte</li>
                  <li>✓ <strong>C5-Testat (BSI)</strong> – Cloud-Sicherheit nach deutschem Standard</li>
                  <li>✓ <strong>EU-Standardvertragsklauseln</strong> – DSGVO-konforme Datenverarbeitung</li>
                </ul>
                <p className="text-sm text-green-700 mt-3">
                  <a href="https://cloud.google.com/security/compliance" target="_blank" rel="noopener noreferrer" className="underline">
                    → Alle Google Cloud Zertifizierungen einsehen
                  </a>
                </p>
              </div>

              <h3 className="text-lg font-medium text-[#1e3a5f] mt-4 mb-2">Qdrant Cloud (Vektor-Datenbank)</h3>
              <p>
                <strong className="text-[#1e3a5f]">Anbieter:</strong> Qdrant Solutions GmbH, Berlin, Deutschland<br />
                <strong className="text-[#1e3a5f]">Zweck:</strong> Speicherung und Suche von Rechtsdokumenten für die KI-Funktion<br />
                <strong className="text-[#1e3a5f]">Serverstandort:</strong> Frankfurt am Main, Deutschland (EU)
              </p>
            </section>

            {/* 6. KI-Verarbeitung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">6. KI-gestützte Datenverarbeitung</h2>
              <p>
                domulex.ai nutzt künstliche Intelligenz zur Beantwortung von Fragen zum Immobilienrecht.
              </p>
              
              <h3 className="text-lg font-medium text-[#1e3a5f] mt-4 mb-2">Google Gemini API</h3>
              <p>
                <strong className="text-[#1e3a5f]">Anbieter:</strong> Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA<br />
                <strong className="text-[#1e3a5f]">Zweck:</strong> KI-basierte Verarbeitung und Beantwortung von Benutzeranfragen<br />
                <strong className="text-[#1e3a5f]">Verarbeitete Daten:</strong> Ihre Chat-Eingaben werden zur Generierung von Antworten an die API übermittelt
              </p>
              
              <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <p className="text-amber-800">
                  <strong>Wichtiger Hinweis:</strong> Bitte geben Sie keine sensiblen personenbezogenen Daten 
                  (z.B. vollständige Namen, Adressen, Kontonummern) in den Chat ein. Die KI-generierten 
                  Antworten stellen keine Rechtsberatung dar.
                </p>
              </div>
            </section>

            {/* 7. Registrierung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">7. Registrierung und Benutzerkonto</h2>
              <p>
                Nutzer können ein Benutzerkonto anlegen. Im Rahmen der Registrierung werden folgende 
                Daten erhoben:
              </p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>E-Mail-Adresse</li>
                <li>Passwort (verschlüsselt gespeichert)</li>
                <li>Optional: Name, Unternehmen</li>
              </ul>
              <p className="mt-3">
                <strong className="text-[#1e3a5f]">Authentifizierung:</strong> Wir nutzen Firebase Authentication 
                von Google. Die Daten werden gemäß den Firebase-Datenschutzrichtlinien verarbeitet.
              </p>
            </section>

            {/* 8. Zahlungsabwicklung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">8. Zahlungsabwicklung</h2>
              <p>
                Für kostenpflichtige Abonnements nutzen wir den Zahlungsdienstleister Stripe:
              </p>
              <p className="mt-2">
                <strong className="text-[#1e3a5f]">Anbieter:</strong> Stripe, Inc., 354 Oyster Point Blvd, South San Francisco, CA 94080, USA<br />
                <strong className="text-[#1e3a5f]">Datenschutz:</strong> <a href="https://stripe.com/de/privacy" target="_blank" rel="noopener noreferrer" className="text-[#b8860b] hover:text-[#9a7209]">https://stripe.com/de/privacy</a>
              </p>
              <p className="mt-3">
                Stripe verarbeitet Ihre Zahlungsdaten direkt. Wir erhalten keine vollständigen 
                Kreditkartennummern, sondern nur Informationen über den Zahlungsstatus.
              </p>
            </section>

            {/* 9. Support */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">9. Hilfe & Support</h2>
              <p>
                Unser Support-System arbeitet in zwei Stufen:
              </p>
              <ul className="list-disc list-inside space-y-2 mt-2">
                <li><strong className="text-[#1e3a5f]">KI-gestützter Support:</strong> Einfache Fragen werden zunächst von einem KI-Agenten beantwortet.</li>
                <li><strong className="text-[#1e3a5f]">Menschlicher Support:</strong> Bei komplexeren Anfragen wird Ihre Nachricht an unser Support-Team weitergeleitet.</li>
              </ul>
              <p className="mt-3">
                Support-Anfragen werden für max. 2 Jahre gespeichert und anschließend gelöscht.
              </p>
            </section>

            {/* 10. Cookies */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">10. Cookies und Speichertechnologien</h2>
              <p>
                Wir setzen Cookies und vergleichbare Technologien ein:
              </p>
              
              <h3 className="text-lg font-medium text-[#1e3a5f] mt-4 mb-2">Notwendige Cookies</h3>
              <p>
                Diese Cookies sind für den Betrieb der Website erforderlich (z.B. Session-Cookies für 
                die Anmeldung). Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO.
              </p>

              <h3 className="text-lg font-medium text-[#1e3a5f] mt-4 mb-2">Analyse-Cookies (mit Einwilligung)</h3>
              <p>
                Mit Ihrer Einwilligung setzen wir ggf. Analyse-Cookies ein, um die Nutzung unserer 
                Website zu verstehen und zu verbessern.
              </p>
            </section>

            {/* 11. Speicherdauer */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">11. Speicherdauer</h2>
              <p>
                Wir speichern Ihre Daten nur so lange, wie es für die Zwecke erforderlich ist:
              </p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li><strong className="text-[#1e3a5f]">Chat-Verläufe:</strong> 30 Tage nach letzter Aktivität</li>
                <li><strong className="text-[#1e3a5f]">Kontodaten:</strong> Bis zur Löschung des Kontos + gesetzliche Aufbewahrungsfristen</li>
                <li><strong className="text-[#1e3a5f]">Rechnungsdaten:</strong> 10 Jahre (gesetzliche Aufbewahrungspflicht)</li>
                <li><strong className="text-[#1e3a5f]">Support-Anfragen:</strong> 2 Jahre</li>
              </ul>
            </section>

            {/* 12. Betroffenenrechte */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">12. Ihre Rechte</h2>
              <p>
                Sie haben folgende Rechte bezüglich Ihrer personenbezogenen Daten:
              </p>
              <ul className="list-disc list-inside space-y-2 mt-3">
                <li><strong className="text-[#1e3a5f]">Auskunftsrecht (Art. 15 DSGVO):</strong> Sie können Auskunft über Ihre gespeicherten Daten verlangen.</li>
                <li><strong className="text-[#1e3a5f]">Berichtigungsrecht (Art. 16 DSGVO):</strong> Sie können die Berichtigung unrichtiger Daten verlangen.</li>
                <li><strong className="text-[#1e3a5f]">Löschungsrecht (Art. 17 DSGVO):</strong> Sie können die Löschung Ihrer Daten verlangen.</li>
                <li><strong className="text-[#1e3a5f]">Einschränkung (Art. 18 DSGVO):</strong> Sie können die Einschränkung der Verarbeitung verlangen.</li>
                <li><strong className="text-[#1e3a5f]">Datenübertragbarkeit (Art. 20 DSGVO):</strong> Sie können Ihre Daten in einem gängigen Format erhalten.</li>
                <li><strong className="text-[#1e3a5f]">Widerspruchsrecht (Art. 21 DSGVO):</strong> Sie können der Verarbeitung widersprechen.</li>
                <li><strong className="text-[#1e3a5f]">Widerruf der Einwilligung:</strong> Sie können erteilte Einwilligungen jederzeit widerrufen.</li>
              </ul>
              <p className="mt-4">
                Zur Ausübung Ihrer Rechte wenden Sie sich an: 
                <a href="mailto:datenschutz@domulex.ai" className="text-[#b8860b] hover:text-[#9a7209] ml-1">datenschutz@domulex.ai</a>
              </p>
            </section>

            {/* 13. Beschwerderecht */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">13. Beschwerderecht bei der Aufsichtsbehörde</h2>
              <p>
                Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. 
                Die für uns zuständige Aufsichtsbehörde ist:
              </p>
              <p className="mt-2">
                <strong className="text-[#1e3a5f]">Die Landesbeauftragte für den Datenschutz Niedersachsen</strong><br />
                Prinzenstraße 5<br />
                30159 Hannover<br />
                Telefon: 0511 120-4500<br />
                E-Mail: poststelle@lfd.niedersachsen.de
              </p>
            </section>

            {/* 14. Änderungen */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">14. Änderungen dieser Datenschutzerklärung</h2>
              <p>
                Wir behalten uns vor, diese Datenschutzerklärung anzupassen, damit sie stets den 
                aktuellen rechtlichen Anforderungen entspricht oder um Änderungen unserer Leistungen 
                umzusetzen. Die neue Datenschutzerklärung gilt dann für Ihren nächsten Besuch.
              </p>
            </section>

          </div>

          <div className="mt-8 pt-6 border-t border-gray-200 text-sm text-gray-500">
            Stand: Dezember 2025
          </div>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
