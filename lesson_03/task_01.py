"""Урок 3, задание 1: информация о питомце из пользовательского ввода."""


def age_suffix(age):
    if 11 <= age % 100 <= 14:
        return "лет"
    if age % 10 == 1:
        return "год"
    if 2 <= age % 10 <= 4:
        return "года"
    return "лет"


def main():
    species = input("Вид питомца: ").strip()
    age = int(input("Возраст питомца: "))
    name = input("Кличка питомца: ").strip()
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")
    print(f'Это {species} по кличке "{name}". Возраст: {age} {age_suffix(age)}.')


if __name__ == "__main__":
    main()
