import pandas as pd
import os
from collections import deque


class RecipeManager:
    def __init__(self, recipe_file, recent_file):
        self.recipe_file = recipe_file
        self.recent_file = recent_file
        self.recipes = self.load_recipes()
        self.recent_recipes = self.load_recent_recipes()

    def load_recipes(self):
        # if file exists
        if os.path.exists(self.recipe_file):
            df = pd.read_csv(self.recipe_file)
            return df.set_index('Name').to_dict(orient='index')
        # if not, create it with appropriate column names
        else:
            try:
                with open(self.recipe_file, 'w') as f:
                    f.write('Name,Category,Ingredients,Instructions\n')
            # handle file creation error
            except IOError as e:
                print(f"Error creating file {self.recipe_file}: {e}")
            return {}

    def load_recent_recipes(self):
        # if file exists
        if os.path.exists(self.recent_file):
            df = pd.read_csv(self.recent_file)
            return deque(df['Name'], maxlen=5)
        # if not, create it with appropriate column name
        else:
            try:
                with open(self.recent_file, 'w') as f:
                    f.write('Name\n')
            # handle file creation error
            except IOError as e:
                print(f"Error creating file {self.recent_file}: {e}")
            return deque(maxlen=5)

    def save_recipes(self):
        df = pd.DataFrame.from_dict(self.recipes, orient='index')
        df.reset_index(inplace=True)
        df.columns = ['Name', 'Category', 'Ingredients', 'Instructions']
        df.to_csv(self.recipe_file, index=False)

    def save_recent_recipes(self):
        df = pd.DataFrame(list(self.recent_recipes), columns=['Name'])
        df.to_csv(self.recent_file, index=False)

    def add_recipe(self, name, category, ingredients, instructions):
        # check if any field is empty
        if name == "" or category == "" or ingredients == "" or instructions == "":
            raise ValueError("All fields must be filled.")
        # check if name already exists
        if name in self.recipes:
            raise ValueError("Recipe name already exists.")
        self.recipes[name] = {'Category': category, 'Ingredients': ingredients, 'Instructions': instructions}
        self.save_recipes()

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()

    def update_recipe(self, old_name, new_name, category, ingredients, instructions):
        if old_name in self.recipes:
            # check if any field is empty
            if new_name == "" or category == "" or ingredients == "" or instructions == "":
                raise ValueError("All fields must be filled.")
            # check if the updated name does not already exist as a recipe
            if old_name != new_name and new_name in self.recipes:
                raise ValueError("New recipe name already exists.")
            del self.recipes[old_name]
        self.recipes[new_name] = {'Category': category, 'Ingredients': ingredients, 'Instructions': instructions}
        self.save_recipes()
