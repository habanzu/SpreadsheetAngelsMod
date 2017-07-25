from enum import Enum
import re

from DataReader import DataReader

"""type.*?"recipe".*?name.*?"(P<name>.*?)".*?icon"""


class RecipeReader(DataReader):
    """The Patterns contain the RegEx to match Recipes. Every RecipeReader needs a path for construction.
       create_recipes is the appropiate function
       to create a list of recipes from a text file. _create_resources is used in create_recipes"""

    resource_pattern = (r'(?P<resource_group>\{\s*'
                        r'type[^"]*"(?P<type>[^"]*)'
                        r'\W*name[^"]*"(?P<resource_name>[^"]*)'
                        r'\W*amount\D*(?P<amount>\d*)'
                        r'[^}]*'
                        r'\s*\})')
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
            placeholder = Building("Placeholder")
            recipe = Recipe(name, placeholder, "placeholder")
            self.create_resources(recipe, entry.group('ingredients'))
            self.create_resources(recipe, entry.group('results'))
            recipes.append(recipe)
            # print(entry.group("ingredients"))
        # print("\n".join(map(str, recipes)))
        return recipes

    def create_resources(self, recipe, text):
        ingredients_iter = re.finditer(self.resource_pattern, text, re.DOTALL)
        for ingredient in ingredients_iter:
            if not ingredient.group('type') == "fluid":
                continue
            resource = Resource(ingredient.group('resource_name'), ResourceType.FLUID)
            recipe.add_educt(resource, ingredient.group("amount"))


class Recipe(object):
    """A class for Recipes. Needs a name, building where its made and the time of the recipe.
    There are 2 dicts for resources(educts, products) which map the Resource as key to the required amount."""

    def __init__(self, name, building, time):
        if not (name and building and time and isinstance(building, Building)):
            raise ValueError("A Recipe needs a name, building and a time.")
        self.name = name
        self.building = building
        self.building = time
        self.products = {}
        self.educts = {}

    def __str__(self):
        l = [self.name]
        l.extend(map(str, self.educts.keys()))
        l.extend(map(str, self.products.keys()))
        return ", ".join(l)

    def number_of_resources(self):
        return len(self.products) + len(self.educts)

    def add_educt(self, educt, count):
        self.educts.update({educt: count})

    def add_product(self, product, count):
        self.products.update({product: count})


class Building(object):
    def __init__(self, name, base_speed=1, no_modules=0, module_speed=0):
        if not name:
            raise ValueError("Illegal name for a building")
        self.name = name
        self.base_speed = base_speed
        self.no_modules = no_modules
        self.module_speed = module_speed

    def update_modules(self, module_speed):
        self.module_speed = module_speed

    def get_speed(self):
        return round(self.base_speed + self.no_modules * self.module_speed * self.base_speed, 1)


class Resource(object):
    def __init__(self, name, res_type):
        if not (name and res_type and isinstance(res_type, ResourceType)):
            raise ValueError("Invalid Arguments for a Resource.")
        self.name = name
        self.res_type = res_type

    def __str__(self):
        return self.name


class ResourceType(Enum):
    FLUID, ITEM = range(2)
