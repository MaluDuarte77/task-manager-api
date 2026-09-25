from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
  email: EmailStr
  password: str


class UserResponse(BaseModel):
  id: int
  email: str

  class Config:
    from_attributes = True


class TaskCreate(BaseModel):
  title: str
  description: str | None = None


class TaskResponse(TaskCreate):
  id: int
  completed: bool
  owner_id: int

  class Config:
    from_attributes = True
