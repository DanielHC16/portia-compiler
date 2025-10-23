// src/components/ParserTBA.tsx
import { useState } from "react";
import { parseSource } from "../api";

export default function ParserTBA() {
  const [source, setSource] = useState<string>("int main() { return 0; }\n");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function runParse() {
    setLoading(true);
    try {
      const resp = await parseSource(source);
      setResult(resp);
    } catch (err: any) {
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel" style={{ gridColumn: "1 / -1" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2>Syntax / Parser</h2>
        <div style={{ marginLeft: "auto" }}>
          <button className="btn" onClick={runParse} disabled={loading}>{loading ? "Running..." : "Run Parser"}</button>
        </div>
      </div>

      <textarea value={source} onChange={e => setSource(e.target.value)} rows={6} style={{ width: "100%", fontFamily: "var(--mono)" }} />
      <div style={{ marginTop: 12 }}>
        <h3>Parser Response</h3>
        <pre style={{ background: "#fff", padding: 12, border: "1px solid var(--border)" }}>
          {result ? JSON.stringify(result, null, 2) : "No response yet"}
        </pre>
      </div>
    </div>
  );
}
