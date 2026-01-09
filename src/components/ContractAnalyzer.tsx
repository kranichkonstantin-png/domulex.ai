'use client';

import { useState } from 'react';
import { ContractAnalysis, apiClient, ClauseAnalysis } from '@/lib/api';

interface ContractAnalyzerProps {
  jurisdiction: 'DE' | 'ES' | 'US';
  role: 'INVESTOR' | 'LANDLORD' | 'TENANT' | 'OWNER' | 'MANAGER';
}

export default function ContractAnalyzer({ jurisdiction, role }: ContractAnalyzerProps) {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<ContractAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setAnalysis(null);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.analyzeContract(file, jurisdiction, role);
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analyse fehlgeschlagen');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: 'GREEN' | 'YELLOW' | 'RED') => {
    switch (risk) {
      case 'GREEN':
        return 'text-green-600 bg-green-100 dark:bg-green-900';
      case 'YELLOW':
        return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900';
      case 'RED':
        return 'text-red-600 bg-red-100 dark:bg-red-900';
    }
  };

  const getRiskIcon = (risk: 'GREEN' | 'YELLOW' | 'RED') => {
    switch (risk) {
      case 'GREEN':
        return '🟢';
      case 'YELLOW':
        return '🟡';
      case 'RED':
        return '🔴';
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <div className="border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg p-8 text-center">
        <input
          type="file"
          accept=".pdf,.doc,.docx,.txt,.rtf,.xls,.xlsx,.csv,.jpg,.jpeg,.png,.webp,.tiff,.tif,.eml,.xml,.html,.htm"
          onChange={handleFileChange}
          className="hidden"
          id="contract-upload"
        />
        <label
          htmlFor="contract-upload"
          className="cursor-pointer flex flex-col items-center space-y-2"
        >
          <svg
            className="w-12 h-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <p className="text-lg font-medium">
            {file ? file.name : 'Vertrag hochladen'}
          </p>
          <p className="text-sm text-gray-500">PDF, Word, Excel, Bilder & mehr</p>
        </label>
      </div>

      {file && (
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {loading ? '🔍 Analysiere Vertrag...' : '🔍 Vertrag analysieren'}
        </button>
      )}

      {error && (
        <div className="p-4 bg-red-100 dark:bg-red-900 rounded-lg text-red-800 dark:text-red-200">
          ❌ {error}
        </div>
      )}

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6">
          {/* Header */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
            <h2 className="text-2xl font-bold mb-4">📋 Vertragsanalyse</h2>
            <div
              className={`inline-flex items-center px-4 py-2 rounded-lg font-semibold ${getRiskColor(
                analysis.overall_risk
              )}`}
            >
              {getRiskIcon(analysis.overall_risk)} Gesamtrisiko: {analysis.overall_risk}
            </div>
            <p className="mt-4 text-gray-700 dark:text-gray-300">{analysis.summary}</p>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold">{analysis.total_clauses_analyzed}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Klauseln</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-red-600">{analysis.red_flags}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">🔴 Kritisch</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-yellow-600">{analysis.yellow_flags}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">🟡 Warnung</p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 text-center">
              <p className="text-2xl font-bold text-green-600">{analysis.green_flags}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">🟢 OK</p>
            </div>
          </div>

          {/* Clause Analysis */}
          <div className="space-y-4">
            <h3 className="text-xl font-bold">📝 Klausel-Analyse</h3>
            {analysis.clauses.map((clause, index) => (
              <details
                key={index}
                className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow"
              >
                <summary className="cursor-pointer font-semibold flex items-center space-x-2">
                  <span>{getRiskIcon(clause.risk_level)}</span>
                  <span>
                    {index + 1}. {clause.clause_type}
                  </span>
                  <span
                    className={`ml-auto px-2 py-1 rounded text-sm ${getRiskColor(
                      clause.risk_level
                    )}`}
                  >
                    {clause.risk_level}
                  </span>
                </summary>
                <div className="mt-4 space-y-3">
                  <div>
                    <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                      📄 Vertragstext:
                    </p>
                    <p className="text-sm bg-gray-50 dark:bg-gray-900 p-2 rounded mt-1">
                      {clause.clause_text}
                    </p>
                  </div>
                  <div>
                    <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                      ⚖️ Rechtslage:
                    </p>
                    <p className="text-sm mt-1">{clause.legal_standard}</p>
                    {clause.source_title && (
                      <a
                        href={clause.source_url || '#'}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs text-blue-600 hover:underline"
                      >
                        Quelle: {clause.source_title}
                      </a>
                    )}
                  </div>
                  <div>
                    <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                      🔍 Analyse:
                    </p>
                    <p className="text-sm mt-1">{clause.comparison}</p>
                  </div>
                  {clause.recommendation && (
                    <div
                      className={`p-3 rounded ${
                        clause.risk_level === 'RED'
                          ? 'bg-red-50 dark:bg-red-900'
                          : clause.risk_level === 'YELLOW'
                          ? 'bg-yellow-50 dark:bg-yellow-900'
                          : 'bg-green-50 dark:bg-green-900'
                      }`}
                    >
                      <p className="font-semibold text-sm">💡 Empfehlung:</p>
                      <p className="text-sm mt-1">{clause.recommendation}</p>
                    </div>
                  )}
                </div>
              </details>
            ))}
          </div>

          <button
            onClick={() => {
              setAnalysis(null);
              setFile(null);
            }}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            🗑️ Analyse löschen
          </button>
        </div>
      )}
    </div>
  );
}
