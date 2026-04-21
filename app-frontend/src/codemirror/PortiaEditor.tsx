// Reusable CodeMirror Editor Component with Portia language support and error highlighting
import { useRef, useEffect, useMemo } from "react";
import { EditorSelection, EditorState, Compartment } from "@codemirror/state";
import type { Extension } from "@codemirror/state";
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter } from "@codemirror/view";
import type { KeyBinding } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap, indentLess, indentMore } from "@codemirror/commands";
import { bracketMatching, indentOnInput, foldGutter, foldKeymap } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import { lintGutter, setDiagnostics } from "@codemirror/lint";
import type { Diagnostic } from "@codemirror/lint";
import { PORTIA_INDENT, portiaIndentation, portiaLanguage } from "./portiaLanguage";
import { getCodeMirrorTheme } from "./themes";

export interface EditorError {
  line: number;
  column: number;
  message: string;
  endLine?: number;
  endColumn?: number;
  token_length?: number;
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
const readOnlyCompartment = new Compartment();

function visualColumn(text: string, tabSize: number): number {
  let column = 0;

  for (const ch of text) {
    column += ch === "\t" ? tabSize - (column % tabSize) : 1;
  }

  return column;
}

function lastCodeCharacter(text: string): string | null {
  let stringQuote: string | null = null;
  let lastChar: string | null = null;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];

    if (stringQuote) {
      if (ch === "\\") {
        i++;
      } else if (ch === stringQuote) {
        stringQuote = null;
      }
      continue;
    }

    if (ch === "/" && next === "/") break;
    if (ch === "/" && next === "*") {
      i++;
      while (i + 1 < text.length && !(text[i] === "*" && text[i + 1] === "/")) {
        i++;
      }
      i++;
      continue;
    }

    if (ch === '"' || ch === "'") {
      stringQuote = ch;
      continue;
    }

    if (!/\s/.test(ch)) {
      lastChar = ch;
    }
  }

  return lastChar;
}

function insertSoftTab(view: EditorView): boolean {
  const { state } = view;

  if (state.readOnly) return false;
  if (state.selection.ranges.some((range) => !range.empty)) {
    return indentMore(view);
  }

  const changes = state.changeByRange((range) => {
    const line = state.doc.lineAt(range.from);
    const column = visualColumn(line.text.slice(0, range.from - line.from), state.tabSize);
    const spaces = PORTIA_INDENT.length - (column % PORTIA_INDENT.length) || PORTIA_INDENT.length;
    const insert = " ".repeat(spaces);

    return {
      changes: { from: range.from, insert },
      range: EditorSelection.cursor(range.from + insert.length),
    };
  });

  view.dispatch(state.update(changes, { scrollIntoView: true, userEvent: "input.indent" }));
  return true;
}

function insertPortiaNewline(view: EditorView): boolean {
  const { state } = view;

  if (state.readOnly) return false;

  const changes = state.changeByRange((range) => {
    const fromLine = state.doc.lineAt(range.from);
    const toLine = state.doc.lineAt(range.to);
    const beforeCursor = fromLine.text.slice(0, range.from - fromLine.from);
    const afterCursor = toLine.text.slice(range.to - toLine.from);
    const currentIndent = fromLine.text.match(/^\s*/)?.[0] ?? "";
    const lastChar = lastCodeCharacter(beforeCursor);
    const opensBlock = lastChar === "{" || lastChar === "[" || lastChar === "(";
    const closesBlock = /^\s*(?:}|]|\))/.test(afterCursor);
    const nextIndent = opensBlock ? `${currentIndent}${PORTIA_INDENT}` : currentIndent;
    const insert = opensBlock && closesBlock
      ? `\n${nextIndent}\n${currentIndent}`
      : `\n${nextIndent}`;

    return {
      changes: { from: range.from, to: range.to, insert },
      range: EditorSelection.cursor(range.from + 1 + nextIndent.length),
    };
  });

  view.dispatch(state.update(changes, { scrollIntoView: true, userEvent: "input" }));
  return true;
}

const portiaKeymap: KeyBinding[] = [
  {
    key: "Tab",
    run: insertSoftTab,
    shift: indentLess,
    preventDefault: true,
  },
  {
    key: "Enter",
    run: insertPortiaNewline,
    preventDefault: true,
  },
];

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
    if (error.token_length && error.token_length > 0) {
      // Use explicit token_length when provided
      to = Math.min(from + error.token_length, lineInfo.to);
    } else if (error.endLine && error.endColumn) {
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
    EditorState.tabSize.of(PORTIA_INDENT.length),
    portiaIndentation,
    indentOnInput(),
    bracketMatching(),
    closeBrackets(),
    lintGutter(),
    portiaLanguage,
    keymap.of([
      ...portiaKeymap,
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
    
    const state = EditorState.create({
      doc: value,
      extensions: [
        baseExtensions,
        themeCompartment.of(getCodeMirrorTheme(theme)),
        readOnlyCompartment.of(EditorState.readOnly.of(readOnly)),
      ],
    });
    
    const view = new EditorView({
      state,
      parent: containerRef.current,
    });
    
    viewRef.current = view;
    
    // Set initial diagnostics if errors exist
    if (errorsRef.current.length > 0) {
      const diagnostics = createDiagnostics(errorsRef.current, view.state.doc);
      view.dispatch(setDiagnostics(view.state, diagnostics));
    }
    
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
    
    // Directly set diagnostics instead of relying on linter re-run
    // This is more reliable and immediate
    const diagnostics = createDiagnostics(errorsRef.current, view.state.doc);
    view.dispatch(setDiagnostics(view.state, diagnostics));
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
