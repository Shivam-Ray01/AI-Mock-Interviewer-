from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AnswerCreate(BaseModel):
    question_id : int 
    answer_text : str

class AnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    answer_text : str
    id : int 
    ai_feedback : Optional[str] = None
    score : Optional[float]= None
    created_at : datetime    