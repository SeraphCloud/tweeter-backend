# Tweeter Backend Deployment Guide for Render

This guide will help you deploy your Django REST API to Render successfully.

## Files Created

The following files have been created to support your Render deployment:

### 1. Procfile
```
web: gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```
This tells Render how to run your application using Gunicorn.

### 2. runtime.txt
```
python-3.12.0
```
This specifies the Python version to use.

### 3. Updated backend/settings.py
- Added validation to ensure SECRET_KEY is set
- Improved DEBUG environment variable parsing
- Enhanced error handling for production deployment

## Environment Variables Required

Set these environment variables in your Render dashboard under **Environment** → **Environment Variables**:

### Required Variables
- `SECRET_KEY`: `w34fQ99Mw4MMfMBwoO072SYsPGg5AFpygf0z4ZkFsDi`
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `tweeter-backend-tex8.onrender.com`
- `DATABASE_URL`: `postgresql://victor:ADJeqONYwjJG2yCXStrw9a6uG3SoSCmf@dpg-d5peglvgi27c73fljpg0-a.virginia-postgres.render.com/tweeterdb_k7jw`

### Superuser Variables (Novas)
- `SUPERUSER_USERNAME`: `victor`
- `SUPERUSER_EMAIL`: `victor@teste.com`
- `SUPERUSER_PASSWORD`: `Vsi2025*`

### Optional Variables (if you have a frontend)
- `CORS_ALLOWED_ORIGINS`: Your frontend domain(s) separated by spaces

## Deployment Steps

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Add Render deployment files"
   git push origin main
   ```

2. **Configure Render Service:**
   - Go to your Render dashboard
   - Select your service
   - Under **Environment**, add the required environment variables listed above
   - Under **Advanced**, ensure the build command is set to:
     ```
     python -m pip install --upgrade pip && pip install -r requirements.txt
     ```
   - The start command should be automatically detected from the Procfile

3. **Deploy:**
   - Trigger a new deployment in Render
   - Monitor the logs for any issues

## Database Migration and Superuser Creation (Automático)

**IMPORTANTE:** O script de inicialização agora executa automaticamente as migrações e cria o superusuário durante o deploy!

### Processo Automático:
1. O Render executa automaticamente o script `init_app.py` antes de iniciar a aplicação
2. Esse script executa as migrações do banco de dados
3. Em seguida, cria o superusuário com as credenciais configuradas nas variáveis de ambiente

### Credenciais do Superusuário:
- **Username:** `victor`
- **Email:** `victor@teste.com`
- **Senha:** `Vsi2025*`

### Acesso ao Admin:
Após o deploy, você poderá acessar o admin Django em:
`https://tweeter-backend-tex8.onrender.com/admin/`

Use as credenciais acima para fazer login.

## API Endpoints

Your API is now available at:
- Base URL: `https://tweeter-backend-tex8.onrender.com`
- Authentication: `https://tweeter-backend-tex8.onrender.com/api/auth/token/`
- Posts: `https://tweeter-backend-tex8.onrender.com/api/posts/`
- Profiles: `https://tweeter-backend-tex8.onrender.com/api/profiles/`

## Troubleshooting

### 400 Bad Request Errors
- Ensure all required environment variables are set
- Check that SECRET_KEY is properly configured
- Verify ALLOWED_HOSTS includes your Render domain

### Database Connection Issues
- Ensure DATABASE_URL is correctly set
- Check that the PostgreSQL database is accessible
- Verify database migrations have been run

### CORS Issues
- Set CORS_ALLOWED_ORIGINS if you have a separate frontend
- Ensure your frontend domain is included

## Next Steps

1. Test your API endpoints
2. Set up monitoring and logging as needed
3. Consider setting up a custom domain
4. Configure SSL/TLS (Render handles this automatically)

## Support

If you continue to experience issues:
1. Check the Render deployment logs
2. Verify all environment variables are correctly set
3. Ensure your requirements.txt is up to date
4. Test locally with the same environment variables