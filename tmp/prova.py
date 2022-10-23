import numpy as np

tipo = np.dtype([("name", "U30"), ("height", "uint32")])
array = np.array([], dtype=tipo)

# insert in tail

array = np.insert(array, array.size, ("Prova", 15))

array = np.insert(array, array.size, ("Prova2", 30))

array = np.insert(array, array.size, ("Prova3", 45))

print(array)
