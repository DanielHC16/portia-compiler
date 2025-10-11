import React from "react";
import type { Token } from "../types";

export const TokenTable: React.FC<{ tokens: Token[] }> = ({ tokens }) => (
  <div className="panel">
    <h3>Tokens</h3>
    {tokens.length === 0 ? (
      <div>No tokens yet</div>
    ) : (
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Lexeme</th>
            <th>Line</th>
            <th>Column</th>
          </tr>
        </thead>
        <tbody>
          {tokens.map((t, i) => (
            <tr key={i}>
              <td>{t.type}</td>
              <td>{t.lexeme}</td>
              <td>{t.line}</td>
              <td>{t.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )}
  </div>
);
