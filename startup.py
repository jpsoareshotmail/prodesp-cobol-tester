#!/usr/bin/env python3
"""
Script de inicialização para verificar diretórios necessários
Executa antes do web_app.py para garantir tudo está pronto
"""

import os
import sys
from pathlib import Path

print("[STARTUP] Verificando ambiente...")

# Diretórios necessários
required_dirs = [
    "PGM POC cob original",
    "templates",
    "static"
]

# Arquivos necessários
required_files = [
    "web_app.py",
    "requirements.txt",
    "mock_data_expanded.py",
    "program_descriptions.py",
    "program_history.py",
    "executor_cobol.py",
    "test_suite_expanded.py",
    "templates/index.html"
]

print("[STARTUP] Verificando diretórios...")
for directory in required_dirs:
    path = Path(directory)
    if not path.exists():
        print(f"  ❌ Diretório faltando: {directory}")
        # Criar diretório vazio se não existir
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Criado: {directory}")
    else:
        print(f"  ✓ {directory}")

print("[STARTUP] Verificando arquivos...")
for file in required_files:
    path = Path(file)
    if not path.exists():
        print(f"  ❌ Arquivo faltando: {file}")
    else:
        size_kb = path.stat().st_size / 1024
        print(f"  ✓ {file} ({size_kb:.1f} KB)")

print("[STARTUP] Verificando programas COBOL...")
pgm_dir = Path("PGM POC cob original")
cobol_files = list(pgm_dir.glob("*.C74"))
print(f"  ✓ Total de programas: {len(cobol_files)}")

if len(cobol_files) == 0:
    print(f"  ⚠️  AVISO: Nenhum arquivo .C74 encontrado!")
    print(f"  Procurando arquivos...")
    all_files = list(pgm_dir.glob("*"))
    if all_files:
        print(f"  Arquivos encontrados: {len(all_files)}")
        for f in all_files[:5]:
            print(f"    - {f.name}")
    else:
        print(f"  Diretório vazio!")

print("[STARTUP] Verificando módulos Python...")
required_modules = [
    "flask",
    "flask_cors",
    "mock_data_expanded",
    "program_descriptions",
    "program_history",
    "executor_cobol",
    "test_suite_expanded"
]

for module in required_modules:
    try:
        if module.startswith("mock_data") or module.startswith("program") or module.startswith("executor") or module.startswith("test"):
            __import__(module)
        else:
            __import__(module)
        print(f"  ✓ {module}")
    except ImportError as e:
        print(f"  ❌ {module}: {e}")

print("[STARTUP] ✅ Startup completo!")
print("[STARTUP] Iniciando Flask...")
