# Pirates

Django app na uživatele, týmy a skupiny, s napojením na SSO.

[![code style: Black](https://img.shields.io/badge/code%20style-Black-000000)](https://github.com/psf/black)
[![license MIT](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
![Python Version](https://img.shields.io/pypi/pyversions/pirates)
![Django Version](https://img.shields.io/pypi/djversions/pirates?color=0C4B33)

## Použití

### Settings

Přidat `pirates` do `INSTALLED_APPS`.

### Modely

Jsou k dipozici abstraktní modely pro uživatele, tým a organizační skupinu. Ty
lze doplnit o další fieldy specifické pro aplikaci. Příklad:

```python
from django.db import models
from pirates.models import AbstractUser

class CustomUser(AbstractUser):
    is_friendly = models.BooleanField(default=True)
```

A nezapomenout model pro uživatele nastavit v settings:

```python
AUTH_USER_MODEL = "myapp.CustomUser"
```

### URLs

URL patterns (v současné době pouze pro OpenID Connect) jsou definovány v
`pirates.urls`. Stačí je připojit k URL patterns projektu:

```python
from pirates.urls import urlpatterns as pirates_urlpatterns 

urlpatterns = [
    # URL patterns projektu
    # ...
] + pirates_urlpatterns

```

### SSO přes OpenID Connect

Implementaci OpenID zajišťuje knihovna
[mozilla-django-oidc](https://github.com/mozilla/mozilla-django-oidc).

V settings projektu je třeba nastavit několik konfiguračních konstant a
autentifikační backend. Příklad settings (s využitím
[django-environ](https://github.com/joke2k/django-environ)):

```python
from os.path import join
import environ

env = environ.Env()

AUTHENTICATION_BACKENDS = ["pirates.auth.PiratesOIDCAuthenticationBackend"]

OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")
OIDC_RP_REALM_URL = env.str("OIDC_RP_REALM_URL")
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_OP_JWKS_ENDPOINT = join(OIDC_RP_REALM_URL, "protocol/openid-connect/certs")
OIDC_OP_AUTHORIZATION_ENDPOINT = join(OIDC_RP_REALM_URL, "protocol/openid-connect/auth")
OIDC_OP_TOKEN_ENDPOINT = join(OIDC_RP_REALM_URL, "protocol/openid-connect/token")
OIDC_OP_USER_ENDPOINT = join(OIDC_RP_REALM_URL, "protocol/openid-connect/userinfo")
```

URL patterns pro OpenID Connect už jsou součástí `pirates.urls` (viz výše).

#### Signál po přihlášení

Po přihlášení uživatele je poslán signál `pirates.signals.post_login` s
parametry:

* `sender` - `PiratesOIDCAuthenticationBackend`
* `user` - přihlášený uživatel (instance `AUTH_USER_MODEL`)
* `created` - `True`/`False` zda-li byl vytvořen nový uživatel
* `request` - instance `HttpRequest`
