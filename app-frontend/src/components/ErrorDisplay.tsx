// src/components/ErrorDisplay.tsx
import React from 'react';

export type ErrorType = 'lexical' | 'syntax' | 'semantic';

export interface CompilerError {
  message: string;
  line: number;
  column: number;
  type?: string;
  token_length?: number;
}

interface ErrorDisplayProps {
  errors: CompilerError[];
  errorType: ErrorType;
}

// Color schemes for different error types
const errorColors = {
  lexical: {
    primary: 'rgb(234, 179, 8)',
    bg: 'rgba(234, 179, 8, 0.08)',
    border: 'rgba(234, 179, 8, 0.3)',
    accent: 'rgba(234, 179, 8, 0.8)',
    label: 'Lexical Error'
  },
  syntax: {
    primary: 'rgb(239, 68, 68)',
    bg: 'rgba(239, 68, 68, 0.08)',
    border: 'rgba(239, 68, 68, 0.3)',
    accent: 'rgba(239, 68, 68, 0.8)',
    label: 'Parsing Error'
  },
  semantic: {
    primary: 'rgb(139, 92, 246)',
    bg: 'rgba(139, 92, 246, 0.08)',
    border: 'rgba(139, 92, 246, 0.3)',
    accent: 'rgba(139, 92, 246, 0.8)',
    label: 'Semantic Error'
  }
};

// Parse and format error message - put Unexpected/Expected on separate lines
function formatErrorMessage(msg: string): React.ReactNode {
  // Try to extract Unexpected and Expected parts
  const unexpectedMatch = msg.match(/Unexpected:\s*(.+?)(?=\s*Expected:|$)/s);
  const expectedMatch = msg.match(/Expected:\s*(.+)/s);

  if (unexpectedMatch || expectedMatch) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
        {unexpectedMatch && (
          <div>
            <span style={{ opacity: 0.7 }}>Unexpected: </span>
            <span style={{ fontFamily: 'var(--mono)' }}>{unexpectedMatch[1].trim()}</span>
          </div>
        )}
        {expectedMatch && (
          <div>
            <span style={{ opacity: 0.7 }}>Expected: </span>
            <span style={{ fontFamily: 'var(--mono)' }}>{expectedMatch[1].trim()}</span>
          </div>
        )}
      </div>
    );
  }

  return msg;
}

export default function ErrorDisplay({ errors, errorType }: ErrorDisplayProps) {
  const colors = errorColors[errorType];

  if (errors.length === 0) return null;

  return (
    <>
      {errors.map((err, i) => (
        <div 
          key={`${errorType}-${i}`} 
          style={{
            padding: '10px 14px',
            background: colors.bg,
            border: `1px solid ${colors.border}`,
            borderLeft: `4px solid ${colors.accent}`,
            borderRadius: 6,
            fontSize: 13,
          }}
        >
          {/* Error type label */}
          <div style={{ 
            fontWeight: 600, 
            color: colors.primary,
            marginBottom: 6,
            fontSize: 13,
          }}>
            {colors.label}
          </div>

          {/* Error message */}
          <div style={{ marginBottom: 6, lineHeight: 1.5 }}>
            {formatErrorMessage(err.message)}
          </div>

          {/* Location */}
          {(err.line > 0 || err.column > 0) && (
            <div style={{ 
              fontSize: 12, 
              color: colors.primary, 
              opacity: 0.7,
              fontWeight: 500 
            }}>
              at line {err.line}, column {err.column}
            </div>
          )}
        </div>
      ))}
    </>
  );
}
