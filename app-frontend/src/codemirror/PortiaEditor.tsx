// Reusable CodeMirror Editor Component with Portia language support and error highlighting
import { useRef, useEffect, useMemo } from "react";
import { EditorState, Compartment } from "@codemirror/state";
import type { Extension } from "@codemirror/state";
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { bracketMatching, indentOnInput, foldGutter, foldKeymap } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import { linter, lintGutter, forceLinting } from "@codemirror/lint";
import type { Diagnostic } from "@codemirror/lint";
import { portiaLanguage } from "./portiaLanguage";
import { getCodeMirrorTheme } from "./themes";

export interface EditorError {
  line: number;
  column: number;
  message: string;
  endLine?: number;
  endColumn?: number;
  errorType?: "lexer" | "parser" | "semantic";
}

interface PortiaEditorProps {
  value: string;
  onChange: (value: string) => void;
  theme: "light" | "dark";
  errors?: EditorError[];
  readOnly?: boolean;
  className?: string;
}

// Compartments for dynamic reconfiguration (preserves cursor position)
const themeCompartment = new Compartment();
const lintCompartment = new Compartment();
const readOnlyCompartment = new Compartment();

// Create error diagnostics from errors array
function createDiagnostics(errors: EditorError[], doc: { lines: number; line: (n: number) => { from: number; to: number; length: number }; sliceString: (from: number, to: number) => string; length: number }): Diagnostic[] {
  if (!errors || errors.length === 0) return [];
  
  const diagnostics: Diagnostic[] = [];
  
  for (const error of errors) {
    // Skip errors with invalid line numbers
    if (error.line <= 0) continue;
    
    // Convert 1-based line/column to positions
    const line = Math.max(1, Math.min(error.line, doc.lines));
    const lineInfo = doc.line(line);
    
    // Calculate position - column is 1-based
    const col = Math.max(0, Math.min((error.column || 1) - 1, lineInfo.length));
    const from = lineInfo.from + col;
    
    // End position - highlight at least one character or until end column
    let to: number;
    if (error.endLine && error.endColumn) {
      const endLine = Math.max(1, Math.min(error.endLine, doc.lines));
      const endLineInfo = doc.line(endLine);
      const endCol = Math.max(0, Math.min(error.endColumn - 1, endLineInfo.length));
      to = endLineInfo.from + endCol;
    } else {
      // Try to extend to end of word/token for better visibility
      const restOfLine = doc.sliceString(from, lineInfo.to);
      const match = restOfLine.match(/^[\w]+/);
      if (match && match[0].length > 0) {
        to = from + match[0].length;
      } else {
        // Highlight at least one character or until end of line
        to = Math.min(from + 1, lineInfo.to);
      }
    }
    
    // Ensure from < to and valid range
    if (from >= to) {
      to = Math.min(from + 1, doc.length);
    }
    
    // Add custom CSS class based on error type
    const errorClass = error.errorType ? `cm-error-${error.errorType}` : "cm-error-semantic";
    
    diagnostics.push({
      from,
      to,
      severity: "error",
      message: error.message,
      source: "portia",
      renderMessage: () => {
        const div = document.createElement("div");
        div.className = errorClass;
        div.textContent = error.message;
        return div;
      },
    });
  }
  
  return diagnostics;
}

export default function PortiaEditor({
  value,
  onChange,
  theme,
  errors = [],
  readOnly = false,
  className = "",
}: PortiaEditorProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<EditorView | null>(null);
  const isUpdatingFromProps = useRef(false);
  const errorsRef = useRef<EditorError[]>(errors);
  
  // Keep errors ref updated
  errorsRef.current = errors;
  
  // Memoize errors to prevent unnecessary updates
  const errorKey = useMemo(() => JSON.stringify(errors), [errors]);
  
  // Base extensions that don't change
  const baseExtensions = useMemo((): Extension[] => [
    lineNumbers(),
    highlightActiveLine(),
    highlightActiveLineGutter(),
    history(),
    foldGutter(),
    indentOnInput(),
    bracketMatching(),
    closeBrackets(),
    lintGutter(),
    portiaLanguage,
    keymap.of([
      ...defaultKeymap,
      ...historyKeymap,
      ...foldKeymap,
      ...closeBracketsKeymap,
    ]),
    EditorView.updateListener.of((update) => {
      if (update.docChanged && !isUpdatingFromProps.current) {
        const newValue = update.state.doc.toString();
        onChange(newValue);
      }
    }),
  ], [onChange]);
  
  // Initialize editor on mount
  useEffect(() => {
    if (!containerRef.current) return;
    
    // Create linter that reads from ref (always current errors)
    const lintExtension = linter((view) => {
      return createDiagnostics(errorsRef.current, view.state.doc);
    }, { delay: 0 });
    
    const state = EditorState.create({
      doc: value,
      extensions: [
        baseExtensions,
        themeCompartment.of(getCodeMirrorTheme(theme)),
        lintCompartment.of(lintExtension),
        readOnlyCompartment.of(EditorState.readOnly.of(readOnly)),
      ],
    });
    
    const view = new EditorView({
      state,
      parent: containerRef.current,
    });
    
    viewRef.current = view;
    
    return () => {
      view.destroy();
      viewRef.current = null;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Mount once only
  
  // Update value from props (preserves cursor position)
  useEffect(() => {
    const view = viewRef.current;
    if (!view) return;
    
    const currentValue = view.state.doc.toString();
    if (currentValue !== value) {
      isUpdatingFromProps.current = true;
      
      // Preserve cursor/selection position
      const selection = view.state.selection;
      
      view.dispatch({
        changes: {
          from: 0,
          to: currentValue.length,
          insert: value,
        },
        // Try to maintain cursor position within bounds
        selection: {
          anchor: Math.min(selection.main.anchor, value.length),
          head: Math.min(selection.main.head, value.length),
        },
      });
      
      isUpdatingFromProps.current = false;
    }
  }, [value]);
  
  // Update theme dynamically (preserves cursor position)
  useEffect(() => {
    const view = viewRef.current;
    if (!view) return;
    
    view.dispatch({
      effects: themeCompartment.reconfigure(getCodeMirrorTheme(theme)),
    });
  }, [theme]);
  
  // Update errors/lint dynamically (preserves cursor position)
  useEffect(() => {
    const view = viewRef.current;
    if (!view) return;
    
    // Force lint refresh by reconfiguring with updated errors
    const newLintExtension = linter((v) => {
      return createDiagnostics(errorsRef.current, v.state.doc);
    }, { delay: 0 });
    
    view.dispatch({
      effects: lintCompartment.reconfigure(newLintExtension),
    });
    
    // Force the linter to re-run immediately
    forceLinting(view);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [errorKey]); // Only update when errors actually change
  
  // Update readOnly dynamically
  useEffect(() => {
    const view = viewRef.current;
    if (!view) return;
    
    view.dispatch({
      effects: readOnlyCompartment.reconfigure(EditorState.readOnly.of(readOnly)),
    });
  }, [readOnly]);
  
  return (
    <div 
      ref={containerRef} 
      className={`portia-editor ${className}`}
      style={{ 
        height: "100%", 
        width: "100%",
        overflow: "hidden",
        borderRadius: "8px",
      }}
    />
  );
}
