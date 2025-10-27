export type Token = {
  type: string;
  lexeme: string;
  line: number;
  column: number;
  endLine: number;
  endColumn: number;
};

export type LexError = {
  message: string;
  lexeme: string;
  line: number;
  column: number;
  endLine: number;
  endColumn: number;
};
