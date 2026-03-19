# Sprint 1 — Bug Report
## Finanpy — Autenticação com E-mail

**Data:** 2026-03-06
**Ambiente:** Django 6.0.3 · Python 3.13 · SQLite
**Identificados por:** QA automatizado (Django Test Client) + análise estática
**Total de bugs:** 4
**Corrigidos:** 4 (3 durante QA automatizado · 1 durante teste manual)

---

## Índice

| ID | Severidade | Componente | Status |
|----|------------|------------|--------|
| [B-01](#b-01) | Medium | `core/urls.py` | Corrigido |
| [B-02](#b-02) | Medium | `users/views.py` | Corrigido |
| [B-03](#b-03) | Low | `users/forms.py` | Corrigido |
| [B-04](#b-04) | High | `users/models.py` | Corrigido |

---

## B-01

**Título:** URL raiz retorna HTTP 404

**Severidade:** Medium
**Componente:** `core/urls.py`
**Status:** Corrigido
**Descoberto em:** TC-02 (1.8.2)
**Data de correção:** 2026-03-06

### Descrição

A URL raiz da aplicação (`/`) não estava mapeada em `core/urls.py`. Qualquer usuário que acessasse o endereço base do sistema recebia uma página de erro 404 do Django, sem qualquer orientação de para onde navegar.

### Passos para reproduzir

1. Iniciar o servidor: `python manage.py runserver`
2. Acessar `http://localhost:8000/` no navegador
3. Observar HTTP 404 — "Page not found"

### Comportamento esperado

Redirecionamento automático (HTTP 302) para `/users/login/` quando o usuário não está autenticado, ou para `/dashboard/` quando autenticado.

### Comportamento obtido

```
HTTP 404 Not Found
Using the URLconf defined in core.urls, Django tried these URL patterns:
  admin/
  users/
None of them matched the URL /.
```

### Causa raiz

`core/urls.py` definia apenas as rotas `admin/` e `users/`. Nenhuma entrada cobria o path vazio `''`.

### Correção aplicada

**Arquivo:** `core/urls.py`

```python
# Antes
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]

# Depois
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/users/login/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]
```

### Impacto

Sem a correção, a primeira impressão de qualquer usuário que acesse o sistema é uma tela de erro 404, o que é inaceitável em produção.

---

## B-02

**Título:** `LoginView` exibe formulário de login para usuário já autenticado

**Severidade:** Medium
**Componente:** `users/views.py` — classe `LoginView`
**Status:** Corrigido
**Descoberto em:** TC-11 (1.8.11)
**Data de correção:** 2026-03-06

### Descrição

Após fazer login com sucesso, se o usuário navegar diretamente para `/users/login/`, o formulário de login é exibido novamente (HTTP 200) em vez de redirecionar para o dashboard. Isso ocorre porque o atributo `redirect_authenticated_user` do `django.contrib.auth.views.LoginView` tem valor `False` por padrão e não foi sobrescrito na classe customizada.

### Passos para reproduzir

1. Acessar `http://localhost:8000/users/login/`
2. Fazer login com credenciais válidas (redireciona para `/dashboard/`)
3. Navegar manualmente de volta para `http://localhost:8000/users/login/`
4. Observar que o formulário de login é exibido novamente

### Comportamento esperado

HTTP 302 redirecionando para `LOGIN_REDIRECT_URL` (`/dashboard/`), pois o usuário já possui sessão ativa.

### Comportamento obtido

HTTP 200 com o formulário de login renderizado, mesmo com o usuário autenticado. Isso cria uma experiência confusa e potencialmente permite que o usuário tente logar uma segunda vez, gerando uma segunda sessão desnecessária.

### Causa raiz

`django.contrib.auth.views.LoginView` possui o atributo de classe:

```python
redirect_authenticated_user = False  # padrão do Django
```

A `LoginView` customizada em `users/views.py` não sobrescrevia esse atributo:

```python
# Antes — sem redirect_authenticated_user
class LoginView(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
```

### Correção aplicada

**Arquivo:** `users/views.py`

```python
# Depois
class LoginView(auth_views.LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
```

### Impacto

Sem a correção, usuários autenticados que voltam para a tela de login ficam em um estado inconsistente. Em cenários com múltiplas abas abertas, isso pode gerar confusão sobre o estado de autenticação da sessão.

---

## B-03

**Título:** Mensagem de erro de login contém espaço duplo no texto em pt-BR

**Severidade:** Low
**Componente:** `users/forms.py` — classe `UserLoginForm`
**Status:** Corrigido
**Descoberto em:** TC-09 (1.8.9)
**Data de correção:** 2026-03-06

### Descrição

Ao tentar fazer login com credenciais inválidas, a mensagem de erro exibida ao usuário continha um espaço duplo entre as palavras "email" e "e senha":

```
"Por favor, entre com um email  e senha corretos."
                                ^
                          espaço duplo aqui
```

### Passos para reproduzir

1. Acessar `/users/login/`
2. Inserir e-mail ou senha incorretos
3. Submeter o formulário
4. Observar a mensagem de erro — há dois espaços consecutivos

### Comportamento esperado

Mensagem de erro clara, sem artefatos visuais, em português correto.

### Comportamento obtido

```
"Por favor, entre com um email  e senha corretos."
```

### Causa raiz

A string de erro padrão do Django para `AuthenticationForm` usa interpolação de variável:

```python
# Django internals (django/contrib/auth/forms.py)
error_messages = {
    'invalid_login': _(
        "Please enter a correct %(username)s and password."
    ),
    ...
}
```

Na tradução pt-BR do Django, essa string é traduzida como:

```
"Por favor, entre com um %(username)s e senha corretos."
```

O `%(username)s` é preenchido com o `verbose_name` do campo `username` do modelo, que neste caso é a string `"email"` — mas com um espaço à direita incluído na interpolação pelo mecanismo de tradução, resultando em `"email "` seguido do texto `" e senha"`, gerando dois espaços consecutivos.

### Correção aplicada

**Arquivo:** `users/forms.py`

```python
# Antes — sem error_messages, herdava o comportamento do Django
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(...)
    password = forms.CharField(...)

# Depois — com error_messages explícitos em pt-BR
class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'E-mail ou senha incorretos. Verifique seus dados e tente novamente.',
        'inactive': 'Esta conta está inativa.',
    }
    username = forms.EmailField(...)
    password = forms.CharField(...)
```

### Impacto

Impacto visual e de qualidade percebida. Embora não bloqueante, mensagens de erro com artefatos tipográficos passam uma impressão de falta de cuidado com o produto.

---

## B-04

**Título:** `create_user()` lança `TypeError` — `CustomUserManager` não implementado

**Severidade:** High
**Componente:** `users/models.py` — model `CustomUser`
**Status:** Corrigido
**Descoberto em:** Teste manual de criação de usuário via `manage.py shell`
**Data de correção:** 2026-03-06

### Descrição

Ao tentar criar um usuário programaticamente via `CustomUser.objects.create_user(email=..., password=...)`, o sistema lançava um `TypeError` porque o `UserManager` padrão do Django (herdado de `AbstractUser`) exige o argumento posicional `username`, que não existe no fluxo do `CustomUser`.

Uma segunda tentativa passando `username=''` gerava um `IntegrityError` no banco de dados, pois o campo `username` do `AbstractUser` possui constraint `UNIQUE` — e já havia um registro com `username=''` criado durante os testes automatizados.

### Passos para reproduzir

```python
# Tentativa 1 — TypeError
from users.models import CustomUser
CustomUser.objects.create_user(email='user@test.com', password='Test@1234')
# TypeError: UserManager.create_user() missing 1 required positional argument: 'username'

# Tentativa 2 — IntegrityError
user = CustomUser(email='user@test.com', username='')
user.set_password('Test@1234')
user.save()
# django.db.utils.IntegrityError: UNIQUE constraint failed: users_customuser.username
```

### Comportamento esperado

`CustomUser.objects.create_user(email='user@test.com', password='Test@1234')` deve criar o usuário sem erros.

### Causa raiz

O model `CustomUser` herdou `AbstractUser` e redefiniu `USERNAME_FIELD = 'email'`, mas não criou um `UserManager` customizado. O `UserManager` padrão do Django (`django.contrib.auth.models.UserManager`) ainda exige `username` como primeiro argumento posicional em `create_user()`, pois foi escrito para o model padrão de `AbstractUser`.

```python
# Django internals — UserManager.create_user() original
def create_user(self, username, email=None, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(username, email, password, **extra_fields)
```

Sem um manager customizado, o `CustomUser` ficava em estado inconsistente: o campo `USERNAME_FIELD` apontava para `email`, mas o manager ainda esperava `username`.

### Correção aplicada

**Arquivo:** `users/models.py`

Criado `CustomUserManager` herdando de `BaseUserManager`, substituindo o manager padrão:

```python
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ...
    objects = CustomUserManager()
    ...
```

A estratégia adotada foi definir `username` automaticamente com o valor do `email`, mantendo a constraint `UNIQUE` do campo satisfeita sem expor `username` ao usuário final.

Migration gerada: `users/migrations/0002_alter_customuser_managers.py`

### Impacto

Crítico para qualquer fluxo de criação de usuário fora do formulário web (scripts de seed, testes automatizados, `createsuperuser`, criação via admin). Sem a correção, o sistema seria inutilizável em ambiente de desenvolvimento e impossível de popular com dados iniciais.

---

## Resumo das Correções

| ID | Arquivo modificado | Linha(s) alteradas | Migration necessária |
|----|-------------------|-------------------|----------------------|
| B-01 | `core/urls.py` | +2 (import `RedirectView`, nova rota) | Não |
| B-02 | `users/views.py` | +1 (`redirect_authenticated_user = True`) | Não |
| B-03 | `users/forms.py` | +4 (dict `error_messages`) | Não |
| B-04 | `users/models.py` | +18 (classe `CustomUserManager`) | Sim (`0002_alter_customuser_managers.py`) |
