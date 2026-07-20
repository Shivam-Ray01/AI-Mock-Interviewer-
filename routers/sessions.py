from fastapi import APIRouter, Depends, HTTPException, UploadFile , File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from core.security import get_current_user
from schemas.sessions import SessionCreate, SessionResponse
from models.interview_sessions import InterviewSession

router = APIRouter()

@router.post("/session", response_model= SessionResponse)
def create_session(session_data: SessionCreate, 
                   current_user: User = Depends(get_current_user),
                   role: str = Form(),
                   job_description :  str = Form(),
                   resume_file : UploadFile = File(),
                   db: Session = Depends(get_db)):
     if not resume_file.filename.endswith(('.pdf', '.docx', '.txt')):
          raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, or TXT allowed.")
     
     contents = resume_file.file.read()

     new_session = InterviewSession(
        User_id = current_user.id,
        status = "in_progress",
        role = session_data.role
    )

     db.add(new_session)
     db.commit()
     db.refresh(new_session)

     return new_session  
