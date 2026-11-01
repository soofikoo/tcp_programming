from typing import Counter

from sqlalchemy import func, select

from models import Track, Listen, TrackGenre, Like, Subscription

W_LIKE, W_LISTEN = 3, 1
TOP_GENRES = 3
W_SUBSCRIPTION = 2.0
W_POPULARITY = 1.0

def popular_tracks(db, limit: int, exclude: set[int] = frozenset()) -> list[tuple[int, int]]:
    """Самые прослушиваемые треки: [(track_id, число прослушиваний)]"""
    req = (
        select(Track.id, func.count(Listen.id).label("plays"))
        .outerjoin(Listen, Listen.track_id == Track.id)
        .group_by(Track.id)
        .order_by(func.count(Listen.id).desc(), Track.id)
        .limit(limit)
    )
    if exclude:
        req = req.where(Track.id.notin_(exclude))
    return db.execute(req).all()

def genre_scores(db, user_id: int) -> Counter:
    """Интерес пользователя к жанрам: {genre_id: вес}"""
    liked = db.scalars(select(TrackGenre.genre_id)
                       .join(Like, Like.track_id == TrackGenre.track_id)
                       .where(Like.user_id == user_id)).all()
    listened = db.scalars(select(TrackGenre.genre_id)
                          .join(Listen, Listen.track_id == TrackGenre.track_id)
                          .where(Listen.user_id == user_id)).all()
    scores = Counter()
    for g in liked:
        scores[g] += W_LIKE
    for g in listened:
        scores[g] += W_LISTEN
    return scores

def seen_tracks(db, user_id: int) -> set[int]:
    """id треков, с которыми пользователь уже взаимодействовал, их не рекомендуем"""
    liked = db.scalars(select(Like.track_id).where(Like.user_id == user_id)).all()
    listened = db.scalars(select(Listen.track_id).where(Listen.user_id == user_id)).all()
    return set(liked) | set(listened)

def candidate_tracks(db, top_genres: list[int], seen: set[int]) -> dict[int, list[int]]:
    """Кандидаты в рекомендации: {track_id: [его жанры из top_genres]}"""
    rows = db.execute(
        select(TrackGenre.track_id, TrackGenre.genre_id)
        .where(TrackGenre.genre_id.in_(top_genres))
    ).all()
    result: dict[int, list[int]] = {}
    for track_id, genre_id in rows:
        if track_id not in seen:
            if track_id not in result:
                result[track_id] = []
            result[track_id].append(genre_id)
    return result

def subscribed_tracks(db, user_id: int, track_ids: list[int]) -> set[int]:
    """Какие из track_ids принадлежат исполнителям, на которых подписан пользователь"""
    rows = db.scalars(
        select(Track.id)
        .join(Subscription, Subscription.artist_id == Track.artist_id)
        .where(Subscription.subscriber_id == user_id, Track.id.in_(track_ids))
    ).all()
    return set(rows)

def plays_count(db, track_ids: list[int]) -> dict[int, int]:
    """Число прослушиваний каждого трека: {track_id: count}"""
    rows = db.execute(
        select(Listen.track_id, func.count(Listen.id))
        .where (Listen.track_id.in_(track_ids))
        .group_by(Listen.track_id)
    ).all()
    return dict(rows)

def recommend(db, user_id: int, limit: int) -> tuple[list[tuple[int, float, str]], bool]:
    scores = genre_scores(db, user_id)

    if not scores:
        tracks = []
        for tid, plays in popular_tracks(db, limit):
            tracks.append((tid, float(plays), "popular"))
        return tracks, True

    top_genres = []
    for g, _ in scores.most_common(TOP_GENRES):
        top_genres.append(g)
    seen = seen_tracks(db, user_id)
    candidates = candidate_tracks(db, top_genres, seen)

    result: list[tuple[int, float, str]] = []
    if candidates:
        ids = list(candidates)
        subs = subscribed_tracks(db, user_id, ids)
        plays = plays_count(db, ids)
        max_plays = max(plays.values(), default=0) or 1
        for tid, genres in candidates.items():
            # базовая оценка, суммарный интерес пользователя к жанрам трека
            score = 0
            for g in genres:
                score += scores[g]
            reason = "genre"
            # бонус за подписку
            if tid in subs:
                score += W_SUBSCRIPTION
                reason += "+subscription"

            # бонус за популярность
            # нормировка популярности самый прослушиваемый кандидат получает 1.0
            score += W_POPULARITY * plays.get(tid, 0) / max_plays
            result.append((tid, float(score), reason))

        result.sort(key=lambda r: r[1], reverse=True)
        result = result[:limit]

    # Персональных кандидатов меньше, чем нужно (например, все треки любимых жанров
    # уже прослушаны), добиваем популярными, исключая уже показанные и прослушанные/лайкнутые
    if len(result) < limit:
        exclude = seen | {tid for tid, _, _ in result}
        for tid, plays in popular_tracks(db, limit - len(result), exclude):
            result.append((tid, float(plays), "popular"))
    return result, False