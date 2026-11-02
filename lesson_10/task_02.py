"""Словарь {n: n ** n} для n от 10 до -5 включительно."""


def powers_dictionary():
    result = {}
    for number in range(10, -6, -1):
        result[number] = number ** number
    return result


if __name__ == "__main__":
    print(powers_dictionary())
