from datetime import date, datetime

from sqlalchemy import select

from database import Session
from models import User, Genre, Album

from services.user_service import create_user
from services.artist_profiles_service import create_artist, get_artist
from services.genres_service import create_genre
from services.albums_service import create_album
from services.tracks_service import create_track
from services.track_genres_service import create_track_genre


def fill() -> None:
    with Session() as session:
        print("Юзер")
        listener = create_user(session, "sofiko", "sofiko@example.com", "listener")
        artist_user = create_user(session, "hehehe", "hehehe@example.com", "artist")

        print("Артист")
        artist_profile = get_artist(session, artist_user.id)
        if artist_profile is None:
            artist_profile = create_artist(session, artist_id=artist_user.id, bio="Инди-поп группа из Владивостока")
            print(f"  + создан artist_profile для {artist_user.username}")
        else:
            print(f"  = artist_profile уже есть для {artist_user.username}")

        print("Жанры")
        indie_pop = create_genre(session, "indie_pop")

        print("Альбомы и треки")

        album = create_album(
            session,
            title="Паника",
            artist_id=artist_user.id,
            release_date=date(2024, 6, 13),
            cover_url="panic.jpg",
        )
        print(f"создан альбом: {album.title}")

        track1 = create_track(
            session, title="Очень-очень", album_id=album.id,
            duration=245, file_path="tracks/ochen_ochen.mp3",
            upload_date=datetime.utcnow(), artist_id=artist_user.id,
        )
        track2 = create_track(
            session, title="Ничего страшного", album_id=album.id,
            duration=198, file_path="tracks/nichego_strashnogo.mp3",
            upload_date=datetime.utcnow(), artist_id=artist_user.id,
        )
        print(f"созданы треки: {track1.title}, {track2.title}")

        print("Жанры к трекам")
        create_track_genre(session, track_id=track1.id, genre_id=indie_pop.id)

if __name__ == "__main__":
    fill()