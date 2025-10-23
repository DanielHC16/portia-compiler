import type { Token } from "../api";

type Props = {
  source: string;
  tokens: (Token & { start?: number; end?: number })[];
  className?: string;
};

/**
 * Highlights source using start/end offsets on tokens when available.
 * Falls back to line/column conversion when offsets are missing.
 */

export default function HighlightedSource({ source, tokens, className }: Props) {
  if (!source) return <div className={className}><pre /></div>;
  if (!tokens || tokens.length === 0) return <div className={className}><pre>{escapeHtml(source)}</pre></div>;

  const useOffsets = tokens.every(t => typeof (t as any).start === "number" && typeof (t as any).end === "number");

  const segments: { text: string; cls?: string }[] = [];
  let pos = 0;

  if (useOffsets) {
    const sorted = tokens.slice().sort((a, b) => (a.start! - b.start!));
    for (const tk of sorted) {
      const s = Math.max(0, Math.min(source.length, tk.start!));
      const e = Math.max(s, Math.min(source.length, tk.end!));
      if (s > pos) segments.push({ text: source.slice(pos, s) });
      const cls = tokenClass(tk.type);
      segments.push({ text: source.slice(s, e), cls });
      pos = e;
    }
    if (pos < source.length) segments.push({ text: source.slice(pos) });
  } else {
    // fallback: compute line starts then map line/col -> offsets
    const lineStarts: number[] = [0];
    for (let i = 0; i < source.length; i++) {
      if (source[i] === "\n") lineStarts.push(i + 1);
    }
    const withOffsets = tokens.map((tk, idx) => {
      const l = Math.max(1, Math.min(lineStarts.length, tk.line));
      const start = lineStarts[l - 1] + Math.max(0, tk.column - 1);
      const end = start + (tk.lexeme ? tk.lexeme.length : 0);
      return { tk, start, end, idx };
    }).sort((a, b) => (a.start - b.start) || (a.idx - b.idx));

    for (const item of withOffsets) {
      const s = Math.max(0, Math.min(source.length, item.start));
      const e = Math.max(s, Math.min(source.length, item.end));
      if (s > pos) segments.push({ text: source.slice(pos, s) });
      const cls = tokenClass(item.tk.type);
      segments.push({ text: source.slice(s, e), cls });
      pos = e;
    }
    if (pos < source.length) segments.push({ text: source.slice(pos) });
  }

  return (
    <div className={className}>
      <pre style={{ margin: 0 }}>
        {segments.map((seg, i) =>
          seg.cls ? (
            <span key={i} className={seg.cls} dangerouslySetInnerHTML={{ __html: escapeHtml(seg.text) }} />
          ) : (
            <span key={i} dangerouslySetInnerHTML={{ __html: escapeHtml(seg.text) }} />
          )
        )}
      </pre>
    </div>
  );
}

function tokenClass(type?: string) {
  if (!type) return undefined;
  if (/^KW_/.test(type)) return "hl-keyword";
  if (type === "INT_LIT" || type === "FLOAT_LIT" || /_INTEGER$/.test(type)) return "hl-number";
  if (type === "STRING_LIT") return "hl-string";
  if (type === "CHAR_LIT") return "hl-char";
  if (type === "COMMENT" || type === "ML_COMMENT" || /COMMENT$/.test(type)) return "hl-comment";
  if (type === "IDENTIFIER") return "hl-identifier";
  if (type === "DELIMITER" || /SEMI|COMMA|DELIM|DELIMITER/.test(type)) return "hl-delim";
  if (type === "OPERATOR" || /ASSIGN|OP|OPERATOR/.test(type)) return "hl-operator";
  if (/^KW_(INT|LONG|FLOAT|DOUBLE|CHAR|BOOL|STRING|VOID|THREAD|FUNC|CONST|VAR|GLOBAL)$/.test(type)) return "hl-type";
  return undefined;
}

function escapeHtml(s: string) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
