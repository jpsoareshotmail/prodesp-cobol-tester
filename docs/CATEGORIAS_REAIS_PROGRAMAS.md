# 📋 Categorias Reais dos 42 Programas COBOL

## Visão Geral

Todos os **42 programas** pertencem ao sistema **DETRAN/PRODESP** - Sistema de Gestão de Veículos e Trânsito. Estão organizados em **3 categorias principais**:

## 🚗 GAA - Gestão Arquivo Automotivo (16 programas)

Sistema de **registro e gestão de veículos** com documentação, placas e dados automotivos.

### Programas de Validação de Placas

| Programa | Objetivo |
|----------|----------|
| **PF-GAA-L004** | Validar formato de placa (Mercosul, Antiga, 2-letras) |
| **PF-GAA-L005** | Consultar dados de veículo por placa |
| **PF-GAA-L007** | Validar documentação (RENAVAM, CRVA) |
| **PF-GAA-L015** | Processar transferência de veículo |

### Programas de Emissão de Documentos

| Programa | Objetivo |
|----------|----------|
| **PF-GAA-L012-DB** | Emitir documentos (CRLV, CRV, DUT) |
| **PF-GAA-T640-DB** | Emissão de CRV para interior |
| **PF-GAA-T255-DB** | Solicitar autorização de CRV |
| **PF-GAA-B100-DB** | Banco de dados de veículos |

### Programas de Verificação e Consulta

| Programa | Objetivo |
|----------|----------|
| **PF-GAA-L032-DB** | Verificação de registro |
| **PF-GAA-L050-DB** | Verificar CIRETRAN e POUPA-TEMPO |
| **PF-GAA-L115-DB** | Consulta de dados |
| **PF-GAA-T013-DB** | Verificar bloqueios e débitos |
| **PF-GAA-T018-DB** | Cadastrar dados de veículo |
| **PF-GAA-T792-DB** | Registro especial |
| **PF-GAA-T920-DB** | Assinatura digital |

---

## 🚙 GEV - Gestão Empadronização Veicular (26 programas)

Sistema de **empadronização e licenciamento** de veículos (CRLV).

### Programas Principais

| Programa | Objetivo |
|----------|----------|
| **PF-GEV-L006-DB** | Gestão de empadronização veicular |
| **PF-GEV-T050-DB** | Tabela de marcas veiculares |
| **PF-GEV-T020-DB** | Tabela de cores |
| **PF-GEV-T021-DB** | Tabela de categorias (Auto, Moto, Caminhão) |
| **PF-GEV-T005-DB** | Tabela de combustíveis (Gasolina, Diesel, GNV) |
| **PF-GEV-T430-DB** | Tabela de circunscrições |

### Programas de Seleção de Placas

| Programa | Objetivo |
|----------|----------|
| **PF-GEV-T431-DB** | Processar seleção de placa |
| **PF-GEV-T432-DB** | Validar placa selecionada |
| **PF-GEV-T433-DB** | Confirmar seleção |
| **PF-GEV-T434-DB** | Cancelar seleção de placa |
| **PF-GEV-T435-DB** | Alterar seleção |
| **PF-GEV-T436-DB** | Histórico de seleções |

### Programas de Licenciamento

| Programa | Objetivo |
|----------|----------|
| **PF-GEV-T441-DB** | Fase 1 licenciamento zero KM |
| **PF-GEV-T442-DB** | Fase 2 licenciamento |
| **PF-GEV-T443-DB** | Fase 3 licenciamento |
| **PF-GEV-T444-DB** | Cancelamento de licenciamento |
| **PF-GEV-T445-DB** | Renovação de licenciamento |
| **PF-GEV-T446-DB** | Análise de licenciamento |

### Programas de Portal DETRAN

| Programa | Objetivo |
|----------|----------|
| **PF-GEV-T535-DB** | Integração com portal |
| **PF-GEV-T630-DB** | Sincronização de dados |
| **PF-GEV-T635-DB** | Validação de portal |
| **PF-GEV-T680-DB** | Licenciamento zero KM - Portal |
| **PF-GEV-T690-DB** | Processamento portal |
| **PF-GEV-T720-DB** | Consultas portal |

---

## 👮 GAT - Gestão Autoridades de Trânsito (2 programas)

Sistema de **gestão de autoridades** e **penalidades de trânsito**.

| Programa | Objetivo |
|----------|----------|
| **PF-GAT-L006-DB** | Gestão de autoridades (DETRAN, polícia) |
| **PF-GAT-T030-DB** | Tabela de penalidades e infrações |

---

## 📊 Resumo por Domínio

### Temas Principais

```
1. PLACAS (9 programas)
   ├─ Validação de formato
   ├─ Seleção de placa
   ├─ Sorteio de placas
   └─ Personalização

2. VEÍCULOS (15 programas)
   ├─ Registro e cadastro
   ├─ Empadronização
   ├─ Dados técnicos
   └─ Transferência

3. DOCUMENTOS (8 programas)
   ├─ CRLV (Certificado Registro)
   ├─ CRV (Certificado Registro Veicular)
   ├─ DUT (Documento Único)
   └─ Assinatura digital

4. INFRAÇÕES (2 programas)
   ├─ Tabela de penalidades
   └─ Gestão de autoridades

5. TABELAS AUXILIARES (8 programas)
   ├─ Marcas
   ├─ Cores
   ├─ Combustíveis
   ├─ Categorias
   ├─ Estados (UF)
   ├─ Circunscrições
   └─ Tipos de documento
```

---

## 🎯 Campos Comuns em Todos os Programas

Praticamente todos os programas usam:

```
Entrada:
  ✓ Placa (ou código identificador)
  ✓ Documentos (RENAVAM, CRVA, CRVE)
  ✓ Dados veículo (marca, modelo, ano)
  ✓ Dados proprietário (CPF, CNPJ)
  ✓ UF (Estado)

Saída:
  ✓ Código de retorno (0-99)
  ✓ Mensagem descritiva
  ✓ Dados validados
  ✓ Status (válido/inválido)
```

---

## 📈 Distribuição

| Categoria | Programas | % | Foco Principal |
|-----------|-----------|---|-----------------|
| **GEV** | 26 | 62% | Empadronização e Licenciamento |
| **GAA** | 16 | 38% | Registro e Gestão Automotiva |
| **GAT** | 2 | 5% | Autoridades e Penalidades |

---

## 💾 Tipos de Dados Processados

Todos os programas trabalham com:

1. **Dados Veicular**
   - Placa (Mercosul, Antiga, 2 letras)
   - RENAVAM, CRVA, CRVE
   - Marca, Modelo, Ano
   - Cor, Combustível, Categoria

2. **Dados Administrativo**
   - CPF/CNPJ Proprietário
   - Endereço, Cidade, UF
   - Telefone, Email

3. **Dados Transacional**
   - Transferência
   - Licenciamento
   - Empadronização
   - Seleção de placa

4. **Dados Regulatório**
   - Infrações
   - Penalidades
   - Bloqueios
   - Débitos

---

## 🔗 Relação entre Programas

```
PF-GAA-L004 (Validar Placa)
    ↓
PF-GAA-L005 (Consultar Veículo)
    ↓
PF-GEV-L006-DB (Empadronizar)
    ↓
PF-GEV-T680-DB (Licenciar)
    ↓
PF-GEV-T690-DB (Portal DETRAN)
```

---

## ✅ Conclusão

**Todos os 42 programas** são especializados em **gestão de veículos e trânsito**, divididos em:

- **GAA**: Gestão do arquivo automotivo (registros, documentos, validações)
- **GEV**: Gestão de empadronização e licenciamento (CRLV, placas, portal)
- **GAT**: Gestão de autoridades e penalidades (DETRAN, infrações)

Cada categoria tem objetivos bem definidos e integrados no fluxo maior de gestão veicular do estado de São Paulo.

---

**Versão**: 1.0  
**Data**: 2026-07-02  
**Sistema**: DETRAN/PRODESP - Gestão Veicular SP
