# Problemas no Render - Solução

Se a aplicação no Render não está listando programas ou fazendo testes.

## Problema: Programas não aparecem

### Causas Possíveis

1. **Diretório PGM POC cob original não está no GitHub**
   - Arquivos .C74 não foram uploaded
   - Git pode estar ignorando pasta

2. **Caminho relativo incorreto**
   - Render roda em diretório diferente
   - Código procura em local errado

3. **Permissões de arquivo**
   - Arquivos não conseguem ser lidos

## Solução Rápida

### Passo 1: Verificar o que está no GitHub

```bash
cd c:\Projetos\outros\prodescp\codigo

# Ver arquivos versionados
git ls-files | grep "\.C74" | head -10

# Se não aparecer nada, arquivos não estão no GitHub!
```

### Passo 2: Adicionar Arquivos COBOL ao GitHub

```bash
# Verificar status
git status

# Se "PGM POC cob original" aparece como untracked:
git add "PGM POC cob original/"

# Ou adicionar tudo
git add .

# Commit
git commit -m "Adicionar programas COBOL"

# Push
git push
```

### Passo 3: Forçar Rebuild no Render

1. Acesse: https://dashboard.render.com
2. Clique seu serviço
3. Vá para "Settings"
4. Clique "Delete service" (não se preocupe, recria)
5. Ou clique "Redeploy" para novo build

### Passo 4: Testar

Aguarde 2-3 minutos e acesse:
https://prodesp-cobol-tester.onrender.com

## Solução Detalhada

### 1. Verificar Git

```bash
# Quantidade de arquivos Python
git ls-files | grep "\.py$" | wc -l
# Deve mostrar: 12

# Quantidade de programas COBOL
git ls-files | grep "\.C74$" | wc -l
# Deve mostrar: 42

# Se 0, arquivos não estão versionados!
```

### 2. .gitignore Bloqueando?

Verificar `.gitignore`:

```bash
# Ver conteúdo
cat .gitignore

# Se tiver algo como:
# PGM POC cob original/
# Ou:
# *.C74

# Remova essas linhas!
```

### 3. Força adicionar (se necessário)

```bash
# Adicionar mesmo se em gitignore
git add -f "PGM POC cob original/"

git commit -m "Força adicionar programas COBOL"

git push
```

### 4. Verificar Logs do Render

No Render Dashboard:

1. Clique seu serviço
2. Clique "Logs"
3. Procure por:
   - `ModuleNotFoundError` - falta módulo Python
   - `FileNotFoundError` - arquivo faltando
   - `No such file or directory` - caminho errado

### 5. Corrigir Caminhos (se necessário)

Se erro é "PGM POC cob original not found", edite `web_app.py`:

```python
# Linha com o caminho:
codigo_dir = Path("PGM POC cob original")

# Se não funcionar, tente caminho absoluto:
codigo_dir = Path(__file__).parent / "PGM POC cob original"
```

## Checklist de Problemas

### ❌ Aplicação mostra "Nenhum programa"

Solução:
- [ ] Verificar git ls-files | grep C74
- [ ] Se vazio, arquivos não estão no GitHub
- [ ] Fazer git add "PGM POC cob original/"
- [ ] git push
- [ ] Redeploy no Render

### ❌ Erro 500 ao tentar listar

Solução:
- [ ] Ver logs do Render
- [ ] Procurar "FileNotFoundError"
- [ ] Verificar caminho do diretório
- [ ] Testar localmente antes

### ❌ Testes não executam

Solução:
- [ ] mock_data_expanded.py está no GitHub?
- [ ] program_descriptions.py está no GitHub?
- [ ] executor_cobol.py está no GitHub?
- [ ] Todos no git ls-files?

### ❌ Código fonte não abre

Solução:
- [ ] Mesmos arquivos .C74 do problema acima
- [ ] Senha está correta?
- [ ] Tente com arquivo diferente

## Script de Diagnóstico

Execute localmente para debugar:

```bash
# Criar script de teste
python startup.py

# Deve mostrar:
# ✓ PGM POC cob original
# ✓ Total de programas: 42
# ✓ Todos módulos carregados
```

## Deploy Completo (Zero)

Se nada funciona, faça deploy do zero:

```bash
# 1. Certificar que GitHub tem tudo
git status
# Deve mostrar "nothing to commit"

# Se não:
git add .
git commit -m "Preparar para deploy"
git push

# 2. Render
# Dashboard → Settings → Delete service
# Clique New Web Service novamente
# Será um novo deploy

# 3. Testar
# https://prodesp-cobol-tester.onrender.com
```

## URLs Úteis

- GitHub: https://github.com/seu-usuario/prodesp-cobol-tester
- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs

## Verificar Diretório Local

```bash
# Listar programas localmente
ls "PGM POC cob original/" | grep "\.C74" | wc -l

# Deve mostrar: 42

# Se mostrar 0 ou erro:
# Diretório não existe ou está vazio!
```

## Render Rebuild

Forçar novo build:

1. Dashboard
2. Seu serviço
3. Manual Redeploy
4. Ou push novo commit no GitHub (automático)

## Último Recurso

Se nada funcionar:

1. Delete service no Render
2. Delete repositório no GitHub
3. Comece do zero:
   ```bash
   git init
   git add .
   git commit -m "Inicial"
   git remote add origin https://github.com/usuario/nome.git
   git push -u origin main
   ```
4. Crie novo serviço no Render

---

**Se mesmo assim não funcionar, envie os logs do Render!**

Render Dashboard → Serviço → Logs (copie últimas linhas)

---

**Versão**: 1.0  
**Data**: 2026-07-03  
**Status**: ✅ Troubleshooting
