from classes.matrics import *
import linearProgramSolvers
import pulp
import numpy as np

# ***********************************************************
#                                                           *
# PART 1: input value number of rows and number of columns  *
#                                                           *
# ***********************************************************

def check_value(x):
    while x<=0 or x>100:
        x = int(input("Wrong value! Enter again: "))
    return x

print("\n>> Setting dimensions...")
rows = check_value(int(input("Enter rows: ")))
cols=rows

# ***********************************************************
#                                                           *
# PART 2: create the crossroads with the occupation matrix  *
#                                                           *
# ***********************************************************

print("\n>> Creating the crossroads...")

create_occ = Occupation(rows, cols)
occupation_matrix = create_occ.create_occupation_matrix()
print(occupation_matrix)

# ***********************************************************
#                                                           *
# PART 3: ask number of cars on the crossroads              *
#                                                           *
# ***********************************************************

num_cars = int(input("\n>> How many cars do you want to insert? Answer: "))
while num_cars<1 or num_cars>(np.count_nonzero(occupation_matrix == 0)): 
    num_cars = int(input("Wrong value! Insert again: "))

insert_cars = create_occ.insert_cars(occupation_matrix, num_cars)
occupation_matrix = insert_cars[0]
print(occupation_matrix, "\n")

# Create car position matrix to compute the final visibility matrix

# Compute the new position of the cars 
positions_cars = insert_cars[1]
new_positions=[]
for i in range(len(positions_cars)):
    pos = positions_cars[i]
    new_pos=pos[0]*rows+pos[1]
    new_positions.append(new_pos)
new_positions=np.array(new_positions)

 # Construct a diagonal matrix with entries > 0 in car positions
diag=np.zeros(rows*cols)
for i in range(len(new_positions)):
    diag[new_positions[i]]=1
diag_matrix=np.diag(diag)

# ***********************************************************
#                                                           *
# PART 4: Visibility matrix construction                    *
#                                                           *
# ***********************************************************

create_vis = Visibility(rows, cols)
complete_visibility = create_vis.create_complete_visibility(occupation_matrix)

print("\nComplete Visibility Matrix:\n", complete_visibility)

matrix = np.dot(diag_matrix,complete_visibility)
matrix = matrix.astype(int)
print("\nActual Visibility Matrix:\n", matrix)

# ***********************************************************
#                                                           *
# PART 5: Linear Programming Optimization                   *
#                                                           *
# ***********************************************************

capacity = int(input("\nInsert max capacity..."))

print("\nMaximum Capacity = ", capacity)

print("\nOPTIMAL SOLVER STATISTICS:")
linearProgramSolvers.optimal_solver(matrix, capacity,0)

print("\nNON OPTIMAL SOLVER STATISTICS:")
linearProgramSolvers.non_optimal_solver(matrix,capacity,0)

print("\nRANDOM SOLVER STATISTICS:")
linearProgramSolvers.random_solver(matrix,capacity,new_positions,0)