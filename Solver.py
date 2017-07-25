import math

from Recipes import Building, RecipeReader


def demo(e, f, g):
   while True:
         d = f ** 2 - 4 * e * g
         if d > 0:
             disc = math.sqrt(d)
             root1 = (-f - disc) / (2 * e)
             root2 = (-f + disc) / (2 * e)
             return root1, root2
         elif d == 0:
             return -f / (2 * e)
         else:
               return None


if __name__ == '__main__':
    #a = int(input("a "))
    #b = int(input("b "))
    #c = int(input("c "))
    #demo(a, b, c)
    r = RecipeReader(r"C:\Users\haban\Documents\PythonProjects\SpreadsheetAngelsMod\petrochem-basics.txt")
    r.create_recipes()
    pass
