import axios from "axios";
import type { Token, LexError } from "./types";

// Backend URL
const BASE = "http://localhost:8000";

export async function lexCode(
  code: string
): Promise<{ tokens: Token[]; errors: LexError[] }> {
  const res = await axios.post(`${BASE}/lex`, { code });
  return res.data;
}
