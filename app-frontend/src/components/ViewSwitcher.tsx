// src/components/ViewSwitcher.tsx
import { useState, useEffect, useRef } from "react";
import LexerPanel from "./LexerPanel";
import ParserPanel from "./ParserPanel";
import SemanticPanel from "./SemanticPanel";
import ICGPanel from "./ICGPanel";
import type { Token, LexError } from "../api";

export default function ViewSwitcher() {
  const [view, setView] = useState<"lexical" | "syntax" | "semantics" | "icg">("lexical");
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
  
  // File input ref for loading files
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Apply theme to document root and persist to localStorage
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("portia-theme", theme);
  }, [theme]);

  // Toggle between dark and light
  const toggleTheme = () => {
    setTheme(prev => prev === "dark" ? "light" : "dark");
  };

  // Save code to a .portia file
  const handleSave = () => {
    const blob = new Blob([sharedCode], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    // Generate a default filename with timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    link.download = `program-${timestamp}.portia`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Trigger file input for loading
  const handleLoadClick = () => {
    fileInputRef.current?.click();
  };

  // Load code from a .portia file
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result;
      if (typeof content === "string") {
        // Normalize line endings
        const normalized = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
        setSharedCode(normalized);
        // Reset tokens and errors when loading new file
        setSharedTokens([]);
        setSharedLexErrors([]);
      }
    };
    reader.readAsText(file);
    // Reset input so same file can be loaded again
    e.target.value = "";
  };

  return (
    <div className="app-shell">
      <div className="header">
        <div className="brand">
          PORTIA
        </div>

        <div className="view-switch" role="tablist" aria-label="View switcher">
          <div className="view-switch-slider" style={{
            left: view === "lexical" ? "4px" : view === "syntax" ? "calc(25% + 2px)" : view === "semantics" ? "calc(50%)" : "calc(75% - 2px)"
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
          <button 
            className={view === "icg" ? "active" : ""} 
            onClick={() => setView("icg")}
            role="tab"
            aria-selected={view === "icg"}
          >
            ICG
          </button>
        </div>

        <div className="controls">
          {/* Hidden file input for loading */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".portia,.txt"
            style={{ display: "none" }}
          />
          
          {/* Save Button */}
          <button 
            className="theme-toggle-btn"
            onClick={handleSave}
            aria-label="Save code as .portia file"
            title="Save code as .portia file"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
              <polyline points="17 21 17 13 7 13 7 21" />
              <polyline points="7 3 7 8 15 8" />
            </svg>
          </button>
          
          {/* Load Button */}
          <button 
            className="theme-toggle-btn"
            onClick={handleLoadClick}
            aria-label="Load .portia file"
            title="Load .portia file"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
              <line x1="12" y1="11" x2="12" y2="17" />
              <polyline points="9 14 12 11 15 14" />
            </svg>
          </button>
          
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
      <div style={{ display: view === "icg" ? "block" : "none", height: "100%" }}>
        <ICGPanel 
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
