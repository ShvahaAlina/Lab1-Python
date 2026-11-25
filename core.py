import json
import os
import sys

BASE_DIR = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)
FILE = os.path.join(BASE_DIR, "games.json")


def load_games():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    # старі записи без нових полів
                    for game in data:
                        game.setdefault("rating", None)
                        game.setdefault("hours", 0)
                    return data

        except json.JSONDecodeError:
            print("Файл пошкоджений або порожній.")

    return []


def save_games(games):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=4)


def add_game(games, title, description, rating=None, hours=0):
    games.append({
        "title": title,
        "description": description,
        "rating": rating,
        "hours": hours,
        "characters": []
    })
    save_games(games)


def edit_game_stats(games, game_number, rating, hours):
    games[game_number]["rating"] = rating
    games[game_number]["hours"] = hours
    save_games(games)


def add_character(games, game_number, name, description):
    games[game_number]["characters"].append({
        "name": name,
        "description": description
    })
    save_games(games)


def edit_character(games, game_number, character_number, description):
    games[game_number]["characters"][character_number]["description"] = description
    save_games(games)
