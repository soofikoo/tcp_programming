from sqlalchemy import select

from database import Session
from models import User, Genre, Album, Track
from services.albums_service import get_album_by_track

from services.user_service import get_users
from services.artist_profiles_service import get_artist, update_artist, get_artist_page
from services.tracks_service import get_track_player, get_track_list_by_genre
from services.track_genres_service import get_track_genres
from services.likes_service import create_like, delete_like, get_likes_user, is_like_track, get_liked_track
from services.listens_service import create_listen, get_list_user_Listen, count_track_Listen
from services.subscriptions_service import create_subscription, count_subscription_by_artist, get_subscription_by_user


def run_demo() -> None:
    with Session() as session:
        listener = session.execute(select(User).where(User.username == "pixsele")).scalar_one()
        artist_user = session.execute(select(User).where(User.username == "oxxxymiron")).scalar_one()
        album = session.execute(select(Album).where(Album.title == "Горгород")).scalar_one()
        album_track = session.execute(
            select(Track).where(Track.album_id == album.id)
        ).scalars().first()
        genre = session.execute(select(Genre).where(Genre.name == "rap")).scalar_one()

        print("Получить профиль пользователя")
        print(get_users(session, listener.id))

        print("Инфа о треке для плеера")
        print(get_track_player(session, album_track.id))

        print("История прослушиваний")
        listen = create_listen(session, user_id=listener.id, track_id=album_track.id)
        print(f"listen создан: user={listen.user_id}, track={listen.track_id}, время={listen.created_at}")
        print("история прослушиваний юзера:", get_list_user_Listen(session, listener.id))
        print("сколько раз трек прослушан всего:", count_track_Listen(session, album_track.id))

        print("Лайки тестим")
        if not is_like_track(session, track_id=album_track.id, user_id=listener.id):
            create_like(session, user_id=listener.id, track_id=album_track.id)
        print("лайкнул ли юзер трек:", is_like_track(session, track_id=album_track.id, user_id=listener.id))
        print("лайки юзера (id):", get_likes_user(session, listener.id))
        print("лайкнутые треки (с инфой для UI):", get_liked_track(session, listener.id))

        delete_like(session, user_id=listener.id, track_id=album_track.id)
        print("после снятия лайка:", is_like_track(session, track_id=album_track.id, user_id=listener.id))
        create_like(session, user_id=listener.id, track_id=album_track.id)

        print("Подсписка")
        try:
            create_subscription(session, subscription_id=listener.id, artist_id=artist_user.id)
            print(f"{listener.username} подписался на {artist_user.username}")
        except ValueError:
            print("подписка уже существует")
        print("подписчиков у артиста:", count_subscription_by_artist(session, artist_user.id))

        print("Жанры трека")
        print(get_track_genres(session, album_track.id))

        print("Треки по жанру")
        print(get_track_list_by_genre(session, [genre.id]))

        print("Профиль артиста обновление")
        print(get_artist(session, artist_user.id))
        update_artist(session, artist_user.id, bio="Обновлённое био — демонстрация update_artist")
        print("bio после обновления:", get_artist(session, artist_user.id).bio)

        print("Альбом по треку")
        print(get_album_by_track(session, album_track.id))

        print("Профиль артиста")

        print(get_artist_page(session, artist_user.id))

        print("Подписки по юзеру")
        print(get_subscription_by_user(session, 1))

if __name__ == "__main__":
    run_demo()