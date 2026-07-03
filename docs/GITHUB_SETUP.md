# Como Adicionar Projeto no GitHub

Guia completo passo a passo.

## Passo 1: Criar Conta GitHub (se não tiver)

1. Acesse https://github.com
2. Clique em **Sign up**
3. Complete com:
   - Email
   - Senha
   - Username (seu nome de usuário)
4. Confirme email

## Passo 2: Criar Novo Repositório

1. Após login, clique em **+** (canto superior direito)
2. Selecione **New repository**
3. Preencha:
   - **Repository name**: `prodesp-cobol-tester`
   - **Description**: `Sistema de Testes COBOL - Prodesp`
   - **Public** ou **Private** (escolha sua preferência)
   - **NÃO** marque "Initialize this repository with..."
4. Clique **Create repository**

## Passo 3: Instalar Git Localmente

Se ainda não tem Git instalado:

1. Acesse https://git-scm.com/download
2. Baixe a versão para Windows
3. Instale com configurações padrão
4. Abra Git Bash (Terminal Git)

## Passo 4: Configurar Git

Abra **Git Bash** ou **PowerShell** na pasta do projeto:

```bash
# Configurar nome
git config --global user.name "Seu Nome"

# Configurar email (use o mesmo do GitHub)
git config --global user.email "seu.email@exemplo.com"

# Verificar configuração
git config --global --list
```

## Passo 5: Inicializar Repositório Local

Na pasta `c:\Projetos\outros\prodescp\codigo`:

```bash
# Entrar na pasta
cd c:\Projetos\outros\prodescp\codigo

# Inicializar git
git init

# Ver status
git status
```

## Passo 6: Adicionar Arquivos

```bash
# Adicionar todos os arquivos
git add .

# Verificar o que será commitado
git status
```

## Passo 7: Criar Primeiro Commit

```bash
git commit -m "Inicial: Sistema de Testes COBOL Prodesp"
```

## Passo 8: Conectar ao GitHub

Copie o comando do GitHub (aparece depois de criar repositório):

```bash
git remote add origin https://github.com/seu-usuario/prodesp-cobol-tester.git
git branch -M main
git push -u origin main
```

Substitua `seu-usuario` pelo seu username do GitHub.

## Passo 9: Autenticar no GitHub

### Opção A: Token (Recomendado para 2024+)

1. No GitHub, vá em **Settings** → **Developer settings** → **Personal access tokens**
2. Clique **Generate new token**
3. Preencha:
   - **Note**: "Git Push Local"
   - **Expiration**: 90 days
   - **Scopes**: marque `repo` (full control)
4. Clique **Generate token**
5. **Copie o token** (aparece apenas uma vez)
6. Quando pedir autenticação no Git, use:
   - **Username**: seu username GitHub
   - **Password**: o token copiado

### Opção B: SSH Key (Mais seguro, mas mais complexo)

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu.email@exemplo.com"

# Pressione Enter para locação padrão
# Digite uma senha (ou deixe em branco)

# Copiar chave pública
clip < ~/.ssh/id_ed25519.pub

# No GitHub: Settings → SSH Keys → New SSH key
# Cole a chave
```

## Passo 10: Fazer Push para GitHub

```bash
# Enviar para GitHub
git push -u origin main

# Ou depois de fazer push uma vez:
git push
```

Se pedir autenticação, cole o token.

## Verificar no GitHub

1. Acesse https://github.com/seu-usuario/prodesp-cobol-tester
2. Todos os arquivos devem aparecer
3. Commit inicial está lá

## Próximas Alterações

Depois que configurou, para cada alteração:

```bash
# Ver o que mudou
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição da mudança"

# Enviar para GitHub
git push
```

## Exemplo Completo (Passo a Passo Rápido)

```bash
# 1. Entrar pasta
cd c:\Projetos\outros\prodescp\codigo

# 2. Inicializar
git init

# 3. Configurar (primeira vez)
git config --global user.name "João Silva"
git config --global user.email "joao@example.com"

# 4. Adicionar arquivos
git add .

# 5. Primeiro commit
git commit -m "Inicial: Sistema de Testes COBOL"

# 6. Conectar ao GitHub
git remote add origin https://github.com/seu-usuario/prodesp-cobol-tester.git
git branch -M main

# 7. Push
git push -u origin main

# Digite username e token quando pedir
```

## Troubleshooting

### Erro: "fatal: not a git repository"
```bash
# Solução: estar na pasta certa e fazer git init
git init
```

### Erro: "fatal: unable to access repository"
```bash
# Solução: verificar URL
git remote -v

# Se errado, remover e adicionar novamente
git remote remove origin
git remote add origin https://github.com/seu-usuario/prodesp-cobol-tester.git
```

### Erro: "Permission denied (publickey)"
```bash
# Solução: usar HTTPS ao invés de SSH
git remote set-url origin https://github.com/seu-usuario/prodesp-cobol-tester.git
```

### Erro: "Authentication failed"
```bash
# Solução: usar token ao invés de senha
# Token do GitHub: Settings → Developer settings → Personal access tokens
```

## Arquivos para Não Fazer Push

Já temos `.gitignore` configurado para:
- `__pycache__/`
- `.venv/`
- `.env`
- `TEST_RESULTS_*.json`
- `*.pyc`

Esses arquivos são ignorados automaticamente.

## Adicionar Mais Arquivos Depois

```bash
# Modificou arquivos?
git status

# Adicionar
git add .

# Commit
git commit -m "Descrição"

# Push
git push
```

## Ver Histórico

```bash
# Ver últimos commits
git log

# Ver com gráfico
git log --oneline --graph

# Ver mudanças
git diff
```

## Clonar Repositório (Para Outros)

Para você ou outros usarem o código:

```bash
git clone https://github.com/seu-usuario/prodesp-cobol-tester.git
cd prodesp-cobol-tester
pip install -r requirements.txt
python web_app.py
```

## Links Úteis

- GitHub: https://github.com
- Git Docs: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com
- Git Cheat Sheet: https://cheatography.com/davechild/cheat-sheets/git/

---

**Versão**: 1.0  
**Data**: 2026-07-02  
**Status**: ✅ Pronto
