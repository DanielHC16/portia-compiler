import React from "react";
import type { LexError } from "../types";

export const ErrorsPanel: React.FC<{ errors: LexError[] }> = ({ errors }) => (
  <div className="panel">
    <h3>Errors</h3>
    {errors.length === 0 ? (
      <div className="no-errors">No errors</div>
    ) : (
      <table>
        <thead>
          <tr>
            <th>Message</th>
            <th>Line</th>
            <th>Column</th>
          </tr>
        </thead>
        <tbody>
          {errors.map((e, i) => (
            <tr key={i}>
              <td>{e.message}</td>
              <td>{e.line}</td>
              <td>{e.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    )}
  </div>
);
