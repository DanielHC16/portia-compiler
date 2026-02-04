// src/components/ASTTreeView.tsx
import { useState } from "react";
import * as React from "react";

interface ASTTreeViewProps {
  ast: any;
}

interface TreeNodeProps {
  node: any;
  depth?: number;
  fieldName?: string;
}

function TreeNode({ node, depth = 0, fieldName }: TreeNodeProps) {
  // Start collapsed for all nodes except the root
  const [collapsed, setCollapsed] = useState(depth > 0);

  if (!node) {
    return <div style={{ color: "var(--text-muted)", fontStyle: "italic" }}>null</div>;
  }

  // Handle primitive values
  if (typeof node !== 'object' || node === null) {
    return <span style={{ color: "var(--success)" }}>{String(node)}</span>;
  }

  // Handle arrays
  if (Array.isArray(node)) {
    if (node.length === 0) {
      return <span style={{ color: "var(--text-muted)" }}>[]</span>;
    }
    return (
      <div style={{ marginLeft: depth > 0 ? 20 : 0 }}>
        <div 
          onClick={() => setCollapsed(!collapsed)}
          style={{ 
            cursor: "pointer", 
            userSelect: "none",
            color: "var(--text-muted)",
            fontWeight: 500
          }}
        >
          {collapsed ? "▶" : "▼"} Array[{node.length}]
        </div>
        {!collapsed && (
          <div style={{ marginLeft: 20, borderLeft: "2px solid var(--border)", paddingLeft: 12 }}>
            {node.map((item, i) => (
              <div key={i} style={{ marginTop: 8 }}>
                <span style={{ color: "var(--warning)", marginRight: 8 }}>[{i}]</span>
                <TreeNode node={item} depth={depth + 1} fieldName={fieldName} />
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  // Get node type from type field or infer from structure
  const nodeType = node.type || getNodeType(node);
  const children = getNodeChildren(node);

  return (
    <div style={{ marginLeft: depth > 0 ? 20 : 0 }}>
      <div 
        onClick={() => setCollapsed(!collapsed)}
        style={{ 
          cursor: children.length > 0 ? "pointer" : "default",
          userSelect: "none",
          padding: "6px 12px",
          background: "var(--bg-secondary)",
          border: "1px solid var(--border)",
          borderRadius: 6,
          marginBottom: 8,
          display: "inline-block",
          maxWidth: "100%",
          wordWrap: "break-word",
          overflowWrap: "break-word",
          boxSizing: "border-box"
        }}
      >
        {children.length > 0 && <span style={{ marginRight: 8 }}>{collapsed ? "▶" : "▼"}</span>}
        <span style={{ fontWeight: 600, color: "var(--primary)" }}>{nodeType}</span>
        {renderNodeValue(node)}
      </div>
      
      {!collapsed && children.length > 0 && (
        <div style={{ 
          marginLeft: 20, 
          borderLeft: "2px solid var(--border)", 
          paddingLeft: 12,
          paddingTop: 4,
          paddingBottom: 4
        }}>
          {children.map((child, i) => (
            <div key={i} style={{ marginTop: 12, marginBottom: 12 }}>
              <div style={{ 
                color: "var(--warning)", 
                fontSize: 12, 
                marginBottom: 4,
                fontWeight: 500,
                textTransform: "uppercase"
              }}>
                {child.label}
              </div>
              <TreeNode node={child.value} depth={depth + 1} fieldName={child.label.replace(/ /g, '_')} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function getNodeType(node: any): string {
  if (node.node_type) return node.node_type;
  if (node.type) return node.type;
  if (node.operator) return `${node.operator} Operator`;
  if (node.identifier) return "Identifier";
  if (node.value !== undefined) return "Literal";
  return "Node";
}

function renderNodeValue(node: any): React.ReactElement | null {
  const parts: React.ReactElement[] = [];

  if (node.value !== undefined && typeof node.value !== 'object') {
    parts.push(
      <span key="value" style={{ marginLeft: 8, color: "var(--success)" }}>
        = {JSON.stringify(node.value)}
      </span>
    );
  }

  if (node.identifier) {
    parts.push(
      <span key="id" style={{ marginLeft: 8, color: "var(--info)" }}>
        "{node.identifier}"
      </span>
    );
  }

  if (node.name && !node.identifier) {
    parts.push(
      <span key="name" style={{ marginLeft: 8, color: "var(--info)" }}>
        "{node.name}"
      </span>
    );
  }

  if (node.data_type) {
    parts.push(
      <span key="dtype" style={{ marginLeft: 8, color: "var(--info)" }}>
        : {node.data_type}
      </span>
    );
  }

  if (node.line !== undefined || node.column !== undefined) {
    parts.push(
      <span key="pos" style={{ marginLeft: 8, fontSize: 11, color: "var(--text-muted)" }}>
        @{node.line}:{node.column}
      </span>
    );
  }

  return parts.length > 0 ? <>{parts}</> : null;
}

function getNodeChildren(node: any): Array<{ label: string; value: any }> {
  const children: Array<{ label: string; value: any }> = [];
  
  // Skip these metadata fields
  const skipFields = ['type', 'node_type', 'line', 'column', 'value', 'identifier', 'name', 'data_type'];
  
  for (const [key, value] of Object.entries(node)) {
    if (skipFields.includes(key)) continue;
    if (value === null || value === undefined) continue;
    
    // Skip empty arrays
    if (Array.isArray(value) && value.length === 0) continue;
    
    children.push({
      label: key.replace(/_/g, ' '),
      value: value
    });
  }
  
  return children;
}

export default function ASTTreeView({ ast }: ASTTreeViewProps) {
  if (!ast) {
    return (
      <div style={{ 
        padding: 24, 
        textAlign: "center", 
        color: "var(--text-muted)",
        fontStyle: "italic" 
      }}>
        No AST available
      </div>
    );
  }

  return (
    <div style={{ 
      padding: 16,
      fontFamily: "var(--mono)",
      fontSize: 13,
      height: "100%",
      overflow: "auto",
      maxWidth: "100%",
      boxSizing: "border-box"
    }}>
      <TreeNode node={ast} />
    </div>
  );
}
