import unittest
from FinalProject.RecipeManager import RecipeManager  # Adjust this import according to your project structure


class TestRecipeManager(unittest.TestCase):
    def setUp(self):
        # names for files
        self.recipe_file = 'test_recipes.txt'
        self.recent_file = 'test_recent_recipes.txt'
        # create files if they don't exist or reset if they do
        with open(self.recipe_file, 'w') as f:
            f.write('Name,Category,Ingredients,Instructions\n')
        with open(self.recent_file, 'w') as f:
            f.write('Name\n')

        # initialize RecipeManager with the created files
        self.manager = RecipeManager(self.recipe_file, self.recent_file)
        # populate the manager's recipe dictionary directly
        self.manager.recipes = {
            'Apple Pie': {'Category': 'Dessert', 'Ingredients': 'Apples, Sugar, Pie crust',
                          'Instructions': 'Mix and bake'},
            'Tomato Soup': {'Category': 'Appetizer', 'Ingredients': 'Tomatoes, Salt, Cream',
                            'Instructions': 'Boil and blend'}
        }
        # save the populated data to the file
        self.manager.save_recipes()

    def test_load_recipes(self):
        self.manager.recipes = {}  # clear existing recipes
        self.manager.recipes = self.manager.load_recipes()
        self.assertIn('Apple Pie', self.manager.recipes)
        self.assertIn('Tomato Soup', self.manager.recipes)

    def test_add_recipe(self):
        recipe_name = "Cheese Pizza"
        self.manager.add_recipe(recipe_name, "Main Course", "Cheese, Pizza Dough, Tomato Sauce", "Bake for 20 minutes")
        self.assertIn(recipe_name, self.manager.recipes)

    def test_add_duplicate_recipe(self):
        with self.assertRaises(ValueError):
            self.manager.add_recipe('Apple Pie', 'Dessert', 'Apples, Sugar, Pie crust', 'Mix and bake')

    def test_remove_recipe(self):
        self.manager.remove_recipe('Tomato Soup')
        self.assertNotIn('Tomato Soup', self.manager.recipes)

    def test_update_recipe(self):
        self.manager.update_recipe('Apple Pie', 'Apple Pie', 'Dessert', 'Apples, More Sugar, Pie crust', 'Mix well and bake')
        self.assertEqual(self.manager.recipes['Apple Pie']['Ingredients'], 'Apples, More Sugar, Pie crust')

    def tearDown(self):
        # clean up after tests
        import os
        if os.path.exists(self.recipe_file):
            os.remove(self.recipe_file)
        if os.path.exists(self.recent_file):
            os.remove(self.recent_file)

