"""Database project configuration"""

from tinydb import TinyDB
from pathlib import Path

ROOTS = Path(__file__).resolve().parent.parent

# Save in DataBase at Project roots
DB = TinyDB(ROOTS / 'db.json', indent=4)
PLAYERS_TABLE = DB.table("Players")
TOURNAMENTS_TABLE = DB.table("Tournaments")
