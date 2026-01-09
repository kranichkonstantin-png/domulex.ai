# 📎 Dokumenten-Upload & KI-Schriftsatzgenerator - Implementierungsplan

**Erstellt:** 29. Dezember 2025  
**Status:** In Planung  
**Priorität:** HOCH

---

## 🎯 Anforderungen Übersicht

### 1. **Multi-Format Dokumenten-Upload (Alle Nutzergruppen)**
- ✅ PDF, DOCX, TXT, JPG, PNG Upload im KI-Chat
- ✅ OCR für Bilder (Texterkennung)
- ✅ Dokumentenanalyse durch KI
- ✅ Integration in Chatkontext
- ✅ Verfügbar für: Basis, Professional, Lawyer Pro

### 2. **KI-basierter Schriftsatzgenerator (Lawyer Pro)**
- ✅ Template-Auswahl (Klagen, Mahnungen, Kündigungen, etc.)
- ✅ KI-gestützte Feld-Generierung
- ✅ Manueller + KI-Editor für Texte
- ✅ Word/PDF Export
- ✅ Import eigener Dokumente
- ✅ Integration mit Dokumentenmanagement

### 3. **Rechtsprechungserweiterung**
- ✅ EuGH bis AG: Vollständiges Immobilienrecht
- ✅ EuGH bis AG: Vollständiges Steuerrecht
- ✅ Alle einschlägigen Urteile

### 4. **Landingpage-Anpassung**
- ✅ Entferne "1.201 Dokumente"
- ✅ Ersetze durch Quellenauflistung

---

## 📋 Implementierungsplan

### **PHASE 1: Backend - Dokumenten-Upload System** 📎

#### A. Multi-Format File Upload API
```python
# /backend/main.py - Neuer Endpoint

@app.post("/upload/document")
async def upload_document(
    file: UploadFile,
    user_id: str = Depends(get_current_user),
    session_id: Optional[str] = None
) -> DocumentUploadResponse:
    """
    Upload und Parse Dokumente (PDF, DOCX, TXT, JPG, PNG)
    - OCR für Bilder
    - Text-Extraktion für PDFs/DOCX
    - Cloud Storage Upload
    - Embedding-Generierung für Suche
    """
    pass
```

**Benötigte Packages:**
- `python-multipart` (FastAPI file upload)
- `pytesseract` (OCR für Bilder)
- `python-docx` (DOCX parsing)
- `PyMuPDF` (PDF parsing - bereits vorhanden)
- `google-cloud-storage` (File storage)
- `Pillow` (Image processing)

**Cloud Storage Setup:**
```bash
# Google Cloud Storage Bucket
gsutil mb -l europe-west3 gs://domulex-user-documents
gsutil uniformbucketlevelaccess set on gs://domulex-user-documents
gsutil cors set cors.json gs://domulex-user-documents
```

#### B. Document Parser Service
```python
# /backend/services/document_parser.py

class DocumentParser:
    """Unified document parsing for all formats"""
    
    async def parse_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF"""
        pass
    
    async def parse_docx(self, file_bytes: bytes) -> str:
        """Extract text from DOCX"""
        pass
    
    async def parse_image_ocr(self, file_bytes: bytes) -> str:
        """OCR text extraction from images"""
        pass
    
    async def parse_document(
        self, 
        file: UploadFile
    ) -> DocumentParseResult:
        """Route to correct parser based on file type"""
        pass
```

#### C. Chat Context Integration
```python
# /backend/models/legal.py

class QueryRequest(BaseModel):
    query: str
    uploaded_documents: Optional[List[str]] = None  # Cloud Storage URLs
    
# /backend/rag/engine.py

async def query_with_documents(
    self,
    query: str,
    uploaded_docs: List[str]
) -> QueryResponse:
    """
    1. Download documents from Cloud Storage
    2. Parse and extract text
    3. Add to context window
    4. Query with RAG + uploaded context
    """
    pass
```

---

### **PHASE 2: Backend - KI-Schriftsatzgenerator** 📝

#### A. Template Engine
```python
# /backend/services/template_engine.py

class DocumentTemplate:
    """Juristische Dokumentvorlagen"""
    
    TEMPLATES = {
        "KLAGE": {
            "title": "Klage (Mietrecht)",
            "fields": [
                {"name": "klaeger", "type": "text", "ai_prompt": "Name des Klägers"},
                {"name": "beklagter", "type": "text", "ai_prompt": "Name des Beklagten"},
                {"name": "sachverhalt", "type": "long_text", "ai_prompt": "Sachverhalt aus Dokumenten"},
                {"name": "antraege", "type": "list", "ai_prompt": "Klageanträge"},
                {"name": "begruendung", "type": "long_text", "ai_prompt": "Rechtliche Begründung"}
            ],
            "template": """
AN DAS AMTSGERICHT {gericht}

KLAGE

In der Rechtssache

{klaeger}
- Kläger -

gegen

{beklagter}
- Beklagter -

wird Klage erhoben.

SACHVERHALT:
{sachverhalt}

KLAGEANTRÄGE:
{antraege}

BEGRÜNDUNG:
{begruendung}
"""
        },
        "MAHNUNG": {...},
        "KUENDIGUNG": {...},
        "MAENGELANZEIGE": {...}
    }

class SchriftsatzGenerator:
    """KI-gestützte Dokumentengenerierung"""
    
    async def generate_field_content(
        self,
        field_name: str,
        field_prompt: str,
        context_documents: List[str],
        user_input: Optional[str] = None
    ) -> str:
        """
        Nutzt Gemini 1.5 Pro um Feld-Inhalte zu generieren
        - Analysiert hochgeladene Dokumente
        - Verwendet RAG für rechtliche Grundlagen
        - Generiert rechtssichere Formulierungen
        """
        pass
    
    async def generate_document(
        self,
        template_id: str,
        field_values: Dict[str, str],
        context_documents: List[str]
    ) -> GeneratedDocument:
        """Generiert vollständiges Dokument"""
        pass
```

#### B. KI-Editor API
```python
# /backend/main.py

@app.post("/documents/generate")
async def generate_legal_document(
    request: DocumentGenerationRequest,
    user: User = Depends(require_lawyer_tier)
) -> GeneratedDocumentResponse:
    """
    Lawyer-only endpoint für Schriftsatzgenerierung
    """
    pass

@app.post("/documents/refine")
async def refine_document_section(
    request: DocumentRefineRequest,
    user: User = Depends(require_lawyer_tier)
) -> RefinedTextResponse:
    """
    KI-Textverbesserung für einzelne Abschnitte
    Prompt: "Formuliere professioneller", "Füge BGB-Zitate hinzu"
    """
    pass
```

#### C. Export Service (DOCX/PDF)
```python
# /backend/services/document_export.py

class DocumentExporter:
    """Export generierter Dokumente"""
    
    async def export_docx(
        self,
        content: str,
        template_id: str
    ) -> bytes:
        """
        Nutzt python-docx
        - Korrekte Formatierung
        - Header/Footer mit Kanzlei-Logo
        - Rechtsschrift-konforme Schriften
        """
        pass
    
    async def export_pdf(
        self,
        content: str,
        template_id: str
    ) -> bytes:
        """
        Nutzt ReportLab
        - PDF/A-konform
        - Druckfertig
        """
        pass
```

**Benötigte Packages:**
- `python-docx` (Word generation)
- `reportlab` (PDF generation)
- `jinja2` (Template rendering)

---

### **PHASE 3: Backend - Urteilsscraper Erweiterung** ⚖️

#### A. EuGH Scraper (Immobilien + Steuer)
```python
# /backend/ingestion/scrapers/eugh_scraper.py

class EuGHScraper:
    """
    Europäischer Gerichtshof - Rechtsprechungsdatenbank
    Quelle: https://curia.europa.eu
    """
    
    RECHTSGEBIETE = [
        "Grundfreiheiten (Wohnrecht)",
        "Verbraucherschutz (Mietrecht)",
        "Dienstleistungsfreiheit (Immobilien)",
        "Steuerrecht (Grunderwerbsteuer, Umsatzsteuer)"
    ]
    
    async def scrape_eugh_immobilien(self, max_docs: int = 50) -> List[Urteil]:
        """
        EuGH Urteile zu Immobilienrecht
        - Wohnrechte in EU
        - Verbraucherschutz
        - Grenzüberschreitende Immobilientransaktionen
        """
        pass
    
    async def scrape_eugh_steuer(self, max_docs: int = 50) -> List[Urteil]:
        """
        EuGH Urteile zu Steuerrecht (Immobilien)
        - Grunderwerbsteuer EU-weit
        - Umsatzsteuer auf Immobilien
        - Doppelbesteuerung
        """
        pass
```

#### B. Erweiterte AG-Scraper
```python
# /backend/ingestion/scrapers/ag_comprehensive_scraper.py

class AGComprehensiveScraper:
    """
    Amtsgerichte - Vollständige Immobilien- & Steuerrechtsprechung
    Quellen:
    - rechtsprechung-im-internet.de (filtert nach AG)
    - Landesjustizportale
    """
    
    async def scrape_ag_all_jurisdictions(self) -> List[Urteil]:
        """
        Alle AG-Urteile zu:
        - Mietrecht (Nebenkosten, Mängel, Kündigung)
        - WEG (Beschlüsse, Verwaltung)
        - Baurecht (Nachbarrecht, Grenzbebauung)
        - Steuerrecht (Grundsteuer, AfA-Streitigkeiten)
        
        Ziel: 200+ AG-Urteile
        """
        pass
```

#### C. Vollständigkeits-Scraper für alle Ebenen
```python
# /backend/ingestion/scrapers/comprehensive_case_law.py

class ComprehensiveCaseLawScraper:
    """
    Koordiniert alle Gerichtsebenen-Scraper
    Ziel: Vollständige Abdeckung
    """
    
    TARGETS = {
        "EuGH": {"immobilien": 50, "steuer": 50},
        "BGH": {"immobilien": 100, "steuer": 50},  # Bereits 23 vorhanden
        "OLG": {"immobilien": 80, "steuer": 30},
        "LG": {"immobilien": 60, "steuer": 20},
        "AG": {"immobilien": 200, "steuer": 50}
    }
    
    async def scrape_all(self) -> ScraperReport:
        """
        Führt alle Scraper aus, tracked Fortschritt
        Erwartet: 640 neue Urteile
        """
        pass
```

**Seed Script:**
```python
# /seed_comprehensive_case_law.py

async def main():
    """
    Seeds alle neuen Urteile in Qdrant
    Aktuell: 1.286 docs
    Ziel: 1.926+ docs
    """
    scraper = ComprehensiveCaseLawScraper()
    report = await scraper.scrape_all()
    
    # Upload to Qdrant mit Embeddings
    # ...
```

---

### **PHASE 4: Frontend - File Upload UI** 🖼️

#### A. File Upload Component
```typescript
// /src/components/FileUpload.tsx

interface FileUploadProps {
  onUpload: (fileUrl: string) => void;
  maxSize?: number; // MB
  allowedTypes: string[]; // ['pdf', 'docx', 'txt', 'jpg', 'png']
  tierRestrictions?: boolean;
}

export function FileUpload({ onUpload, allowedTypes }: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleDrop = useCallback(async (files: File[]) => {
    // Drag & Drop logic
    // Upload to backend /upload/document
    // Track progress
    // Return Cloud Storage URL
  }, []);

  return (
    <div className="file-upload-zone">
      {/* Dropzone with react-dropzone */}
      {/* File preview thumbnails */}
      {/* Upload progress bar */}
    </div>
  );
}
```

#### B. Chat Integration
```typescript
// /src/components/ChatInterface.tsx

const [uploadedDocs, setUploadedDocs] = useState<UploadedDocument[]>([]);

const handleDocumentUpload = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/api/upload/document', {
    method: 'POST',
    body: formData
  });
  
  const doc = await response.json();
  setUploadedDocs(prev => [...prev, doc]);
};

// In Chat Query:
const queryWithDocuments = async (message: string) => {
  await queryAPI({
    query: message,
    uploaded_documents: uploadedDocs.map(d => d.url)
  });
};
```

#### C. Document Preview
```typescript
// /src/components/DocumentPreview.tsx

export function DocumentPreview({ document }: { document: UploadedDocument }) {
  return (
    <div className="doc-preview">
      {/* PDF viewer with react-pdf */}
      {/* Image preview */}
      {/* Text excerpt */}
      {/* OCR status indicator */}
      <button onClick={() => removeDocument(document.id)}>
        Entfernen
      </button>
    </div>
  );
}
```

**Benötigte Packages (Frontend):**
- `react-dropzone` (bereits installiert!)
- `react-pdf` (PDF preview)
- `@react-pdf-viewer/core` (advanced PDF features)

---

### **PHASE 5: Frontend - Schriftsatzgenerator Dashboard** 📝

#### A. Template Selector
```typescript
// /src/components/legal-docs/TemplateSelector.tsx

const TEMPLATES = [
  {
    id: 'klage',
    name: 'Klage (Mietrecht)',
    icon: '⚖️',
    description: 'Klage vor dem Amtsgericht wegen Mietstreitigkeiten'
  },
  {
    id: 'mahnung',
    name: 'Zahlungsmahnung',
    icon: '💶',
    description: 'Außergerichtliche Mahnung für Mietrückstände'
  },
  // ... weitere Templates
];

export function TemplateSelector({ onSelect }: Props) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {TEMPLATES.map(template => (
        <TemplateCard 
          key={template.id}
          template={template}
          onClick={() => onSelect(template)}
        />
      ))}
    </div>
  );
}
```

#### B. AI-Assisted Form
```typescript
// /src/components/legal-docs/DocumentForm.tsx

export function DocumentForm({ 
  template, 
  uploadedDocs 
}: DocumentFormProps) {
  const [fields, setFields] = useState<FieldValue[]>([]);
  const [generating, setGenerating] = useState(false);

  const handleAIGenerate = async (fieldName: string) => {
    setGenerating(true);
    
    const response = await fetch('/api/documents/generate-field', {
      method: 'POST',
      body: JSON.stringify({
        template_id: template.id,
        field_name: fieldName,
        context_documents: uploadedDocs,
        user_input: fields[fieldName]
      })
    });
    
    const { content } = await response.json();
    setFields(prev => ({ ...prev, [fieldName]: content }));
    setGenerating(false);
  };

  return (
    <form className="space-y-6">
      {template.fields.map(field => (
        <div key={field.name} className="field-group">
          <label>{field.label}</label>
          {field.type === 'text' && (
            <input 
              value={fields[field.name] || ''}
              onChange={e => setFields({...fields, [field.name]: e.target.value})}
            />
          )}
          {field.type === 'long_text' && (
            <div className="relative">
              <textarea 
                rows={8}
                value={fields[field.name] || ''}
                onChange={e => setFields({...fields, [field.name]: e.target.value})}
              />
              <button
                type="button"
                onClick={() => handleAIGenerate(field.name)}
                className="absolute top-2 right-2 btn-ai"
              >
                <Sparkles /> KI generieren
              </button>
            </div>
          )}
        </div>
      ))}
      
      <button 
        type="submit"
        onClick={handleFullGenerate}
        className="btn-primary"
      >
        Dokument generieren
      </button>
    </form>
  );
}
```

#### C. Rich Text Editor mit KI-Refinement
```typescript
// /src/components/legal-docs/DocumentEditor.tsx

import { Editor } from '@tinymce/tinymce-react';

export function DocumentEditor({ 
  initialContent, 
  onSave 
}: DocumentEditorProps) {
  const [content, setContent] = useState(initialContent);
  const [selectedText, setSelectedText] = useState('');

  const handleAIRefine = async (action: 'improve' | 'add_citations' | 'formal') => {
    const response = await fetch('/api/documents/refine', {
      method: 'POST',
      body: JSON.stringify({
        text: selectedText,
        action: action
      })
    });
    
    const { refined } = await response.json();
    // Replace selectedText with refined version
  };

  return (
    <div className="document-editor">
      <div className="editor-toolbar">
        <button onClick={() => handleExport('docx')}>
          <FileWord /> Als Word exportieren
        </button>
        <button onClick={() => handleExport('pdf')}>
          <FilePdf /> Als PDF exportieren
        </button>
        <button onClick={handleAIRefine}>
          <Sparkles /> Mit KI verbessern
        </button>
      </div>
      
      <Editor
        value={content}
        onEditorChange={setContent}
        onSelectionChange={setSelectedText}
        init={{
          height: 600,
          menubar: false,
          plugins: ['lists', 'link', 'table', 'wordcount'],
          toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright | bullist numlist'
        }}
      />
    </div>
  );
}
```

**Benötigte Packages (Frontend):**
- `@tinymce/tinymce-react` (WYSIWYG Editor)
- `lucide-react` (Icons)

---

### **PHASE 6: Frontend - Landingpage Anpassung** 🌐

#### A. Quellenauflistung statt Dokumentenzahl
```typescript
// /src/app/page.tsx - Zeile 218-224 ersetzen

// ALT:
<div className="text-center">
  <div className="text-3xl font-bold text-[#1e3a5f]">1.201</div>
  <div className="text-sm text-gray-500">Rechtsdokumente</div>
</div>

// NEU:
<div className="text-center">
  <div className="space-y-2">
    <div className="text-sm font-semibold text-[#1e3a5f]">Rechtsquellen</div>
    <div className="text-xs text-gray-500 space-y-1">
      <div>✓ BGB, WEG, ZPO, EStG</div>
      <div>✓ BGH, BFH, OLG, LG, AG</div>
      <div>✓ EuGH, BMF, Literatur</div>
    </div>
  </div>
</div>
```

#### B. Features-Sektion erweitern
```typescript
// Zeile 284 - Feature-Beschreibung aktualisieren

{
  icon: '📚',
  title: 'Umfassende Rechtsquellen',
  description: 'Gesetze (BGB, WEG, ZPO, EStG), Rechtsprechung (EuGH-AG), Literatur (Kommentare, Handbücher) und BMF-Schreiben. Alle Quellen mit Fundstellen.'
}
```

---

### **PHASE 7: Testing & Deployment** 🚀

#### A. Backend Tests
```python
# /backend/tests/test_document_upload.py

def test_upload_pdf():
    """Test PDF upload and parsing"""
    pass

def test_upload_image_ocr():
    """Test image upload with OCR"""
    pass

def test_document_generation():
    """Test Schriftsatz generation"""
    pass

def test_docx_export():
    """Test DOCX export functionality"""
    pass
```

#### B. Frontend Tests
```typescript
// /src/__tests__/FileUpload.test.tsx

describe('FileUpload', () => {
  it('should upload PDF files', async () => {});
  it('should reject invalid file types', async () => {});
  it('should show upload progress', async () => {});
});
```

#### C. Integration Tests
```bash
# Test vollständiger Workflow
1. User uploads PDF
2. OCR extracts text
3. Text wird in Chat-Context hinzugefügt
4. Query mit Dokumentenkontext
5. Antwort enthält Informationen aus uploaded PDF
```

#### D. Deployment Checklist
- [ ] Backend: Cloud Storage Setup
- [ ] Backend: Tesseract OCR installiert
- [ ] Backend: python-docx, reportlab installiert
- [ ] Backend: Neue Endpoints deployed
- [ ] Frontend: react-dropzone, @tinymce/tinymce-react installiert
- [ ] Frontend: FileUpload component integriert
- [ ] Frontend: DocumentEditor component integriert
- [ ] Frontend: Landingpage aktualisiert
- [ ] Database: Neue Urteile geseedet (640+ neue Dokumente)
- [ ] Testing: E2E Tests bestanden
- [ ] Documentation: API-Docs aktualisiert

---

## 📊 Zeitplan & Ressourcen

### Geschätzter Aufwand:
| Phase | Backend | Frontend | Testing | Total |
|-------|---------|----------|---------|-------|
| Dokumenten-Upload | 8h | 6h | 2h | 16h |
| Schriftsatzgenerator | 12h | 10h | 3h | 25h |
| Urteilsscraper | 6h | - | 2h | 8h |
| Landingpage | - | 2h | 1h | 3h |
| **TOTAL** | **26h** | **18h** | **8h** | **52h** |

### Meilensteine:
1. ✅ **Woche 1:** Dokumenten-Upload Backend + Frontend (16h)
2. ✅ **Woche 2:** Schriftsatzgenerator Backend (12h)
3. ✅ **Woche 3:** Schriftsatzgenerator Frontend (10h)
4. ✅ **Woche 4:** Urteilsscraper + Landingpage + Testing (14h)

**Deployment:** Ende Woche 4

---

## 🔒 Sicherheit & Compliance

### Datenschutz (DSGVO)
- ✅ Hochgeladene Dokumente werden verschlüsselt gespeichert
- ✅ Cloud Storage mit IAM-Berechtigungen (nur user hat Zugriff)
- ✅ Automatische Löschung nach 90 Tagen Inaktivität
- ✅ Keine Verwendung für KI-Training

### Tier-Restrictions
| Feature | Basis | Professional | Lawyer Pro |
|---------|-------|--------------|------------|
| Dokumenten-Upload | ✅ 3 Docs | ✅ 20 Docs | ✅ Unbegrenzt |
| OCR | ✅ | ✅ | ✅ |
| Schriftsatzgenerierung | ❌ | ❌ | ✅ |
| Word/PDF Export | ❌ | ❌ | ✅ |
| Template-Editor | ❌ | ❌ | ✅ |

---

## 📈 Erfolgskriterien

### Technisch:
- [ ] Upload-Success-Rate > 98%
- [ ] OCR-Genauigkeit > 95% (deutsche Texte)
- [ ] Schriftsatz-Generierung < 30 Sekunden
- [ ] DOCX/PDF Export < 5 Sekunden

### Business:
- [ ] 50% der Lawyer-Tier nutzt Schriftsatzgenerator
- [ ] Durchschnittlich 5 Dokumente pro User hochgeladen
- [ ] NPS > 8 für Dokumenten-Features

### Rechtsprechungsdatenbank:
- [ ] 1.926+ Dokumente in Qdrant (aktuell: 1.286)
- [ ] EuGH: 100 Urteile
- [ ] BGH/BFH: 150 Urteile
- [ ] OLG: 110 Urteile
- [ ] LG: 80 Urteile
- [ ] AG: 250 Urteile

---

## 🚀 Next Steps

1. **Sofort:** Cloud Storage Setup
2. **Tag 1-3:** Backend Dokumenten-Upload implementieren
3. **Tag 4-6:** Frontend FileUpload Component
4. **Tag 7-10:** Schriftsatzgenerator Backend
5. **Tag 11-14:** Schriftsatzgenerator Frontend
6. **Tag 15-18:** Urteilsscraper Erweiterung
7. **Tag 19-20:** Landingpage + Testing
8. **Tag 21:** Deployment

**Geschätzter Launch:** ~3 Wochen

---

**Erstellt für:** domulex.ai  
**Version:** 1.0  
**Letzte Aktualisierung:** 29. Dezember 2025
