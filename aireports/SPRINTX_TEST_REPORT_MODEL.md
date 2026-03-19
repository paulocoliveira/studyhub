# Sprint 1 — Test Report
## Finanpy — Autenticação com E-mail

**Data de execução:** 2026-03-06
**Ambiente:** Django 6.0.3 · Python 3.13 · SQLite · TailwindCSS CDN
**Método:** Django Test Client (script automatizado) + análise estática de código
**Executado por:** Claude Code (django-web-qa-specialist agent)

---

## Resumo Executivo

| Métrica | Valor |
|---------|-------|
| Total de testes | 12 |
| PASS | 9 |
| WARN | 3 |
| FAIL | 0 |
| Bugs encontrados | 4 |
| Bugs corrigidos na sprint | 3 |
| Bugs pendentes (próxima sprint) | 1 |

**Resultado geral:** APROVADO COM RESSALVAS — nenhuma falha crítica ou bloqueante. O núcleo do fluxo de autenticação (registro, validação, login, logout) está funcional.

---

## Escopo dos Testes

### Componentes testados

| Componente | Arquivo | Status |
|------------|---------|--------|
| Model `CustomUser` | `users/models.py` | Testado |
| `CustomUserManager` | `users/models.py` | Testado |
| `EmailBackend` | `users/backends.py` | Testado |
| `UserRegisterForm` | `users/forms.py` | Testado |
| `UserLoginForm` | `users/forms.py` | Testado |
| `RegisterView` | `users/views.py` | Testado |
| `LoginView` | `users/views.py` | Testado |
| `LogoutView` | `users/views.py` | Testado |
| Template `register.html` | `templates/users/register.html` | Testado |
| Template `login.html` | `templates/users/login.html` | Testado |
| URLs `users/urls.py` | `users/urls.py` | Testado |
| Rota raiz `/` | `core/urls.py` | Testado |

### Componentes fora do escopo (Sprint 2+)

- `Profile` model e signal de criação automática
- Dashboard (`/dashboard/`)
- Landing page

---

## Casos de Teste

### TC-01 — Verificação de integridade do projeto Django

| Campo | Valor |
|-------|-------|
| **ID** | TC-01 |
| **Tarefa** | 1.8.1 |
| **Descrição** | Verificar que `python manage.py check` não reporta erros |
| **Pré-condição** | Ambiente virtual ativo, dependências instaladas |
| **Comando** | `python manage.py check` |
| **Resultado esperado** | `System check identified no issues (0 silenced).` |
| **Resultado obtido** | `System check identified no issues (0 silenced).` |
| **Status** | **PASS** |

---

### TC-02 — Acesso à URL raiz

| Campo | Valor |
|-------|-------|
| **ID** | TC-02 |
| **Tarefa** | 1.8.2 |
| **Descrição** | Verificar que GET `/` retorna resposta válida (não 500, não 404) |
| **Pré-condição** | Servidor Django configurado |
| **Input** | `GET /` |
| **Resultado esperado** | HTTP 302 redirect para `/users/login/` |
| **Resultado obtido (inicial)** | HTTP 404 — rota raiz não definida |
| **Bug associado** | B-01 |
| **Correção aplicada** | Adicionado `RedirectView` em `core/urls.py` |
| **Resultado após correção** | HTTP 302 para `/users/login/` |
| **Status** | **WARN → corrigido** |

---

### TC-03 — Acesso à página de cadastro

| Campo | Valor |
|-------|-------|
| **ID** | TC-03 |
| **Tarefa** | 1.8.3 |
| **Descrição** | Verificar que GET `/users/register/` renderiza o formulário de cadastro |
| **Input** | `GET /users/register/` |
| **Resultado esperado** | HTTP 200 com formulário renderizado |
| **Resultado obtido** | HTTP 200 |
| **Status** | **PASS** |

---

### TC-04 — Cadastro com e-mail inválido

| Campo | Valor |
|-------|-------|
| **ID** | TC-04 |
| **Tarefa** | 1.8.4 |
| **Descrição** | Verificar que o formulário rejeita e-mail malformado com mensagem de erro |
| **Input** | `POST /users/register/` com `email=nao-e-um-email` |
| **Resultado esperado** | HTTP 200 + erro de validação no campo email |
| **Resultado obtido** | HTTP 200 + erro exibido no template |
| **Status** | **PASS** |

---

### TC-05 — Cadastro com senha fraca

| Campo | Valor |
|-------|-------|
| **ID** | TC-05 |
| **Tarefa** | 1.8.5 |
| **Descrição** | Verificar que o formulário rejeita senhas que não passam nos validators do Django |
| **Input** | `POST /users/register/` com `password1=123`, `password2=123` |
| **Resultado esperado** | HTTP 200 + erros de validação de senha + usuário não criado |
| **Resultado obtido** | HTTP 200 + erros + `CustomUser.objects.count()` inalterado |
| **Status** | **PASS** |

---

### TC-06 — Cadastro com dados válidos

| Campo | Valor |
|-------|-------|
| **ID** | TC-06 |
| **Tarefa** | 1.8.6 |
| **Descrição** | Verificar que o cadastro com dados válidos cria o usuário no banco |
| **Input** | `POST /users/register/` com `email=test@finanpy.com`, `password1=TestPass123!`, `password2=TestPass123!` |
| **Resultado esperado** | Usuário criado no banco de dados |
| **Resultado obtido** | Usuário criado com sucesso (`CustomUser.objects.get(email='test@finanpy.com')`) |
| **Status** | **PASS** |

---

### TC-07 — Redirecionamento após cadastro

| Campo | Valor |
|-------|-------|
| **ID** | TC-07 |
| **Tarefa** | 1.8.7 |
| **Descrição** | Verificar que após cadastro válido o usuário é redirecionado para a tela de login |
| **Resultado esperado** | HTTP 302 para `/users/login/` |
| **Resultado obtido** | HTTP 302 para `/users/login/` |
| **Status** | **PASS** |

---

### TC-08 — Logout

| Campo | Valor |
|-------|-------|
| **ID** | TC-08 |
| **Tarefa** | 1.8.8 |
| **Descrição** | Verificar que POST `/users/logout/` encerra a sessão e redireciona |
| **Pré-condição** | Usuário autenticado |
| **Input** | `POST /users/logout/` |
| **Resultado esperado** | HTTP 302 para `/users/login/` |
| **Resultado obtido** | HTTP 302 para `/users/login/` |
| **Status** | **PASS** |

---

### TC-09 — Login com credenciais inválidas

| Campo | Valor |
|-------|-------|
| **ID** | TC-09 |
| **Tarefa** | 1.8.9 |
| **Descrição** | Verificar que login com e-mail ou senha incorretos exibe mensagem de erro sem 500 |
| **Input** | `POST /users/login/` com `username=errado@test.com`, `password=senhaerrada` |
| **Resultado esperado** | HTTP 200 + mensagem de erro visível |
| **Resultado obtido** | HTTP 200 + mensagem de erro renderizada em `text-rose-400` |
| **Observação** | Mensagem original do Django pt-br tinha espaço duplo ("email  e senha") — corrigido via B-03 |
| **Status** | **PASS** |

---

### TC-10 — Login com credenciais válidas

| Campo | Valor |
|-------|-------|
| **ID** | TC-10 |
| **Tarefa** | 1.8.10 |
| **Descrição** | Verificar que login com credenciais corretas autentica e redireciona para o dashboard |
| **Input** | `POST /users/login/` com `username=test@finanpy.com`, `password=TestPass123!` |
| **Resultado esperado** | HTTP 302 para `/dashboard/` |
| **Resultado obtido** | HTTP 302 para `/dashboard/` |
| **Status** | **PASS** |

---

### TC-11 — Usuário autenticado acessa tela de login

| Campo | Valor |
|-------|-------|
| **ID** | TC-11 |
| **Tarefa** | 1.8.11 |
| **Descrição** | Verificar que usuário já logado é redirecionado ao acessar `/users/login/` |
| **Pré-condição** | Usuário autenticado na sessão |
| **Input** | `GET /users/login/` |
| **Resultado esperado** | HTTP 302 para `/dashboard/` |
| **Resultado obtido (inicial)** | HTTP 200 — formulário exibido novamente |
| **Bug associado** | B-02 |
| **Correção aplicada** | `redirect_authenticated_user = True` em `users/views.py` |
| **Resultado após correção** | HTTP 302 para `/dashboard/` |
| **Status** | **WARN → corrigido** |

---

### TC-12 — Criação automática de Profile após cadastro

| Campo | Valor |
|-------|-------|
| **ID** | TC-12 |
| **Tarefa** | 1.8.12 |
| **Descrição** | Verificar que ao cadastrar um usuário, um `Profile` é criado automaticamente via signal |
| **Resultado esperado** | `Profile` criado e associado ao usuário |
| **Resultado obtido** | `profiles/models.py` vazio — model não implementado |
| **Pendência** | Sprint 2 (tarefas 2.1 e 2.2) |
| **Status** | **WARN — pendência confirmada** |

---

## Bugs Descobertos Durante os Testes

| ID | Prioridade | Status | Descrição |
|----|------------|--------|-----------|
| B-01 | Medium | Corrigido | URL raiz `/` retornava 404 |
| B-02 | Medium | Corrigido | `LoginView` não redirecionava usuário já autenticado |
| B-03 | Low | Corrigido | Mensagem de erro de login com espaço duplo |
| B-04 | High | Corrigido | `CustomUserManager` ausente — `create_user()` falhava com `TypeError` |

> Detalhes completos em `SPRINT1_BUG_REPORT.md`

---

## Cobertura por Tarefa da Sprint 1

| Tarefa | Descrição | Testada | Resultado |
|--------|-----------|---------|-----------|
| 1.1 | Customizar model de usuário | Sim | PASS |
| 1.2 | Backend de autenticação customizado | Sim | PASS |
| 1.3 | Formulários de autenticação | Sim | PASS |
| 1.4 | Views de autenticação | Sim | PASS (com correções B-02) |
| 1.5 | Templates de autenticação | Sim | PASS |
| 1.6 | URLs de autenticação | Sim | PASS (com correção B-01) |
| 1.7 | Registro no admin | Verificado via `check` | PASS |
| 1.8 | Fluxo completo | Sim | PASS (com correções) |

---

## Ambiente de Teste

```
Sistema operacional : macOS Darwin 25.3.0
Python              : 3.13
Django              : 6.0.3
Banco de dados      : SQLite (db.sqlite3)
Autenticação        : users.backends.EmailBackend
AUTH_USER_MODEL     : users.CustomUser
LOGIN_URL           : /users/login/
LOGIN_REDIRECT_URL  : /dashboard/
LOGOUT_REDIRECT_URL : /users/login/
```
