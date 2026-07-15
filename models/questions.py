from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy import Column , Integer, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key= True, index= True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    question_text = Column( Text, nullable = False)
    created_at = Column(DateTime(timezone= True), server_default= func.now())
    session = relationship("InterviewSession", back_populates="questions")
    answer = relationship("Answer", back_populates="question")