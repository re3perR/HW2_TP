import pytest
from ingredient import Ingredient
from recipe import Recipe
from shopping_list import ShoppingList


def test_ingredient_creation():
    ingredient = Ingredient("Кириешки", 333, "г")
    assert ingredient.name == "Кириешки"
    assert ingredient.quantity == 333.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Кириешки", 333, "г")
    assert str(ingredient) == "Кириешки: 333.0 г"


def test_ingredient_equal_same_name_and_unit():
    ingredient1 = Ingredient("Кириешки", 333, "г")
    ingredient2 = Ingredient("Кириешки", 777, "г")
    assert ingredient1 == ingredient2


def test_ingredient_not_equal_different_name():
    ingredient1 = Ingredient("Чипсы", 242, "г")
    ingredient2 = Ingredient("Лук", 242, "г")

    assert ingredient1 != ingredient2


def test_ingredient_not_equal_different_unit():
    ingredient1 = Ingredient("Чипсы", 500, "г")
    ingredient2 = Ingredient("Лук", 500, "кг")
    assert ingredient1 !=    ingredient2


def test_recipe_creation():
    ingredients = [
        Ingredient("Яйца", 3, "шт"),
        Ingredient("Подсолнечное масло", 15, "мл")
    ]
    recipe = Recipe("Яичница", ingredients)
    assert recipe.title == "Яичница"
    assert recipe.ingredients == ingredients


def test_recipe_add_new_ingredient():
    recipe = Recipe("Яичница", [Ingredient("Яйца", 3, "шт")])
    recipe.add_ingredient(Ingredient("Подсолнечное масло", 15, "мл"))
    assert len(recipe.ingredients) == 2
    assert recipe.ingredients[1].name == "Подсолнечное масло"
    assert recipe.ingredients[1].quantity == 15.0
    assert recipe.ingredients[1].unit == "мл"


def test_recipe_add_existing_ingredient():
    recipe = Recipe("Яичница", [Ingredient("Яйца", 3, "шт")])
    recipe.add_ingredient(Ingredient("Яйца", 2, "шт"))
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 5.0


def test_recipe_scale_returns_new_recipe():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    scaled_recipe = recipe.scale(2)
    assert isinstance(scaled_recipe, Recipe)
    assert scaled_recipe is not recipe
    assert scaled_recipe.title == "Яичница"
    assert scaled_recipe.ingredients[0].quantity == 6.0
    assert scaled_recipe.ingredients[1].quantity == 30.0


def test_recipe_scale_does_not_change_original_recipe():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    recipe.scale(2)
    assert recipe.ingredients[0].quantity == 3.0
    assert recipe.ingredients[1].quantity == 15.0


def test_recipe_scale_invalid_ratio():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-2)


def test_recipe_len():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    result = shopping_list.get_list()
    assert len(result) == 2
    assert result[0].name == "Подсолнечное масло"
    assert result[0].quantity == 30.0
    assert result[0].unit == "мл"
    assert result[1].name == "Яйца"
    assert result[1].quantity == 6.0
    assert result[1].unit == "шт"


def test_shopping_list_invalid_portions():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, -1)


def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    recipe2 = Recipe("Омлет",
        [
            Ingredient("Молоко", 200, "мл"),
            Ingredient("Яйца", 3, "шт")
        ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)
    shopping_list.remove_recipe("Омлет")
    result = shopping_list.get_list()
    assert len(result) == 2
    assert result[0].name == "Подсолнечное масло"
    assert result[1].name == "Яйца"


def test_shopping_list_remove_missing_recipe_does_nothing():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    shopping_list.remove_recipe("Омлет")
    result = shopping_list.get_list()
    assert len(result) == 2
    assert result[0].name == "Подсолнечное масло"
    assert result[1].name == "Яйца"


def test_shopping_list_get_list_sums_same_ingredients():
    recipe1 = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    recipe2 = Recipe("Омлет",
        [
            Ingredient("Молоко", 200, "мл"),
            Ingredient("Яйца", 3, "шт")
        ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)
    result = shopping_list.get_list()
    assert len(result) == 3
    items = {(ingredient.name, ingredient.unit): ingredient.quantity for ingredient in result}
    assert items[("Яйца", "шт")] == 6.0
    assert items[("Подсолнечное масло", "мл")] == 15.0
    assert items[("Молоко", "мл")] == 200.0


def test_shopping_list_get_list_sorted_by_name():
    recipe = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл"),
            Ingredient("Соль", 2, "г"),
        ])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    result = shopping_list.get_list()
    names = [ingredient.name for ingredient in result]
    assert names == ["Подсолнечное масло", "Соль", "Яйца"]


def test_shopping_list_add_operator():
    recipe1 = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    recipe2 = Recipe("Омлет",
        [
            Ingredient("Молоко", 200, "мл"),
            Ingredient("Яйца", 3, "шт")
        ])
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 2)
    list2.add_recipe(recipe2, 1)
    list3 = list1 + list2
    result = list3.get_list()
    names = [ingredient.name for ingredient in result]
    assert names == ["Молоко", "Подсолнечное масло", "Яйца"]


def test_shopping_list_add_operator_does_not_change_original_lists():
    recipe1 = Recipe("Яичница",
        [
            Ingredient("Яйца", 3, "шт"),
            Ingredient("Подсолнечное масло", 15, "мл")
        ])
    recipe2 = Recipe("Омлет",
        [
            Ingredient("Молоко", 200, "мл"),
            Ingredient("Яйца", 3, "шт")
        ])
    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    list3 = list1 + list2
    assert len(list1.get_list()) == 2
    assert len(list2.get_list()) == 2
    assert len(list3.get_list()) == 3