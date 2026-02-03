# Tweeter API

Uma API RESTful para uma rede social estilo Twitter, construída com Django e Django REST Framework.

## 🔗 Deploy

**URL Base:** [https://tweeter-backend-tex8.onrender.com](https://tweeter-backend-tex8.onrender.com)

---

## 🚀 Guia Rápido

### Pré-requisitos

- Python 3.10+
- pip ou poetry

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd tweeter
   ```

2. **Instale as dependências:**
   ```bash
   # Usando poetry (recomendado)
   poetry install

   # Ou usando pip
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` no diretório raiz:
   ```env
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost 127.0.0.1
   ```

4. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

A API estará disponível em `http://localhost:8000`

---

## 📚 Endpoints da API

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-------------|
| POST | `/api/register/` | Registrar novo usuário |
| POST | `/api/token/` | Obter token de acesso JWT |
| POST | `/api/token/refresh/` | Renovar token de acesso JWT |

### Perfis

| Método | Endpoint | Descrição |
|--------|----------|-------------|
| GET | `/api/profiles/` | Listar todos os perfis |
| GET | `/api/profiles/{id}/` | Recuperar um perfil específico |
| PUT/PATCH | `/api/profiles/{id}/` | Atualizar um perfil |
| DELETE | `/api/profiles/{id}/` | Excluir um perfil |

### Posts

| Método | Endpoint | Descrição |
|--------|----------|-------------|
| GET | `/api/posts/` | Listar todos os posts |
| POST | `/api/posts/` | Criar um novo post |
| GET | `/api/posts/{id}/` | Recuperar um post específico |
| PUT/PATCH | `/api/posts/{id}/` | Atualizar um post |
| DELETE | `/api/posts/{id}/` | Excluir um post |

### Comentários

| Método | Endpoint | Descrição |
|--------|----------|-------------|
| GET | `/api/comments/` | Listar todos os comentários |
| POST | `/api/comments/` | Criar um novo comentário |
| GET | `/api/comments/{id}/` | Recuperar um comentário específico |
| PUT/PATCH | `/api/comments/{id}/` | Atualizar um comentário |
| DELETE | `/api/comments/{id}/` | Excluir um comentário |

---

## 🔐 Autenticação

Esta API usa autenticação JWT (JSON Web Token) através do `djangorestframework-simplejwt`.

### Obtendo um Token

**Requisição:**
```bash
POST /api/token/
Content-Type: application/json

{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usando o Token

Inclua o token de acesso no cabeçalho Authorization:
```
Authorization: Bearer <seu-token-de-acesso>
```

### Renovando um Token

**Requisição:**
```bash
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "seu-token-refresh"
}
```

---

## 🛠️ Comandos Disponíveis

```bash
# Criar superusuário
python manage.py createsuperuser

# Executar testes
python manage.py test

# Aplicar migrações
python manage.py migrate

# Criar migrações (após alterações nos modelos)
python manage.py makemigrations

# Coletar arquivos estáticos (produção)
python manage.py collectstatic

# Criar dados iniciais
python manage.py seed_users
```

---

## 🏗️ Tecnologias

- **Framework:** Django 6.0
- **API:** Django REST Framework
- **Autenticação:** JWT (djangorestframework-simplejwt)
- **Banco de Dados:** PostgreSQL (produção) / SQLite (desenvolvimento)
- **Servidor WSGI:** Gunicorn
- **CORS:** django-cors-headers

---

## 📦 Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|----------|-------------|------------|
| `SECRET_KEY` | Sim | Chave secreta do Django |
| `DEBUG` | Não | Modo de debug (padrão: False) |
| `DATABASE_URL` | Não | URL de conexão do banco de dados |
| `ALLOWED_HOSTS` | Não | Lista de hosts permitidos separados por espaço |
| `PORT` | Não | Porta do servidor (produção) |
| `SUPERUSER_USERNAME` | Não | Nome de usuário do admin (criado automaticamente) |
| `SUPERUSER_EMAIL` | Não | Email do admin (criado automaticamente) |
| `SUPERUSER_PASSWORD` | Não | Senha do admin (criado automaticamente) |

---

## 🚀 Deploy no Render

1. Conecte seu repositório GitHub ao Render
2. Crie um novo Web Service
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`
4. Adicione as variáveis de ambiente no painel do Render
5. Faça o deploy!

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.
