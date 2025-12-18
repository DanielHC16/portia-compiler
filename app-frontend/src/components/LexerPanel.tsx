// src/components/LexerPanel.tsx
import { useEffect, useRef, useState, useCallback } from "react";
import { lexCode, type Token, type LexError } from "../api";
import TokenList from "./TokenList";

const EXAMPLE = ``;

type SimpleToken = Token & { start?: number; end?: number };

export default function LexerPanel() {
  const [code, setCode] = useState<string>(EXAMPLE);
  const [lexedCode, setLexedCode] = useState<string>("");  // The code that was actually lexed
  const [tokens, setTokens] = useState<SimpleToken[]>([]);
  const [errors, setErrors] = useState<LexError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments, setHideComments] = useState(false);
  
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const preRef = useRef<HTMLPreElement | null>(null);
  const lineNumbersRef = useRef<HTMLDivElement | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Normalize smart/curly quotes to straight quotes for lexer compatibility
  const normalizeQuotes = (text: string): string => {
    return text
      .replace(/[\u201C\u201D\u201E\u201F\u2033\u2036]/g, '"')  // " " „ ‟ ″ ‶ → "
      .replace(/[\u2018\u2019\u201A\u201B\u2032\u2035]/g, "'"); // ' ' ‚ ‛ ′ ‵ → '
  };

  // Run lexer - only updates when manually triggered
  async function runLex() {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    
    setLoading(true);
    setErrors([]);
    
    try {
      // Normalize quotes before sending to lexer
      const normalizedCode = normalizeQuotes(code);
      const resp = await lexCode(normalizedCode, { signal: controller.signal });
      setTokens(resp.tokens as SimpleToken[]);
      setErrors(resp.errors);
      setLexedCode(normalizedCode);  // Store the normalized code that was lexed
    } catch (err: any) {
      if (err?.name !== 'AbortError') {
        setErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
        setTokens([]);
        setLexedCode("");
      }
    } finally {
      setLoading(false);
    }
  }

  // Handle code changes - just update the code, keep tokens/errors visible
  const handleCodeChange = useCallback((newCode: string) => {
    setCode(newCode);
    // Tokens and errors stay visible for reference until user runs lexer again or clicks reset
  }, []);

  // Handle paste - normalize quotes automatically
  const handlePaste = useCallback((e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    e.preventDefault();
    const pastedText = e.clipboardData.getData('text');
    const normalizedText = normalizeQuotes(pastedText);
    
    const textarea = textareaRef.current;
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const newCode = code.substring(0, start) + normalizedText + code.substring(end);
    
    setCode(newCode);
    
    // Set cursor position after paste
    setTimeout(() => {
      textarea.selectionStart = textarea.selectionEnd = start + normalizedText.length;
      textarea.focus();
    }, 0);
  }, [code, normalizeQuotes]);

  // Reset function - clears everything
  const handleReset = useCallback(() => {
    setCode(EXAMPLE);
    setTokens([]);
    setErrors([]);
    setLexedCode("");
  }, []);

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
    
    ta.addEventListener("scroll", onScroll, { passive: true });
    return () => ta.removeEventListener("scroll", onScroll);
  }, []);

  // Build highlight segments from tokens + errors (line/column -> char positions)
  // Only used when we have tokens (after running lexer) and only for the lexed code
  const buildHighlightsFromTokens = useCallback((src: string, toks: SimpleToken[], errs: LexError[]) => {
    if (!src) return [{ text: "", cls: undefined }];

    // Calculate line start positions
    const lineStarts: number[] = [0];
    for (let i = 0; i < src.length; i++) {
      if (src[i] === '\n') lineStarts.push(i + 1);
    }

    // Build error ranges
    const errorRanges: Array<{start: number, end: number}> = [];
    for (const err of errs) {
      if (err.start_index !== undefined && err.end_index !== undefined) {
        errorRanges.push({ start: err.start_index, end: err.end_index });
      } else if (err.line > 0 && err.line <= lineStarts.length) {
        const lineStart = lineStarts[err.line - 1];
        const start = lineStart + Math.max(0, err.column - 1);
        if (start < src.length) {
          let end = start + 1;
          while (end < src.length && /[a-zA-Z0-9_]/.test(src[end])) end++;
          errorRanges.push({ start, end });
        }
      }
    }

    type Match = { start: number; end: number; cls?: string; hasError?: boolean };
    const matches: Match[] = [];

    // Add tokens
    for (const tok of toks) {
      if (!tok.lexeme || tok.line === undefined || tok.column === undefined) continue;
      if (tok.line < 1 || tok.line > lineStarts.length) continue;
      
      const lineStart = lineStarts[tok.line - 1];
      let start = lineStart + tok.column - 1;
      let end = start + tok.lexeme.length;
      
      // Verify token position
      if (start < 0 || end > src.length || src.slice(start, end) !== tok.lexeme) {
        start = lineStart + tok.column;
        end = start + tok.lexeme.length;
      }
      
      // If still no match, try to find on line
      if (start < 0 || end > src.length || src.slice(start, end) !== tok.lexeme) {
        const lineEnd = lineStarts[tok.line] ?? src.length;
        const lineText = src.slice(lineStart, lineEnd);
        const tokenIndex = lineText.indexOf(tok.lexeme);
        
        if (tokenIndex !== -1) {
          start = lineStart + tokenIndex;
          end = start + tok.lexeme.length;
        } else {
          continue;
        }
      }
      
      const hasError = errorRanges.some(er => (start < er.end && end > er.start));
      matches.push({ start, end, cls: tokenClass(tok.type), hasError });
    }

    // Add standalone error ranges
    for (const er of errorRanges) {
      if (!matches.some(m => m.start < er.end && m.end > er.start)) {
        matches.push({ start: er.start, end: er.end, cls: undefined, hasError: true });
      }
    }

    if (matches.length === 0) return [{ text: src, cls: undefined }];

    // Sort and build segments
    matches.sort((a, b) => a.start - b.start);
    
    const segments: { text: string; cls?: string }[] = [];
    let pos = 0;
    
    for (const m of matches) {
      if (m.start > pos) segments.push({ text: src.slice(pos, m.start), cls: undefined });
      const classes = [m.cls, m.hasError ? 'hl-error' : ''].filter(Boolean).join(' ');
      segments.push({ text: src.slice(m.start, m.end), cls: classes || undefined });
      pos = m.end;
    }
    
    if (pos < src.length) segments.push({ text: src.slice(pos), cls: undefined });
    
    return segments;
  }, []);

  // Generate highlighted HTML - ONLY for the exact lexed code, nothing else
  const highlightedHTML = useCallback(() => {
    // STRICT: Only apply highlighting if code EXACTLY matches what was lexed
    if (lexedCode && code === lexedCode && tokens.length > 0) {
      const rawSegments = buildHighlightsFromTokens(code, tokens, errors);
      return rawSegments
        .map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text))
        .join("");
    }
    // Show plain text (no highlighting) - user can still see what they're typing
    return escapeHtml(code);
  }, [code, lexedCode, tokens, errors, buildHighlightsFromTokens]);
  
  // Calculate line numbers
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
          <button className="btn ghost" onClick={handleReset}>
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
                  fontFamily: "var(--mono)",
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
                    fontFamily: "var(--mono)",
                    fontSize: 14,
                    lineHeight: "1.5",
                    pointerEvents: "none",
                    overflow: "hidden",
                    borderTopLeftRadius: 0,
                    borderBottomLeftRadius: 0,
                  }}
                >
                  <span dangerouslySetInnerHTML={{ __html: highlightedHTML() }} />
                </pre>
                
                {/* Editable textarea */}
                <textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => handleCodeChange(e.target.value)}
                  onPaste={handlePaste}
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
                    fontFamily: "var(--mono)",
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
    "add", "subtract", "multiply", "divide", "modulo",
    "assign", "add_assign", "minus_assign", "mult_assign", "div_assign", "modulo_assign",
    "equal_equal", "not_equal", "less_than", "greater_than", "less_equal", "greater_equal",
    "logical_and", "logical_or", "logical_not",
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
