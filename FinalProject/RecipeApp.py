import tkinter as tk
from tkinter import ttk, messagebox
from RecipeManager import RecipeManager


class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Organizer")
        self.root.geometry('950x450')
        self.manager = RecipeManager('recipes.txt', 'recent_recipes.txt')
        self.categories = ["Dessert", "Main Course", "Appetizer", "Beverage", "Snack"]
        self.sort_order = False  # True for ascending, False for descending

        self.setup_widgets()
        self.update_treeview()

    def setup_widgets(self):
        # title
        self.lbl_title = ttk.Label(self.root, text="Digital Recipe Organizer", font=('Arial', 20))
        self.lbl_title.grid(row=0, column=0, columnspan=10, pady=10)

        # category filter dropdown
        self.category_var = tk.StringVar()
        self.category_var.set("All Categories")
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var, values=["All Categories"] + self.categories, state='readonly')
        self.category_dropdown.grid(row=1, column=0, padx=10, pady=10)
        self.category_dropdown.bind('<<ComboboxSelected>>', self.filter_by_category)

        # search bar and find button
        self.search_var = tk.StringVar()
        ttk.Label(self.root, text="Search:").grid(row=1, column=1, padx=10)
        self.search_entry = ttk.Entry(self.root, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=2, sticky='ew')
        self.search_button = ttk.Button(self.root, text="Find", command=self.search_recipes)
        self.search_button.grid(row=1, column=3, padx=10)

        # recipe name and category frame
        self.frame_recipes = ttk.Frame(self.root)
        self.frame_recipes.grid(row=2, column=0, columnspan=4, sticky='nswe', padx=5)

        self.tree_recipes = ttk.Treeview(self.frame_recipes, columns=('Recipe Name', 'Category'), show='headings')
        self.tree_recipes.heading('Recipe Name', text='Recipe Name', command=self.toggle_sort_order)
        self.tree_recipes.heading('Category', text='Category')
        self.tree_recipes.pack(side='left', fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame_recipes, orient='vertical', command=self.tree_recipes.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree_recipes.configure(yscrollcommand=self.scrollbar.set)

        self.tree_recipes.bind('<<TreeviewSelect>>', self.show_details)

        # recipe details frame
        self.frame_details = ttk.Frame(self.root)
        self.frame_details.grid(row=2, column=4, columnspan=4, sticky='nswe', padx=5, pady=10)

        ttk.Label(self.frame_details, text="Recipe Details", font=('Arial', 16)).grid(row=0, column=0)
        self.text_details = tk.Text(self.frame_details, height=15, width=50)
        self.text_details.grid(row=1, column=0)

        # buttons to add,edit,remove and view recent recipes
        self.btn_add_recipe = ttk.Button(self.root, text="Add Recipe", command=self.add_recipe_dialog)
        self.btn_add_recipe.grid(row=4, column=0, sticky='ew', padx=10, pady=10)

        self.btn_edit_recipe = ttk.Button(self.root, text="Edit Recipe", command=self.edit_recipe_dialog)
        self.btn_edit_recipe.grid(row=4, column=1, sticky='ew', padx=10, pady=10)

        self.btn_remove_recipe = ttk.Button(self.root, text="Remove Recipe", command=self.remove_recipe)
        self.btn_remove_recipe.grid(row=4, column=2, sticky='ew', padx=10, pady=10)

        self.btn_view_recent = ttk.Button(self.root, text="View Recent Recipes", command=self.view_recent_recipes)
        self.btn_view_recent.grid(row=4, column=3, sticky='ew', padx=10, pady=10)

    def update_treeview(self):
        items = [(name, details) for name, details in self.manager.recipes.items()]
        items = self.insertion_sort(items, key=lambda x: x[0].lower(), reverse=not self.sort_order)
        self.tree_recipes.delete(*self.tree_recipes.get_children())
        for name, details in items:
            if self.category_var.get() == "All Categories" or details.get('Category') == self.category_var.get():
                self.tree_recipes.insert('', 'end', values=(name, details.get('Category', 'N/A')))

    def search_recipes(self):
        search_text = self.search_var.get().lower()
        self.tree_recipes.delete(*self.tree_recipes.get_children())
        for name, details in self.manager.recipes.items():
            if search_text in name.lower() or search_text in details['Ingredients'].lower():
                self.tree_recipes.insert('', 'end', values=(name, details.get('Category', 'N/A')))

    def show_details(self, event):
        selected_item = self.tree_recipes.selection()
        if selected_item:
            # MUST convert to string as numbers will be taken as a number and not be able to be found
            recipe_name = str(self.tree_recipes.item(selected_item[0])['values'][0])
            details = self.manager.recipes[recipe_name]
            display_text = f"Ingredients:\n{details['Ingredients']}\nInstructions:\n{details['Instructions']}"
            self.text_details.delete('1.0', tk.END)
            self.text_details.insert(tk.END, display_text)
            # manage recent recipes
            if recipe_name in self.manager.recent_recipes:
                self.manager.recent_recipes.remove(recipe_name)
            self.manager.recent_recipes.appendleft(recipe_name)
            self.manager.save_recent_recipes()

    def toggle_sort_order(self):
        self.sort_order = not self.sort_order
        self.update_treeview()

    # sorting method
    def insertion_sort(self, items, key=lambda x: x, reverse=False):
        for i in range(1, len(items)):
            current = items[i]
            position = i
            while position > 0 and (key(items[position - 1]) > key(current) if reverse else key(items[position - 1]) < key(current)):
                items[position] = items[position - 1]
                position -= 1
            items[position] = current
        return items

    def filter_by_category(self, event):
        # update the treeview based on the selected category
        self.update_treeview()

    def add_recipe_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.resizable(False, False)
        dialog.title("Add a New Recipe")
        dialog.geometry("500x450")

        # fields for recipe data
        ttk.Label(dialog, text="Recipe Name:").pack(pady=(10, 0))
        entry_name = ttk.Entry(dialog)
        entry_name.pack(pady=(0, 10))

        ttk.Label(dialog, text="Category:").pack()
        combo_category = ttk.Combobox(dialog, values=self.categories, state='readonly')
        combo_category.pack(pady=10)

        ttk.Label(dialog, text="Ingredients:").pack()
        text_ingredients = tk.Text(dialog, height=5)
        text_ingredients.pack(pady=10)

        ttk.Label(dialog, text="Instructions:").pack()
        text_instructions = tk.Text(dialog, height=5)
        text_instructions.pack(pady=10)

        def submit_recipe():
            name = entry_name.get()
            category = combo_category.get()
            ingredients = text_ingredients.get("1.0", tk.END).strip()
            instructions = text_instructions.get("1.0", tk.END).strip()
            try:
                self.manager.add_recipe(name, category, ingredients, instructions)
                self.update_treeview()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Submit", command=submit_recipe).pack(pady=20)

    def edit_recipe_dialog(self):
        selected_item = self.tree_recipes.selection()
        if selected_item:
            # MUST convert to string as numbers will be taken as a number and not be able to be found
            recipe_name = str(self.tree_recipes.item(selected_item[0])['values'][0])
            details = self.manager.recipes[recipe_name]

            edit_window = tk.Toplevel(self.root)
            edit_window.resizable(False, False)
            edit_window.title("Edit Recipe")
            edit_window.geometry("500x450")

            # fields for recipe data
            ttk.Label(edit_window, text="Recipe Name:").pack(pady=(10, 0))
            entry_name = ttk.Entry(edit_window)
            entry_name.insert(0, recipe_name)
            entry_name.pack(pady=(0, 10))

            ttk.Label(edit_window, text="Category:").pack()
            combo_category = ttk.Combobox(edit_window, values=self.categories, state='readonly')
            combo_category.set(details.get('Category', 'N/A'))
            combo_category.pack(pady=10)

            ttk.Label(edit_window, text="Ingredients:").pack()
            text_ingredients = tk.Text(edit_window, height=5)
            text_ingredients.insert(tk.END, details['Ingredients'])
            text_ingredients.pack(pady=10)

            ttk.Label(edit_window, text="Instructions:").pack()
            text_instructions = tk.Text(edit_window, height=5)
            text_instructions.insert(tk.END, details['Instructions'])
            text_instructions.pack(pady=10)

            def submit_edit():
                new_name = entry_name.get()
                new_category = combo_category.get()
                new_ingredients = text_ingredients.get("1.0", tk.END).strip()
                new_instructions = text_instructions.get("1.0", tk.END).strip()
                try:
                    self.manager.update_recipe(recipe_name, new_name, new_category, new_ingredients, new_instructions)
                    self.update_treeview()
                    edit_window.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            ttk.Button(edit_window, text="Submit", command=submit_edit).pack(pady=20)
        else:
            messagebox.showinfo("Edit Recipe", "Please select a recipe to edit.")

    def remove_recipe(self):
        selected_item = self.tree_recipes.selection()
        if selected_item:
            # MUST convert to string as numbers will be taken as a number and not be able to be found
            recipe_name = str(self.tree_recipes.item(selected_item[0])['values'][0])
            if messagebox.askyesno("Remove Recipe", f"Are you sure you want to delete '{recipe_name}'?"):
                self.manager.remove_recipe(recipe_name)
                self.update_treeview()

    def view_recent_recipes(self):
        recent_window = tk.Toplevel(self.root)
        recent_window.resizable(False, False)
        recent_window.title("Recent Recipes")
        recent_window.geometry("200x200")
        ttk.Label(recent_window, text="Recent Recipes", font=('Arial', 16)).pack(pady=10)
        listbox = tk.Listbox(recent_window)
        listbox.pack(fill='both', expand=True)
        for recipe in self.manager.recent_recipes:
            listbox.insert(tk.END, recipe)
