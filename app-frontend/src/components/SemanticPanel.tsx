// src/components/SemanticPanel.tsx
import { useEffect, useRef, useState, useCallback } from "react";
import { lexCode, parseTokens, analyzeAst, type Token, type LexError } from "../api";
import TokenList from "./TokenList";
import ErrorDisplay from "./ErrorDisplay";

const EXAMPLE = `int main() {
    return 0;
}`;

type SimpleToken = Token & { start?: number; end?: number };

type SemanticError = {
  message: string;
  line: number;
  column: number;
  type?: string;
};

type SemanticPanelProps = {
  sharedCode: string;
  setSharedCode: (code: string) => void;
  sharedTokens: Token[];
  sharedLexErrors: LexError[];
};

export default function SemanticPanel({ sharedCode, setSharedCode, sharedTokens, sharedLexErrors }: SemanticPanelProps) {
  const [lexedCode, setLexedCode] = useState<string>(sharedCode || "");
  const [tokens, setTokens] = useState<SimpleToken[]>(sharedTokens as SimpleToken[] || []);
  const [lexErrors, setLexErrors] = useState<LexError[]>(sharedLexErrors || []);
  const [parseErrors, setParseErrors] = useState<LexError[]>([]);
  const [semanticErrors, setSemanticErrors] = useState<SemanticError[]>([]);
  const [ast, setAst] = useState<any>(null);
  const [rightPanelView, setRightPanelView] = useState<'tokens' | 'ast'>('tokens');
  const [loading, setLoading] = useState(false);
  const [hideComments, _setHideComments] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  
  // Sync tokens/errors with shared state when it changes
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

  // Run full pipeline: lexer -> parser -> semantic
  async function runSemanticAnalysis() {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    
    setLoading(true);
    setLexErrors([]);
    setParseErrors([]);
    setSemanticErrors([]);
    setAnalysisComplete(false);
    
    try {
      // Step 1: Run lexer
      const normalizedCode = normalizeQuotes(sharedCode).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const lexResp = await lexCode(normalizedCode, { signal: controller.signal });
      setTokens(lexResp.tokens as SimpleToken[]);
      setLexErrors(lexResp.errors);
      setLexedCode(normalizedCode);
      
      if (lexResp.errors.length > 0) {
        setAst(null);
        return;
      }
      
      // Step 2: Run parser
      const tokensForParser = lexResp.tokens.filter((token: Token) => 
        !['space', 'newline', 'single_comment', 'multi_comment'].includes(token.type)
      );
      const parseResp = await parseTokens(tokensForParser, normalizedCode, lexResp.errors, { signal: controller.signal });
      
      if (!parseResp.success || !parseResp.ast) {
        const errorObjects = parseResp.errors?.map((e: any) => ({
          message: e.message || String(e),
          line: e.line || 0,
          column: e.column || 0,
          token_length: e.token_length || 0
        })) || [{ message: "Parse failed", line: 0, column: 0, token_length: 0 }];
        setParseErrors(errorObjects);
        setAst(null);
        return;
      }
      
      setAst(parseResp.ast);
      setParseErrors([]);
      
      // Step 3: Run semantic analysis
      try {
        const semanticResp = await analyzeAst(parseResp.ast, { signal: controller.signal });
        
        if (semanticResp.errors && semanticResp.errors.length > 0) {
          setSemanticErrors(semanticResp.errors.map((e: any) => ({
            message: e.message || String(e),
            line: e.line || 0,
            column: e.column || 0,
            type: e.type || 'semantic_error'
          })));
        } else {
          setSemanticErrors([]);
          setAnalysisComplete(true);
        }
      } catch (err: any) {
        if (err?.name !== 'AbortError') {
          setSemanticErrors([{ message: err?.message ?? String(err), line: 0, column: 0, type: 'internal_error' }]);
        }
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

  // Reset function
  const handleReset = useCallback(() => {
    setSharedCode(EXAMPLE);
    setTokens([]);
    setLexErrors([]);
    setParseErrors([]);
    setSemanticErrors([]);
    setAst(null);
    setRightPanelView('tokens');
    setLexedCode("");
    setAnalysisComplete(false);
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
      const lineStarts: number[] = [0];
      for (let i = 0; i < src.length; i++) {
        if (src[i] === '\n') lineStarts.push(i + 1);
      }

      type Range = { start: number; end: number; cls?: string; isError: boolean };
      const tokenRanges: Range[] = [];
      const errorRanges: Range[] = [];

      for (const tok of toks) {
        if (!tok.lexeme || tok.line === undefined || tok.column === undefined) continue;
        if (tok.line < 1 || tok.line > lineStarts.length) continue;
        
        const lineStart = lineStarts[tok.line - 1];
        let start = lineStart + tok.column - 1;
        let end = start + tok.lexeme.length;
        
        if (start >= 0 && end <= src.length && src.slice(start, end) === tok.lexeme) {
          tokenRanges.push({ start, end, cls: tokenClass(tok.type), isError: false });
        }
      }

      for (const err of errs) {
        if (err.line === undefined || err.line < 1 || err.column === undefined || err.column < 1) continue;
        if (err.line > lineStarts.length) continue;

        const lineStart = lineStarts[err.line - 1];
        const errorStart = lineStart + err.column - 1;
        const errorLength = (err as any).token_length || 1;
        const errorEnd = errorStart + errorLength;

        if (errorStart >= 0 && errorEnd <= src.length) {
          errorRanges.push({ start: errorStart, end: errorEnd, cls: 'hl-error', isError: true });
        }
      }

      const allRanges = [...tokenRanges, ...errorRanges];
      if (allRanges.length === 0) return [{ text: src, cls: undefined }];

      allRanges.sort((a, b) => a.start - b.start || (a.isError ? -1 : 1));

      const segments: { text: string; cls?: string }[] = [];
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

        const coveringRanges = allRanges.filter(r => r.start <= segStart && r.end >= segEnd);
        
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
      return [{ text: src, cls: undefined }];
    }
  }, []);

  const highlightedHTML = useCallback(() => {
    try {
      const allErrors = [...lexErrors, ...parseErrors, ...semanticErrors.map(e => ({ ...e, token_length: 1 }))];
      if (lexedCode && sharedCode === lexedCode && (tokens.length > 0 || allErrors.length > 0)) {
        const rawSegments = buildHighlightsFromTokens(sharedCode, tokens, allErrors as LexError[]);
        const html = rawSegments
          .map(s => s.cls ? `<span class="${s.cls}">${escapeHtml(s.text)}</span>` : escapeHtml(s.text))
          .join("");
        return html || escapeHtml(sharedCode);
      }
      return escapeHtml(sharedCode);
    } catch (e) {
      return escapeHtml(sharedCode);
    }
  }, [sharedCode, lexedCode, tokens, lexErrors, parseErrors, semanticErrors, buildHighlightsFromTokens]);
  
  const lines = sharedCode.split('\n');
  const lineCount = lines.length;
  const lineNumbers = Array.from({ length: lineCount }, (_, i) => i + 1);

  // Determine overall status
  const hasErrors = lexErrors.length > 0 || parseErrors.length > 0 || semanticErrors.length > 0;
  const isSuccess = analysisComplete && !hasErrors;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Semantic Analyzer</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: 'center' }}>
          <button 
            className="btn" 
            onClick={runSemanticAnalysis} 
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Run Analyzer"}
          </button>
          <button className="btn ghost" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>

      {/* Grid layout: Top row (Source + Tokens/AST), Bottom row (Terminal) */}
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

        {/* Top-Right: Tokens / AST Panel with toggle */}
        <div className="panel" style={{ display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <h3 style={{ margin: 0 }}>{rightPanelView === 'tokens' ? 'Tokens' : 'AST'}</h3>
            <div style={{ display: "flex", gap: 4 }}>
              <button 
                className={`btn small ${rightPanelView === 'tokens' ? '' : 'ghost'}`}
                onClick={() => setRightPanelView('tokens')}
                style={{ padding: '4px 12px', fontSize: 12 }}
              >
                Tokens
              </button>
              <button 
                className={`btn small ${rightPanelView === 'ast' ? '' : 'ghost'}`}
                onClick={() => setRightPanelView('ast')}
                disabled={!ast}
                style={{ padding: '4px 12px', fontSize: 12, opacity: ast ? 1 : 0.5 }}
              >
                AST
              </button>
            </div>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {rightPanelView === 'tokens' ? (
              <TokenList tokens={tokens} hideComments={hideComments} />
            ) : (
              <pre style={{
                margin: 0,
                padding: 8,
                fontSize: 12,
                fontFamily: "var(--mono)",
                whiteSpace: "pre-wrap",
                wordWrap: "break-word",
                lineHeight: 1.5,
              }}>
                {ast ? JSON.stringify(ast, null, 2) : "No AST available. Run analyzer first."}
              </pre>
            )}
          </div>
        </div>

        {/* Bottom: Terminal / Results Panel (full width) */}
        <div className="panel" style={{ gridColumn: "1 / -1", display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <h3 style={{ margin: 0 }}>Terminal</h3>
            <div className="small" style={{
              color: hasErrors ? "var(--text-muted)" : isSuccess ? "var(--success)" : "var(--text-muted)",
              fontWeight: isSuccess ? 600 : 400,
              padding: isSuccess ? "4px 12px" : "0",
              borderRadius: isSuccess ? "12px" : "0",
              backgroundColor: isSuccess ? "rgba(34, 197, 94, 0.1)" : "transparent",
              border: isSuccess ? "1px solid rgba(34, 197, 94, 0.3)" : "none"
            }}>
              {lexErrors.length > 0 ? `Lexical Errors: ${lexErrors.length}` : 
               parseErrors.length > 0 ? `Syntax Errors: ${parseErrors.length}` : 
               semanticErrors.length > 0 ? `Semantic Errors: ${semanticErrors.length}` :
               isSuccess ? '✓ Semantic Analysis Complete' : 'Ready'}
            </div>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {!hasErrors ? (
              <div style={{ color: isSuccess ? "var(--success)" : "var(--text-muted)", fontStyle: "italic", fontSize: "13px" }}>
                {isSuccess ? "Semantic analysis successful. No errors found." : "Run analyzer to check code"}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {/* Lexical errors */}
                <ErrorDisplay errors={lexErrors} errorType="lexical" />
                
                {/* Parse errors */}
                <ErrorDisplay errors={parseErrors} errorType="syntax" />
                
                {/* Semantic errors */}
                <ErrorDisplay errors={semanticErrors} errorType="semantic" />
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
