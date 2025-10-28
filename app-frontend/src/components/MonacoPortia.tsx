// src/components/MonacoPortia.tsx
import { useEffect, useRef, useState } from "react";
import Editor, { type OnMount } from "@monaco-editor/react";
import type { Token } from "../api";

/**
 * MonacoPortia
 * - Readonly Monaco editor used for reliable syntax highlighting driven by token ranges.
 * - Accepts tokens that either contain numeric start/end offsets (0-based, end exclusive)
 *   or line/column (1-based) + lexeme. Decorations are applied deterministically and replaced each update.
 *
 * Props:
 *  - value: source string
 *  - tokens: array of Token with optional start/end
 *  - language: monaco language id (default "cpp")
 *  - theme: monaco theme name (default "vs-dark")
 */
type Props = {
  value: string;
  tokens: (Token & { start?: number; end?: number })[];
  language?: string;
  theme?: string;
  className?: string;
};

export default function MonacoPortia({ value, tokens, language = "cpp", theme = "vs-dark", className }: Props) {
  const editorRef = useRef<any | null>(null);
  const monacoRef = useRef<any | null>(null);
  const [decorations, setDecorations] = useState<string[]>([]);

  const onMount: OnMount = (monacoEditor, monaco) => {
    editorRef.current = monacoEditor;
    monacoRef.current = monaco;

    // configure editor options
    monacoEditor.updateOptions({
      readOnly: true,
      minimap: { enabled: false },
      lineNumbers: "on",
      glyphMargin: false,
      folding: false,
      renderLineHighlight: "none",
      scrollBeyondLastLine: false,
    });

    // ensure correct initial size/layout
    setTimeout(() => monacoEditor.layout(), 0);
  };

  // Utility: compute lineStarts for fallback
  function computeLineStarts(src: string) {
    const lineStarts: number[] = [0];
    for (let i = 0; i < src.length; i++) if (src[i] === "\n") lineStarts.push(i + 1);
    return lineStarts;
  }

  // Convert token offsets (start,end) to {startLine,startCol,endLine,endCol} for Monaco range
  function offsetsToRange(src: string, start: number, end: number) {
    const lineStarts = computeLineStarts(src);
    // clamp
    const s = Math.max(0, Math.min(src.length, start));
    const e = Math.max(s, Math.min(src.length, end));
    // find line for position
    function posToLineCol(pos: number) {
      // binary search lineStarts
      let lo = 0, hi = lineStarts.length - 1;
      while (lo <= hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (lineStarts[mid] <= pos) lo = mid + 1;
        else hi = mid - 1;
      }
      const lineIndex = Math.max(0, lo - 1);
      const line = lineIndex + 1;
      const col = pos - lineStarts[lineIndex] + 1;
      return { line, col };
    }
    const sLc = posToLineCol(s);
    const eLc = posToLineCol(e);
    return { startLine: sLc.line, startCol: sLc.col, endLine: eLc.line, endCol: eLc.col };
  }

  // Fallback: compute start/end from token.line/token.column + lexeme length
  function lineColToRange(src: string, line: number, column: number, length: number) {
    const lineStarts = computeLineStarts(src);
    const l = Math.max(1, Math.min(lineStarts.length, line));
    const start = lineStarts[l - 1] + Math.max(0, column - 1);
    const end = start + length;
    return offsetsToRange(src, start, end);
  }

  // Map token type to Monaco decoration class (CSS class names below)
  function tokenToClass(type?: string) {
    if (!type) return undefined;
    
    // Keywords - all PORTIA reserved words
    const keywords = [
      "BREAK", "BOOL", "CONST", "CASE", "CHAR", "DEFAULT", "DOUBLE", "DO",
      "ELSE", "FALSE", "FLOAT", "FUNC", "FOR", "GLOBAL", "INT", "IF",
      "LOCAL", "LONG", "MAIN", "RETURN", "STRING", "SWITCH", "THREAD",
      "THREADLN", "TRAP", "TRUE", "USING", "VOID", "VAR", "WHILE", "WEAVE"
    ];
    if (keywords.includes(type)) return "mp-keyword";
    
    if (type === "INT_LIT" || type === "FLOAT_LIT" || /_INTEGER$/.test(type)) return "mp-number";
    if (type === "STRING_LIT") return "mp-string";
    if (type === "CHAR_LIT") return "mp-char";
    if (type === "COMMENT" || type === "ML_COMMENT" || /COMMENT$/.test(type)) return "mp-comment";
    if (type === "IDENTIFIER") return "mp-identifier";
    if (type === "DELIMITER" || /SEMI|COMMA|DELIM|DELIMITER/.test(type)) return "mp-delim";
    if (type === "OPERATOR" || /ASSIGN|OP|OPERATOR/.test(type)) return "mp-operator";
    return "mp-identifier";
  }

  // Recompute decorations on tokens or value change
  useEffect(() => {
    const monaco = monacoRef.current;
    const editor = editorRef.current;
    if (!monaco || !editor) return;

    // Normalize tokens to ranges using offsets when available or fallback
    const ranges: { range: any; options: any }[] = [];
    for (const t of tokens) {
      try {
        let r;
        if (typeof t.start === "number" && typeof t.end === "number") {
          const rr = offsetsToRange(value, Math.floor(t.start), Math.floor(t.end));
          r = new monaco.Range(rr.startLine, rr.startCol, rr.endLine, rr.endCol);
        } else {
          // fallback using token.line/token.column + lexeme length
          const lexLen = t.lexeme ? t.lexeme.length : 0;
          const rr = lineColToRange(value, t.line || 1, t.column || 1, lexLen);
          r = new monaco.Range(rr.startLine, rr.startCol, rr.endLine, rr.endCol);
        }
        if (r && r.isEmpty() === false) {
          const cls = tokenToClass(t.type);
          ranges.push({
            range: r,
            options: {
              isWholeLine: false,
              className: cls,
            },
          });
        }
      } catch {
        // skip tokens that fail range conversion
      }
    }

    // Apply decorations; clear previous
    const newIds = editor.deltaDecorations(decorations, ranges.map(r => ({ range: r.range, options: r.options })));
    setDecorations(newIds);
    // cleanup on unmount handled implicitly
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tokens, value, monacoRef.current, editorRef.current]);

  // keep editor content in sync (monaco React handles value prop)
  return (
    <div className={className} style={{ height: "100%", width: "100%" }}>
      <Editor
        height="100%"
        defaultLanguage={language}
        value={value}
        theme={theme}
        onMount={onMount}
        options={{ readOnly: true, minimap: { enabled: false }, lineDecorationsWidth: 0 }}
      />
    </div>
  );
}
