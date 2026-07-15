from pydantic import BaseModel, ConfigDict
from datetime import datetime

class QuestionCreate(BaseModel):
    session_id : int 
    question_text : str

class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    question_text : str
    id : int
    created_at : datetime
