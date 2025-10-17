# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, StringConstraints, constr, conint, ConfigDict
from typing import Annotated

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
StudentID = Annotated[str, constr(pattern=r'^S\d{7}$')]

class UserCreate(BaseModel):
    
    student_id: StudentID # used pattern instead of regex as python v2 no longer uses regex
    name: NameStr
    email: EmailStr
    age: int = Field(gt=18)

class UserRead(BaseModel):
    id: int
    student_id: StudentID
    name: NameStr
    email: EmailStr
    age: int

    model_config = ConfigDict(from_attributes=True)
