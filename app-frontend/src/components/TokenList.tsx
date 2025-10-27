// src/components/TokenList.tsx
export type Token = { type: string; lexeme: string; line: number; column: number };

type Props = {
  tokens: Token[];
  hideComments?: boolean;
};

export default function TokenList({ tokens, hideComments = false }: Props) {
  const visible = hideComments ? tokens.filter(t => !(t.type === "COMMENT" || t.type === "ML_COMMENT")) : tokens;

  return (
    <div>
      <div className="token-controls">
        <div className="small">Tokens: {visible.length}</div>
      </div>
      <table className="token-table">
        <thead>
          <tr>
            <th className="token-type">Type</th>
            <th className="token-lexeme">Lexeme</th>
            <th className="token-pos">Line</th>
            <th className="token-pos">Col</th>
          </tr>
        </thead>
        <tbody>
          {visible.map((t, i) => (
            <tr key={i}>
              <td className="token-type">{t.type}</td>
              <td className="token-lexeme">{t.lexeme}</td>
              <td className="token-pos">{t.line}</td>
              <td className="token-pos">{t.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
