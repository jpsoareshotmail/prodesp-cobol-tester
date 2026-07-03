# Visualização de Código Fonte Protegida por Senha

## O que foi adicionado

✅ **Funcionalidade:**
- Botão [Codigo] em cada programa (cor roxa)
- Modal para visualizar código fonte COBOL
- Proteção por senha: `prodesp_2026`
- Exibição formatada com syntax highlighting

✅ **Segurança:**
- Senha protegida no backend
- Validação de autenticação
- Erro 401 se senha incorreta

✅ **Interface:**
- Modal responsivo
- Campo de senha com Enter para confirmar
- Botão "Carregar Codigo"
- Exibição de informações do arquivo
- Código em fundo escuro com realce

## Como Usar

### Para Desenvolvedores

1. Abra a lista "Selecionar Programas"
2. Ao lado de cada programa, há 3 botões:
   - [Testar] - Executar programa
   - [Historico] - Ver alterações
   - [Codigo] - Ver código fonte (NOVO)

3. Clique em [Codigo]
4. Uma modal abre pedindo senha
5. Digite: `prodesp_2026`
6. Clique "Carregar Codigo"
7. O código COBOL é exibido formatado

### Exemplo

```
Programa: PF-GAA-L004
Arquivo: PF-GAA-L004.C74
Tamanho: 12.34 KB

[CÓDIGO COBOL EXIBIDO]
       IDENTIFICATION DIVISION.
       PROGRAM-ID. PF-GAA-L004.
       ...
```

## Arquivos Modificados

### web_app.py
- Novo endpoint: `POST /api/programa/<nome>/codigo`
- Valida senha: `prodesp_2026`
- Lê arquivo .C74 do disco
- Retorna código com informações

### templates/index.html
- Novo botão [Codigo] em cada programa
- Novo modal de código fonte
- Funções JavaScript:
  - `abrirCodigoFonte(nome)` - Abre modal
  - `carregarCodigoFonte(nome)` - Faz requisição
  - `closeCodigoFonte()` - Fecha modal

## Estrutura da Resposta API

### Requisição
```json
POST /api/programa/PF-GAA-L004/codigo
{
  "senha": "prodesp_2026"
}
```

### Resposta de Sucesso (200)
```json
{
  "sucesso": true,
  "programa": "PF-GAA-L004",
  "arquivo": "PF-GAA-L004.C74",
  "tamanho": 12582,
  "codigo": "[conteúdo do arquivo]"
}
```

### Resposta de Erro - Senha Incorreta (401)
```json
{
  "error": "Senha incorreta",
  "sucesso": false
}
```

### Resposta de Erro - Arquivo Não Encontrado (404)
```json
{
  "error": "Arquivo de código não encontrado",
  "sucesso": false
}
```

## Logs no Console

Quando abre código fonte, aparecem logs:

```
[CODIGO] Tentativa de acesso ao código: PF-GAA-L004
[CODIGO] Senha incorreta!  <- Se errar
[CODIGO] Código carregado com sucesso: 12582 bytes  <- Se acertar
```

## Segurança

⚠️ **Notas:**

1. **Senha no Frontend**: O JavaScript envia a senha ao servidor
   - Usar HTTPS em produção para criptografar
   - Render automaticamente usa HTTPS

2. **Senha Hardcoded**: `prodesp_2026`
   - Para produção, considerar variável de ambiente
   - Ou base de dados de usuários

3. **Arquivo Local**: Lê do disco do servidor
   - Funciona em desenvolvimento
   - Em cloud, arquivos devem estar no repositório

## Visual

### Modal Aberto
```
┌─────────────────────────────────────────────────────┐
│ Codigo Fonte - PF-GAA-L004                      [×] │
│                                                     │
│ Autenticacao                                        │
│ ┌─────────────────────────────────────────────────┐ │
│ │ Senha de Acesso:                                │ │
│ │ [Senha ___________] [Carregar Codigo]           │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Arquivo COBOL                                       │
│ Programa: PF-GAA-L004                               │
│ Arquivo: PF-GAA-L004.C74                            │
│ Tamanho: 12.34 KB                                   │
│ Tipo: COBOL (Micro Focus)                           │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │       IDENTIFICATION DIVISION.                  │ │
│ │       PROGRAM-ID. PF-GAA-L004.                  │ │
│ │       ...                                       │ │
│ │ [CÓDIGO COM SCROLL]                             │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Próximas Melhorias

- [ ] Syntax highlighting (colorir palavras-chave COBOL)
- [ ] Download do arquivo original
- [ ] Copiar código para clipboard
- [ ] Busca de texto no código
- [ ] Numeração de linhas
- [ ] Temas (claro/escuro)

## Compatibilidade

✅ Funciona com:
- Firefox
- Chrome
- Edge
- Safari
- Navegadores modernos com ES6

---

**Versão**: 1.0  
**Data**: 2026-07-02  
**Status**: ✅ Pronto para Uso
