// src/api.ts
// Central frontend API client for every compiler phase. Keeping the request
// helpers here gives each panel the same backend contract for lexing, parsing,
// semantic analysis, TAC generation, and runtime execution.
export type Token = { type: string; lexeme: string; line: number; column: number };
export type LexError = { 
  message: string; 
  line: number; 
  column: number;
  start_index?: number;
  end_index?: number;
  token_length?: number;  // Parser errors include token length for exact highlighting
};

// ICG Types
export type ICGError = {
  type: string;
  message: string;
  line: number;
  column: number;
  token_length?: number;
};

export type TACTriple = {
  op: string;
  arg1: any;
  arg2: any;
  line: number;
  col: number;
};

export type TACTable = {
  triples: TACTriple[];
  pointers: number[];
};

export type GenerateResponse = {
  success: boolean;
  tac: TACTable | null;
  tac_text: string | null;
  tac_html: string | null;
  errors: ICGError[];
};

export type RunResponse = {
  success: boolean;
  tac: TACTable | null;
  tac_text: string | null;
  tac_html: string | null;
  output: string[];
  return_value: any;
  errors: ICGError[];
  waiting_for_input: boolean;
  input_var_name: string | null;
  input_var_type: string | null;
  input_line: number;
  input_col: number;
};

// In production (Vercel build), import.meta.env.PROD === true and all requests
// go to the same-origin /api/* serverless functions.
// In development (npm run dev) they fall back to the local backend servers.
const _isProd = import.meta.env.PROD;
const _lexerBase    = import.meta.env.VITE_LEXER_BACKEND_URL    ?? "http://localhost:8000";
const _parserBase   = import.meta.env.VITE_PARSER_BACKEND_URL   ?? "http://localhost:8001";
const _semanticBase = import.meta.env.VITE_SEMANTIC_BACKEND_URL ?? "http://localhost:8002";
const _icgBase      = import.meta.env.VITE_ICG_BACKEND_URL      ?? "http://localhost:8003";

const LEX_URL         = _isProd ? "/api/lex"          : `${_lexerBase}/lex`;
const PARSE_URL       = _isProd ? "/api/parse"        : `${_parserBase}/parse`;
const PARSE_SRC_URL   = _isProd ? "/api/parse_source" : `${_parserBase}/parse/source`;
const ANALYZE_AST_URL = _isProd ? "/api/analyze_ast"  : `${_semanticBase}/analyze/ast`;
const ICG_RUN_URL     = _isProd ? "/api/icg_run"      : `${_icgBase}/run`;
const ICG_GENERATE_URL = _isProd ? "/api/icg_generate" : `${_icgBase}/generate`;
const ICG_EXECUTE_URL  = _isProd ? "/api/icg_execute"  : `${_icgBase}/execute`;

// Send one JSON POST request and normalize HTTP failures into thrown errors.
// Panels pass AbortSignal here so a newer run can cancel an older request.
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

// Phase 1: send raw source text to the lexer and return token/error arrays.
export async function lexCode(code: string, opts?: { signal?: AbortSignal }): Promise<{ tokens: Token[]; errors: LexError[] }> {
  const response = await postJSON(LEX_URL, { code }, opts);
  return {
    tokens: response.tokens || [],
    errors: response.errors || []
  };
}

// Convenience syntax endpoint that lets the parser service call the lexer first.
export async function parseSource(source: string, opts?: { signal?: AbortSignal }) {
  return postJSON(PARSE_SRC_URL, { source }, opts);
}

// Phase 2: send lexer tokens to the parser. The source and lexer errors are
// forwarded so the backend can produce better parser responses and block on
// lexical failures.
export async function parseTokens(tokens: Token[], source?: string, lexer_errors?: LexError[], opts?: { signal?: AbortSignal }) {
  return postJSON(PARSE_URL, { tokens, source, lexer_errors }, opts);
}

// Phase 3: send the parser AST to semantic analysis and receive errors plus
// the exported symbol table used by the ICG/runtime phase.
export async function analyzeAst(ast: any, opts?: { signal?: AbortSignal }) {
  return postJSON(ANALYZE_AST_URL, { ast }, opts);
}

// =============================================================================
// ICG (Intermediate Code Generation) API
// =============================================================================

// Phase 4a: generate TAC from a semantically valid AST without executing it.
export async function generateTAC(
  ast: any,
  symbolTable?: any,
  opts?: { signal?: AbortSignal }
): Promise<GenerateResponse> {
  return postJSON(ICG_GENERATE_URL, { ast, symbol_table: symbolTable }, opts);
}

// Phase 4b: execute serialized TAC, usually for debugging generated triples.
export async function executeTAC(
  tac: TACTable,
  inputs: string[] = [],
  symbolTable?: any,
  opts?: { signal?: AbortSignal }
) {
  return postJSON(ICG_EXECUTE_URL, { tac, inputs, symbol_table: symbolTable }, opts);
}

// Phase 4 main path: generate TAC and run it in one backend call. The ICG panel
// uses this so it can display both generated code and runtime output together.
export async function runProgram(
  ast: any,
  inputs: string[] = [],
  symbolTable?: any,
  opts?: { signal?: AbortSignal }
): Promise<RunResponse> {
  return postJSON(ICG_RUN_URL, { ast, inputs, symbol_table: symbolTable }, opts);
}
