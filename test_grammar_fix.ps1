#!/usr/bin/env pwsh
# Test script to verify the grammar fix for arithmetic in conditions

Write-Output "=== Testing Grammar Fix for Arithmetic in Conditions ==="

# Test code that should be rejected
$testCode = @'
int main() {
    if (x + 1) {
        trap(x);
    }
    return 0;
}
'@

Write-Output "1. Testing problematic code: if (x + 1)"

# Step 1: Get tokens from lexer
$lexerPayload = @{
    source_code = $testCode
} | ConvertTo-Json

try {
    $lexerResponse = Invoke-RestMethod -Uri "http://localhost:8000/tokens" -Method POST -Body $lexerPayload -ContentType "application/json"
    
    if ($lexerResponse.success) {
        Write-Output "✓ Lexer succeeded: $($lexerResponse.tokens.Count) tokens"
        
        # Step 2: Send tokens to parser
        $parserPayload = @{
            tokens = $lexerResponse.tokens
        } | ConvertTo-Json -Depth 5
        
        $parserResponse = Invoke-RestMethod -Uri "http://localhost:8002/parse" -Method POST -Body $parserPayload -ContentType "application/json"
        
        Write-Output ""
        Write-Output "=== PARSER RESULT ==="
        if ($parserResponse.success -eq $false) {
            Write-Output "🎯 SUCCESS: Parser correctly rejected arithmetic in condition!"
            Write-Output "   Line: $($parserResponse.errors[0].line)"
            Write-Output "   Column: $($parserResponse.errors[0].column)"
            Write-Output "   Message: $($parserResponse.errors[0].message)"
            Write-Output ""
            Write-Output "✅ Grammar fix is working correctly!"
        } else {
            Write-Output "❌ FAILURE: Parser still accepts arithmetic in conditions"
            Write-Output "   The grammar changes did not take effect properly"
        }
    } else {
        Write-Output "❌ Lexer failed: $($lexerResponse.errors[0].message)"
    }
} catch {
    Write-Output "❌ Error: $($_.Exception.Message)"
}