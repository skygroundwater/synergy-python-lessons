"""Консольная база питомцев: create, read, update, delete и stop."""

import collections


pets = {
    1: {"Мухтар": {"Вид питомца": "Собака", "Возраст питомца": 9, "Имя владельца": "Павел"}},
    2: {"Каа": {"Вид питомца": "желторотый питон", "Возраст питомца": 19, "Имя владельца": "Саша"}},
}
next_id = 3


def get_suffix(age):
    if 11 <= age % 100 <= 14:
        return "лет"
    if age % 10 == 1:
        return "год"
    if 2 <= age % 10 <= 4:
        return "года"
    return "лет"


def get_pet(ID):
    return pets[ID] if ID in pets.keys() else False


def format_pet(pet):
    name = next(iter(pet.keys()))
    details = next(iter(pet.values()))
    age = details["Возраст питомца"]
    return (f'Это {details["Вид питомца"]} по кличке "{name}". '
            f'Возраст питомца: {age} {get_suffix(age)}. '
            f'Имя владельца: {details["Имя владельца"]}')


def input_details():
    name = input("Кличка: ").strip()
    species = input("Вид питомца: ").strip()
    age_text = input("Возраст: ").strip()
    while not age_text.isdecimal():
        age_text = input("Введите целый неотрицательный возраст: ").strip()
    owner = input("Имя владельца: ").strip()
    return {name: {"Вид питомца": species, "Возраст питомца": int(age_text), "Имя владельца": owner}}


def create():
    global next_id
    last = collections.deque(pets, maxlen=1)[0] if pets else 0
    # Счётчик не даёт повторно использовать ID после удаления последней записи.
    ID = max(last + 1, next_id)
    pets[ID] = input_details()
    next_id = ID + 1
    print("Создан питомец с ID", ID)
    return ID


def read(ID=None):
    if ID is None:
        ID = input_id()
    pet = get_pet(ID)
    if pet is False:
        print("Питомец с таким ID не найден")
        return False
    result = format_pet(pet)
    print(result)
    return result


def update(ID=None):
    if ID is None:
        ID = input_id()
    if get_pet(ID) is False:
        print("Питомец с таким ID не найден")
        return False
    pets[ID] = input_details()
    print("Запись обновлена")
    return True


def delete(ID=None):
    if ID is None:
        ID = input_id()
    if get_pet(ID) is False:
        print("Питомец с таким ID не найден")
        return False
    del pets[ID]
    print("Запись удалена")
    return True


def pets_list():
    if not pets:
        print("База питомцев пуста")
    for ID, pet in pets.items():
        print(f"ID {ID}: {format_pet(pet)}")


def input_id():
    text = input("ID питомца: ").strip()
    while not text.isdecimal():
        text = input("Введите целый неотрицательный ID: ").strip()
    return int(text)


def main():
    command = ""
    commands = {"create": create, "read": read, "update": update,
                "delete": delete, "list": pets_list}
    print("Команды: create, read, update, delete, list, stop")
    while command != "stop":
        command = input("Команда: ").strip().lower()
        if command in commands:
            commands[command]()
        elif command != "stop":
            print("Неизвестная команда")


if __name__ == "__main__":
    main()
