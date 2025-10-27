// src/components/SemanticTBA.tsx
import { useState } from "react";
import { lexCode, analyzeTokens } from "../api";

export default function SemanticTBA() {
  const [source, setSource] = useState<string>("int main() { return 0; }\n");
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
    <div className="panel" style={{ gridColumn: "1 / -1" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2>Semantics</h2>
        <div style={{ marginLeft: "auto" }}>
          <button className="btn" onClick={runAnalyze} disabled={loading}>{loading ? "Analyzing..." : "Run Semantic"}</button>
        </div>
      </div>

      <textarea value={source} onChange={e => setSource(e.target.value)} rows={6} style={{ width: "100%", fontFamily: "var(--mono)" }} />
      <div style={{ marginTop: 12 }}>
        <h3>Result</h3>
        <pre style={{ background: "#fff", padding: 12, border: "1px solid var(--border)" }}>
          {result ? JSON.stringify(result, null, 2) : "No result yet"}
        </pre>
      </div>
    </div>
  );
}
