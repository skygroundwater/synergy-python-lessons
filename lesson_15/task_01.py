"""Наследование Transport и создание экземпляра Autobus."""


class Transport:
    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage

    def __str__(self):
        return (f"Название автомобиля: {self.name} "
                f"Скорость: {self.max_speed} Пробег: {self.mileage}")


class Autobus(Transport):
    pass


if __name__ == "__main__":
    autobus = Autobus("Renaul Logan", 180, 12)
    print(autobus)
