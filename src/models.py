from sqlmodel import SQLModel, Field, ForeignKey


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str


class Scores(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    song_id: int
    round_number: int
    score_costume: int
    score_show: int
    score_song: int
