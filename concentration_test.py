import numpy as np
np.set_printoptions(precision=2)

def latexprint(ndarray,prec = 2):
    string = "\hline"
    for row in ndarray:
        string += "\n    " + " & ".join("{:.2f}".format(x) for x in row)
        string += " \\\\ \n\hline"

    print(string)

grid_size = (6,6)
a = 1
b = 2

conc_map = np.full(grid_size,0,dtype=np.float64)

marker_tracker = [
    (1,1),(4,5)
] # markers denoted in (x,y) format

for i_y,i_x in np.ndindex(grid_size):
    # this iterates over every single cell in the grid
    conc = 0
    for marker in marker_tracker:
        # this iterates over the markers
        dist = ((marker[1] - i_y)**2 + (marker[0] - i_x)**2)**0.5 + 1
        
        conc += a/(dist**(b))

    conc_map[i_y,i_x] = conc

print(conc_map)
latexprint(conc_map)

