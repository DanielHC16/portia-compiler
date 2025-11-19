// src/components/TokenList.tsx
export type Token = { type: string; lexeme: string; line: number; column: number };

type Props = {
  tokens: Token[];
  hideComments?: boolean;
};

export default function TokenList({ tokens, hideComments = false }: Props) {
  const filtered = hideComments
    ? tokens.filter(t => !(t.type === 'single_comment' || t.type === 'multi_comment'))
    : tokens;

  const containerRef = useRef<HTMLDivElement | null>(null);
  const [viewportHeight, setViewportHeight] = useState(0);
  const [scrollTop, setScrollTop] = useState(0);
  const ROW_HEIGHT = 21; // keep in sync with styling

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const onResize = () => setViewportHeight(el.clientHeight);
    onResize();
    const observer = new ResizeObserver(onResize);
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const onScroll = () => {
    const el = containerRef.current;
    if (!el) return;
    setScrollTop(el.scrollTop);
  };

  const total = filtered.length;
  const startIndex = Math.max(0, Math.floor(scrollTop / ROW_HEIGHT) - 5); // buffer above
  const visibleCount = viewportHeight > 0 ? Math.ceil(viewportHeight / ROW_HEIGHT) + 10 : 50; // buffer below
  const endIndex = Math.min(total, startIndex + visibleCount);
  const slice = filtered.slice(startIndex, endIndex);
  const topSpacer = startIndex * ROW_HEIGHT;
  const bottomSpacer = (total - endIndex) * ROW_HEIGHT;

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
                    <td className='token-lexeme'>{t.lexeme}</td>
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
