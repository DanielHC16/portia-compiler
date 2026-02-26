// src/components/SemanticPanel.tsx
import { useEffect, useRef, useState, useCallback } from "react";
import { lexCode, parseTokens, analyzeAst, type Token, type LexError } from "../api";
import TokenList from "./TokenList";
import ErrorDisplay from "./ErrorDisplay";
import { PortiaEditor, type EditorError } from "../codemirror";

// Console logging helper for semantic analysis
function logSemanticResult(symbolTable: any, success: boolean, errors: any[]) {
  if (success) {
    console.log(
      "%c✓ SEMANTIC ANALYSIS SUCCESSFUL",
      "color: #22c55e; font-weight: bold; font-size: 14px;"
    );
    console.log("%cSymbol Table:", "color: #a855f7; font-weight: bold;");
    console.table(
      Object.entries(symbolTable || {}).map(([name, info]: [string, any]) => ({
        ID: name,
        TYPE: info.dtype || info.ret_type || "-",
        DIMS: info.dims ? JSON.stringify(info.dims) : "-",
        DECLARED: info.line || "-",
        ACCESSED: "-",
        PARAMETERS: info.params ? info.params.map((p: any) => `${p.dtype} ${p.name}`).join(", ") : "-",
        ARGS: "-",
        VALUE: "-",
      }))
    );
    console.log("%cFull Symbol Table:", "color: #06b6d4;");
    console.dir(symbolTable, { depth: null });
  } else {
    console.log(
      "%c✗ SEMANTIC ANALYSIS FAILED",
      "color: #ef4444; font-weight: bold; font-size: 14px;"
    );
    console.error("%cSemantic Errors:", "color: #ef4444; font-weight: bold;", errors);
  }
}

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
  theme: "light" | "dark";
};

export default function SemanticPanel({ sharedCode, setSharedCode, sharedTokens, sharedLexErrors, theme }: SemanticPanelProps) {
  const [tokens, setTokens] = useState<SimpleToken[]>(sharedTokens as SimpleToken[] || []);
  const [lexErrors, setLexErrors] = useState<LexError[]>(sharedLexErrors || []);
  const [parseErrors, setParseErrors] = useState<LexError[]>([]);
  const [semanticErrors, setSemanticErrors] = useState<SemanticError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments] = useState(false);
  const [analysisComplete, setAnalysisComplete] = useState(false);
  
  const abortRef = useRef<AbortController | null>(null);

  // Sync tokens/errors with shared state when it changes
  useEffect(() => {
    setTokens(sharedTokens as SimpleToken[] || []);
    setLexErrors(sharedLexErrors || []);
  }, [sharedTokens, sharedLexErrors]);

  // Convert all errors to EditorErrors for CodeMirror
  const editorErrors: EditorError[] = [
    ...lexErrors.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "lexer" as const })),
    ...parseErrors.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "parser" as const })),
    ...semanticErrors.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "semantic" as const })),
  ];

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
      // Step 1: Lexer
      const normalizedCode = normalizeQuotes(sharedCode).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const lexResp = await lexCode(normalizedCode, { signal: controller.signal });
      setTokens(lexResp.tokens as SimpleToken[]);
      setLexErrors(lexResp.errors);
      
      if (lexResp.errors.length > 0) {
        setLoading(false);
        return;
      }
      
      // Step 2: Parser
      const tokensForParser = lexResp.tokens.filter((token: Token) => 
        !['space', 'newline', 'single_comment', 'multi_comment'].includes(token.type)
      );
      const parseResp = await parseTokens(tokensForParser, normalizedCode, lexResp.errors, { signal: controller.signal });
      
      if (!parseResp.success || !parseResp.ast) {
        console.error("Parse Errors:", parseResp.errors);
        if (parseResp.errors && parseResp.errors.length > 0) {
          const errorObjects = parseResp.errors.map((e: any) => {
            if (typeof e === 'object' && e.message) {
              return { message: e.message, line: e.line || 0, column: e.column || 0 };
            }
            return { message: String(e), line: 0, column: 0 };
          });
          setParseErrors(errorObjects);
        }
        setLoading(false);
        return;
      }
      
      console.log("AST:", parseResp.ast);
      
      // Step 3: Semantic Analysis
      try {
        const semanticResp = await analyzeAst(parseResp.ast, { signal: controller.signal });
        
        if (semanticResp.errors && semanticResp.errors.length > 0) {
          const semErrors = semanticResp.errors.map((e: any) => ({
            message: e.message || String(e),
            line: e.line || 0,
            column: e.column || 0,
            type: e.type || 'error'
          }));
          setSemanticErrors(semErrors);
          logSemanticResult(semanticResp.symbol_table, false, semErrors);
        } else {
          logSemanticResult(semanticResp.symbol_table, true, []);
        }
        
        setAnalysisComplete(true);
      } catch (err: any) {
        if (err?.name !== 'AbortError') {
          setSemanticErrors([{ message: err?.message ?? String(err), line: 0, column: 0, type: 'error' }]);
        }
      }
    } catch (err: any) {
      if (err?.name !== 'AbortError') {
        setLexErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
        setTokens([]);
      }
    } finally {
      setLoading(false);
    }
  }

  // Handle code changes
  const handleCodeChange = useCallback((value: string | undefined) => {
    if (value === undefined) return;
    const normalized = value.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    setSharedCode(normalized);
  }, [setSharedCode]);

  // Reset function
  const handleReset = useCallback(() => {
    setSharedCode(EXAMPLE);
    setTokens([]);
    setLexErrors([]);
    setParseErrors([]);
    setSemanticErrors([]);
    setAnalysisComplete(false);
  }, [setSharedCode]);

  // Get total error count
  const totalErrors = lexErrors.length + parseErrors.length + semanticErrors.length;

  // Convert semantic errors to CompilerError format for ErrorDisplay (preserving type)
  const semanticErrorsForDisplay = semanticErrors.map(e => ({
    message: e.message,
    line: e.line,
    column: e.column,
    type: e.type
  }));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Semantic Analyzer</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: 'center' }}>
          <button className="btn" onClick={runSemanticAnalysis} disabled={loading}>
            {loading ? "Analyzing..." : "Run Analyzer"}
          </button>
          <button className="btn ghost" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>

      {/* Flex layout: Top section (Source + Tokens/AST), Bottom section (Terminal) */}
      <div style={{ 
        display: "flex", 
        flexDirection: "column",
        flex: "1 1 auto", 
        minHeight: 0,
        overflow: "hidden",
        gap: 16
      }}>
        {/* Top: Source + Tokens/AST side by side - takes all remaining space */}
        <div style={{ 
          display: "flex", 
          flex: "1 1 0",
          gap: 16, 
          minHeight: 0,
          maxHeight: "calc(100% - 340px)",
          overflow: "hidden"
        }}>
          {/* Source Code */}
          <div className="panel" style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
            <h3 style={{ marginTop: 0, marginBottom: 8, flexShrink: 0 }}>Source Code</h3>
            <div style={{ flex: 1, minHeight: 0, overflow: "hidden" }}>
              <PortiaEditor
                value={sharedCode}
                onChange={handleCodeChange}
                theme={theme}
                errors={editorErrors}
              />
            </div>
          </div>

          {/* Tokens Panel */}
          <div className="panel" style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
            <h3 style={{ margin: 0, marginBottom: 12, flexShrink: 0 }}>Tokens</h3>
            <div style={{ flex: 1, minHeight: 0, overflow: "auto" }}>
              <TokenList tokens={tokens} hideComments={hideComments} />
            </div>
          </div>
        </div>

        {/* Bottom: Terminal / Errors Panel - FIXED 320px height */}
        <div className="panel" style={{ flex: "0 0 320px", display: "flex", flexDirection: "column", overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8, flexShrink: 0 }}>
            <h3 style={{ margin: 0 }}>Terminal</h3>
            <div className="small" style={{
              color: totalErrors > 0 ? "var(--text-muted)" : analysisComplete ? "var(--success)" : "var(--text-muted)",
              fontWeight: analysisComplete && totalErrors === 0 ? 600 : 400,
              padding: analysisComplete && totalErrors === 0 ? "4px 12px" : "0",
              borderRadius: analysisComplete && totalErrors === 0 ? "12px" : "0",
              backgroundColor: analysisComplete && totalErrors === 0 ? "rgba(34, 197, 94, 0.1)" : "transparent",
              border: analysisComplete && totalErrors === 0 ? "1px solid rgba(34, 197, 94, 0.3)" : "none"
            }}>
              {lexErrors.length > 0 ? `Lexical Errors: ${lexErrors.length}` : 
               parseErrors.length > 0 ? `Syntax Errors: ${parseErrors.length}` : 
               semanticErrors.length > 0 ? `Semantic Errors: ${semanticErrors.length}` :
               analysisComplete ? '✓ Analysis complete' : 'Ready'}
            </div>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {totalErrors === 0 ? (
              <div style={{ color: analysisComplete ? "var(--success)" : "var(--text-muted)", fontStyle: "italic", fontSize: "13px" }}>
                {analysisComplete ? "No errors found." : "Run analyzer to check code"}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <ErrorDisplay errors={lexErrors} errorType="lexical" />
                <ErrorDisplay errors={parseErrors} errorType="syntax" />
                <ErrorDisplay errors={semanticErrorsForDisplay} errorType="semantic" />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
