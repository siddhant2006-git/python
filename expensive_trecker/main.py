import json 
import math 


CATEGORIES=("food","game","entertainment","bills","other")
EXPENSIVE = [
    {"CATEGORIES": "food", "amount": 50},
    {"CATEGORIES": "bills", "amount": 600},
    {"CATEGORIES": "game", "amount": 6003},
    {"CATEGORIES":"entertainment","amount":200}
]

DATAFILE="EXPENSIVE.json"

def load_expensive():
    try:
        with open(DATAFILE,"r") as file :
            return json.load(file)
    except FileNotFoundError:
        return []

    # indent -indent ka use JSON data ko proper spacing ke saath readable format me save karne ke liye hota hai.
def savedata():
  with open(DATAFILE,"w") as file :
    json.dump(EXPENSIVE,file,indent=4)

