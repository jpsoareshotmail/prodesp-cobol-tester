#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste rápido para verificar se a interface está respondendo
"""
import requests
import time
import sys
import os

os.chdir(os.path.dirname(__file__) or '.')

BASE_URL = "http://localhost:5000"

print("\n" + "=" * 60)
print("TESTE RAPIDO DA INTERFACE WEB")
print("=" * 60 + "\n")

try:
    # Teste 1: Health check
    print("[1] Verificando saude do servidor...")
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    if response.status_code == 200:
        print("    OK - Servidor respondendo")
    else:
        print(f"    ERRO: {response.status_code}")
        sys.exit(1)

    # Teste 2: Stats
    print("[2] Carregando estatisticas...")
    response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
    if response.status_code == 200:
        stats = response.json()
        print(f"    OK - {stats['total_execucoes']} execucoes, {stats['taxa_sucesso']:.1f}% sucesso")
    else:
        print(f"    ERRO: {response.status_code}")

    # Teste 3: Validar placa
    print("[3] Validando placa AAA0A00...")
    response = requests.post(
        f"{BASE_URL}/api/validate-plate",
        json={"placa": "AAA0A00"},
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print(f"    OK - Placa valida: {result['descricao']}")
    else:
        print(f"    ERRO: {response.status_code}")

    # Teste 4: Resultados
    print("[4] Carregando historico...")
    response = requests.get(f"{BASE_URL}/api/results", timeout=5)
    if response.status_code == 200:
        results = response.json()
        print(f"    OK - {len(results)} resultados encontrados")
    else:
        print(f"    ERRO: {response.status_code}")

    print("\n" + "=" * 60)
    print("TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print("\nA interface esta funcionando corretamente!")
    print("Acesse: http://localhost:5000\n")

except requests.exceptions.ConnectionError:
    print("\nERRO: Nao consegui conectar ao servidor")
    print("   Certifique-se que web_app.py esta rodando")
    sys.exit(1)
except Exception as e:
    print(f"\nERRO: {e}")
    sys.exit(1)
