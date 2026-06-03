from ingredient import Ingredient


class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0 #https://docs.python.org/3/library/functions.html#isinstance

    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredient = Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit)
            new_ingredients.append(new_ingredient)
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_str = ", ".join([str(ingredient) for ingredient in self.ingredients]) #https://docs.python.org/3/tutorial/datastructures.html
        return f"{self.title}: {ingredients_str}" ##https://docs.python.org/3/tutorial/inputoutput.html