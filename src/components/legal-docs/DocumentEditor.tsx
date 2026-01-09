'use client';

import { useState } from 'react';

interface DocumentEditorProps {
  content: string;
  templateId: string;
  onExport: (format: 'docx' | 'pdf', kanzleiName?: string, kanzleiAdresse?: string) => void;
  onBack: () => void;
}

export function DocumentEditor({ content, templateId, onExport, onBack }: DocumentEditorProps) {
  const [editedContent, setEditedContent] = useState(content);
  const [kanzleiName, setKanzleiName] = useState('');
  const [kanzleiAdresse, setKanzleiAdresse] = useState('');
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format: 'docx' | 'pdf') => {
    setExporting(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/documents/export`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: editedContent,
            template_id: templateId,
            format,
            kanzlei_name: kanzleiName || undefined,
            kanzlei_adresse: kanzleiAdresse || undefined,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('Export fehlgeschlagen');
      }

      // Download file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${templateId}_${new Date().toISOString().split('T')[0]}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      onExport(format, kanzleiName, kanzleiAdresse);
    } catch (error) {
      alert(`Export-Fehler: ${error instanceof Error ? error.message : 'Unbekannter Fehler'}`);
    } finally {
      setExporting(false);
    }
  };

  const wordCount = editedContent.split(/\s+/).filter(w => w.length > 0).length;
  const charCount = editedContent.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={onBack}
            className="text-blue-600 hover:text-blue-700 text-sm mb-2 flex items-center gap-1"
          >
            ← Neue Generierung
          </button>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Dokument bearbeiten
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {wordCount} Wörter • {charCount} Zeichen
          </p>
        </div>
      </div>

      {/* Law Firm Info (Optional) */}
      <div className="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
          Kanzlei-Informationen (optional)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
              Kanzleiname
            </label>
            <input
              type="text"
              value={kanzleiName}
              onChange={(e) => setKanzleiName(e.target.value)}
              placeholder="z.B. Rechtsanwaltskanzlei Müller"
              className="w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
            />
          </div>
          <div>
            <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
              Adresse
            </label>
            <input
              type="text"
              value={kanzleiAdresse}
              onChange={(e) => setKanzleiAdresse(e.target.value)}
              placeholder="z.B. Musterstraße 123, 12345 Berlin"
              className="w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600"
            />
          </div>
        </div>
      </div>

      {/* Editor */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <div className="bg-gray-100 dark:bg-gray-700 px-4 py-2 border-b border-gray-200 dark:border-gray-600">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            💡 Tipp: Bearbeiten Sie den Text nach Bedarf. Formatierung bleibt beim Export erhalten.
          </p>
        </div>
        <textarea
          value={editedContent}
          onChange={(e) => setEditedContent(e.target.value)}
          className="w-full px-6 py-4 text-sm font-mono leading-relaxed focus:outline-none dark:bg-gray-800 dark:text-gray-100"
          rows={25}
          style={{ resize: 'vertical' }}
        />
      </div>

      {/* Action Buttons */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Verwerfen
        </button>

        <div className="flex gap-3">
          <button
            onClick={() => handleExport('docx')}
            disabled={exporting}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {exporting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Exportiere...
              </>
            ) : (
              <>
                📄 DOCX Download
              </>
            )}
          </button>

          <button
            onClick={() => handleExport('pdf')}
            disabled={exporting}
            className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {exporting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Exportiere...
              </>
            ) : (
              <>
                📕 PDF Download
              </>
            )}
          </button>
        </div>
      </div>

      {/* Preview Info */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          ℹ️ <strong>Export-Hinweis:</strong> Das Dokument wird mit professionellem Layout exportiert.
          DOCX-Dateien können in Word weiterbearbeitet werden. PDF-Dateien sind fertig zum Versenden.
        </p>
      </div>
    </div>
  );
}
