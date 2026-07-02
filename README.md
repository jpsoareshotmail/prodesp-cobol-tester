# Sistema Legado COBOL - Prodesp

Repositório com código-fonte original da aplicação de validação e processamento de dados veiculares da Prodesp (Companhia de Processamento de Dados do Estado de São Paulo).

## Visão Geral

- **Linguagem**: COBOL (Micro Focus COBOL 6.1)
- **Tipo**: Aplicação de lote (batch) para mainframe
- **Funcionalidade Principal**: Validação de placas veiculares, processamento de RENAVAM e empadronização de veículos
- **Tamanho**: 72 arquivos totais (42 programas, 16 bibliotecas, 14 dados)

---

## Estrutura do Projeto

```
.
├── PGM POC cob original/          # Programas COBOL compilados
│   ├── PF-GAA-*.C74              # Validador de placas (16 arquivos)
│   ├── PF-GEV-*.C74              # Empadronização veicular (24 arquivos)
│   ├── PF-GAT-*.C74              # Gestão de autoridades (2 arquivos)
│   ├── MF-*.SEQ                  # Arquivos de dados sequenciais
│   └── [56 arquivos]
│
├── fontes_faltanters/            # Bibliotecas e copybooks
│   ├── SUP_SEECDT00.txt          # Estruturas de data
│   ├── ZPF_LIB_*.txt             # Validadores
│   └── [16 arquivos]
│
├── build.sh                       # Script de compilação automatizado
├── runner.py                      # Executor e simulador (não precisa COBOL)
├── PLANO_EXECUCAO.md             # Plano detalhado de execução
├── INSTALAR_GNUCOBOL.md          # Guia de instalação
└── README.md                      # Este arquivo
```

---

## Início Rápido (Sem COBOL Instalado)

### Analisar o Projeto
```bash
cd "c:\Projetos\outros\prodescp\codigo"
python runner.py
```

Saída esperada:
```
[*] EXECUTOR DE SISTEMA LEGADO COBOL - PRODESP

FASE 1: ANALISE DE ARQUIVOS
  * Programas (.C74):        42
  * Bibliotecas (.txt):      16
  * Arquivos de dados (.SEQ):14

FASE 2: TESTE DE VALIDACAO (Simulado)
  [OK] VALIDA | Placa: AAA0A00 | Codigo: 11 | Mercosul - Sao Paulo
  ...
```

---

## Compilar e Rodar (Com GnuCOBOL)

### 1. Instalar GnuCOBOL

**Windows**:
- Baixe em: https://sourceforge.net/projects/gnucobol/files/
- Execute o instalador
- Reinicie o terminal

**Linux/macOS**:
```bash
# Ubuntu/Debian
sudo apt-get install gnucobol

# macOS
brew install gnu-cobol
```

### 2. Compilar com Build Script
```bash
bash build.sh
```

Opções:
```bash
bash build.sh clean   # Limpar
bash build.sh all     # Build completo
bash build.sh test    # Rodar testes
```

### 3. Executar Programas

```bash
# Validador de placas
./build/bin/PF-GAA-L004.exe

# Processador de banco de dados
./build/bin/PF-GAA-B100-DB.exe

# Listar todos os executáveis
ls build/bin/
```

---

## Compilação Manual

Se preferir compilar diretamente sem o build script:

### Compilar um Programa
```bash
cd "PGM POC cob original"
cobc -x PF-GAA-L004.C74 -o validador.exe
./validador.exe
```

### Compilar com Bibliotecas
```bash
cobc -x PF-GAA-L004.C74 -I../fontes_faltanters -o validador.exe
```

### Compilar Todos
```bash
cd "PGM POC cob original"
for f in *.C74; do
  cobc -x "$f" -o "${f%.C74}.exe"
done
```

---

## Componentes Principais

### 1. **Validador de Placas** (PF-GAA-L004.C74)
Valida formatos de placas veiculares:
- Mercosul (SP)
- Mercosul (Outros estados)
- Antigas (SP)
- Antigas (Outros estados)
- 2 letras (carros e motos)

**Entrada**: Placa com até 10 caracteres
**Saída**: Código de validação (0-34)

### 2. **Processador de Banco de Dados** (PF-GAA-B100-DB.C74)
Manipula tabelas grandes:
- Até 619 KB em um arquivo (PF-GAA-T640-DB.C74)
- Múltiplas estruturas de dados
- Processamento em lote

### 3. **Empadronização Veicular** (PF-GEV-T*.C74)
Processa dados de empadronização:
- 24 arquivos diferentes
- Tabelas de referência (5-335 KB)

---

## Arquivos de Teste

Arquivos .SEQ (dados sequenciais) disponíveis:
- `MF-GAA-AUML01.SEQ` - 8.4 KB
- `MF-GAA-CAPA01.SEQ` - 6.7 KB
- `MF-GAA-COFI02.SEQ` - 20 KB
- E mais 11 arquivos

**Como usar**:
```bash
./build/bin/validador.exe < dados/MF-GAA-AUML01.SEQ
```

---

## Próximos Passos

### Curto Prazo (Esta semana)
1. [x] Analisar estrutura do projeto
2. [ ] Instalar GnuCOBOL
3. [ ] Compilar programas piloto
4. [ ] Testar com dados reais

### Médio Prazo (Este mês)
5. [ ] Documentar estruturas de dados
6. [ ] Criar harness de testes
7. [ ] Pipeline de build CI/CD
8. [ ] Migração progressiva para linguagem moderna

### Longo Prazo
9. [ ] Modernizar código (Java/Python/C#)
10. [ ] Criar APIs REST
11. [ ] Integração com sistemas atuais

---

## Problemas Comuns

### GnuCOBOL não encontrado
```bash
# Verificar instalação
cobc --version

# Se não encontrar, reinstale:
# Windows: https://sourceforge.net/projects/gnucobol/
# Linux: sudo apt-get install gnucobol
```

### Erro de compilação: "Cannot find copybook"
```bash
# Compilar com flag -I para incluir diretório de libs
cobc -x programa.C74 -I../fontes_faltanters -o prog.exe
```

### Programa compila mas não executa
- Verificar se há dados de entrada esperados
- Consultar cabeçalho do programa COBOL
- Usar runner.py para teste simulado

---

## Dependências

| Ferramenta | Versão | Status |
|-----------|--------|--------|
| GnuCOBOL | 3.x+ | Necessário para compilar |
| Python | 3.x | Recomendado (runner.py) |
| Git | 2.x+ | Recomendado |
| Bash | 4.x+ | Necessário para build.sh |

---

## Contato e Suporte

- **Documentação Completa**: Ver `PLANO_EXECUCAO.md`
- **Guia de Instalação**: Ver `INSTALAR_GNUCOBOL.md`
- **Análise do Código**: Executar `python runner.py`
- **Compilação**: Executar `bash build.sh`

---

## Licença

Código original da Prodesp. Acesso via senha fornecida em `Senha Prodesp - Código fonte original.pdf`.

---

## Histórico

| Data | Versão | Descrição |
|------|--------|-----------|
| 2026-07-02 | 1.0 | Setup inicial e análise |
| | | |

---

## Quick Start Checklist

- [ ] Python instalado
- [ ] Executou `python runner.py` com sucesso
- [ ] GnuCOBOL instalado (opcional)
- [ ] Compilou com `bash build.sh` (opcional)
- [ ] Executou primeiro programa
- [ ] Documentação lida

**Você está aqui: Fase de Setup e Análise ✅**

Próximo passo: Instalar GnuCOBOL (veja INSTALAR_GNUCOBOL.md)
