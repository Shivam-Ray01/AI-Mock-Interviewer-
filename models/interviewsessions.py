from sqlalchemy import Column, Integer , String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from database import Base

__tablename__= "interviewsessios"
class InterviewSession(Base):
    id = Column(Integer, primary_key= True, index=True  )
    User_id = Column(Integer,ForeignKey("users.id"))

