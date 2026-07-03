# Autenticação e Tela de Login

## O que foi adicionado

✅ **Tela de Login**
- Aparece automaticamente ao abrir a aplicação
- Design limpo e responsivo
- Campo de senha com Enter para confirmar

✅ **Autenticação**
- Senha: `prodesp_2026`
- Validação em tempo real
- Armazenamento seguro em localStorage

✅ **Gerenciamento de Sessão**
- Token armazenado localmente
- Mantém autenticação ao recarregar página
- Botão [Sair] para logout

✅ **Segurança**
- Senha mascarada no campo
- Mensagens de erro claras
- Logout limpa sessão

## Como Funciona

### 1. Primeira Visita
```
Usuario acessa: http://localhost:5000
         |
         v
Tela de Login aparece
         |
         v
Digite: prodesp_2026
         |
         v
Clique [Entrar] ou pressione Enter
         |
         v
Dashboard aparece
```

### 2. Recarregar Página
```
Usuario faz F5 / Recarrega página
         |
         v
Sistema verifica token em localStorage
         |
         v
Se token válido --> Mostra dashboard diretamente
Se não --> Mostra login novamente
```

### 3. Logout
```
Usuario clica [Sair] no header
         |
         v
Token é removido de localStorage
         |
         v
Tela de login aparece novamente
```

## Interface de Login

### Visual
```
┌─────────────────────────────────────────┐
│                                         │
│         🔐 Sistema COBOL               │
│                                         │
│   Prodesp - Testes Automatizados       │
│                                         │
│  Senha de Acesso:                       │
│  ┌─────────────────────────────────┐  │
│  │ ••••••••••••                     │  │
│  └─────────────────────────────────┘  │
│                                         │
│      [    Entrar    ]                  │
│                                         │
│  Sistema de testes do sistema           │
│  legado COBOL                           │
│                                         │
└─────────────────────────────────────────┘
```

### Cores e Estilos
- Fundo: Gradiente roxa (igual ao dashboard)
- Caixa: Branca com sombra
- Botão: Azul primário
- Erro: Vermelho com borda

## Funcionalidades

### Campo de Senha
- Mascarado automaticamente
- Enter para confirmar
- Foco automático ao abrir login
- Limpa em caso de erro

### Mensagens de Erro
```
Cenários:
1. Campo vazio
   "Digite a senha para continuar"

2. Senha incorreta
   "Senha incorreta! Tente novamente."
```

### Botão de Logout
- Localizado no canto superior direito do header
- Cor vermelha para destaque
- Remove token ao clicar
- Volta à tela de login

## Armazenamento

### localStorage
```javascript
// Ao autenticar
localStorage.setItem('prodesp_token', 'prodesp_2026');

// Ao sair
localStorage.removeItem('prodesp_token');

// Na carga
const token = localStorage.getItem('prodesp_token');
```

### Benefícios
✅ Mantém login ao recarregar página
✅ Fácil de implementar
✅ Não requer servidor de sessão
✅ Ideal para apps estáticas

### Limitações
⚠️ Token armazenado em texto plano (plaintext)
⚠️ Acessível via console do navegador
⚠️ Para produção, usar cookies seguros

## Logs no Console

Quando faz login/logout, aparecem logs:

```
[AUTH] Tentativa de autenticação
[AUTH] Autenticado com sucesso!
[AUTH] Mostrando dashboard
[AUTH] Desconectado
[AUTH] Mostrando tela de login
```

## Fluxo de Segurança

```
┌─────────────────────────────┐
│  Usuario acessa aplicação   │
└────────────┬────────────────┘
             │
             v
┌─────────────────────────────┐
│  Verifica localStorage      │
└────────────┬────────────────┘
             │
        ┌────┴─────┐
        │           │
      Sim           Não
        │           │
        v           v
   ┌────────┐  ┌─────────┐
   │Mostra  │  │ Mostra  │
   │Board   │  │ Login   │
   └────────┘  └────┬────┘
                    │
                    v
              ┌──────────────┐
              │ Usuario      │
              │ digita       │
              │ senha        │
              └──────┬───────┘
                     │
              ┌──────v───────┐
              │ Valida senha │
              └──────┬───────┘
                     │
                ┌────┴──────┐
                │            │
              Correta      Errada
                │            │
                v            v
            ┌────────┐  ┌────────┐
            │Salva   │  │ Mostra │
            │token   │  │ Erro   │
            └────┬───┘  └────────┘
                 │
                 v
            ┌─────────────┐
            │ Mostra Board│
            └─────────────┘
```

## Configuração

### Senha Atual
```
prodesp_2026
```

### Para Mudar a Senha

**Opção 1: Modificar no HTML**
```javascript
// Em templates/index.html, procure por:
if (senha !== 'prodesp_2026') {

// Altere para:
if (senha !== 'sua_nova_senha') {

// E também em:
localStorage.setItem('prodesp_token', 'prodesp_2026');

// Para:
localStorage.setItem('prodesp_token', 'sua_nova_senha');
```

**Opção 2: Usar Variável de Ambiente (Melhor)**
```python
# Em web_app.py, adicione:
import os
SENHA_LOGIN = os.getenv('SENHA_LOGIN', 'prodesp_2026')

# E envie para template:
return render_template('index.html', senha_hash='...')
```

## Testes

### Testar Login

1. Abra http://localhost:5000
2. Vê tela de login
3. Digite: `prodesp_2026`
4. Clique [Entrar]
5. Dashboard aparece

### Testar Logout

1. Clique botão [Sair]
2. Volta à tela de login
3. localStorage foi limpo
4. Pode fazer login novamente

### Testar Persistência

1. Faça login
2. Pressione F5 (recarregar)
3. Dashboard aparece sem pedir senha
4. localStorage mantém token

### Testar Erro

1. Digite: `senha_errada`
2. Clique [Entrar]
3. Mensagem de erro aparece
4. Campo limpa automaticamente

## Compatibilidade

✅ Navegadores com suporte a:
- localStorage
- ES6 JavaScript
- CSS Flexbox
- Event listeners

✅ Funciona em:
- Chrome/Edge
- Firefox
- Safari
- Navegadores modernos

## Melhorias Futuras

- [ ] Autenticação com múltiplos usuários
- [ ] Senha criptografada (bcrypt)
- [ ] Sessão com servidor (JWT)
- [ ] Recuperação de senha
- [ ] Histórico de login/logout
- [ ] 2FA (Two-Factor Authentication)
- [ ] Timeout de sessão automático

## Variáveis Globais

```javascript
autenticado       // Boolean: true se logado
localStorage      // Armazena token
```

## Funções

```javascript
autenticar()      // Valida e faz login
mostrarLogin()    // Mostra tela de login
mostrarDashboard()// Mostra dashboard
logout()          // Desconecta usuário
```

---

**Versão**: 1.0  
**Data**: 2026-07-02  
**Status**: ✅ Pronto para Uso
**Senha**: prodesp_2026
