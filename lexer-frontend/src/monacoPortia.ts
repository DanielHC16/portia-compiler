import * as monaco from "monaco-editor";

export function registerPortiaLanguage() {
  // Register the language ID
  monaco.languages.register({ id: "portia" });

  // Define the Monarch tokenizer
  monaco.languages.setMonarchTokensProvider("portia", {
    keywords: [
      // Declarations / Storage
      "global", "using", "local", "var", "const",

      // Functions
      "func", "return", "main",

      // Types
      "int", "long", "float", "double", "char", "bool", "string", "void",

      // Concurrency / Weaving
      "weave", "thread", "threadln",

      // Control Flow
      "if", "else", "switch", "case", "break", "default",
      "for", "while", "do",

      // Error Handling
      "trap",

      // Literals
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

        // numbers
        [/\d+/, "number"],

        // strings
        [/\"([^\"\\]|\\.)*\"/, "string"],

        // operators
        [/==|!=|=|\+|\-|\*|\/|%|\.\./, "operator"],

        // delimiters
        [/[{}()\[\];,]/, "delimiter"],

        // whitespace
        [/[ \t\r\n]+/, "white"],
      ],
    },
  });
}
