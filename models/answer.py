from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Text, Integer, DateTime, Float
from database import Base
from sqlalchemy import ForeignKey

class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, index= True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text, nullable=False )
    ai_feedback = Column(Text)
    score = Column(Float)
    created_at = Column(DateTime(timezone= True), server_default= func.now())
    question = relationship("Question", back_populates="answer")
    


