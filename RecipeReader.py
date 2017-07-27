import re

from DataReader import DataReader
import Recipes


def make_readable(locale_path, recipes):
    end_pattern = r'=(?P<new_name>.*)'
    d = DataReader(locale_path)
    remove_recipes = []
    for entry in recipes:
        pattern = entry.name + end_pattern
        match = re.search(pattern, d.content)
        if match:
            entry.name = match.group("new_name")
        else:
            remove_recipes.append(entry)
            continue
        remove_resources = []
        for pair in entry.get_resources().items():
            pattern = pair[0].name + end_pattern
            match = re.search(pattern, d.content)
            if match:
                pair[0].name = match.group("new_name")
            else:
                remove_resources.append(pair[0])
                continue
        for resource in remove_resources:
            entry.remove_resource(resource)
        if entry.number_of_resources() == 0:
            remove_recipes.append(entry)
    for entry in remove_recipes:
        recipes.remove(entry)
    return recipes


class RecipeReader(DataReader):
    """The Patterns contain the RegEx to match Recipes. Every RecipeReader needs a path for construction.
       create_recipes is the appropiate function
       to create a list of recipes from a text file. _create_resources is used in create_recipes"""

    resource_pattern = (r'[{}][^{}-]*(?!--)[^{}-]*'
                        r'(?P<resource_group>\{\s*'
                        r'type[^"]*"(?P<type>[^"]*)'
                        r'\W*name[^"]*"(?P<resource_name>[^"]*)'
                        r'\W*amount\D*(?P<amount>\d*)'
                        r'[^}]*)')
    resource_dummy = (
        r'(?:\{[^{}]+\})'
    )
    ingredients_pattern = (r'ingredients[^{]*'
                           r'(?P<ingredients>\{'
                           r'(?:[^{}]*') + resource_dummy + \
                          (r'[^{}]*)+'
                           r'\})')
    results_pattern = (r'results[^{]*'
                       r'(?P<results>\{'
                       r'(?:[^{}]*' + resource_dummy +
                       r'[^{}]*)+'
                       r'\})')
    recipe_pattern = (r'type.*?"recipe"'
                      r'.*?name[^"]+"(?P<name>[^"]+)"'
                      r'[^{}]*?(?=ingredients)') + ingredients_pattern + '[^r]*' + results_pattern

    def __init__(self, path):
        super().__init__(path)

    def create_recipes(self):
        recipes = []
        recipe_iter = re.finditer(self.recipe_pattern, self.content, re.DOTALL)
        for entry in recipe_iter:
            name = entry.group('name')
            placeholder = Recipes.Building("Placeholder")
            recipe = Recipes.Recipe(name, placeholder, "placeholder")
            self.create_resources(recipe, entry.group('ingredients'), educt=True)
            self.create_resources(recipe, entry.group('results'), educt=False)
            recipes.append(recipe)
            # print(entry.group("ingredients"))
        # print("\n".join(map(str, recipes)))
        return recipes

    def create_resources(self, recipe, text, educt=False):
        ingredients_iter = re.finditer(self.resource_pattern, text, re.DOTALL)
        for ingredient in ingredients_iter:
            if not ingredient.group('type') == "fluid":
                continue
            resource = Recipes.Resource(ingredient.group('resource_name'), Recipes.ResourceType.FLUID)
            if educt:
                recipe.add_educt(resource, int(ingredient.group("amount")))
            else:
                recipe.add_product(resource, int(ingredient.group("amount")))
