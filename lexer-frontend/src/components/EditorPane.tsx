import Editor from "@monaco-editor/react";
import React, { useRef } from "react";
import { registerPortiaLanguage } from "../monacoPortia";

export const EditorPane: React.FC<{ onCodeChange: (code: string) => void }> = ({
  onCodeChange,
}) => {
  const timer = useRef<number | null>(null);

  const handleChange = (value?: string) => {
    if (timer.current) {
      window.clearTimeout(timer.current);
    }
    timer.current = window.setTimeout(() => onCodeChange(value ?? ""), 250);
  };

  const handleEditorWillMount = () => {
    // Register the custom PORTIA language before the editor mounts
    registerPortiaLanguage();
  };

  return (
    <Editor
      height="60vh"
      language="portia"   
      defaultValue={`// Type PORTIA code here\nlocal var int x = 10;`}
      onChange={handleChange}
      theme="hc-black" // vs-dark, vs-light, hc-black, or custom themes TODO: Enable switching
      beforeMount={handleEditorWillMount}
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
