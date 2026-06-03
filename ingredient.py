class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, val):
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(val)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}" #https://docs.python.org/3/tutorial/inputoutput.html

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')" #https://docs.python.org/3/tutorial/inputoutput.html

    def __eq__(self, other):
        if not isinstance(other, Ingredient): #https://docs.python.org/3/library/functions.html#isinstance
            return False
        return self.name == other.name and self.unit == other.unit