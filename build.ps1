<#
.SYNOPSIS
    Builds MatchaRegex as a standalone Windows application with Nuitka.

.DESCRIPTION
    Produces build\main.dist\MatchaRegex.exe together with all required DLLs
    and data files. Copy the whole main.dist folder to distribute the app.

.PARAMETER Clean
    Delete the previous build output before building.

.PARAMETER IncludeConfig
    Ship the local src\config folder (saved regex presets) with the build.

.PARAMETER Console
    Keep a console window attached (useful for debugging crashes).

.EXAMPLE
    .\build.ps1 -Clean
#>
[CmdletBinding()]
param(
    [switch]$Clean,
    [switch]$IncludeConfig,
    [switch]$Console
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$AppName   = "MatchaRegex"
$Version   = "1.0.0"
$Entry     = "src\main.py"
$Icon      = "src\gui\assets\icons\matcha-latte.ico"
$OutputDir = "build"

# --- Resolve Python (project venv preferred, uv as fallback) ---------------
$VenvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        throw "No .venv found and 'uv' is not installed. Run 'uv sync' first."
    }
    Write-Host "Creating virtual environment with uv sync..." -ForegroundColor Cyan
    uv sync
    if ($LASTEXITCODE -ne 0) { throw "uv sync failed." }
}

& $VenvPython -c "import nuitka" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Nuitka is not installed in .venv. Run 'uv sync' (it is a dev dependency)."
}

foreach ($path in @($Entry, $Icon)) {
    if (-not (Test-Path $path)) { throw "Required file not found: $path" }
}

if ($Clean -and (Test-Path $OutputDir)) {
    Write-Host "Removing previous build output..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force $OutputDir
}

# --- Nuitka arguments --------------------------------------------------------
$NuitkaArgs = @(
    "-m", "nuitka",
    "--standalone",
    "--enable-plugin=pyside6",
    "--assume-yes-for-downloads",          # allows Nuitka to fetch a C compiler if none is installed
    "--output-dir=$OutputDir",
    "--output-filename=$AppName.exe",
    "--windows-icon-from-ico=$Icon",
    "--company-name=Jovan",
    "--product-name=$AppName",
    "--file-version=$Version",
    "--product-version=$Version",
    "--file-description=$AppName - regex log search",
    # Runtime data loaded from disk (see src\app_paths.py)
    "--include-data-dir=src\gui\assets\styles=gui\assets\styles",
    "--include-data-dir=src\gui\assets\images=gui\assets\images",
    "--include-data-files=$Icon=gui\assets\icons\matcha-latte.ico"
)

if ($Console) {
    $NuitkaArgs += "--windows-console-mode=force"
} else {
    $NuitkaArgs += "--windows-console-mode=disable"
}

if ($IncludeConfig) {
    if (Test-Path "src\config") {
        $NuitkaArgs += "--include-data-dir=src\config=config"
    } else {
        Write-Warning "src\config does not exist - skipping."
    }
}

$NuitkaArgs += $Entry

# --- Build -------------------------------------------------------------------
Write-Host "Building $AppName $Version with Nuitka..." -ForegroundColor Cyan
$Stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

& $VenvPython @NuitkaArgs
if ($LASTEXITCODE -ne 0) {
    throw "Nuitka build failed with exit code $LASTEXITCODE."
}

$DistDir = Join-Path $OutputDir "main.dist"
$Exe     = Join-Path $DistDir "$AppName.exe"
$Stopwatch.Stop()

if (-not (Test-Path $Exe)) { throw "Build finished but $Exe was not found." }

Write-Host ""
Write-Host ("Build succeeded in {0:mm\:ss}." -f $Stopwatch.Elapsed) -ForegroundColor Green
Write-Host "Executable: $Exe"
Write-Host "Distribute the whole folder: $DistDir"
