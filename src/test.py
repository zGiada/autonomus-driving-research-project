from classes.matrics import *
import linearProgramSolvers
import pulp
import numpy as np

def print_stats(avg):
    #print("\nAverage percentage of utilized capacity = ", avg[0], "%")
    #print("\nNumber of cells not visible = ", avg[1])   
    #print("\nAverage number of cells not transmitted to the controller = ", avg[2])
    print("Average percentage of transmitted cells = ", avg[3], "%")

num_iter = 20
rows = 20
cols=rows
capacity = 10
num_cars = 25
sum_optimal = np.zeros(4)
sum_non_optimal = np.zeros(4)
sum_random = np.zeros(4)

for i in range(num_iter):

    # Create occupation matrix
    create_occ = Occupation(rows, cols)
    occupation_matrix = create_occ.create_occupation_matrix()

    # Insert cars
    insert_cars = create_occ.insert_cars(occupation_matrix, num_cars)
    occupation_matrix = insert_cars[0]

    # Create car position matrix to compute the final visibility matrix
    positions_cars = insert_cars[1]
    new_positions=[]
    # Compute the new position of the cars 
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

    # Compute visibility matrix
    create_vis = Visibility(rows, cols)
    complete_visibility = create_vis.create_complete_visibility(occupation_matrix)

    # Actual Visiibility Matrix
    matrix = np.dot(diag_matrix,complete_visibility)
    matrix = matrix.astype(int)

    # Compute the statistics for each solver
    optimal_stats = linearProgramSolvers.optimal_solver(matrix, capacity,1)
    sum_optimal = sum_optimal + optimal_stats
    non_optimal_stats = linearProgramSolvers.non_optimal_solver(matrix,capacity,1)
    sum_non_optimal = sum_non_optimal + non_optimal_stats
    random_stats = linearProgramSolvers.random_solver(matrix,capacity,new_positions,1)
    sum_random = sum_random + random_stats

# Avarage 
avg_optimal = np.round(sum_optimal/num_iter,2)
avg_non_optimal = np.round(sum_non_optimal/num_iter,2)
avg_random = np.round(sum_random/num_iter,2)

# Print the results
print("\nOPTIMAL SOLVER STATISTICS:")
print_stats(avg_optimal)

print("\nNON OPTIMAL SOLVER STATISTICS:")
print_stats(avg_non_optimal)

print("\nRANDOM SOLVER STATISTICS:")
print_stats(avg_random)