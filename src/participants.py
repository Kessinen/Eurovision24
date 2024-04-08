import json

'''
  {
    "id": 1,
    "country": "Albania",
    "country_img": "https://eurovision.tv/sites/default/files/media/image/2023-08/ESC-HEART-ALBANIA-WHITE%402000px.png",
    "name": "BESA",
    "song": "TITAN",
    "img": "https://eurovision.tv/sites/default/files/styles/teaser/public/media/image/2024-03/4ac43501-b970-4809-a30b-73eaeb93f3f5.jpeg",
    "url": "https://eurovision.tv/participant/besa-2024",
    "round": 2,
    "place": 2
  },
'''

def get_participants(round_number: int = None) -> list[dict]:
    participants_json = None
    retval = []
    with open("participants.json", "r") as f:
        participants_json = json.load(f)
    if round_number == None:
        return retval
    retval = [participant for participant in participants_json if participant["round"] == round_number]
    retval.sort(key=lambda x: x["place"])
    return retval
    
    

    
