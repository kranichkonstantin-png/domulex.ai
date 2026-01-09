'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface UploadedDocument {
  id: string;
  filename: string;
  doc_type: string;
  char_count: number;
  word_count: number;
  ocr_applied: boolean;
  extracted_text_preview?: string;
  extracted_text_full?: string;  // Full text for analysis
}

interface FileUploadProps {
  onUpload: (document: UploadedDocument) => void;
  maxSize?: number; // MB
  allowedTypes?: string[];
  maxFiles?: number;
  className?: string;
  disabled?: boolean; // Sperrt Upload wenn keine Anfragen mehr verfügbar
}

export function FileUpload({
  onUpload,
  maxSize = 10,
  allowedTypes = ['pdf', 'docx', 'doc', 'txt', 'rtf', 'jpg', 'jpeg', 'png', 'webp', 'tiff', 'tif', 'xlsx', 'xls', 'csv', 'eml', 'xml', 'html', 'htm'],
  maxFiles = 5,
  className = '',
  disabled = false
}: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedDocument[]>([]);

  const handleDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    setError(null);
    setUploading(true);
    setProgress(0);

    try {
      for (let i = 0; i < acceptedFiles.length; i++) {
        const file = acceptedFiles[i];
        
        // Check file size
        if (file.size > maxSize * 1024 * 1024) {
          setError(`Datei ${file.name} ist zu groß (max ${maxSize}MB)`);
          continue;
        }

        // Check file type
        const ext = file.name.split('.').pop()?.toLowerCase() || '';
        if (!allowedTypes.includes(ext)) {
          setError(`Dateityp .${ext} nicht unterstützt`);
          continue;
        }

        // Upload to backend
        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', 'demo_user'); // TODO: Get from Firebase Auth
        formData.append('session_id', 'demo_session'); // TODO: Get from chat context

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://domulex-backend-841507936108.europe-west3.run.app';
        const response = await fetch(`${apiUrl}/upload/document`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Upload fehlgeschlagen');
        }

        const result = await response.json();
        
        if (result.success && result.document) {
          const doc = {
            ...result.document,
            extracted_text_preview: result.extracted_text_preview,
            extracted_text_full: result.extracted_text_full,  // 📎 Full text for analysis
          };
          setUploadedFiles(prev => [...prev, doc]);
          onUpload(doc);
        } else {
          throw new Error(result.error || 'Upload fehlgeschlagen');
        }

        setProgress(((i + 1) / acceptedFiles.length) * 100);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload fehlgeschlagen');
    } finally {
      setUploading(false);
      setProgress(0);
    }
  }, [maxSize, allowedTypes, onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleDrop,
    maxFiles,
    accept: {
      // Dokumente
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
      'text/rtf': ['.rtf'],
      'application/rtf': ['.rtf'],
      // Excel & Tabellen
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'text/csv': ['.csv'],
      // Bilder (für OCR/Scans)
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/webp': ['.webp'],
      'image/tiff': ['.tiff', '.tif'],
      // E-Mail & Weitere
      'message/rfc822': ['.eml'],
      'application/xml': ['.xml'],
      'text/html': ['.html', '.htm']
    },
    disabled: uploading || disabled,
  });

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id));
  };

  return (
    <div className={`file-upload-container ${className}`}>
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-gray-50 hover:border-gray-400'}
          ${uploading || disabled ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center gap-3">
          <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          
          {uploading ? (
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Uploading...</p>
              <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-blue-500 transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          ) : (
            <>
              <p className="text-base font-medium text-gray-700">
                {isDragActive ? 'Dateien hier ablegen...' : 'Dateien hier ablegen oder klicken'}
              </p>
              <p className="text-sm text-gray-500">
                PDF, DOC, DOCX, TXT, RTF, XLS, XLSX, CSV, JPG, PNG, TIFF, EML
              </p>
            </>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700">❌ {error}</p>
        </div>
      )}

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="mt-6 space-y-3">
          <h4 className="text-sm font-semibold text-gray-700">Hochgeladene Dokumente:</h4>
          
          {uploadedFiles.map((doc) => (
            <div 
              key={doc.id}
              className="flex items-start gap-3 p-4 bg-white border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
            >
              {/* File Icon */}
              <div className="flex-shrink-0">
                {doc.doc_type === 'pdf' && (
                  <svg className="w-10 h-10 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                  </svg>
                )}
                {doc.doc_type === 'docx' && (
                  <svg className="w-10 h-10 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                  </svg>
                )}
                {doc.doc_type === 'image' && (
                  <svg className="w-10 h-10 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                  </svg>
                )}
                {doc.doc_type === 'txt' && (
                  <svg className="w-10 h-10 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                  </svg>
                )}
              </div>

              {/* File Info */}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {doc.filename}
                </p>
                <div className="mt-1 flex items-center gap-3 text-xs text-gray-500">
                  <span>{doc.word_count} Wörter</span>
                  <span>•</span>
                  <span>{doc.char_count} Zeichen</span>
                  {doc.ocr_applied && (
                    <>
                      <span>•</span>
                      <span className="text-blue-600">📷 OCR</span>
                    </>
                  )}
                </div>
                {doc.extracted_text_preview && (
                  <p className="mt-2 text-xs text-gray-600 line-clamp-2">
                    {doc.extracted_text_preview}
                  </p>
                )}
              </div>

              {/* Remove Button */}
              <button
                onClick={() => removeFile(doc.id)}
                className="flex-shrink-0 p-1 text-gray-400 hover:text-red-500 transition-colors"
                title="Entfernen"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
