from sqlalchemy import Column, Integer , String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from database import Base

class InterviewSession(Base):
    __tablename__= "interview_sessions"
    id = Column(Integer, primary_key= True, index=True  )
    User_id = Column(Integer,ForeignKey("Users.id"))
    status = Column( String(50), nullable = False)
    created_at = Column(DateTime(timezone= True), server_default= func.now())
    user = relationship("User", back_populates="sessions")   
    questions = relationship("Question", back_populates= "session") 
