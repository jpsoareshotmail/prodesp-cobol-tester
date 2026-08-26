"""
Autenticacao e gestao de usuarios da interface web.

- Usuarios sao persistidos em data/users.json
- Senhas guardadas apenas como hash PBKDF2-HMAC-SHA256 + salt (nunca em texto puro)
- Papeis: 'admin' (gerencia usuarios) e 'user'
- Um admin inicial e criado automaticamente na primeira execucao

API:
  init_auth()                      -> garante o arquivo de usuarios + admin inicial
  verify_login(username, senha)    -> dict do usuario ou None
  list_users()                     -> lista (sem hash)
  create_user(username, senha, role, criado_por)
  delete_user(username)
  set_password(username, nova_senha)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parent.parent / 'data' / 'users.json'

# Admin inicial (troque a senha no primeiro acesso)
DEFAULT_ADMIN_USER = 'admin'
DEFAULT_ADMIN_PASS = os.environ.get('ADMIN_INITIAL_PASSWORD', 'prodesp_2026')

_PBKDF2_ITERATIONS = 200_000


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------
def _hash_password(senha: str, salt: str = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'),
                             bytes.fromhex(salt), _PBKDF2_ITERATIONS)
    return salt, dk.hex()


def _check_password(senha: str, salt: str, hash_hex: str) -> bool:
    _, calc = _hash_password(senha, salt)
    return hmac.compare_digest(calc, hash_hex)


# ---------------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------------
def _load() -> dict:
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _save(users: dict) -> None:
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, indent=2, ensure_ascii=False), encoding='utf-8')


def init_auth() -> None:
    """Garante que o arquivo de usuarios exista com um admin inicial."""
    users = _load()
    if DEFAULT_ADMIN_USER not in users:
        salt, h = _hash_password(DEFAULT_ADMIN_PASS)
        users[DEFAULT_ADMIN_USER] = {
            'username': DEFAULT_ADMIN_USER,
            'salt': salt,
            'hash': h,
            'role': 'admin',
            'criado_em': datetime.now().isoformat(timespec='seconds'),
            'criado_por': 'sistema',
            'must_change_password': True,
        }
        _save(users)


# ---------------------------------------------------------------------------
# Operacoes
# ---------------------------------------------------------------------------
def verify_login(username: str, senha: str):
    username = (username or '').strip()
    users = _load()
    u = users.get(username)
    if not u:
        return None
    if _check_password(senha or '', u['salt'], u['hash']):
        return {
            'username': u['username'],
            'role': u['role'],
            'must_change_password': bool(u.get('must_change_password', False)),
        }
    return None


def list_users() -> list:
    users = _load()
    return sorted(
        [
            {
                'username': u['username'],
                'role': u['role'],
                'criado_em': u.get('criado_em', ''),
                'criado_por': u.get('criado_por', ''),
            }
            for u in users.values()
        ],
        key=lambda x: x['username'],
    )


def create_user(username: str, senha: str, role: str = 'user', criado_por: str = '') -> dict:
    username = (username or '').strip()
    if not username or not senha:
        raise ValueError('Usuario e senha sao obrigatorios.')
    if len(senha) < 6:
        raise ValueError('A senha deve ter no minimo 6 caracteres.')
    if role not in ('admin', 'user'):
        raise ValueError('Papel invalido (use admin ou user).')
    users = _load()
    if username in users:
        raise ValueError('Usuario ja existe.')
    salt, h = _hash_password(senha)
    users[username] = {
        'username': username,
        'salt': salt,
        'hash': h,
        'role': role,
        'criado_em': datetime.now().isoformat(timespec='seconds'),
        'criado_por': criado_por or 'admin',
        'must_change_password': True,
    }
    _save(users)
    return {'username': username, 'role': role}


def delete_user(username: str) -> None:
    username = (username or '').strip()
    users = _load()
    if username not in users:
        raise ValueError('Usuario nao encontrado.')
    if username == DEFAULT_ADMIN_USER:
        raise ValueError('Nao e permitido excluir o admin inicial.')
    admins = [u for u in users.values() if u['role'] == 'admin']
    if users[username]['role'] == 'admin' and len(admins) <= 1:
        raise ValueError('Nao e permitido excluir o unico administrador.')
    del users[username]
    _save(users)


def set_password(username: str, nova_senha: str, forcar_troca: bool = True) -> None:
    """Redefine a senha (uso do admin). Por padrao marca must_change_password
    para o usuario trocar no proximo login."""
    username = (username or '').strip()
    if len(nova_senha or '') < 6:
        raise ValueError('A senha deve ter no minimo 6 caracteres.')
    users = _load()
    if username not in users:
        raise ValueError('Usuario nao encontrado.')
    salt, h = _hash_password(nova_senha)
    users[username]['salt'] = salt
    users[username]['hash'] = h
    users[username]['must_change_password'] = forcar_troca
    _save(users)


def change_own_password(username: str, senha_atual: str, nova_senha: str) -> None:
    """O proprio usuario troca a senha, validando a senha atual.
    Limpa a flag must_change_password."""
    username = (username or '').strip()
    users = _load()
    u = users.get(username)
    if not u:
        raise ValueError('Usuario nao encontrado.')
    if not _check_password(senha_atual or '', u['salt'], u['hash']):
        raise ValueError('Senha atual incorreta.')
    if len(nova_senha or '') < 6:
        raise ValueError('A nova senha deve ter no minimo 6 caracteres.')
    if nova_senha == senha_atual:
        raise ValueError('A nova senha deve ser diferente da atual.')
    salt, h = _hash_password(nova_senha)
    u['salt'] = salt
    u['hash'] = h
    u['must_change_password'] = False
    _save(users)
