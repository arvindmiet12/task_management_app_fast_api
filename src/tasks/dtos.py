from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreateDTO(BaseModel):
    title: str
    description: str 
    status: str = "pending"



    ##created_at: datetime = datetime.now()
    ##updated_at: datetime = datetime.now()   