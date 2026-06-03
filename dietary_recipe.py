from recipe import Recipe


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}" ###https://docs.python.org/3/tutorial/inputoutput.html