# Prodesp COBOL Tester 🧪

Sistema de testes web para programas COBOL legados da Prodesp (São Paulo).

## Estrutura do Projeto

```
prodesp-cobol-tester/
├── README.md                      # Este arquivo
├── requirements.txt               # Dependências Python
├── Procfile                       # Configuração deploy
├── render.yaml                    # Render deploy config
│
├── app/                           # Código da aplicação
│   ├── web_app.py                 # Flask principal
│   ├── executor_cobol.py           # Executor COBOL
│   ├── startup.py                 # Startup script
│   └── runner.py                  # Suporte
│
├── data/                          # Dados e configurações
│   ├── mock_data_expanded.py       # Dados mockados
│   ├── program_descriptions.py     # Descrições dos programas
│   ├── program_history.py          # Histórico de versões
│   └── test_cases.json            # Casos de teste
│
├── tests/                         # Testes automatizados
│   ├── test_suite.py              # Suite básica
│   ├── test_suite_expanded.py      # Suite expandida (42 programas)
│   └── test_mobile_example.py      # Testes mobile
│
├── templates/                     # Interface web
│   ├── index.html                 # Dashboard principal
│   └── test_page.html             # Página de testes
│
├── docs/                          # Documentação
│   ├── SETUP.md                   # Como começar
│   ├── GITHUB_SETUP.md            # Setup GitHub
│   ├── DEPLOY_RENDER.md           # Deploy Render
│   ├── AUTENTICACAO_LOGIN.md      # Login
│   ├── CODIGO_FONTE_PROTEGIDO.md  # Código fonte protegido
│   └── ...                        # 40+ documentos
│
├── scripts/                       # Scripts úteis
│   ├── run_web.sh                 # Rodar localmente
│   ├── setup_github.ps1           # Setup GitHub
│   └── build.sh                   # Build script
│
└── PGM POC cob original/          # Programas COBOL (42 arquivos .C74)
```

## Início Rápido

### Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
python app/web_app.py

# Acessar
http://localhost:5000
```

### Na Nuvem (Render)

1. Push para GitHub
2. Deploy no Render
3. Acessar URL pública

Ver: `docs/RENDER_RAPIDO.txt`

## Autenticação

Senha: `prodesp_2026`

## Funcionalidades

✅ **Dashboard** - Estatísticas de testes
✅ **42 Programas COBOL** - Todos os programas Prodesp
✅ **Testes Automatizados** - Suite básica e expandida
✅ **Seleção Individual** - Testar programa por programa
✅ **Histórico de Versões** - Quem mudou, quando, por quê
✅ **Visualizar Código** - Protegido por senha
✅ **Dados Mockados** - Para cada programa

## Documentação

- `docs/SETUP.md` - Como começar
- `docs/GITHUB_SETUP.md` - Setup GitHub
- `docs/DEPLOY_RENDER.md` - Deploy Render
- `docs/AUTENTICACAO_LOGIN.md` - Sistema de autenticação
- `docs/CODIGO_FONTE_PROTEGIDO.md` - Visualizar código
- `docs/ESTRUTURA_PASTAS.txt` - Estrutura de pastas

## Deploy

### Render (Recomendado)

```bash
git push origin main
# Render detecta mudanças e faz deploy automático
```

URL: `https://prodesp-cobol-tester.onrender.com`

### GitHub

```bash
git remote add origin https://github.com/seu-usuario/prodesp-cobol-tester.git
git push -u origin main
```

## Programas Disponíveis

- **GAA** (16) - Gestão Arquivo Automotivo
- **GEV** (24) - Gestão Empadronização Veicular
- **GAT** (2) - Gestão Autoridades Trânsito

Total: **42 programas**

## Tecnologias

- **Backend**: Python Flask
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Deploy**: Render
- **Versionamento**: Git + GitHub

## Contribuir

1. Clone o repositório
2. Crie uma branch
3. Faça suas mudanças
4. Abra um PR

## Licença

Projeto Prodesp - Sistema de Testes COBOL

---

**Versão**: 2.5.0  
**Última atualização**: 2026-07-03  
**Status**: ✅ Produção
