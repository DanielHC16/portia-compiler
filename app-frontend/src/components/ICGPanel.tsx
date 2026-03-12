// src/components/ICGPanel.tsx
import { useEffect, useRef, useState, useCallback } from "react";
import { lexCode, parseTokens, analyzeAst, runProgram, type Token, type LexError, type RunResponse } from "../api";
import ErrorDisplay from "./ErrorDisplay";
import { PortiaEditor, type EditorError } from "../codemirror";

// Console logging helper for ICG results
function logICGResult(tac: any, tacText: string | null, output: string[], success: boolean, errors: any[]) {
  if (success) {
    console.log(
      "%c✓ ICG EXECUTION SUCCESSFUL",
      "color: #22c55e; font-weight: bold; font-size: 14px;"
    );
    if (tac && tac.triples && tac.triples.length > 0) {
      console.log("%c=== Generated TAC (Indirect Triples) ===", "color: #a855f7; font-weight: bold;");
      console.log("%c┌───────┬────────────┬────────────┬────────────┬──────┬─────┐", "color: #888;");
      console.log("%c│ Index │     Op     │    Arg1    │    Arg2    │ Line │ Col │", "color: #a855f7; font-weight: bold;");
      console.log("%c├───────┼────────────┼────────────┼────────────┼──────┼─────┤", "color: #888;");
      tac.triples.forEach((triple: any, idx: number) => {
        const op = String(triple.op || '-').padEnd(10).substring(0, 10);
        const arg1 = formatArg(triple.arg1).padEnd(10).substring(0, 10);
        const arg2 = formatArg(triple.arg2).padEnd(10).substring(0, 10);
        const line = String(triple.line || '-').padStart(4);
        const col = String(triple.col || '-').padStart(3);
        console.log(`%c│ ${String(idx).padStart(5)} │ ${op} │ ${arg1} │ ${arg2} │ ${line} │ ${col} │`, "color: #888;");
      });
      console.log("%c└───────┴────────────┴────────────┴────────────┴──────┴─────┘", "color: #888;");
      console.log("%cPointer Order: [" + tac.pointers.join(", ") + "]", "color: #666; font-style: italic;");
    } else if (tacText) {
      console.log("%cGenerated TAC:", "color: #a855f7; font-weight: bold;");
      console.log(tacText);
    }
    if (output.length > 0) {
      console.log("%cProgram Output:", "color: #06b6d4; font-weight: bold;");
      output.forEach(line => console.log(line));
    }
  } else {
    console.log(
      "%c✗ ICG EXECUTION FAILED",
      "color: #ef4444; font-weight: bold; font-size: 14px;"
    );
    console.error("%cErrors:", "color: #ef4444; font-weight: bold;", errors);
  }
}

// Format TAC argument for display
function formatArg(arg: any): string {
  if (arg === null || arg === undefined) return '-';
  if (typeof arg === 'object' && 'ref' in arg) return `(${arg.ref})`;
  return String(arg);
}

const EXAMPLE = `int main() {
    return 0;
}`;

type ICGError = {
  message: string;
  line: number;
  column: number;
  type?: string;
  token_length?: number;
};

type ICGPanelProps = {
  sharedCode: string;
  setSharedCode: (code: string) => void;
  sharedTokens: Token[];
  sharedLexErrors: LexError[];
  theme: "light" | "dark";
};

// Terminal line types for unified terminal display
type TerminalLine = {
  type: "output" | "input" | "error";
  content: string;
};

// Input validation functions
function validateInput(value: string, expectedType: string): { valid: boolean; error?: string } {
  const trimmed = value.trim();
  const type = (expectedType || "string").toLowerCase();
  
  if (type === "int" || type === "long") {
    if (!/^-?\d+$/.test(trimmed)) {
      return { valid: false, error: `Invalid input type. Expected ${type}.` };
    }
    return { valid: true };
  }
  
  if (type === "float" || type === "double") {
    if (!/^-?\d+(\.\d+)?$/.test(trimmed) && !/^-?\d+$/.test(trimmed)) {
      return { valid: false, error: `Invalid input type. Expected ${type}.` };
    }
    return { valid: true };
  }
  
  if (type === "bool") {
    const lower = trimmed.toLowerCase();
    if (!["true", "false"].includes(lower)) {
      return { valid: false, error: `Invalid input type. Expected ${type}.` };
    }
    return { valid: true };
  }
  
  if (type === "char") {
    if (trimmed.length !== 1) {
      return { valid: false, error: `Invalid input type. Expected single character.` };
    }
    return { valid: true };
  }
  
  // string or unknown - accept anything
  return { valid: true };
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export default function ICGPanel({ sharedCode, setSharedCode, sharedTokens: _sharedTokens, sharedLexErrors, theme }: ICGPanelProps) {
  // Compiler error states (for editor highlighting)
  const [lexErrors, setLexErrors] = useState<LexError[]>(sharedLexErrors || []);
  const [parseErrors, setParseErrors] = useState<LexError[]>([]);
  const [semanticErrors, setSemanticErrors] = useState<ICGError[]>([]);
  const [icgErrors, setIcgErrors] = useState<ICGError[]>([]);
  
  // Execution states
  const [loading, setLoading] = useState(false);
  const [executionComplete, setExecutionComplete] = useState(false);
  const [currentAst, setCurrentAst] = useState<any>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_currentSymbolTable, setCurrentSymbolTable] = useState<any>(null);
  
  // Terminal state - single unified buffer
  const [terminalLines, setTerminalLines] = useState<TerminalLine[]>([]);
  
  // Input state
  const [waitingForInput, setWaitingForInput] = useState(false);
  const [expectedInputType, setExpectedInputType] = useState<string | null>(null);
  const [inputLine, setInputLine] = useState<number>(0);
  const [inputCol, setInputCol] = useState<number>(0);
  const [pendingInputs, setPendingInputs] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState<string>("");
  
  const inputRef = useRef<HTMLInputElement>(null);
  const terminalRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);
  const consumedOutputCountRef = useRef<number>(0);
  const previousBackendOutputRef = useRef<string[]>([]);  // Store actual output strings

  // Sync errors with shared state
  useEffect(() => {
    setLexErrors(sharedLexErrors || []);
  }, [sharedLexErrors]);

  // Auto-scroll terminal to bottom when content changes
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [terminalLines, waitingForInput]);

  // Auto-focus input when waiting for input
  useEffect(() => {
    if (waitingForInput && inputRef.current) {
      inputRef.current.focus();
    }
  }, [waitingForInput]);

  // Convert errors to EditorErrors for CodeMirror
  const editorErrors: EditorError[] = [
    ...lexErrors.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "lexer" as const })),
    ...parseErrors.map(err => ({ line: err.line, column: err.column, message: err.message, errorType: "parser" as const })),
    ...semanticErrors.map(err => ({ line: err.line, column: err.column, message: err.message, token_length: err.token_length, errorType: "semantic" as const })),
    ...icgErrors.map(err => ({ line: err.line, column: err.column, message: err.message, token_length: err.token_length, errorType: "semantic" as const })),
  ];

  // Normalize smart/curly quotes
  const normalizeQuotes = (text: string): string => {
    return text
      .replace(/[\u201C\u201D\u201E\u201F\u2033\u2036]/g, '"')
      .replace(/[\u2018\u2019\u201A\u201B\u2032\u2035]/g, "'");
  };

  // Add line to terminal
  const appendTerminalLine = useCallback((type: TerminalLine["type"], content: string) => {
    setTerminalLines(prev => [...prev, { type, content }]);
  }, []);

  // Add multiple output lines
  const appendOutputLines = useCallback((lines: string[]) => {
    setTerminalLines(prev => [
      ...prev,
      ...lines.map(content => ({ type: "output" as const, content }))
    ]);
  }, []);

  // Run full pipeline: lexer -> parser -> semantic -> ICG
  async function runICG(inputs: string[] = [], appendMode: boolean = false) {
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    
    setLoading(true);
    setLexErrors([]);
    setParseErrors([]);
    setSemanticErrors([]);
    setIcgErrors([]);
    
    // Clear terminal only if not appending (fresh run)
    if (!appendMode) {
      setTerminalLines([]);
      consumedOutputCountRef.current = 0;
      previousBackendOutputRef.current = [];
    }
    
    setExecutionComplete(false);
    setWaitingForInput(false);
    setExpectedInputType(null);
    
    try {
      // Step 1: Lexer
      const normalizedCode = normalizeQuotes(sharedCode).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      const lexResp = await lexCode(normalizedCode, { signal: controller.signal });
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
      
      // Step 3: Semantic Analysis
      const semanticResp = await analyzeAst(parseResp.ast, { signal: controller.signal });
      
      if (semanticResp.errors && semanticResp.errors.length > 0) {
        const semErrors = semanticResp.errors.map((e: any) => ({
          message: e.message || String(e),
          line: e.line || 0,
          column: e.column || 0,
          type: e.type || 'error',
          token_length: e.token_length || 0
        }));
        setSemanticErrors(semErrors);
        setLoading(false);
        return;
      }
      
      // Store for re-execution
      setCurrentAst(parseResp.ast);
      setCurrentSymbolTable(semanticResp.symbol_table);
      
      // Step 4: ICG - Generate and Execute
      const icgResp: RunResponse = await runProgram(
        parseResp.ast,
        inputs,
        semanticResp.symbol_table,
        { signal: controller.signal }
      );
      
      // Append output lines to terminal (only new ones in append mode)
      console.log('[ICG DEBUG] output handling:', { 
        appendMode, 
        outputLength: icgResp.output.length, 
        output: icgResp.output,
        prevOutput: previousBackendOutputRef.current
      });
      
      if (icgResp.output.length > 0) {
        if (appendMode) {
          // Handle output after trap() input
          // Compare with previous backend output to find what's new
          const prevOutput = previousBackendOutputRef.current;
          const newOutput = icgResp.output;
          
          console.log('[ICG DEBUG] appendMode comparison:', { 
            prevOutput, 
            newOutput
          });
          
          // Find new content to display
          const linesToAdd: string[] = [];
          
          // Process each line from backend output
          for (let i = 0; i < newOutput.length; i++) {
            if (i >= prevOutput.length) {
              // Completely new line
              linesToAdd.push(newOutput[i]);
              console.log('[ICG DEBUG] new line:', newOutput[i]);
            } else if (newOutput[i] !== prevOutput[i]) {
              // Line content changed
              if (newOutput[i].startsWith(prevOutput[i])) {
                // Line grew - only add the new part
                const newPart = newOutput[i].slice(prevOutput[i].length);
                if (newPart) {
                  linesToAdd.push(newPart);
                  console.log('[ICG DEBUG] line grew, new part:', newPart);
                }
              } else {
                // Line replaced - add the whole new line
                linesToAdd.push(newOutput[i]);
                console.log('[ICG DEBUG] line replaced:', newOutput[i]);
              }
            }
          }
          
          console.log('[ICG DEBUG] lines to add:', linesToAdd);
          
          if (linesToAdd.length > 0) {
            appendOutputLines(linesToAdd);
          }
        } else {
          console.log('[ICG DEBUG] not appendMode, adding all outputs');
          appendOutputLines(icgResp.output);
        }
        
        // Always update the stored previous output
        previousBackendOutputRef.current = [...icgResp.output];
        consumedOutputCountRef.current = icgResp.output.length;
        console.log('[ICG DEBUG] updated refs:', { 
          prevOutput: previousBackendOutputRef.current,
          consumedCount: consumedOutputCountRef.current
        });
      }
      
      if (!icgResp.success && icgResp.errors.length > 0) {
        const icgErrs = icgResp.errors.map((e: any) => ({
          message: e.message || String(e),
          line: e.line || 0,
          column: e.column || 0,
          type: e.type || 'runtime_error',
          token_length: e.token_length || 0
        }));
        setIcgErrors(icgErrs);
        logICGResult(icgResp.tac, icgResp.tac_text, icgResp.output, false, icgErrs);
      } else if (icgResp.waiting_for_input) {
        // Program needs input
        logICGResult(icgResp.tac, icgResp.tac_text, icgResp.output, true, []);
        setWaitingForInput(true);
        setExpectedInputType(icgResp.input_var_type);
        setInputLine(icgResp.input_line);
        setInputCol(icgResp.input_col);
        setLoading(false);
        return;
      } else {
        logICGResult(icgResp.tac, icgResp.tac_text, icgResp.output, true, []);
      }
      
      setExecutionComplete(true);
    } catch (err: any) {
      if (err?.name !== 'AbortError') {
        setIcgErrors([{ message: err?.message ?? String(err), line: 0, column: 0, type: 'error' }]);
      }
    } finally {
      setLoading(false);
    }
  }

  // Handle input submission
  const handleInputSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    
    if (!waitingForInput || !expectedInputType) return;
    
    const value = inputValue;
    
    // Validate input
    const validation = validateInput(value, expectedInputType);
    
    if (!validation.valid) {
      // Show error in terminal - exact format required
      appendTerminalLine("input", `> ${value}`);
      appendTerminalLine("error", "");
      appendTerminalLine("error", "ERROR: RuntimeError");
      appendTerminalLine("error", `Line: ${inputLine}`);
      appendTerminalLine("error", `Column: ${inputCol}`);
      appendTerminalLine("error", `Message: ${validation.error}`);
      appendTerminalLine("error", "");
      
      // Clear input but keep waiting for valid input
      setInputValue("");
      return;
    }
    
    // Valid input - append to terminal and resume
    appendTerminalLine("input", `> ${value}`);
    
    const newInputs = [...pendingInputs, value];
    setPendingInputs(newInputs);
    setWaitingForInput(false);
    setExpectedInputType(null);
    setInputValue("");
    
    // Re-run with accumulated inputs (append mode to keep terminal history)
    if (currentAst) {
      runICG(newInputs, true);
    }
  }, [waitingForInput, expectedInputType, inputValue, pendingInputs, currentAst, inputLine, inputCol, appendTerminalLine]);

  // Handle code changes
  const handleCodeChange = useCallback((value: string | undefined) => {
    if (value === undefined) return;
    const normalized = value.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    setSharedCode(normalized);
    setTerminalLines([]);
    consumedOutputCountRef.current = 0;
    previousBackendOutputRef.current = [];
    setExecutionComplete(false);
    setPendingInputs([]);
    setWaitingForInput(false);
  }, [setSharedCode]);

  // Reset function
  const handleReset = useCallback(() => {
    setSharedCode(EXAMPLE);
    setLexErrors([]);
    setParseErrors([]);
    consumedOutputCountRef.current = 0;
    previousBackendOutputRef.current = [];
    setSemanticErrors([]);
    setIcgErrors([]);
    setTerminalLines([]);
    setExecutionComplete(false);
    setCurrentAst(null);
    setCurrentSymbolTable(null);
    setPendingInputs([]);
    setWaitingForInput(false);
    setExpectedInputType(null);
    setInputValue("");
  }, [setSharedCode]);

  // Get total error count (compiler errors only, not runtime validation errors)
  const compilerErrors = lexErrors.length + parseErrors.length + semanticErrors.length + icgErrors.length;

  // Get status message
  const getStatusMessage = () => {
    if (lexErrors.length > 0) return `Lexical Errors: ${lexErrors.length}`;
    if (parseErrors.length > 0) return `Syntax Errors: ${parseErrors.length}`;
    if (semanticErrors.length > 0) return `Semantic Errors: ${semanticErrors.length}`;
    if (icgErrors.length > 0) return `Runtime Errors: ${icgErrors.length}`;
    if (waitingForInput) return 'Waiting for input...';
    if (executionComplete) return '✓ Execution complete';
    return 'Ready';
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, height: "100%", padding: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h2 style={{ margin: 0 }}>Intermediate Code Generator</h2>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: 'center' }}>
          <button className="btn" onClick={() => { setPendingInputs([]); runICG([]); }} disabled={loading}>
            {loading ? "Running..." : "Run Program"}
          </button>
          <button className="btn ghost" onClick={handleReset}>
            Reset
          </button>
        </div>
      </div>

      {/* Two-column layout: Source Code | Terminal */}
      <div style={{ 
        display: "flex", 
        flex: "1 1 auto", 
        minHeight: 0,
        overflow: "hidden",
        gap: 16
      }}>
        {/* Source Code Panel */}
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

        {/* Terminal Panel - Single scrollable area */}
        <div className="panel" style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0, overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8, flexShrink: 0 }}>
            <h3 style={{ margin: 0 }}>Terminal</h3>
            <div className="small" style={{
              color: compilerErrors > 0 ? "var(--error)" : executionComplete ? "var(--success)" : "var(--text-muted)",
              fontWeight: executionComplete && compilerErrors === 0 ? 600 : 400,
              padding: executionComplete && compilerErrors === 0 ? "4px 12px" : "0",
              borderRadius: executionComplete && compilerErrors === 0 ? "12px" : "0",
              backgroundColor: executionComplete && compilerErrors === 0 ? "rgba(34, 197, 94, 0.1)" : "transparent",
              border: executionComplete && compilerErrors === 0 ? "1px solid rgba(34, 197, 94, 0.3)" : "none"
            }}>
              {getStatusMessage()}
            </div>
          </div>
          
          {/* Single terminal area */}
          <div 
            ref={terminalRef}
            style={{ 
              flex: "1 1 auto", 
              overflow: "auto", 
              fontFamily: "var(--mono)", 
              fontSize: "13px",
              background: "var(--bg)",
              padding: 12,
              borderRadius: 6,
              border: "1px solid var(--border)"
            }}
          >
            {/* Compiler Errors (if any) */}
            {compilerErrors > 0 && (
              <div style={{ marginBottom: 8 }}>
                <ErrorDisplay errors={lexErrors} errorType="lexical" />
                <ErrorDisplay errors={parseErrors} errorType="syntax" />
                <ErrorDisplay errors={semanticErrors.map(e => ({ message: e.message, line: e.line, column: e.column, type: e.type }))} errorType="semantic" />
                <ErrorDisplay errors={icgErrors.map(e => ({ message: e.message, line: e.line, column: e.column, type: e.type }))} errorType="runtime" />
              </div>
            )}
            
            {/* Terminal output stream */}
            {compilerErrors === 0 && (
              <>
                {terminalLines.map((line, i) => (
                  <div 
                    key={i} 
                    style={{ 
                      color: line.type === "error" ? "var(--error)" : 
                             line.type === "input" ? "var(--accent)" : 
                             "var(--text)",
                      whiteSpace: "pre-wrap"
                    }}
                  >
                    {line.content}
                  </div>
                ))}
                
                {/* Input prompt */}
                {waitingForInput && (
                  <form onSubmit={handleInputSubmit} style={{ display: "flex", alignItems: "center" }}>
                    <span style={{ color: "var(--accent)" }}>&gt;&nbsp;</span>
                    <input
                      ref={inputRef}
                      type="text"
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      style={{
                        background: "transparent",
                        border: "none",
                        outline: "none",
                        color: "var(--text)",
                        fontFamily: "var(--mono)",
                        fontSize: "13px",
                        flex: 1,
                        padding: 0,
                        margin: 0
                      }}
                    />
                  </form>
                )}
                
                {/* Ready state (no execution yet) */}
                {terminalLines.length === 0 && !waitingForInput && !loading && !executionComplete && (
                  <div style={{ color: "var(--text-muted)", fontStyle: "italic" }}>
                    Click "Run Program" to execute
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
