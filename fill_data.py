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


def get_or_create_user(session, username: str, email: str, role: str) -> User:
    user = session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if user is not None:
        print(f"  = user уже есть: {username}")
        return user
    # В реальности пароль хешируется
    user = create_user(session, username=username, email=email, password="hashed_stub_pw", role=role)
    print(f"  + создан user: {username} ({role})")
    return user


def get_or_create_genre(session, name: str) -> Genre:
    genre = session.execute(select(Genre).where(Genre.name == name)).scalar_one_or_none()
    if genre is not None:
        print(f"  = genre уже есть: {name}")
        return genre
    genre = create_genre(session, name=name)
    print(f"  + создан genre: {name}")
    return genre


def fill() -> None:
    with Session() as session:
        print("Юзер")
        listener = get_or_create_user(session, "pixsele", "pixsele@example.com", "listener")
        artist_user = get_or_create_user(session, "oxxxymiron", "oxxxy@example.com", "artist")

        print("Артист")
        artist_profile = get_artist(session, artist_user.id)
        if artist_profile is None:
            artist_profile = create_artist(session, artist_id=artist_user.id, bio="Российский рэп-исполнитель")
            print(f"  + создан artist_profile для {artist_user.username}")
        else:
            print(f"  = artist_profile уже есть для {artist_user.username}")

        print("Жанры")
        rap = get_or_create_genre(session, "rap")
        rock = get_or_create_genre(session, "rock")
        pop = get_or_create_genre(session, "pop")

        print("Альбомы и треки")
        existing_album = session.execute(
            select(Album).where(Album.title == "Горгород")
        ).scalar_one_or_none()

        if existing_album is not None:
            print("альбом и треки уже есть")
            return

        album = create_album(
            session,
            title="Горгород",
            artist_id=artist_user.id,
            release_date=date(2015, 10, 23),
            cover_url="gorgorod.jpg",
        )
        print(f"создан альбом: {album.title}")

        track1 = create_track(
            session, title="Башня из слоновой кости", album_id=album.id,
            duration=245, file_path="tracks/tower.mp3",
            upload_date=datetime.utcnow(), artist_id=artist_user.id,
        )
        track2 = create_track(
            session, title="Признаки жизни", album_id=album.id,
            duration=198, file_path="tracks/signs.mp3",
            upload_date=datetime.utcnow(), artist_id=artist_user.id,
        )
        print(f"созданы треки: {track1.title}, {track2.title}")

        print("Жанры к трекам")
        create_track_genre(session, track_id=track1.id, genre_id=rap.id)
        create_track_genre(session, track_id=track1.id, genre_id=rock.id)
        create_track_genre(session, track_id=track2.id, genre_id=rap.id)

if __name__ == "__main__":
    fill()