from fastapi import FastAPI
from faceit import Faceit
import os
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

app = FastAPI()
faceit = Faceit(os.getenv("FACEIT_API_KEY"))

@app.get("/")
def read_root():
    return {"message" : "Ok."}  

@app.get("/player/{player_name}")
def get_player_stats(player_name: str):
    player = faceit.get_player_by_nickname(player_name)
    r = faceit.get_player_stats(player["player_id"])
    r["player_name"] = player_name
    r["level"] = player["games"]["cs2"]["skill_level"]
    r["elo"] = player["games"]["cs2"]["faceit_elo"]
    r["url"] = player["faceit_url"].replace("{lang}", "en")
    return r