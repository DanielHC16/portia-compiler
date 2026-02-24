// src/api.ts
export type Token = { type: string; lexeme: string; line: number; column: number };
export type LexError = { 
  message: string; 
  line: number; 
  column: number;
  start_index?: number;
  end_index?: number;
  token_length?: number;  // Parser errors include token length for exact highlighting
};

// In production (Vercel build), import.meta.env.PROD === true and all requests
// go to the same-origin /api/* serverless functions.
// In development (npm run dev) they fall back to the local backend servers.
const _isProd = import.meta.env.PROD;
const _lexerBase    = import.meta.env.VITE_LEXER_BACKEND_URL    ?? "http://localhost:8000";
const _parserBase   = import.meta.env.VITE_PARSER_BACKEND_URL   ?? "http://localhost:8001";
const _semanticBase = import.meta.env.VITE_SEMANTIC_BACKEND_URL ?? "http://localhost:8002";

const LEX_URL         = _isProd ? "/api/lex"          : `${_lexerBase}/lex`;
const PARSE_URL       = _isProd ? "/api/parse"         : `${_parserBase}/parse`;
const PARSE_SRC_URL   = _isProd ? "/api/parse_source"  : `${_parserBase}/parse/source`;
const ANALYZE_AST_URL = _isProd ? "/api/analyze_ast"   : `${_semanticBase}/analyze/ast`;

async function postJSON(url: string, body: any, opts?: { signal?: AbortSignal }) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: opts?.signal
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }
  return res.json();
}

export async function lexCode(code: string, opts?: { signal?: AbortSignal }): Promise<{ tokens: Token[]; errors: LexError[] }> {
  const response = await postJSON(LEX_URL, { code }, opts);
  return {
    tokens: response.tokens || [],
    errors: response.errors || []
  };
}

export async function parseSource(source: string, opts?: { signal?: AbortSignal }) {
  return postJSON(PARSE_SRC_URL, { source }, opts);
}

export async function parseTokens(tokens: Token[], source?: string, lexer_errors?: LexError[], opts?: { signal?: AbortSignal }) {
  return postJSON(PARSE_URL, { tokens, source, lexer_errors }, opts);
}

export async function analyzeTokens(tokens: Token[], opts?: { signal?: AbortSignal }) {
  // No standalone token-only analysis endpoint in Vercel; not used by the UI.
  const _semanticBase_ = import.meta.env.VITE_SEMANTIC_BACKEND_URL ?? "http://localhost:8002";
  return postJSON(`${_semanticBase_}/analyze`, { tokens }, opts);
}

export async function analyzeAst(ast: any, opts?: { signal?: AbortSignal }) {
  return postJSON(ANALYZE_AST_URL, { ast }, opts);
}
