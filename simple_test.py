#!/usr/bin/env python3
"""
Teste simples para verificar que tudo funciona
"""
import json
from datetime import datetime
from pathlib import Path

# Gerar um resultado de teste simples
result = {
    "data": datetime.now().isoformat(),
    "duracao": 0.5,
    "total": 5,
    "passed": 3,
    "failed": 2,
    "errored": 0,
    "taxa_sucesso": 60.0,
    "resultados": [
        {
            "test_id": "TC-001",
            "nome": "Mercosul - Sao Paulo",
            "categoria": "Validador",
            "status": "PASS",
            "entrada": "AAA0A00",
            "saida_esperada": "11",
            "saida_obtida": "11",
            "tempo_ms": 0.02,
            "mensagem": "OK"
        },
        {
            "test_id": "TC-002",
            "nome": "Mercosul - Outro Estado",
            "categoria": "Validador",
            "status": "FAIL",
            "entrada": "XYZ1234",
            "saida_esperada": "12",
            "saida_obtida": "21",
            "tempo_ms": 0.01,
            "mensagem": "Resultado incorreto"
        },
        {
            "test_id": "TC-003",
            "nome": "2 letras - Carros",
            "categoria": "Validador",
            "status": "PASS",
            "entrada": "AB12C34",
            "saida_esperada": "33",
            "saida_obtida": "33",
            "tempo_ms": 0.01,
            "mensagem": "OK"
        },
        {
            "test_id": "TC-020",
            "nome": "Placa vazia",
            "categoria": "Casos Limite",
            "status": "PASS",
            "entrada": "",
            "saida_esperada": "0",
            "saida_obtida": "0",
            "tempo_ms": 0.01,
            "mensagem": ""
        },
        {
            "test_id": "TC-030",
            "nome": "Com caracteres especiais",
            "categoria": "Caracteres Especiais",
            "status": "FAIL",
            "entrada": "ABC@1234",
            "saida_esperada": "0",
            "saida_obtida": "33",
            "tempo_ms": 0.01,
            "mensagem": "Falha na validacao"
        }
    ]
}

# Salvar arquivo
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"TEST_RESULTS_{timestamp}.json"

with open(filename, 'w') as f:
    json.dump(result, f, indent=2)

print(f"[OK] Arquivo criado: {filename}")
print(f"  Total: {result['total']}")
print(f"  Passou: {result['passed']}")
print(f"  Falhou: {result['failed']}")
print(f"  Taxa: {result['taxa_sucesso']:.1f}%")
