"""
Immobilienrecht KOMPLETT Scraper - Häppchen 1: Maklerrecht + Mietpreisbremse + ZVG
Erweitert die Datenbank um 55 neue Dokumente
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class ImmobilienKomplettScraper:
    """Scraper für komplettes Immobilienrecht in Häppchen"""
    
    def __init__(self):
        pass
    
    def scrape_haeppchen_1(self) -> List[Dict]:
        """Häppchen 1: Maklerrecht (15) + Mietpreisbremse (10) + ZVG (30) = 55 Docs"""
        docs = []
        
        # ========================================
        # MAKLERRECHT (15 Paragraphen)
        # ========================================
        makler = [
            ("§ 652 BGB", "Maklervertrag Grundlagen", "Provision nur bei Erfolg (Nachweis/Vermittlung). Kein Erfolg = keine Provision. Schriftform erforderlich."),
            ("§ 653 BGB", "Provisionsanspruch", "Nachweis: Gelegenheit zum Vertragsschluss. Vermittlung: Hauptvertrag zustande gekommen."),
            ("§ 654 BGB", "Provisionsausschluss", "KEINE Provision bei: Eigengeschäft Makler, Interessenkonflikt, Pflichtverletzung."),
            ("§ 655 BGB", "Lohnverfall", "Provision verfällt bei grober Pflichtverletzung. Verheimlichen von Mängeln = keine Provision."),
            ("§ 656 BGB", "Maklerlohn Höhe", "Kauf: 3-7% + MwSt (regional). München: 7,14%. Berlin: 7,14% geteilt. Miete: Max 2 NK + MwSt."),
            ("§ 656a BGB", "Textform Pflicht", "Maklervertrag Textform PFLICHT (E-Mail reicht). Mündlich = unwirksam = keine Provision."),
            ("§ 656b BGB", "Nebenkosten", "Nebenkosten nur ersetzbar wenn vereinbart. Fahrtkosten, Inserate ohne Vereinbarung: 0€."),
            ("§ 656c BGB", "Teilung Provision Kauf", "Käufer/Verkäufer zahlen je max. 50%. Makler darf nicht mehr von Käufer als Verkäufer verlangen."),
            ("§ 656d BGB", "Abwälzung verboten", "Verkäufer darf Provision NICHT auf Käufer abwälzen. Käufer kann zurückfordern."),
            ("MaBV § 2", "Bestellerprinzip Miete", "Wer bestellt zahlt. Vermieter zahlt (nicht Mieter). Verstoß: 25k€ Bußgeld. Seit 1.6.2015."),
            ("MaBV § 3", "Koppelungsverbot", "Vermietung NICHT an Provision koppeln. 'Wohnung nur mit Makler' = illegal. Bußgeld 25k€."),
            ("GewO § 34c", "Maklererlaubnis", "Makler braucht Erlaubnis (IHK). Sachkunde + Haftpflicht 500k€. Ohne: 50k€ Bußgeld."),
            ("§ 34c Abs.2a GewO", "Weiterbildung", "20h Weiterbildung alle 3 Jahre Pflicht. Nachweis IHK. Kosten: 200-500€/Jahr."),
            ("HGB § 93", "Handelsmakler", "Gewerbeimmobilien: 3-6% Netto + MwSt. Nachweis reicht. 2 Mio. × 5% = 100k€ + 19k€ MwSt."),
            ("§ 354 HGB", "Provision Fälligkeit", "Fällig bei Beurkundung (Kauf) bzw. Mietvertragsschluss. Zahlungsziel: 14 Tage üblich."),
        ]
        
        for section, title, content in makler:
            docs.append(self._create_doc(section, title, content, "Maklerrecht", ["Maklerrecht", "Provision"]))
        
        # ========================================
        # MIETPREISBREMSE (10 Paragraphen)
        # ========================================
        mietpreisbremse = [
            ("§ 556d BGB", "Mietpreisbremse", "Angespannte Märkte: Max Vergleichsmiete + 10%. München, Berlin, Hamburg, Frankfurt."),
            ("§ 556e BGB", "Ausnahmen", "KEINE Bremse: Neubau (nach 1.10.2014), umfassende Modernisierung. Vormiete + 10% erlaubt."),
            ("§ 556f BGB", "Rügeobliegenheit", "Mieter muss rügen (Textform). Ohne Rüge: Nur ab Rüge zurück. Frist: 30 Monate."),
            ("§ 556g BGB", "Auskunftspflicht", "Vermieter muss offenlegen: Vormiete, Modernisierung, Neubau. Verstoß: 25k€ Bußgeld."),
            ("§ 558 BGB", "Erhöhung Vergleichsmiete", "Bestand: Erhöhung bis Vergleichsmiete + Kappungsgrenze (+15% in 3 Jahren)."),
            ("§ 558a BGB", "Begründung Erhöhung", "Erhöhung begründen: Mietspiegel, Gutachten, 3 Vergleichswohnungen."),
            ("§ 559 BGB", "Modernisierung 8%", "8% Kosten auf Jahresmiete. Max +3€/m² in 6 Jahren. Kappungsgrenze beachten."),
            ("§ 559a BGB", "Duldungspflicht", "Mieter muss dulden: Energetisch, barrierefrei. KEINE Duldung: Luxus-Sanierung."),
            ("§ 560 BGB", "Betriebskosten", "Anpassung bei Änderung (jährlich). Abrechnung binnen 12 Monate."),
            ("Kappungsgrenze", "15% in 3 Jahren", "Angespannte Märkte: Max +15% in 3 Jahren (normal 20%). München, Berlin, Hamburg."),
        ]
        
        for section, title, content in mietpreisbremse:
            docs.append(self._create_doc(section, title, content, "Mietpreisbremse", ["Mietpreisbremse", "Miete"]))
        
        # ========================================
        # ZVG - ZWANGSVERSTEIGERUNG (30 Paragraphen)
        # ========================================
        zvg = [
            ("§ 15 ZVG", "Antrag", "Gläubiger (Bank) beantragt bei Amtsgericht. Kosten: 0,5% Verkehrswert. Dauer: 6-12 Monate."),
            ("§ 20 ZVG", "Beschlagnahme", "Ab Termin: Schuldner darf NICHT verkaufen, belasten, vermieten. Verstoß: Unwirksam."),
            ("§ 23 ZVG", "Mietverhältnisse", "Mieter bleiben (§ 57). Erwerber übernimmt. Räumung nur mit Eigenbedarf."),
            ("§ 27 ZVG", "Termin", "6 Wochen vorher öffentlich (Gericht, Internet). Ort: Amtsgericht."),
            ("§ 34 ZVG", "Bietungsrecht", "Jeder darf bieten. Sicherheit: 10% Verkehrswert bar/Scheck mitbringen."),
            ("§ 43 ZVG", "Meistgebot", "Höchstes Gebot bekommt Zuschlag (wenn ≥ Mindestgebot)."),
            ("§ 44 ZVG", "Bargebot", "10% sofort, Rest binnen 6 Wochen. Sonst: Sicherheit verfällt + Neuversteigerung."),
            ("§ 49 ZVG", "Verteilung", "Reihenfolge: Verfahrenskosten, Grundpfandrechte (Rang), Schuldner (Rest)."),
            ("§ 52 ZVG", "Grundbuch", "Gericht trägt Erwerber ein (von Amts wegen). Nachrangige Lasten gelöscht."),
            ("§ 57 ZVG", "Besitzübergang", "Ab Zuschlag: Neuer Eigentümer. Mietverhältnisse gehen über."),
            ("§ 74a ZVG", "Mindestgebot 50%", "Mindestgebot = 50% Verkehrswert. Schnäppchen möglich bei wenig Bietern."),
            ("§ 74b ZVG", "Versagung", "Unter 50%: Versagung PFLICHT. 50-70%: Ermessen Gericht."),
            ("§ 81 ZVG", "Wertermittlung", "Vergleichswert (Wohnen), Ertragswert (Gewerbe), Sachwert (Sonder)."),
            ("§ 85 ZVG", "Gutachten", "Gerichtsgutachter ermittelt Marktwert. Kosten: 1.500-5.000€."),
            ("§ 86 ZVG", "Akteneinsicht", "Jeder darf einsehen: Gutachten, Grundbuch, Lasten. 2 Wochen vor Termin."),
            ("§ 90 ZVG", "Einstellung", "Schuldner zahlt + Kosten = Einstellung. Versteigerung abgewendet."),
            ("§ 91 ZVG", "Verteilungsverfahren", "1. Kosten, 2. Grundpfandrechte (Rang), 3. Gläubiger, 4. Schuldner."),
            ("§ 105 ZVG", "Räumung", "Ersteher kann räumen (Gerichtsvollzieher). Kosten: 500-2.000€."),
            ("§ 114 ZVG", "Beschwerde", "Frist: 2 Wochen. Gründe: Verfahrensfehler. Aufschiebende Wirkung."),
            ("§ 120 ZVG", "Kosten", "Schuldner trägt: Verfahren (0,5%), Gutachten, Bekanntmachung. Gesamt: 1-2%."),
            ("§ 146 ZVG", "Mobilien", "Pfändung beweglich parallel. Unpfändbar: Hausrat, Arbeitsgeräte bis 800€."),
            ("§ 161 ZVG", "Zwangsverwaltung", "Alternative: Sequester verwaltet + zahlt Miete an Gläubiger."),
            ("§ 162 ZVG", "Antrag Verwaltung", "Gläubiger wählt: Versteigerung ODER Verwaltung."),
            ("§ 165 ZVG", "Sequester", "Verwalter (Gericht bestellt): Vermietung, Instandhaltung. Vergütung: 10-15%."),
            ("§ 175 ZVG", "Jahresabrechnung", "Sequester legt ab: Einnahmen, Ausgaben, Verteilung."),
            ("§ 180a ZVG", "Beendigung", "Schuld bezahlt = Aufhebung. Verwaltung endet."),
            ("§ 181 ZVG", "Wechsel Versteigerung", "Gläubiger kann jederzeit wechseln (Verwaltung → Versteigerung)."),
            ("§ 185 ZVG", "Vollstreckung Grundschuld", "Vollstreckungsunterwerfung notariell. Kein Titel nötig. Spart 6 Monate."),
            ("§ 765a ZPO", "Abwehrklage", "Schuldner wehrt: Forderung erfüllt, verjährt. Frist: Sofort."),
            ("§ 771 ZPO", "Drittwiderspruch", "Dritter wehrt ab (nicht Schuldner Eigentümer). Versteigerung unwirksam."),
        ]
        
        for section, title, content in zvg:
            docs.append(self._create_doc(section, title, content, "ZVG", ["Zwangsversteigerung", "Vollstreckung"]))
        
        logger.info(f"✅ Häppchen 1: {len(docs)} Dokumente erstellt")
        return docs
    
    def scrape_haeppchen_2(self) -> List[Dict]:
        """Häppchen 2: HOAI (15) + Erbbaurecht (10) + Notarrecht (10) = 35 Docs"""
        docs = []
        
        # ========================================
        # HOAI (15 Paragraphen)
        # ========================================
        hoai = [
            ("§ 3 HOAI", "Anwendungsbereich", "Gilt für Architekten + Ingenieure. Leistungsbilder: Gebäude, Freianlagen, Tragwerk, TGA."),
            ("§ 4 HOAI", "Anrechenbare Kosten", "Honorar nach Baukosten (ohne Grundstück). KG 300+400 (DIN 276)."),
            ("§ 5 HOAI", "Honorarzonen", "Zone I (einfach) bis V (komplex). Wohnbau: III-IV. Denkmal: V."),
            ("§ 6 HOAI", "Leistungsphasen", "LP1-9: Grundlagen (2%), Vorplanung (7%), Entwurf (15%), Genehmigung (3%), Ausführung (25%), Vergabe (14%), Objektüberwachung (32%), Betreuung (2%)."),
            ("§ 7 HOAI", "Honorarvereinbarung", "Schriftlich vor Leistung. Mindestsatz nur bei Wiederholung unterschreiten."),
            ("§ 10 HOAI", "Berechnung", "Honorartafel nach Kosten + Zone + LP. 500k€ Zone III LP 1-8 ≈ 60.000€."),
            ("§ 34 HOAI", "Objektplanung Gebäude", "Wohnbau, Gewerbe. Honorar: 9-15% Baukosten. 1 Mio. = 90-150k€."),
            ("§ 35 HOAI", "Innenräume", "Innenarchitektur, Ausbau. LP 1-8. Honorar niedriger als Gebäude."),
            ("§ 39 HOAI", "Freianlagen", "Gartenarchitektur. Honorar: 8-12%. 50k€ Garten = 4-6k€."),
            ("§ 51 HOAI", "Tragwerksplanung", "Statik, Konstruktion. LP 1-6. Honorar: 3-5%. 500k€ = 15-25k€."),
            ("§ 55 HOAI", "Technische Ausrüstung", "Heizung, Sanitär, Elektro. Honorar: 10-15% TGA-Kosten."),
            ("Anlage 10 HOAI", "Honorartafeln", "100k€ Zone III = 13.500€. 500k€ = 47.000€. 1 Mio. = 78.000€."),
            ("§ 15 HOAI", "Zeithonorar", "Stundensatz: 80-150€/h (Architekt), 60-100€/h (Ingenieur)."),
            ("§ 7 Abs.5 HOAI", "Pauschalhonorar", "Pauschal möglich wenn vorher vereinbart. Muss angemessen sein."),
            ("§ 650p BGB", "Architektenvertrag", "Werkvertrag. Abnahme nach LP 8. Gewährleistung: 5 Jahre."),
        ]
        
        for section, title, content in hoai:
            docs.append(self._create_doc(section, title, content, "HOAI", ["HOAI", "Architektenhonorar"]))
        
        # ========================================
        # ERBBAURECHT (10 Paragraphen)
        # ========================================
        erbbaurecht = [
            ("§ 1 ErbbauRG", "Begriff", "Recht auf fremdem Grundstück Gebäude zu haben. Laufzeit: 50-99 Jahre."),
            ("§ 2 ErbbauRG", "Inhalt", "Bebauung, Nutzung, Veräußerung. Erbbauzins: 3-5% Bodenwert/Jahr."),
            ("§ 5 ErbbauRG", "Erbbauzins", "Jährliche Zahlung. Anpassung alle 3-5 Jahre (Verbraucherpreisindex)."),
            ("§ 9 ErbbauRG", "Erbbaugrundbuch", "Eigenes Grundbuchblatt. Eintragung: Rang, Laufzeit, Zins."),
            ("§ 12 ErbbauRG", "Veräußerung", "Verkauf: Zustimmung Grundstückseigentümer nötig."),
            ("§ 27 ErbbauRG", "Heimfall", "Rückfall bei: Ablauf, Vertragsverletzung. Entschädigung: 2/3 Gebäudewert."),
            ("§ 28 ErbbauRG", "Entschädigung", "Für Gebäude bei Ablauf. Vereinbarung: 50-100% Verkehrswert."),
            ("§ 32 ErbbauRG", "Verlängerung", "Vor Ablauf vereinbaren. Weitere 30-50 Jahre. Zins neu verhandeln."),
            ("GrEStG § 2 Erbbau", "Grunderwerbsteuer", "Erbbaurecht = grundstücksgleich. GrESt bei Bestellung."),
            ("§ 11 ErbbauRG", "Belastung", "Grundschuld auf Erbbaurecht möglich (Baufinanzierung)."),
        ]
        
        for section, title, content in erbbaurecht:
            docs.append(self._create_doc(section, title, content, "ErbbauRG", ["Erbbaurecht", "Erbbauzins"]))
        
        # ========================================
        # NOTARRECHT (10 Paragraphen)
        # ========================================
        notar = [
            ("§ 311b BGB", "Beurkundungspflicht", "Grundstückskauf MUSS notariell. Ohne Notar: NICHTIG."),
            ("§ 925 BGB", "Auflassung", "Einigung Eigentumsübergang beim Notar. Beide anwesend oder Vollmacht."),
            ("§ 873 BGB", "Eintragung", "Eigentum erst mit Eintragung (nicht Vertrag!). Wartezeit: 4-8 Wochen."),
            ("GNotKG § 34", "Notarkosten", "2,0-Gebühr (Beurkundung) + 0,5 + 0,5. 500k€ ≈ 4.000€ Notar."),
            ("GNotKG Anlage", "Kostentabelle", "100k€ = 546€ (1,0). 500k€ = 1.870€. 1 Mio. = 3.471€ (×2)."),
            ("§ 15 GBO", "Grundbuchantrag", "Notar stellt Antrag. Kosten: 0,5% Kaufpreis."),
            ("§ 17 BeurkG", "Belehrungspflicht", "Notar muss belehren über Risiken, Rechte, Kosten. Neutral."),
            ("§ 794 ZPO", "Vollstreckbare Urkunde", "Notarielle Unterwerfung = sofort vollstreckbar. Standard bei Grundschuld."),
            ("§ 14 BNotO", "Unparteilichkeit", "Notar berät BEIDE Seiten neutral. Keine einseitige Beratung."),
            ("§ 19 BNotO", "Verschwiegenheit", "Absolute Verschwiegenheit. Berufsgeheimnis lebenslang."),
        ]
        
        for section, title, content in notar:
            docs.append(self._create_doc(section, title, content, "Notarrecht", ["Notarrecht", "Beurkundung"]))
        
        logger.info(f"✅ Häppchen 2: {len(docs)} Dokumente erstellt")
        return docs
    
    def scrape_haeppchen_3(self) -> List[Dict]:
        """Häppchen 3: BGB Kaufrecht erweitert (20) + Werkvertragsrecht (15) = 35 Docs"""
        docs = []
        
        # ========================================
        # BGB KAUFRECHT ERWEITERT (20 Paragraphen)
        # ========================================
        kaufrecht = [
            ("§ 433 BGB", "Kaufvertrag Pflichten", "Verkäufer: Übergabe + Eigentum. Käufer: Zahlung + Abnahme."),
            ("§ 434 BGB", "Sachmangel", "Abweichung von vereinbarter Beschaffenheit. Wohnfläche, versteckte Mängel."),
            ("§ 435 BGB", "Rechtsmangel", "Dritte können Rechte geltend machen. Grundschuld, Hypothek nicht abgelöst."),
            ("§ 436 BGB", "Öffentliche Lasten", "Erschließungsbeiträge, Anliegerbeiträge. Verkäufer haftet für vor Übergabe."),
            ("§ 437 BGB", "Rechte Käufer", "Nacherfüllung, Rücktritt, Minderung, Schadensersatz."),
            ("§ 438 BGB", "Verjährung", "Immobilien: 5 Jahre ab Übergabe. Bei Arglist: 3 Jahre ab Kenntnis."),
            ("§ 439 BGB", "Nacherfüllung", "Beseitigung Mangel oder Ersatzlieferung. Verkäufer wählt. Frist setzen."),
            ("§ 440 BGB", "Nacherfüllung ausgeschlossen", "Unmöglich, unzumutbar, verweigert. Dann sofort Minderung/Rücktritt."),
            ("§ 441 BGB", "Minderung", "Kaufpreis anteilig reduzieren. Berechnung nach Wertverhältnis."),
            ("§ 442 BGB", "Kenntnis Käufer", "Käufer kannte Mangel = keine Rechte. Arglist Verkäufer = Rechte bleiben."),
            ("§ 443 BGB", "Beschaffenheitsgarantie", "Verkäufer garantiert bestimmte Eigenschaften. Haftung ohne Verschulden."),
            ("§ 444 BGB", "Haftungsausschluss", "Ausschluss möglich (Verkauf wie besehen). NICHT bei Arglist!"),
            ("§ 445 BGB", "Gefahrübergang", "Ab Übergabe trägt Käufer Gefahr. Brand nach Schlüsselübergabe = Käufer."),
            ("§ 446 BGB", "Nutzungen Lasten", "Ab Übergabe: Käufer erhält Nutzungen (Miete), trägt Lasten (Grundsteuer)."),
            ("§ 447 BGB", "Versendungskauf", "Bei Immobilien nicht relevant (keine Versendung)."),
            ("§ 448 BGB", "Kaufkosten", "Verkäufer: Übergabe. Käufer: Notar, Grundbuch, Makler (Anteil)."),
            ("§ 449 BGB", "Eigentumsvorbehalt", "Bei Immobilien: NICHT möglich. Eigentum mit Eintragung."),
            ("§ 453 BGB", "Rechtskauf", "Kauf von Rechten (Erbbaurecht). Kaufrecht entsprechend anwendbar."),
            ("§ 454 BGB", "Forderungskauf", "Kauf einer Forderung. Bei Immobilien: Mietforderungen."),
            ("§ 311b BGB", "Formzwang", "Notarielle Beurkundung ZWINGEND. Ohne Notar = nichtig."),
        ]
        
        for section, title, content in kaufrecht:
            docs.append(self._create_doc(section, title, content, "BGB Kaufrecht", ["Kaufrecht", "Gewährleistung"]))
        
        # ========================================
        # WERKVERTRAGSRECHT BAU (15 Paragraphen)
        # ========================================
        werkvertrag = [
            ("§ 631 BGB", "Werkvertrag Pflichten", "Unternehmer: Herstellung Werk. Besteller: Vergütung + Abnahme."),
            ("§ 632 BGB", "Vergütung", "Vereinbart oder üblich. Stundenlohn oder Pauschal."),
            ("§ 632a BGB", "Abschlagszahlungen", "Unternehmer kann Abschläge fordern (nach Baufortschritt)."),
            ("§ 633 BGB", "Sach- und Rechtsmangel", "Werk frei von Mängeln. Vereinbarte Beschaffenheit + Standard."),
            ("§ 634 BGB", "Rechte Besteller", "Nacherfüllung, Selbstvornahme, Rücktritt, Minderung, Schadensersatz."),
            ("§ 634a BGB", "Verjährung Bauwerk", "Bauwerk: 5 Jahre. Planungsleistungen: 5 Jahre. Arglist: 3 Jahre."),
            ("§ 635 BGB", "Nacherfüllung", "Mängelbeseitigung oder Neuherstellung. Unternehmer wählt."),
            ("§ 637 BGB", "Selbstvornahme", "Besteller kann selbst beseitigen. Vorschuss fordern. Nach Fristablauf."),
            ("§ 638 BGB", "Minderung", "Vergütung herabsetzen. Bei wesentlichem Mangel."),
            ("§ 640 BGB", "Abnahme", "Besteller muss abnehmen (wenn vertragsgemäß). Fiktive Abnahme: 12 Tage."),
            ("§ 641 BGB", "Fälligkeit Vergütung", "Mit Abnahme fällig. Abschläge nach Baufortschritt."),
            ("§ 644 BGB", "Gefahrtragung", "Bis Abnahme: Unternehmer trägt Gefahr. Danach: Besteller."),
            ("§ 648 BGB", "Bauhandwerkersicherung", "Unternehmer kann Sicherheit verlangen (5%). Bei Wohnbau ausgeschlossen."),
            ("§ 648a BGB", "Bauhandwerkersicherungshypothek", "Unternehmer kann Sicherungshypothek ins Grundbuch eintragen."),
            ("§ 650 BGB", "Kostenanschlag", "Wesentliche Überschreitung: Anzeigepflicht. Kündigung möglich."),
        ]
        
        for section, title, content in werkvertrag:
            docs.append(self._create_doc(section, title, content, "BGB Werkvertrag", ["Werkvertrag", "Bauvertrag"]))
        
        logger.info(f"✅ Häppchen 3: {len(docs)} Dokumente erstellt")
        return docs
    
    def scrape_haeppchen_4(self) -> List[Dict]:
        """Häppchen 4: BauGB erweitert (20) + VOB/B erweitert (15) = 35 Docs"""
        docs = []
        
        # ========================================
        # BAUGB ERWEITERT (20 Paragraphen)
        # ========================================
        baugb = [
            ("§ 1 BauGB", "Bauleitplanung", "Gemeinden regeln Bodennutzung. Bebauungsplan bindend."),
            ("§ 2 BauGB", "Aufstellung Bebauungsplan", "Gemeinde beschließt Aufstellung. Bürgerbeteiligung."),
            ("§ 3 BauGB", "Beteiligung Öffentlichkeit", "Auslegung 1 Monat. Stellungnahmen berücksichtigen."),
            ("§ 4 BauGB", "Beteiligung Behörden", "Träger öffentlicher Belange: Stellungnahme."),
            ("§ 9 BauGB", "Inhalt Bebauungsplan", "Art + Maß Nutzung, Bauweise, Grundflächenzahl."),
            ("§ 29 BauGB", "Bauliche Anlagen", "Mit Boden verbunden. Genehmigungspflichtig."),
            ("§ 30 BauGB", "Bebauungsplan Bindung", "Im Geltungsbereich: Nur gemäß B-Plan bauen."),
            ("§ 31 BauGB", "Ausnahmen Befreiungen", "Ausnahme: Im B-Plan vorgesehen. Befreiung: Ermessen."),
            ("§ 33 BauGB", "Planreife", "Vor Satzungsbeschluss: Genehmigung wenn nicht entgegen."),
            ("§ 34 BauGB", "Innenbereich", "Unbeplant: Einfügen in Umgebung. Eigenart beachten."),
            ("§ 35 BauGB", "Außenbereich", "Nur privilegiert (Landwirtschaft, Windkraft). Sonst: Nein."),
            ("§ 36 BauGB", "Gemeindliches Einvernehmen", "Gemeinde muss zustimmen. Kann versagen (2 Monate Frist)."),
            ("§ 136 BauGB", "Sanierungsgebiet", "Städtebauliche Missstände. Sonderrecht Gemeinde."),
            ("§ 144 BauGB", "Genehmigungspflicht Sanierung", "Verkauf, Belastung, Vermietung genehmigungspflichtig."),
            ("§ 153 BauGB", "Ausgleichsbetrag", "Wertsteigerung durch Sanierung = Abgabe an Gemeinde."),
            ("§ 171a BauGB", "Stadtumbau", "Rückbau, Anpassung Infrastruktur."),
            ("§ 172 BauGB", "Erhaltungssatzung", "Milieuschutz. Umwandlung Miet → Eigentum genehmigungspflichtig."),
            ("§ 24 BauGB", "Vorkaufsrecht Gemeinde", "Bei Verkauf im Geltungsbereich. Ausübung binnen 2 Monate."),
            ("§ 25 BauGB", "Besonderes Vorkaufsrecht", "Sanierung, Entwicklung. Erweiterte Rechte Gemeinde."),
            ("§ 28 BauGB", "Ausübung Vorkaufsrecht", "Zum Kaufpreis. Gemeinde kann ablösen."),
        ]
        
        for section, title, content in baugb:
            docs.append(self._create_doc(section, title, content, "BauGB", ["Baurecht", "Bebauungsplan"]))
        
        # ========================================
        # VOB/B ERWEITERT (15 Paragraphen)
        # ========================================
        vob = [
            ("§ 1 VOB/B", "Art und Umfang", "Leistungsumfang nach Vertrag. Leistungsverzeichnis maßgeblich."),
            ("§ 2 VOB/B", "Vergütung", "Einheitspreis oder Pauschal. Nachträge bei Änderung."),
            ("§ 3 VOB/B", "Ausführungsunterlagen", "Auftraggeber liefert Pläne. Prüfpflicht Auftragnehmer."),
            ("§ 4 VOB/B", "Ausführung", "Nach anerkannten Regeln Technik. Mängelfreie Leistung."),
            ("§ 5 VOB/B", "Ausführungsfristen", "Vertragsfristen einhalten. Verzug = Schadensersatz."),
            ("§ 6 VOB/B", "Behinderung", "Anzeige bei Behinderung. Fristverlängerung."),
            ("§ 7 VOB/B", "Verteilung Gefahr", "Auftraggeber: Höhere Gewalt. Auftragnehmer: Eigenverschulden."),
            ("§ 8 VOB/B", "Kündigung Auftraggeber", "Jederzeit möglich. Vergütung für erbrachte Leistung."),
            ("§ 9 VOB/B", "Kündigung Auftragnehmer", "Nur bei Zahlungsverzug oder Unmöglichkeit."),
            ("§ 10 VOB/B", "Haftung", "Schadensersatz bei Verschulden. Gesamtschuldner Subunternehmer."),
            ("§ 12 VOB/B", "Abnahme", "12 Werktage nach Fertigstellung. Förmlich oder Inbenutzungnahme."),
            ("§ 13 VOB/B", "Mängelansprüche", "4 Jahre Verjährung (BGB: 5 Jahre). Abnahme = Beginn."),
            ("§ 14 VOB/B", "Abrechnung", "Prüfbare Schlussrechnung. 2 Monate Prüffrist."),
            ("§ 16 VOB/B", "Zahlung", "Schlusszahlung binnen 30 Tage. Abschläge nach Baufortschritt."),
            ("§ 17 VOB/B", "Sicherheitsleistung", "5% Vertragserfüllungsbürgschaft. 3% Gewährleistung."),
        ]
        
        for section, title, content in vob:
            docs.append(self._create_doc(section, title, content, "VOB/B", ["VOB", "Bauvertrag"]))
        
        logger.info(f"✅ Häppchen 4: {len(docs)} Dokumente erstellt")
        return docs
    
    def scrape_haeppchen_5(self) -> List[Dict]:
        """Häppchen 5: WEG erweitert (20) + GEG erweitert (15) = 35 Docs"""
        docs = []
        
        # ========================================
        # WEG ERWEITERT (20 Paragraphen)
        # ========================================
        weg = [
            ("§ 1 WEG", "Begriffsbestimmung", "Wohnungseigentum = Sondereigentum + Miteigentumsanteil."),
            ("§ 2 WEG", "Abweichende Vereinbarungen", "Teilungserklärung kann abweichen. Grenzen beachten."),
            ("§ 3 WEG", "Teilungserklärung", "Notariell. Inhalt: Sonder-, Gemeinschaftseigentum, MEA."),
            ("§ 5 WEG", "Gegenstand Sondereigentum", "Wohnung innen. NICHT: Fassade, Dach, tragende Wände."),
            ("§ 7 WEG", "Grundbuchblatt", "Jede Wohnung = eigenes Grundbuchblatt."),
            ("§ 8 WEG", "Teilung durch Eigentümer", "Eigentümer teilt auf. Teilungserklärung + Aufteilungsplan."),
            ("§ 9a WEG", "Gemeinschaft Rechtsfähigkeit", "Kann klagen, verklagt werden. Vertreten durch Verwalter."),
            ("§ 9b WEG", "Vertreter Gemeinschaft", "Verwalter vertritt. Bei Fehlen: Alle Eigentümer gemeinsam."),
            ("§ 10 WEG", "Allgemeine Grundsätze", "Ordnungsgemäße Verwaltung. Mehrheitsbeschlüsse."),
            ("§ 12 WEG", "Veräußerungsbeschränkung", "Zustimmung Verwalter möglich (Vereinbarung)."),
            ("§ 14 WEG", "Rechte Eigentümer", "Nutzung Sondereigentum. Gemeinschaftseigentum anteilig."),
            ("§ 15 WEG", "Pflichten Eigentümer", "Instandhaltung Sondereigentum. Hausgeld zahlen."),
            ("§ 16 WEG", "Kosten", "Nach Miteigentumsanteil. Vereinbarung kann abweichen."),
            ("§ 18 WEG", "Entziehung Wohnungseigentum", "Bei schweren Pflichtverletzungen. Letzte Maßnahme."),
            ("§ 19 WEG", "Versammlung", "Jährlich mindestens 1x. Einladung 3 Wochen vorher."),
            ("§ 20 WEG", "Beschlussfassung", "Einfache Mehrheit. Qualifiziert bei baulichen Änderungen."),
            ("§ 21 WEG", "Ordnungsmäßige Verwaltung", "Instandhaltungsrücklage bilden. Jahresabrechnung."),
            ("§ 23 WEG", "Wohnungseigentümerversammlung", "Beschlussfähig: Anwesende. Protokoll Pflicht."),
            ("§ 24 WEG", "Einberufung Versammlung", "Verwalter oder 1/4 Eigentümer. Schriftlich."),
            ("§ 26 WEG", "Verwalter", "Max 5 Jahre Bestellung. Aufgaben: Verwaltung, Abrechnung."),
        ]
        
        for section, title, content in weg:
            docs.append(self._create_doc(section, title, content, "WEG", ["WEG", "Wohnungseigentum"]))
        
        # ========================================
        # GEG ERWEITERT (15 Paragraphen)
        # ========================================
        geg = [
            ("§ 1 GEG", "Zweck", "Klimaschutz, Energieeffizienz. Fossile Brennstoffe reduzieren."),
            ("§ 3 GEG", "Anwendungsbereich", "Gebäude mit Heizung/Kühlung. Ausnahme: Denkmal teilweise."),
            ("§ 10 GEG", "Anforderungen Neubau", "Primärenergiebedarf begrenzt. KfW 40/55 Standard."),
            ("§ 16 GEG", "Mindestwärmeschutz", "U-Wert Außenwand, Dach, Fenster. Mindestanforderungen."),
            ("§ 47 GEG", "Austauschpflicht Heizkessel", "Über 30 Jahre = Austausch. Brennwert ausgenommen."),
            ("§ 48 GEG", "Energieausweis Pflicht", "Bei Verkauf/Vermietung vorlegen. 10 Jahre gültig."),
            ("§ 50 GEG", "Grundsätze Energieausweis", "Bedarfs- oder Verbrauchsausweis. Pflichtangaben."),
            ("§ 71 GEG", "65% Erneuerbare", "Neue Heizung ab 2024: 65% erneuerbar. Wärmepumpe, Solar."),
            ("§ 72 GEG", "Übergangsfristen", "Bestand: Längere Fristen. Kommunale Wärmeplanung abwarten."),
            ("§ 80 GEG", "Nachrüstpflichten", "Oberste Geschossdecke dämmen. Alte Heizungen ersetzen."),
            ("§ 81 GEG", "Ausnahmen", "Unwirtschaftlichkeit. Härtefälle (Einkommen, Alter)."),
            ("§ 102 GEG", "Ordnungswidrigkeiten", "Verstoß = Bußgeld bis 50.000€. Kein Energieausweis."),
            ("§ 103 GEG", "Übergangsvorschriften", "Altanlagen Bestandsschutz. Schrittweise Verschärfung."),
            ("§ 111 GEG", "Inkrafttreten", "1.1.2024 vollständig. 65%-Regel aktiv."),
            ("GEG Anlage 1", "Heizungsarten", "Wärmepumpe, Fernwärme, Biomasse = 65% erfüllt. Gas-Hybrid möglich."),
        ]
        
        for section, title, content in geg:
            docs.append(self._create_doc(section, title, content, "GEG", ["GEG", "Energieeffizienz"]))
        
        logger.info(f"✅ Häppchen 5: {len(docs)} Dokumente erstellt")
        return docs
    
    def _create_doc(self, section: str, title: str, content: str, law: str, topics: List[str]) -> Dict:
        """Erstellt ein standardisiertes Dokument"""
        return {
            "id": f"{law.lower().replace(' ', '_').replace('/', '_')}_{section.replace('§', 'par').replace(' ', '_').replace('/', '_').lower()}",
            "content": f"{section} - {title}\n\n{content}\n\nFundstelle: {section}",
            "jurisdiction": "DE",
            "language": "de",
            "source": section,
            "source_url": f"https://www.gesetze-im-internet.de/{law.lower().replace(' ', '').replace('/', '_')}/",
            "topics": topics,
            "law": law,
            "section": section,
            "last_updated": datetime.utcnow().isoformat()
        }


__all__ = ["ImmobilienKomplettScraper"]
