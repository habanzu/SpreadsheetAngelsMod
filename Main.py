import RecipeWriter
from RecipeReader import RecipeReader, make_readable


r = RecipeReader(r"C:\Users\haban\Documents\PythonProjects\SpreadsheetAngelsMod\petrochem-basics.txt")
d = RecipeWriter.RecipeWriter('AngelsTest.xlsx')
g = r.create_recipes()
d.write_recipes(make_readable('petrochem_lokale.txt', g))
d.save_changes()
