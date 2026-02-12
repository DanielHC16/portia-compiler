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
  setSharedCode: (code: string) => void;
  sharedTokens: Token[];
  sharedLexErrors: LexError[];
};

export default function ParserPanel({ sharedCode, setSharedCode, sharedTokens, sharedLexErrors }: ParserPanelProps) {
  const [lexedCode, setLexedCode] = useState<string>(sharedCode || "");
  const [tokens, setTokens] = useState<SimpleToken[]>(sharedTokens as SimpleToken[] || []);
  const [lexErrors, setLexErrors] = useState<LexError[]>(sharedLexErrors || []);
  const [parseErrors, setParseErrors] = useState<string[]>([]);
  const [parseErrorObjects, setParseErrorObjects] = useState<LexError[]>([]);
  const [ast, setAst] = useState<any>(null);
  const [viewMode, setViewMode] = useState<'tokens' | 'tree' | 'json'>('tokens');
  const [loading, setLoading] = useState(false);
  const [hideComments, _setHideComments] = useState(false);
  
  // Sync tokens/errors with shared state when it changes (but not code - that's shared)
  useEffect(() => {
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
      const normalizedCode = normalizeQuotes(sharedCode).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
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
          const parseResp = await parseTokens(tokensWithoutComments, normalizedCode, lexResp.errors, { signal: controller.signal });
          
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
                return { 
                  message: e.message, 
                  line: e.line || 0, 
                  column: e.column || 0,
                  token_length: e.token_length || 0  // Include token length for exact highlighting
                };
              }
              return { message: String(e), line: 0, column: 0, token_length: 0 };
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
    setSharedCode(EXAMPLE);
    setTokens([]);
    setLexErrors([]);
    setParseErrors([]);
    setParseErrorObjects([]);
    setAst(null);
    setViewMode('tokens');
    setLexedCode("");
  }, [setSharedCode]);

  // Handle code changes
  const handleCodeChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setSharedCode(e.target.value);
  }, [setSharedCode]);

  // Handle special key combinations
  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.target as HTMLTextAreaElement;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const newCode = sharedCode.substring(0, start) + '    ' + sharedCode.substring(end);
      setSharedCode(newCode);
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 4;
      }, 0);
    }
  }, [sharedCode, setSharedCode]);

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
      // Calculate line start positions (0-indexed character positions)
      const lineStarts: number[] = [0];
      for (let i = 0; i < src.length; i++) {
        if (src[i] === '\n') lineStarts.push(i + 1);
      }

      // Collect all ranges: syntax tokens + error underlines
      // Error ranges take priority and will be rendered separately
      type Range = { start: number; end: number; cls?: string; isError: boolean };
      const tokenRanges: Range[] = [];
      const errorRanges: Range[] = [];

      // 1. Build syntax token ranges
      for (const tok of toks) {
        if (!tok.lexeme || tok.line === undefined || tok.column === undefined) continue;
        if (tok.line < 1 || tok.line > lineStarts.length) continue;
        
        const lineStart = lineStarts[tok.line - 1];
        let start = lineStart + tok.column - 1;
        let end = start + tok.lexeme.length;
        
        // Verify position matches
        if (start >= 0 && end <= src.length && src.slice(start, end) === tok.lexeme) {
          tokenRanges.push({ start, end, cls: tokenClass(tok.type), isError: false });
        }
      }

      // 2. Build error ranges from parser-provided data ONLY
      // NO merging, NO text search, NO token inference
      for (const err of errs) {
        if (err.line === undefined || err.line < 1 || err.column === undefined || err.column < 1) {
          continue;
        }
        if (err.line > lineStarts.length) {
          continue;
        }

        const lineStart = lineStarts[err.line - 1];
        const errorStart = lineStart + err.column - 1; // 1-based column → 0-based index
        const errorLength = err.token_length || 1;
        const errorEnd = errorStart + errorLength;

        if (errorStart < 0 || errorEnd > src.length) {
          continue;
        }

        console.log('[Error Underline] Range:', err.line, err.column, '→ chars', errorStart, '-', errorEnd, '=', JSON.stringify(src.slice(errorStart, errorEnd)));
        
        // Always add standalone error range - never merge into tokens
        errorRanges.push({ start: errorStart, end: errorEnd, cls: 'hl-error', isError: true });
      }

      // 3. Build final segments by merging token and error ranges
      // Errors take visual priority (rendered on top via CSS)
      const allRanges = [...tokenRanges, ...errorRanges];
      if (allRanges.length === 0) return [{ text: src, cls: undefined }];

      // Sort by start position, errors first at same position
      allRanges.sort((a, b) => a.start - b.start || (a.isError ? -1 : 1));

      // Build non-overlapping segments using sweep line algorithm
      const segments: { text: string; cls?: string }[] = [];

      // Create a simple segment list from all ranges
      // Handle overlaps by letting error class override
      const points = new Set<number>();
      for (const r of allRanges) {
        points.add(r.start);
        points.add(r.end);
      }
      points.add(0);
      points.add(src.length);
      const sortedPoints = Array.from(points).sort((a, b) => a - b);

      for (let i = 0; i < sortedPoints.length - 1; i++) {
        const segStart = sortedPoints[i];
        const segEnd = sortedPoints[i + 1];
        if (segStart >= segEnd) continue;

        // Find all ranges covering this segment
        const coveringRanges = allRanges.filter(r => r.start <= segStart && r.end >= segEnd);
        
        // Determine class: error takes priority, then token class
        let cls: string | undefined;
        const hasError = coveringRanges.some(r => r.isError);
        const tokenRange = coveringRanges.find(r => !r.isError && r.cls);
        
        if (hasError && tokenRange) {
          cls = `${tokenRange.cls} hl-error`;
        } else if (hasError) {
          cls = 'hl-error';
        } else if (tokenRange) {
          cls = tokenRange.cls;
        }

        segments.push({ text: src.slice(segStart, segEnd), cls });
      }

      return segments.length > 0 ? segments : [{ text: src, cls: undefined }];
    } catch (e) {
      console.error('[Highlight] Exception:', e);
      return [{ text: src, cls: undefined }];
    }
  }, []);

  const highlightedHTML = useCallback(() => {
    try {
      if (lexedCode && sharedCode === lexedCode && (tokens.length > 0 || lexErrors.length > 0 || parseErrorObjects.length > 0)) {
        // Combine lexical and parser errors for highlighting
        const allErrors = [...lexErrors, ...parseErrorObjects];
        const rawSegments = buildHighlightsFromTokens(sharedCode, tokens, allErrors);
        const html = rawSegments
          .map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text))
          .join("");
        return html || escapeHtml(sharedCode);
      }
      return escapeHtml(sharedCode);
    } catch (e) {
      // Fallback on any error
      return escapeHtml(sharedCode);
    }
  }, [sharedCode, lexedCode, tokens, lexErrors, parseErrorObjects, buildHighlightsFromTokens]);
  
  const lines = sharedCode.split('\n');
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
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Run Parser"}
          </button>
          <button className="btn ghost" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>

      {/* Grid layout: Top row (Source + Tokens), Bottom row (Terminal) */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr", gap: 16, flex: "1 1 auto", minHeight: 0 }}>
        {/* Top-Left: Source Code */}
        <div className="panel" style={{ display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Source Code</h3>
          <div style={{ position: "relative", flex: "1 1 auto", minHeight: 0, display: "flex", overflow: "hidden" }}>
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
                value={sharedCode}
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

        {/* Top-Right: Tokens Panel */}
        <div className="panel" style={{ display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
          <h3 style={{ margin: 0, marginBottom: 12 }}>Tokens</h3>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            <TokenList tokens={tokens} hideComments={hideComments} />
          </div>
        </div>

        {/* Bottom: Terminal / Errors Panel (full width) */}
        <div className="panel" style={{ gridColumn: "1 / -1", display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
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
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {lexErrors.length === 0 && parseErrors.length === 0 ? (
              <div style={{ color: "var(--success)", fontStyle: "italic", fontSize: "13px" }}>
                {tokens.length > 0 ? "No syntax errors" : "Run parser to analyze code"}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {/* Show lexical errors first */}
                {lexErrors.map((err, i) => (
                  <div key={`lex-${i}`} style={{
                    padding: "10px 14px",
                    background: "rgba(234, 179, 8, 0.08)",
                    border: "1px solid rgba(234, 179, 8, 0.3)",
                    borderLeft: "4px solid rgba(234, 179, 8, 0.8)",
                    borderRadius: 6,
                    fontSize: 13,
                  }}>
                    <div style={{ fontWeight: 600, color: "rgb(234, 179, 8)", marginBottom: 6, fontSize: 14 }}>
                      {err.message}
                    </div>
                    <div style={{ fontSize: 12, color: "rgba(234, 179, 8, 0.7)", fontWeight: 500 }}>
                      at line {err.line}, column {err.column}
                    </div>
                  </div>
                ))}
                
                {/* Show parse errors */}
                {parseErrorObjects.map((err, i) => {
                  // Format the error message to highlight bracketed content and put Unexpected/Expected on separate lines
                  const formatErrorMessage = (msg: string) => {
                    // First, extract header (everything before "Unexpected:")
                    const unexpectedMatch = msg.match(/^(.*?)(Unexpected:.*)/s);
                    if (!unexpectedMatch) {
                      // No "Unexpected:" found, just return with bracket highlighting
                      const parts = msg.split(/(\[.*?\])/g);
                      return parts.map((part, idx) => {
                        if (part.startsWith('[') && part.endsWith(']')) {
                          return (
                            <span key={idx} style={{ 
                              color: "rgba(248, 113, 113, 0.9)", 
                              fontWeight: 700,
                              background: "rgba(248, 113, 113, 0.15)",
                              padding: "2px 6px",
                              borderRadius: 3,
                              fontFamily: "var(--mono)"
                            }}>
                              {part}
                            </span>
                          );
                        }
                        return <span key={idx}>{part}</span>;
                      });
                    }

                    const header = unexpectedMatch[1].trim();
                    const rest = unexpectedMatch[2];

                    // Extract Unexpected and Expected parts
                    const expectedMatch = rest.match(/^(Unexpected:.*?)(Expected:.*)/s);
                    
                    const renderBracketedText = (text: string, keyPrefix: string) => {
                      const parts = text.split(/(\[.*?\])/g);
                      return parts.map((part, idx) => {
                        if (part.startsWith('[') && part.endsWith(']')) {
                          return (
                            <span key={`${keyPrefix}-${idx}`} style={{ 
                              color: "rgba(248, 113, 113, 0.9)", 
                              fontWeight: 700,
                              background: "rgba(248, 113, 113, 0.15)",
                              padding: "2px 6px",
                              borderRadius: 3,
                              fontFamily: "var(--mono)"
                            }}>
                              {part}
                            </span>
                          );
                        }
                        return <span key={`${keyPrefix}-${idx}`}>{part}</span>;
                      });
                    };

                    if (expectedMatch) {
                      const unexpectedPart = expectedMatch[1].trim();
                      const expectedPart = expectedMatch[2].trim();
                      
                      return (
                        <>
                          {header && <div style={{ marginBottom: 4 }}>{header}</div>}
                          <div style={{ marginBottom: 2 }}>{renderBracketedText(unexpectedPart, 'unexp')}</div>
                          <div>{renderBracketedText(expectedPart, 'exp')}</div>
                        </>
                      );
                    } else {
                      // Only Unexpected, no Expected
                      return (
                        <>
                          {header && <div style={{ marginBottom: 4 }}>{header}</div>}
                          <div>{renderBracketedText(rest, 'unexp')}</div>
                        </>
                      );
                    }
                  };

                  return (
                    <div key={`parse-${i}`} style={{
                      padding: "10px 14px",
                      background: "rgba(239, 68, 68, 0.08)",
                      border: "1px solid rgba(239, 68, 68, 0.3)",
                      borderLeft: "4px solid rgba(239, 68, 68, 0.8)",
                      borderRadius: 6,
                      fontSize: 13,
                    }}>
                      <div style={{ fontWeight: 600, color: "rgb(239, 68, 68)", marginBottom: 6, fontSize: 14, lineHeight: "1.6" }}>
                        {formatErrorMessage(err.message)}
                      </div>
                      {(err.line > 0 || err.column > 0) && (
                        <div style={{ fontSize: 12, color: "rgba(239, 68, 68, 0.7)", fontWeight: 500 }}>
                          at line {err.line}, column {err.column}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
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
