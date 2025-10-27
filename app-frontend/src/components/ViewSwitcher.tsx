// src/components/ViewSwitcher.tsx
import { useState } from "react";
import LexerPanel from "./LexerPanel";
import ParserTBA from "./ParserTBA";
import SemanticTBA from "./SemanticTBA";

export default function ViewSwitcher() {
  const [view, setView] = useState<"lexical" | "syntax" | "semantics">("lexical");

  return (
    <div className="app-shell">
      <div className="header">
        <div className="brand">PORTIA</div>

        <div className="view-switch" role="tablist" aria-label="View switcher">
          <button className={view === "lexical" ? "active" : ""} onClick={() => setView("lexical")}>Lexical</button>
          <button className={view === "syntax" ? "active" : ""} onClick={() => setView("syntax")}>Syntax</button>
          <button className={view === "semantics" ? "active" : ""} onClick={() => setView("semantics")}>Semantics</button>
        </div>

        <div className="controls">
          <div className="small">Local dev</div>
        </div>
      </div>

      {view === "lexical" && <LexerPanel />}
      {view === "syntax" && <ParserTBA />}
      {view === "semantics" && <SemanticTBA />}
    </div>
  );
}
