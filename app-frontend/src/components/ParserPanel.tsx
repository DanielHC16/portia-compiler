// src/components/ParserPanel.tsx
import { useEffect, useRef, useState, useCallback } from "react";
import { lexCode, parseTokens, type Token, type LexError } from "../api";
import TokenList from "./TokenList";
import ErrorDisplay from "./ErrorDisplay";
import { PortiaEditor, type EditorError } from "../codemirror";

const EXAMPLE = `int main() {
    return 0;
}`;

type SimpleToken = Token & { start?: number; end?: number };

type ParserPanelProps = {
  sharedCode: string;
  setSharedCode: (code: string) => void;
  sharedTokens: Token[];
  sharedLexErrors: LexError[];
  theme: "light" | "dark";
};

export default function ParserPanel({ sharedCode, setSharedCode, sharedTokens, sharedLexErrors, theme }: ParserPanelProps) {
  const [tokens, setTokens] = useState<SimpleToken[]>(sharedTokens as SimpleToken[] || []);
  const [lexErrors, setLexErrors] = useState<LexError[]>(sharedLexErrors || []);
  const [parseErrors, setParseErrors] = useState<string[]>([]);
  const [parseErrorObjects, setParseErrorObjects] = useState<LexError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments] = useState(false);
  
  const abortRef = useRef<AbortController | null>(null);

  // Sync tokens/errors with shared state when it changes
  useEffect(() => {
    setTokens(sharedTokens as SimpleToken[] || []);
    setLexErrors(sharedLexErrors || []);
  }, [sharedTokens, sharedLexErrors]);

  // Convert errors to EditorErrors for CodeMirror
  const editorErrors: EditorError[] = [
    ...lexErrors.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "lexer" as const })),
    ...parseErrorObjects.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "parser" as const })),
  ];

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
    setParseErrorObjects([]);
    
    try {
      // First run lexer
      const normalizedCode = normalizeQuotes(sharedCode).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const lexResp = await lexCode(normalizedCode, { signal: controller.signal });
      setTokens(lexResp.tokens as SimpleToken[]);
      setLexErrors(lexResp.errors);
      
      // If no lexical errors, run parser
      if (lexResp.errors.length === 0) {
        try {
          // Filter out whitespace, newline, and comment tokens before parsing
          const tokensForParser = lexResp.tokens.filter((token: Token) => 
            !['space', 'newline', 'single_comment', 'multi_comment'].includes(token.type)
          );
          const parseResp = await parseTokens(tokensForParser, normalizedCode, lexResp.errors, { signal: controller.signal });
          
          // Check if parser succeeded
          if (parseResp.success && parseResp.ast) {
            setParseErrors([]);
            setParseErrorObjects([]);
          } else if (parseResp.errors && parseResp.errors.length > 0) {
            const errorObjects = parseResp.errors.map((e: any) => {
              if (typeof e === 'object' && e.message) {
                return { 
                  message: e.message, 
                  line: e.line || 0, 
                  column: e.column || 0,
                  token_length: e.token_length || 0
                };
              }
              return { message: String(e), line: 0, column: 0, token_length: 0 };
            });
            const errorMessages = errorObjects.map((e: any) => e.message);
            setParseErrors(errorMessages);
            setParseErrorObjects(errorObjects);
          } else {
            setParseErrors([]);
            setParseErrorObjects([]);
          }
        } catch (err: any) {
          if (err?.name !== 'AbortError') {
            setParseErrors([err?.message ?? String(err)]);
          }
        }
      } else {
        setParseErrors(["Cannot parse: lexical errors present"]);
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
    setParseErrorObjects([]);
  }, [setSharedCode]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Syntax Analyzer</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: 'center' }}>
          <button className="btn" onClick={runParser} disabled={loading}>
            {loading ? "Analyzing..." : "Run Parser"}
          </button>
          <button className="btn ghost" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>

      {/* Flex layout: Top section (Source + Tokens), Bottom section (Terminal) */}
      <div style={{ 
        display: "flex", 
        flexDirection: "column",
        flex: "1 1 auto", 
        minHeight: 0,
        overflow: "hidden",
        gap: 16
      }}>
        {/* Top: Source + Tokens side by side - takes all remaining space */}
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
              color: (lexErrors.length > 0 || parseErrors.length > 0) ? "var(--text-muted)" : tokens.length > 0 ? "var(--success)" : "var(--text-muted)",
              fontWeight: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? 600 : 400,
              padding: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "4px 12px" : "0",
              borderRadius: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "12px" : "0",
              backgroundColor: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "rgba(34, 197, 94, 0.1)" : "transparent",
              border: tokens.length > 0 && lexErrors.length === 0 && parseErrors.length === 0 ? "1px solid rgba(34, 197, 94, 0.3)" : "none"
            }}>
              {lexErrors.length > 0 ? `Lexical Errors: ${lexErrors.length}` : 
               parseErrors.length > 0 ? `Syntax Errors: ${parseErrors.length}` : 
               tokens.length > 0 ? '✓ Parse complete' : 'Ready'}
            </div>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {lexErrors.length === 0 && parseErrors.length === 0 ? (
              <div style={{ color: "var(--success)", fontStyle: "italic", fontSize: "13px" }}>
                {tokens.length > 0 ? "No syntax errors." : "Run parser to analyze code"}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <ErrorDisplay errors={lexErrors} errorType="lexical" />
                <ErrorDisplay errors={parseErrorObjects} errorType="syntax" />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
