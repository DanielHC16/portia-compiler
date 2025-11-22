// src/components/LexerPanel.tsx
import { useEffect, useRef, useState, useLayoutEffect } from "react";
import { lexCode, type Token, type LexError } from "../api";
import TokenList from "./TokenList";

const EXAMPLE = `// PORTIA by LoomVI`;

type SimpleToken = Token & { start?: number; end?: number };

export default function LexerPanel() {
  const [code, setCode] = useState<string>(EXAMPLE);
  const [tokens, setTokens] = useState<SimpleToken[]>([]);
  const [errors, setErrors] = useState<LexError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments, setHideComments] = useState(false);
  const [autoLexDisabled, setAutoLexDisabled] = useState(false);
  const [lexTime, setLexTime] = useState<number | null>(null);
  const [highlightTime, setHighlightTime] = useState<number | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const preRef = useRef<HTMLPreElement | null>(null);
  const lineNumbersRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    runLex();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const abortRef = useRef<AbortController | null>(null);
  const debounceRef = useRef<number | null>(null);
  const pendingScrollRef = useRef<number | null>(null);
  const highlightStartRef = useRef<number | null>(null);

  async function runLex() {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    const start = performance.now();
    setLoading(true);
    setErrors([]);
    try {
      const resp = await lexCode(code, { signal: controller.signal });
      setTokens(resp.tokens as SimpleToken[]);
      setErrors(resp.errors);
      setLexTime(performance.now() - start);
    } catch (err: any) {
      if (err?.name === 'AbortError') return; 
      setErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
      setTokens([]);
      setLexTime(null);
    } finally {
      setLoading(false);
    }
  }

  async function runLexWithCode(sourceCode: string) {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    const start = performance.now();
    setLoading(true);
    setErrors([]);
    try {
      const resp = await lexCode(sourceCode, { signal: controller.signal });
      setTokens(resp.tokens as SimpleToken[]);
      setErrors(resp.errors);
      setLexTime(performance.now() - start);
    } catch (err: any) {
      if (err?.name === 'AbortError') return;
      setErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
      setTokens([]);
      setLexTime(null);
    } finally {
      setLoading(false);
    }
  }

  const LINE_DISABLE_THRESHOLD = 80; // disable auto lex at or above this line count

  function handleCodeChange(newCode: string) {
    const ta = textareaRef.current;
    const prevScroll = ta ? ta.scrollTop : 0;
    pendingScrollRef.current = prevScroll;
    setCode(newCode);
    // Disable auto lex for large line counts; manual run required
    const lineCount = newCode.split('\n').length;
    if (lineCount >= LINE_DISABLE_THRESHOLD) {
      setAutoLexDisabled(true);
      return;
    } else if (autoLexDisabled && lineCount < LINE_DISABLE_THRESHOLD) {
      // Re-enable if user shrinks code
      setAutoLexDisabled(false);
    }
    if (debounceRef.current) window.clearTimeout(debounceRef.current);
    debounceRef.current = window.setTimeout(() => {
      runLexWithCode(newCode);
    }, 350);
  }

  // Use layout effect to restore scroll before paint to prevent visible jump
  useLayoutEffect(() => {
    if (pendingScrollRef.current !== null) {
      const ta = textareaRef.current;
      const pre = preRef.current;
      const lines = lineNumbersRef.current;
      if (ta) ta.scrollTop = pendingScrollRef.current;
      if (pre) pre.scrollTop = pendingScrollRef.current;
      if (lines) lines.scrollTop = pendingScrollRef.current;
      pendingScrollRef.current = null;
    }
  }, [code]);
  

  // Removed auto-closing pairs feature per user request

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

  // Build highlight segments from tokens + errors (line/column -> char positions)
  function buildHighlightsFromTokens(src: string, toks: SimpleToken[], errs: LexError[]) {
    if (!src) return [{ text: "", cls: undefined }];

    // Calculate character positions from line/column for tokens
    const lineStarts: number[] = [0];
    for (let i = 0; i < src.length; i++) {
      if (src[i] === '\n') {
        lineStarts.push(i + 1);
      }
    }

    // Build error positions for highlighting - prioritize start_index/end_index if available
    const errorRanges: Array<{start: number, end: number}> = [];
    
    for (const err of errs) {
      // Use start_index and end_index if available (character position based)
      if (err.start_index !== undefined && err.end_index !== undefined) {
        errorRanges.push({ start: err.start_index, end: err.end_index });
      } else {
        // Fallback to line/column calculation
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
    }

    // Track used ranges
    const used: boolean[] = new Array(src.length).fill(false);

    type Match = { start: number; end: number; cls?: string; lexeme: string; hasError?: boolean };

    const matches: Match[] = [];

    // Add tokens using their line/column positions
    if (toks && toks.length > 0) {
      for (const tok of toks) {
        if (!tok.lexeme || tok.line === undefined || tok.column === undefined) continue;
        
        // Calculate character position from line/column
        if (tok.line > 0 && tok.line <= lineStarts.length) {
          const lineStart = lineStarts[tok.line - 1];
          const start = lineStart + Math.max(0, tok.column - 1);
          const end = start + tok.lexeme.length;
          
          // Bounds check
          if (start >= src.length || end > src.length) continue;
          
          // Verify the lexeme actually matches at this position
          if (src.slice(start, end) !== tok.lexeme) continue;
          
          // Check for overlap
          let overlap = false;
          for (let i = start; i < end; i++) {
            if (used[i]) {
              overlap = true;
              break;
            }
          }
          
          if (!overlap) {
            // Check if this token overlaps with any error range
            const hasError = errorRanges.some(errRange => 
              (start >= errRange.start && start < errRange.end) ||
              (end > errRange.start && end <= errRange.end) ||
              (start <= errRange.start && end >= errRange.end)
            );
            
            const cls = tokenClass(tok.type);
            matches.push({ start, end, cls, lexeme: tok.lexeme, hasError });
            for (let i = start; i < end; i++) used[i] = true;
          }
        }
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

  const [highlightedHTML, setHighlightedHTML] = useState<string>("");

  useEffect(() => {
    let active = true;
    highlightStartRef.current = performance.now();
    const rawSegments = buildHighlightsFromTokens(code, tokens, errors);
    const html = rawSegments.map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text)).join("");
    // Schedule highlight application on idle or next frame to reduce jank
    const apply = () => {
      if (!active) return;
      setHighlightedHTML(html);
      if (highlightStartRef.current !== null) {
        setHighlightTime(performance.now() - highlightStartRef.current);
      }
    };
    if ('requestIdleCallback' in window) {
      (window as any).requestIdleCallback(apply, { timeout: 100 });
    } else {
      requestAnimationFrame(apply);
    }
    return () => { active = false; };
  }, [code, tokens, errors]);
  
  // Calculate line numbers - ensure we count correctly even without trailing newline
  const lines = code.split('\n');
  const lineCount = lines.length;
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header with actions */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Lexical Analyzer</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: 'center' }}>
          <button className="btn" onClick={runLex} disabled={loading}>
            {loading ? "Lexing..." : "Run Lexer"}
          </button>
          {autoLexDisabled && (
            <button className="btn warning" onClick={() => { setAutoLexDisabled(false); runLex(); }} title="Re-enable auto lexing (currently disabled due to line count)">Enable Auto</button>
          )}
          <button
            className="btn ghost"
            onClick={async () => {
              setCode(EXAMPLE);
              setTokens([]);
              setErrors([]);
              // Run lexer with EXAMPLE code directly to avoid stale closure
              await runLexWithCode(EXAMPLE);
            }}
          >
            Reset
          </button>
          {/* Performance metrics hidden per request */}
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
              {autoLexDisabled && (
                <div style={{ position: 'absolute', top: 8, right: 8, left: 60, zIndex: 2, background: 'var(--warn-bg, #442)', color: 'var(--warn-text, #f7d774)', padding: '8px 12px', border: '1px solid var(--border)', borderRadius: 6, fontSize: 12 }}>
                  Auto lex disabled (≥ {LINE_DISABLE_THRESHOLD} lines). Use "Run Lexer" manually or reduce lines below {LINE_DISABLE_THRESHOLD}.
                </div>
              )}
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
                  onChange={(e) => handleCodeChange(e.target.value)}
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
            <h3 style={{ margin: 0 }}>Lexer Table</h3>
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
  
  // All PORTIA keywords (as defined in TOKEN_REFERENCE.md)
  const keywords = [
    // Scope
    "local", "global", "using",
    // Main
    "main",
    // Data types
    "int", "bool", "string", "float", "double", "long", "char", "void", "weave",
    // Declarations
    "const", "var",
    // I/O
    "trap", "thread", "threadln",
    // Functions
    "func", "return",
    // Conditionals
    "if", "else", "switch", "case", "default",
    // Loops
    "while", "do", "for",
    // Loop control
    "break",
    // Boolean literals
    "true", "false"
  ];
  
  // Check if it's a keyword (case-insensitive comparison)
  if (keywords.includes(type.toLowerCase())) return "hl-keyword";
  
  // Boolean literals (kept for backward compatibility if needed)
  if (type === "bool_lit") return "hl-keyword";
  
  // Numeric literals
  if (type === "int_lit" || type === "long_lit" || type === "float_lit" || type === "double_lit") return "hl-number";
  
  // String and char literals
  if (type === "string_lit") return "hl-string";
  if (type === "char_lit") return "hl-char";
  
  // Comments
  if (type === "single_comment" || type === "multi_comment") return "hl-comment";
  
  // Identifiers
  if (type === "identifier") return "hl-identifier";
  
  // Operators
  const operators = [
    "plus", "minus", "multiply", "divide", "modulo",
    "assign", "add_assign", "minus_assign", "mult_assign", "div_assign", "modulo_assign",
    "equal_equal", "not_equal", "less_than", "greater_than", "less_equal", "greater_equal",
    "logical_and", "logical_or", "not",
    "increment", "decrement",
    "concat"
  ];
  if (operators.includes(type)) return "hl-operator";
  
  // Delimiters
  const delimiters = [
    "open_paren", "close_paren",
    "open_bracket", "close_bracket",
    "open_curly", "close_curly",
    "semicolon", "comma", "colon", "dot"
  ];
  if (delimiters.includes(type)) return "hl-delim";
  
  return undefined;
}
