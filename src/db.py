from sqlmodel import SQLModel, Session

from models import Users, Scores


def get_scores(user: int, round: int, participant: int) -> dict:
    from main import engine

    with Session(engine) as session:
        values = (
            session.query(Scores)
            .filter(
                Scores.user_id == user,
                Scores.round_number == round,
                Scores.song_id == participant,
            )
            .first()
        )
    if values is None:
        return {"score_costume": 0, "score_show": 0, "score_song": 0}
    return {
        "score_costume": values.score_costume,
        "score_show": values.score_show,
        "score_song": values.score_song,
    }


def set_scores(
    user: int,
    round: int,
    participant: int,
    score_costume: int,
    score_show: int,
    score_song: int,
):
    from main import engine

    with Session(engine) as session:
        # check if score already exists
        values = (
            session.query(Scores)
            .filter(
                Scores.user_id == user,
                Scores.round_number == round,
                Scores.song_id == participant,
            )
            .first()
        )
        if values is not None:
            values.score_costume = score_costume
            values.score_show = score_show
            values.score_song = score_song
            session.commit()
            return
        session.add(
            Scores(
                user_id=user,
                round_number=round,
                song_id=participant,
                score_costume=score_costume,
                score_show=score_show,
                score_song=score_song,
            )
        )
        session.commit()


def get_mean_score(user: int, round: int, participant: int) -> float:
    from main import engine

    with Session(engine) as session:
        values = (
            session.query(Scores)
            .filter(Scores.round_number == round, Scores.song_id == participant)
            .all()
        )
    if len(values) == 0:
        return 0.0
    total: float = 0.0
    for value in values:
        total += value.score_costume
        total += value.score_show
        total += value.score_song
    return total / len(values * 3)
