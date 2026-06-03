from ingredient import Ingredient


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        new_recipe = recipe.scale(portions)
        for i in new_recipe.ingredients:
            self._items.append((i, recipe.title))

    def remove_recipe(self, title):
        self._items = [i for i in self._items if i[1] != title] #https://docs.python.org/3/tutorial/datastructures.html

    def get_list(self):
        s = dict()
        for i in self._items:
            ingredient = i[0]
            key = (ingredient.name, ingredient.unit)
            if key in s:
                s[key] += ingredient.quantity
            else:
                s[key] = ingredient.quantity
        ms = []
        for key, value in s.items():
            ms.append(Ingredient(key[0], value, key[1]))
        ms = sorted(ms, key=lambda ing: ing.name) #https://docs.python.org/3/tutorial/controlflow.html
        return ms

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list