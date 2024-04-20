from sqlmodel import SQLModel, Field, ForeignKey


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    profile_picture: int = Field(default=1)


class Scores(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    participant_id: int
    round_number: int
    score_costume: int
    score_show: int
    score_song: int

class Participants(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    country: str
    country_img: str
    name: str
    song: str
    img: str
    url: str
    round: int
    turn: int