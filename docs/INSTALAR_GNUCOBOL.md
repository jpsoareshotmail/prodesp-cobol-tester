# Instalação do GnuCOBOL para Rodar o Sistema Prodesp

## Visão Geral
O **GnuCOBOL** é um compilador COBOL open-source que permite rodar o código original da Prodesp.

---

## Windows 11 Enterprise (Seu Sistema)

### Opção 1: Instalador Direto (Recomendado)
**Tempo**: ~10 minutos

1. **Baixar o instalador**
   - Acesse: https://sourceforge.net/projects/gnucobol/files/
   - Baixe a versão mais recente para Windows (x64)
   - Procure por: `gnucobol-X.X-setup.exe`

2. **Executar instalador**
   ```
   gnucobol-3.2-setup.exe
   ```
   - Clique "Next" nas telas de instalação
   - Deixe o caminho padrão: `C:\Program Files\GnuCOBOL`
   - Marque "Add to PATH" (importante!)

3. **Verificar instalação**
   ```bash
   cobc --version
   ```

4. **Compilar programa piloto**
   ```bash
   cd "c:\Projetos\outros\prodescp\codigo"
   cobc -x "PGM POC cob original\PF-GAA-L004.C74" -o validador.exe
   ```

5. **Executar**
   ```bash
   ./validador.exe
   ```

---

### Opção 2: Via Chocolatey (Se tiver instalado)
**Tempo**: ~5 minutos

```powershell
choco install gnucobol
```

Depois verificar:
```bash
cobc --version
```

---

### Opção 3: Compilar do Código-Fonte (Avançado)
**Tempo**: ~30 minutos + download

```bash
# Pré-requisitos
git clone https://github.com/GnuCOBOL/GnuCOBOL.git
cd GnuCOBOL
./configure
make
make install
```

---

## macOS

```bash
brew install gnu-cobol
```

---

## Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install gnucobol
```

---

## Testes Após Instalação

### 1. Verificar versão
```bash
cobc --version
```

Saída esperada:
```
GnuCOBOL 3.2 (build date: ...)
...
```

### 2. Compilar programa de teste
```bash
cd "c:\Projetos\outros\prodescp\codigo\PGM POC cob original"

# Compilar PF-GAA-L004 (Validador de placas)
cobc -x PF-GAA-L004.C74 -o test-placa.exe
```

### 3. Executar testes
```bash
python ../runner.py
```

---

## Solução de Problemas

### "cobc: command not found"
- **Causa**: Não está no PATH
- **Solução**: 
  1. Reinstalar GnuCOBOL
  2. Marcar "Add to PATH" durante instalação
  3. Reiniciar terminal/PowerShell

### "COBOL syntax error"
- **Causa**: Versão incompatível ou código inválido
- **Solução**: Verificar versão do COBOL no arquivo:
  ```cobc
  000000* VERSION  6.1   ; SAVED 20260508 12:02:53  |6.0
  ```

### Erro ao linkar bibliotecas
- **Causa**: Copybooks faltando
- **Solução**: Compilar com flag `-I`:
  ```bash
  cobc -x -I. PF-GAA-L004.C74
  ```

---

## Próximos Passos

### 1. Compilar Todos os Programas
```bash
cd "c:\Projetos\outros\prodescp\codigo\PGM POC cob original"

for f in *.C74; do
  cobc -x "$f" -o "${f%.C74}.exe" 2>&1 | grep -i error
done
```

### 2. Compilar Bibliotecas Compartilhadas
```bash
cd "c:\Projetos\outros\prodescp\codigo"

# Compilar copybooks
cobc -c fontes_faltanters/SUP_SEECDT00.txt
cobc -c fontes_faltanters/SUP_SEECDTPD.txt
```

### 3. Executar com Dados de Teste
```bash
cd "PGM POC cob original"

# Usar arquivos .SEQ como entrada
./test-placa.exe < ../MF-GAA-AUML01.SEQ
```

---

## Estrutura de Compilação Recomendada

```
codigo/
├── build/                    # Saída compilada
│   ├── bin/                 # Executáveis
│   │   ├── validador-placa.exe
│   │   ├── processador-dados.exe
│   │   └── ...
│   └── lib/                 # Bibliotecas compiladas
│       ├── SUP_SEECDT00.o
│       └── ...
│
├── Makefile                 # Automação de build
├── run_tests.sh            # Script de testes
└── compile_all.sh          # Compilar tudo
```

---

## Makefile Exemplo

```makefile
COBC = cobc
COBC_FLAGS = -x -I.
SRC_DIR = PGM\ POC\ cob\ original
FALTANTES = fontes_faltanters
BIN_DIR = build/bin
LIB_DIR = build/lib

all: prepare $(BIN_DIR)/validador.exe

prepare:
	mkdir -p $(BIN_DIR) $(LIB_DIR)

$(BIN_DIR)/validador.exe: $(SRC_DIR)/PF-GAA-L004.C74
	$(COBC) $(COBC_FLAGS) $< -o $@

clean:
	rm -rf $(BIN_DIR) $(LIB_DIR)

run: $(BIN_DIR)/validador.exe
	./$(BIN_DIR)/validador.exe
```

---

## Status Esperado Após Instalação

| Etapa | Status | Comando |
|-------|--------|---------|
| Instalação | ✅ | `cobc --version` |
| Compilação | ✅ | `cobc -x *.C74 -o prog.exe` |
| Execução | ✅ | `./prog.exe` |
| Testes | ✅ | `python runner.py` |

---

## Recursos Adicionais

- **Documentação Official**: https://www.gnu.org/software/cobol/
- **GitHub**: https://github.com/GnuCOBOL/GnuCOBOL
- **Manual**: https://gnucobol.sourceforge.io/doc/gnucobol.html
- **Exemplos**: https://github.com/GnuCOBOL/GnuCOBOL/tree/master/examples

---

## Próximas Ações

1. **[URGENTE]** Instalar GnuCOBOL
2. Compilar programa piloto
3. Testar com dados reais
4. Documentar estrutura de dados
5. Criar pipeline de build

**Pronto? Execute:**
```bash
cd "c:\Projetos\outros\prodescp\codigo"
python runner.py
```
