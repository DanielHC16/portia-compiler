// CodeMirror themes - Portia Dark (synthwave-inspired with purple) and Portia Light
import { EditorView } from "@codemirror/view";
import type { Extension } from "@codemirror/state";
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags } from "@lezer/highlight";

// ===================== PORTIA DARK THEME (Synthwave with Purple) =====================
const portiaDarkColors = {
  bg: "#0f0a1a",
  bgEditor: "#12091f",
  text: "#e8e0f0",
  accent: "#a855f7",
  comment: "#6b6b9a",
  keyword: "#c084fc",
  string: "#4ade80",
  number: "#f0abfc",
  variable: "#67e8f9",
  builtin: "#fbbf24",
  operator: "#c084fc",
  punctuation: "#9ca3af",
  selection: "rgba(168, 85, 247, 0.35)",
  cursor: "#a855f7",
  lineHighlight: "rgba(168, 85, 247, 0.1)",
};

const portiaDarkHighlight = HighlightStyle.define([
  { tag: tags.keyword, color: portiaDarkColors.keyword, fontWeight: "600" },
  { tag: tags.comment, color: portiaDarkColors.comment, fontStyle: "italic" },
  { tag: tags.string, color: portiaDarkColors.string },
  { tag: tags.number, color: portiaDarkColors.number },
  { tag: tags.variableName, color: portiaDarkColors.variable },
  { tag: tags.function(tags.variableName), color: portiaDarkColors.builtin },
  { tag: tags.bool, color: portiaDarkColors.number },
  { tag: tags.atom, color: portiaDarkColors.number },
  { tag: tags.operator, color: portiaDarkColors.operator },
  { tag: tags.punctuation, color: portiaDarkColors.punctuation },
  { tag: tags.bracket, color: portiaDarkColors.punctuation },
  { tag: tags.typeName, color: portiaDarkColors.accent },
  { tag: tags.definition(tags.variableName), color: portiaDarkColors.variable },
]);

const portiaDarkTheme = EditorView.theme({
  "&": {
    backgroundColor: portiaDarkColors.bgEditor,
    color: portiaDarkColors.text,
  },
  ".cm-content": {
    caretColor: portiaDarkColors.cursor,
    fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
    fontSize: "14px",
    lineHeight: "1.6",
    padding: "12px 0",
    fontVariantLigatures: "none",
  },
  ".cm-cursor, .cm-dropCursor": {
    borderLeftColor: portiaDarkColors.cursor,
    borderLeftWidth: "2px",
  },
  "&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection": {
    backgroundColor: portiaDarkColors.selection,
  },
  ".cm-activeLine": {
    backgroundColor: portiaDarkColors.lineHighlight,
  },
  ".cm-gutters": {
    backgroundColor: portiaDarkColors.bgEditor,
    color: portiaDarkColors.comment,
    border: "none",
  },
  ".cm-activeLineGutter": {
    backgroundColor: portiaDarkColors.lineHighlight,
    color: portiaDarkColors.accent,
  },
  ".cm-lineNumbers .cm-gutterElement": {
    padding: "0 12px 0 8px",
  },
  ".cm-scroller": {
    overflow: "auto",
  },
}, { dark: true });

export const portiaDark: Extension = [portiaDarkTheme, syntaxHighlighting(portiaDarkHighlight)];

// ===================== PORTIA LIGHT THEME =====================
const portiaLightColors = {
  bg: "#faf8ff",
  bgEditor: "#ffffff",
  text: "#1a0f2e",
  accent: "#7c3aed",
  comment: "#6b7280",
  keyword: "#7c3aed",
  string: "#059669",
  number: "#9333ea",
  variable: "#0284c7",
  builtin: "#d97706",
  operator: "#7c3aed",
  punctuation: "#6b7280",
  selection: "rgba(124, 58, 237, 0.2)",
  cursor: "#7c3aed",
  lineHighlight: "rgba(124, 58, 237, 0.06)",
};

const portiaLightHighlight = HighlightStyle.define([
  { tag: tags.keyword, color: portiaLightColors.keyword, fontWeight: "600" },
  { tag: tags.comment, color: portiaLightColors.comment, fontStyle: "italic" },
  { tag: tags.string, color: portiaLightColors.string },
  { tag: tags.number, color: portiaLightColors.number },
  { tag: tags.variableName, color: portiaLightColors.variable },
  { tag: tags.function(tags.variableName), color: portiaLightColors.builtin },
  { tag: tags.bool, color: portiaLightColors.number },
  { tag: tags.atom, color: portiaLightColors.number },
  { tag: tags.operator, color: portiaLightColors.operator },
  { tag: tags.punctuation, color: portiaLightColors.punctuation },
  { tag: tags.bracket, color: portiaLightColors.punctuation },
  { tag: tags.typeName, color: portiaLightColors.accent },
  { tag: tags.definition(tags.variableName), color: portiaLightColors.variable },
]);

const portiaLightTheme = EditorView.theme({
  "&": {
    backgroundColor: portiaLightColors.bgEditor,
    color: portiaLightColors.text,
  },
  ".cm-content": {
    caretColor: portiaLightColors.cursor,
    fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
    fontSize: "14px",
    lineHeight: "1.6",
    padding: "12px 0",
    fontVariantLigatures: "none",
  },
  ".cm-cursor, .cm-dropCursor": {
    borderLeftColor: portiaLightColors.cursor,
    borderLeftWidth: "2px",
  },
  "&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection": {
    backgroundColor: portiaLightColors.selection,
  },
  ".cm-activeLine": {
    backgroundColor: portiaLightColors.lineHighlight,
  },
  ".cm-gutters": {
    backgroundColor: portiaLightColors.bgEditor,
    color: portiaLightColors.comment,
    border: "none",
    borderRight: "1px solid rgba(124, 58, 237, 0.15)",
  },
  ".cm-activeLineGutter": {
    backgroundColor: portiaLightColors.lineHighlight,
    color: portiaLightColors.accent,
  },
  ".cm-lineNumbers .cm-gutterElement": {
    padding: "0 12px 0 8px",
  },
  ".cm-scroller": {
    overflow: "auto",
  },
}, { dark: false });

export const portiaLight: Extension = [portiaLightTheme, syntaxHighlighting(portiaLightHighlight)];

// Return the CodeMirror extension bundle for the active app theme.
export function getCodeMirrorTheme(theme: "light" | "dark"): Extension {
  return theme === "light" ? portiaLight : portiaDark;
}
