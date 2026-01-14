// src/components/ViewSwitcher.tsx
import { useState, useEffect } from "react";
import LexerPanel from "./LexerPanel";
import ParserTBA from "./ParserTBA";
import SemanticTBA from "./SemanticTBA";
import type { Token, LexError } from "../api";

export default function ViewSwitcher() {
  const [view, setView] = useState<"lexical" | "syntax" | "semantics">("lexical");
  const [theme, setTheme] = useState<"light" | "dark">("dark");
  
  // Shared state across all panels
  const [sharedCode, setSharedCode] = useState<string>("");
  const [sharedTokens, setSharedTokens] = useState<Token[]>([]);
  const [sharedLexErrors, setSharedLexErrors] = useState<LexError[]>([]);

  useEffect(() => {
    // Apply theme to document root
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === "dark" ? "light" : "dark");
  };

  return (
    <div className="app-shell">
      <div className="header">
        <div className="brand">
          PORTIA
        </div>

        <div className="view-switch" role="tablist" aria-label="View switcher">
          <div className="view-switch-slider" style={{
            transform: view === "lexical" ? "translateX(0%)" : view === "syntax" ? "translateX(100%)" : "translateX(200%)"
          }} />
          <button 
            className={view === "lexical" ? "active" : ""} 
            onClick={() => setView("lexical")}
            role="tab"
            aria-selected={view === "lexical"}
          >
            Lexical
          </button>
          <button 
            className={view === "syntax" ? "active" : ""} 
            onClick={() => setView("syntax")}
            role="tab"
            aria-selected={view === "syntax"}
          >
            Syntax
          </button>
          <button 
            className={view === "semantics" ? "active" : ""} 
            onClick={() => setView("semantics")}
            role="tab"
            aria-selected={view === "semantics"}
          >
            Semantics
          </button>
        </div>

        <div className="controls">
          <button 
            className="theme-toggle" 
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
            title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          >
            {theme === "dark" ? (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="5"/>
                <line x1="12" y1="1" x2="12" y2="3"/>
                <line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/>
                <line x1="21" y1="12" x2="23" y2="12"/>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
              </svg>
            ) : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Keep all panels mounted to preserve state, show/hide with display */}
      <div style={{ display: view === "lexical" ? "block" : "none", height: "100%" }}>
        <LexerPanel 
          sharedCode={sharedCode}
          setSharedCode={setSharedCode}
          setSharedTokens={setSharedTokens}
          setSharedLexErrors={setSharedLexErrors}
        />
      </div>
      <div style={{ display: view === "syntax" ? "block" : "none", height: "100%" }}>
        <ParserTBA 
          sharedCode={sharedCode}
          sharedTokens={sharedTokens}
          sharedLexErrors={sharedLexErrors}
        />
      </div>
      <div style={{ display: view === "semantics" ? "block" : "none", height: "100%" }}>
        <SemanticTBA />
      </div>
    </div>
  );
}
