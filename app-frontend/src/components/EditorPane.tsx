import React, { useRef, useEffect } from "react";
import Editor from "@monaco-editor/react";
import type { BeforeMount, OnMount } from "@monaco-editor/react";
import type * as Monaco from "monaco-editor";
import { registerPortiaLanguage } from "../monacoPortia";
import type { LexError } from "../types";

interface EditorPaneProps {
  onCodeChange?: (code: string) => void;
  errors?: LexError[];
}

export const EditorPane: React.FC<EditorPaneProps> = ({ onCodeChange, errors = [] }) => {
  const editorRef = useRef<Monaco.editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<typeof Monaco | null>(null);
  const timer = useRef<number | null>(null);

  const setLexerDiagnostics = (errs: LexError[]) => {
    const model = editorRef.current?.getModel();
    if (!model || !monacoRef.current) return;
    const markers: Monaco.editor.IMarkerData[] = errs.map((err) => ({
      severity: monacoRef.current!.MarkerSeverity.Error,
      message: err.message,
      startLineNumber: err.line,
      startColumn: err.column,
      endLineNumber: err.line,
      endColumn: err.column + 1,
    }));
    monacoRef.current!.editor.setModelMarkers(model, "portia", markers);
  };

  // Update diagnostics whenever errors prop changes
  useEffect(() => {
    setLexerDiagnostics(errors);
  }, [errors]);

  const beforeMount: BeforeMount = (monaco) => {
    monacoRef.current = monaco;
    registerPortiaLanguage(monaco);
  };

  const onMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    monaco.editor.setTheme("portia-hc-dark");
    const model = editor.getModel();
    if (model) monaco.editor.setModelLanguage(model, "portia");
  };

  const onChange = (value?: string) => {
    if (timer.current) window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      const code = value ?? "";
      onCodeChange?.(code);
    }, 20); // Reduced from 250ms to 20ms for near-instant response
  };

  return (
    <div style={{ height: "80vh", border: "1px solid #444" }}>
      <Editor
        height="100%"
        defaultLanguage="portia"
        theme="portia-hc-dark"
        defaultValue={`// PORTIA demo`}
        beforeMount={beforeMount}
        onMount={onMount}
        onChange={onChange}
        options={{
          fontSize: 14,
          minimap: { enabled: false },
          automaticLayout: true,
          wordWrap: "on",
        }}
      />
    </div>
  );
};
