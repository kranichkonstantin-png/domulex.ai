#!/usr/bin/env python3
"""BGB Sachenrecht komplett"""

import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import uuid

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
client = QdrantClient(host=os.environ['QDRANT_HOST'], port=6333, api_key=os.environ['QDRANT_API_KEY'], https=True)

def embed(text):
    return genai.embed_content(model='models/text-embedding-004', content=text[:8000])['embedding']

print('🚀 BGB SACHENRECHT SEEDING')

bgb_sr = [
    # Eigentum §§ 903-924
    {'title': 'BGB § 903 - Befugnisse des Eigentümers', 'content': 'Der Eigentümer einer Sache kann, soweit nicht das Gesetz oder Rechte Dritter entgegenstehen, mit der Sache nach Belieben verfahren und andere von jeder Einwirkung ausschließen. Der Eigentümer eines Tieres hat bei der Ausübung seiner Befugnisse die besonderen Vorschriften zum Schutz der Tiere zu beachten.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 904 - Notstand', 'content': 'Der Eigentümer einer Sache ist nicht berechtigt, die Einwirkung eines anderen auf die Sache zu verbieten, wenn die Einwirkung zur Abwendung einer gegenwärtigen Gefahr notwendig und der drohende Schaden gegenüber dem aus der Einwirkung entstehenden Schaden unverhältnismäßig groß ist. Der Eigentümer kann Ersatz des ihm entstehenden Schadens verlangen.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 905 - Begrenzung des Eigentums', 'content': 'Das Recht des Eigentümers eines Grundstücks erstreckt sich auf den Raum über der Oberfläche und auf den Erdkörper unter der Oberfläche. Der Eigentümer kann jedoch Einwirkungen nicht verbieten, die in solcher Höhe oder Tiefe vorgenommen werden, dass er an der Ausschließung kein Interesse hat.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 906 - Zuführung unwägbarer Stoffe', 'content': 'Der Eigentümer eines Grundstücks kann die Zuführung von Gasen, Dämpfen, Gerüchen, Rauch, Ruß, Wärme, Geräusch, Erschütterungen und ähnliche von einem anderen Grundstück ausgehende Einwirkungen insoweit nicht verbieten, als die Einwirkung die Benutzung seines Grundstücks nicht oder nur unwesentlich beeinträchtigt. Eine wesentliche Beeinträchtigung liegt nicht vor, wenn die Einwirkung ortsüblich und nicht durch wirtschaftlich zumutbare Maßnahmen vermeidbar ist.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 907 - Anlagen auf Nachbargrundstücken', 'content': 'Der Eigentümer eines Grundstücks kann verlangen, dass auf den Nachbargrundstücken nicht Anlagen hergestellt oder gehalten werden, von denen mit Sicherheit vorauszusehen ist, dass ihr Bestand oder ihre Benutzung eine unzulässige Einwirkung auf sein Grundstück zur Folge hat.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 909 - Vertiefung', 'content': 'Ein Grundstück darf nicht in der Weise vertieft werden, dass der Boden des Nachbargrundstücks die erforderliche Stütze verliert, es sei denn, dass für eine genügende anderweitige Befestigung gesorgt ist.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 910 - Überhang', 'content': 'Der Eigentümer eines Grundstücks kann Wurzeln eines Baumes oder eines Strauches, die von einem Nachbargrundstück eingedrungen sind, abschneiden und behalten. Das Gleiche gilt von herüberragenden Zweigen, wenn der Eigentümer dem Besitzer des Nachbargrundstücks eine angemessene Frist zur Beseitigung bestimmt hat und die Beseitigung nicht innerhalb der Frist erfolgt.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 911 - Überfall', 'content': 'Früchte, die von einem Baume oder einem Strauche auf ein Nachbargrundstück hinüberfallen, gelten als Früchte dieses Grundstücks. Diese Vorschrift findet keine Anwendung, wenn das Nachbargrundstück dem öffentlichen Gebrauch dient.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 912 - Überbau', 'content': 'Hat der Eigentümer eines Grundstücks bei der Errichtung eines Gebäudes über die Grenze gebaut, ohne dass ihm Vorsatz oder grobe Fahrlässigkeit zur Last fällt, so hat der Nachbar den Überbau zu dulden, es sei denn, dass er vor oder sofort nach der Grenzüberschreitung Widerspruch erhoben hat. Der Nachbar ist durch eine Geldrente zu entschädigen.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 917 - Notweg', 'content': 'Fehlt einem Grundstück die zur ordnungsmäßigen Benutzung notwendige Verbindung mit einem öffentlichen Wege, so kann der Eigentümer von den Nachbarn verlangen, dass sie bis zur Hebung des Mangels die Benutzung ihrer Grundstücke zur Herstellung der erforderlichen Verbindung dulden. Die Richtung des Notwegs und der Umfang des Benutzungsrechts werden erforderlichenfalls durch Urteil bestimmt.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 919 - Grenzabmarkung', 'content': 'Der Eigentümer eines Grundstücks kann von dem Eigentümer eines Nachbargrundstücks verlangen, dass dieser zur Errichtung fester Grenzzeichen und, wenn ein Grenzzeichen verrückt oder unkenntlich geworden ist, zur Wiederherstellung mitwirkt. Die Art der Abmarkung und das Verfahren bestimmen sich nach den Landesgesetzen.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 921 - Gemeinschaftliche Benutzung von Grenzanlagen', 'content': 'Werden zwei Grundstücke durch einen Zwischenraum, Rain, Winkel, einen Graben, eine Mauer, Hecke, Planke oder eine andere Einrichtung, die zum Vorteil beider Grundstücke dient, voneinander geschieden, so wird vermutet, dass die Eigentümer der Grundstücke zur Benutzung der Einrichtung gemeinschaftlich berechtigt sind.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    
    # Erwerb und Verlust des Eigentums an Grundstücken §§ 925-928
    {'title': 'BGB § 925 - Auflassung', 'content': 'Die zur Übertragung des Eigentums an einem Grundstück nach § 873 erforderliche Einigung des Veräußerers und des Erwerbers (Auflassung) muss bei gleichzeitiger Anwesenheit beider Teile vor einer zuständigen Stelle erklärt werden. Zur Entgegennahme der Auflassung ist, unbeschadet der Zuständigkeit weiterer Stellen, jeder Notar zuständig.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 925a - Vorlage der Genehmigung', 'content': 'Bei der Auflassung soll das Grundbuchamt die Genehmigung der Behörde einholen, wenn das Grundstück in einem Sanierungsgebiet, einem förmlich festgelegten Entwicklungsbereich oder einem Umlegungsgebiet liegt.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 926 - Zubehör', 'content': 'Sind bei der Veräußerung eines Grundstücks dem Grundstück dienende bewegliche Sachen mitveräußert, so erstreckt sich die für den Erwerb des Grundstücks vorgenommene Eintragung auf diese Sachen, auch wenn sie dem Erwerber noch nicht übergeben sind.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 927 - Aufgebot des Eigentümers', 'content': 'Der Eigentümer eines Grundstücks kann, wenn das Grundstück seit 30 Jahren im Eigenbesitz eines anderen ist, durch Aufgebot ausgeschlossen werden. Der Eigenbesitzer kann alsdann das Eigentum erwerben.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 928 - Aufgabe des Eigentums', 'content': 'Das Eigentum an einem Grundstück kann dadurch aufgegeben werden, dass der Eigentümer den Verzicht dem Grundbuchamt gegenüber erklärt und der Verzicht in das Grundbuch eingetragen wird. Das Recht zur Aneignung des aufgegebenen Grundstücks steht dem Fiskus des Landes zu.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    
    # Erwerb und Verlust des Eigentums an beweglichen Sachen §§ 929-984
    {'title': 'BGB § 929 - Einigung und Übergabe', 'content': 'Zur Übertragung des Eigentums an einer beweglichen Sache ist erforderlich, dass der Eigentümer die Sache dem Erwerber übergibt und beide darüber einig sind, dass das Eigentum übergehen soll. Ist der Erwerber im Besitz der Sache, so genügt die Einigung über den Übergang des Eigentums.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 932 - Gutgläubiger Erwerb vom Nichtberechtigten', 'content': 'Durch eine nach § 929 erfolgte Veräußerung wird der Erwerber auch dann Eigentümer, wenn die Sache nicht dem Veräußerer gehört, es sei denn, dass er zu der Zeit, zu der er nach diesen Vorschriften das Eigentum erwerben würde, nicht in gutem Glauben ist. Der Erwerber ist nicht in gutem Glauben, wenn ihm bekannt oder infolge grober Fahrlässigkeit unbekannt ist, dass die Sache nicht dem Veräußerer gehört.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 946 - Verbindung mit einem Grundstück', 'content': 'Wird eine bewegliche Sache mit einem Grundstück dergestalt verbunden, dass sie wesentlicher Bestandteil des Grundstücks wird, so erstreckt sich das Eigentum an dem Grundstück auf diese Sache.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 985 - Herausgabeanspruch', 'content': 'Der Eigentümer kann von dem Besitzer die Herausgabe der Sache verlangen.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1004 - Beseitigungs- und Unterlassungsanspruch', 'content': 'Wird das Eigentum in anderer Weise als durch Entziehung oder Vorenthaltung des Besitzes beeinträchtigt, so kann der Eigentümer von dem Störer die Beseitigung der Beeinträchtigung verlangen. Sind weitere Beeinträchtigungen zu besorgen, so kann der Eigentümer auf Unterlassung klagen.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    
    # Dienstbarkeiten §§ 1018-1093
    {'title': 'BGB § 1018 - Grunddienstbarkeit', 'content': 'Ein Grundstück kann zugunsten des jeweiligen Eigentümers eines anderen Grundstücks in der Weise belastet werden, dass dieser das Grundstück in einzelnen Beziehungen benutzen darf oder dass auf dem Grundstück gewisse Handlungen nicht vorgenommen werden dürfen oder dass die Ausübung eines Rechts ausgeschlossen ist.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1030 - Nießbrauch an Sachen', 'content': 'Eine Sache kann in der Weise belastet werden, dass derjenige, zu dessen Gunsten die Belastung erfolgt, berechtigt ist, die Nutzungen der Sache zu ziehen (Nießbrauch). Der Nießbrauch kann durch den Ausschluss einzelner Nutzungen beschränkt werden.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1090 - Beschränkte persönliche Dienstbarkeit', 'content': 'Ein Grundstück kann in der Weise belastet werden, dass derjenige, zu dessen Gunsten die Belastung erfolgt, berechtigt ist, das Grundstück in einzelnen Beziehungen zu benutzen, oder dass ihm eine sonstige Befugnis zusteht.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1093 - Wohnungsrecht', 'content': 'Als beschränkte persönliche Dienstbarkeit kann auch das Recht bestellt werden, ein Gebäude oder einen Teil eines Gebäudes unter Ausschluss des Eigentümers als Wohnung zu benutzen. Der Berechtigte ist befugt, seine Familie sowie die zur standesmäßigen Bedienung und zur Pflege erforderlichen Personen in die Wohnung aufzunehmen.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    
    # Reallasten, Vorkaufsrecht, Hypothek §§ 1105-1203
    {'title': 'BGB § 1105 - Reallast', 'content': 'Ein Grundstück kann in der Weise belastet werden, dass an denjenigen, zu dessen Gunsten die Belastung erfolgt, wiederkehrende Leistungen aus dem Grundstück zu entrichten sind (Reallast). Als Inhalt der Reallast kann auch vereinbart werden, dass die Leistungen in bestimmter Höhe zu entrichten sind.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1094 - Dingliches Vorkaufsrecht', 'content': 'Ein Grundstück kann in der Weise belastet werden, dass derjenige, zu dessen Gunsten die Belastung erfolgt, dem Eigentümer gegenüber zum Vorkauf berechtigt ist.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1113 - Hypothek', 'content': 'Ein Grundstück kann in der Weise belastet werden, dass an denjenigen, zu dessen Gunsten die Belastung erfolgt, eine bestimmte Geldsumme zur Befriedigung wegen einer ihm zustehenden Forderung aus dem Grundstück zu zahlen ist (Hypothek).', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1191 - Grundschuld', 'content': 'Ein Grundstück kann in der Weise belastet werden, dass an denjenigen, zu dessen Gunsten die Belastung erfolgt, eine bestimmte Geldsumme aus dem Grundstück zu zahlen ist (Grundschuld). Die Belastung kann auch in der Weise erfolgen, dass Zinsen von der Geldsumme zu entrichten sind.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
    {'title': 'BGB § 1199 - Rentenschuld', 'content': 'Ein Grundstück kann in der Weise belastet werden, dass in regelmäßig wiederkehrenden Terminen eine bestimmte Geldsumme aus dem Grundstück zu zahlen ist (Rentenschuld). Bei der Bestellung der Rentenschuld muss der Betrag bestimmt werden, durch dessen Zahlung die Rentenschuld abgelöst werden kann.', 'source': 'BGB', 'category': 'Sachenrecht', 'doc_type': 'Gesetz'},
]

print(f'📤 Uploading {len(bgb_sr)} Dokumente...')
points = []
for i, doc in enumerate(bgb_sr):
    vector = embed(doc['content'])
    points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=doc))
    if (i+1) % 10 == 0:
        print(f'  📝 {i+1}/{len(bgb_sr)} embedded...')

for i in range(0, len(points), 25):
    batch = points[i:i+25]
    client.upsert(collection_name='legal_documents', points=batch)
    print(f'  ✅ Batch {i//25+1}: {len(batch)} docs')

info = client.get_collection('legal_documents')
print(f'📊 Gesamt: {info.points_count} Dokumente')
