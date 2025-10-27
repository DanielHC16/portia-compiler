// src/components/LexerPanel.tsx
import { useEffect, useRef, useState } from "react";
import { lexCode, type Token, type LexError } from "../api";
import TokenList from "./TokenList";

const EXAMPLE = `// PORTIA by LoomVI
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
  const lineNumbersRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    runLex();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function scheduleLex() {
    if (typingRef.current !== null) window.clearTimeout(typingRef.current);
    typingRef.current = window.setTimeout(() => {
      runLex();
      typingRef.current = null;
    }, 20);
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

  // Sync scroll between textarea, highlighting overlay, and line numbers
  useEffect(() => {
    const ta = textareaRef.current;
    const pre = preRef.current;
    const lineNums = lineNumbersRef.current;
    if (!ta || !pre || !lineNums) return;
    
    const onScroll = () => {
      const scrollTop = ta.scrollTop;
      const scrollLeft = ta.scrollLeft;
      pre.scrollTop = scrollTop;
      pre.scrollLeft = scrollLeft;
      lineNums.scrollTop = scrollTop;
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
  function buildHighlightsFromTokens(src: string, toks: SimpleToken[], errs: LexError[]) {
    if (!src) return [{ text: "", cls: undefined }];
    if (!toks || toks.length === 0) return [{ text: src, cls: undefined }];

    // Build error positions for highlighting
    const errorRanges: Array<{start: number, end: number}> = [];
    
    // Calculate line start positions (line numbers are 1-indexed from backend)
    const lineStarts: number[] = [0];
    for (let i = 0; i < src.length; i++) {
      if (src[i] === '\n') {
        lineStarts.push(i + 1);
      }
    }
    
    for (const err of errs) {
      // Error line and column are 1-indexed
      if (err.line > 0 && err.line <= lineStarts.length) {
        const lineStart = lineStarts[err.line - 1];
        const colPos = lineStart + Math.max(0, err.column - 1);
        
        // Bounds check
        if (colPos >= src.length) continue;
        
        // Find the end of the error token - look for the next whitespace or special char
        let endPos = colPos + 1;
        while (endPos < src.length && 
               src[endPos] !== ' ' && 
               src[endPos] !== '\t' && 
               src[endPos] !== '\n' &&
               src[endPos] !== '\r' &&
               /[a-zA-Z0-9_]/.test(src[endPos])) {
          endPos++;
        }
        
        errorRanges.push({ start: colPos, end: endPos });
      }
    }

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

    type Match = { start: number; end: number; cls?: string; lexeme: string; hasError?: boolean };

    const matches: Match[] = [];

    for (const info of lexList) {
      const lex = info.lexeme;
      const typ = info.type;
      const maxCount = info.count;
      if (!lex) continue;
      
      // Use literal string search for better performance and accuracy
      let searchPos = 0;
      let found = 0;
      
      while (searchPos < src.length && found < maxCount) {
        const s = src.indexOf(lex, searchPos);
        if (s === -1) break;
        
        const e = s + lex.length;
        
        // check overlap with existing used ranges
        let overlap = false;
        for (let i = s; i < e; i++) {
          if (used[i]) {
            overlap = true;
            break;
          }
        }
        
        if (!overlap) {
          // Check if this token overlaps with any error range
          const hasError = errorRanges.some(errRange => 
            (s >= errRange.start && s < errRange.end) ||
            (e > errRange.start && e <= errRange.end) ||
            (s <= errRange.start && e >= errRange.end)
          );
          
          // accept match
          const cls = tokenClass(typ);
          matches.push({ start: s, end: e, cls, lexeme: lex, hasError });
          for (let i = s; i < e; i++) used[i] = true;
          found += 1;
        }
        
        searchPos = s + 1;
      }
    }

    // Add error ranges that weren't covered by tokens
    for (const errRange of errorRanges) {
      let overlap = false;
      for (let i = errRange.start; i < errRange.end; i++) {
        if (used[i]) {
          overlap = true;
          break;
        }
      }
      
      if (!overlap) {
        matches.push({ 
          start: errRange.start, 
          end: errRange.end, 
          cls: undefined, 
          lexeme: src.slice(errRange.start, errRange.end),
          hasError: true 
        });
        for (let i = errRange.start; i < errRange.end; i++) used[i] = true;
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
      const classNames = [m.cls, m.hasError ? 'hl-error' : ''].filter(Boolean).join(' ');
      segments.push({ text: src.slice(m.start, m.end), cls: classNames || undefined });
      pos = m.end;
    }
    if (pos < src.length) segments.push({ text: src.slice(pos) });
    return segments;
  }

  const rawSegments = buildHighlightsFromTokens(code, tokens, errors);
  const highlightedHTML = rawSegments.map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text)).join("");
  
  // Calculate line numbers - ensure we count correctly even without trailing newline
  const lines = code.split('\n');
  const lineCount = lines.length;
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header with actions */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Lexical Analyzer</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          <button className="btn" onClick={runLex} disabled={loading}>
            {loading ? "Lexing..." : "Run Lexer"}
          </button>
          <button
            className="btn ghost"
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

      {/* Two-column layout: Left (Source + Errors) | Right (Tokens) */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, flex: "1 1 auto", minHeight: 0 }}>
        {/* Left Column: Source Code and Errors */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16, minHeight: 0 }}>
          {/* Code Editor with Syntax Highlighting */}
          <div className="panel" style={{ flex: "1 1 auto", display: "flex", flexDirection: "column", minHeight: 0 }}>
            <h3 style={{ marginTop: 0, marginBottom: 8 }}>Source Code</h3>
            <div style={{ position: "relative", flex: "1 1 auto", minHeight: 300, display: "flex" }}>
              {/* Line Numbers */}
              <div
                ref={lineNumbersRef}
                style={{
                  position: "relative",
                  width: 40,
                  padding: "12px 8px",
                  background: "var(--bg-secondary)",
                  borderLeft: "1px solid var(--border)",
                  borderTop: "1px solid var(--border)",
                  borderBottom: "1px solid var(--border)",
                  borderTopLeftRadius: 6,
                  borderBottomLeftRadius: 6,
                  overflow: "hidden",
                  userSelect: "none",
                  textAlign: "right",
                  fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace",
                  fontSize: 14,
                  lineHeight: "1.5",
                  color: "var(--text-muted)",
                  opacity: 0.6,
                }}
              >
                {lineNumbers.map((num) => (
                  <div key={num} style={{ minHeight: "21px" }}>{num}</div>
                ))}
              </div>

              {/* Code container */}
              <div style={{ position: "relative", flex: 1, minWidth: 0 }}>
                {/* Highlighted overlay */}
                <pre
                  ref={preRef}
                  className="source-display"
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    margin: 0,
                    padding: "12px",
                    whiteSpace: "pre-wrap",
                    wordWrap: "break-word",
                    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace",
                    fontSize: 14,
                    lineHeight: "1.5",
                    pointerEvents: "none",
                    overflow: "hidden",
                    borderTopLeftRadius: 0,
                    borderBottomLeftRadius: 0,
                  }}
                >
                  <span dangerouslySetInnerHTML={{ __html: highlightedHTML }} />
                </pre>
                
                {/* Editable textarea */}
                <textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => {
                    setCode(e.target.value);
                    scheduleLex();
                  }}
                  aria-label="source-input"
                  spellCheck={false}
                  className="source-edit"
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    width: "100%",
                    height: "100%",
                    margin: 0,
                    padding: "12px",
                    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', 'Courier New', monospace",
                    fontSize: 14,
                    lineHeight: "1.5",
                    backgroundColor: "transparent",
                    color: "transparent",
                    resize: "none",
                    outline: "none",
                    caretColor: "var(--text)",
                    whiteSpace: "pre-wrap",
                    wordWrap: "break-word",
                    borderTopLeftRadius: 0,
                    borderBottomLeftRadius: 0,
                  }}
                />
              </div>
            </div>
          </div>

          {/* Errors Panel */}
          <div className="panel" style={{ flex: "0 0 auto" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
              <h3 style={{ margin: 0 }}>Errors</h3>
              <div className="small">Problems: {errors.length}</div>
            </div>
            <div style={{ maxHeight: 200, overflow: "auto" }}>
              {errors.length === 0 ? (
                <div style={{ color: "var(--success)", fontStyle: "italic", fontSize: "13px" }}>No lexical errors</div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {errors.map((err, i) => (
                    <div key={i} style={{
                      padding: "8px 12px",
                      background: "var(--bg-secondary)",
                      border: "1px solid var(--border)",
                      borderLeft: "3px solid var(--error)",
                      borderRadius: 4,
                      fontSize: 13,
                    }}>
                      <div style={{ fontWeight: 600, color: "var(--error)", marginBottom: 4 }}>
                        {err.message}
                      </div>
                      <div style={{ fontSize: 12, color: "var(--text-muted)" }}>
                        Line {err.line}, Column {err.column}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Tokens Panel */}
        <div className="panel" style={{ display: "flex", flexDirection: "column", minHeight: 0 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
            <h3 style={{ margin: 0 }}>Tokens</h3>
            <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <input
                type="checkbox"
                checked={hideComments}
                onChange={(e) => setHideComments(e.target.checked)}
              />
              <span className="small">Hide comments</span>
            </label>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            <TokenList tokens={tokens} hideComments={hideComments} />
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
  if (type === "COMMENT" || type === "ML_COMMENT" || /COMMENT$/.test(type)) return "hl-comment";
  if (type === "IDENTIFIER") return "hl-identifier";
  if (type === "DELIMITER") return "hl-delim";
  if (type === "OPERATOR") return "hl-operator";
  if (/^KW_(INT|LONG|FLOAT|DOUBLE|CHAR|BOOL|STRING|VOID|THREAD|FUNC|CONST|VAR|GLOBAL|RETURN)$/.test(type)) return "hl-type";
  return undefined;
}
