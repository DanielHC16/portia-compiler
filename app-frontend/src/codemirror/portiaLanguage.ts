// CodeMirror Portia Language Support
import { StreamLanguage } from "@codemirror/language";

// Simple mode definition for Portia language
const portiaMode = StreamLanguage.define({
  name: "portia",
  startState: () => ({
    inString: false,
    stringQuote: null as string | null,
    inComment: false,
    inBlockComment: false,
  }),
  token: (stream, state) => {
    // Multiline string continuation. Handle this before the normal
    // whitespace path so continuation lines stay visually inside the string.
    if (state.inString && state.stringQuote === '"') {
      if (stream.eatSpace()) return "string";

      while (!stream.eol()) {
        const ch = stream.next();
        if (ch === '"') {
          state.inString = false;
          state.stringQuote = null;
          break;
        }
        if (ch === "\\") stream.next();
      }
      return "string";
    }

    // Skip whitespace
    if (stream.eatSpace()) return null;

    // Block comments /* */
    if (state.inBlockComment) {
      if (stream.match("*/")) {
        state.inBlockComment = false;
        return "comment";
      }
      stream.next();
      return "comment";
    }

    // Start block comment
    if (stream.match("/*")) {
      state.inBlockComment = true;
      return "comment";
    }

    // Line comments //
    if (stream.match("//")) {
      stream.skipToEnd();
      return "comment";
    }

    // Strings with double quotes
    if (stream.match('"')) {
      state.inString = true;
      state.stringQuote = '"';
      while (!stream.eol()) {
        const ch = stream.next();
        if (ch === '"') {
          state.inString = false;
          state.stringQuote = null;
          break;
        }
        if (ch === '\\') stream.next(); // escape
      }
      return "string";
    }

    // Strings with single quotes (char)
    if (stream.match("'")) {
      while (!stream.eol()) {
        const ch = stream.next();
        if (ch === "'") break;
        if (ch === '\\') stream.next(); // escape
      }
      return "string";
    }

    // Numbers (including floats)
    if (stream.match(/^-?\d+\.?\d*/)) {
      return "number";
    }

    // Keywords and identifiers
    if (stream.match(/^[a-zA-Z_][a-zA-Z0-9_]*/)) {
      const word = stream.current();
      
      // Portia keywords
      const keywords = [
        "int", "float", "double", "char", "string", "bool", "void",
        "if", "else", "while", "for", "do", "return", "break", "continue",
        "switch", "case", "default", "struct", "enum", "const", "static",
        "public", "private", "class", "new", "delete", "nullptr", "null",
        "try", "catch", "throw", "finally", "import", "export", "module",
        "function", "fn", "let", "var", "const", "type", "interface",
        "async", "await", "yield", "from",
      ];
      
      // Boolean literals
      const booleans = ["true", "false", "TRUE", "FALSE"];
      
      // Built-in functions
      const builtins = ["print", "println", "read", "readln", "sizeof", "typeof"];
      
      if (keywords.includes(word)) return "keyword";
      if (booleans.includes(word)) return "atom";
      if (builtins.includes(word)) return "builtin";
      
      return "variable";
    }

    // Operators
    if (stream.match(/^[+\-*/%=<>!&|^~?:]+/)) {
      return "operator";
    }

    // Brackets and delimiters
    if (stream.match(/^[()[\]{}.,;]/)) {
      return "punctuation";
    }

    // Move forward if nothing matched
    stream.next();
    return null;
  },
  languageData: {
    commentTokens: { line: "//", block: { open: "/*", close: "*/" } },
  },
});

export const portiaLanguage = portiaMode;
export default portiaLanguage;
