# Deploy no Render

Guia passo a passo para fazer deploy da aplicação Flask no Render (plano gratuito).

## Pré-requisitos

1. **Conta GitHub** - https://github.com
2. **Conta Render** - https://render.com (gratuito)
3. **Git instalado** - https://git-scm.com

## Passo 1: Preparar Repositório Git

```bash
cd c:\Projetos\outros\prodescp\codigo

# Inicializar repositório git (se ainda não fez)
git init

# Adicionar arquivos
git add .

# Criar commit
git commit -m "Inicial: Sistema de Testes COBOL"

# Adicionar origem remota (substitua seu-usuario e seu-repo)
git remote add origin https://github.com/seu-usuario/seu-repo.git

# Fazer push para GitHub
git branch -M main
git push -u origin main
```

## Passo 2: Conectar no Render

1. Acesse https://render.com
2. Clique em **"Sign up"** (use GitHub para mais fácil)
3. Autorize o acesso ao seu GitHub

## Passo 3: Criar Novo Serviço

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Selecione seu repositório GitHub
4. Configure:

   - **Name**: `prodesp-cobol-tester`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free (gratuito, com limitações)

5. Clique em **"Create Web Service"**

## Passo 4: Acompanhar Deploy

- O Render vai começar a fazer build automaticamente
- Você verá logs do processo
- Quando terminar, terá uma URL como: `https://prodesp-cobol-tester.onrender.com`

## Limitações do Plano Free

⚠️ **Importante:**
- Apps dormem após 15 minutos de inatividade
- Primeira requisição após dormência leva ~30 segundos (cold start)
- 0.5 GB de RAM
- Sem banda larga garantida
- Ideal apenas para testes/demos

## Como Evitar Dormência (Opcional)

Você pode usar um serviço como **UptimeRobot** para "manter acordado":

1. Crie conta em https://uptimerobot.com
2. Adicione monitor HTTP para sua URL
3. Configure para fazer ping a cada 5 minutos

## Estrutura de Arquivos Necessária

Certifique-se de ter na raiz do repositório:

```
codigo/
├── web_app.py                 (aplicação principal)
├── requirements.txt           (dependências Python)
├── Procfile                   (comando para executar)
├── render.yaml               (configuração Render)
├── .gitignore                (arquivos a ignorar)
├── templates/
│   └── index.html            (interface web)
├── PGM POC cob original/      (programas COBOL)
├── program_descriptions.py    (descrições)
├── program_history.py         (histórico)
├── mock_data_expanded.py      (dados mockados)
└── executor_cobol.py          (executor)
```

## Testando Localmente Antes do Deploy

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar localmente
python web_app.py

# Acessar em http://localhost:5000
```

## Troubleshooting

### Build falha
- Verifique `requirements.txt`
- Certifique-se que todos os arquivos estão no Git
- Veja logs do Render para detalhes

### Aplicação fica offline
- Plano Free tem limitações de tempo de atividade
- Considere upgrade para plano pago

### Erro 404 no deploy
- Verifique se `web_app.py` existe
- Verifique comando `Start Command`
- Certifique-se que Flask está rodando na porta `$PORT`

## URLs Importantes

- Render: https://render.com
- Dashboard: https://dashboard.render.com
- Seu App: https://prodesp-cobol-tester.onrender.com

## Próximos Passos

Após deploy bem-sucedido:

1. Teste a interface web
2. Verifique os endpoints da API
3. Execute alguns testes de programas
4. Copie a URL para compartilhar com outros

---

**Versão**: 1.0  
**Data**: 2026-07-02  
**Status**: Pronto para deploy
