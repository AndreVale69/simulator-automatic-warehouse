import numpy as np

# Contains the measurements of the size of the drawers
type = np.dtype([("name", "U30"), ("height", "uint32")])
data_left_column = np.array([], dtype=type)