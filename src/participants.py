import json


def get_all_participants(round_number: int = None) -> list[dict]:
    participants_json = None
    retval = []
    with open("data/participants.json", "r") as f:
        participants_json = json.load(f)
    if round_number == None:
        return retval
    retval = [
        participant
        for participant in participants_json
        if participant["round"] == round_number
    ]
    retval.sort(key=lambda x: x["place"])
    return retval


def get_participant(id: int) -> dict:
    participants_json = None
    retval = {}
    with open("data/participants.json", "r") as f:
        participants_json = json.load(f)
    retval = [
        participant for participant in participants_json if participant["id"] == id
    ][0]
    return retval
