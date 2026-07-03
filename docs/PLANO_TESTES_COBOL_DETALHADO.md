# Plano Detalhado de Testes - Sistema COBOL Prodesp

## Documento de Especificação de Testes

**Data**: 2026-07-02  
**Projeto**: Sistema Legado COBOL Prodesp  
**Versão**: 1.0  
**Status**: Documentação Completa

---

## 1. Introdução

Este documento especifica a estratégia completa de testes para o sistema legado COBOL da Prodesp, que valida e processa dados veiculares (placas, RENAVAM, empadronização).

### 1.1 Objetivo
Garantir que todos os 42 programas COBOL funcionem corretamente, identificando bugs antes da compilação com GnuCOBOL e validando a lógica de negócio.

### 1.2 Escopo
- **72 arquivos totais**
  - 42 programas COBOL (.C74)
  - 16 bibliotecas/copybooks (.txt)
  - 14 arquivos de dados (.SEQ)

### 1.3 Estratégia Geral
```
Testes Unitários (60%)
    ↓
Testes de Integração (25%)
    ↓
Testes de Sistemas (10%)
    ↓
Testes de Regressão (5%)
```

---

## 2. Estrutura de Testes

### 2.1 Programas Principais a Testar

#### Grupo 1: Validador de Placas (PF-GAA-L004)
```
Nome: PF-GAA-L004.C74
Objetivo: Validar placas veiculares
Entrada: LC-PLACA (10 caracteres)
Saída: LC-RETORNO (código 0-34)
Prioridade: CRÍTICA
```

**Códigos de Retorno**:
```
00 = Placa Inválida
11 = Mercosul - São Paulo
12 = Mercosul - Outros Estados
21 = Antiga - São Paulo
22 = Antiga - Outros Estados
33 = 2 Letras - Carros
34 = 2 Letras - Motos
```

#### Grupo 2: Processador de Banco de Dados (PF-GAA-B100-DB)
```
Nome: PF-GAA-B100-DB.C74
Objetivo: Processar arquivo de dados sequencial
Entrada: Arquivo .SEQ
Saída: Registros processados
Prioridade: ALTA
```

#### Grupo 3: Empadronização Veicular (PF-GEV-*)
```
Nome: 24 programas PF-GEV-T*.C74
Objetivo: Gerenciar tabelas de empadronização
Entrada: ID ou chave de busca
Saída: Dados do veículo
Prioridade: MÉDIA
```

### 2.2 Estruturas de Dados Críticas

#### Copybooks (SUP_SEECDT00.txt)
```cobol
01  SC0G-FIELDS.
    05 SC0N-CUT-OFF-YEAR PIC 99 VALUE 86.
    05 SC0X-CCYYMMDD.
       10 SC0X-CC PIC XX.
       10 SC0N-YYMMDD PIC 9(6).
```

**Testes Requeridos**:
- Validar interpretação de anos (2-dígitos vs 4-dígitos)
- Validar conversão de formatos de data
- Validar limites de valores

---

## 3. Casos de Teste - Validador de Placas

### 3.1 Testes Positivos

| TC-ID | Entrada | Saída | Tipo | Prioridade |
|-------|---------|-------|------|-----------|
| TC-001 | AAA0A00 | 11 | Mercosul SP | CRÍTICA |
| TC-002 | ABC1234 | 11 | Mercosul SP | CRÍTICA |
| TC-003 | JWD0A00 | 11 | Mercosul SP | CRÍTICA |
| TC-004 | XYZ1234 | 12 | Mercosul Outros | ALTA |
| TC-005 | SP1234 | 21 | Antiga SP | ALTA |
| TC-006 | RJ1234 | 22 | Antiga Outros | ALTA |
| TC-007 | AB1234 | 33 | 2 Letras Carro | MÉDIA |
| TC-008 | MN123 | 34 | 2 Letras Moto | MÉDIA |

### 3.2 Testes Negativos

| TC-ID | Entrada | Saída | Validação | Prioridade |
|-------|---------|-------|-----------|-----------|
| TC-020 | "" | 0 | Vazia | CRÍTICA |
| TC-021 | "   " | 0 | Espaços | CRÍTICA |
| TC-022 | "123456" | 0 | Apenas números | ALTA |
| TC-023 | "ABCDEF" | 0 | Apenas letras | ALTA |
| TC-024 | "ABC@1234" | 0 | Caracteres especiais | MÉDIA |
| TC-025 | "ABC-1234" | 0 | Com hífen | MÉDIA |

### 3.3 Testes de Casos Extremos

| TC-ID | Entrada | Saída | Cenário | Prioridade |
|-------|---------|-------|---------|-----------|
| TC-040 | NULL | 0 | Valor nulo | ALTA |
| TC-041 | "1234567890ABC" | 0 | Muito longa | MÉDIA |
| TC-042 | "A" | 0 | Muito curta | MÉDIA |
| TC-043 | "AAAAAAAAAA" | 0 | Todas letras | MÉDIA |

### 3.4 Testes de Range

| TC-ID | Faixa | Saída | Descrição | Prioridade |
|-------|-------|-------|-----------|-----------|
| TC-050 | AA-GK | 11-12 | Ranges SP | ALTA |
| TC-051 | QSN-QSZ | 12 | Ranges Outros | ALTA |
| TC-052 | SSR-SWZ | 12 | Ranges Outros | ALTA |
| TC-053 | TIO-TMJ | 12 | Ranges Outros | ALTA |
| TC-054 | UDA-UGV | 12 | Ranges Outros | ALTA |
| TC-055 | UOG-USB | 12 | Ranges Outros | ALTA |

---

## 4. Casos de Teste - Processador de Banco de Dados

### 4.1 Testes de Dados

| TC-ID | Arquivo | Registros | Validação | Prioridade |
|-------|---------|-----------|-----------|-----------|
| TC-100 | vazio.seq | 0 | Sem erro, 0 registros | ALTA |
| TC-101 | pequeno.seq | 10 | Processa todos | CRÍTICA |
| TC-102 | medio.seq | 1.000 | Processa sem erro | ALTA |
| TC-103 | grande.seq | 10.000 | Performance < 10s | MÉDIA |
| TC-104 | corrompido.seq | - | Trata erro | ALTA |

### 4.2 Testes de Integridade

| TC-ID | Validação | Tipo | Prioridade |
|-------|-----------|------|-----------|
| TC-110 | Checksum | Integridade | ALTA |
| TC-111 | Contagem | Integridade | ALTA |
| TC-112 | Tipos | Integridade | ALTA |
| TC-113 | Relacionamentos | Integridade | ALTA |

---

## 5. Execução de Testes

### 5.1 Ambiente de Teste

```
Hardware:
  - CPU: 2+ GHz
  - RAM: 2+ GB
  - Disco: 1+ GB livre

Software:
  - Python 3.13+
  - GnuCOBOL 3.2+ (quando compilar)
  - Git 2.55+
  - pytest 7.4+
```

### 5.2 Setup do Emulador/Simulator

```bash
# Android Emulator
emulator -avd TestDevice -no-snapshot-save
adb devices

# iOS Simulator
open -a Simulator
xcrun simctl list devices
```

### 5.3 Executar Testes

#### Teste Unitário (Simulador Python)
```bash
cd c:\Projetos\outros\prodescp\codigo
python executor_cobol.py validar AAA0A00
```

#### Suite Completa
```bash
python test_suite.py
```

#### Teste Específico
```bash
python executor_cobol.py validar SP1234
```

#### Com Relatório
```bash
python test_suite.py --report json
python test_suite.py --report txt
```

---

## 6. Critérios de Aceitação

### 6.1 Por Tipo de Teste

**Unitários**
```
✓ Todos passam
✓ Tempo < 100ms por teste
✓ 100% sem dependências externas
```

**Integração**
```
✓ 95%+ de sucesso
✓ Todos os programas comunicam
✓ Dados não são perdidos
```

**Sistema**
```
✓ 90%+ de sucesso
✓ Fluxo completo funciona
✓ Sem erros críticos
```

**Regressão**
```
✓ 100% compatibilidade
✓ Sem mudanças inesperadas
✓ Performance mantida
```

### 6.2 Taxa de Sucesso Requerida

| Fase | Taxa Mínima | Críticos | Bloqueadores |
|------|-------------|----------|------------|
| Desenvolvimento | 80% | 100% | 0 |
| Pré-Deploy | 95% | 100% | 0 |
| Produção | 99%+ | 100% | 0 |

---

## 7. Métricas de Teste

### 7.1 Cobertura

```
Escopo: 72 arquivos
  - Programas: 42 (100%)
  - Bibliotecas: 16 (60%)
  - Dados: 14 (40%)

Linha: 4.897 linhas de código
  - Unit tests: 2.000+ linhas
  - Integration: 1.000+ linhas
  - E2E: 500+ linhas

Funcionalidades:
  - Validação: 100%
  - Processamento: 80%
  - Empadronização: 60%
```

### 7.2 Performance

```
Validação:
  - Unitária: < 1ms
  - Suite: < 10s
  - Com relatório: < 30s

Processamento:
  - 10 registros: < 1s
  - 1.000 registros: < 5s
  - 10.000 registros: < 30s
```

### 7.3 Bugs Esperados

```
Críticos: 0 (antes de deploy)
Altos: 0-2 (aceitável)
Médios: 0-5 (tolerável)
Baixos: 0-10+ (informativo)
```

---

## 8. Processo de Teste

### 8.1 Ciclo de Vida do Teste

```
1. Análise (DONE)
   └─ Arquivos mapeados
   └─ Estrutura documentada

2. Design (IN PROGRESS)
   └─ Casos definidos
   └─ Dados preparados

3. Implementação (IN PROGRESS)
   └─ Testes codificados
   └─ Fixtures criadas

4. Execução (PENDING)
   └─ Testes rodados
   └─ Bugs reportados

5. Reporte (PENDING)
   └─ Relatório final
   └─ Sign-off

6. Deploy (PENDING)
   └─ Produção
   └─ Monitoramento
```

### 8.2 Responsabilidades

| Papel | Responsabilidade |
|------|-----------------|
| Analista QA | Definir casos de teste |
| Dev QA | Implementar testes |
| Dev COBOL | Compilar programas |
| DevOps | CI/CD, Relatórios |
| PM | Aprovação, Sign-off |

---

## 9. Gestão de Defeitos

### 9.1 Severidade

```
CRÍTICA: Sistema não funciona
  └─ Ex: Validador retorna código errado

ALTA: Funcionalidade quebrada
  └─ Ex: Campo não valida

MÉDIA: Funcionalidade parcial
  └─ Ex: Mensagem de erro incorreta

BAIXA: Cosmética
  └─ Ex: Texto com typo
```

### 9.2 Ciclo de Vida do Defeito

```
Encontrado → Documentado → Triagem → Corrigido → Verificado → Fechado
```

### 9.3 Exemplo de Bug Report

```
ID: BUG-001
Título: Validador retorna código inválido
Severidade: CRÍTICA
Componente: PF-GAA-L004
Descrição: Entrada "SP1234" retorna 11 ao invés de 21
Reproduzir: python executor_cobol.py validar SP1234
Esperado: Código 21
Obtido: Código 11
Anexos: screenshot.png, log.txt
```

---

## 10. Cronograma de Testes

### 10.1 Timeline

```
Semana 1: Setup
  - [ ] Montar ambiente
  - [ ] Instalar dependências
  - [ ] Compilar COBOL (opcional)

Semana 2: Testes Unitários
  - [ ] Testar Validador
  - [ ] Testar Processador
  - [ ] Testar Empadronização

Semana 3: Testes Integração
  - [ ] Multi-programas
  - [ ] Fluxos completos
  - [ ] Dados reais

Semana 4: Regressão & Deploy
  - [ ] Testes histórico
  - [ ] Aprovação final
  - [ ] Deploy produção
```

### 10.2 Marcos

```
2026-07-09: Testes unitários 100%
2026-07-16: Testes integração 95%+
2026-07-23: Regressão 100%
2026-07-30: Aprovação para deploy
```

---

## 11. Documentação

### 11.1 Documentos Relacionados

```
✓ PLANO_TESTES.md - Visão geral
✓ RESUMO_TESTES.md - Relatório atual
✓ PLANO_EXECUCAO.md - Setup técnico
✓ test_suite.py - Implementação
✓ test_cases.json - Casos estruturados
```

### 11.2 Como Usar Esta Documentação

1. **Para novos testadores**: Ler seções 1-3
2. **Para desenvolvedores**: Ler seções 4-5
3. **Para DevOps**: Ler seções 6-8
4. **Para relatórios**: Ler seções 7, 9-10
5. **Para troubleshooting**: Ler seção 11

---

## 12. Recursos

### 12.1 Ferramentas
- Python 3.13+
- pytest 7.4+
- GnuCOBOL 3.2+
- Git 2.55+

### 12.2 Referências
- GUIA_TESTES_MOBILE.md - Testes mobile
- PLANO_TESTES_COBOL_DETALHADO.md - Este documento
- executor_cobol.py - Executor
- test_suite.py - Suite

### 12.3 Documentação Oficial
- COBOL Specs: ANSI COBOL-85
- GnuCOBOL: http://gnucobol.sourceforge.io
- Micro Focus: Versão 6.1

---

## 13. Conclusão

Este plano fornece cobertura abrangente do sistema COBOL legado Prodesp:

✅ **72 arquivos analisados**
✅ **42 programas mapeados**
✅ **50+ casos de teste definidos**
✅ **Processo documentado**
✅ **Métricas estabelecidas**

**Próxima ação**: Executar suite de testes e reportar resultados.

---

## Anexo A: Checklist de Testes

### Antes de Compilar
- [ ] Todos os testes unitários passam
- [ ] 100% dos casos críticos OK
- [ ] Sem erros de sintaxe
- [ ] Documentação completa

### Após Compilar
- [ ] Binários gerados
- [ ] Testes funcionais 95%+
- [ ] Performance aceitável
- [ ] Regressão 100%

### Antes de Deploy
- [ ] Aprovação QA
- [ ] Aprovação PM
- [ ] Relatório final
- [ ] Plano rollback

---

## Anexo B: Exemplo de Execução

```bash
# 1. Setup
cd c:\Projetos\outros\prodescp\codigo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Testes
python test_suite.py
python test_suite.py --report json

# 3. Relatório
cat TEST_RESULTS_*.json

# 4. Aprovação
# [Reviewer aprova resultados]

# 5. Deploy
# [Deploy para produção]
```

---

**Documento Completo**  
Versão: 1.0  
Data: 2026-07-02  
Aprovado por: QA Lead
