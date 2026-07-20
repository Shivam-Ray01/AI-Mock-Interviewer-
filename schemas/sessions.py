from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class SessionCreate(BaseModel):
    role : str

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    id : int
    status : str
    created_at : datetime
    user_id : int= Field(validation_alias="User_id")
    role : str
    resume_text: Optional[str] = None