import argparse

import core
import commands
import functions


# ---------- інтерактивне меню (якщо запустити без аргументів) ----------

def run_menu(games):
    while True:
        print("\n====== GAME CATALOG ======")
        print("1. Показати ігри (show)")
        print("2. Додати гру (add)")
        print("3. Додати персонажа (add character)")
        print("4. Деталі гри (details)")
        print("5. Редагувати персонажа (edit)")
        print("6. Вийти (exit)")

        command = input("\nВведіть команду: ")

        if not commands.dispatch(games, command):
            print("До побачення!")
            break


# ---------- перевірка аргументів ----------

def rating_type(value):
    try:
        number = float(value.replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError("рейтинг має бути числом")
    if not 0 <= number <= 10:
        raise argparse.ArgumentTypeError("рейтинг має бути від 0 до 10")
    return number


def hours_type(value):
    try:
        number = float(value.replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError("години мають бути числом")
    if number < 0:
        raise argparse.ArgumentTypeError("години не можуть бути меншими за 0")
    return number


def get_game_index(games, number):
    """Перетворює номер гри (з 1) в індекс або друкує помилку."""
    if 1 <= number <= len(games):
        return number - 1
    print("Невірний номер гри!")
    return None


# ---------- обробники підкоманд ----------

def cmd_show(games, args):
    functions.show_games(games)


def cmd_add(games, args):
    title = args.title.strip()
    if not title:
        print("Введіть назву гри.")
        return

    core.add_game(
        games, title, args.description.strip(), args.rating, args.hours
    )
    print("Гру додано!")


def cmd_add_character(games, args):
    index = get_game_index(games, args.game)
    if index is None:
        return

    name = args.name.strip()
    if not name:
        print("Введіть ім'я персонажа.")
        return

    core.add_character(games, index, name, args.description.strip())
    print("Персонажа додано!")


def cmd_details(games, args):
    index = get_game_index(games, args.game)
    if index is None:
        return

    functions.show_game_details(games[index])


def cmd_edit_character(games, args):
    index = get_game_index(games, args.game)
    if index is None:
        return

    characters = games[index]["characters"]
    if not 1 <= args.character <= len(characters):
        print("Невірний номер персонажа!")
        return

    description = args.description.strip()
    if not description:
        print("Опис не може бути порожнім.")
        return

    core.edit_character(games, index, args.character - 1, description)
    print("Опис змінено!")


def cmd_stats(games, args):
    index = get_game_index(games, args.game)
    if index is None:
        return

    if args.rating is None and args.hours is None:
        print("Вкажіть --rating та/або --hours.")
        return

    game = games[index]
    rating = args.rating if args.rating is not None else game.get("rating")
    hours = args.hours if args.hours is not None else game.get("hours", 0)

    core.edit_game_stats(games, index, rating, hours)
    print("Рейтинг/години оновлено!")


# ---------- розбір командного рядка ----------

def build_parser():
    parser = argparse.ArgumentParser(
        description="Каталог ігор. Без аргументів запускається меню."
    )
    sub = parser.add_subparsers(dest="command", metavar="команда")

    p = sub.add_parser("show", help="показати список ігор")
    p.set_defaults(handler=cmd_show)

    p = sub.add_parser("add", help="додати гру")
    p.add_argument("title", help="назва гри")
    p.add_argument("-d", "--description", default="", help="опис гри")
    p.add_argument("-r", "--rating", type=rating_type, default=None,
                   help="рейтинг 0-10")
    p.add_argument("-t", "--hours", type=hours_type, default=0,
                   help="скільки годин награно")
    p.set_defaults(handler=cmd_add)

    p = sub.add_parser("add-character", help="додати персонажа до гри")
    p.add_argument("game", type=int, help="номер гри")
    p.add_argument("name", help="ім'я персонажа")
    p.add_argument("-d", "--description", default="",
                   help="опис персонажа")
    p.set_defaults(handler=cmd_add_character)

    p = sub.add_parser("details", help="показати деталі гри")
    p.add_argument("game", type=int, help="номер гри")
    p.set_defaults(handler=cmd_details)

    p = sub.add_parser("edit-character", help="змінити опис персонажа")
    p.add_argument("game", type=int, help="номер гри")
    p.add_argument("character", type=int, help="номер персонажа")
    p.add_argument("description", help="новий опис")
    p.set_defaults(handler=cmd_edit_character)

    p = sub.add_parser("stats", help="оновити рейтинг і години гри")
    p.add_argument("game", type=int, help="номер гри")
    p.add_argument("-r", "--rating", type=rating_type, default=None,
                   help="новий рейтинг 0-10")
    p.add_argument("-t", "--hours", type=hours_type, default=None,
                   help="нова кількість годин")
    p.set_defaults(handler=cmd_stats)

    return parser


def main():
    args = build_parser().parse_args()
    games = core.load_games()

    if args.command is None:
        run_menu(games)
    else:
        args.handler(games, args)


if __name__ == "__main__":
    main()
