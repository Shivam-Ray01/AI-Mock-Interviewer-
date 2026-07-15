from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SessionCreate(BaseModel):
    user_id : int

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    id : int
    status : str
    created_at : datetime
    user_id : int