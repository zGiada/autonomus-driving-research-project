import pulp
import numpy as np


def print_statistics(x,y,matrix,capacity):

    column_sum = np.sum(matrix, axis=0)
    not_visible_cells = np.count_nonzero(column_sum == 0)
    not_tx_cells = np.count_nonzero(y == 0)

    print("\nVector TX = ", x)
    print("\nController vector = ", y)
    print("\nPercentage of utilized capacity = ", np.sum(x)/capacity*100, "%")
    
    print("\nNumber of cells not visible = ", not_visible_cells)
    print("Number of cells not transmitted to the controller = ", not_tx_cells)

    print("\nPercentage of transmitted cells = ", np.round((len(y)-not_tx_cells)/(len(y)-not_visible_cells)*100,2),"%")

def return_statistics(x,y,matrix,capacity):

    column_sum = np.sum(matrix, axis=0)
    not_visible_cells = np.count_nonzero(column_sum == 0)
    not_tx_cells = np.count_nonzero(y == 0)

    return((np.sum(x)/capacity*100), (not_visible_cells), (not_tx_cells), ((len(y)-not_tx_cells)/(len(y)-not_visible_cells)*100))    

# ***********************************************************
#                                                           *
# 1ST METHOD: OPTIMAL SOLUTION                              *
#                                                           *
# ***********************************************************
def optimal_solver(matrix, capacity, test_flag):

    # Extract the dimensions of the matrix
    rows, cols = matrix.shape
    problem = pulp.LpProblem("Maximize_Nonzero_Elements", pulp.LpMaximize)

    # Define vector of transmission as decision variable
    vector_tx = [pulp.LpVariable(f'x{i}', cat='Binary', lowBound=0, upBound=1) for i in range(rows)]

    # Compute the controller vector as the product of row vector_tx and visibility matrix
    controller_vector = np.array([pulp.lpSum(vector_tx[j] * column[j] for j in range(rows)) for column in matrix.T])

    # Define a auxiliary vector called non_zero_vector 
    non_zero_vector = [pulp.LpVariable(f'z{i}', cat='Binary', lowBound=0, upBound=1) for i in range(rows)]
    for index in range(len(controller_vector)):
        # it is forced to be 1 when the controller vector is greater than 0 
        # it is forced to be 0 when the controller vector is equal to 0
        problem += controller_vector[index] <= 10000 * non_zero_vector[index] 
        problem += non_zero_vector[index] <=  controller_vector[index] 

   
    # Objective function is the maximization of the sum of binary variables in non_zero_vector
    # indeed we want to maximize the number of non zero element in the controller_vector
    objective = pulp.lpSum(non_zero_vector)
    problem += objective

    # Add constraint on the capacity: the total number of transmissions must not exceed the maximum permitted capacity
    problem += pulp.lpSum(vector_tx) <= capacity

    # Solve the problem
    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    
    x=[] # Vector tx found by the solver
    z=[] # Non-zero vector found by the solver

    for i in range(len(vector_tx)):
        x.append(int(pulp.value(vector_tx[i])))
        z.append(int(pulp.value(non_zero_vector[i])))

    x=np.array(x)
    #print("Non-zero vector = ",z)

    # Resulting controller vector  
    y = np.array([np.dot(x, column) for column in matrix.T])
    y = y.astype(int)

    # Print the statistics of the solver
    if(test_flag):
        return return_statistics(x,y,matrix,capacity)
    else:
        print_statistics(x,y,matrix,capacity)
    


# ***********************************************************
#                                                           *
# 2ND METHOD: NON OPTIMAL SOLUTION                          *
#                                                           *
# ***********************************************************

def non_optimal_solver(matrix,capacity,test_flag):

    # Extract the dimensions of the matrix
    rows, cols = matrix.shape

    problem1 = pulp.LpProblem("Maximize_Elements_Sum", pulp.LpMaximize)

    # Define vector of transmission as decision variable
    vector_tx = [pulp.LpVariable(f'x{i}', cat='Binary') for i in range(rows)]

    # Compute the controller vector as the product of row vector_tx and visibility matrix
    controller_vector = np.array([pulp.lpSum(vector_tx[j] * column[j] for j in range(rows)) for column in matrix.T])

    # Objective function is the maximization of the sum of elements in controller_vector
    objective = pulp.lpSum(controller_vector)
    problem1 += objective

    # Add constraint on the capacity: the total number of transmissions must not exceed the maximum permitted capacity
    problem1 += pulp.lpSum(vector_tx) <= capacity

    # Solve the problem
    problem1.solve(pulp.PULP_CBC_CMD(msg=0))


    x=[] # Vector tx found by the solver
    for i in range(len(vector_tx)):
        x.append(int(pulp.value(vector_tx[i])))
    x=np.array(x)
    
    # Resulting controller vector 
    y = np.array([np.dot(x, column) for column in matrix.T])
    y = y.astype(int) 

    #Print the statistics of the solver
    if(test_flag):
        return return_statistics(x,y,matrix,capacity)
    else:
        print_statistics(x,y,matrix,capacity)



# ***********************************************************
#                                                           *
# 3RD METHOD: RANDOM SOLUTION                               *
#                                                           *
# ***********************************************************

def random_solver(matrix, capacity, car_positions, test_flag):
    
    # Extract the dimensions of the matrix
    rows, cols = matrix.shape

    # Compute a RANDOM vector tx
    # First set all entries to 0
    vector_tx = np.zeros(rows)
    
    # Calculate the number of entries of car_positions to discard
    # the remain car_positions will contributes as 1s in vector_tx
    num_entries = len(car_positions)
    if(num_entries>capacity):
        num_to_discard = len(car_positions)-capacity
    else:
        num_to_discard = 0

    # Generate random indices to discard positions
    indices_to_discard = np.random.choice(num_entries, size=num_to_discard, replace=False)

    # Remove the entries at the selected indices
    new_car_positions = np.delete(car_positions, indices_to_discard)

    for i in range(len(new_car_positions)):
        vector_tx[new_car_positions[i]]=1

    vector_tx = vector_tx.astype(int)

    # Resulting controller vector 
    controller_vector = np.array([np.dot(vector_tx, column) for column in matrix.T])
    controller_vector = controller_vector.astype(int)

    #Print the statistics of the solver
    if(test_flag):
        return return_statistics(vector_tx,controller_vector,matrix,capacity)
    else:
        print_statistics(vector_tx,controller_vector,matrix,capacity)
