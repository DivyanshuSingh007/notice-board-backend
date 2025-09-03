# Render Deployment Guide

## Quick Setup

### 1. Connect to GitHub
- Go to [Render Dashboard](https://dashboard.render.com/)
- Click "New +" → "Web Service"
- Connect your GitHub repository: `DivyanshuSingh007/notice-board-backend`

### 2. Configure Service
- **Name**: `notice-board-backend` (or any name you prefer)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn main:app -c gunicorn.conf.py`

### 3. Environment Variables
Set these in Render dashboard:
```
FRONTEND_ORIGINS=https://notice-board-frontend-phi.vercel.app
FRONTEND_ORIGIN_REGEX=https://.*\.vercel\.app$
SECRET_KEY=your-secret-key-here
ALLOW_MAKE_ADMIN=false
```

### 4. Deploy
- Click "Create Web Service"
- Wait for build to complete
- Your backend will be available at: `https://your-service-name.onrender.com`

## Test CORS After Deployment

```bash
# Test preflight
curl -i -X OPTIONS https://your-service-name.onrender.com/auth/register \
  -H "Origin: https://notice-board-frontend-phi.vercel.app" \
  -H "Access-Control-Request-Method: POST"

# Test health endpoint
curl -i https://your-service-name.onrender.com/health \
  -H "Origin: https://notice-board-frontend-phi.vercel.app"
```

## Expected Results
- Preflight should return 200 with CORS headers
- Health endpoint should return 200 with CORS headers
- Registration should work from your frontend

## Troubleshooting
- If CORS still fails, check environment variables are set correctly
- Ensure you're using the new Render URL, not the old Railway one
- Check build logs for any errors during deployment
