# Render Deploy - Checklist

Use este checklist para acompanhar o deploy.

## ✅ Antes de Começar

- [ ] Tem conta GitHub
- [ ] Projeto está no GitHub
- [ ] Pode fazer login no GitHub
- [ ] requirements.txt existe e tem dependências
- [ ] Procfile ou render.yaml existe
- [ ] web_app.py está no repositório
- [ ] Pasta templates/ está no repositório

## ✅ Criar Conta Render

- [ ] Acesse https://render.com
- [ ] Clique "Sign up"
- [ ] Escolha "Sign up with GitHub"
- [ ] Autorize Render acessar GitHub
- [ ] Complete cadastro
- [ ] Confirme email

## ✅ Conectar GitHub ao Render

- [ ] Acesse https://dashboard.render.com
- [ ] Vá para Settings
- [ ] Clique "GitHub"
- [ ] "Connect account"
- [ ] Autorize Render
- [ ] Selecione repositório (ou deixa acessar todos)

## ✅ Criar Web Service

- [ ] Render Dashboard aberto
- [ ] Clique "New +"
- [ ] Escolha "Web Service"
- [ ] Seu repositório apareceu na lista

## ✅ Configurar Serviço

Configure exatamente assim:

```
Name:                 prodesp-cobol-tester
Runtime:              Python 3
Build Command:        pip install -r requirements.txt
Start Command:        gunicorn web_app:app --bind 0.0.0.0:$PORT
Environment:          Production
Plan:                 Free
```

- [ ] Nome: `prodesp-cobol-tester`
- [ ] Runtime: `Python 3`
- [ ] Build: `pip install -r requirements.txt`
- [ ] Start: `gunicorn web_app:app --bind 0.0.0.0:$PORT`
- [ ] Plan: `Free`
- [ ] Clique "Create Web Service"

## ✅ Acompanhar Build

- [ ] Render começa a compilar
- [ ] Vê logs em tempo real
- [ ] Procura por erros:
  - [ ] ModuleNotFoundError?
  - [ ] ImportError?
  - [ ] File not found?

## ✅ Deploy Sucesso

- [ ] Build finished
- [ ] Status: "Live"
- [ ] URL gerada como: `https://prodesp-cobol-tester.onrender.com`

## ✅ Testar Aplicação

- [ ] Copie URL do Render
- [ ] Abra em novo navegador
- [ ] Página de login aparece
- [ ] Digite: `prodesp_2026`
- [ ] Dashboard aparece
- [ ] Clique em botões (Testar, Histórico, Código)

## ✅ Verificar Funcionalidades

- [ ] Login funciona
- [ ] [Testes Básicos] executa
- [ ] [Testes Expandidos] executa
- [ ] [Selecionar Programa para Teste] abre lista
- [ ] [Código] pede senha
- [ ] [Histórico] mostra dados
- [ ] [Sair] faz logout

## ✅ Monitorar Aplicação

- [ ] Render Dashboard aberto
- [ ] Clique no serviço
- [ ] Vê status: "Live"
- [ ] Vê logs
- [ ] Vê métricas

## 🔍 Se Algo Deu Errado

- [ ] Veja logs do Render
- [ ] Procure por erro específico
- [ ] Clique "Redeploy" para tentar novamente
- [ ] Se erro persiste, veja Troubleshooting abaixo

## ⚙️ Troubleshooting

### Build falha com "ModuleNotFoundError"

Solução:
- [ ] requirements.txt está correto?
- [ ] Fez push do requirements.txt para GitHub?
- [ ] Dependências têm versão específica?

### Start Command error

Solução:
- [ ] Start Command tem `$PORT`?
- [ ] Sem `$PORT`, app não consegue rodar na porta certa

### Port error "Address already in use"

Solução:
- [ ] Verificar se Start Command usa `$PORT`
- [ ] Render atribui porta dinamicamente

### App dorme depois de 15 min

Normal no plano Free:
- [ ] Primeira requisição demora ~30s
- [ ] Depois volta ao normal
- [ ] Use UptimeRobot para manter acordado

### Erro 502 Bad Gateway

Solução:
- [ ] App pode estar crashando
- [ ] Veja logs
- [ ] Teste localmente
- [ ] Clique "Redeploy"

### Erro 503 Service Unavailable

Solução:
- [ ] App pode estar com problema
- [ ] Aguarde alguns segundos
- [ ] Recarregue página

## 📊 Monitorar Performance

- [ ] Render Dashboard
- [ ] Clique seu serviço
- [ ] Vá para "Metrics"
- [ ] Veja CPU, Memory, Request Count

## 🚀 Próximas Etapas

Após deploy bem-sucedido:

- [ ] Teste toda a interface
- [ ] Verifique funcionalidades principais
- [ ] Compartilhe URL com outros
- [ ] Monitore performance
- [ ] Configure UptimeRobot (opcional)
- [ ] Upgrade para plano pago se necessário

## 📝 URLs Importantes

| Item | URL |
|------|-----|
| Render | https://render.com |
| Dashboard | https://dashboard.render.com |
| Seu Serviço | https://prodesp-cobol-tester.onrender.com |
| GitHub | https://github.com/seu-usuario/prodesp-cobol-tester |
| UptimeRobot | https://uptimerobot.com |

## 💾 Fazer Deploy de Mudanças

Quando fizer alterações no código:

```bash
# 1. Adicione mudanças
git add .

# 2. Faça commit
git commit -m "Descrição da mudança"

# 3. Push para GitHub
git push

# 4. Render detecta automaticamente
#    e faz novo deploy
```

- [ ] Mudança feita localmente
- [ ] Git commit + push
- [ ] Render detecta mudança
- [ ] Deploy inicia automaticamente
- [ ] Teste nova versão

## ✨ Status Final

Quando tudo funciona:

```
✅ Deploy completo
✅ App rodando em produção
✅ URL pública disponível
✅ Todos podem acessar
✅ Pronto para usar!
```

---

**Versão**: 1.0  
**Data**: 2026-07-02  
**Status**: ✅ Pronto para Deploy
