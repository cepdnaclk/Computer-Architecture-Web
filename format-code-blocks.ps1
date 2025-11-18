# PowerShell script to format code blocks in lecture markdown files

$lectureFiles = Get-ChildItem "Lectures\markdown\*.md"

foreach ($file in $lectureFiles) {
    Write-Host "Processing: $($file.Name)"
    
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    
    # Pattern 1: Fix assembly code blocks without language specifier
    # Match lines like: assembly (not followed by `) then code lines starting with spaces
    $content = $content -replace '(?m)^assembly\s*\r?\n((?:[ ]{4,}.*\r?\n)+)', '```assembly' + "`n" + '$1```' + "`n"
    
    # Pattern 2: Fix c code blocks without language specifier
    $content = $content -replace '(?m)^c\s*\r?\n((?:[ ]{4,}.*\r?\n)+)', '```c' + "`n" + '$1```' + "`n"
    
    # Pattern 3: Fix bash code blocks without language specifier
    $content = $content -replace '(?m)^bash\s*\r?\n((?:[ ]{4,}.*\r?\n)+)', '```bash' + "`n" + '$1```' + "`n"
    
    # Pattern 4: Fix python code blocks without language specifier
    $content = $content -replace '(?m)^python\s*\r?\n((?:[ ]{4,}.*\r?\n)+)', '```python' + "`n" + '$1```' + "`n"
    
    # Pattern 5: Fix verilog code blocks without language specifier
    $content = $content -replace '(?m)^verilog\s*\r?\n((?:[ ]{4,}.*\r?\n)+)', '```verilog' + "`n" + '$1```' + "`n"
    
    # Pattern 6: Fix Assembly with capital A
    $content = $content -replace '(?m)^Assembly\s*\r?\n((?:[ ]{4,}.*\r?\n)+)', '```assembly' + "`n" + '$1```' + "`n"
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  Updated" -ForegroundColor Green
    } else {
        Write-Host "  No changes needed" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Formatting complete!" -ForegroundColor Cyan
