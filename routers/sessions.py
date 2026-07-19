from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from core.security import get_current_user
from schemas.sessions import SessionCreate, SessionResponse
from models.interview_sessions import InterviewSession

router = APIRouter()

@router.post("/session", response_model= SessionResponse)
def create_session(session_data: SessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
     new_session = InterviewSession(
        user_id = current_user.id,
        status = "in_progress",
        role = session_data.role
    )

     db.add(new_session)
     db.commit()
     db.refresh(new_session)

     return new_session  
