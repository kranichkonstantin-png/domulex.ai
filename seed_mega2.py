#!/usr/bin/env python3
"""
Mega-Seeding Teil 2: 100+ Dokumente
- Komplettes BGB Mietrecht
- Mehr Rechtsprechung
- Checklisten und Muster
"""

import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import google.generativeai as genai

QDRANT_HOST = "11856a38-8506-409b-a67a-ee9d8c1bc4cf.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_PORT = 6333
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.po714-tQsevHd5Nr63f1oKoRcuSyOYi_Krre9-CGBzw"
COLLECTION_NAME = "legal_documents"
GEMINI_API_KEY = "AIzaSyDHb8dTwM-jpr5k7GPCVuQbfon38tckOls"

genai.configure(api_key=GEMINI_API_KEY)

def get_embedding(text: str) -> list:
    result = genai.embed_content(model="models/embedding-001", content=text[:8000], task_type="retrieval_document")
    return result['embedding']

def generate_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# Mehr BGB Mietrecht
BGB_MIETRECHT = [
    {"paragraph": "§ 535 BGB", "titel": "Inhalt und Hauptpflichten des Mietvertrags", "inhalt": "Durch den Mietvertrag wird der Vermieter verpflichtet, dem Mieter den Gebrauch der Mietsache während der Mietzeit zu gewähren. Der Vermieter hat die Mietsache dem Mieter in einem zum vertragsgemäßen Gebrauch geeigneten Zustand zu überlassen und sie während der Mietzeit in diesem Zustand zu erhalten. Der Mieter ist verpflichtet, dem Vermieter die vereinbarte Miete zu entrichten."},
    {"paragraph": "§ 536 BGB", "titel": "Mietminderung bei Sach- und Rechtsmängeln", "inhalt": "Hat die Mietsache zur Zeit der Überlassung an den Mieter einen Mangel, der ihre Tauglichkeit zum vertragsgemäßen Gebrauch aufhebt, oder entsteht während der Mietzeit ein solcher Mangel, so ist der Mieter für die Zeit, in der die Tauglichkeit aufgehoben ist, von der Entrichtung der Miete befreit. Für die Zeit, während der die Tauglichkeit gemindert ist, hat er nur eine angemessen herabgesetzte Miete zu entrichten."},
    {"paragraph": "§ 536a BGB", "titel": "Schadens- und Aufwendungsersatzanspruch des Mieters wegen eines Mangels", "inhalt": "Ist ein Mangel im Sinne des § 536 bei Vertragsschluss vorhanden oder entsteht ein solcher Mangel später wegen eines Umstands, den der Vermieter zu vertreten hat, oder kommt der Vermieter mit der Beseitigung eines Mangels in Verzug, so kann der Mieter unbeschadet der Rechte aus § 536 Schadensersatz verlangen."},
    {"paragraph": "§ 537 BGB", "titel": "Entrichtung der Miete bei persönlicher Verhinderung des Mieters", "inhalt": "Der Mieter wird von der Entrichtung der Miete nicht dadurch befreit, dass er durch einen in seiner Person liegenden Grund an der Ausübung seines Gebrauchsrechts gehindert wird. Der Vermieter muss sich jedoch den Wert der ersparten Aufwendungen sowie derjenigen Vorteile anrechnen lassen, die er aus einer anderweitigen Verwertung des Gebrauchs erlangt."},
    {"paragraph": "§ 538 BGB", "titel": "Abnutzung der Mietsache durch vertragsgemäßen Gebrauch", "inhalt": "Veränderungen oder Verschlechterungen der Mietsache, die durch den vertragsgemäßen Gebrauch herbeigeführt werden, hat der Mieter nicht zu vertreten. Der Mieter schuldet keinen Ersatz für normale Abnutzungserscheinungen."},
    {"paragraph": "§ 539 BGB", "titel": "Ersatz sonstiger Aufwendungen und Wegnahmerecht des Mieters", "inhalt": "Der Mieter kann vom Vermieter Aufwendungen auf die Mietsache, die der Vermieter ihm nicht nach § 536a Abs. 2 zu ersetzen hat, nach den Vorschriften über die Geschäftsführung ohne Auftrag ersetzt verlangen. Der Mieter ist berechtigt, eine Einrichtung wegzunehmen, mit der er die Mietsache versehen hat."},
    {"paragraph": "§ 540 BGB", "titel": "Gebrauchsüberlassung an Dritte", "inhalt": "Der Mieter ist ohne die Erlaubnis des Vermieters nicht berechtigt, den Gebrauch der Mietsache einem Dritten zu überlassen, insbesondere sie weiter zu vermieten. Verweigert der Vermieter die Erlaubnis, so kann der Mieter das Mietverhältnis außerordentlich mit der gesetzlichen Frist kündigen, sofern nicht in der Person des Dritten ein wichtiger Grund vorliegt."},
    {"paragraph": "§ 541 BGB", "titel": "Unterlassungsklage bei vertragswidrigem Gebrauch", "inhalt": "Setzt der Mieter einen vertragswidrigen Gebrauch der Mietsache trotz einer Abmahnung des Vermieters fort, so kann dieser auf Unterlassung klagen."},
    {"paragraph": "§ 542 BGB", "titel": "Ende des Mietverhältnisses", "inhalt": "Ist die Mietzeit nicht bestimmt, so kann jede Vertragspartei das Mietverhältnis nach den gesetzlichen Vorschriften kündigen. Ein Mietverhältnis, das auf bestimmte Zeit eingegangen ist, endet mit dem Ablauf dieser Zeit, sofern es nicht in den gesetzlich zugelassenen Fällen außerordentlich gekündigt oder verlängert wird."},
    {"paragraph": "§ 543 BGB", "titel": "Außerordentliche fristlose Kündigung aus wichtigem Grund", "inhalt": "Jede Vertragspartei kann das Mietverhältnis aus wichtigem Grund außerordentlich fristlos kündigen. Ein wichtiger Grund liegt vor, wenn dem Kündigenden unter Berücksichtigung aller Umstände des Einzelfalls, insbesondere eines Verschuldens der Vertragsparteien, und unter Abwägung der beiderseitigen Interessen die Fortsetzung des Mietverhältnisses bis zum Ablauf der Kündigungsfrist oder bis zur sonstigen Beendigung des Mietverhältnisses nicht zugemutet werden kann."},
    {"paragraph": "§ 544 BGB", "titel": "Vertrag über mehr als 30 Jahre", "inhalt": "Wird ein Mietvertrag für eine längere Zeit als 30 Jahre geschlossen, so kann nach Ablauf von 30 Jahren jede Vertragspartei das Mietverhältnis außerordentlich mit der gesetzlichen Frist kündigen. Die Kündigung ist unzulässig, wenn der Vertrag für die Lebenszeit des Vermieters oder des Mieters geschlossen worden ist."},
    {"paragraph": "§ 546 BGB", "titel": "Rückgabepflicht des Mieters", "inhalt": "Der Mieter ist verpflichtet, die Mietsache nach Beendigung des Mietverhältnisses zurückzugeben. Hat der Mieter den Gebrauch der Mietsache einem Dritten überlassen, so kann der Vermieter die Sache nach Beendigung des Mietverhältnisses auch von dem Dritten zurückfordern."},
    {"paragraph": "§ 546a BGB", "titel": "Entschädigung des Vermieters bei verspäteter Rückgabe", "inhalt": "Gibt der Mieter die Mietsache nach Beendigung des Mietverhältnisses nicht zurück, so kann der Vermieter für die Dauer der Vorenthaltung als Entschädigung die vereinbarte Miete oder die Miete verlangen, die für vergleichbare Sachen ortsüblich ist. Die Geltendmachung eines weiteren Schadens ist nicht ausgeschlossen."},
    {"paragraph": "§ 548 BGB", "titel": "Verjährung der Ersatzansprüche und des Wegnahmerechts", "inhalt": "Die Ersatzansprüche des Vermieters wegen Veränderungen oder Verschlechterungen der Mietsache verjähren in sechs Monaten. Die Verjährung beginnt mit dem Zeitpunkt, in dem er die Mietsache zurückerhält. Mit der Verjährung des Anspruchs des Vermieters auf Rückgabe der Mietsache verjähren auch seine Ersatzansprüche."},
    {"paragraph": "§ 549 BGB", "titel": "Auf Wohnraummietverhältnisse anwendbare Vorschriften", "inhalt": "Für Mietverhältnisse über Wohnraum gelten die Vorschriften der §§ 535 bis 548, soweit sich nicht aus den §§ 549 bis 577a etwas anderes ergibt."},
    {"paragraph": "§ 550 BGB", "titel": "Form des Mietvertrags", "inhalt": "Wird der Mietvertrag für längere Zeit als ein Jahr nicht in schriftlicher Form geschlossen, so gilt er für unbestimmte Zeit. Die Kündigung ist jedoch frühestens zum Ablauf eines Jahres nach Überlassung des Wohnraums zulässig."},
    {"paragraph": "§ 551 BGB", "titel": "Begrenzung und Anlage von Mietsicherheiten", "inhalt": "Hat der Mieter dem Vermieter für die Erfüllung seiner Pflichten Sicherheit zu leisten, so darf diese vorbehaltlich des Absatzes 3 Satz 4 höchstens das Dreifache der auf einen Monat entfallenden Miete ohne die als Pauschale oder als Vorauszahlung ausgewiesenen Betriebskosten betragen. Der Mieter kann die Sicherheit in drei gleichen monatlichen Teilzahlungen leisten."},
    {"paragraph": "§ 552 BGB", "titel": "Abwendung des Wegnahmerechts des Mieters", "inhalt": "Der Vermieter kann die Ausübung des Wegnahmerechts durch Zahlung einer angemessenen Entschädigung abwenden, es sei denn, dass der Mieter ein berechtigtes Interesse an der Wegnahme hat."},
    {"paragraph": "§ 554 BGB", "titel": "Barrierereduzierung, E-Mobilität und Einbruchsschutz", "inhalt": "Der Mieter kann verlangen, dass ihm der Vermieter bauliche Veränderungen der Mietsache erlaubt, die dem Gebrauch durch Menschen mit Behinderungen, dem Laden elektrisch betriebener Fahrzeuge oder dem Einbruchsschutz dienen. Der Mieter trägt die Kosten."},
    {"paragraph": "§ 555a BGB", "titel": "Erhaltungsmaßnahmen", "inhalt": "Der Mieter hat Maßnahmen zu dulden, die zur Instandhaltung oder Instandsetzung der Mietsache erforderlich sind (Erhaltungsmaßnahmen). Der Vermieter hat die Erhaltungsmaßnahme dem Mieter rechtzeitig anzukündigen, es sei denn, sie ist nur mit einer unerheblichen Einwirkung auf die Mietsache verbunden oder ihre sofortige Durchführung ist zwingend erforderlich."},
    {"paragraph": "§ 555b BGB", "titel": "Modernisierungsmaßnahmen", "inhalt": "Modernisierungsmaßnahmen sind bauliche Veränderungen, durch die 1. in Bezug auf die Mietsache Endenergie nachhaltig eingespart wird, 2. nicht erneuerbare Primärenergie nachhaltig eingespart oder das Klima nachhaltig geschützt wird, 3. der Wasserverbrauch nachhaltig reduziert wird, 4. der Gebrauchswert der Mietsache nachhaltig erhöht wird oder 5. die allgemeinen Wohnverhältnisse auf Dauer verbessert werden."},
    {"paragraph": "§ 555c BGB", "titel": "Ankündigung von Modernisierungsmaßnahmen", "inhalt": "Der Vermieter hat dem Mieter eine Modernisierungsmaßnahme spätestens drei Monate vor ihrem Beginn in Textform anzukündigen. Die Ankündigung muss Angaben über Art und voraussichtlichen Umfang der Modernisierungsmaßnahme, voraussichtlichen Beginn und Dauer, Mieterhöhung sowie voraussichtliche künftige Betriebskosten enthalten."},
    {"paragraph": "§ 555d BGB", "titel": "Duldung von Modernisierungsmaßnahmen, Härteeinwand", "inhalt": "Der Mieter hat eine Modernisierungsmaßnahme zu dulden. Dies gilt nicht, wenn die Maßnahme für den Mieter, seine Familie oder einen Angehörigen seines Haushalts eine Härte bedeuten würde, die auch unter Würdigung der berechtigten Interessen sowohl des Vermieters als auch anderer Mieter in dem Gebäude nicht zu rechtfertigen ist."},
    {"paragraph": "§ 556 BGB", "titel": "Vereinbarungen über Betriebskosten", "inhalt": "Die Vertragsparteien können vereinbaren, dass der Mieter Betriebskosten trägt. Betriebskosten sind die Kosten, die dem Eigentümer durch das Eigentum am Grundstück oder durch den bestimmungsgemäßen Gebrauch des Gebäudes laufend entstehen."},
    {"paragraph": "§ 556a BGB", "titel": "Abrechnungsmaßstab für Betriebskosten", "inhalt": "Haben die Vertragsparteien nichts anderes vereinbart, sind die Betriebskosten vorbehaltlich anderweitiger Vorschriften nach dem Anteil der Wohnfläche umzulegen. Betriebskosten, die von einem erfassten Verbrauch oder einer erfassten Verursachung durch den Mieter abhängen, sind nach einem Maßstab umzulegen, der dem unterschiedlichen Verbrauch oder der unterschiedlichen Verursachung Rechnung trägt."},
]

# Checklisten
CHECKLISTEN = [
    {"titel": "Checkliste: Wohnungsbesichtigung Mietinteressent", "inhalt": "1. Lage prüfen: Verkehrsanbindung, Einkaufsmöglichkeiten, Schulen. 2. Wohnung: Zustand Wände, Decken, Böden. 3. Fenster und Türen: Dichtigkeit, Funktionalität. 4. Heizung: Art, Alter, letzter Wartungstermin. 5. Warmwasser: Funktioniert es, wie lange dauert es? 6. Steckdosen: Anzahl und Verteilung. 7. Internet: Verfügbare Anbieter und Geschwindigkeiten. 8. Nebenkosten: Höhe und was ist enthalten. 9. Keller/Stellplatz: Verfügbar, welche Kosten? 10. Nachbarschaft: Wer wohnt nebenan, wie hellhörig?"},
    {"titel": "Checkliste: Wohnungsübergabe Einzug", "inhalt": "1. Zählerstände ablesen: Strom, Gas, Wasser. 2. Alle Räume fotografieren mit Datum. 3. Vorhandene Mängel im Protokoll vermerken. 4. Schlüssel zählen und dokumentieren. 5. Funktionskontrolle: Heizung, Warmwasser, Elektrik, Klingel. 6. Fenster und Türen auf Funktion prüfen. 7. Badezimmer: Abfluss, Armaturen, Silikonfugen. 8. Küche: Alle Geräte funktionsfähig? 9. Protokoll beidseitig unterschreiben. 10. Termin für eventuelle Nachbesserungen vereinbaren."},
    {"titel": "Checkliste: Wohnungsübergabe Auszug", "inhalt": "1. Renovierungspflichten aus Mietvertrag prüfen. 2. Schönheitsreparaturen durchführen (falls vereinbart). 3. Einbauten und Bohrlöcher: Rückbau erforderlich? 4. Wohnung besenrein übergeben. 5. Alle Zählerstände ablesen und dokumentieren. 6. Fotodokumentation aller Räume. 7. Alle Schlüssel zurückgeben. 8. Übergabeprotokoll erstellen und unterschreiben. 9. Nachsendeauftrag bei Post stellen. 10. Versorger und Behörden informieren."},
    {"titel": "Checkliste: Immobilienkauf", "inhalt": "1. Budget festlegen: Eigenkapital, maximale Monatsrate. 2. Finanzierungszusage einholen. 3. Grundbuchauszug prüfen: Eigentümer, Lasten, Rechte. 4. Energieausweis einsehen. 5. Bei WEG: Protokolle und Wirtschaftsplan lesen. 6. Bausubstanz prüfen lassen (Gutachter). 7. Nebenkosten kalkulieren: Grunderwerbsteuer, Notar, Makler. 8. Kaufvertragsentwurf genau lesen. 9. Übergabetermin und Kaufpreisfälligkeit klären. 10. Notartermin vorbereiten."},
    {"titel": "Checkliste: Eigentumswohnung kaufen - WEG prüfen", "inhalt": "1. Teilungserklärung und Gemeinschaftsordnung lesen. 2. Letzte 3 Protokolle der Eigentümerversammlungen. 3. Aktueller Wirtschaftsplan und Hausgeldabrechnung. 4. Höhe der Instandhaltungsrücklage. 5. Geplante Sanierungsmaßnahmen? Sonderumlagen? 6. Hausordnung lesen. 7. Verwaltung: Wer ist es, wie zufrieden sind die Eigentümer? 8. Wie ist das Verhältnis Selbstnutzer zu Kapitalanlegern? 9. Gibt es Rechtsstreitigkeiten in der WEG? 10. Nutzungseinschränkungen (z.B. gewerbliche Nutzung)?"},
    {"titel": "Checkliste: Vermietung einer Wohnung", "inhalt": "1. Mietpreis festlegen: Mietspiegel, Marktlage prüfen. 2. Exposé erstellen mit Fotos und Grundriss. 3. Energieausweis bereithalten (Pflicht!). 4. Interessenten prüfen: Bonität, Mieterselbstauskunft. 5. Besichtigungen organisieren. 6. Mietvertrag vorbereiten: Kaltmiete, Nebenkosten, Kaution. 7. Kaution vereinbaren (max. 3 Monatsmieten). 8. Übergabetermin festlegen und Protokoll vorbereiten. 9. Zählerstände ablesen und Anmeldung bei Versorgern. 10. Meldebestätigung für den Mieter ausstellen."},
    {"titel": "Checkliste: Nebenkostenabrechnung prüfen", "inhalt": "1. Frist eingehalten? (12 Monate nach Abrechnungszeitraum). 2. Richtiger Abrechnungszeitraum? 3. Nur umlegbare Kosten enthalten? (§ 2 BetrKV). 4. Kosten für Leerstand beim Vermieter? 5. Verteilerschlüssel korrekt? 6. Vorjahreswerte zum Vergleich heranziehen. 7. Vorauszahlungen richtig angerechnet? 8. Belege anfordern und prüfen (Einsichtsrecht). 9. Rechenfehler suchen. 10. Bei Fehlern: Schriftlich widersprechen (innerhalb 12 Monate)."},
    {"titel": "Checkliste: Mietminderung", "inhalt": "1. Mangel dokumentieren: Fotos, Datum, Beschreibung. 2. Vermieter unverzüglich schriftlich informieren. 3. Frist zur Mängelbeseitigung setzen. 4. Minderungsquote recherchieren (Minderungstabellen). 5. Minderung erst ab Kenntnis des Vermieters. 6. Nicht eigenmächtig zu viel mindern (Kündigungsrisiko). 7. Besser: Miete unter Vorbehalt zahlen. 8. Bei kompletter Unbewohnbarkeit: 100% Minderung möglich. 9. Bei Streit: Mieterverein oder Anwalt konsultieren. 10. Beweislast für Mangel liegt beim Mieter."},
]

# Mehr Rechtsprechung
RECHTSPRECHUNG = [
    {"aktenzeichen": "BGH VIII ZR 329/22", "datum": "2023-11-08", "titel": "Eigenbedarfskündigung bei Vorratskündigung", "inhalt": "Eine Eigenbedarfskündigung kann treuwidrig sein, wenn der Vermieter bei Vertragsschluss den Eigenbedarf bereits vorhergesehen hat und den Mieter nicht darüber aufgeklärt hat. Die Voraussicht des Eigenbedarfs führt aber nicht automatisch zur Unwirksamkeit der Kündigung."},
    {"aktenzeichen": "BGH VIII ZR 118/21", "datum": "2022-09-21", "titel": "Schönheitsreparaturen bei renoviert übernommener Wohnung", "inhalt": "Hat der Mieter eine renovierte Wohnung übernommen, kann er auch bei unwirksamer Schönheitsreparaturklausel vom Vermieter keine Durchführung von Schönheitsreparaturen verlangen, solange der Zustand der Wohnung nicht wesentlich schlechter ist als bei Vertragsbeginn."},
    {"aktenzeichen": "BGH VIII ZR 287/20", "datum": "2021-11-24", "titel": "Mietkaution: Aufrechnung gegen Schadensersatz", "inhalt": "Der Vermieter kann gegenüber dem Anspruch des Mieters auf Rückzahlung der Kaution mit Schadensersatzansprüchen wegen Beschädigung der Mietsache aufrechnen. Die Aufrechnung setzt voraus, dass die Schadensersatzansprüche fällig und hinreichend beziffert sind."},
    {"aktenzeichen": "BGH VIII ZR 343/18", "datum": "2020-05-27", "titel": "Modernisierungsankündigung: Anforderungen", "inhalt": "Eine Modernisierungsankündigung muss den Mieter in die Lage versetzen, das Ausmaß der zu erwartenden Beeinträchtigungen und die zu erwartende Mieterhöhung einzuschätzen. Pauschale Angaben genügen den Anforderungen des § 555c BGB nicht."},
    {"aktenzeichen": "BGH VIII ZR 232/18", "datum": "2020-04-08", "titel": "Betriebskostenabrechnung: Einsichtsrecht in Belege", "inhalt": "Der Mieter hat das Recht, die Belege der Betriebskostenabrechnung einzusehen. Der Vermieter muss die Einsichtnahme am Ort der Hausverwaltung ermöglichen. Die Vorlage von Kopien kann der Mieter nur bei besonderem Interesse verlangen."},
    {"aktenzeichen": "BGH VIII ZR 263/17", "datum": "2019-06-12", "titel": "Kündigung wegen Zahlungsverzug: Schonfristzahlung", "inhalt": "Die Schonfristzahlung nach § 569 Abs. 3 Nr. 2 BGB heilt auch eine ordentliche Kündigung, die auf denselben Rückstand gestützt wird, wenn sie zusammen mit einer außerordentlichen fristlosen Kündigung ausgesprochen wurde."},
    {"aktenzeichen": "BGH V ZR 165/20", "datum": "2022-02-04", "titel": "WEG: Umfang des Gemeinschaftseigentums", "inhalt": "Fenster einschließlich des Rahmens gehören zum Gemeinschaftseigentum. Die Kosten für die Instandhaltung und Instandsetzung trägt grundsätzlich die Gemeinschaft. Eine abweichende Kostentragung kann in der Gemeinschaftsordnung vereinbart werden."},
    {"aktenzeichen": "BGH V ZR 25/21", "datum": "2022-06-24", "titel": "WEG: Beschlusskompetenz für bauliche Veränderungen", "inhalt": "Nach der WEG-Reform 2020 können bauliche Veränderungen grundsätzlich mit einfacher Mehrheit beschlossen werden. Die Kostenverteilung richtet sich nach § 21 WEG. Unverhältnismäßige Beeinträchtigungen einzelner Eigentümer sind weiterhin zu vermeiden."},
    {"aktenzeichen": "BGH V ZR 176/19", "datum": "2020-12-18", "titel": "Grundstückskauf: Arglistiges Verschweigen von Mängeln", "inhalt": "Der Verkäufer eines Hausgrundstücks handelt arglistig, wenn er bei Vertragsschluss einen ihm bekannten erheblichen Mangel (hier: Hausschwamm) verschweigt, den der Käufer nicht kennt und den er nach der Verkehrsauffassung auch nicht kennen muss."},
    {"aktenzeichen": "BGH V ZR 8/19", "datum": "2020-01-24", "titel": "Grunddienstbarkeit: Wegerecht", "inhalt": "Der Umfang eines Wegerechts bestimmt sich nach dem Inhalt der Eintragung im Grundbuch und der diese Eintragung in Bezug genommenen Eintragungsbewilligung. Veränderungen der Grundstücksnutzung können zu einer Erweiterung des Wegerechts führen."},
]

# Vertragsklauseln - wirksam/unwirksam
VERTRAGSKLAUSELN = [
    {"titel": "Wirksame Mietvertragsklausel: Tierhaltung", "inhalt": "Die Haltung von Kleintieren (Hamster, Fische, Vögel) ist erlaubt. Die Haltung von Hunden und Katzen bedarf der vorherigen Zustimmung des Vermieters. Diese Klausel ist wirksam, da dem Vermieter ein berechtigtes Interesse an der Einzelfallprüfung bei größeren Tieren zugestanden wird."},
    {"titel": "Unwirksame Mietvertragsklausel: Generelles Tierhaltungsverbot", "inhalt": "Ein generelles Tierhaltungsverbot ist unwirksam, da es auch die Haltung von Kleintieren umfasst, die zum vertragsgemäßen Gebrauch einer Mietwohnung gehört. Der Mieter darf trotz Klausel Kleintiere halten."},
    {"titel": "Wirksame Klausel: Kaution in Raten", "inhalt": "Der Mieter ist berechtigt, die Kaution in drei gleichen monatlichen Raten zu zahlen. Die erste Rate ist zu Beginn des Mietverhältnisses fällig. Diese Klausel entspricht § 551 Abs. 2 BGB und ist wirksam."},
    {"titel": "Unwirksame Klausel: Kaution sofort fällig", "inhalt": "Eine Klausel, die die sofortige vollständige Zahlung der Kaution bei Vertragsschluss verlangt, ist unwirksam. Der Mieter hat nach § 551 Abs. 2 BGB das Recht, in drei Raten zu zahlen. Eine abweichende Vereinbarung zu Lasten des Mieters ist unwirksam."},
    {"titel": "Wirksame Klausel: Kleinreparaturen", "inhalt": "Der Mieter trägt die Kosten für Kleinreparaturen an Installationsgegenständen für Elektrizität, Wasser und Gas, Heiz- und Kocheinrichtungen, Fenster- und Türverschlüssen sowie Verschlussvorrichtungen von Fensterläden. Die Obergrenze beträgt 100 EUR pro Einzelfall und 200 EUR pro Jahr."},
    {"titel": "Unwirksame Klausel: Kleinreparaturen ohne Obergrenze", "inhalt": "Eine Kleinreparaturklausel ohne Angabe einer Höchstgrenze pro Einzelfall oder ohne Jahreshöchstgrenze ist insgesamt unwirksam. Der Mieter muss dann gar keine Kleinreparaturen bezahlen."},
    {"titel": "Wirksame Klausel: Kündigung wegen Pflichtverletzung", "inhalt": "Der Vermieter kann das Mietverhältnis außerordentlich kündigen, wenn der Mieter schuldhaft in erheblichem Maße seine Pflichten verletzt. Diese Klausel gibt nur das gesetzliche Kündigungsrecht wieder und ist wirksam."},
    {"titel": "Unwirksame Klausel: Automatische Mieterhöhung", "inhalt": "Eine Klausel, die automatische jährliche Mieterhöhungen um einen festen Prozentsatz vorsieht, ist bei Wohnraummietverträgen unwirksam. Mieterhöhungen müssen nach den gesetzlichen Vorschriften (§§ 557 ff. BGB) erfolgen."},
]

def main():
    print("Verbinde mit Qdrant Cloud...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, https=True)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente vorher: {info.points_count}")
    
    all_docs = []
    
    # BGB Mietrecht
    for item in BGB_MIETRECHT:
        text = f"{item['paragraph']}: {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['paragraph'], "type": "Gesetz", "category": "Mietrecht", "title": item['titel']}})
    
    # Checklisten
    for item in CHECKLISTEN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Checkliste", "category": "Praxis", "title": item['titel']}})
    
    # Rechtsprechung
    for item in RECHTSPRECHUNG:
        text = f"{item['aktenzeichen']} ({item['datum']}): {item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['aktenzeichen'], "type": "Rechtsprechung", "category": "BGH", "title": item['titel']}})
    
    # Vertragsklauseln
    for item in VERTRAGSKLAUSELN:
        text = f"{item['titel']}\n\n{item['inhalt']}"
        all_docs.append({"id": generate_id(text), "text": text, "metadata": {"source": item['titel'], "type": "Praxiswissen", "category": "Vertragsklauseln", "title": item['titel']}})
    
    print(f"Generiere Embeddings für {len(all_docs)} Dokumente...")
    
    points = []
    for i, doc in enumerate(all_docs):
        try:
            embedding = get_embedding(doc["text"])
            points.append(PointStruct(id=doc["id"], vector=embedding, payload={"text": doc["text"], **doc["metadata"]}))
            if (i + 1) % 10 == 0: print(f"  {i + 1}/{len(all_docs)}")
        except Exception as e:
            print(f"Fehler: {e}")
    
    print(f"Lade {len(points)} Dokumente hoch...")
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    
    info = client.get_collection(COLLECTION_NAME)
    print(f"Dokumente nachher: {info.points_count}")

if __name__ == "__main__":
    main()
