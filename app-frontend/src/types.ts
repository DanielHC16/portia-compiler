export type Token = {
  type: string;
  lexeme: string;
  line: number;
  column: number;
};

export type LexError = {
  message: string;
  line: number;
  column: number;
};
