import React, { useRef } from "react";
import Editor from "@monaco-editor/react";
import type { BeforeMount, OnMount } from "@monaco-editor/react";
import type * as Monaco from "monaco-editor";
import { registerPortiaLanguage } from "../monacoPortia";

export const EditorPane: React.FC<{ onCodeChange?: (code: string) => void }> = ({ onCodeChange }) => {
  const editorRef = useRef<Monaco.editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<typeof Monaco | null>(null);
  const timer = useRef<number | null>(null);

  const setLexerDiagnostics = (errors: any[]) => {
    const model = editorRef.current?.getModel();
    if (!model || !monacoRef.current) return;
    const markers: Monaco.editor.IMarkerData[] = errors.map((err: any) => ({
      severity: monacoRef.current!.MarkerSeverity.Error,
      message: err.message,
      startLineNumber: err.line,
      startColumn: err.column,
      endLineNumber: err.line,
      endColumn: err.column + 1,
    }));
    monacoRef.current!.editor.setModelMarkers(model, "portia", markers);
  };

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

      fetch("http://localhost:8000/lex", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      })
        .then((res) => res.json())
        .then(({ tokens, errors }) => {
          setLexerDiagnostics(errors);
        })
        .catch((err) => console.error("Lexer request failed:", err));
    }, 250);
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
