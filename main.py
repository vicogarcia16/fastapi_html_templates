from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.database import engine, get_db, SessionLocal
from db import models
from contextlib import asynccontextmanager

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    num_films = db.query(models.Film).count()
    if num_films == 0:
        films = [
            {"name": "Blade Runner","director": "Ridley Scott"},
            {"name": "Pulp Fiction","director": "Quentin Tarantino"},
            {"name": "Mulholland Drive","director": "David Lynch"},
            {"name": "Jurassic Park","director": "Steven Spielberg"},
            {"name": "Tokio Story","director": "Yasujirô Ozu"},
            {"name": "Interstellar","director": "Denis Villeneuve"},
            {"name": "The Wolf of Wall Street","director": "Martin Scorsese"},
            {"name": "Inception","director": "Christopher Nolan"}
        ]
        for film in films:
            db_film = models.Film(**film)
            db.add(db_film)
        db.commit()
    else:
        print(f"{num_films} films already in database")

    yield
    db.close()
 
app = FastAPI(lifespan=lifespan)   

@app.get("/index/", response_class=HTMLResponse)
async def movielist(request: Request, 
                    hx_request: Optional[str] = Header(None),
                    db: Session = Depends(get_db),
                    page: int = 1
                    ):
    N = 2
    OFFSET = (page - 1) * N
    films = db.query(models.Film).offset(OFFSET).limit(N).all()
    context = {"request": request, "films": films, "page": page}
    if hx_request:
        return templates.TemplateResponse("table.html", context=context)
    return templates.TemplateResponse("index.html", context=context)