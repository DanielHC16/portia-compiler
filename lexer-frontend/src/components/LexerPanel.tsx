// src/components/LexerPanel.tsx
import { useEffect, useRef, useState } from "react";
import { lexCode, type Token, type LexError } from "../api";
import TokenList from "./TokenList";

const EXAMPLE = `
thread("Hello World");
`;

type SimpleToken = Token & { start?: number; end?: number };

export default function LexerPanel() {
  const [code, setCode] = useState<string>(EXAMPLE);
  const [tokens, setTokens] = useState<SimpleToken[]>([]);
  const [errors, setErrors] = useState<LexError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments, setHideComments] = useState(false);

  const typingRef = useRef<number | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const preRef = useRef<HTMLPreElement | null>(null);

  useEffect(() => {
    runLex();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function scheduleLex() {
    if (typingRef.current !== null) window.clearTimeout(typingRef.current);
    typingRef.current = window.setTimeout(() => {
      runLex();
      typingRef.current = null;
    }, 320);
  }

  async function runLex() {
    setLoading(true);
    setErrors([]);
    try {
      const resp = await lexCode(code);
      setTokens(resp.tokens as SimpleToken[]);
      setErrors(resp.errors);
    } catch (err: any) {
      setErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
      setTokens([]);
    } finally {
      setLoading(false);
    }
  }

  // Sync scroll: when textarea scrolls, mirror pre scroll
  useEffect(() => {
    const ta = textareaRef.current;
    const pre = preRef.current;
    if (!ta || !pre) return;
    const onScroll = () => {
      pre.scrollTop = ta.scrollTop;
      pre.scrollLeft = ta.scrollLeft;
    };
    ta.addEventListener("scroll", onScroll);
    return () => ta.removeEventListener("scroll", onScroll);
  }, []);

  // Build deterministic non-overlapping matches using only lexeme and type.
  // Strategy:
  //  - Collect token lexemes and types.
  //  - Deduplicate identical lexeme/type by counting occurrences (we allow multiple matches up to occurrence count).
  //  - Sort lexemes by length desc to prefer longest matches first.
  //  - Search source for each lexeme, record matches that don't overlap previous matches, stop when occurrence count reached.
  //  - After collecting matches, sort them by start and render segments.
  function buildHighlightsFromTokens(src: string, toks: SimpleToken[]) {
    if (!src) return [{ text: "", cls: undefined }];
    if (!toks || toks.length === 0) return [{ text: src, cls: undefined }];

    // Prepare token lexeme -> { type, count }
    type LexInfo = { lexeme: string; type: string; count: number };
    const map = new Map<string, LexInfo>();

    for (const t of toks) {
      const lex = t.lexeme ?? "";
      if (!lex) continue;
      const key = `${lex}\u0000${t.type ?? "UNKNOWN"}`;
      const existing = map.get(key);
      if (existing) existing.count += 1;
      else map.set(key, { lexeme: lex, type: t.type ?? "UNKNOWN", count: 1 });
    }

    // Convert map to array and sort by lexeme length desc (longer first)
    const lexList = Array.from(map.values()).sort((a, b) => b.lexeme.length - a.lexeme.length);

    // Track used ranges
    const used: boolean[] = new Array(src.length).fill(false);

    type Match = { start: number; end: number; cls?: string; lexeme: string };

    const matches: Match[] = [];

    // Helper: safely create regex for literal lexeme (escape and use global)
    function escapeForRegex(s: string) {
      return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }

    for (const info of lexList) {
      const lex = info.lexeme;
      const typ = info.type;
      const maxCount = info.count;
      if (!lex) continue;
      const re = new RegExp(escapeForRegex(lex), "g");
      let found = 0;
      let m: RegExpExecArray | null;
      while ((m = re.exec(src)) !== null) {
        const s = m.index;
        const e = s + (m[0]?.length ?? 0);
        // check overlap with existing used ranges
        let overlap = false;
        for (let i = s; i < e; i++) {
          if (used[i]) {
            overlap = true;
            break;
          }
        }
        if (overlap) continue;
        // accept match
        const cls = tokenClass(typ);
        matches.push({ start: s, end: e, cls, lexeme: lex });
        for (let i = s; i < e; i++) used[i] = true;
        found += 1;
        if (found >= maxCount) break; // don't find more than token count
      }
    }

    if (matches.length === 0) return [{ text: src, cls: undefined }];

    // Sort matches by start
    matches.sort((a, b) => a.start - b.start || b.end - a.end);

    // Build segments: non-matching gaps + matched spans
    const segments: { text: string; cls?: string }[] = [];
    let pos = 0;
    for (const m of matches) {
      if (m.start > pos) segments.push({ text: src.slice(pos, m.start) });
      segments.push({ text: src.slice(m.start, m.end), cls: m.cls });
      pos = m.end;
    }
    if (pos < src.length) segments.push({ text: src.slice(pos) });
    return segments;
  }

  const rawSegments = buildHighlightsFromTokens(code, tokens);
  const highlightedHTML = rawSegments.map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text)).join("");

  return (
    <div className="workspace" style={{ alignItems: "stretch" }}>
      <div className="panel" style={{ minHeight: 320 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <h2>Source</h2>
          <div style={{ marginLeft: "auto" }}>
            <button className="btn" onClick={runLex} disabled={loading}>
              {loading ? "Lexing..." : "Run Lexer"}
            </button>
            <button
              className="btn ghost"
              style={{ marginLeft: 8 }}
              onClick={() => {
                setCode(EXAMPLE);
                setTokens([]);
                setErrors([]);
                setTimeout(() => runLex(), 50);
              }}
            >
              Reset
            </button>
          </div>
        </div>

        <div style={{ marginTop: 6 }}>
          <div style={{ display: "flex", gap: 12, alignItems: "flex-start", flexDirection: "column" }}>
            <div style={{ width: "100%" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                <div style={{ fontSize: 13, color: "#6b7280" }}>Source (read-only)</div>
              </div>
              <div className="source-display" style={{ minHeight: 200 }}>
                <pre
                  ref={preRef}
                  style={{
                    margin: 0,
                    whiteSpace: "pre-wrap",
                    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace",
                    fontSize: 13,
                  }}
                >
                  <span dangerouslySetInnerHTML={{ __html: highlightedHTML }} />
                </pre>
              </div>
            </div>

            <div style={{ width: "100%" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                <div style={{ fontSize: 13, color: "#6b7280" }}>Edit</div>
              </div>
              <div className="source-edit">
                <textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => {
                    setCode(e.target.value);
                    scheduleLex();
                  }}
                  rows={12}
                  aria-label="source-input"
                  style={{
                    width: "100%",
                    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace",
                    fontSize: 13,
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="side">
        <div className="tokens panel">
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <h2 style={{ margin: 0 }}>Tokens</h2>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <input
                  type="checkbox"
                  checked={hideComments}
                  onChange={(e) => setHideComments(e.target.checked)}
                />
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
            {errors.length === 0 ? (
              <div style={{ color: "#666" }}>No lexical errors</div>
            ) : (
              <ul style={{ margin: 0, paddingLeft: 16 }}>
                {errors.map((err, i) => (
                  <li key={i}>
                    <strong>{err.message}</strong> — line {err.line}, col {err.column}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/* helpers */

function escapeHtml(s: string) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function tokenClass(type?: string) {
  if (!type) return undefined;
  if (/^KW_/.test(type)) return "hl-keyword";
  if (type === "INT_LIT" || type === "FLOAT_LIT") return "hl-number";
  if (type === "STRING_LIT") return "hl-string";
  if (type === "CHAR_LIT") return "hl-char";
  if (type === "COMMENT" || type === "ML_COMMENT") return "hl-comment";
  if (type === "IDENTIFIER") return "hl-identifier";
  if (type === "DELIMITER") return "hl-delim";
  if (type === "OPERATOR") return "hl-operator";
  if (/^KW_(INT|LONG|FLOAT|DOUBLE|CHAR|BOOL|STRING|VOID|THREAD|FUNC|CONST|VAR|GLOBAL|RETURN)$/.test(type)) return "hl-type";
  return undefined;
}
