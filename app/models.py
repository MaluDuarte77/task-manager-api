from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)

  tasks = relationship("Task", back_populates="owner")


class Task(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True, nullable=False)
  description = Column(String, nullable=True)
  completed = Column(Boolean, default=False)
  owner_id = Column(Integer, ForeignKey("users.id"))

  owner = relationship("User", back_populates="tasks")
