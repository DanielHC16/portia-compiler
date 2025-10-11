import { useState, useEffect } from "react";
import "./components/Layout.css";
import { EditorPane } from "./components/EditorPane";
import { TokenTable } from "./components/TokenTable";
import { ErrorsPanel } from "./components/ErrorsPanel";
import { lexCode } from "./api";
import type { Token, LexError } from "./types";
import { registerPortiaLanguage } from "./monacoPortia";

export default function App() {
  const [tokens, setTokens] = useState<Token[]>([]);
  const [errors, setErrors] = useState<LexError[]>([]);

  // Register the custom PORTIA language in Monaco once on mount
  useEffect(() => {
    registerPortiaLanguage();
  }, []);

  async function onCodeChange(code: string) {
    try {
      const res = await lexCode(code);
      setTokens(res.tokens);
      setErrors(res.errors);
    } catch (e) {
      console.error("Error calling backend:", e);
    }
  }

  return (
    <div className="app">
      <div>
        <EditorPane onCodeChange={onCodeChange} />
      </div>
      <div>
        <TokenTable tokens={tokens} />
        <ErrorsPanel errors={errors} />
      </div>
    </div>
  );
}
