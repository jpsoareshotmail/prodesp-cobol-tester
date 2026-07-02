# Script para Setup do GitHub
# Execute: .\setup_github.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup GitHub - Prodesp COBOL Tester" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está na pasta correta
if (!(Test-Path "web_app.py")) {
    Write-Host "ERRO: web_app.py nao encontrado!" -ForegroundColor Red
    Write-Host "Execute este script na pasta: c:\Projetos\outros\prodescp\codigo" -ForegroundColor Yellow
    exit
}

Write-Host "[1/5] Verificando Git..." -ForegroundColor Cyan
try {
    git --version | Out-Null
    Write-Host "      Git ja instalado!" -ForegroundColor Green
} catch {
    Write-Host "      ERRO: Git nao instalado!" -ForegroundColor Red
    Write-Host "      Baixe em: https://git-scm.com/download" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "[2/5] Configurando Git..." -ForegroundColor Cyan
$name = Read-Host "Digite seu nome completo"
$email = Read-Host "Digite seu email (mesmo do GitHub)"

git config --global user.name "$name"
git config --global user.email "$email"
Write-Host "      Configurado!" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] Inicializando repositorio..." -ForegroundColor Cyan
if (!(Test-Path ".git")) {
    git init
    Write-Host "      Repositorio inicializado!" -ForegroundColor Green
} else {
    Write-Host "      Repositorio ja existe!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/5] Adicionando arquivos..." -ForegroundColor Cyan
git add .
$count = (git ls-files | Measure-Object -Line).Lines
Write-Host "      $count arquivos adicionados!" -ForegroundColor Green

Write-Host ""
Write-Host "[5/5] Primeiro commit..." -ForegroundColor Cyan
if (git diff --cached --quiet) {
    Write-Host "      Nenhuma mudanca para fazer commit" -ForegroundColor Yellow
} else {
    git commit -m "Inicial: Sistema de Testes COBOL Prodesp"
    Write-Host "      Commit criado!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Proximas etapas:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Crie repositorio no GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Yellow
Write-Host "   Repository name: prodesp-cobol-tester" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Copie a URL do repositorio" -ForegroundColor White
Write-Host ""
Write-Host "3. Execute os comandos abaixo:" -ForegroundColor White
Write-Host "   git remote add origin [COLE_A_URL_AQUI]" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Quando pedir autenticacao:" -ForegroundColor White
Write-Host "   Username: seu username do GitHub" -ForegroundColor Yellow
Write-Host "   Password: seu Personal Access Token" -ForegroundColor Yellow
Write-Host "   (Gerar em: Settings > Developer settings > Personal access tokens)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Documentacao completa:" -ForegroundColor Cyan
Write-Host "   GITHUB_SETUP.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
