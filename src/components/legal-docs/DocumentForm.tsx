'use client';

import { useState } from 'react';
import { FileUpload } from '../FileUpload';

interface UploadedDocument {
  id: string;
  filename: string;
  doc_type: string;
  char_count: number;
  word_count: number;
  ocr_applied: boolean;
  extracted_text_preview?: string;
}

interface TemplateField {
  name: string;
  label: string;
  type: 'text' | 'textarea' | 'date' | 'select';
  required: boolean;
  hilfe?: string;
  optionen?: string[];
}

interface Template {
  id: string;
  name: string;
  beschreibung: string;
  kategorie: string;
  felder: TemplateField[];
}

interface DocumentFormProps {
  template: Template;
  onGenerate: (fieldValues: Record<string, string>, contextDocs: UploadedDocument[]) => void;
  onBack: () => void;
}

export function DocumentForm({ template, onGenerate, onBack }: DocumentFormProps) {
  const [fieldValues, setFieldValues] = useState<Record<string, string>>({});
  const [contextDocuments, setContextDocuments] = useState<UploadedDocument[]>([]);
  const [generatingField, setGeneratingField] = useState<string | null>(null);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleFieldChange = (fieldName: string, value: string) => {
    setFieldValues(prev => ({ ...prev, [fieldName]: value }));
    // Clear error when user types
    if (errors[fieldName]) {
      setErrors(prev => {
        const next = { ...prev };
        delete next[fieldName];
        return next;
      });
    }
  };

  const handleAIGenerate = async (field: TemplateField) => {
    if (contextDocuments.length === 0) {
      alert('Bitte laden Sie mindestens ein Dokument hoch, um KI-Unterstützung zu nutzen.');
      return;
    }

    setGeneratingField(field.name);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/documents/generate-field`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            template_id: template.id,
            field_name: field.name,
            context_documents: contextDocuments.map(doc => ({
              document_id: doc.id,
              text: doc.extracted_text_preview || '',
            })),
            user_input: fieldValues[field.name] || '',
          }),
        }
      );

      if (!response.ok) {
        throw new Error('KI-Generierung fehlgeschlagen');
      }

      const data = await response.json();
      handleFieldChange(field.name, data.generated_content);
    } catch (error) {
      alert(`Fehler: ${error instanceof Error ? error.message : 'Unbekannter Fehler'}`);
    } finally {
      setGeneratingField(null);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    
    template.felder.forEach(field => {
      if (field.required && !fieldValues[field.name]?.trim()) {
        newErrors[field.name] = 'Dieses Feld ist erforderlich';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      alert('Bitte füllen Sie alle erforderlichen Felder aus.');
      return;
    }

    onGenerate(fieldValues, contextDocuments);
  };

  const renderField = (field: TemplateField) => {
    const commonClasses = "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700";
    const isGenerating = generatingField === field.name;

    return (
      <div key={field.name} className="space-y-2">
        {/* Label */}
        <div className="flex items-center justify-between">
          <label className="block text-sm font-semibold text-gray-900 dark:text-white">
            {field.label}
            {field.required && <span className="text-red-500 ml-1">*</span>}
          </label>

          {/* AI Generate Button */}
          {(field.type === 'textarea' || field.type === 'text') && contextDocuments.length > 0 && (
            <button
              type="button"
              onClick={() => handleAIGenerate(field)}
              disabled={isGenerating}
              className="text-xs bg-purple-600 hover:bg-purple-700 text-white px-3 py-1 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-1"
            >
              {isGenerating ? (
                <>
                  <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  KI generiert...
                </>
              ) : (
                <>
                  ✨ KI-Assistent
                </>
              )}
            </button>
          )}
        </div>

        {/* Help Text */}
        {field.hilfe && (
          <p className="text-xs text-gray-500 dark:text-gray-400">{field.hilfe}</p>
        )}

        {/* Input Field */}
        {field.type === 'text' && (
          <input
            type="text"
            value={fieldValues[field.name] || ''}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className={commonClasses}
            placeholder={`${field.label} eingeben...`}
          />
        )}

        {field.type === 'textarea' && (
          <textarea
            value={fieldValues[field.name] || ''}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            rows={6}
            className={commonClasses}
            placeholder={`${field.label} eingeben...`}
          />
        )}

        {field.type === 'date' && (
          <input
            type="date"
            value={fieldValues[field.name] || ''}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className={commonClasses}
          />
        )}

        {field.type === 'select' && field.optionen && (
          <select
            value={fieldValues[field.name] || ''}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className={commonClasses}
          >
            <option value="">Bitte wählen...</option>
            {field.optionen.map(option => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        )}

        {/* Error Message */}
        {errors[field.name] && (
          <p className="text-sm text-red-600 dark:text-red-400">{errors[field.name]}</p>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={onBack}
            className="text-blue-600 hover:text-blue-700 text-sm mb-2 flex items-center gap-1"
          >
            ← Zurück zur Vorlagenauswahl
          </button>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            {template.name}
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {template.beschreibung}
          </p>
        </div>
      </div>

      {/* Context Documents Upload */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 dark:text-blue-100 mb-2">
          📎 Kontextdokumente hochladen (optional)
        </h3>
        <p className="text-xs text-blue-800 dark:text-blue-200 mb-3">
          Laden Sie relevante Dokumente hoch (z.B. Mietvertrag, Korrespondenz), um die KI-basierte Feldgenerierung zu nutzen.
        </p>
        <FileUpload
          onUpload={(doc) => setContextDocuments(prev => [...prev, doc])}
          maxSize={10}
          maxFiles={5}
        />
        
        {contextDocuments.length > 0 && (
          <div className="mt-3 space-y-1">
            {contextDocuments.map((doc, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs bg-white dark:bg-gray-800 p-2 rounded">
                <span className="truncate flex-1">{doc.filename}</span>
                <button
                  type="button"
                  onClick={() => setContextDocuments(prev => prev.filter((_, i) => i !== idx))}
                  className="ml-2 text-red-600 hover:text-red-800"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* All Fields */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 space-y-6">
          {template.felder.map(field => renderField(field))}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={onBack}
            className="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Abbrechen
          </button>
          
          <button
            type="submit"
            className="px-8 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            Dokument generieren →
          </button>
        </div>
      </form>
    </div>
  );
}
