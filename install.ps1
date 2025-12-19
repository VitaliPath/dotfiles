# --- install.ps1 ---
# Run this from PowerShell as Administrator

$ErrorActionPreference = "Stop"

Write-Host "🔗 Linking Vim configurations..." -ForegroundColor Cyan

function Link-File {
    param ([string]$name)
    $src = "$PSScriptRoot\vim\$name"
    $dest = "$HOME\_$name" # Windows uses _vimrc usually, or .vimrc

    if (Test-Path $dest) {
        Write-Host "   Backing up existing $dest" -ForegroundColor Yellow
        Move-Item -Path $dest -Destination "$dest.bak" -Force
    }
    
    # Symlink (Requires Admin or Developer Mode)
    New-Item -ItemType SymbolicLink -Path $dest -Target $src | Out-Null
    Write-Host "   Linked $src -> $dest" -ForegroundColor Green
}

Link-File "vimrc"
Link-File "vimspector.json"

# Setup Vim Plug for Windows
$vimPlugPath = "$HOME/vimfiles/autoload/plug.vim"
if (-not (Test-Path $vimPlugPath)) {
    Write-Host "🔌 Installing vim-plug..." -ForegroundColor Cyan
    $null = New-Item -ItemType Directory -Force -Path "$HOME/vimfiles/autoload"
    Invoke-WebRequest "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim" -OutFile $vimPlugPath
}

Write-Host "✅ Setup complete! Restart your terminal." -ForegroundColor Green