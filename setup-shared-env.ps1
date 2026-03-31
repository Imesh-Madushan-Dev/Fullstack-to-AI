param(
    [string]$VenvName = "venv"
)

$ErrorActionPreference = "Stop"

$venvPath = Join-Path $PSScriptRoot $VenvName
$activatePath = Join-Path $venvPath "Scripts\Activate.ps1"
$requirementsPath = Join-Path $PSScriptRoot "requirements-shared.txt"

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating shared virtual environment at $venvPath"
    python -m venv $venvPath
} else {
    Write-Host "Shared virtual environment already exists at $venvPath"
}

if (-not (Test-Path $activatePath)) {
    throw "Could not find activation script at $activatePath"
}

if (-not (Test-Path $requirementsPath)) {
    throw "Could not find $requirementsPath"
}

. $activatePath

Write-Host "Upgrading pip"
python -m pip install --upgrade pip

Write-Host "Installing shared dependencies from requirements-shared.txt"
python -m pip install -r $requirementsPath

Write-Host "Shared environment is ready."
Write-Host "Activate anytime with: .\\$VenvName\\Scripts\\Activate.ps1"
