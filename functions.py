#середній час проходження гри 
def format_rating(game):
    rating = game.get("rating")
    return "—" if rating is None else f"{rating:g}/10"


def show_games(games):
    if not games:
        print("Каталог порожній.")
        return

    for i, game in enumerate(games, 1):
        print(
            f"{i}. {game['title']} "
            f"(рейтинг: {format_rating(game)}, "
            f"награно: {game.get('hours', 0):g} год)"
        )


def choose_game(games):
    show_games(games)

    if not games:
        return None

    try:
        number = int(input("Номер гри: "))

        if 1 <= number <= len(games):
            return number - 1

        print("Невірний номер!")
        return None

    except ValueError:
        print("Введіть число!")
        return None


def show_game_details(game):
    print("\nНазва:", game["title"])
    print("Опис:", game["description"])
    print("Рейтинг:", format_rating(game))
    print("Награно:", f"{game.get('hours', 0):g} год")

    print("\nПерсонажі:")

    if not game["characters"]:
        print("Персонажів поки немає.")
        return

    for i, character in enumerate(game["characters"], 1):
        print(f"\n{i}. {character['name']}")
        print("Опис:", character["description"])
