from fastapi import FastAPI

from api.routers import genres, auth, tracks, albums, artists, users

app = FastAPI(title="Music API")

@app.get("/ping")
def ping():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(genres.router)
app.include_router(albums.router)
app.include_router(tracks.router)
app.include_router(artists.router)