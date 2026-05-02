// src/components/LexerPanel.tsx
import { useRef, useState, useCallback } from "react";
import { lexCode, type Token, type LexError } from "../api";
import TokenList from "./TokenList";
import ErrorDisplay from "./ErrorDisplay";
import { PortiaEditor, type EditorError } from "../codemirror";

const EXAMPLE = `int main() {
    return 0;
}`;

type SimpleToken = Token & { start?: number; end?: number };

type LexerPanelProps = {
  sharedCode: string;
  setSharedCode: (code: string) => void;
  setSharedTokens: (tokens: Token[]) => void;
  setSharedLexErrors: (errors: LexError[]) => void;
  theme: "light" | "dark";
};

export default function LexerPanel({ sharedCode, setSharedCode, setSharedTokens, setSharedLexErrors, theme }: LexerPanelProps) {
  // Local state mirrors the latest manual lexer run. Shared state is updated
  // after a successful request so parser/semantic/ICG panels can reuse tokens.
  const [tokens, setTokens] = useState<SimpleToken[]>([]);
  const [errors, setErrors] = useState<LexError[]>([]);
  const [loading, setLoading] = useState(false);
  const [hideComments, setHideComments] = useState(false);
  
  const abortRef = useRef<AbortController | null>(null);

  // Convert LexErrors to EditorErrors for CodeMirror
  const editorErrors: EditorError[] = errors.map(err => ({
    line: err.line,
    column: err.column,
    message: err.message,
    errorType: "lexer" as const,
  }));

  // Normalize smart/curly quotes to straight quotes for lexer compatibility.
  // This prevents copy-pasted code from rich text editors from producing
  // misleading lexical errors around strings and chars.
  const normalizeQuotes = (text: string): string => {
    return text
      .replace(/[\u201C\u201D\u201E\u201F\u2033\u2036]/g, '"')  // " " „ ‟ ″ ‶ → "
      .replace(/[\u2018\u2019\u201A\u201B\u2032\u2035]/g, "'"); // ' ' ‚ ‛ ′ ‵ → '
  };

  // Run only the lexical phase. Any in-flight run is cancelled first so older
  // responses cannot overwrite the latest editor contents.
  async function runLex() {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    
    setLoading(true);
    setErrors([]);
    
    try {
      // Normalize quotes AND line endings before sending to lexer
      const normalizedCode = normalizeQuotes(sharedCode).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const resp = await lexCode(normalizedCode, { signal: controller.signal });
      setTokens(resp.tokens as SimpleToken[]);
      setErrors(resp.errors);
      
      // Update shared state for other panels
      setSharedCode(normalizedCode);
      setSharedTokens(resp.tokens);
      setSharedLexErrors(resp.errors);
    } catch (err: any) {
      if (err?.name !== 'AbortError') {
        setErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
        setTokens([]);
        setSharedTokens([]);
        setSharedLexErrors([{ message: err?.message ?? String(err), line: 0, column: 0 }]);
      }
    } finally {
      setLoading(false);
    }
  }

  // Update shared source text while leaving the previous token/error result
  // visible until the user explicitly runs the lexer again.
  const handleCodeChange = useCallback((value: string | undefined) => {
    if (value === undefined) return;
    // Normalize line endings to match what the backend will use
    const normalized = value.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    setSharedCode(normalized);
    // Tokens and errors stay visible for reference until user runs lexer again or clicks reset
  }, [setSharedCode]);

  // Restore the default sample and clear this panel's lexer output.
  const handleReset = useCallback(() => {
    setSharedCode(EXAMPLE);
    setTokens([]);
    setErrors([]);
  }, [setSharedCode]);

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
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12, flexShrink: 0 }}>
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
              color: errors.length > 0 ? "var(--text-muted)" : tokens.length > 0 ? "var(--success)" : "var(--text-muted)",
              fontWeight: tokens.length > 0 && errors.length === 0 ? 600 : 400,
              padding: tokens.length > 0 && errors.length === 0 ? "4px 12px" : "0",
              borderRadius: tokens.length > 0 && errors.length === 0 ? "12px" : "0",
              backgroundColor: tokens.length > 0 && errors.length === 0 ? "rgba(34, 197, 94, 0.1)" : "transparent",
              border: tokens.length > 0 && errors.length === 0 ? "1px solid rgba(34, 197, 94, 0.3)" : "none"
            }}>
              {errors.length > 0 ? `Lexical Errors: ${errors.length}` : tokens.length > 0 ? '✓ Lexing success' : 'Ready'}
            </div>
          </div>
          <div style={{ flex: "1 1 auto", overflow: "auto" }}>
            {errors.length === 0 ? (
              <div style={{ color: "var(--success)", fontStyle: "italic", fontSize: "13px" }}>
                {tokens.length > 0 ? "No lexical errors." : "Run lexer to analyze code"}
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <ErrorDisplay errors={errors} errorType="lexical" />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
