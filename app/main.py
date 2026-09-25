from app import models, schemas
from app.database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="API profissional para gestão de tarefas",
    version="1.0.0",
)


@app.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = (
      db.query(models.User).filter(models.User.email == user.email).first()
  )
  if db_user:
    raise HTTPException(status_code=400, detail="Email já cadastrado")

  fake_hashed_password = user.password + "notreallyencrypted"
  new_user = models.User(email=user.email, hashed_password=fake_hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@app.post(
    "/tasks/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate, user_id: int, db: Session = Depends(get_db)
):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

  new_task = models.Task(**task.dict(), owner_id=user_id)
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  return new_task


@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def list_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
  tasks = db.query(models.Task).offset(skip).limit(limit).all()
  return tasks
