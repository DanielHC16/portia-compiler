// CodeMirror Portia Language Support
import { indentService, indentUnit, StreamLanguage } from "@codemirror/language";
import type { IndentContext } from "@codemirror/language";
import type { Extension } from "@codemirror/state";

export const PORTIA_INDENT = "    ";

type IndentScanState = {
  depth: number;
  inBlockComment: boolean;
  stringQuote: string | null;
};

const openingDelimiters = new Set(["{", "[", "("]);
const closingDelimiters = new Set(["}", "]", ")"]);
const portiaKeywords = new Set([
  "bool",
  "break",
  "case",
  "char",
  "const",
  "default",
  "do",
  "double",
  "else",
  "float",
  "for",
  "func",
  "global",
  "if",
  "int",
  "local",
  "long",
  "main",
  "return",
  "string",
  "switch",
  "thread",
  "threadln",
  "trap",
  "using",
  "var",
  "void",
  "weave",
  "while",
]);
const portiaBooleans = new Set(["true", "false"]);
const portiaBuiltins = new Set(["abs", "len", "pow", "sqrt"]);

function scanIndentLine(line: string, state: IndentScanState): IndentScanState {
  let { depth, inBlockComment, stringQuote } = state;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    const next = line[i + 1];

    if (inBlockComment) {
      if (ch === "*" && next === "/") {
        inBlockComment = false;
        i++;
      }
      continue;
    }

    if (stringQuote) {
      if (ch === "\\") {
        i++;
      } else if (ch === stringQuote) {
        stringQuote = null;
      }
      continue;
    }

    if (ch === "/" && next === "/") break;
    if (ch === "/" && next === "*") {
      inBlockComment = true;
      i++;
      continue;
    }

    if (ch === '"' || ch === "'") {
      stringQuote = ch;
      continue;
    }

    if (openingDelimiters.has(ch)) {
      depth++;
    } else if (closingDelimiters.has(ch)) {
      depth = Math.max(0, depth - 1);
    }
  }

  return { depth, inBlockComment, stringQuote };
}

function lastCodeCharacter(line: string, state: IndentScanState): string | null {
  let { inBlockComment, stringQuote } = state;
  let lastChar: string | null = null;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    const next = line[i + 1];

    if (inBlockComment) {
      if (ch === "*" && next === "/") {
        inBlockComment = false;
        i++;
      }
      continue;
    }

    if (stringQuote) {
      if (ch === "\\") {
        i++;
      } else if (ch === stringQuote) {
        stringQuote = null;
      }
      continue;
    }

    if (ch === "/" && next === "/") break;
    if (ch === "/" && next === "*") {
      inBlockComment = true;
      i++;
      continue;
    }

    if (ch === '"' || ch === "'") {
      stringQuote = ch;
      continue;
    }

    if (!/\s/.test(ch)) {
      lastChar = ch;
    }
  }

  return lastChar;
}

function scanToLineStart(context: IndentContext, lineNumber: number): IndentScanState {
  let state: IndentScanState = { depth: 0, inBlockComment: false, stringQuote: null };

  for (let lineNo = 1; lineNo < lineNumber; lineNo++) {
    state = scanIndentLine(context.state.doc.line(lineNo).text, state);
  }

  return state;
}

function portiaIndent(context: IndentContext, pos: number): number | null {
  const sourceLine = context.state.doc.lineAt(pos);
  const targetLine = context.lineAt(pos, 1);
  let scanState = scanToLineStart(context, sourceLine.number);
  const beforeBreakText = context.lineAt(pos, -1).text;
  const opensNextLine = openingDelimiters.has(lastCodeCharacter(beforeBreakText, scanState) ?? "");
  const startsWithClosingDelimiter = /^\s*(?:}|]|\))/.test(targetLine.text);

  if (!opensNextLine && !startsWithClosingDelimiter) {
    return null;
  }

  if (
    context.simulatedBreak !== null &&
    context.simulatedBreak >= sourceLine.from &&
    context.simulatedBreak <= sourceLine.to
  ) {
    scanState = scanIndentLine(context.lineAt(pos, -1).text, scanState);
  }

  const depth = Math.max(0, scanState.depth - (startsWithClosingDelimiter ? 1 : 0));

  return depth * context.unit;
}

export const portiaIndentation: Extension = [
  indentUnit.of(PORTIA_INDENT),
  indentService.of(portiaIndent),
];

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

      if (portiaKeywords.has(word)) return "keyword";
      if (portiaBooleans.has(word)) return "atom";
      if (portiaBuiltins.has(word)) return "builtin";
      
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
    indentOnInput: /^\s*(?:}|]|\))$/,
  },
});

export const portiaLanguage = portiaMode;
export default portiaLanguage;
