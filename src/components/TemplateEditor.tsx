'use client';

import { useState, useRef } from 'react';

interface TemplateEditorProps {
  template: {
    id: string;
    name: string;
    content: string;
  };
  onClose: () => void;
  onSave: (content: string) => void;
  userTier?: string;  // Neu: user_tier für erweiterte KI-Leistung
  onQueryUsed?: () => void;  // Callback wenn KI-Anfrage verbraucht wird
  queriesRemaining?: number;  // Verbleibende Anfragen
}

export default function TemplateEditor({ template, onClose, onSave, userTier, onQueryUsed, queriesRemaining }: TemplateEditorProps) {
  const [content, setContent] = useState(template.content);
  const [isProcessing, setIsProcessing] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [extractedText, setExtractedText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'manual' | 'ai' | 'upload'>('ai');
  const [useGeneralKnowledge, setUseGeneralKnowledge] = useState(false);  // 🔑 NEU: Toggle für allgemeines KI-Wissen
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-lytuxcyyka-ey.a.run.app';
  
  // 🔑 Anwalt hat erweiterte KI-Leistung
  const isLawyer = userTier === 'lawyer';

  const handleExtractDocument = async (file: File) => {
    setIsProcessing(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch(`${API_URL}/templates/extract-document`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Fehler beim Extrahieren des Dokuments');
      }

      const data = await response.json();
      setExtractedText(data.text);
      setSuccess(`✅ ${data.char_count.toLocaleString()} Zeichen aus "${data.filename}" extrahiert`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Fehler beim Extrahieren');
      setExtractedText(null);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAIFill = async () => {
    if (!userInput.trim() && !extractedText) {
      setError('Bitte geben Sie Ihre Daten ein oder laden Sie ein Dokument hoch.');
      return;
    }

    // Check query limit for non-lawyer users
    if (userTier !== 'lawyer' && queriesRemaining !== undefined && queriesRemaining <= 0) {
      setError('Sie haben Ihr Anfrage-Kontingent aufgebraucht. Bitte upgraden Sie Ihren Tarif für weitere KI-Vorlagen.');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setSuccess(null);

    try {
      const requestBody = {
        template_content: template.content,
        template_name: template.name,
        instructions: userInput.trim() || 'Fülle die Vorlage mit den extrahierten Daten aus.',
        document_text: extractedText || undefined,
        user_tier: userTier,  // 🔑 Anwalt bekommt erweiterte KI-Leistung
        use_general_knowledge: isLawyer ? useGeneralKnowledge : false,  // 🔑 NEU: Allgemeines KI-Wissen (nur Lawyer)
      };

      const response = await fetch(`${API_URL}/templates/fill`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Fehler bei der KI-Verarbeitung');
      }

      const data = await response.json();
      setContent(data.filled_content);
      setSuccess(`✅ Vorlage ausgefüllt! Änderungen: ${data.changes_made.join(', ')}`);
      
      // Increment query count for non-lawyer users
      if (userTier !== 'lawyer' && onQueryUsed) {
        onQueryUsed();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ein Fehler ist aufgetreten');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check file type - alle gängigen Formate
      const allowedTypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
        'text/csv',
        'text/rtf',
        'text/html',
        'application/rtf',
        'application/xml',
        'image/jpeg',
        'image/png',
        'image/webp',
        'image/tiff',
        'message/rfc822'
      ];
      if (!allowedTypes.includes(file.type)) {
        setError('Nicht unterstütztes Dateiformat. Erlaubt: PDF, Word, Excel, Bilder, Text, CSV, HTML, XML, E-Mail');
        return;
      }
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError('Datei zu groß. Maximal 10MB erlaubt.');
        return;
      }
      setUploadedFile(file);
      setError(null);
      // Auto-extract text from the document
      await handleExtractDocument(file);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${template.name.replace(/\s+/g, '_')}_ausgefuellt.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-[#1e3a5f]">
              🤖 Vorlage mit KI anpassen
            </h2>
            <p className="text-sm text-gray-500 mt-1">{template.name}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden flex">
          {/* Left Panel - Input */}
          <div className="w-1/2 border-r border-gray-200 flex flex-col">
            {/* Tabs */}
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('ai')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'ai'
                    ? 'text-[#1e3a5f] border-b-2 border-[#1e3a5f] bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                🤖 KI-Assistent
              </button>
              <button
                onClick={() => setActiveTab('upload')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'upload'
                    ? 'text-[#1e3a5f] border-b-2 border-[#1e3a5f] bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📄 Dokument hochladen
              </button>
              <button
                onClick={() => setActiveTab('manual')}
                className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'manual'
                    ? 'text-[#1e3a5f] border-b-2 border-[#1e3a5f] bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                ✏️ Manuell bearbeiten
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
              {activeTab === 'ai' && (
                <div className="space-y-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-sm text-blue-800">
                      <strong>💡 So funktioniert's:</strong><br />
                      Geben Sie Ihre Daten ein und die KI füllt die Vorlage automatisch aus.
                      Sie können auch ein Dokument hochladen, aus dem die Daten extrahiert werden.
                    </p>
                  </div>

                  {isLawyer && (
                    <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-300 rounded-lg p-4 shadow-sm">
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">⚖️</span>
                        <div className="flex-1">
                          <p className="text-sm font-semibold text-amber-900 mb-2">
                            Quellenauswahl für Vorlagenbearbeitung
                          </p>
                          
                          {/* Toggle für allgemeines KI-Wissen */}
                          <label className="flex items-center justify-between cursor-pointer group p-3 bg-white rounded-lg border border-amber-200">
                            <div>
                              <p className="text-sm font-medium text-gray-700 group-hover:text-[#1e3a5f] transition-colors">
                                {useGeneralKnowledge ? '🔴 Allgemeines KI-Wissen aktiv' : '🟢 Verlässliche Datenbank aktiv'}
                              </p>
                              <p className="text-xs text-gray-500 mt-1">
                                {useGeneralKnowledge 
                                  ? 'Allgemeines Trainingswissen der KI (erhöhtes Halluzinationsrisiko)'
                                  : 'Nur geprüfte Datenbank: Gesetze, Urteile, BMF-Schreiben, Kommentare'}
                              </p>
                            </div>
                            <div className="relative ml-4">
                              <input
                                type="checkbox"
                                checked={useGeneralKnowledge}
                                onChange={(e) => setUseGeneralKnowledge(e.target.checked)}
                                className="sr-only peer"
                              />
                              <div className="w-11 h-6 bg-green-500 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-amber-200 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500"></div>
                            </div>
                          </label>
                          
                          {useGeneralKnowledge && (
                            <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded">
                              <p className="text-xs font-bold text-red-900 mb-1">
                                ⚠️ WARNUNG: Allgemeines KI-Wissen aktiv
                              </p>
                              <p className="text-xs text-red-700">
                                Die KI nutzt allgemeines Trainingswissen statt der verlässlichen Datenbank.
                                <strong> Prüfen Sie ALLE Paragraphen, Urteile und Fakten nach!</strong>
                              </p>
                            </div>
                          )}
                          
                          {!useGeneralKnowledge && (
                            <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded">
                              <p className="text-xs font-bold text-green-900 mb-1">
                                ✅ Verlässliche Datenbank aktiv
                              </p>
                              <p className="text-xs text-green-700">
                                Nur geprüfte Quellen: BGB, WEG, BauGB, EStG + Höchstgerichte (BGH, BFH, EuGH) + BMF-Schreiben
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Ihre Daten und Anweisungen
                    </label>
                    <textarea
                      value={userInput}
                      onChange={(e) => setUserInput(e.target.value)}
                      placeholder={`Beispiel:
- Mein Name: Hans Müller
- Adresse: Hauptstraße 10, 10115 Berlin
- Vermieter: Immobilien GmbH, Berliner Str. 5
- Mietbeginn: 01.01.2024
- Mangel: Schimmel im Bad seit 2 Wochen
- Mietminderung: 20%`}
                      className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent resize-none text-sm"
                    />
                  </div>

                  {uploadedFile && (
                    <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <span className="text-green-600">📎</span>
                      <span className="text-sm text-green-800 flex-1">{uploadedFile.name}</span>
                      <button
                        onClick={() => setUploadedFile(null)}
                        className="text-green-600 hover:text-green-800"
                      >
                        ✕
                      </button>
                    </div>
                  )}

                  <button
                    onClick={handleAIFill}
                    disabled={isProcessing}
                    className={`w-full py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 ${
                      isProcessing
                        ? 'bg-gray-300 cursor-not-allowed'
                        : 'bg-[#1e3a5f] text-white hover:bg-[#2d4a6f]'
                    }`}
                  >
                    {isProcessing ? (
                      <>
                        <span className="animate-spin">⚙️</span>
                        KI verarbeitet...
                      </>
                    ) : (
                      <>
                        🤖 Mit KI ausfüllen
                      </>
                    )}
                  </button>
                </div>
              )}

              {activeTab === 'upload' && (
                <div className="space-y-4">
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                    <p className="text-sm text-amber-800">
                      <strong>📄 Dokument-Upload:</strong><br />
                      Laden Sie einen bestehenden Vertrag, Brief oder Dokument hoch.
                      Die KI extrahiert die relevanten Daten und füllt die Vorlage aus.
                    </p>
                  </div>

                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-[#1e3a5f] hover:bg-gray-50 transition-colors"
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      onChange={handleFileUpload}
                      accept=".pdf,.doc,.docx,.txt,.rtf,.xls,.xlsx,.csv,.jpg,.jpeg,.png,.webp,.tiff,.tif,.eml,.xml,.html,.htm"
                      className="hidden"
                    />
                    <div className="text-4xl mb-3">📁</div>
                    <p className="text-gray-600 font-medium">
                      Klicken oder Datei hierher ziehen
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      PDF, Word, Excel, Bilder, CSV, HTML & mehr (max. 10MB)
                    </p>
                  </div>

                  {uploadedFile && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">📄</span>
                        <div className="flex-1">
                          <p className="font-medium text-green-800">{uploadedFile.name}</p>
                          <p className="text-sm text-green-600">
                            {(uploadedFile.size / 1024).toFixed(1)} KB
                          </p>
                        </div>
                        <button
                          onClick={() => {
                            setUploadedFile(null);
                            setExtractedText(null);
                          }}
                          className="text-green-600 hover:text-green-800"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  )}

                  {extractedText && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <p className="text-sm font-medium text-blue-800 mb-2">
                        ✅ Extrahierter Text ({extractedText.length.toLocaleString()} Zeichen):
                      </p>
                      <div className="max-h-32 overflow-y-auto text-xs text-blue-700 bg-white p-2 rounded border border-blue-100">
                        {extractedText.substring(0, 500)}
                        {extractedText.length > 500 && '...'}
                      </div>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Zusätzliche Anweisungen (optional)
                    </label>
                    <textarea
                      value={userInput}
                      onChange={(e) => setUserInput(e.target.value)}
                      placeholder="z.B. 'Verwende die Adresse des Mieters aus dem Dokument' oder 'Die Miete soll auf 950€ geändert werden'"
                      className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent resize-none text-sm"
                    />
                  </div>

                  <button
                    onClick={handleAIFill}
                    disabled={isProcessing || !extractedText}
                    className={`w-full py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 ${
                      isProcessing || !extractedText
                        ? 'bg-gray-300 cursor-not-allowed'
                        : 'bg-[#1e3a5f] text-white hover:bg-[#2d4a6f]'
                    }`}
                  >
                    {isProcessing ? (
                      <>
                        <span className="animate-spin">⚙️</span>
                        Vorlage wird ausgefüllt...
                      </>
                    ) : (
                      <>
                        🤖 Vorlage mit Daten ausfüllen
                      </>
                    )}
                  </button>
                </div>
              )}

              {activeTab === 'manual' && (
                <div className="space-y-4">
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <p className="text-sm text-gray-600">
                      <strong>✏️ Manuelle Bearbeitung:</strong><br />
                      Bearbeiten Sie die Vorlage direkt im Textfeld rechts.
                      Alle Änderungen werden sofort übernommen.
                    </p>
                  </div>
                  
                  <div className="text-sm text-gray-500">
                    <p className="font-medium mb-2">Typische Platzhalter:</p>
                    <ul className="space-y-1 text-xs">
                      <li>• Max Mustermann → Ihr Name</li>
                      <li>• Musterstraße 12 → Ihre Adresse</li>
                      <li>• 12345 Berlin → Ihre PLZ und Stadt</li>
                      <li>• Immobilien Schmidt GmbH → Ihr Vermieter</li>
                      <li>• 850,00 € → Ihre Beträge</li>
                    </ul>
                  </div>
                </div>
              )}

              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-800">❌ {error}</p>
                </div>
              )}

              {success && (
                <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm text-green-800">{success}</p>
                </div>
              )}
            </div>
          </div>

          {/* Right Panel - Editor */}
          <div className="w-1/2 flex flex-col">
            <div className="p-4 border-b border-gray-200 bg-gray-50">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">
                  📝 Vorschau & Bearbeitung
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={handleCopy}
                    className="px-3 py-1.5 text-xs bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    📋 Kopieren
                  </button>
                  <button
                    onClick={handleDownload}
                    className="px-3 py-1.5 text-xs bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    ⬇️ Download
                  </button>
                </div>
              </div>
            </div>
            <div className="flex-1 p-4">
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="w-full h-full p-4 border border-gray-300 rounded-lg font-mono text-sm resize-none focus:ring-2 focus:ring-[#1e3a5f] focus:border-transparent"
                style={{ minHeight: '400px' }}
              />
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 bg-gray-50 flex items-center justify-between">
          <div className="text-xs text-gray-500">
            ⚠️ Dies ist keine Rechtsberatung. Prüfen Sie das Dokument vor der Verwendung.
          </div>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-100"
            >
              Abbrechen
            </button>
            <button
              onClick={() => onSave(content)}
              className="px-6 py-2 text-sm bg-[#b8860b] text-white rounded-lg hover:bg-[#9a7209] font-medium"
            >
              ✓ Speichern & Verwenden
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
