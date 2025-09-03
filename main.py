from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from notice import router as notice_router, delete_expired_notices
import asyncio
import threading
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from db import BASE, engine
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv()

# Global variable to control the cleanup thread
cleanup_thread = None
stop_cleanup = False

def periodic_cleanup():
    """
    Background thread that runs cleanup every 24 hours
    """
    global stop_cleanup
    while not stop_cleanup:
        try:
            # Run cleanup
            delete_expired_notices()
            # Sleep for 24 hours (86400 seconds)
            time.sleep(86400)
        except Exception as e:
            print(f"Error in periodic cleanup: {e}")
            # If there's an error, wait 1 hour before trying again
            time.sleep(3600)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global cleanup_thread, stop_cleanup
    stop_cleanup = False
    # Startup logic
    cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
    cleanup_thread.start()
    print("Automatic notice cleanup started - will run every 24 hours")
    BASE.metadata.create_all(bind=engine)
    print("Database tables checked/created")
    yield
    # Shutdown logic
    stop_cleanup = True
    if cleanup_thread:
        cleanup_thread.join(timeout=5)

app = FastAPI(lifespan=lifespan)

# Add CORS middleware for frontend development and production
frontend_origins_env = os.getenv("FRONTEND_ORIGINS", "").strip()
if frontend_origins_env:
    allow_origins = [o.strip() for o in frontend_origins_env.split(",") if o.strip()]
else:
    # Sensible defaults; override via FRONTEND_ORIGINS
    allow_origins = [
        "https://notice-board-frontend-p4doxnki0-divyanshusingh007s-projects.vercel.app",
        "https://notice-board-frontend-phi.vercel.app",
        "http://notice-board-frontend-phi.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:4173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
async def root():
    """
    Health check endpoint for Railway
    """
    return {
        "message": "Notice Board Backend API",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for Railway
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """
    Handle OPTIONS requests for CORS preflight
    """
    return {"message": "OK"}

# Register routers
app.include_router(auth_router)
app.include_router(notice_router)
