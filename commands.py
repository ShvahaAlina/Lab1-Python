
import core
import functions


def do_add(games):
    title = input("Назва гри: ").strip()
    description = input("Опис гри: ").strip()

    if not title:
        print("Введіть назву гри.")
        return

    core.add_game(games, title, description)
    print("Гру додано!")


def do_show(games):
    functions.show_games(games)


def do_add_character(games):
    number = functions.choose_game(games)

    if number is None:
        return

    name = input("Ім'я персонажа: ").strip()
    description = input("Опис персонажа: ").strip()

    if not name:
        print("Введіть ім'я персонажа.")
        return

    core.add_character(games, number, name, description)
    print("Персонажа додано!")


def do_details(games):
    number = functions.choose_game(games)

    if number is None:
        return

    functions.show_game_details(games[number])


def do_edit(games):
    number = functions.choose_game(games)

    if number is None:
        return

    characters = games[number]["characters"]

    if not characters:
        print("У цій грі немає персонажів.")
        return

    for i, character in enumerate(characters, 1):
        print(f"{i}. {character['name']}")

    try:
        char_number = int(input("Номер персонажа: "))

        if char_number < 1 or char_number > len(characters):
            print("Невірний номер!")
            return

        description = input("Новий опис: ").strip()

        if not description:
            print("Опис не може бути порожнім.")
            return

        core.edit_character(
            games, number, char_number - 1, description
        )

        print("Опис змінено!")

    except ValueError:
        print("Введіть число!")


def dispatch(games, command):
    commands = {
        "1": do_show,
        "show": do_show,

        "2": do_add,
        "add": do_add,

        "3": do_add_character,
        "add character": do_add_character,

        "4": do_details,
        "details": do_details,

        "5": do_edit,
        "edit": do_edit
    }

    command = command.strip().lower()

    if command in ["6", "exit"]:
        return False

    handler = commands.get(command)

    if handler is None:
        print("Невідома команда.")
        return True

    handler(games)
    return True
