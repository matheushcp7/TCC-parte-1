from fastapi import FastAPI, status, Depends
from schemas import Mensagem
import models
from database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/mensagens", status_code=status.HTTP_201_CREATED)
def criar_mensagem(nova_mensagem: Mensagem, db_session: Session = Depends(get_db)):
    mensagem_criada = models.Model_Mensagem(**nova_mensagem.model_dump())
    db_session.add(mensagem_criada)
    db_session.commit()
    db_session.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}