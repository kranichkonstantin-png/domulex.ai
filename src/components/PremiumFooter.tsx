import Link from 'next/link';

export default function PremiumFooter() {
  return (
    <footer className="bg-gradient-to-b from-[#0f1f2e] to-[#0a1520] py-16 px-4" role="contentinfo">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-5 gap-10 mb-10">
          <div>
            <div className="flex items-center mb-4">
              <span className="text-xl font-semibold"><span className="text-white">domulex</span><span className="text-[#b8860b]">.ai</span></span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              KI-gestützte Rechtsplattform für Immobilienrecht.
            </p>
          </div>
          <nav aria-label="Produkt-Navigation">
            <h4 className="font-semibold text-white mb-5">Produkt</h4>
            <ul className="space-y-3 text-gray-400 text-sm" role="list">
              <li><Link href="/funktionen" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Funktionen</Link></li>
              <li><Link href="/preise" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Preise</Link></li>
              <li><Link href="/auth/login" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Anmelden</Link></li>
            </ul>
          </nav>
          <nav aria-label="Medien-Navigation">
            <h4 className="font-semibold text-white mb-5">Medien</h4>
            <ul className="space-y-3 text-gray-400 text-sm" role="list">
              <li><Link href="/news" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">News</Link></li>
              <li><Link href="/presse" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Presse</Link></li>
              <li><Link href="/redaktion" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Redaktion</Link></li>
            </ul>
          </nav>
          <nav aria-label="Rechtliche Navigation">
            <h4 className="font-semibold text-white mb-5">Rechtliches</h4>
            <ul className="space-y-3 text-gray-400 text-sm" role="list">
              <li><Link href="/impressum" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Impressum</Link></li>
              <li><Link href="/datenschutz" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Datenschutz</Link></li>
              <li><Link href="/agb" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">AGB</Link></li>
              <li><Link href="/avv" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">AVV (B2B)</Link></li>
              <li><Link href="/nda" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">NDA (B2B)</Link></li>
            </ul>
          </nav>
          <nav aria-label="Support-Navigation">
            <h4 className="font-semibold text-white mb-5">Support</h4>
            <ul className="space-y-3 text-gray-400 text-sm" role="list">
              <li><Link href="/hilfe" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Hilfe</Link></li>
              <li><Link href="/faq" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">FAQ</Link></li>
              <li><Link href="/kuendigen" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">Abo kündigen</Link></li>
              <li><a href="mailto:kontakt@domulex.ai" className="hover:text-white transition-all duration-300 hover:translate-x-1 inline-block focus:outline-none focus:ring-2 focus:ring-[#b8860b] focus:ring-offset-2 focus:ring-offset-[#0f1f2e] rounded">kontakt@domulex.ai</a></li>
            </ul>
          </nav>
        </div>
        <div className="border-t border-gray-800/50 pt-10 text-center text-gray-500 text-sm">
          <p className="mb-4">© 2026 Home Invest & Management GmbH. Alle Rechte vorbehalten.</p>
          <p className="text-xs text-gray-600 max-w-2xl mx-auto leading-relaxed">
            <span className="text-white">domulex</span><span className="text-[#b8860b]">.ai</span> bietet KI-gestützte Rechtsanalysen auf Basis von 50.000+ Dokumenten. 
            Die Plattform ersetzt keine anwaltliche Beratung bei Gerichtsverfahren oder komplexen Rechtsstreitigkeiten.
          </p>
        </div>
      </div>
    </footer>
  );
}
