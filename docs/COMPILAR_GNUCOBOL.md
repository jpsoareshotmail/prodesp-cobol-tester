# Compilar GnuCOBOL a partir do Código-Fonte

## Situação Atual
Você baixou o **código-fonte** do GnuCOBOL em `C:\gnucobol-3.2_win\gnucobol-3.2_win`, mas ainda precisa **compilar o compilador** para gerar os binários executáveis (`cobc.exe`).

---

## Opção 1: Usar Binário Pré-compilado (Recomendado - Mais Rápido)

Ao invés de compilar do zero, baixe um binário pré-compilado:

### Windows
**Versão pré-compilada com MinGW**:
https://sourceforge.net/projects/gnucobol/files/GnuCOBOL%20Binaries%20for%20Windows/

Procure por:
- `gnucobol-3.2-bin-mingw.zip` ou similar

**Passos**:
1. Baixe o arquivo .zip
2. Extraia em um local simples (ex: `C:\gnucobol-bin`)
3. Adicione ao PATH:
   ```powershell
   $env:Path += ";C:\gnucobol-bin\bin"
   ```

4. Verifique:
   ```bash
   cobc --version
   ```

---

## Opção 2: Compilar com MSYS2 (Windows)

Se preferir compilar localmente:

### Passo 1: Instalar MSYS2
- Baixe: https://www.msys2.org/
- Execute instalador
- Abra "MSYS2 MinGW 64-bit"

### Passo 2: Instalar Ferramentas
```bash
pacman -S mingw-w64-x86_64-gcc
pacman -S mingw-w64-x86_64-make
pacman -S mingw-w64-x86_64-pkg-config
```

### Passo 3: Compilar GnuCOBOL
```bash
cd C:/gnucobol-3.2_win/gnucobol-3.2_win

./configure --prefix=/opt/gnucobol \
  --with-curses=ncursesw \
  --without-db

make
make install
```

**Tempo**: 30-60 minutos (primeira vez)

---

## Opção 3: Usar Docker (Mais Fácil)

Se não quiser instalar nada:

### Dockerfile
```dockerfile
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y gnucobol && \
    apt-get clean

WORKDIR /cobol
COPY . .

ENTRYPOINT ["cobc"]
```

### Build
```bash
docker build -t gnucobol:3.2 .
```

### Use
```bash
docker run -v $(pwd):/cobol gnucobol:3.2 -x programa.C74 -o programa.exe
```

---

## Opção 4: Usar Alternativa - TinyCOBOL ou Simulador

Se compilar for muito complexo, use o **simulador Python** que já criamos:

```bash
cd c:\Projetos\outros\prodescp\codigo
python runner.py
```

Isso **não precisa** de compilador COBOL.

---

## Recomendação

### Se você tem 15 minutos:
**→ Opção 1** (Baixar binário pré-compilado)

### Se você tem 60 minutos:
**→ Opção 2** (Compilar com MSYS2)

### Se quer evitar complicações:
**→ Opção 3** (Docker) ou **→ Opção 4** (Simulador Python)

---

## Próximos Passos

Após conseguir `cobc` funcionando:

```bash
cd c:\Projetos\outros\prodescp\codigo

# Compilar programa piloto
cobc -x "PGM POC cob original\PF-GAA-L004.C74" -o validador.exe

# Ou compilar tudo
bash build.sh
```

---

## Suporte Rápido

Se tiver problemas, consulte:
- `README.md` - Documentação geral
- `INSTALAR_GNUCOBOL.md` - Guia original (para download de binários)
- `runner.py` - Simulador (funciona sem compilador)

Quer que eu ajude com uma das opções acima?
