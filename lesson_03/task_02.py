"""Урок 3, задание 2: ввод этапов и вывод через => без проверки ответов."""


def main():
    stage_1 = input("Первый этап развития человека: ")
    stage_2 = input("Второй этап: ")
    stage_3 = input("Третий этап: ")
    stage_4 = input("Четвёртый этап: ")
    stage_5 = input("Последний этап (Homo sapiens sapiens): ")
    print(stage_1, stage_2, stage_3, stage_4, stage_5, sep="=>")


if __name__ == "__main__":
    main()
