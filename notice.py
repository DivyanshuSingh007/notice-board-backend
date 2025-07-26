from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta
from db import Sessionlocal
from models import Notice, Users
from auth import get_current_user  # Depends on how you structured auth
from dependencies import get_db
from enum import Enum
import logging
from notifications import notification_service

router = APIRouter(prefix="/notice", tags=["Notice"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[Users, Depends(get_current_user)]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define notice types
class NoticeType(str, Enum):
    maintenance = "Maintenance"
    rent_sell = "Rent/Sell"
    meeting = "Meeting"
    event = "Event"
    lost_found = "Lost & Found"
    announcement = "General Announcement"
    security = "Security Alert"
    visitor = "Visitor Information"
    payment = "Payment Reminder"
    service = "Service"
    emergency = "Emergency"
    other = "Other"

def delete_expired_notices():
    """
    Delete notices that have expired (event_date is in the past)
    """
    try:
        db = Sessionlocal()
        today = date.today()
        
        # Find expired notices
        expired_notices = db.query(Notice).filter(
            Notice.event_date < today,
            Notice.event_date.isnot(None)
        ).all()
        
        if expired_notices:
            for notice in expired_notices:
                db.delete(notice)
            db.commit()
            logger.info(f"Deleted {len(expired_notices)} expired notices")
        else:
            logger.info("No expired notices found to delete")
            
    except Exception as e:
        logger.error(f"Error deleting expired notices: {e}")
    finally:
        db.close()

# Pydantic models
class NoticeRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    event_date: Optional[date] = None
    event_start_time: Optional[time] = None
    event_end_time: Optional[time] = None
    type: NoticeType

class NoticeResponse(BaseModel):
    id: int
    title: str
    description: str
    post_date: date
    event_date: Optional[date] = None
    event_start_time: Optional[time] = None
    event_end_time: Optional[time] = None
    type: str
    
    class Config:
        from_attributes = True
        # Handle None values properly
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
            time: lambda v: v.isoformat() if v else None,
        }

@router.post("/", response_model=NoticeResponse)
def create_notice(
    notice_request: NoticeRequest,
    background_tasks: BackgroundTasks,
    db: db_dependency,
    current_user: current_user_dependency
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can post notices")

    notice_data = notice_request.dict()
    notice_data["post_date"] = date.today()
    notice = Notice(**notice_data)
    db.add(notice)
    db.commit()
    db.refresh(notice)
    
    # Prepare notice data for notifications
    notification_data = {
        "title": notice.title,
        "description": notice.description,
        "type": notice.type,
        "post_date": notice.post_date.isoformat(),
        "event_date": notice.event_date.isoformat() if notice.event_date else None,
        "event_start_time": notice.event_start_time.isoformat() if notice.event_start_time else None,
        "event_end_time": notice.event_end_time.isoformat() if notice.event_end_time else None,
    }
    
    # Add background tasks
    background_tasks.add_task(delete_expired_notices)
    background_tasks.add_task(notification_service.notify_all_users, db, notification_data)
    
    logger.info(f"Notice created by {current_user.email}.")
    
    return notice

@router.get("/", response_model=List[NoticeResponse])
def get_all_notices(db: db_dependency):
    # Check for expired notices before returning the list
    delete_expired_notices()
    notices = db.query(Notice).all()
    
    # Convert to response models manually to handle NULL values
    response_notices = []
    for notice in notices:
        notice_dict = {
            "id": notice.id,
            "title": notice.title,
            "description": notice.description,
            "post_date": notice.post_date,
            "event_date": notice.event_date,
            "event_start_time": notice.event_start_time,
            "event_end_time": notice.event_end_time,
            "type": notice.type
        }
        response_notices.append(NoticeResponse(**notice_dict))
    
    return response_notices

@router.get("/{notice_id}", response_model=NoticeResponse)
def get_notice_by_id(notice_id: int, db: db_dependency):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.put("/{notice_id}", response_model=NoticeResponse)
def update_notice(
    notice_id: int,
    notice_request: NoticeRequest,
    background_tasks: BackgroundTasks,
    db: db_dependency,
    current_user: current_user_dependency
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can update notices")

    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    # Only update fields from NoticeRequest (not post_date)
    update_data = notice_request.dict()
    for key, value in update_data.items():
        setattr(notice, key, value)
    
    db.commit()
    db.refresh(notice)
    
    # Add background task to check for expired notices
    background_tasks.add_task(delete_expired_notices)
    
    return notice

@router.delete("/{notice_id}")
def delete_notice(
    notice_id: int,
    db: db_dependency,
    current_user: current_user_dependency
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete notices")

    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    db.delete(notice)
    db.commit()
    
    return {"message": "Notice deleted successfully"}

@router.post("/cleanup-expired")
def cleanup_expired_notices(
    background_tasks: BackgroundTasks,
    current_user: current_user_dependency
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can trigger cleanup")
    
    # Add background task to delete expired notices
    background_tasks.add_task(delete_expired_notices)
    
    return {"message": "Cleanup task scheduled"}

@router.post("/test-notifications")
async def test_notifications(
    background_tasks: BackgroundTasks,
    current_user: current_user_dependency,
    db: db_dependency
):
    """Test endpoint to send notifications to all users"""
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Only admins can test notifications")
    
    # Test notice data
    test_notice_data = {
        "title": "Test Notice - Notification System",
        "description": "This is a test notice to verify that the email and SMS notification system is working correctly.",
        "type": "announcement",
        "post_date": date.today().isoformat(),
        "event_date": None,
        "event_start_time": None,
        "event_end_time": None,
    }
    
    # Send notifications in background
    background_tasks.add_task(notification_service.notify_all_users, db, test_notice_data)
    
    return {
        "message": "Test notifications sent to all registered users",
        "notice_data": test_notice_data
    }
