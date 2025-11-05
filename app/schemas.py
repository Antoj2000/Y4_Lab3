# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, StringConstraints, constr, conint, ConfigDict
from typing import Annotated

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
StudentID = Annotated[str, constr(pattern=r'^S\d{7}$')]

class UserCreate(BaseModel):
    
   
    name: NameStr
    email: EmailStr
    age: int = Field(gt=18)
    student_id: StudentID

class UserRead(BaseModel):
    id: int
    name: NameStr
    email: EmailStr
    age: int
    student_id: StudentID
 
    model_config = ConfigDict(from_attributes=True)
