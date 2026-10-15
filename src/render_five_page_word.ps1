$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$taskRoot=Split-Path -Parent $PSScriptRoot
$docPath=Join-Path $taskRoot 'reports/peinado_1012953314_assignment1_final_5pages.docx'
$outPath=Join-Path $taskRoot 'tmp/five_page'
$app=New-Object -ComObject Word.Application
$app.Visible=$false
$app.DisplayAlerts=0
try {
 Write-Output 'Opening for page rendering'
 $d=$app.Documents.Open($docPath,$false,$true,$false)
 $d.ActiveWindow.View.Type=3
 $d.ActiveWindow.View.DisplayPageBoundaries=$true
 $d.Repaginate()
 $pages=$d.ActiveWindow.Panes.Item(1).Pages
 Write-Output ('Native page count: '+$pages.Count)
 for($i=1;$i -le $pages.Count;$i++) {
  Write-Output ('Rendering page '+$i)
  $null=$app.Selection.GoTo(1,1,$i)
  $d.ActiveWindow.View.DisplayPageBoundaries=$true
  $app.ScreenRefresh()
  Start-Sleep -Milliseconds 500
  $d.Repaginate()
  $pages=$d.ActiveWindow.Panes.Item(1).Pages
  [byte[]]$bits=$pages.Item($i).EnhMetaFileBits
  $stream=New-Object System.IO.MemoryStream(,$bits)
  $meta=New-Object System.Drawing.Imaging.Metafile($stream)
  
  $bitmap=New-Object System.Drawing.Bitmap(1700,2200)
  $g=[System.Drawing.Graphics]::FromImage($bitmap)
  $g.Clear([System.Drawing.Color]::White)
  $g.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $g.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.DrawImage($meta,0,0,1700,2200)
  $bitmap.Save((Join-Path $outPath ('native-page-'+$i+'.png')),[System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose();$bitmap.Dispose();$meta.Dispose();$stream.Dispose()
 }
 $d.Close(0)
 Write-Output 'Page rendering complete'
} finally {$app.Quit()}



