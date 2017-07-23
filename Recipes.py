from enum import Enum
import re

class RecipeReader():
    def __init__(self, path):
        self.path = path
        try:
            file = open(path,"r")
            content = file.read()
            file.close()
        except IOError:
            raise ValueError("A valid path is required.")

    def create_Recipes(self):
        muster = re.compile()



class Recipe(object):

    """A class for Recipes. Needs a name, building where its made and the time of the recipe.
    There are 2 dicts for resources(educts, products) which map the Resource as key to the required amount."""
    def __init(self, name, building, time):
        if not (name and building and time and isinstance(building, Building)):
            raise ValueError("A Recipe needs a name, building and a time.")
        self.name = name
        self.building = building
        self.building = time
        self.products = {}
        self.educts = {}

    def number_of_resources(self):
        return len(self.products) + len(self.educts)

    def add_educt(self, educt, count):
        self.educts.update({educt: count})
        
    def add_product(self, product, count):
        self.products.update({product: count})


class Building(object):
    def __init__(self, name, base_speed=1, no_modules=0,module_speed=0):
        if not(name):
            raise ValueError("Illegal name for a building")
        self.name = name
        self.base_speed = base_speed
        self.no_modules = no_modules
        self.module_speed = module_speed

    def update_modules(self, module_speed):
        self.module_speed = module_speed

    def get_speed(self):
        return round(self.base_speed + self.no_modules*self.module_speed*self.base_speed,1)


class Resource(object):
    def __init__(self, name, res_type):
        if not (name and res_type and isinstance(res_type, ResourceType)):
            raise ValueError("Invalid Arguments for a Resource.")
        self.name = name
        self.res_type = res_type


class ResourceType(Enum):
    FLUID, ITEM = range(2)
