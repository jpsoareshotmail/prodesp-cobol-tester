# 🧪 Interface Web para Testes - Sistema COBOL Prodesp

Interface moderna e intuitiva para executar, monitorar e analisar testes do sistema COBOL de validação de placas veiculares.

## 📋 Características

- ✅ **Dashboard Interativo** - Visualize estatísticas em tempo real
- ✅ **Execução de Testes** - Execute a suite completa com um clique
- ✅ **Validação Manual** - Teste placas individuais instantaneamente
- ✅ **Histórico** - Acesso aos últimos 5 testes executados
- ✅ **Detalhamento** - Visualize cada teste em detalhes
- ✅ **Monitoramento** - Acompanhe o progresso em tempo real
- ✅ **Responsivo** - Funciona em desktop, tablet e mobile
- ✅ **Design Moderno** - Interface limpa e intuitiva com Tailwind CSS

## 🚀 Início Rápido

### Windows

```bash
# 1. Abrir prompt de comando na pasta do projeto
cd c:\Projetos\outros\prodescp\codigo

# 2. Executar o script de inicialização
run_web.bat
```

### Linux / macOS

```bash
# 1. Ir para a pasta do projeto
cd /caminho/para/prodescp/codigo

# 2. Tornar script executável
chmod +x run_web.sh

# 3. Executar
./run_web.sh
```

### Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente (Windows)
venv\Scripts\activate

# Ou ativar (Linux/macOS)
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar servidor
python3 web_app.py
```

## 📱 Acesso

Após iniciar o servidor, abra seu navegador em:

```
http://localhost:5000
```

O navegador será aberto automaticamente (em alguns sistemas).

## 🎯 Funcionalidades Detalhadas

### Dashboard

O dashboard exibe:
- **Execuções de Testes**: Total de execuções realizadas
- **Taxa de Sucesso**: Porcentagem média de testes passando
- **Testes Passando**: Número total de testes bem-sucedidos

Esses dados são atualizados automaticamente a cada 5 segundos.

### Executar Testes

1. Clique em "▶ Executar Testes Completos"
2. Acompanhe o progresso com a barra de progresso
3. Veja qual teste está sendo executado no momento
4. Após conclusão, visualize os resultados automaticamente

**Atalho**: Você pode cancelar uma execução em andamento clicando em "⏹ Cancelar"

### Validar Placa Individual

1. Digite a placa na caixa "Digite a placa (ex: AAA0A00)"
2. Clique em "Validar" ou pressione Enter
3. Veja o resultado instantaneamente com:
   - Status de validade
   - Código de resultado
   - Tipo/descrição da placa

### Histórico de Testes

Dois modos de visualização:

#### Resultados Recentes
- Cards mostrando os últimos 10 testes
- Taxa de sucesso visual (verde/amarelo/vermelho)
- Clique para ver detalhes completos
- Data e hora de execução

#### Detalhado
- Tabela com todos os testes de um resultado
- Colunas: ID, Nome, Categoria, Status, Entrada, Esperado, Obtido, Tempo
- Filtro por status (PASS/FAIL)
- Classificação por colunas

### Modal de Detalhes

Clique em qualquer resultado recente para ver:
- Informações gerais (arquivo, data, duração)
- Resumo estatístico (total, passou, falhou, erros)
- Lista completa de testes com detalhes

## 🔧 Configuração

### Alterar Porta

Edite `web_app.py` e procure por:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Troque `5000` pela porta desejada.

### Desabilitar Debug Mode

Para produção, altere `debug=True` para `debug=False`:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Acessar de Outro Computador

O servidor escuta em `0.0.0.0`, então é acessível via:
- Localhost: `http://localhost:5000`
- Outro PC na rede: `http://SEU_IP:5000`

Para descobrir seu IP:
- **Windows**: `ipconfig` (procure por IPv4)
- **Linux/macOS**: `ifconfig` ou `ip addr`

## 📊 Estrutura de Resultados

Os resultados são salvos como `TEST_RESULTS_YYYYMMDD_HHMMSS.json` com a estrutura:

```json
{
  "data": "2026-07-02T11:12:32.053457",
  "duracao": 0.35,
  "total": 20,
  "passed": 14,
  "failed": 6,
  "errored": 0,
  "taxa_sucesso": 70.0,
  "resultados": [
    {
      "test_id": "TC-001",
      "nome": "Mercosul - Sao Paulo",
      "categoria": "Validador",
      "status": "PASS",
      "entrada": "AAA0A00",
      "saida_esperada": "11",
      "saida_obtida": "11",
      "tempo_ms": 0.017
    }
  ]
}
```

## 🐛 Troubleshooting

### Porta já em uso

Se receber erro "Address already in use":

```bash
# Windows - Matar processo na porta 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

Ou altere a porta em `web_app.py`.

### Python não encontrado

Certifique-se que Python 3.7+ está instalado:

```bash
python3 --version
```

Se não estiver, instale de: https://www.python.org/

### Dependências não instaladas

```bash
# Ativar ambiente virtual (se necessário)
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstalar
pip install --upgrade -r requirements.txt
```

### Navegador não abriu automaticamente

Abra manualmente em: `http://localhost:5000`

## 📐 Arquitetura

```
web_app.py          - Backend Flask (API REST)
├── /api/health     - Status do servidor
├── /api/results    - Histórico de testes
├── /api/test/run   - Iniciar testes
├── /api/test/status - Status atual
├── /api/test/cancel - Cancelar execução
└── /api/validate-plate - Validar placa

templates/
└── index.html      - Frontend (HTML + CSS + JS)
    ├── Dashboard
    ├── Executor de testes
    ├── Validador de placas
    └── Histórico

test_suite.py       - Suite de testes COBOL
executor_cobol.py   - Executor de validação
```

## 🔐 Segurança

### Recomendações para Produção

1. **Desabilitar Debug Mode**
   ```python
   app.run(debug=False)
   ```

2. **Usar HTTPS**
   ```python
   from ssl import SSLContext
   ssl_context = SSLContext()
   ssl_context.load_cert_chain('cert.pem', 'key.pem')
   app.run(ssl_context=ssl_context)
   ```

3. **Adicionar Autenticação** (se necessário)
   ```python
   from flask_httpauth import HTTPBasicAuth
   auth = HTTPBasicAuth()
   ```

4. **Limitar Taxa de Requisições**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app)
   ```

## 📝 Logs

Os testes também geram saída em console do servidor. Para salvar logs:

```bash
# Windows
python3 web_app.py > server.log 2>&1

# Linux/macOS
python3 web_app.py > server.log 2>&1
```

## 🚢 Deployment

### Gunicorn (Recomendado)

```bash
# Instalar
pip install gunicorn

# Executar com 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python3", "web_app.py"]
```

Build e run:
```bash
docker build -t cobol-tests .
docker run -p 5000:5000 cobol-tests
```

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique o console do servidor (STDOUT)
2. Verifique o console do navegador (F12 → Console)
3. Leia as mensagens de erro com atenção
4. Consulte o README do projeto principal

## 📄 Licença

Este projeto é parte do sistema COBOL legado Prodesp.

---

**Última atualização**: 2026-07-02
**Versão**: 1.0.0
