# Notice Board Backend API

A FastAPI-based backend for a notice board application with user authentication and notice management.

## Features

- 🔐 JWT-based authentication
- 📝 CRUD operations for notices
- 👥 User management with admin roles
- 🗓️ Event scheduling with date/time
- 🧹 Automatic cleanup of expired notices
- 🔒 Role-based access control

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for deployment)
- Domain name (for production)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd NoticeBoardBackend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Deployment Options

### Option 1: Docker Deployment (Recommended)

1. **Update configuration**
   - Edit `nginx.conf` and replace `yourdomain.com` with your actual domain
   - Update `docker-compose.yml` with your domain in `ALLOWED_ORIGINS`

2. **Deploy with SSL**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Manual deployment**
   ```bash
   docker-compose up -d --build
   ```

### Option 2: VPS Deployment

1. **Set up your VPS**
   - Ubuntu 20.04+ recommended
   - Install Docker and Docker Compose

2. **Upload your code**
   ```bash
   scp -r . user@your-server:/home/user/noticeboard
   ```

3. **SSH into your server**
   ```bash
   ssh user@your-server
   cd noticeboard
   ```

4. **Deploy**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Option 3: Platform as a Service

#### Railway
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

#### Render
1. Create a new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn main:app -c gunicorn.conf.py`

## Environment Variables

Create a `.env` file based on `env_example.txt`:

```env
DATABASE_URL=sqlite:///./notice.db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info
- `POST /auth/logout` - Logout user

### Notices (Admin only)
- `GET /notice/` - Get all notices
- `POST /notice/` - Create new notice
- `GET /notice/{id}` - Get specific notice
- `PUT /notice/{id}` - Update notice
- `DELETE /notice/{id}` - Delete notice

## Security Features

- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ CORS protection
- ✅ Rate limiting
- ✅ SSL/TLS encryption
- ✅ Security headers
- ✅ Role-based access control

## Monitoring

- Health check: `GET /health`
- Application logs: `docker-compose logs -f app`
- Nginx logs: `docker-compose logs -f nginx`

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **SSL certificate issues**
   ```bash
   # For Let's Encrypt
   certbot certonly --standalone -d yourdomain.com
   ```

3. **Database issues**
   ```bash
   # Reset database
   rm notice.db
   # Restart application
   docker-compose restart app
   ```

## Support

For issues and questions:
- Check the logs: `docker-compose logs`
- Review the API docs: `http://localhost:8000/docs`
- Open an issue on GitHub 