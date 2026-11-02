"""Касса: пополнение, количество полных тысяч и снятие денег."""

from decimal import Decimal


class Kassa:
    def __init__(self, amount=0):
        self.amount = self._money(amount)

    @staticmethod
    def _money(value):
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0:
            raise ValueError("Сумма должна быть конечной и неотрицательной")
        if amount != amount.quantize(Decimal("0.01")):
            raise ValueError("Сумма должна задаваться с точностью до копейки")
        return amount

    def top_up(self, X):
        self.amount += self._money(X)
        return self.amount

    def count_1000(self):
        return int(self.amount // 1000)

    def take_away(self, X):
        amount = self._money(X)
        if amount > self.amount:
            raise ValueError("Недостаточно денег в кассе")
        self.amount -= amount
        return self.amount


Касса = Kassa


if __name__ == "__main__":
    cash = Kassa(1500)
    cash.top_up(750)
    print("Полных тысяч:", cash.count_1000())
    cash.take_away(1200)
    print("Остаток:", cash.amount)
