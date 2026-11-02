"""Вложенный словарь питомца, заполненный исключительно через input()."""


def get_suffix(age):
    if 11 <= age % 100 <= 14:
        return "лет"
    if age % 10 == 1:
        return "год"
    if 2 <= age % 10 <= 4:
        return "года"
    return "лет"


def main():
    pets = {}
    name = input("Кличка: ").strip()
    species = input("Вид питомца: ").strip()
    age = int(input("Возраст: "))
    owner = input("Имя владельца: ").strip()
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")
    pets[name] = {"Вид питомца": species, "Возраст питомца": age, "Имя владельца": owner}
    # По условию информацию извлекаем с помощью keys() и values().
    pet_name = next(iter(pets.keys()))
    details = next(iter(pets.values()))
    print(f'Это {details["Вид питомца"]} по кличке "{pet_name}". '
          f'Возраст питомца: {details["Возраст питомца"]} {get_suffix(age)}. '
          f'Имя владельца: {details["Имя владельца"]}')


if __name__ == "__main__":
    main()
