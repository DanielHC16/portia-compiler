// src/components/TokenList.tsx
export type Token = { type: string; lexeme: string; line: number; column: number };

type Props = {
  tokens: Token[];
  hideComments?: boolean;
};

export default function TokenList({ tokens, hideComments = false }: Props) {
  const visible = hideComments ? tokens.filter(t => !(t.type === "COMMENT" || t.type === "ML_COMMENT")) : tokens;

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div className="token-controls">
        <div className="small">Count: {visible.length}</div>
      </div>
      {visible.length === 0 ? (
        <div style={{ color: "#666", fontStyle: "italic", padding: "20px", textAlign: "center" }}>
          No tokens to display
        </div>
      ) : (
        <div style={{ flex: "1 1 auto", overflow: "auto" }}>
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
      )}
    </div>
  );
}
