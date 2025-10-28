# PORTIA Frontend# React + TypeScript + Vite



Interactive web interface for the PORTIA compiler, built with React, TypeScript, and Vite.This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.



## StructureCurrently, two official plugins are available:



```- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh

src/- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

├── api.ts              # Backend API client (lexer, parser, semantic)

├── index.css           # Global styles and CSS variables## React Compiler

├── main.tsx            # Application entry point

└── components/The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

    ├── Layout.css      # Component-specific styles

    ├── ViewSwitcher.tsx    # Main app with tab navigation## Expanding the ESLint configuration

    ├── LexerPanel.tsx      # Lexical analysis interface

    ├── ParserTBA.tsx       # Syntax parser (to be implemented)If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

    ├── SemanticTBA.tsx     # Semantic analyzer (to be implemented)

    └── TokenList.tsx       # Token display component```js

```export default defineConfig([

  globalIgnores(['dist']),

## Features  {

    files: ['**/*.{ts,tsx}'],

### Lexical Analysis    extends: [

- Real-time syntax highlighting      // Other configs...

- Token generation with 20ms debounce

- Error highlighting and reporting      // Remove tseslint.configs.recommended and replace with this

- Line numbers and synchronized scrolling      tseslint.configs.recommendedTypeChecked,

- Hide/show comments toggle      // Alternatively, use this for stricter rules

      tseslint.configs.strictTypeChecked,

### Syntax Analysis (TBA)      // Optionally, add this for stylistic rules

- Parse tree generation      tseslint.configs.stylisticTypeChecked,

- AST visualization

      // Other configs...

### Semantic Analysis (TBA)    ],

- Symbol table    languageOptions: {

- Type checking      parserOptions: {

- Scope analysis        project: ['./tsconfig.node.json', './tsconfig.app.json'],

        tsconfigRootDir: import.meta.dirname,

## Development      },

      // other options...

```bash    },

npm install  },

npm run dev])

``````



## Backend IntegrationYou can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:



The frontend connects to three backend services:```js

// eslint.config.js

- **Lexer**: `http://localhost:8000`import reactX from 'eslint-plugin-react-x'

- **Parser**: `http://localhost:8001`import reactDom from 'eslint-plugin-react-dom'

- **Semantic**: `http://localhost:8002`

export default defineConfig([

Configure via environment variables:  globalIgnores(['dist']),

- `VITE_LEXER_BACKEND_URL`  {

- `VITE_PARSER_BACKEND_URL`    files: ['**/*.{ts,tsx}'],

- `VITE_SEMANTIC_BACKEND_URL`    extends: [

      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
