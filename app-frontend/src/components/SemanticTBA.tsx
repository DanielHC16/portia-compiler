// src/components/SemanticTBA.tsx
import { useState } from "react";
import { lexCode, analyzeTokens } from "../api";

const EXAMPLE = `int main() {
  return 0;
}
`;

export default function SemanticTBA() {
  const [source, setSource] = useState(EXAMPLE);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function runAnalyze() {
    setLoading(true);
    setResult(null);
    try {
      const lexResp = await lexCode(source);
      const tokens = lexResp.tokens;
      const analysis = await analyzeTokens(tokens);
      setResult({ lex: lexResp, analysis });
    } catch (err: any) {
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 16, height: "100%", display: "flex", flexDirection: "column", gap: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Semantic Analyzer</h2>
        <span style={{ fontSize: 12, color: "var(--text-muted)", fontStyle: "italic" }}>Preview</span>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          <button className="btn" onClick={runAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Run Analyzer"}
          </button>
          <button className="btn ghost" onClick={() => { setSource(EXAMPLE); setResult(null); }}>
            Reset
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="panel" style={{ flex: "1 1 auto", display: "flex", flexDirection: "column", gap: 16, minHeight: 0 }}>
        {/* Source Input */}
        <div>
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Source Code</h3>
          <div className="source-edit">
            <textarea
              value={source}
              onChange={(e) => setSource(e.target.value)}
              spellCheck={false}
              rows={12}
              style={{
                width: "100%",
                fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace",
                fontSize: 14,
              }}
            />
          </div>
        </div>

        {/* Analysis Results */}
        <div style={{ flex: "1 1 auto", display: "flex", flexDirection: "column", minHeight: 0 }}>
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Semantic Analysis Results</h3>
          <div style={{ 
            flex: "1 1 auto", 
            overflow: "auto",
            background: "var(--bg-secondary)",
            border: "1px solid var(--border)",
            borderRadius: 6,
            padding: 12,
          }}>
            <pre style={{
              margin: 0,
              fontSize: 13,
              lineHeight: 1.6,
              fontFamily: "var(--mono)",
              color: "var(--text)",
              whiteSpace: "pre-wrap",
              wordWrap: "break-word",
            }}>
              {result ? JSON.stringify(result, null, 2) : ""}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
