# Railway Deployment Guide

This guide will help you deploy your NoticeBoardBackend to Railway.

## Prerequisites

1. **GitHub Repository**: Your code should be pushed to a GitHub repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **Environment Variables**: Prepare your environment variables

## Step 1: Prepare Your Repository

Your repository should already have these files:
- ✅ `requirements.txt` - Python dependencies
- ✅ `main.py` - FastAPI application entry point
- ✅ `railway.json` - Railway configuration
- ✅ `gunicorn.conf.py` - Gunicorn configuration
- ✅ `Procfile` - Process definition

## Step 2: Set Up Railway Project

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your NoticeBoardBackend repository

3. **Configure Environment Variables**
   - Go to your project's "Variables" tab
   - Add the following environment variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///./notice.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration (update with your frontend URL)
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com

# Email Configuration (Optional - for notifications)
RESEND_API_KEY=re_your-resend-api-key-here
MAIL_FROM=your-verified-email@yourdomain.com

# SMS Configuration (Optional - for notifications)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
```

## Step 3: Deploy

1. **Automatic Deployment**
   - Railway will automatically detect your Python app
   - It will use the `railway.json` configuration
   - The app will be built and deployed automatically

2. **Monitor Deployment**
   - Check the "Deployments" tab for build logs
   - Monitor the "Logs" tab for runtime logs

## Step 4: Verify Deployment

1. **Check Health Endpoint**
   - Visit: `https://your-app-name.railway.app/`
   - Should return: `{"message": "Notice Board Backend API", "status": "healthy", "timestamp": "..."}`

2. **Check API Documentation**
   - Visit: `https://your-app-name.railway.app/docs`
   - Should show FastAPI interactive documentation

3. **Test API Endpoints**
   - Try: `https://your-app-name.railway.app/notice/`
   - Should return notices (empty array if no notices)

## Step 5: Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to "Settings" tab
   - Click "Add Domain"
   - Enter your domain name
   - Update DNS records as instructed

2. **Update CORS Settings**
   - Update `ALLOWED_ORIGINS` in environment variables
   - Include your custom domain

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct dependencies
   - Verify Python version compatibility
   - Check build logs in Railway dashboard

2. **App Won't Start**
   - Check if `gunicorn.conf.py` exists
   - Verify `main.py` has correct FastAPI app instance
   - Check runtime logs in Railway dashboard

3. **Database Issues**
   - SQLite database will be created automatically
   - For production, consider using Railway's PostgreSQL service

4. **Environment Variables**
   - Ensure all required variables are set
   - Check variable names match your code
   - Restart deployment after changing variables

### Logs and Debugging

1. **View Logs**
   - Go to "Logs" tab in Railway dashboard
   - Check for error messages
   - Monitor application startup

2. **Common Error Messages**
   - `ModuleNotFoundError`: Check `requirements.txt`
   - `Port already in use`: Railway handles this automatically
   - `Database connection failed`: Check `DATABASE_URL`

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | Database connection string | `sqlite:///./notice.db` |
| `SECRET_KEY` | Yes | JWT secret key | `your-super-secret-key` |
| `ALGORITHM` | Yes | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Yes | Token expiration time | `30` |
| `HOST` | Yes | Server host | `0.0.0.0` |
| `PORT` | Yes | Server port | `8000` |
| `ALLOWED_ORIGINS` | Yes | CORS allowed origins | `http://localhost:5173` |
| `RESEND_API_KEY` | No | Email service API key | `re_...` |
| `MAIL_FROM` | No | Sender email address | `noreply@yourdomain.com` |
| `TWILIO_ACCOUNT_SID` | No | Twilio account SID | `AC...` |
| `TWILIO_AUTH_TOKEN` | No | Twilio auth token | `...` |
| `TWILIO_PHONE_NUMBER` | No | Twilio phone number | `+1234567890` |

## API Endpoints

After deployment, your API will be available at:
- **Base URL**: `https://your-app-name.railway.app`
- **API Docs**: `https://your-app-name.railway.app/docs`
- **Health Check**: `https://your-app-name.railway.app/health`

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout user

### Notice Endpoints (Admin only)
- `GET /notice/` - Get all notices
- `POST /notice/` - Create new notice
- `GET /notice/{id}` - Get specific notice
- `PUT /notice/{id}` - Update notice
- `DELETE /notice/{id}` - Delete notice

## Monitoring and Maintenance

1. **Automatic Scaling**
   - Railway automatically scales based on traffic
   - No manual configuration needed

2. **Logs and Monitoring**
   - View logs in Railway dashboard
   - Monitor resource usage
   - Set up alerts if needed

3. **Updates**
   - Push changes to GitHub
   - Railway automatically redeploys
   - Zero-downtime deployments

## Support

If you encounter issues:
1. Check Railway documentation: [docs.railway.app](https://docs.railway.app)
2. Review build and runtime logs
3. Verify environment variables
4. Test locally before deploying 