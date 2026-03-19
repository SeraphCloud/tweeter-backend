# Tweeter Backend

API REST de uma rede social estilo Twitter, construída com Django e Django REST Framework.  
O projeto oferece autenticação JWT, feed personalizado com base em seguidores, curtidas, comentários e gerenciamento de perfil de usuário com imagem no Cloudinary.

## Sumário

- [Visão Geral](#visao-geral)
- [Tecnologias](#tecnologias)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pre-requisitos)
- [Configuração de Ambiente](#configuracao-de-ambiente)
- [Como Rodar Localmente](#como-rodar-localmente)
- [Autenticação](#autenticacao)
- [Endpoints da API](#endpoints-da-api)
- [Regras de Negócio Principais](#regras-de-negocio-principais)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Testes e Qualidade](#testes-e-qualidade)
- [Deploy (Main)](#deploy-main)

## Visao Geral

Este backend implementa os recursos centrais de uma aplicação social:

- Cadastro e login de usuários.
- Perfil editável com foto.
- Sistema de seguir/deixar de seguir usuários.
- Feed com posts do próprio usuário e de quem ele segue.
- Curtidas e comentários em posts.

Por padrão, os endpoints exigem autenticação JWT, exceto registro e login.

## Tecnologias

- Python 3
- Django
- Django REST Framework
- Simple JWT (`djangorestframework-simplejwt`)
- PostgreSQL (via `DATABASE_URL` e `dj-database-url`)
- Cloudinary (`cloudinary` e `django-cloudinary-storage`)
- `python-dotenv` para carregar variáveis de ambiente

## Arquitetura do Projeto

- `users`: autenticação, perfil e relacionamento de seguidores.
- `tweets`: posts, curtidas e comentários.
- `tweeter_backend`: configurações globais e roteamento principal.

A autenticação padrão da API é JWT e a permissão padrão é `IsAuthenticated`.

## Funcionalidades

- **Usuários**
  - Registro com senha criptografada.
  - Login com geração de `access` e `refresh token`.
  - Atualização parcial de perfil.
  - Follow/unfollow com endpoint de toggle.
  - Listagem de seguidores e seguindo.

- **Tweets**
  - CRUD de posts.
  - Curtir/descurtir post (toggle).
  - Comentar em post.
  - Feed ordenado por data (`created_at` decrescente).
  - Campo `liked_by_me` e contagem de likes no serializer.

## Pre-requisitos

- Python 3.11+ (recomendado)
- Pip
- Banco PostgreSQL acessível por URL
- Conta Cloudinary (para upload de imagem de perfil)

## Configuracao de Ambiente

Crie um arquivo `.env` na raiz do projeto (não versionado) com:

```env
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Observações:

- O projeto usa `dj_database_url.config(default=os.environ.get('DATABASE_URL'))`.
- O storage de mídia está configurado com `MediaCloudinaryStorage`.
- Em produção, ajuste `DEBUG`, `ALLOWED_HOSTS` e `SECRET_KEY` via variáveis seguras.

## Como Rodar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/SeraphCloud/tweeter-backend.git
cd tweeter-backend
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

3. Instale as dependências do projeto:

```bash
pip install django djangorestframework djangorestframework-simplejwt python-dotenv dj-database-url cloudinary django-cloudinary-storage psycopg2-binary
```

4. Aplique as migrações:

```bash
python manage.py migrate
```

5. Rode o servidor:

```bash
python manage.py runserver
```

API base local: `http://127.0.0.1:8000/api/`

## Autenticacao

Fluxo padrão com JWT:

1. `POST /api/users/register/` para criar usuário.
2. `POST /api/users/login/` para obter `access` e `refresh`.
3. Enviar header nas rotas protegidas:

```http
Authorization: Bearer <access_token>
```

4. `POST /api/users/token/refresh` para renovar o token de acesso.

## Endpoints da API

Base URL: `/api`

### Usuários (`/api/users/`)

- `POST /register/` - cria usuário
- `POST /login/` - autentica e retorna tokens JWT
- `POST /token/refresh` - renova `access token`
- `GET /profile/` - retorna o usuário autenticado
- `PATCH /profile/` - atualiza parcialmente o perfil
- `POST /<pk>/follow/` - alterna seguir/deixar de seguir
- `GET /<pk>/followers/` - lista seguidores do usuário
- `GET /<pk>/following/` - lista usuários seguidos

### Tweets (`/api/tweets/`)

Endpoints padrão de `ModelViewSet`:

- `GET /tweets/`
- `POST /tweets/`
- `GET /tweets/<id>/`
- `PUT /tweets/<id>/`
- `PATCH /tweets/<id>/`
- `DELETE /tweets/<id>/`

Ações customizadas:

- `POST /tweets/<id>/like/` - alterna like/unlike
- `POST /tweets/<id>/comment/` - cria comentário no post

## Regras de Negocio Principais

- Não é permitido seguir a si mesmo.
- O endpoint de follow funciona como toggle:
  - Se já segue, remove relação (`unfollow`).
  - Se não segue, cria relação (`follow`).
- O feed de posts retorna:
  - Posts do usuário autenticado.
  - Posts dos usuários que ele segue.
- Lista de posts vem em ordem decrescente de criação.

## Estrutura de Pastas

```text
tweeter_backend/
├─ manage.py
├─ tweeter_backend/
│  ├─ settings.py
│  └─ urls.py
├─ users/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  ├─ urls.py
│  └─ migrations/
└─ tweets/
   ├─ models.py
   ├─ serializers.py
   ├─ views.py
   ├─ urls.py
   └─ migrations/
```

## Testes e Qualidade

Atualmente o projeto possui estrutura para testes, mas sem suíte completa implementada.

Comandos úteis:

```bash
python manage.py test
python manage.py check
```

## Deploy (Main)

Fluxo recomendado para publicar alterações na `main`:

```bash
git add .
git commit -m "docs: adiciona README completo do projeto"
git push origin main
```

Após o push, sua plataforma de deploy (Render, Railway, Heroku ou outra) deve executar:

- Instalação de dependências
- `python manage.py migrate`
- Inicialização da aplicação Django

Garanta que as variáveis de ambiente de produção (`DATABASE_URL`, `CLOUDINARY_URL`, `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG`) estejam configuradas no provedor.
