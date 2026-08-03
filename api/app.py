from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from . import models, schemas, database
from .database import engine, get_db
from .routes import router
from services.qa_service import ask




app = FastAPI()

models.Base.metadata.create_all(engine)

get_db = database.get_db



@router.post('/ask')
def add_question(request: schemas.QACreate,
                 db: Session = Depends(get_db)):

    answer = ask(request.question)
    qa = models.QA(
        question=request.questio,
        answer=answer
    )

    db.add(qa)
    db.commit()
    db.refresh(qa)

    return {
        "question": qa.question,
        "answer": qa.answer,
    }


@router.get('/', response_model=list[schemas.QAOut], status_code=status.HTTP_200_OK)
def show_qa(db: Session = Depends(get_db)):

    qas = db.query(models.QA).all()
    return qas