// src/components/LexerPanel.tsx
import { useEffect, useRef, useState } from "react";
import { lexCode, type Token, type LexError } from "../api";
import TokenList from "./TokenList";
import HighlightedSource from "./HighlightedSource";

const EXAMPLE = `// P0131 (2023-07-06)

int global = 1;

const float pi = 3.14;

int main() {
    // comment
    thread("Hello world");

    return 0;
}
`;

export default function LexerPanel() {
  const [code, setCode] = useState<string>(EXAMPLE);
  const [tokens, setTokens] = useState<Token[]>([]);
  const [errors, setErrors] = useState<LexError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments, setHideComments] = useState(false);

  const typingRef = useRef<number | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const displayRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    runLex();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function scheduleLex() {
    if (typingRef.current !== null) window.clearTimeout(typingRef.current);
    typingRef.current = window.setTimeout(() => {
      runLex();
      typingRef.current = null;
    }, 350);
  }

  async function runLex() {
    setLoading(true);
    setErrors([]);
    try {
      const resp = await lexCode(code);
      setTokens(resp.tokens);
      setErrors(resp.errors);
    } catch (err: any) {
      setErrors([{ message: err.message, line: 0, column: 0 }]);
      setTokens([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const ta = textareaRef.current;
    const disp = displayRef.current;
    if (!ta || !disp) return;
    const onScroll = () => {
      disp.scrollTop = ta.scrollTop;
      disp.scrollLeft = ta.scrollLeft;
    };
    ta.addEventListener("scroll", onScroll);
    return () => ta.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className="workspace" style={{ alignItems: "stretch" }}>
      <div className="panel" style={{ minHeight: 320 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <h2>Source</h2>
          <div style={{ marginLeft: "auto" }}>
            <button className="btn" onClick={runLex} disabled={loading}>{loading ? "Lexing..." : "Run Lexer"}</button>
            <button className="btn ghost" style={{ marginLeft: 8 }} onClick={() => { setCode(EXAMPLE); setTokens([]); setErrors([]); }}>Reset</button>
          </div>
        </div>

        <div className="source-wrap" style={{ marginTop: 6 }}>
          <div className="source-display" ref={displayRef}>
            <HighlightedSource source={code} tokens={tokens} className="hl-container" />
          </div>

          <div className="source-edit" style={{ marginTop: 8 }}>
            <textarea
              ref={textareaRef}
              value={code}
              onChange={(e) => { setCode(e.target.value); scheduleLex(); }}
              rows={10}
              aria-label="source-input"
            />
          </div>
        </div>
      </div>

      <div className="side">
        <div className="tokens panel">
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <h2 style={{ margin: 0 }}>Tokens</h2>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <input type="checkbox" checked={hideComments} onChange={e => setHideComments(e.target.checked)} />
                <span className="small">Hide comments</span>
              </label>
            </div>
          </div>

          <TokenList tokens={tokens} hideComments={hideComments} />
        </div>

        <div className="errors panel">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2 style={{ margin: 0 }}>Errors</h2>
            <div className="small">Problems: {errors.length}</div>
          </div>
          <div style={{ marginTop: 8 }}>
            {errors.length === 0 ? <div style={{ color: "#666" }}>No lexical errors</div> : (
              <ul style={{ margin: 0, paddingLeft: 16 }}>
                {errors.map((err, i) => <li key={i}><strong>{err.message}</strong> — line {err.line}, col {err.column}</li>)}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
