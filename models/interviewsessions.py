from sqlalchemy import Column, Integer , String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from database import Base

class InterviewSession(Base):
    __tablename__= "interviewsessios"
    id = Column(Integer, primary_key= True, index=True  )
    User_id = Column(Integer,ForeignKey("users.id"))
    status = Column( str(50), nullable = False)
    created_at = DateTime(timezone= True)

user = relationship("User", back_populates="sessions")    
