'use client';

import Link from 'next/link';
import Logo from '@/components/Logo';
import PremiumFooter from '@/components/PremiumFooter';

export default function NDAPage() {
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
          <h1 className="text-3xl font-bold text-[#1e3a5f] mb-2">Geheimhaltungsvereinbarung (NDA)</h1>
          <p className="text-gray-500 mb-8">Non-Disclosure Agreement für Geschäftskunden</p>
          
          <div className="prose prose-gray max-w-none">
            <p className="text-sm text-gray-500 mb-6">Stand: Januar 2026</p>

            <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 mb-8">
              <p className="text-sm text-gray-700">
                <strong>Hinweis:</strong> Diese Geheimhaltungsvereinbarung wird automatisch Bestandteil des Vertrags für gewerbliche Kunden (B2B), Kanzleien und Unternehmen.
              </p>
            </div>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 1 Vertragsparteien</h2>
            <p>Diese Geheimhaltungsvereinbarung (nachfolgend &quot;NDA&quot;) wird geschlossen zwischen:</p>
            <ul className="list-disc pl-6 space-y-2">
              <li>
                <strong>Home Invest &amp; Management GmbH</strong><br />
                (Betreiberin von domulex.ai, nachfolgend &quot;Anbieter&quot;)
              </li>
              <li>
                <strong>Dem gewerblichen Kunden</strong><br />
                (wie im Bestellprozess angegeben, nachfolgend &quot;Kunde&quot;)
              </li>
            </ul>
            <p className="mt-4">gemeinsam als &quot;Parteien&quot; bezeichnet.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 2 Gegenstand der Vereinbarung</h2>
            <p><strong>(1)</strong> Diese NDA regelt den Umgang mit vertraulichen Informationen, die im Rahmen der Nutzung der Plattform domulex.ai zwischen den Parteien ausgetauscht werden.</p>
            <p><strong>(2)</strong> Die Vereinbarung gilt gegenseitig: Beide Parteien können sowohl Offenleger als auch Empfänger vertraulicher Informationen sein.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 3 Definition vertraulicher Informationen</h2>
            <p><strong>(1)</strong> &quot;Vertrauliche Informationen&quot; umfassen alle Informationen, unabhängig von ihrer Form (schriftlich, mündlich, elektronisch), die:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Als &quot;vertraulich&quot; oder &quot;geheim&quot; gekennzeichnet sind, oder</li>
              <li>Ihrer Natur nach als vertraulich zu betrachten sind, oder</li>
              <li>Im geschäftlichen Kontext üblicherweise als vertraulich gelten</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Zu den vertraulichen Informationen zählen insbesondere:</p>
            <p className="font-semibold mt-4 mb-2">Seitens des Kunden:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Mandantendaten und -akten (bei Rechtsanwälten)</li>
              <li>Hochgeladene Verträge (Miet-, Kauf-, Gewerbemietverträge)</li>
              <li>Interne Geschäftsdokumente</li>
              <li>Korrespondenz und Schriftsätze</li>
              <li>Finanzielle Informationen</li>
              <li>Strategische Geschäftsinformationen</li>
            </ul>

            <p className="font-semibold mt-4 mb-2">Seitens des Anbieters:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Technische Implementierungsdetails der Plattform</li>
              <li>Proprietäre Algorithmen und KI-Modelle</li>
              <li>Geschäftsstrategien und Roadmaps</li>
              <li>Nicht-öffentliche Preis- und Konditionsmodelle</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 4 Ausnahmen von der Vertraulichkeit</h2>
            <p>Die Geheimhaltungspflicht gilt nicht für Informationen, die:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Zum Zeitpunkt der Offenlegung bereits öffentlich bekannt waren</li>
              <li>Nach der Offenlegung ohne Verschulden des Empfängers öffentlich wurden</li>
              <li>Dem Empfänger bereits vor der Offenlegung bekannt waren</li>
              <li>Von einem Dritten rechtmäßig ohne Geheimhaltungspflicht erhalten wurden</li>
              <li>Unabhängig vom Empfänger entwickelt wurden</li>
              <li>Aufgrund gesetzlicher Verpflichtung offengelegt werden müssen</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 5 Pflichten der Parteien</h2>
            <p><strong>(1)</strong> Jede Partei verpflichtet sich:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Vertrauliche Informationen streng geheim zu halten</li>
              <li>Diese nur für den vereinbarten Zweck zu verwenden</li>
              <li>Diese nicht an Dritte weiterzugeben ohne vorherige schriftliche Zustimmung</li>
              <li>Angemessene Schutzmaßnahmen zu ergreifen (mindestens wie für eigene vertrauliche Informationen)</li>
              <li>Den Zugang auf Mitarbeiter zu beschränken, die diese Informationen für ihre Tätigkeit benötigen</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Der Anbieter verpflichtet sich zusätzlich:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Hochgeladene Dokumente nicht für Trainingszwecke der KI zu verwenden</li>
              <li>Mandantendaten streng von anderen Kundendaten zu trennen</li>
              <li>Inhalte von Anfragen nicht an andere Kunden oder Dritte weiterzugeben</li>
              <li>Keine Analyse oder Auswertung von Kundendaten zu kommerziellen Zwecken durchzuführen</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 6 Zulässige Offenlegung</h2>
            <p><strong>(1)</strong> Die Weitergabe an folgende Personen ist unter Wahrung der Geheimhaltungspflicht gestattet:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Mitarbeiter, die zur Geheimhaltung verpflichtet sind</li>
              <li>Beauftragte Dienstleister mit entsprechenden Vertraulichkeitsvereinbarungen</li>
              <li>Rechtliche und steuerliche Berater unter Berufsgeheimnis</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Bei gesetzlich zwingender Offenlegung (z.B. Gerichtsbeschluss, behördliche Anordnung) ist die andere Partei unverzüglich zu informieren, soweit rechtlich zulässig.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 7 Technische Schutzmaßnahmen des Anbieters</h2>
            <p>Zum Schutz vertraulicher Informationen hat der Anbieter folgende Maßnahmen implementiert:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li><strong>Verschlüsselung:</strong> TLS 1.3 für Übertragung, AES-256 für Speicherung</li>
              <li><strong>Zugriffskontrolle:</strong> Rollenbasiert, Multi-Faktor-Authentifizierung</li>
              <li><strong>Logging:</strong> Vollständige Audit-Protokolle aller Zugriffe</li>
              <li><strong>Serverstandort:</strong> Ausschließlich in Deutschland (Frankfurt am Main)</li>
              <li><strong>Zero Data Retention:</strong> Bei KI-Verarbeitung keine dauerhafte Speicherung durch Google</li>
              <li><strong>Regelmäßige Sicherheitsaudits:</strong> Penetrationstests und Schwachstellenanalysen</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 8 Berufsgeheimnisträger (§ 203 StGB)</h2>
            <p><strong>(1)</strong> Für Kunden, die Berufsgeheimnisträger gemäß § 203 StGB sind (insbesondere Rechtsanwälte), gelten besondere Schutzmaßnahmen.</p>
            <p><strong>(2)</strong> Der Anbieter ist sich der besonderen Vertraulichkeitsanforderungen bewusst und handelt als &quot;sonstige mitwirkende Person&quot; im Sinne des § 203 Abs. 3 StGB.</p>
            <p><strong>(3)</strong> Alle Mitarbeiter des Anbieters mit Zugang zu Mandantendaten sind gesondert zur Verschwiegenheit verpflichtet.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 9 Rückgabe und Löschung</h2>
            <p><strong>(1)</strong> Auf Verlangen oder bei Beendigung der Geschäftsbeziehung sind vertrauliche Informationen:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Zurückzugeben (in elektronischer Form) oder</li>
              <li>Unwiderruflich zu löschen</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Die Löschung ist schriftlich zu bestätigen.</p>
            <p><strong>(3)</strong> Ausnahmen gelten für gesetzliche Aufbewahrungspflichten und Backup-Systeme mit automatischer Löschung.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 10 Dauer der Vereinbarung</h2>
            <p><strong>(1)</strong> Diese NDA tritt mit Vertragsabschluss (Buchung eines Tarifs) in Kraft.</p>
            <p><strong>(2)</strong> Die Geheimhaltungspflichten bestehen:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Während der gesamten Vertragslaufzeit</li>
              <li><strong>Nach Vertragsende: 5 Jahre</strong> für allgemeine Geschäftsinformationen</li>
              <li><strong>Unbefristet</strong> für Mandantengeheimnisse und besonders sensible Daten</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 11 Vertragsstrafe</h2>
            <p><strong>(1)</strong> Bei schuldhafter Verletzung der Geheimhaltungspflichten kann die geschädigte Partei eine Vertragsstrafe verlangen:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Bei einfacher Fahrlässigkeit: bis zu 10.000 €</li>
              <li>Bei grober Fahrlässigkeit oder Vorsatz: bis zu 50.000 €</li>
            </ul>

            <p className="mt-4"><strong>(2)</strong> Die Geltendmachung weitergehender Schadensersatzansprüche bleibt unberührt.</p>
            <p><strong>(3)</strong> Die Vertragsstrafe wird auf etwaige Schadensersatzansprüche angerechnet.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 12 Rechtsbehelfe</h2>
            <p><strong>(1)</strong> Bei drohender oder erfolgter Verletzung dieser Vereinbarung ist die geschädigte Partei berechtigt, Unterlassungsansprüche geltend zu machen.</p>
            <p><strong>(2)</strong> Im Fall einer drohenden oder erfolgten Verletzung durch den Anbieter kann der Kunde die sofortige Sperrung und Löschung seiner Daten verlangen.</p>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 13 Meldepflicht bei Sicherheitsvorfällen</h2>
            <p><strong>(1)</strong> Bei Kenntnisnahme eines tatsächlichen oder vermuteten Sicherheitsvorfalls, der vertrauliche Informationen betrifft, ist die andere Partei unverzüglich zu informieren.</p>
            <p><strong>(2)</strong> Die Information muss enthalten:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Art des Vorfalls</li>
              <li>Betroffene Informationen</li>
              <li>Ergriffene Gegenmaßnahmen</li>
              <li>Kontaktperson für Rückfragen</li>
            </ul>

            <h2 className="text-xl font-semibold text-[#1e3a5f] mt-8 mb-4">§ 14 Schlussbestimmungen</h2>
            <p><strong>(1)</strong> Änderungen und Ergänzungen dieser NDA bedürfen der Textform.</p>
            <p><strong>(2)</strong> Sollten einzelne Bestimmungen unwirksam sein, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.</p>
            <p><strong>(3)</strong> Es gilt deutsches Recht.</p>
            <p><strong>(4)</strong> Gerichtsstand für alle Streitigkeiten aus dieser Vereinbarung ist Frankfurt am Main.</p>
            <p><strong>(5)</strong> Diese NDA wird automatisch Bestandteil des Nutzungsvertrags bei Buchung durch gewerbliche Kunden.</p>

            <div className="mt-12 p-6 bg-amber-50 border border-amber-100 rounded-xl">
              <h3 className="font-semibold text-[#1e3a5f] mb-4">🔒 Automatische Geltung für B2B-Kunden</h3>
              <p className="text-gray-700 text-sm">
                Mit Abschluss eines Tarifs (Starter, Profi oder Lawyer Pro) als gewerblicher Kunde, Freiberufler oder Unternehmen wird diese Geheimhaltungsvereinbarung automatisch Bestandteil des Vertrags. Eine separate Unterzeichnung ist nicht erforderlich. Die Zustimmung erfolgt im Rahmen des Checkout-Prozesses.
              </p>
            </div>

            <div className="mt-8 p-6 bg-gray-50 rounded-xl">
              <h3 className="font-semibold text-[#1e3a5f] mb-4">Kontakt</h3>
              <p className="text-gray-600">
                Home Invest &amp; Management GmbH<br />
                Rechtsabteilung<br />
                E-Mail: <a href="mailto:legal@domulex.ai" className="text-[#b8860b]">legal@domulex.ai</a>
              </p>
            </div>
          </div>
        </div>

        {/* Download Button */}
        <div className="mt-8 text-center">
          <a 
            href="/downloads/nda.pdf" 
            className="inline-flex items-center gap-2 px-6 py-3 bg-[#1e3a5f] hover:bg-[#2d4a6f] text-white rounded-xl font-medium transition-colors"
          >
            📄 NDA als PDF herunterladen
          </a>
        </div>
      </main>

      <PremiumFooter />
    </div>
  );
}
