// src/api.ts
export type Token = { type: string; lexeme: string; line: number; column: number };
export type LexError = { 
  message: string; 
  line: number; 
  column: number;
  start_index?: number;
  end_index?: number;
};

const LEXER_URL = import.meta.env.VITE_LEXER_BACKEND_URL ?? "http://localhost:8000";
const PARSER_URL = import.meta.env.VITE_PARSER_BACKEND_URL ?? "http://localhost:8001";
const SEMANTIC_URL = import.meta.env.VITE_SEMANTIC_BACKEND_URL ?? "http://localhost:8002";

async function postJSON(url: string, body: any) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${text}`);
  }
  return res.json();
}

export async function lexCode(code: string): Promise<{ tokens: Token[]; errors: LexError[] }> {
  return postJSON(`${LEXER_URL}/lex`, { code });
}

export async function parseSource(source: string) {
  return postJSON(`${PARSER_URL}/parse/source`, { source });
}

export async function parseTokens(tokens: Token[], source?: string) {
  return postJSON(`${PARSER_URL}/parse`, { tokens, source });
}

export async function analyzeTokens(tokens: Token[]) {
  return postJSON(`${SEMANTIC_URL}/analyze`, { tokens });
}

export async function analyzeAst(ast: any) {
  return postJSON(`${SEMANTIC_URL}/analyze/ast`, { ast });
}
