from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session as DbSession
from api.routers import genres, auth, login, track, albums, artist_profiles, likes, listens, subscriptions
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
app.include_router(track.router)
app.include_router(albums.router)
app.include_router(artist_profiles.router)
app.include_router(likes.router)
app.include_router(listens.router)
app.include_router(subscriptions.router)
