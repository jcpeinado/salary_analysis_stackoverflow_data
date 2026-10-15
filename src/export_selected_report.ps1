$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$docPath = Join-Path $taskRoot 'reports/peinado_1012953314_assignment1_selected.docx'
$pdfPath = Join-Path $taskRoot 'reports/peinado_1012953314_assignment1_selected.pdf'
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
  $reportDoc = $wordApp.Documents.Open($docPath, $false, $true)
  $reportDoc.ExportAsFixedFormat($pdfPath, 17)
  $reportDoc.Close(0)
  Write-Output $pdfPath
} finally { $wordApp.Quit() }
