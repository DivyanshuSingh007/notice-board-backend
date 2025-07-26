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

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware for frontend development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Development
        "http://localhost:3000",  # Alternative dev port
        "http://notice-board-frontend-phi.vercel.app",  # Vercel frontend
        "https://notice-board-frontend-phi.vercel.app",  # Vercel frontend (HTTPS)
        "https://yourdomain.com",  # Replace with your actual domain
        "https://www.yourdomain.com",  # Replace with your actual domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.on_event("startup")
async def startup_event():
    """
    Start the periodic cleanup thread when the application starts
    """
    global cleanup_thread, stop_cleanup
    stop_cleanup = False
    
    # Start the cleanup thread
    cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
    cleanup_thread.start()
    print("Automatic notice cleanup started - will run every 24 hours")

    # Create all tables if they don't exist
    BASE.metadata.create_all(bind=engine)
    print("Database tables checked/created")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Stop the periodic cleanup thread when the application shuts down
    """
    global stop_cleanup
    stop_cleanup = True
    if cleanup_thread:
        cleanup_thread.join(timeout=5)
    print("Automatic notice cleanup stopped")

app.include_router(auth_router)
app.include_router(notice_router)
