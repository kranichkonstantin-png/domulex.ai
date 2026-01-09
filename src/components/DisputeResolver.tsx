'use client';

import { useState } from 'react';
import { ConflictRequest, ConflictResponse, apiClient } from '@/lib/api';

interface DisputeResolverProps {
  jurisdiction: 'DE' | 'ES' | 'US';
  language: 'de' | 'es' | 'en';
}

export default function DisputeResolver({ jurisdiction, language }: DisputeResolverProps) {
  const [partyALabel, setPartyALabel] = useState('Vermieter');
  const [partyBLabel, setPartyBLabel] = useState('Mieter');
  const [partyAStatement, setPartyAStatement] = useState('');
  const [partyBStatement, setPartyBStatement] = useState('');
  const [analysis, setAnalysis] = useState<ConflictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!partyAStatement.trim() || !partyBStatement.trim()) {
      setError('Bitte beide Perspektiven eingeben');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const request: ConflictRequest = {
        party_a_statement: partyAStatement,
        party_b_statement: partyBStatement,
        jurisdiction,
        party_a_label: partyALabel,
        party_b_label: partyBLabel,
        user_language: language,
      };

      const result = await apiClient.resolveConflict(request);
      setAnalysis(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analyse fehlgeschlagen');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold">⚖️ Konfliktlösung</h2>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Neutrale Mediation für Immobilienstreitigkeiten
        </p>
      </div>

      {/* Party Labels */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">Partei A Bezeichnung</label>
          <input
            type="text"
            value={partyALabel}
            onChange={(e) => setPartyALabel(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            placeholder="z.B. Vermieter"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Partei B Bezeichnung</label>
          <input
            type="text"
            value={partyBLabel}
            onChange={(e) => setPartyBLabel(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            placeholder="z.B. Mieter"
          />
        </div>
      </div>

      {/* Statements */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            🔵 {partyALabel} Perspektive
          </label>
          <textarea
            value={partyAStatement}
            onChange={(e) => setPartyAStatement(e.target.value)}
            className="w-full h-40 px-4 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 resize-none"
            placeholder={`Beschreibe die Sicht von ${partyALabel}...`}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">
            🟠 {partyBLabel} Perspektive
          </label>
          <textarea
            value={partyBStatement}
            onChange={(e) => setPartyBStatement(e.target.value)}
            className="w-full h-40 px-4 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 resize-none"
            placeholder={`Beschreibe die Sicht von ${partyBLabel}...`}
          />
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-100 dark:bg-red-900 rounded-lg text-red-800 dark:text-red-200">
          ❌ {error}
        </div>
      )}

      <button
        onClick={handleAnalyze}
        disabled={loading || !partyAStatement.trim() || !partyBStatement.trim()}
        className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
      >
        {loading ? '⚖️ Analysiere Konflikt...' : '🔍 Rechtslage analysieren'}
      </button>

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6 mt-8">
          {/* Summary */}
          <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-6">
            <h3 className="text-lg font-bold mb-2">📋 Zusammenfassung</h3>
            <p>{analysis.dispute_summary}</p>
          </div>

          {/* Success Probabilities */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-lg font-bold mb-4">📊 Erfolgswahrscheinlichkeiten</h3>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  🔵 {partyALabel}
                </p>
                <div className="text-2xl font-bold text-blue-600">
                  {analysis.success_probability_a.toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${analysis.success_probability_a}%` }}
                  />
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  🟠 {partyBLabel}
                </p>
                <div className="text-2xl font-bold text-orange-600">
                  {analysis.success_probability_b.toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div
                    className="bg-orange-600 h-2 rounded-full"
                    style={{ width: `${analysis.success_probability_b}%` }}
                  />
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  🤝 Vergleich
                </p>
                <div className="text-2xl font-bold text-green-600">
                  {analysis.settlement_likelihood.toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: `${analysis.settlement_likelihood}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Party Analyses */}
          <div className="grid grid-cols-2 gap-4">
            {/* Party A */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
              <h3 className="text-lg font-bold mb-4">🔵 Argumente für {partyALabel}</h3>
              <div className="space-y-3">
                <div>
                  <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                    Rechtliche Grundlage:
                  </p>
                  <p className="text-sm mt-1">{analysis.party_a_analysis.legal_arguments}</p>
                </div>
                <div>
                  <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                    Bewertung:
                  </p>
                  <p className="text-sm mt-1">
                    {analysis.party_a_analysis.strength_assessment}
                  </p>
                </div>
                {analysis.party_a_analysis.supporting_sources.length > 0 && (
                  <details className="text-sm">
                    <summary className="cursor-pointer font-semibold">
                      📚 Quellen ({analysis.party_a_analysis.supporting_sources.length})
                    </summary>
                    <div className="mt-2 space-y-1">
                      {analysis.party_a_analysis.supporting_sources.map((source, idx) => (
                        <a
                          key={idx}
                          href={source.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-blue-600 hover:underline"
                        >
                          {source.title}
                        </a>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            </div>

            {/* Party B */}
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
              <h3 className="text-lg font-bold mb-4">🟠 Argumente für {partyBLabel}</h3>
              <div className="space-y-3">
                <div>
                  <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                    Rechtliche Grundlage:
                  </p>
                  <p className="text-sm mt-1">{analysis.party_b_analysis.legal_arguments}</p>
                </div>
                <div>
                  <p className="font-semibold text-sm text-gray-600 dark:text-gray-400">
                    Bewertung:
                  </p>
                  <p className="text-sm mt-1">
                    {analysis.party_b_analysis.strength_assessment}
                  </p>
                </div>
                {analysis.party_b_analysis.supporting_sources.length > 0 && (
                  <details className="text-sm">
                    <summary className="cursor-pointer font-semibold">
                      📚 Quellen ({analysis.party_b_analysis.supporting_sources.length})
                    </summary>
                    <div className="mt-2 space-y-1">
                      {analysis.party_b_analysis.supporting_sources.map((source, idx) => (
                        <a
                          key={idx}
                          href={source.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-blue-600 hover:underline"
                        >
                          {source.title}
                        </a>
                      ))}
                    </div>
                  </details>
                )}
              </div>
            </div>
          </div>

          {/* Neutral Assessment */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
            <h3 className="text-lg font-bold mb-4">⚖️ Neutrale Bewertung</h3>
            <p className="text-gray-700 dark:text-gray-300">
              {analysis.neutral_assessment}
            </p>
          </div>

          {/* Recommendation */}
          <div
            className={`rounded-lg p-6 ${
              analysis.settlement_likelihood > 60
                ? 'bg-green-50 dark:bg-green-900'
                : 'bg-yellow-50 dark:bg-yellow-900'
            }`}
          >
            <h3 className="text-lg font-bold mb-4">💡 Empfehlung des Mediators</h3>
            <p className="text-gray-800 dark:text-gray-200">{analysis.recommendation}</p>
          </div>

          <button
            onClick={() => setAnalysis(null)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            🗑️ Analyse löschen
          </button>
        </div>
      )}
    </div>
  );
}
