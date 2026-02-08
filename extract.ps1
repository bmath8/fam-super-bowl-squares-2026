$html = Get-Content -Path "index.html" -Raw
$pattern = '(?s)<script type="text/babel">(.*?)</script>'
$match = [regex]::Match($html, $pattern)
if ($match.Success) {
    $jsCode = $match.Groups[1].Value
    Set-Content -Path "extracted.js" -Value $jsCode
    Write-Host "Extracted JS to extracted.js (first 500 chars):"
    Write-Host $jsCode.Substring(0, [Math]::Min(500, $jsCode.Length))
} else {
    Write-Host "No script tag found"
}
