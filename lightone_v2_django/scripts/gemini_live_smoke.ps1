param(
    [string]$Model = "gemini-3.5-flash",
    [int]$TimeoutSeconds = 20
)

$ErrorActionPreference = "Stop"

$AppRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $AppRoot

$secureKey = Read-Host "Google AI Studio GEMINI_API_KEY" -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
$TempFile = Join-Path $env:TEMP "lightone_gemini_smoke.py"
try {
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    if ([string]::IsNullOrWhiteSpace($plainKey)) {
        throw "GEMINI_API_KEY is required for the live smoke test."
    }

    $env:GEMINI_API_KEY = $plainKey
    $env:AI_ENABLED = "1"
    $env:GEMINI_REPORT_MODEL = $Model
    $env:GEMINI_TIMEOUT_SECONDS = [string]$TimeoutSeconds

    $PythonCode = @'
import json
import os
from google import genai
from pydantic import BaseModel, Field

class SmokeResult(BaseModel):
    summary: str = Field(description="비의료 PT 상담 참고용 응답 요약")
    trainer_review_required: bool
    safety_notice: str

client = genai.Client()
interaction = client.interactions.create(
    model=os.environ.get("GEMINI_REPORT_MODEL", "gemini-3.5-flash"),
    input="LIGHTONE 합성 테스트입니다. 비의료 PT 상담 참고용 한 문장 요약을 JSON으로 작성하세요.",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": SmokeResult.model_json_schema(),
    },
)
result = SmokeResult.model_validate_json(interaction.output_text)
print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
'@
    Set-Content -LiteralPath $TempFile -Value $PythonCode -Encoding UTF8
    python $TempFile
}
finally {
    if ($bstr -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
    Remove-Variable plainKey -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $TempFile -ErrorAction SilentlyContinue
}
