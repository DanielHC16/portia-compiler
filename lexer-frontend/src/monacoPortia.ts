import type * as Monaco from "monaco-editor";

export function registerPortiaLanguage(monaco: typeof Monaco) {
  monaco.languages.register({ id: "portia" });

  monaco.languages.setMonarchTokensProvider("portia", {
    keywords: [
      "global", "using", "local", "var", "const", "let", "type",
      "func", "return", "main",
      "int", "long", "float", "double", "char", "bool", "string", "void",
      "weave", "thread", "threadln",
      "if", "else", "switch", "case", "break", "default",
      "for", "while", "do",
      "trap",
      "true", "false",
    ],

    tokenizer: {
      root: [
        // identifiers and keywords
        [/[a-zA-Z_][\w]*/, {
          cases: {
            "@keywords": "keyword",
            "@default": "identifier"
          }
        }],

        // floats then ints
        [/\d+\.\d+/, "number.float"],
        [/\d+/, "number"],

        // strings
        [/\"([^\"\\]|\\.)*\"/, "string"],

        // ✅ comments
        [/\/\/.*$/, "comment"],                // single-line
        [/\/\*/, "comment", "@comment"],       // enter comment state

        // operators
        [/==|!=|=|\+|\-|\*|\/|%|\.\./, "operator"],

        // delimiters
        [/[{}()\[\];,]/, "delimiter"],

        // whitespace
        [/[ \t\r\n]+/, "white"],
      ],

      // ✅ multi-line comment state
      comment: [
        [/[^\/*]+/, "comment"],
        [/\*\//, "comment", "@pop"],           // closing */
        [/[\/*]/, "comment"]                   // still inside comment
      ],
    },
  });

  monaco.editor.defineTheme("portia-hc-dark", {
    base: "hc-black",
    inherit: true,
    rules: [
      { token: "keyword",      foreground: "FFCC00", fontStyle: "bold" },
      { token: "identifier",   foreground: "FFFFFF" },
      { token: "number",       foreground: "00FF00" },
      { token: "number.float", foreground: "7FFF00" },
      { token: "string",       foreground: "00BFFF" },
      { token: "operator",     foreground: "FF69B4" },
      { token: "delimiter",    foreground: "AAAAAA" },
      { token: "comment",      foreground: "888888", fontStyle: "italic" },
    ],
    colors: {
      "editor.background": "#000000",
      "editor.foreground": "#FFFFFF",
    },
  });
}
