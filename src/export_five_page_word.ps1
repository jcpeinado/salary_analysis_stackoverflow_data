$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$docPath=Join-Path $taskRoot 'reports/peinado_1012953314_assignment1_final_5pages.docx'
$pdfPath=Join-Path $taskRoot 'reports/peinado_1012953314_assignment1_final_5pages.pdf'
Write-Output 'Connecting to the existing Word application'
$wordApp=[Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
Write-Output 'Opening the new report read-only'
$reportDoc=$wordApp.Documents.Open($docPath,$false,$true,$false)
try {
 Write-Output 'Repaginating'
 $reportDoc.Repaginate()
 Write-Output ('Pages: '+$reportDoc.ComputeStatistics(2))
 Write-Output 'Exporting PDF'
 $reportDoc.ExportAsFixedFormat($pdfPath,17)
 Write-Output 'Export complete'
} finally { $reportDoc.Close(0) }
