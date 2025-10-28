import type * as Monaco from "monaco-editor";

export function registerPortiaLanguage(monaco: typeof Monaco) {
  // Register the language if not already registered
  const languages = monaco.languages.getLanguages();
  if (!languages.find(lang => lang.id === "portia")) {
    monaco.languages.register({ id: "portia" });
  }

  // Set the Monarch tokenizer
  monaco.languages.setMonarchTokensProvider("portia", {
    defaultToken: "invalid",
    ignoreCase: false,
    
    keywords: [
      "break", "bool", "const", "case", "char", "default", "double", "do",
      "else", "false", "float", "func", "for", "global", "int", "if",
      "local", "long", "main", "return", "string", "switch", "thread",
      "threadln", "trap", "true", "using", "void", "var", "while", "weave"
    ],

    tokenizer: {
      root: [
        // Whitespace
        [/[ \t\r\n]+/, "white"],

        // Comments (must come before operators to catch //)
        [/\/\/.*$/, "comment"],
        [/\/\*/, "comment", "@comment"],

        // Keywords and identifiers
        [/[a-zA-Z_]\w*/, {
          cases: {
            "@keywords": "keyword",
            "@default": "identifier"
          }
        }],

        // Numbers
        [/\d+\.\d+([eE][\-+]?\d+)?/, "number.float"],
        [/\d+/, "number"],

        // Strings
        [/"([^"\\]|\\.)*$/, "string.invalid"],  // non-terminated string
        [/"/, "string", "@string"],

        // Characters
        [/'[^'\\]'/, "string"],
        [/'\\.'/, "string"],
        [/'/, "string.invalid"],

        // Operators
        [/==|!=|<=|>=|&&|\|\||<<|>>|\+\+|--|\.\.|\+=|-=|\*=|\/=|%=/, "operator"],
        [/[=+\-*\/%<>!&|]/, "operator"],

        // Delimiters
        [/[{}()\[\];,:\.]/, "delimiter"],
      ],

      comment: [
        [/[^\/*]+/, "comment"],
        [/\*\//, "comment", "@pop"],
        [/[\/*]/, "comment"]
      ],

      string: [
        [/[^\\"]+/, "string"],
        [/\\./, "string.escape"],
        [/"/, "string", "@pop"],
        [/$/, "string.invalid", "@pop"]
      ],
    },
  });

  // Define the theme
  monaco.editor.defineTheme("portia-hc-dark", {
    base: "hc-black",
    inherit: true,
    rules: [
      { token: "keyword",      foreground: "FFCC00", fontStyle: "bold" },
      { token: "identifier",   foreground: "FFFFFF" },
      { token: "number",       foreground: "00FF00" },
      { token: "number.float", foreground: "7FFF00" },
      { token: "string",       foreground: "00BFFF" },
      { token: "string.escape", foreground: "FF00FF" },
      { token: "string.invalid", foreground: "FF0000" },
      { token: "operator",     foreground: "FF69B4" },
      { token: "delimiter",    foreground: "AAAAAA" },
      { token: "comment",      foreground: "888888", fontStyle: "italic" },
      { token: "invalid",      foreground: "FF0000" },
    ],
    colors: {
      "editor.background": "#000000",
      "editor.foreground": "#FFFFFF",
    },
  });
}
