// src/components/TokenList.tsx
import { useRef, useEffect, useState } from 'react';
export type Token = { type: string; lexeme: string; line: number; column: number };

type Props = {
  tokens: Token[];
  hideComments?: boolean;
};

export default function TokenList({ tokens, hideComments = false }: Props) {
  // Optional filtering hides comment tokens in the table without mutating the
  // original token stream shared with other panels.
  const filtered = hideComments
    ? tokens.filter(t => !(t.type === 'single_comment' || t.type === 'multi_comment'))
    : tokens;

  // Escape newlines inside string literals so each table row remains one line.
  const formatLexeme = (token: Token) => {
    if (token.type === "stringlit") {
      return token.lexeme.replace(/\n/g, "\\n");
    }
    return token.lexeme;
  };

  // Apply specialized classes for literal lexemes so strings/chars can receive
  // clearer table styling.
  const getLexemeClassName = (token: Token) => {
    if (token.type === "stringlit") return "token-lexeme token-lexeme-string";
    if (token.type === "charlit") return "token-lexeme token-lexeme-char";
    return "token-lexeme";
  };

  const containerRef = useRef<HTMLDivElement | null>(null);
  const [viewportHeight, setViewportHeight] = useState(0);
  const [scrollTop, setScrollTop] = useState(0);
  const ROW_HEIGHT = 21; // keep in sync with styling

  useEffect(() => {
    // ResizeObserver keeps virtualization accurate when the token panel changes
    // height due to responsive layout or panel resizing.
    const el = containerRef.current;
    if (!el) return;
    const onResize = () => setViewportHeight(el.clientHeight);
    onResize();
    const observer = new ResizeObserver(onResize);
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  // Track scroll position so only visible token rows are rendered.
  const onScroll = () => {
    const el = containerRef.current;
    if (!el) return;
    setScrollTop(el.scrollTop);
  };

  // Lightweight row virtualization for large token streams.
  const total = filtered.length;
  const startIndex = Math.max(0, Math.floor(scrollTop / ROW_HEIGHT) - 5); // buffer above
  const visibleCount = viewportHeight > 0 ? Math.ceil(viewportHeight / ROW_HEIGHT) + 10 : 50; // buffer below
  const endIndex = Math.min(total, startIndex + visibleCount);
  const slice = filtered.slice(startIndex, endIndex);
  const topSpacer = startIndex * ROW_HEIGHT;
  // bottomSpacer no longer needed since table absolute height manages spacing

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className='token-controls'>
        <div className='small'>Count: {filtered.length}</div>
      </div>
      {filtered.length === 0 ? (
        <div style={{ color: '#666', fontStyle: 'italic', padding: '20px', textAlign: 'center' }}>
          No tokens to display
        </div>
      ) : (
        <div ref={containerRef} style={{ flex: '1 1 auto', overflow: 'auto' }} onScroll={onScroll}>
          <div style={{ position: 'relative', height: total * ROW_HEIGHT }}>
            <table className='token-table' style={{ position: 'absolute', top: topSpacer, left: 0, right: 0 }}>
              <thead>
                <tr>
                  <th className='token-lexeme'>Lexeme</th>
                  <th className='token-type'>Token</th>
                  <th className='token-pos'>Line</th>
                  <th className='token-pos'>Col</th>
                </tr>
              </thead>
              <tbody>
                {slice.map((t, i) => (
                  <tr key={startIndex + i} style={{ height: ROW_HEIGHT }}>
                    <td className={getLexemeClassName(t)} title={t.lexeme}>
                      {formatLexeme(t)}
                    </td>
                    <td className='token-type'>{t.type}</td>
                    <td className='token-pos'>{t.line}</td>
                    <td className='token-pos'>{t.column}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {/* bottom spacer handled by container height */}
          </div>
        </div>
      )}
    </div>
  );
}
