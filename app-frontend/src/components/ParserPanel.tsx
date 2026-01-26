// src/components/ParserPanel.tsx
import { useEffect, useRef, useState, useCallback } from "react";
import { lexCode, parseTokens, type Token, type LexError } from "../api";
import TokenList from "./TokenList";
import ASTTreeView from "./ASTTreeView";

const EXAMPLE = `int main() {
    return 0;
}`;

type SimpleToken = Token & { start?: number; end?: number };

type ParserPanelProps = {
  sharedCode: string;
  sharedTokens: Token[];
  sharedLexErrors: LexError[];
};

export default function ParserPanel({ sharedCode, sharedTokens, sharedLexErrors }: ParserPanelProps) {
  const [code, setCode] = useState<string>(sharedCode || EXAMPLE);
  const [lexedCode, setLexedCode] = useState<string>(sharedCode || "");
  const [tokens, setTokens] = useState<SimpleToken[]>(sharedTokens as SimpleToken[] || []);
  const [lexErrors, setLexErrors] = useState<LexError[]>(sharedLexErrors || []);
  const [parseErrors, setParseErrors] = useState<string[]>([]);
  const [parseErrorObjects, setParseErrorObjects] = useState<LexError[]>([]);
  const [ast, setAst] = useState<any>(null);
  const [viewMode, setViewMode] = useState<'tokens' | 'tree' | 'json'>('tokens');
  const [loading, setLoading] = useState(false);
  const [hideComments, setHideComments] = useState(false);
  
  // Sync with shared state when it changes
  useEffect(() => {
    setCode(sharedCode || EXAMPLE);
    setLexedCode(sharedCode || "");
    setTokens(sharedTokens as SimpleToken[] || []);
    setLexErrors(sharedLexErrors || []);
  }, [sharedCode, sharedTokens, sharedLexErrors]);
  
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const preRef = useRef<HTMLPreElement | null>(null);
  const lineNumbersRef = useRef<HTMLDivElement | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Normalize smart/curly quotes to straight quotes
  const normalizeQuotes = (text: string): string => {
    return text
      .replace(/[\u201C\u201D\u201E\u201F\u2033\u2036]/g, '"')
      .replace(/[\u2018\u2019\u201A\u201B\u2032\u2035]/g, "'");
  };

  // Run lexer and parser
  async function runParser() {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    
    setLoading(true);
    setLexErrors([]);
    setParseErrors([]);
    
    try {
      // First run lexer
      const normalizedCode = normalizeQuotes(code).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const lexResp = await lexCode(normalizedCode, { signal: controller.signal });
      setTokens(lexResp.tokens as SimpleToken[]);
      setLexErrors(lexResp.errors);
      setLexedCode(normalizedCode);
      
      // If no lexical errors, run parser
      if (lexResp.errors.length === 0) {
        try {
          // Filter out comment tokens before parsing
          const tokensWithoutComments = lexResp.tokens.filter((token: Token) => 
            token.type !== 'single_comment' && token.type !== 'multi_comment'
          );
          const parseResp = await parseTokens(tokensWithoutComments, normalizedCode, { signal: controller.signal });
          
          // Debug: log the parse response
          console.log('[Parser Response]', parseResp);
          console.log('[Errors]', parseResp.errors);
          
          // Check if parser succeeded
          if (parseResp.success && parseResp.ast) {
            setAst(parseResp.ast);
            setParseErrors([]);
            setParseErrorObjects([]);
          } else if (parseResp.errors && parseResp.errors.length > 0) {
            // Store both error objects (for highlighting) and error strings (for display)
            const errorObjects = parseResp.errors.map((e: any) => {
              if (typeof e === 'object' && e.message) {
                return { message: e.message, line: e.line || 0, column: e.column || 0 };
              }
              return { message: String(e), line: 0, column: 0 };
            });
            const errorMessages = errorObjects.map((e: any) => e.message);
            setParseErrors(errorMessages);
            setParseErrorObjects(errorObjects);
            setAst(null);
          } else if (parseResp.status === "tba") {
            setParseErrors([`Parser logic in progress: ${parseResp.message}`]);
            setParseErrorObjects([]);
            setAst(null);
          } else {
            setParseErrors([]);
            setParseErrorObjects([]);
            setAst(parseResp.ast || null);
          }
        } catch (err: any) {
          if (err?.name !== 'AbortError') {
            setParseErrors([err?.message ?? String(err)]);
            setAst(null);
          }
        }
      } else {
        setParseErrors(["Cannot parse: lexical errors present"]);
        setAst(null);
      }
    } catch (err: any) {
      if (err?.name !== 'AbortError') {
        setLexErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
        setTokens([]);
        setLexedCode("");
      }
    } finally {
      setLoading(false);
    }
  }

  // Code is read-only in Parser Panel - all changes come from Lexer Panel

  // Reset function
  const handleReset = useCallback(() => {
    setCode(EXAMPLE);
    setTokens([]);
    setLexErrors([]);
    setParseErrors([]);
    setParseErrorObjects([]);
    setAst(null);
    setViewMode('tokens');
    setLexedCode("");
  }, []);

  // Handle code changes
  const handleCodeChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCode(e.target.value);
  }, []);

  // Handle special key combinations
  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target as HTMLTextAreaElement;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const newCode = code.substring(0, start) + '    ' + code.substring(end);
      setCode(newCode);
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 4;
      }, 0);
    }
  }, [code]);

  // Sync scroll
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

  // Build highlights
  const buildHighlightsFromTokens = useCallback((src: string, toks: SimpleToken[], errs: LexError[]) => {
    if (!src) return [{ text: "", cls: undefined }];

    try {
      const lineStarts: number[] = [0];
      for (let i = 0; i < src.length; i++) {
        if (src[i] === '\n') lineStarts.push(i + 1);
      }

    const errorRanges: Array<{start: number, end: number}> = [];
    for (const err of errs) {
      if (err.start_index !== undefined && err.end_index !== undefined) {
        errorRanges.push({ start: err.start_index, end: err.end_index });
      } else if (err.line > 0 && err.line <= lineStarts.length) {
        const lineStart = lineStarts[err.line - 1];
        const start = lineStart + (err.column - 1);
        if (start >= 0 && start < src.length) {
          let end = start + 1;
          while (end < src.length && /[a-zA-Z0-9_]/.test(src[end])) end++;
          errorRanges.push({ start, end });
        }
      }
    }

    type Match = { start: number; end: number; cls?: string; isError?: boolean };
    const matches: Match[] = [];

    for (const tok of toks) {
      if (!tok.lexeme || tok.line === undefined || tok.column === undefined) continue;
      if (tok.line < 1 || tok.line > lineStarts.length) continue;
      
      const lineStart = lineStarts[tok.line - 1];
      let start = lineStart + tok.column - 1;
      let end = start + tok.lexeme.length;
      
      if (start < 0 || end > src.length || src.slice(start, end) !== tok.lexeme) {
        start = lineStart + tok.column;
        end = start + tok.lexeme.length;
      }
      
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
      
      matches.push({ start, end, cls: tokenClass(tok.type), isError: false });
    }

    for (const er of errorRanges) {
      let foundOverlap = false;
      
      for (const m of matches) {
        if (m.start < er.end && m.end > er.start) {
          m.isError = true;
          foundOverlap = true;
        }
      }
      
      if (!foundOverlap) {
        matches.push({ start: er.start, end: er.end, cls: undefined, isError: true });
      }
    }

    if (matches.length === 0) return [{ text: src, cls: undefined }];

    matches.sort((a, b) => a.start - b.start);
    
    const segments: { text: string; cls?: string }[] = [];
    let pos = 0;
    
    for (const m of matches) {
      if (m.start > pos) segments.push({ text: src.slice(pos, m.start), cls: undefined });
      
      const classes = [m.cls, m.isError ? 'hl-error' : ''].filter(Boolean).join(' ');
      segments.push({ text: src.slice(m.start, m.end), cls: classes || undefined });
      pos = m.end;
    }
    
    if (pos < src.length) segments.push({ text: src.slice(pos), cls: undefined });
    
    return segments.length > 0 ? segments : [{ text: src, cls: undefined }];
    } catch (e) {
      // On any error, return plain text
      return [{ text: src, cls: undefined }];
    }
  }, []);

  const highlightedHTML = useCallback(() => {
    try {
      if (lexedCode && code === lexedCode && (tokens.length > 0 || lexErrors.length > 0 || parseErrorObjects.length > 0)) {
        // Combine lexical and parser errors for highlighting
        const allErrors = [...lexErrors, ...parseErrorObjects];
        const rawSegments = buildHighlightsFromTokens(code, tokens, allErrors);
        const html = rawSegments
          .map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text))
          .join("");
        return html || escapeHtml(code);
      }
      return escapeHtml(code);
    } catch (e) {
      // Fallback on any error
      return escapeHtml(code);
    }
  }, [code, lexedCode, tokens, lexErrors, parseErrorObjects, buildHighlightsFromTokens]);
  
  const lines = code.split('\n');
  const lineCount = lines.length;
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Syntax Analyzer</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: 'center' }}>
          <button 
            className="btn" 
            onClick={runParser} 
            disabled={loading || lexErrors.length > 0}
            title={lexErrors.length > 0 ? "Fix lexical errors before parsing" : ""}
          >
            {loading ? "Analyzing..." : "Run Parser"}
          </button>
          <button className="btn ghost" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>

      {/* Two-column layout */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, flex: "1 1 auto", minHeight: 0 }}>
        {/* Left Column: Source Code and Terminal */}
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
                  ref={textareaRef as any}
                  value={code}
                  onChange={handleCodeChange}
                  onKeyDown={handleKeyDown}
                  aria-label="source-code-editor"
                  className="source-display"
                  spellCheck={false}
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
                    resize: "none",
                    border: "none",
                    outline: "none",
                    background: "transparent",
                    color: "transparent",
                    caretColor: "var(--text)",
                    overflow: "auto",
                    whiteSpace: "pre-wrap",
                    wordWrap: "break-word",
                    borderTopLeftRadius: 0,
                    borderBottomLeftRadius: 0,
                  }}
                />
              </div>
            </div>
          </div>

          {/* Terminal / Errors Panel */}
          <div className="panel" style={{ flex: "0 0 auto" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
              <h3 style={{ margin: 0 }}>Terminal</h3>
              <div className="small" style={{
                color: (lexErrors.length > 0 || parseErrors.length > 0) ? "var(--text-muted)" : tokens.length > 0 ? "var(--success)" : "var(--text-muted)",
                fontWeight: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? 600 : 400,
                padding: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "4px 12px" : "0",
                borderRadius: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "12px" : "0",
                backgroundColor: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "rgba(34, 197, 94, 0.1)" : "transparent",
                border: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "1px solid rgba(34, 197, 94, 0.3)" : "none"
              }}>
                {lexErrors.length > 0 ? `Lexical Errors: ${lexErrors.length}` : 
                 parseErrors.length > 0 ? `Syntax Errors: ${parseErrors.length}` : 
                 tokens.length > 0 ? '✓ Parsing success' : 'No errors'}
              </div>
            </div>
            <div style={{ maxHeight: 200, overflow: "auto" }}>
              {lexErrors.length === 0 && parseErrors.length === 0 ? (
                <div style={{ color: "var(--success)", fontStyle: "italic", fontSize: "13px" }}>
                  {tokens.length > 0 ? "No syntax errors" : "Run parser to analyze code"}
                </div>
              ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {/* Show lexical errors first */}
                  {lexErrors.map((err, i) => (
                    <div key={`lex-${i}`} style={{
                      padding: "8px 12px",
                      background: "var(--bg-secondary)",
                      border: "1px solid var(--border)",
                      borderLeft: "3px solid var(--error)",
                      borderRadius: 4,
                      fontSize: 13,
                    }}>
                      <div style={{ fontWeight: 600, color: "var(--error)", marginBottom: 4 }}>
                        [Lexical] {err.message}
                      </div>
                      <div style={{ fontSize: 12, color: "var(--text-muted)" }}>
                        Line {err.line}, Column {err.column}
                      </div>
                    </div>
                  ))}
                  
                  {/* Show parse errors */}
                  {parseErrorObjects.map((err, i) => (
                    <div key={`parse-${i}`} style={{
                      padding: "8px 12px",
                      background: "var(--bg-secondary)",
                      border: "1px solid var(--border)",
                      borderLeft: "3px solid var(--warning)",
                      borderRadius: 4,
                      fontSize: 13,
                    }}>
                      <div style={{ fontWeight: 600, color: "var(--warning)", marginBottom: 4 }}>
                        [Syntax] {err.message}
                      </div>
                      {(err.line > 0 || err.column > 0) && (
                        <div style={{ fontSize: 12, color: "var(--text-muted)" }}>
                          Line {err.line}, Column {err.column}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Tokens or AST Panel */}
        <div className="panel" style={{ display: "flex", flexDirection: "column", minHeight: 0 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
            <h3 style={{ margin: 0 }}>
              {viewMode === 'tokens' ? 'Tokens' : viewMode === 'tree' ? 'AST Tree' : 'AST JSON'}
            </h3>
            <div style={{ display: "flex", gap: 8 }}>
              <button 
                className={`btn ${viewMode === 'tokens' ? '' : 'ghost'}`}
                onClick={() => setViewMode('tokens')}
                style={{ padding: "6px 12px", fontSize: 12 }}
              >
                Show Tokens
              </button>
              <button 
                className={`btn ${viewMode === 'tree' ? '' : 'ghost'}`}
                onClick={() => setViewMode('tree')}
                style={{ padding: "6px 12px", fontSize: 12 }}
                disabled={!ast}
              >
                Show Tree
              </button>
              <button 
                className={`btn ${viewMode === 'json' ? '' : 'ghost'}`}
                onClick={() => setViewMode('json')}
                style={{ padding: "6px 12px", fontSize: 12 }}
                disabled={!ast}
              >
                Show Raw
              </button>
            </div>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {viewMode === 'tree' && ast ? (
              <ASTTreeView ast={ast} />
            ) : viewMode === 'json' && ast ? (
              <div style={{ fontFamily: "var(--mono)", fontSize: 13, height: "100%" }}>
                <pre style={{ 
                  margin: 0, 
                  padding: 12, 
                  background: "var(--bg-secondary)", 
                  borderRadius: 6,
                  whiteSpace: "pre-wrap",
                  wordBreak: "break-word"
                }}>
                  {JSON.stringify(ast, null, 2)}
                </pre>
              </div>
            ) : (
              <TokenList tokens={tokens} hideComments={hideComments} />
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
  
  const keywords = [
    "local", "global", "using", "main",
    "int", "bool", "string", "float", "double", "long", "char", "void", "weave",
    "const", "var",
    "trap", "thread", "threadln",
    "func", "return",
    "if", "else", "switch", "case", "default",
    "while", "do", "for",
    "break",
    "true", "false"
  ];
  
  if (keywords.includes(type.toLowerCase())) return "hl-keyword";
  if (type === "bool_lit") return "hl-keyword";
  if (type === "int_lit" || type === "long_lit" || type === "float_lit" || type === "double_lit") return "hl-number";
  if (type === "string_lit") return "hl-string";
  if (type === "char_lit") return "hl-char";
  if (type === "single_comment" || type === "multi_comment") return "hl-comment";
  if (type === "id") return "hl-identifier";
  
  const operators = [
    "add", "subtract", "multiply", "divide", "modulo",
    "assign", "add_assign", "minus_assign", "mult_assign", "div_assign", "modulo_assign",
    "equal_equal", "not_equal", "less_than", "greater_than", "less_equal", "greater_equal",
    "logical_and", "logical_or", "logical_not",
    "increment", "decrement",
    "concat"
  ];
  if (operators.includes(type)) return "hl-operator";
  
  const delimiters = [
    "open_paren", "close_paren",
    "open_bracket", "close_bracket",
    "open_curly", "close_curly",
    "semicolon", "comma", "colon", "dot"
  ];
  if (delimiters.includes(type)) return "hl-delim";
  
  return undefined;
}
