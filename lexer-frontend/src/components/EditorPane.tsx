import Editor from "@monaco-editor/react";
import React, { useRef } from "react";

export const EditorPane: React.FC<{ onCodeChange: (code: string) => void }> = ({
  onCodeChange,
}) => {
  const timer = useRef<number | null>(null);

  const handleChange = (value?: string) => {
    if (timer.current) window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => onCodeChange(value ?? ""), 250);
  };

  return (
    <Editor
      height="60vh"
      defaultLanguage="plaintext"
      defaultValue="// Type PORTIA code here"
      onChange={handleChange}
      theme="vs-dark"
      options={{
        fontSize: 14,
        minimap: { enabled: false },
        smoothScrolling: true,
        wordWrap: "on",
        scrollBeyondLastLine: false,
      }}
    />
  );
};
