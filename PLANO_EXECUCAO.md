# 🚀 Plano de Execução - Sistema Legado COBOL Prodesp

## Status Atual
- **Arquivos COBOL**: 56 programas extraídos ✅
- **Arquivos de Suporte**: 16 fontes de biblioteca extraídas ✅
- **Compilador COBOL**: ❌ Não instalado
- **Ambiente Java**: ✅ Java 25.0.2 LTS disponível
- **Python**: ✅ Python 3.13.14 disponível

---

## Estratégia de Execução

### Opção 1: Usar GnuCOBOL (Recomendado - Gratuito)
**Características**:
- Compilador COBOL open-source
- Suporta sintaxe COBOL padrão
- Funciona em Windows (via MinGW)
- Sem licença necessária

**Instalação**:
```bash
# Via Chocolatey (se disponível)
choco install gnucobol

# Ou download direto
# https://sourceforge.net/projects/gnucobol/files/
```

**Próximos passos após instalação**:
1. Compilar programa piloto: `PF-GAA-L004.C74`
2. Linkar com bibliotecas (SUP_SEECDT00.txt, etc)
3. Executar com dados de teste

---

### Opção 2: Wrapper em Java (Alternativa)
Criar um executor Java que:
- Lê os arquivos COBOL
- Interpreta estruturas de dados
- Simula validação de placas
- Executa sem compilador COBOL

**Vantagem**: Funciona imediatamente
**Desvantagem**: Não executa o código original

---

### Opção 3: Docker Container
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y gnucobol
COPY ./codigo /app
WORKDIR /app
```

---

## Componentes Principais a Executar

### 1. **Validador de Placas** (PF-GAA-L004)
```cobol
OBJETIVO: Validar placas veiculares
ENTRADA: LC-PLACA (10 caracteres)
SAÍDA: LC-RETORNO (códigos 00-34)
STATUS: Pronto para compilar
```

**Códigos de retorno**:
- 00: Placa inválida
- 11: Mercosul - São Paulo
- 12: Mercosul - Outros estados
- 21: Antiga - São Paulo
- 22: Antiga - Outros estados
- 33: 2 letras - Carros
- 34: 2 letras - Motos

### 2. **Estruturas de Dados** (SUP_SEECDT00.txt)
Copybook com múltiplas interpretações de data:
- CCYYMMDD (8 dígitos)
- MMDDYY (6 dígitos)
- DD/MM/YYYY (formatado)

### 3. **Bibliotecas de Validação** (Faltam)
- `ZPF_LIB_DIGITCHECK_009.txt`: Validação de dígitos
- `ZPF_LIB_DATAS_026.txt`: Validação de datas
- `ZPF_LIB_CONVERTCHARACTER_005.txt`: Conversão de caracteres

---

## Arquivos de Dados Disponíveis

| Arquivo | Tipo | Tamanho | Descrição |
|---------|------|---------|-----------|
| MF-GAA-AUML01.SEQ | Dados | 8.4 KB | Anuidades |
| MF-GAA-CAPA01.SEQ | Dados | 6.7 KB | Capacidades |
| MF-GAA-COFI*.SEQ | Dados | 20 KB | Configurações financeiras |
| MF-GAA-EMIS*.SEQ | Dados | 13 KB | Emissões |
| MF-GAA-RENA*.SEQ | Dados | 8 KB | Dados RENAVAM |
| PF-GAA-T*.C74 | Banco | até 619 KB | Tabelas grandes |

---

## Próximas Ações

### Imediato (Hoje)
- [ ] Instalar GnuCOBOL
- [ ] Compilar PF-GAA-L004.C74
- [ ] Testar com dados de amostra

### Curto prazo (Esta semana)
- [ ] Compilar todos os programas GAA
- [ ] Criar harness de testes
- [ ] Documentar estruturas de dados

### Médio prazo (Este mês)
- [ ] Pipeline de build automatizado
- [ ] Testes de integração
- [ ] Documentação técnica

---

## Recursos Necessários

### Software
- GnuCOBOL 3.x+ (Windows/MinGW)
- Editor de texto (VS Code com suporte COBOL)

### Hardware
- ~500 MB espaço livre
- 2 GB RAM mínimo

### Conhecimento
- Sintaxe COBOL
- Estruturas de dados
- Processamento em lote

---

## Comandos de Referência (Após instalar GnuCOBOL)

```bash
# Compilar um programa
cobc -x PF-GAA-L004.C74 -o pgm-placa.exe

# Compilar com bibliotecas
cobc -x PF-GAA-L004.C74 -I. -o pgm-placa.exe

# Executar
./pgm-placa.exe

# Compilar para biblioteca
cobc -c SUP_SEECDT00.txt

# Debug
cobc -x -g PF-GAA-L004.C74
```

---

## Status de Blockers

| Blocker | Severidade | Solução |
|---------|-----------|---------|
| GnuCOBOL não instalado | 🔴 Crítico | Instalar via apt/choco/manual |
| Bibliotecas compartilhadas incompletas | 🟡 Alta | Localizadas em `fontes_faltanters/` |
| Sem dados de teste | 🟡 Alta | Usar arquivos .SEQ disponíveis |
| Falta de documentação | 🟢 Média | Gerar dinamicamente |

---

## Ambiente Confirmado

✅ **Java 25.0.2 LTS** - Pode ser usado para wrapper
✅ **Python 3.13.14** - Para ferramentas auxiliares
✅ **Git 2.55.0** - Para versionamento
❌ **GnuCOBOL** - Precisa instalar
❌ **Chocolatey** - Pode instalar manualmente

---

## Conclusão

**Recomendação**: Instalar GnuCOBOL e compilar o programa piloto de validação de placas.
**Tempo estimado**: 30 min (download + instalação + primeiro build)
**Resultado esperado**: Executável funcional com dados de teste

**Quer prosseguir com a instalação do GnuCOBOL?**
