from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI, Request, Response, Cookie, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from rich import print
import os
import pathlib

from models import Users, Scores, Participants
from db import get_scores, set_scores, get_mean_score, populate_db

app = FastAPI()
load_dotenv()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# SQL Model

if not pathlib.Path("database").exists():
    pathlib.Path("database").mkdir()
engine = create_engine("sqlite:///database/data.sqlite")
SQLModel.metadata.create_all(engine)
populate_db()

# Routes


@app.get("/")
async def index(request: Request, response: Response):
    if request.cookies.get("user") is None:
        return RedirectResponse("/login")
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login")
async def login(request: Request, response: Response):
    users = []
    with Session(engine) as session:
        users = session.query(Users).all()
    print(users)
    return templates.TemplateResponse(
        "login.html", {"request": request, "users": users}
    )


@app.get("/login/{id}")
async def loginUser(request: Request, response: Response, id: str = None):
    resp = RedirectResponse("/")
    resp.set_cookie(key="user", value=id)
    return resp


@app.get("/contest/{round_number}")
async def contest(request: Request, response: Response, round_number: int = 1):
    
    # Check if user is logged in
    if request.cookies.get("user") is None:
        return RedirectResponse("/login")
    
    # Initialize variables
    round_names = {1: "1. Semifinaali", 2: "2. Semifinaali", 3: "Finaali"}
    round_data = {
        "round_name": round_names[round_number],
        "partisipants": [],
    }

    # Get scores
    with Session(engine) as session:
        participant_list = session.query(Participants).filter(Participants.round == round_number).order_by(Participants.turn).all()

        for participant in participant_list:
            participant_data = participant.dict()
            participant_data["mean_score"] = get_mean_score(int(request.cookies.get("user")), round_number, participant.id)
            round_data["partisipants"].append(participant_data)

    resp = templates.TemplateResponse(
        "contest.html", {"request": request, "round_data": round_data}
    )
    resp.set_cookie(key="round", value=str(round_number))
    return resp


@app.get("/participant/{id}")
def participant(request: Request, response: Response, id: int = None):
    if request.cookies.get("user") is None:
        return RedirectResponse("/login")
    if request.cookies.get("round") is None:
        return RedirectResponse("/")
    scores = get_scores(
        int(request.cookies.get("user")), int(request.cookies.get("round")), int(id)
    )
    with Session(engine) as session:
        participant_info = session.query(Participants).filter(Participants.id == id).first()
    #participant_info = get_participant(int(id))
    return templates.TemplateResponse(
        "participant.html",
        {
            "request": request,
            "participant_info": participant_info,
            "scores": scores,
            "round": request.cookies.get("round"),
        },
    )


@app.post("/participant/{id}")
def participant(
    request: Request,
    response: Response,
    id: int = None,
    score_song: int = Form(...),
    score_costume: int = Form(...),
    score_show: int = Form(...),
):
    if request.cookies.get("user") is None:
        return RedirectResponse("/login")
    if request.cookies.get("round") is None:
        return RedirectResponse("/")
    with Session(engine) as session:
        participant_info = session.query(Participants).filter(Participants.id == id).first()

    if participant_info is None:
        return RedirectResponse("/")

    set_scores(
        int(request.cookies.get("user")),
        int(request.cookies.get("round")),
        int(id),
        score_costume,
        score_show,
        score_song,
    )
    scores = {
        "score_song": score_song if score_song is not None else 0,
        "score_costume": score_costume if score_costume is not None else 0,
        "score_show": score_show if score_show is not None else 0,
    }
    return templates.TemplateResponse(
        "participant.html",
        {
            "request": request,
            "participant_info": participant_info,
            "scores": scores,
            "round": request.cookies.get("round"),
        },
    )


@app.get("/logout")
def logout(request: Request, response: Response):
    resp = RedirectResponse("/login")
    resp.delete_cookie(key="user")
    resp.delete_cookie(key="round")
    return resp
