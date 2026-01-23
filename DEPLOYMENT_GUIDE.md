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

## Database Migration

After deployment, you'll need to run database migrations:

1. In your Render dashboard, go to your service
2. Click on **Shell** or **SSH** (depending on your plan)
3. Run:
   ```bash
   python manage.py migrate
   ```

## Creating a Superuser (Optional)

If you need admin access:
1. Use the Render shell/SSH
2. Run:
   ```bash
   python manage.py createsuperuser
   ```

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