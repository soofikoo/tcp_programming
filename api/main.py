from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session as DbSession
from api.routers import genres, auth, login
from api.deps import get_db
from api.schemas.genre import GenreOut
from services.genres_service import get_genre

app = FastAPI(title="Music API")

@app.get("/ping")
def ping():
    return {"status": "ok"}

app.include_router(genres.router)
app.include_router(auth.router)
app.include_router(login.router)
