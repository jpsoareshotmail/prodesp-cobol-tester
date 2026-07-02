# Plano de Testes - Sistema COBOL Prodesp

## 1. Estratégia de Testes

### Objetivo
Garantir que o sistema legado COBOL funcione corretamente após compilação e identificar problemas antes da produção.

### Níveis de Teste

```
Testes Unitários
    ↓
Testes de Integração
    ↓
Testes de Sistema
    ↓
Testes de Regressão
    ↓
Testes de Performance
    ↓
Deploy
```

---

## 2. Escopo de Testes

### 2.1 Validador de Placas (PF-GAA-L004) ⭐ PRIORITÁRIO

**Tipos de Testes**: Unitários + Integração

**Casos de Teste**:
```
ENTRADA VÁLIDA:
  ✓ AAA0A00  → Código 11 (Mercosul SP)
  ✓ ABC1234  → Código 11 (Mercosul SP)
  ✓ JWD0A00  → Código 11 (Mercosul SP)
  ✓ XYZ0A00  → Código 12 (Mercosul Outros)
  ✓ SP1234   → Código 21/22 (Antiga)
  ✓ RJ1234   → Código 22 (Antiga Outros)
  ✓ AB1234   → Código 33 (2 letras carros)
  ✓ MN123    → Código 34 (2 letras motos)

ENTRADA INVÁLIDA:
  ✓ ""       → Código 00 (Vazia)
  ✓ "123"    → Código 00 (Inválida)
  ✓ "ABC123" → Código 00 (Formato errado)
  ✓ NULL     → Código 00 (Nula)
  ✓ "########" → Código 00 (Caracteres inválidos)
```

**Critério de Aceição**:
- Todas as 13 entradas retornam o código esperado
- Tempo de resposta < 100ms

---

### 2.2 Processador de Banco de Dados (PF-GAA-B100-DB)

**Tipos de Testes**: Integração + Dados

**Dados de Teste**:
- Arquivo vazio (0 registros)
- Arquivo pequeno (10 registros)
- Arquivo médio (1.000 registros)
- Arquivo grande (10.000+ registros)

**Validações**:
- Lê arquivo sequencial corretamente
- Processa todos os registros
- Gera saída esperada
- Não perde dados

---

### 2.3 Empadronização Veicular (PF-GEV-*)

**Tipos de Testes**: Integração

**Dados de Teste**:
- Tabelas de referência carregam corretamente
- Buscas retornam dados consistentes
- Performance aceitável

---

## 3. Estratégia por Tipo de Teste

### 3.1 Testes Unitários

**Objetivo**: Validar cada programa COBOL individualmente

**Escopo**:
- Validação de entrada
- Processamento de lógica
- Saída esperada

**Ferramenta**: test_suite.py

**Exemplo**:
```python
test_validador_placa()
  entrada: "AAA0A00"
  saida_esperada: 11
  saida_obtida: ?
  resultado: PASS/FAIL
```

---

### 3.2 Testes de Integração

**Objetivo**: Validar múltiplos programas trabalhando juntos

**Escopo**:
- Validador → Processador
- Processador → Tabelas
- Fluxo completo

**Dados**: Arquivos .SEQ disponibilizados

---

### 3.3 Testes de Dados

**Objetivo**: Garantir integridade dos dados

**Escopo**:
- Arquivos .SEQ processados corretamente
- Dados não são corrompidos
- Relacionamentos mantidos

**Validações**:
- Checksum de registros
- Contagem de registros
- Tipos de dados

---

### 3.4 Testes de Regressão

**Objetivo**: Garantir que mudanças não quebram funcionalidade existente

**Escopo**:
- Reexecutar testes unitários após mudanças
- Validar compatibilidade com versão anterior

**Frequência**: Antes de cada deploy

---

### 3.5 Testes de Performance

**Objetivo**: Garantir que sistema roda em tempo aceitável

**Métricas**:
- Tempo de compilação
- Tempo de execução
- Uso de memória
- Throughput (registros/segundo)

**Limites**:
- Compilação: < 30 segundos
- Validação: < 100ms
- Processamento: < 1ms/registro
- Uso RAM: < 256 MB

---

## 4. Casos de Teste Detalhados

### 4.1 Validador de Placas (PF-GAA-L004)

| ID | Entrada | Saída Esperada | Categoria | Prioridade |
|----|---------|----------------|-----------|-----------|
| TC-001 | AAA0A00 | 11 | Mercosul SP | CRÍTICA |
| TC-002 | ABC1234 | 11 | Mercosul SP | CRÍTICA |
| TC-003 | XYZ1234 | 12 | Mercosul Outros | ALTA |
| TC-004 | SP1234 | 21/22 | Antiga SP | ALTA |
| TC-005 | RJ1234 | 22 | Antiga Outros | ALTA |
| TC-006 | AB1234 | 33 | 2 letras Carros | MÉDIA |
| TC-007 | MN123 | 34 | 2 letras Motos | MÉDIA |
| TC-008 | "" | 00 | Vazia | CRÍTICA |
| TC-009 | "123456" | 00 | Inválida | CRÍTICA |
| TC-010 | NULL | 00 | Nula | ALTA |
| TC-011 | "ABC###" | 00 | Caracteres Inválidos | MÉDIA |
| TC-012 | "         " | 00 | Espaços | MÉDIA |
| TC-013 | "1234567890X" | 00 | Formato Longo | MÉDIA |

### 4.2 Processador de Banco de Dados (PF-GAA-B100-DB)

| ID | Entrada | Validação | Prioridade |
|----|---------|-----------|-----------|
| TC-020 | Arquivo Vazio | Sem erro, 0 registros | ALTA |
| TC-021 | 10 registros | Processa todos | CRÍTICA |
| TC-022 | 1.000 registros | Processa todos, < 1s | ALTA |
| TC-023 | 10.000 registros | Processa todos, < 10s | MÉDIA |
| TC-024 | Arquivo Corrompido | Trata erro graciosamente | ALTA |

---

## 5. Ambiente de Teste

### 5.1 Hardware Mínimo
- CPU: 2 GHz+
- RAM: 2 GB
- Disco: 1 GB livre

### 5.2 Software
- Python 3.13+
- GnuCOBOL 3.2+ (para testes com compilador)
- Git 2.55+

### 5.3 Dados de Teste
- Arquivos .SEQ da pasta `PGM POC cob original`
- Dados de entrada manual
- Dados aleatórios (gerados)

---

## 6. Execução de Testes

### 6.1 Teste Manual

```bash
# Validar uma placa
python executor_cobol.py validar AAA0A00

# Listar programas
python executor_cobol.py listar
```

### 6.2 Teste Automatizado

```bash
# Todos os testes
python test_suite.py

# Testes específicos
python test_suite.py --test validador
python test_suite.py --test processador
python test_suite.py --test integração

# Com relatório
python test_suite.py --report html
python test_suite.py --report json
```

### 6.3 Teste com GnuCOBOL (Após Compilar)

```bash
# Compilar
bash build.sh

# Testar binários
./build/bin/PF-GAA-L004.exe < dados_teste.txt
```

---

## 7. Critério de Aceição

### Testes Devem Passar
- ✓ Todos os casos de teste prioritários
- ✓ Taxa de sucesso ≥ 95%
- ✓ Sem erros críticos
- ✓ Performance dentro dos limites

### Antes de Deploy
- ✓ Testes unitários: 100%
- ✓ Testes integração: ≥ 95%
- ✓ Testes regressão: 100%
- ✓ Documentação atualizada

---

## 8. Relatórios de Teste

### 8.1 Formato
```
Relatório de Testes - Sistema COBOL Prodesp
Data: 2026-07-02
Versão: 1.0

RESUMO EXECUTIVO:
  Total de Testes: 25
  Passaram: 24
  Falharam: 1
  Taxa de Sucesso: 96%

DETALHES:
  [PASS] TC-001: Validador placa Mercosul SP
  [PASS] TC-002: Validador placa 2-letras
  [FAIL] TC-020: Processador arquivo vazio
  ...

RECOMENDAÇÕES:
  1. Corrigir erro em TC-020
  2. Otimizar performance de TC-023
  3. Expandir cobertura de testes
```

### 8.2 Métricas
- Taxa de sucesso (%)
- Tempo de execução
- Cobertura de código
- Bugs encontrados

---

## 9. Cronograma de Testes

| Fase | Duração | O Que | Status |
|------|---------|-------|--------|
| Preparação | 1 dia | Criar suite | ⏳ |
| Unitários | 2 dias | Validador | ⏳ |
| Integração | 2 dias | Multi-programas | ⏳ |
| Regressão | 1 dia | Histórico | ⏳ |
| Performance | 1 dia | Otimização | ⏳ |
| **Total** | **1 semana** | | |

---

## 10. Gestão de Bugs

### Ciclo de Vida
```
Encontrado → Documentado → Triagem → Corrigido → Verificado → Fechado
```

### Severidade
- **CRÍTICA**: Sistema não funciona
- **ALTA**: Funcionalidade principal quebrada
- **MÉDIA**: Funcionalidade parcialmente quebrada
- **BAIXA**: Cosmética ou documentação

### Exemplo de Bug Report
```
ID: BUG-001
Título: Validador retorna código inválido
Severidade: CRÍTICA
Dados: Entrada "SP1234" retorna 11 ao invés de 21
Reproduzir: python executor_cobol.py validar SP1234
Esperado: Código 21 (Antiga SP)
Obtido: Código 11 (Mercosul SP)
```

---

## 11. Próximos Passos

1. **Imediato**: Implementar test_suite.py
2. **Esta semana**: Executar testes unitários
3. **Próxima semana**: Testes integração
4. **Antes de deploy**: Testes regressão

---

## 12. Documentação de Suporte

- **test_suite.py** — Implementação de testes automatizados
- **test_cases.json** — Casos de teste em formato estruturado
- **run_tests.sh** — Script para executar testes
- **TEST_RESULTS.txt** — Relatório dos últimos testes

---

## Conclusão

Este plano fornece cobertura abrangente do sistema COBOL legado. 

**Próxima ação**: Implementar test_suite.py e executar testes iniciais.
