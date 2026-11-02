"""Вывод списка рекурсией: циклы и генераторы не используются."""


def print_list(values, index=0):
    if index == len(values):
        print("Конец списка")
        return
    print(values[index])
    print_list(values, index + 1)


if __name__ == "__main__":
    my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    print_list(my_list)
