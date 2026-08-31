# =============================================================================
# Envia para a EC2 os arquivos que NAO vao pelo git (estao no .gitignore),
# necessarios para o teste COBOL real funcionar:
#   - fontes_convertidos/   (fontes Originais .C74 e Convertidos)
#   - cobol_build/copy/      (copybooks stubs)
#   - PGM POC cob original/  (fontes originais, se usar essa feature)
#
# Uso (PowerShell, na pasta do projeto):
#   .\deploy\enviar-fontes.ps1 -Ip 44.195.132.167
# =============================================================================
param(
    [Parameter(Mandatory = $true)][string]$Ip,
    [string]$Key = "vmchaves\poc-prodesp-kp.pem",
    [string]$User = "ec2-user",
    [string]$Destino = "prodesp-cobol-tester"
)

$ErrorActionPreference = "Stop"

Write-Host "Enviando fontes COBOL para $User@$Ip ..." -ForegroundColor Cyan

# garante a pasta de copybooks no destino
ssh -i $Key "$User@$Ip" "mkdir -p ~/$Destino/cobol_build/copy"

# fontes convertidos (Originais + Convertidos)
if (Test-Path "fontes_convertidos") {
    Write-Host "  -> fontes_convertidos/"
    scp -i $Key -r "fontes_convertidos" "$User@${Ip}:~/$Destino/"
}

# copybooks/stubs de compilacao
if (Test-Path "cobol_build\copy") {
    Write-Host "  -> cobol_build/copy/"
    scp -i $Key -r "cobol_build\copy" "$User@${Ip}:~/$Destino/cobol_build/"
}

# fontes originais (opcional - usados na aba de codigo)
if (Test-Path "PGM POC cob original") {
    Write-Host "  -> PGM POC cob original/"
    scp -i $Key -r "PGM POC cob original" "$User@${Ip}:~/$Destino/"
}

Write-Host "Concluido. Reinicie o servidor na EC2 se ele ja estiver rodando." -ForegroundColor Green
