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

const LEXER_URL = import.meta.env.VITE_LEXER_BACKEND_URL ?? "http://localhost:8000";
const PARSER_URL = import.meta.env.VITE_PARSER_BACKEND_URL ?? "http://localhost:8001";
const SEMANTIC_URL = import.meta.env.VITE_SEMANTIC_BACKEND_URL ?? "http://localhost:8002";

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
  const response = await postJSON(`${LEXER_URL}/lex`, { code }, opts);
  
  return {
    tokens: response.tokens || [],
    errors: response.errors || []
  };
}

export async function parseSource(source: string, opts?: { signal?: AbortSignal }) {
  return postJSON(`${PARSER_URL}/parse/source`, { source }, opts);
}

export async function parseTokens(tokens: Token[], source?: string, opts?: { signal?: AbortSignal }) {
  return postJSON(`${PARSER_URL}/parse`, { tokens, source }, opts);
}

export async function analyzeTokens(tokens: Token[], opts?: { signal?: AbortSignal }) {
  return postJSON(`${SEMANTIC_URL}/analyze`, { tokens }, opts);
}

export async function analyzeAst(ast: any, opts?: { signal?: AbortSignal }) {
  return postJSON(`${SEMANTIC_URL}/analyze/ast`, { ast }, opts);
}
