from fastapi import FastAPI, status, Depends, Request
from schemas import Mensagem
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
 'http://localhost:3000'
]

app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=['*'],
 allow_headers=['*']
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    mensagens = db.query(models.Model_Mensagem).all()
    return templates.TemplateResponse(request=request, name="index.html", context={"mensagens": mensagens})

@app.get("/mensagens", response_model=List[Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int=100):
    mensagens = db.query(models.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens

@app.post("/mensagens", status_code=status.HTTP_201_CREATED)
def criar_mensagem(nova_mensagem: Mensagem, db_session: Session = Depends(get_db)):
    mensagem_criada = models.Model_Mensagem(**nova_mensagem.model_dump())
    db_session.add(mensagem_criada)
    db_session.commit()
    db_session.refresh(mensagem_criada)
    return {"message": mensagem_criada}