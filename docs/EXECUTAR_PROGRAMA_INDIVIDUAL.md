# ⚡ Executar Programa Individual com Dados Customizados

## O Que É

Novo recurso que permite **selecionar um programa específico e executá-lo com dados mockados** que o usuário pode modificar.

Perfeito para:
- Testar um programa isoladamente
- Debug rápido com dados pré-preenchidos
- Experimentar diferentes entradas
- Validar comportamento do programa

## Como Usar

### 1. Clicar em "🎯 Selecionar Programas"

A janela de seleção abre mostrando todos os 42 programas.

### 2. Clicar no Botão "⚡ Testar" Ao Lado do Programa

```
┌─────────────────────────────────────────┐
│ ☐ PF-GAA-L004                   [⚡ Testar] ← Clique aqui
│   Validador de Placas                    │
└─────────────────────────────────────────┘
```

### 3. Formulário Abre Com Dados Pré-Preenchidos

```
┌─────────────────────────────────────────┐
│ ⚡ Executar Programa Individual         │
│                                         │
│ 📝 PF-GAA-L004 - Validador de Placas  │
│ [← Voltar]                              │
│                                         │
│ Placa:                                  │
│ [AAA0A00____________]                   │
│                                         │
│ Exemplos Rápidos:                       │
│ [📋 Mercosul - SP] [📋 2 letras]       │
│                                         │
│ [▶ Executar Programa] [↻ Limpar]      │
│                                         │
│ ✓ Execução bem-sucedida!               │
│ Programa: PF-GAA-L004                  │
│ Saída: {"valida": true, "codigo": 11} │
└─────────────────────────────────────────┘
```

### 4. Modificar Valores (Opcional)

Os valores padrão (mockados) são preenchidos automaticamente, mas você pode:
- Digitar novos valores
- Clicar em "Exemplos Rápidos" para carregar predefinidos
- Limpar o formulário para começar do zero

### 5. Executar

Clique em "▶ Executar Programa" para rodar com os dados fornecidos.

### 6. Ver Resultado

O resultado aparece em seção dedicada mostrando:
- Status (sucesso ou erro)
- Dados de entrada
- Dados de saída

## Dados Mockados Disponíveis

### PF-GAA-L004 (Validador de Placas)

**Campos:**
- `placa` (Texto, máx 10 caracteres)

**Exemplos:**
```
1. Mercosul - São Paulo      → AAA0A00
2. 2 letras - Carros         → AB12C34
3. Placa Antiga - SP         → SP1234
4. Com caractere especial    → ABC-1234
5. Vazia                     → (vazio)
```

**Saída Esperada:**
```json
{
  "valida": true/false,
  "codigo": 0-34,
  "descricao": "Tipo de placa"
}
```

### PF-GEV-L006-DB (Gestão Empadronização)

**Campos:**
- `placa` (Texto)
- `ano` (Número, 1980-2026)
- `marca` (Texto)

**Exemplos:**
```
1. Mercosul Recente    → AAA0A00 / 2020 / Toyota
2. Antigo              → SP1234 / 2010 / Volkswagen
```

### PF-GAT-L006-DB (Gestão Autoridades)

**Campos:**
- `codigo` (Número, 001-999)
- `nome` (Texto)
- `uf` (Select: SP, RJ, MG, BA, RS)

**Exemplos:**
```
1. DETRAN SP    → 001 / DETRAN SP / SP
2. DETRAN RJ    → 002 / DETRAN RJ / RJ
```

## Estrutura de Dados Mockados

Cada programa pode ter um arquivo `mock_data.py` com:

```python
{
    "PF-NOME-L001": {
        "tipo": "categoria",
        "descricao": "Descrição do programa",
        "campos": [
            {
                "nome": "campo1",
                "label": "Rótulo do Campo",
                "tipo": "texto/numero/select/textarea",
                "placeholder": "Dica de entrada",
                "valor": "Valor padrão",
                "maxlength": "20",  # para texto
                "opcoes": [...]     # para select
            }
        ],
        "exemplos": [
            {
                "campo1": "valor1",
                "campo2": "valor2",
                "descricao": "Descrição do exemplo"
            }
        ]
    }
}
```

## API Endpoints

### GET `/api/programa/<nome>/dados`

Retorna dados mockados para um programa:

```bash
curl http://localhost:5000/api/programa/PF-GAA-L004/dados
```

Resposta:
```json
{
  "tipo": "placa",
  "descricao": "Validador de Placas",
  "campos": [
    {
      "nome": "placa",
      "label": "Placa",
      "tipo": "texto",
      "valor": "AAA0A00"
    }
  ],
  "exemplos": [...]
}
```

### POST `/api/programa/<nome>/executar`

Executa programa com dados:

```bash
curl -X POST http://localhost:5000/api/programa/PF-GAA-L004/executar \
  -H "Content-Type: application/json" \
  -d '{"placa": "AAA0A00"}'
```

Resposta (Sucesso):
```json
{
  "sucesso": true,
  "programa": "PF-GAA-L004",
  "entrada": {"placa": "AAA0A00"},
  "saida": {
    "valida": true,
    "codigo": 11,
    "descricao": "Mercosul - São Paulo"
  }
}
```

Resposta (Erro):
```json
{
  "sucesso": false,
  "error": "Dados inválidos",
  "erros": ["Campo obrigatório: Placa"]
}
```

### POST `/api/programa/<nome>/validar`

Valida dados sem executar:

```bash
curl -X POST http://localhost:5000/api/programa/PF-GAA-L004/validar \
  -H "Content-Type: application/json" \
  -d '{"placa": "AAA0A00"}'
```

## Tipos de Campos Suportados

### Texto (`tipo: "texto"`)
```html
<input type="text" value="padrão" maxlength="50">
```

### Número (`tipo: "numero"`)
```html
<input type="number" value="2020" min="1980" max="2026">
```

### Select (`tipo: "select"`)
```html
<select>
  <option value="SP">São Paulo</option>
  <option value="RJ">Rio de Janeiro</option>
</select>
```

### Textarea (`tipo: "textarea"`)
```html
<textarea rows="5">Dados multi-linha</textarea>
```

## Casos de Uso

### 1. Debug Rápido de Um Programa

```
Problema: PF-GEV-T005-DB não valida RENAVAM
Ação:
  1. Abrir seletor
  2. Clicar em ⚡ Testar ao lado de PF-GEV-T005-DB
  3. Modificar número do RENAVAM
  4. Executar
  5. Ver resultado imediatamente
```

### 2. Testar Múltiplas Entradas

```
Necessidade: Validar placa com 5 formatos diferentes
Ação:
  1. Abrir PF-GAA-L004
  2. Clicar em cada exemplo
  3. Ver resultado para cada um
  4. Identificar padrões de falha
```

### 3. Validar Campos Obrigatórios

```
Necessidade: Verificar validação de entrada
Ação:
  1. Abrir programa
  2. Clicar em [↻ Limpar]
  3. Deixar campos vazios
  4. Executar
  5. Ver mensagens de erro
```

## Arquivos Criados/Modificados

### Novo
- `mock_data.py` - Base de dados mockados

### Modificado
- `web_app.py` - 3 novos endpoints
- `templates/index.html` - Interface do executor

## Features

✅ Seleção de programa com botão "Testar"  
✅ Formulário dinâmico baseado em dados do programa  
✅ Valores pré-preenchidos (mockados)  
✅ Botões de exemplos rápidos  
✅ Validação de entrada  
✅ Execução individual do programa  
✅ Resultado formatado em JSON  
✅ Tratamento de erros  
✅ Volta ao seletor a qualquer momento  

## Próximos Passos Sugeridos

1. **Adicionar mais dados mockados**
   - Para cada programa criar exemplos específicos
   - Validações mais robustas

2. **Histórico de execuções**
   - Lembrar últimas entradas
   - Salvar execuções bem-sucedidas

3. **Export de resultados**
   - Exportar resultado em JSON
   - Exportar entrada/saída em CSV

4. **Comparação entre execuções**
   - Comparar resultados de diferentes programas
   - Identificar divergências

---

**Versão**: 2.2.0  
**Data**: 2026-07-02  
**Status**: ✅ Implementado e Testado
