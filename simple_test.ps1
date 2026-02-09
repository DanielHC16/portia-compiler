#!/usr/bin/env pwsh

Write-Output "Testing Grammar Fix for Arithmetic in Conditions"

$testCode = @'
int main() {
    if (x + 1) {
        trap(x);
    }
    return 0;
}
'@

Write-Output "1. Getting tokens from lexer..."

$lexerPayload = @{
    code = $testCode
} | ConvertTo-Json

$lexerResponse = Invoke-RestMethod -Uri "http://localhost:8000/lex" -Method POST -Body $lexerPayload -ContentType "application/json"

if ($lexerResponse.tokens -and $lexerResponse.tokens.Count -gt 0) {
    Write-Output "   Lexer returned: $($lexerResponse.tokens.Count) tokens"
    if ($lexerResponse.errors -and $lexerResponse.errors.Count -gt 0) {
        Write-Output "   Lexer has $($lexerResponse.errors.Count) errors (but continuing with tokens)"
    }
    
    Write-Output "2. Sending tokens to parser..."
    $parserPayload = @{
        tokens = $lexerResponse.tokens
        lexer_errors = $lexerResponse.errors
    } | ConvertTo-Json -Depth 5
    
    $parserResponse = Invoke-RestMethod -Uri "http://localhost:8002/parse" -Method POST -Body $parserPayload -ContentType "application/json"
    
    Write-Output ""
    Write-Output "RESULT:"
    if ($parserResponse.success -eq $false) {
        Write-Output "SUCCESS: Parser rejected arithmetic in condition!"
        Write-Output "Error at line $($parserResponse.errors[0].line), column $($parserResponse.errors[0].column)"
        Write-Output "Message: $($parserResponse.errors[0].message)"
        Write-Output ""
        Write-Output "Grammar fix is working correctly!"
    } else {
        Write-Output "FAILURE: Parser still accepts arithmetic in conditions" 
        Write-Output "Grammar changes did not take effect"
    }
} else {
    Write-Output "Lexer failed or returned no tokens"
    if ($lexerResponse.errors) {
        Write-Output "Lexer errors: $($lexerResponse.errors[0].message)"
    }
}