from fastapi import APIRouter, Depends, HTTPException, UploadFile , File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from core.security import get_current_user
from schemas.sessions import SessionResponse
from models.interview_sessions import InterviewSession
from models.questions import Question
from services.gemini import generate_questions

router = APIRouter()

@router.post("/session", response_model= SessionResponse)
def create_session(current_user: User = Depends(get_current_user),
                   role: str = Form(),
                   job_description :  str = Form(),
                   resume_file : UploadFile = File(),
                   db: Session = Depends(get_db)):
     if not resume_file.filename.endswith(('.pdf', '.docx', '.txt')):
          raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, or TXT allowed.")
     
     try:
          files = resume_file.file.read()
          resume_content = files.decode("utf-8")
     except Exception:
          resume_content = (f"Uploaded file : {resume_file.filename}")     

     new_session = InterviewSession(
        User_id = current_user.id,
        status = "in_progress",
        role = role,
        resume_text = resume_content
    )

     db.add(new_session)
     db.commit()
     db.refresh(new_session)

     ai_questions = generate_questions(
        role=role,
        job_description=job_description,
        resume_text=resume_content,
        count=5
    )
     
     for q_text in ai_questions:
        question_entry = Question(
            session_id=new_session.id,
            question_text=q_text
        )
        db.add(question_entry)

     db.commit()

     return new_session  
