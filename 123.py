import random
import sys

class_attributes = {
    "Воин": {"Здоровье": 100, "Урон": 20},
    "Маг": {"Здоровье": 50, "Урон": 40},
    "Лучник": {"Здоровье": 75, "Урон": 30},
}


def open_menu():
    print("Вы проиграли!")
    print("1. Начать игру заново")
    print("2. Выйти")
    choice = input("Выберите пункт: ")
    if choice == "1":
        main()
    elif choice == "2":
        exit()
    else:
        print("Неверный выбор!")


def start_game():
    print("Добро пожаловать в текстовую игру!")
    print(
        "Конец света наступил, и вы оказались в постапокалиптическом мире, где человеческая раса на грани вымирания. Вы - один из немногих выживших, и ваша единственная цель - пройти через опасные подземелья и найти спасение.")
    print("Удачи!")
    print()


def choose_class():
    print("Выберите класс персонажа:")
    for i, char_class in enumerate(classes):
        print(f"{i + 1}. {char_class}")
    class_choice = int(input("> "))
    player["class"] = classes[class_choice - 1]


def boss_appears():
    chance = random.randint(1, 10)
    if chance <= 2:
        print("Босс появился! Будьте готовы к сильному противнику!")
        return True
    else:
        return False
    while True:
        print(f"Здоровье: {player_health}")
        print(f"Атака: {player_attack}")

        if enemy_killed % 2 == 0 and enemy_killed > 0:
            level_up(player_name, player_health, player_attack)

        command = input("Что вы хотите сделать? (атаковать/инвентарь/выйти): ")
        if command == "атаковать":
            if attack(player_name, player_attack):
                enemies_killed += 1
                print("Враг побежден!")
                if enemies_killed == 5:
                    if attack_boss(player_name, player_health, player_attack):
                        print("Босс повержен! Поздравляем, вы победили дракона!")
                        if show_menu():
                            start_game()
                        else:
                            break


def start_class_attributes_menu():
    print("Выберите стартовые характеристики:")
    print("1. Воин")
    print("2. Маг")
    print("3. Лучник")

    class_choice = int(input("> "))

    if class_choice == 1:
        player["class"] = classes[0]
        player["health"] = class_attributes["Воин"]["Здоровье"]
        player["attack"] = class_attributes["Воин"]["Урон"]
    elif class_choice == 2:
        player["class"] = classes[1]
        player["health"] = class_attributes["Маг"]["Здоровье"]
        player["attack"] = class_attributes["Маг"]["Урон"]
    elif class_choice == 3:
        player["class"] = classes[2]
        player["health"] = class_attributes["Лучник"]["Здоровье"]
        player["attack"] = class_attributes["Лучник"]["Урон"]


def generate_enemy():
    enemy_name = random.choice(enemy_names)
    enemy_health = random.randint(50, 80)
    enemy_attack = random.randint(5, 10)
    return {"name": enemy_name, "health": enemy_health, "attack": enemy_attack}


def fight(enemy):
    print(f"Вы встретили врага: {enemy['name']}")
    while player["health"] > 0 and enemy["health"] > 0:
        print(f"Здоровье игрока: {player['health']}")
        print(f"Здоровье врага: {enemy['health']}")
        print("1. Атаковать")
        print("2. Убежать")
        choice = int(input("> "))
        if choice == 1:
            player_attack = random.randint(10, 18)
            enemy_attack = random.randint(5, 8)
            print(f"Вы атаковали врага и нанесли {player_attack} урона.")
            print(f"Враг атаковал вас и нанес {enemy_attack} урона.")
            player["health"] -= enemy_attack
            enemy["health"] -= player_attack

        elif choice == 2:
            print("Вы решили сбежать!")
            return

        if player["health"] > 0:

            item_drop_chance = random.randint(1, 5)
            if item_drop_chance == 1:
                dropped_item = random.choice(items)
                player["inventory"].append(dropped_item)
                print(f"Враг оставил вам предмет: {dropped_item}!")
        if player["health"] < 0:
            open_menu()


def use_item(item):
    if item in player["inventory"]:
        print(f"Вы использовали предмет {item}!")
        player["inventory"].remove(item)
        if item == "Зелье здоровья":
            player["health"] += random.randint(10, 30)
            print("Восстановлено здоровье!")
    else:
        print("У вас нет такого предмета!")


def get_item():
    return player["inventory"][random.randint(0, len(player["inventory"]))]


def print_inventory():
    print("Ваш инвентарь:")
    for item in player["inventory"]:
        print(item)


def show_stats():
    print(f"Имя: {player['name']}")
    print(f"Класс: {player['class']}")
    print(f"Здоровье: {player['health']}")
    print()


def save_game():
    with open("save_game.txt", "w") as save_file:
        save_file.write(f"Имя: {player['name']}\n")
        save_file.write(f"Класс: {player['class']}\n")
        save_file.write(f"Здоровье: {player['health']}\n")
        save_file.write("Инвентарь:\n")
        for item in player['inventory']:
            save_file.write(f"{item}\n")
    print("Игра сохранена!")


def load_game():
    try:
        with open("save_game.txt", "r") as save_file:
            lines = save_file.readlines()
        player["name"] = lines[0].split(": ")[1].strip()
        player["class"] = lines[1].split(": ")[1].strip()
        player["health"] = int(lines[2].split(": ")[1].strip())
        player["inventory"] = [line.strip() for line in lines[4:]]
        print("Игра загружена!")
    except FileNotFoundError:
        print("Нет сохраненной игры!")


# Функция открытия меню при проигрыше


# if player['health'] <= 0:
#     open_menu()

def delete_save():
    try:
        os.remove("save_game.txt")
        print("Сохранение удалено!")
    except FileNotFoundError:
        print("Нет сохраненной игры!")


# Основной код игры
classes = ["Воин", "Маг", "Лучник"]

player = {
    "name": "",
    "class": "",
    "health": 100,
    "inventory": []
}

enemy_names = ["Скелет", "Гоблин", "Дракон"]

items = ["Зелье здоровья", "Меч", "Лук", "Кольчуга"]


def main():
    start_game()

    while True:
        print()
        print("1. Начать новую игру")
        print("2. Загрузить сохранение")
        print("3. Выход")
        choice = int(input("> "))
        try:
            if choice == 1:
                player["name"] = input("Введите имя персонажа: ")
                choose_class()
                break
            elif choice == 2:
                load_game()
                break
            elif choice == 3:
                break
            else:
                print("Неверный код, введите то, что есть в меню!Не другое")
                return
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

    while player["health"] > 0:
        print()
        print("1. Искать врага")
        print("2. Использовать предмет")
        print("3. Посмотреть инвентарь")
        print("4. Показать статистику")
        print("5. Сохранить игру")
        print("6. Удалить сохранение")
        print("7. Загрузить игру")
        print("8. Выйти из игры")
        choice = int(input("> "))
        try:
            if choice == 1:
                fight(generate_enemy())
                boss_appears()
            elif choice == 2:
                use_item(get_item())

            elif choice == 3:
                print_inventory()

            elif choice == 4:
                show_stats()

            elif choice == 5:
                save_game()

            elif choice == 6:
                delete_save()

            elif choice == 7:
                load_game()

            elif choice == 8:
                exit()
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")


main()
