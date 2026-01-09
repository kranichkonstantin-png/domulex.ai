'use client';

import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';

export default function AGBPage() {
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
          <h1 className="text-3xl font-bold text-[#1e3a5f] mb-8">Allgemeine Geschäftsbedingungen (AGB)</h1>
          
          <div className="prose max-w-none space-y-6 text-gray-600">
            
            {/* § 1 Geltungsbereich */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 1 Geltungsbereich und Vertragspartner</h2>
              <p>
                (1) Diese Allgemeinen Geschäftsbedingungen (nachfolgend „AGB") gelten für die Nutzung 
                der Plattform domulex.ai, betrieben von:
              </p>
              <p className="mt-2">
                <strong className="text-[#1e3a5f]">Home Invest & Management GmbH</strong><br />
                Zur Maate 19<br />
                31515 Wunstorf<br />
                Handelsregister: AG Hannover, HRB 220181<br />
                (nachfolgend „Anbieter")
              </p>
              <p className="mt-3">
                (2) Diese AGB gelten für alle Verträge, die zwischen dem Anbieter und dem Nutzer 
                über die Plattform domulex.ai geschlossen werden.
              </p>
              <p className="mt-2">
                (3) Abweichende Bedingungen des Nutzers werden nicht anerkannt, es sei denn, der 
                Anbieter stimmt ihrer Geltung ausdrücklich schriftlich zu.
              </p>
            </section>

            {/* § 2 Leistungsbeschreibung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 2 Leistungsbeschreibung</h2>
              <p>
                (1) domulex.ai ist eine KI-gestützte Informationsplattform für Immobilienrecht 
                einschließlich Immobilien-Steuerrecht. Die Plattform bietet:
              </p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>KI-Chat zur Beantwortung von Fragen zum deutschen Immobilienrecht</li>
                <li>Steuerrechtliche Informationen (AfA, Grunderwerbsteuer, Spekulationsfrist, Werbungskosten)</li>
                <li>Zugang zu einer Datenbank mit Rechtstexten (BGB, WEG, BauGB, EStG, BFH-Urteile etc.)</li>
                <li>Vertragsanalyse-Funktionen (je nach Tarif)</li>
                <li>Fallanalyse mit Erfolgsaussichten-Prognose (je nach Tarif)</li>
                <li>Rechtsprechungsanalyse mit Urteilssuche (je nach Tarif)</li>
                <li>Erstellung eigener Vorlagen mit KI-Unterstützung</li>
                <li>Speicherung und Wiederverwendung eigener Dokumente</li>
              </ul>
              
              <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <p className="text-amber-800">
                  <strong>WICHTIGER HINWEIS:</strong> Die von domulex.ai bereitgestellten Informationen 
                  stellen <strong>KEINE RECHTS- ODER STEUERBERATUNG</strong> dar. Die KI-generierten 
                  Antworten dienen ausschließlich zu allgemeinen Informationszwecken. Für verbindliche 
                  rechtliche oder steuerliche Beurteilungen wenden Sie sich bitte an einen zugelassenen 
                  Rechtsanwalt oder Steuerberater.
                </p>
              </div>
              
              <p className="mt-4">
                (2) Der Anbieter ist berechtigt, den Funktionsumfang der Plattform jederzeit zu 
                erweitern, anzupassen oder einzuschränken, soweit dies dem Nutzer zumutbar ist.
              </p>
            </section>

            {/* § 3 Vertragsschluss */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 3 Vertragsschluss und Registrierung</h2>
              <p>
                (1) Die Nutzung der Plattform setzt eine Registrierung voraus. Mit der Registrierung 
                gibt der Nutzer ein Angebot auf Abschluss eines Nutzungsvertrages ab.
              </p>
              <p className="mt-2">
                (2) Der Vertrag kommt zustande, wenn der Anbieter die Registrierung durch eine 
                Bestätigungs-E-Mail oder durch Freischaltung des Nutzerkontos annimmt.
              </p>
              <p className="mt-2">
                (3) Der Nutzer versichert, dass alle bei der Registrierung angegebenen Daten 
                wahrheitsgemäß und vollständig sind.
              </p>
              <p className="mt-2">
                (4) Die Registrierung ist nur volljährigen, unbeschränkt geschäftsfähigen natürlichen 
                Personen oder juristischen Personen gestattet.
              </p>
            </section>

            {/* § 4 Tarife und Preise */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 4 Tarife und Preise</h2>
              <p>
                (1) Die Plattform bietet verschiedene Tarife an:
              </p>
              
              <div className="mt-4 space-y-3">
                <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
                  <h3 className="font-semibold text-[#1e3a5f]">Test-Tarif (Kostenlos)</h3>
                  <p className="text-sm mt-1">3 KI-Anfragen insgesamt zum Testen. Nach 6 Monaten ohne Upgrade wird das Konto automatisch gelöscht.</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <h3 className="font-semibold text-[#1e3a5f]">Basis (19€/Monat)</h3>
                  <p className="text-sm mt-1">25 KI-Anfragen pro Monat, 5.000 Rechtsquellen, Quellenangaben, Chat-Historie, eigene Vorlagen erstellen</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <h3 className="font-semibold text-[#1e3a5f]">Professional (39€/Monat)</h3>
                  <p className="text-sm mt-1">250 Anfragen pro Monat, 50.000+ Rechtsquellen, Vertragsanalyse, Nebenkostenabrechnung, Renditerechner, Baurecht-Assistent, Mahnwesen, Zählerstandserfassung, WEG-Beschlussbuch, Handwerker-Kontakte, Mieterhöhung-Rechner</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <h3 className="font-semibold text-[#1e3a5f]">Lawyer Pro (69€/Monat)</h3>
                  <p className="text-sm mt-1">Unbegrenzte Anfragen (Fair-Use: 2.000/Monat), 50.000+ Rechtsquellen, CRM-Features, Fallanalyse, Rechtsprechungsanalyse, Schriftsatzgenerator, Fristenverwaltung, Dokumentenmanagement</p>
                  <p className="text-xs text-gray-500 mt-2">„Unbegrenzt" bedeutet ein Fair-Use-Kontingent von 2.000 Anfragen pro Monat, das für die Einzelnutzung ausreichend ist. Account-Sharing ist untersagt.</p>
                </div>
              </div>
              
              <p className="mt-4">
                (2) Die aktuellen Preise sind auf der Website einsehbar. Alle Preise verstehen sich 
                inklusive der gesetzlichen Mehrwertsteuer.
              </p>
              <p className="mt-2">
                (3) Der Anbieter behält sich das Recht vor, Preise anzupassen. Preiserhöhungen 
                werden dem Nutzer mindestens 30 Tage vor Inkrafttreten per E-Mail mitgeteilt.
              </p>
            </section>

            {/* § 5 Zahlung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 5 Zahlung und Abrechnung</h2>
              <p>
                (1) Die Zahlung erfolgt über den Zahlungsdienstleister Stripe. Es werden folgende 
                Zahlungsmethoden akzeptiert:
              </p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Kreditkarte (Visa, Mastercard, American Express)</li>
                <li>SEPA-Lastschrift</li>
                <li>Weitere über Stripe verfügbare Zahlungsmethoden</li>
              </ul>
              <p className="mt-3">
                (2) Bei Abonnements erfolgt die Abrechnung monatlich oder jährlich im Voraus, 
                je nach gewähltem Zahlungsintervall.
              </p>
              <p className="mt-2">
                (3) Bei Zahlungsverzug ist der Anbieter berechtigt, den Zugang zur Plattform 
                zu sperren und Verzugszinsen in gesetzlicher Höhe zu berechnen.
              </p>
            </section>

            {/* § 6 Laufzeit und Kündigung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 6 Laufzeit und Kündigung</h2>
              <p>
                (1) Kostenpflichtige Abonnements haben eine Mindestlaufzeit von einem Monat 
                (bei monatlicher Zahlung) bzw. einem Jahr (bei jährlicher Zahlung).
              </p>
              <p className="mt-2">
                (2) Das Abonnement verlängert sich automatisch um die jeweilige Laufzeit, wenn 
                es nicht vor Ablauf gekündigt wird.
              </p>
              <p className="mt-2">
                (3) Die Kündigung kann jederzeit mit Wirkung zum Ende der aktuellen Abrechnungsperiode 
                erfolgen. Die Kündigung kann über das Nutzerkonto oder per E-Mail an kontakt@domulex.ai 
                erfolgen.
              </p>
              <p className="mt-2">
                (4) Das Recht zur außerordentlichen Kündigung aus wichtigem Grund bleibt unberührt.
              </p>
            </section>

            {/* § 7 Widerrufsrecht */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 7 Widerrufsrecht</h2>
              
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg mb-4">
                <p className="text-green-800 text-sm">
                  <strong>✅ Besonderer Vorteil:</strong> Bei domulex.ai gewähren wir <strong>allen Kunden</strong> – 
                  sowohl Verbrauchern als auch gewerblichen Nutzern – ein freiwilliges 14-tägiges Widerrufsrecht. 
                  Dies geht über die gesetzlichen Anforderungen hinaus, da Unternehmer gemäß § 14 BGB 
                  normalerweise kein gesetzliches Widerrufsrecht haben.
                </p>
              </div>
              
              <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <h3 className="font-semibold text-[#1e3a5f] mb-3 text-lg">Widerrufsbelehrung</h3>
                
                <p><strong className="text-[#1e3a5f]">Widerrufsrecht</strong></p>
                <p className="mt-2">
                  Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen Vertrag 
                  zu widerrufen.
                </p>
                <p className="mt-2">
                  Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag des Vertragsschlusses.
                </p>
                
                <p className="mt-3">
                  Um Ihr Widerrufsrecht auszuüben, müssen Sie uns
                </p>
                <div className="mt-2 p-3 bg-gray-100 rounded">
                  <p>
                    <strong className="text-[#1e3a5f]">Home Invest & Management GmbH</strong><br />
                    Zur Maate 19<br />
                    31515 Wunstorf<br />
                    Deutschland<br /><br />
                    E-Mail: <a href="mailto:kontakt@domulex.ai" className="text-[#b8860b]">kontakt@domulex.ai</a>
                  </p>
                </div>
                <p className="mt-3">
                  mittels einer eindeutigen Erklärung (z.B. ein mit der Post versandter Brief, Telefax 
                  oder E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren. Sie 
                  können dafür das beigefügte Muster-Widerrufsformular verwenden, das jedoch nicht 
                  vorgeschrieben ist.
                </p>
                <p className="mt-2">
                  Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die 
                  Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.
                </p>
                
                <p className="mt-4"><strong className="text-[#1e3a5f]">Folgen des Widerrufs</strong></p>
                <p className="mt-2">
                  Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir von 
                  Ihnen erhalten haben, einschließlich der Lieferkosten (mit Ausnahme der zusätzlichen 
                  Kosten, die sich daraus ergeben, dass Sie eine andere Art der Lieferung als die von 
                  uns angebotene, günstigste Standardlieferung gewählt haben), unverzüglich und 
                  spätestens binnen vierzehn Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung 
                  über Ihren Widerruf dieses Vertrags bei uns eingegangen ist.
                </p>
                <p className="mt-2">
                  Für diese Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der 
                  ursprünglichen Transaktion eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich 
                  etwas anderes vereinbart; in keinem Fall werden Ihnen wegen dieser Rückzahlung 
                  Entgelte berechnet.
                </p>
                
                <p className="mt-4"><strong className="text-[#1e3a5f]">Besonderer Hinweis zum vorzeitigen Erlöschen des Widerrufsrechts</strong></p>
                <p className="mt-2">
                  Haben Sie verlangt, dass die Dienstleistungen während der Widerrufsfrist beginnen 
                  sollen, so haben Sie uns einen angemessenen Betrag zu zahlen, der dem Anteil der 
                  bis zu dem Zeitpunkt, zu dem Sie uns von der Ausübung des Widerrufsrechts 
                  hinsichtlich dieses Vertrags unterrichten, bereits erbrachten Dienstleistungen im 
                  Vergleich zum Gesamtumfang der im Vertrag vorgesehenen Dienstleistungen entspricht.
                </p>
                <p className="mt-2">
                  Das Widerrufsrecht erlischt vorzeitig, wenn wir die Dienstleistung vollständig 
                  erbracht haben und mit der Ausführung der Dienstleistung erst begonnen haben, 
                  nachdem Sie dazu Ihre ausdrückliche Zustimmung gegeben haben und gleichzeitig 
                  Ihre Kenntnis davon bestätigt haben, dass Sie Ihr Widerrufsrecht bei vollständiger 
                  Vertragserfüllung durch uns verlieren.
                </p>
              </div>
              
              {/* Muster-Widerrufsformular */}
              <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <h3 className="font-semibold text-[#1e3a5f] mb-3 text-lg">Muster-Widerrufsformular</h3>
                <p className="text-sm text-gray-500 mb-4">
                  (Wenn Sie den Vertrag widerrufen wollen, dann füllen Sie bitte dieses Formular aus 
                  und senden Sie es zurück.)
                </p>
                
                <div className="p-4 bg-white rounded border border-gray-200 text-sm">
                  <p>An:</p>
                  <p className="mt-1">
                    Home Invest & Management GmbH<br />
                    Zur Maate 19<br />
                    31515 Wunstorf<br />
                    E-Mail: kontakt@domulex.ai
                  </p>
                  
                  <p className="mt-4">
                    Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen Vertrag 
                    über die Erbringung der folgenden Dienstleistung:
                  </p>
                  
                  <div className="mt-3 space-y-3">
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Dienstleistung:</span>
                      <span className="flex-1 border-b border-gray-300">domulex.ai Abonnement</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Bestellt am (*):</span>
                      <span className="flex-1 border-b border-gray-300"></span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Erhalten am (*):</span>
                      <span className="flex-1 border-b border-gray-300"></span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Name des/der Verbraucher(s):</span>
                      <span className="flex-1 border-b border-gray-300"></span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">Anschrift des/der Verbraucher(s):</span>
                      <span className="flex-1 border-b border-gray-300"></span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-500">E-Mail-Adresse:</span>
                      <span className="flex-1 border-b border-gray-300"></span>
                    </div>
                  </div>
                  
                  <p className="mt-6">
                    ___________________________________<br />
                    <span className="text-gray-500 text-xs">Datum, Unterschrift des/der Verbraucher(s) 
                    (nur bei Mitteilung auf Papier)</span>
                  </p>
                  
                  <p className="mt-4 text-gray-500 text-xs">
                    (*) Unzutreffendes streichen.
                  </p>
                </div>
                
                <p className="mt-4 text-sm text-gray-500">
                  Sie können das Widerrufsformular auch elektronisch per E-Mail an 
                  <a href="mailto:kontakt@domulex.ai" className="text-[#b8860b] ml-1">kontakt@domulex.ai</a> senden.
                </p>
              </div>
            </section>

            {/* § 8 Pflichten des Nutzers */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 8 Pflichten des Nutzers und Nutzungsbeschränkungen</h2>
              <p>
                (1) Der Nutzer verpflichtet sich:
              </p>
              <ul className="list-disc list-inside space-y-1 mt-2">
                <li>Die Plattform nur für rechtmäßige Zwecke zu nutzen</li>
                <li>Seine Zugangsdaten geheim zu halten und vor Zugriff Dritter zu schützen</li>
                <li>Keine Inhalte einzugeben, die rechtswidrig, beleidigend oder schädlich sind</li>
                <li>Die Plattform nicht zu manipulieren oder zu überlasten</li>
                <li>Keine automatisierten Abfragen (Bots, Scraper) ohne Genehmigung zu nutzen</li>
              </ul>
              
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800">
                  <strong>⚠️ WICHTIG - Einzelgerät-Nutzung:</strong> Jedes Nutzerkonto darf zu jedem 
                  Zeitpunkt <strong>nur auf EINEM Gerät gleichzeitig</strong> verwendet werden. Bei 
                  Anmeldung auf einem neuen Gerät werden alle anderen aktiven Sitzungen automatisch 
                  beendet. Die Weitergabe von Zugangsdaten an Dritte oder die gleichzeitige Nutzung 
                  auf mehreren Geräten durch verschiedene Personen ist ausdrücklich untersagt und 
                  stellt einen Verstoß gegen diese AGB dar. Der Anbieter ist berechtigt, bei 
                  wiederholten Verstößen das Nutzerkonto ohne Vorankündigung zu sperren.
                </p>
              </div>
              
              <p className="mt-3">
                (2) Bei Verdacht auf Missbrauch der Zugangsdaten ist der Nutzer verpflichtet, 
                den Anbieter unverzüglich zu informieren.
              </p>
              <p className="mt-2">
                (3) Bei Verstoß gegen diese Pflichten ist der Anbieter berechtigt, den Zugang 
                zur Plattform zu sperren und den Vertrag fristlos zu kündigen.
              </p>
              <p className="mt-2">
                (4) Die Nutzung der Plattform ist personengebunden. Jeder Nutzer benötigt ein 
                eigenes Konto. Die gemeinsame Nutzung eines Kontos durch mehrere Personen 
                (Account-Sharing) ist nicht gestattet und führt zur sofortigen Sperrung.
              </p>
            </section>

            {/* § 9 Haftung */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 9 Haftungsbeschränkung</h2>
              <p>
                (1) Der Anbieter haftet unbeschränkt für Schäden aus der Verletzung des Lebens, 
                des Körpers oder der Gesundheit sowie für Vorsatz und grobe Fahrlässigkeit.
              </p>
              <p className="mt-2">
                (2) Für leichte Fahrlässigkeit haftet der Anbieter nur bei Verletzung einer 
                wesentlichen Vertragspflicht (Kardinalpflicht). Die Haftung ist in diesem Fall 
                auf den vorhersehbaren, vertragstypischen Schaden begrenzt.
              </p>
              <p className="mt-2">
                (3) <strong className="text-[#1e3a5f]">Keine Haftung für KI-Inhalte:</strong> Der Anbieter übernimmt keine 
                Haftung für die Richtigkeit, Vollständigkeit oder Aktualität der von der KI 
                generierten Informationen. Die Nutzung der KI-Antworten erfolgt auf eigenes Risiko.
              </p>
              <p className="mt-2">
                (4) Der Anbieter haftet nicht für Schäden, die durch eine rechtliche Entscheidung 
                entstehen, die auf Grundlage der von der Plattform bereitgestellten Informationen 
                getroffen wurde.
              </p>
            </section>

            {/* § 10 Verfügbarkeit */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 10 Verfügbarkeit der Plattform</h2>
              <p>
                (1) Der Anbieter bemüht sich um eine hohe Verfügbarkeit der Plattform, garantiert 
                jedoch keine bestimmte Verfügbarkeit.
              </p>
              <p className="mt-2">
                (2) Der Anbieter ist berechtigt, die Plattform für Wartungsarbeiten, Updates oder 
                aus technischen Gründen vorübergehend einzuschränken oder zu unterbrechen.
              </p>
              <p className="mt-2">
                (3) Geplante Wartungsarbeiten werden nach Möglichkeit vorab angekündigt.
              </p>
            </section>

            {/* § 11 Urheberrecht */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 11 Geistiges Eigentum</h2>
              <p>
                (1) Alle Rechte an der Plattform, einschließlich Software, Design, Texte und 
                Datenbanken, verbleiben beim Anbieter.
              </p>
              <p className="mt-2">
                (2) Der Nutzer erhält ein einfaches, nicht übertragbares Nutzungsrecht für die 
                Dauer des Vertrages.
              </p>
              <p className="mt-2">
                (3) Die Vervielfältigung, Bearbeitung oder Weitergabe von Inhalten der Plattform 
                bedarf der vorherigen schriftlichen Zustimmung des Anbieters.
              </p>
            </section>

            {/* § 12 Datenschutz */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 12 Datenschutz</h2>
              <p>
                Die Verarbeitung personenbezogener Daten erfolgt gemäß unserer 
                <Link href="/datenschutz" className="text-[#b8860b] hover:text-[#9a7209] ml-1">Datenschutzerklärung</Link>.
              </p>
            </section>

            {/* § 13 Änderungen */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 13 Änderungen der AGB</h2>
              <p>
                (1) Der Anbieter behält sich vor, diese AGB mit Wirkung für die Zukunft zu ändern.
              </p>
              <p className="mt-2">
                (2) Der Anbieter wird den Nutzer über Änderungen mindestens 30 Tage vor Inkrafttreten 
                per E-Mail informieren.
              </p>
              <p className="mt-2">
                (3) Widerspricht der Nutzer den Änderungen nicht innerhalb von 30 Tagen nach Zugang 
                der Änderungsmitteilung, gelten die geänderten AGB als angenommen.
              </p>
            </section>

            {/* § 14 Schlussbestimmungen */}
            <section>
              <h2 className="text-xl font-semibold text-[#1e3a5f] mb-3">§ 14 Schlussbestimmungen</h2>
              <p>
                (1) Es gilt das Recht der Bundesrepublik Deutschland unter Ausschluss des 
                UN-Kaufrechts.
              </p>
              <p className="mt-2">
                (2) Erfüllungsort und Gerichtsstand ist, soweit gesetzlich zulässig, der Sitz 
                des Anbieters (Wunstorf).
              </p>
              <p className="mt-2">
                (3) Sollten einzelne Bestimmungen dieser AGB unwirksam sein oder werden, bleibt 
                die Wirksamkeit der übrigen Bestimmungen unberührt.
              </p>
              <p className="mt-2">
                (4) Die Vertragssprache ist Deutsch.
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
