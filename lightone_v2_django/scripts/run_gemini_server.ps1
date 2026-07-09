param(
    [string]$Model = "gemini-3.5-flash",
    [int]$TimeoutSeconds = 20,
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$AppRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $AppRoot

$secureKey = Read-Host "Google AI Studio GEMINI_API_KEY" -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    if ([string]::IsNullOrWhiteSpace($plainKey)) {
        throw "GEMINI_API_KEY is required to enable Gemini report drafts."
    }

    $env:GEMINI_API_KEY = $plainKey
    $env:AI_ENABLED = "1"
    $env:GEMINI_REPORT_MODEL = $Model
    $env:GEMINI_TIMEOUT_SECONDS = [string]$TimeoutSeconds

    python manage.py check
    python manage.py runserver "$HostAddress`:$Port"
}
finally {
    if ($bstr -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
    Remove-Variable plainKey -ErrorAction SilentlyContinue
}
