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
// Lexer = Yellow, Parser = Orange, Semantic = Red
const errorColors = {
  lexical: {
    primary: 'rgb(234, 179, 8)',
    bg: 'rgba(234, 179, 8, 0.1)',
    border: 'rgba(234, 179, 8, 0.3)',
    accent: 'rgb(234, 179, 8)',
    label: 'Lexical Error'
  },
  syntax: {
    primary: 'rgb(249, 115, 22)',
    bg: 'rgba(249, 115, 22, 0.1)',
    border: 'rgba(249, 115, 22, 0.3)',
    accent: 'rgb(249, 115, 22)',
    label: 'Parsing Error'
  },
  semantic: {
    primary: 'rgb(239, 68, 68)',
    bg: 'rgba(239, 68, 68, 0.1)',
    border: 'rgba(239, 68, 68, 0.3)',
    accent: 'rgb(239, 68, 68)',
    label: 'Semantic Error'
  }
};

// Parse and format error message - clean up duplicates and format nicely
function formatErrorMessage(msg: string): React.ReactNode {
  // Remove duplicate token formats like "'token' (token)" -> "'token'"
  let cleanMsg = msg.replace(/'([^']+)'\s*\(\1\)/g, "'$1'");
  
  // Try to extract Unexpected and Expected parts
  const unexpectedMatch = cleanMsg.match(/Unexpected:\s*(.+?)(?=\s*Expected:|$)/s);
  const expectedMatch = cleanMsg.match(/Expected:\s*(.+)/s);

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

  return cleanMsg;
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
