# Inicia a instalacao local do projeto sem depender do PATH do Windows.
# Exemplos: ./scripts/hermes-local.ps1 --version
#           ./scripts/hermes-local.ps1 auth add openrouter --type oauth
$ErrorActionPreference = 'Stop'
$projectDirectory = Split-Path -Parent $PSScriptRoot
$localHermesHome = Join-Path $env:LOCALAPPDATA 'hermes'
$launcher = Join-Path $localHermesHome 'bin/hermes.exe'
if (-not (Test-Path -LiteralPath $launcher)) {
    throw 'Instalacao do Hermes nao encontrada em LOCALAPPDATA/hermes/bin.'
}
$previousHermesHome = $env:HERMES_HOME
try {
    $env:HERMES_HOME = $localHermesHome
    Push-Location -LiteralPath $projectDirectory
    try {
        & $launcher @args
        $commandExitCode = $LASTEXITCODE
    } finally {
        Pop-Location
    }
} finally {
    $env:HERMES_HOME = $previousHermesHome
}
exit $commandExitCode
