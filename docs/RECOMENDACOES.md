# Recomendacoes - Migracao COBOL Unisys 74 / DMS → IBM z/OS COBOL 6.5 / DB2

## 1. Ambiente de Teste

### 1.1 Situacao Atual (GnuCOBOL local)
- **Compilador:** GnuCOBOL 3.1.2 (open source, Windows)
- **Banco:** Stubs (sem banco real)
- **CICS:** Comentado/stub
- **Resultado:** 26 de 42 programas compilam (62%) — valida logica de negocio

### 1.2 Proximo Passo Recomendado: IBM Wazi as a Service
- z/OS na nuvem IBM Cloud com COBOL 6.5, DB2, CICS reais
- Trial de 30 dias disponivel
- Permite compilar e executar com o ambiente alvo real
- URL: https://www.ibm.com/products/wazi-as-a-service

### 1.3 Alternativa: Acesso ao Mainframe da Prodesp
- Solicitar acesso ao z/OS via Zowe CLI ou IBM Developer for z/OS (IDz)
- Submeter jobs de compilacao (JCL) remotamente
- Exige liberacao de acesso e ambiente de homologacao

---

## 2. Compilacao Final (z/OS)

### 2.1 Requisitos para compilar no z/OS com COBOL 6.5
| Item | Descricao |
|------|-----------|
| Compilador | IBM Enterprise COBOL for z/OS 6.5 |
| Pre-compilador DB2 | DB2 Precompiler (DSNHPC) |
| CICS Translator | CICS TS 5.x ou 6.x |
| Linkeditor | Binder (IEWL) |
| Copybooks | PDS com todas as COPY libraries |
| DDL do banco | Scripts CREATE TABLE para DB2 |
| CICS CSD | Definicoes de transacoes/programas |

### 2.2 Ordem de compilacao no z/OS
1. CICS Translator (EXEC CICS → CALL)
2. DB2 Precompiler (EXEC SQL → CALL)
3. COBOL Compiler (fonte → object)
4. Linkeditor (object → load module)

### 2.3 JCL modelo para compilacao
```
//COMPILE  EXEC IGYWCL,PARM.COBOL='RENT,APOST,MAP'
//COBOL.SYSIN  DD DSN=SYS1.SOURCE(FGAA004),DISP=SHR
//COBOL.SYSLIB DD DSN=SYS1.COPYLIB,DISP=SHR
//LKED.SYSLMOD DD DSN=SYS1.LOADLIB(FGAA004),DISP=SHR
```

---

## 3. Testes de Validacao

### 3.1 Estrategia de Teste Recomendada

| Fase | Ambiente | Objetivo | Ferramenta |
|------|----------|----------|-----------|
| 1. Logica pura | GnuCOBOL (local) | Comparar original vs convertido | COBOL Tester (este projeto) |
| 2. Compilacao | z/OS (Wazi/mainframe) | Verificar compilacao com COBOL 6.5 | JCL de compilacao |
| 3. Unitario | z/OS ou GnuCOBOL | Testar cada programa isolado | COBOL Check / stubs |
| 4. Integracao | z/OS com DB2 | Testar com banco real | Dados de homologacao |
| 5. Regressao | z/OS com CICS | Testar transacoes online | CICS TS test |

### 3.2 Casos de Teste Prioritarios

| Programa | Funcao | Teste |
|----------|--------|-------|
| FGAA004 (PF-GAA-L004) | Validacao de placas | Testar todas as faixas (SP, outros estados, Mercosul) |
| FGAA012D (PF-GAA-L012-DB) | Emissao documentos | Testar com registros de furto/alerta |
| FGAA032D (PF-GAA-L032-DB) | Verificacao registro | Testar existencia/inexistencia |
| OGEV441D (PF-GEV-T441-DB) | Licenciamento Zero KM | Fluxo completo de licenciamento |
| PGAA100D (PF-GAA-B100-DB) | Processamento batch | Volume de dados |

### 3.3 Validacao de Diferencas Detectadas

Ao comparar Original (v6.1/2026) vs Convertido (v4.1/2024):
- **5 diferencas de faixa de placas** — patches de 2025/2026 nao presentes no convertido
- Validar se o convertido deve ter os patches aplicados ANTES da migracao

---

## 4. Riscos e Mitigacoes

| Risco | Impacto | Mitigacao |
|-------|---------|-----------|
| Diferenca de encoding (EBCDIC vs ASCII) | Dados corrompidos | Converter dados de teste para EBCDIC |
| COMP fields com tamanho diferente | Resultados errados | Testar com dados de boundary (max/min) |
| Object COBOL (INVOKE) nao suportado | 5 programas nao compilam | Reescrever como CALL padrao |
| DMS → DB2 mapeamento incompleto | Queries falham | Validar DDL com DBA |
| CICS containers vs commarea | Dados perdidos | Mapear containers para commarea |
| Copybooks faltantes | Compilacao falha | Solicitar PDS completo ao cliente |

---

## 5. Pendencias para Compilacao Total (16 programas restantes)

### 5.1 Programas com Object COBOL (INVOKE)
- OGEV050D, OGEV433D, OGEV443D, OGAA018D, OGAA640D
- **Acao:** Reescrever INVOKE como CALL padrao (manual)
- **Responsavel:** Equipe de conversao

### 5.2 Programas com REDEFINES posicional
- OGAA615D, OGAA792D, OGEV005D, OGEV021D, PGAA100D
- **Acao:** Ajustar posicao do REDEFINES nos copybooks
- **Responsavel:** Automatizavel (melhorar gen_real_copybooks.py)

### 5.3 Programas com IF desbalanceado
- OGAA255D, OGAA920D, FGAT006D, OGAA013D
- **Acao:** Melhorar preprocessor para fechar IFs ao comentar EXEC SQL
- **Responsavel:** Automatizavel (melhorar sql_preprocessor.py)

### 5.4 Programas complexos (muitos erros)
- OGEV630D, OGEV635D, OGEV680D, OGAA792D
- **Acao:** Revisao manual do fonte convertido
- **Responsavel:** Analista COBOL senior

---

## 6. Entregaveis Recomendados

| # | Entregavel | Status |
|---|-----------|--------|
| 1 | Interface web de comparacao (Original vs Convertido) | Pronto |
| 2 | Pre-processador SQL/CICS automatico | Pronto |
| 3 | Copybooks inferidos (2071 campos) | Pronto |
| 4 | Documentacao de mudancas (MUDANCAS_CONVERSAO.md) | Pronto |
| 5 | Scripts de compilacao em lote | Pronto |
| 6 | Relatorio de diferencas de comportamento | Pronto (via /api/comparar-placa) |
| 7 | JCL de compilacao para z/OS | Pendente (precisa de ambiente) |
| 8 | Dados de teste para DB2 | Pendente (precisa de DDL) |
| 9 | Plano de teste de regressao completo | Pendente |

---

## 7. Proximos Passos Imediatos

1. **Solicitar copybooks reais** da Prodesp (PDS SYS1.COPYLIB ou equivalente)
   - Com eles, os 16 programas restantes provavelmente compilam todos
   
2. **Solicitar DDL das tabelas** (CREATE TABLE do DMS/DB2)
   - Permite criar mock de banco local para testes unitarios

3. **Avaliar IBM Wazi** para compilacao final com COBOL 6.5

4. **Definir se os patches de 2025/2026** (faixas de placa UDA-UGV, UOG-USB, TIO-TMJ)
   devem ser aplicados no convertido ANTES ou DEPOIS da migracao

5. **Planejar teste de regressao** com dados reais em ambiente de homologacao
