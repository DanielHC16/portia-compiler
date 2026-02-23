// src/components/ViewSwitcher.tsx
import { useState, useEffect } from "react";
import LexerPanel from "./LexerPanel";
import ParserPanel from "./ParserPanel";
import SemanticPanel from "./SemanticPanel";
import type { Token, LexError } from "../api";

export default function ViewSwitcher() {
  const [view, setView] = useState<"lexical" | "syntax" | "semantics">("lexical");
  // Load theme from localStorage or default to dark
  const [theme, setTheme] = useState<"dark" | "light">(() => {
    const saved = localStorage.getItem("portia-theme");
    if (saved === "light" || saved === "dark") {
      return saved;
    }
    return "dark";
  });
  
  // Shared state across all panels
  const [sharedCode, setSharedCode] = useState<string>(`int main() {
    return 0;
}`);
  const [sharedTokens, setSharedTokens] = useState<Token[]>([]);
  const [sharedLexErrors, setSharedLexErrors] = useState<LexError[]>([]);

  useEffect(() => {
    // Apply theme to document root and persist to localStorage
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("portia-theme", theme);
  }, [theme]);

  // Toggle between dark and light
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
          {/* Dark/Light Theme Toggle */}
          <button 
            className="theme-toggle-btn"
            onClick={toggleTheme}
            aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          >
            {theme === "dark" ? (
              /* Sun icon for switching to light */
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="5" />
                <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
              </svg>
            ) : (
              /* Moon icon for switching to dark */
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
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
          theme={theme}
        />
      </div>
      <div style={{ display: view === "syntax" ? "block" : "none", height: "100%" }}>
        <ParserPanel 
          sharedCode={sharedCode}
          setSharedCode={setSharedCode}
          sharedTokens={sharedTokens}
          sharedLexErrors={sharedLexErrors}
          theme={theme}
        />
      </div>
      <div style={{ display: view === "semantics" ? "block" : "none", height: "100%" }}>
        <SemanticPanel 
          sharedCode={sharedCode}
          setSharedCode={setSharedCode}
          sharedTokens={sharedTokens}
          sharedLexErrors={sharedLexErrors}
          theme={theme}
        />
      </div>
    </div>
  );
}
