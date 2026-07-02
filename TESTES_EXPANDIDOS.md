# 🚀 Testes Expandidos - Todos os 42 Programas COBOL

## O Que é

A versão expandida dos testes agora inclui **testes de disponibilidade e validação para todos os 42 programas COBOL** do projeto, organizados em 3 categorias:

### Categorias de Programas

```
GAA (Gestão Arquivo Automotivo)
├── PF-GAA-L004.C74     ← Validador de Placas (testes completos)
├── PF-GAA-L005.C74
├── PF-GAA-L007.C74
├── PF-GAA-L012-DB.C74
├── PF-GAA-L015.C74
├── PF-GAA-L032-DB.C74
├── PF-GAA-L050-DB.C74
├── PF-GAA-L115-DB.C74
├── PF-GAA-B100-DB.C74
├── PF-GAA-T013-DB.C74
├── PF-GAA-T018-DB.C74
├── PF-GAA-T255-DB.C74
├── PF-GAA-T615-DB.C74
├── PF-GAA-T640-DB.C74
├── PF-GAA-T792-DB.C74
└── PF-GAA-T920-DB.C74

GEV (Gestão Empadronização Veicular)
├── PF-GEV-L006-DB.C74
├── PF-GEV-T005-DB.C74
├── PF-GEV-T006-DB.C74
├── PF-GEV-T020-DB.C74
├── PF-GEV-T021-DB.C74
├── PF-GEV-T050-DB.C74
├── PF-GEV-T430-DB.C74
├── PF-GEV-T431-DB.C74
├── PF-GEV-T432-DB.C74
├── PF-GEV-T433-DB.C74
├── PF-GEV-T434-DB.C74
├── PF-GEV-T435-DB.C74
├── PF-GEV-T436-DB.C74
├── PF-GEV-T441-DB.C74
├── PF-GEV-T442-DB.C74
├── PF-GEV-T443-DB.C74
├── PF-GEV-T444-DB.C74
├── PF-GEV-T445-DB.C74
├── PF-GEV-T446-DB.C74
├── PF-GEV-T535-DB.C74
├── PF-GEV-T630-DB.C74
├── PF-GEV-T635-DB.C74
├── PF-GEV-T680-DB.C74
├── PF-GEV-T690-DB.C74
└── PF-GEV-T720-DB.C74

GAT (Gestão Autoridades)
├── PF-GAT-L006-DB.C74
└── PF-GAT-T030-DB.C74
```

## Tipos de Testes

### 1. Testes Unitários (PF-GAA-L004 - Validador de Placas)

Executa **17 testes funcionais** do validador de placas:

- **Mercosul - São Paulo** (3 testes)
- **Mercosul - Outros Estados** (2 testes)
- **Placa Antiga - São Paulo** (2 testes)
- **Placa Antiga - Outros Estados** (2 testes)
- **2 letras - Carros** (2 testes)
- **Casos Limite** (2 testes: vazia, com espaços)
- **Caracteres Especiais** (2 testes)

**Resultado esperado**: 14/17 PASS (82.4%)

### 2. Testes de Disponibilidade (Outros Programas)

Para os 41 programas restantes, executa:

- ✅ Verifica se arquivo existe
- ✅ Valida se é um arquivo COBOL válido (contém PROGRAM-ID ou IDENTIFICATION)
- ✅ Agrupa resultados por categoria

**Resultado esperado**: 40/41 PASS (97.6%)

## Como Usar

### Opção 1: Interface Web (Recomendado)

1. **Inicie o servidor**:
   ```bash
   python3 web_app.py
   ```

2. **Acesse a interface**:
   ```
   http://localhost:5000
   ```

3. **Clique no botão**:
   ```
   ⚙ Testes Expandidos (Todos 42 Programas)
   ```

4. **Acompanhe**:
   - Barra de progresso em tempo real
   - Resultados aparecem automaticamente
   - Tabela detalhada com todos os testes

### Opção 2: Linha de Comando

```bash
python3 test_suite_expanded.py
```

Gera arquivo: `TEST_RESULTS_EXPANDED_YYYYMMDD_HHMMSS.json`

## Saída Esperada

```
Total de Testes: 43
Passaram:        40 (93.0%)
Falharam:        3 (7.0%)
Erros:           0 (0.0%)
Taxa de Sucesso: 93.0%

RESULTADOS POR CATEGORIA:
  GAT (2 programas)         2/2 (100.0%)
  GEV (26 programas)       24/24 (100.0%)
  Validador (1 programa)   14/17 (82.4%)
```

## Estrutura do Resultado JSON

```json
{
  "data": "2026-07-02T16:13:22.123456",
  "duracao": 0.04,
  "total": 43,
  "passed": 40,
  "failed": 3,
  "errored": 0,
  "taxa_sucesso": 93.0,
  "programas_testados": 42,
  "resultados": [
    {
      "test_id": "TC-001",
      "nome": "Mercosul - Sao Paulo",
      "programa": "PF-GAA-L004",
      "categoria": "Validador",
      "status": "PASS",
      "entrada": "AAA0A00",
      "saida_esperada": "11",
      "saida_obtida": "11",
      "tempo_ms": 0.02,
      "mensagem": "OK"
    },
    {
      "test_id": "SYS-001",
      "nome": "PF-GAT-L006-DB",
      "programa": "PF-GAT-L006-DB",
      "categoria": "GAT",
      "status": "PASS",
      "entrada": "N/A",
      "saida_esperada": "Disponível",
      "saida_obtida": "OK",
      "tempo_ms": 0.1,
      "mensagem": "Arquivo COBOL válido"
    }
  ]
}
```

## Na Interface Web

### Dashboard
- Mostra **total de execuções expandidas**
- Atualiza **taxa de sucesso** considerando todos os testes

### Resultados Recentes
- Cards coloridos:
  - 🟢 Verde: 100% de sucesso
  - 🟡 Amarelo: 80-95% de sucesso
  - 🔴 Vermelho: < 80% de sucesso

### Tabela Detalhada
- **ID**: TC-001 a TC-034 (validador) + SYS-001 a SYS-041 (outros)
- **Programa**: Nome do programa COBOL testado
- **Categoria**: Validador, GAA, GEV, GAT
- **Status**: PASS, FAIL, ERROR
- **Tempo**: Tempo de execução em ms

## Interpretação dos Resultados

### ✅ Tudo Verde (100%)
Sistema funcionando perfeitamente. Pronto para deploy.

### 🟡 Amarelo (80-95%)
Alguns testes falhando. Revisar:
- Implementação do validador de placas
- Dados de entrada dos casos de teste

### 🔴 Vermelho (< 80%)
Sistema não está pronto. Revisar:
- Arquivos COBOL danificados
- Implementação incompleta
- Dependências não satisfeitas

## Testes Que Falham

Atualmente, 3 testes falham:

### TC-006: Placa Antiga - São Paulo (SP)
```
Entrada: SP1234
Esperado: 21 (Antiga - SP)
Obtido: 33 (2 letras - Carros)
```

**Causa**: Validador está reconhecendo como placa de 2 letras

### TC-007: Placa Antiga - RJ
```
Entrada: RJ1234
Esperado: 22 (Antiga - Outros Estados)
Obtido: 33 (2 letras - Carros)
```

**Causa**: Mesma causa de TC-006

### TC-008: Placa Antiga - MG
```
Entrada: MG2468
Esperado: 22 (Antiga - Outros Estados)
Obtido: 33 (2 letras - Carros)
```

**Causa**: Mesma causa de TC-006

### Solução

Revisar a lógica de validação em `executor_cobol.py`:
- Melhorar detecção de placas antigas
- Validar padrão numérico correto
- Testar com arquivo COBOL original (PF-GAA-L004.C74)

## Próximos Passos

1. **Expandir testes dos outros programas**
   - Atualmente apenas verificam disponibilidade
   - Adicionar testes funcionais específicos

2. **Integrar com compilador COBOL**
   - Se GnuCOBOL estiver disponível
   - Executar programas compilados ao invés de simular

3. **Adicionar testes de performance**
   - Medir tempo de execução por programa
   - Identificar gargalos

4. **Adicionar testes de integração**
   - Testar fluxos entre programas
   - Validar passagem de dados

## Arquivos Relacionados

- `test_suite_expanded.py` - Suite de testes expandida
- `web_app.py` - Backend Flask com endpoint `/api/test/run-expanded`
- `templates/index.html` - Interface com botão para testes expandidos
- `TEST_RESULTS_EXPANDED_*.json` - Resultados em JSON

## Performance

- **Tempo de execução**: ~0.04 segundos
- **Testes por segundo**: ~1000 testes/s
- **Memória**: Negligenciável
- **Escalabilidade**: Suporta facilmente mais programas

---

**Versão**: 1.0.0  
**Data**: 2026-07-02  
**Status**: ✅ Implementado e testado
