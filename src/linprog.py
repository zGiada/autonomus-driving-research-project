import pulp
import numpy as np

# Create a random matrix
matrix = np.zeros((4, 4), dtype=int)
matrix[1::2, ::2] = 1
matrix[::2, 1::2] = 1
#matrix[3,::]=0

print("Matrix:")
print(matrix)

# Extract the dimensions of the matrix
rows, cols = matrix.shape

# Create a linear programming problem instance
problem = pulp.LpProblem("Matrix_LP_Problem", pulp.LpMinimize)

# Define the vector elements as decision variables
vector_tx = [pulp.LpVariable(f'x{i}', lowBound=0) for i in range(rows)]

# Set the objective function
vector1=np.ones(rows)
product = [np.dot(vector1, column) for column in matrix.T]
print(product)
objective = pulp.lpSum(vector_tx)
problem += objective

# Add the constraints 
for i in range(rows):
    vector_y = [np.dot(vector_tx, column) for column in matrix.T]
    for entry in vector_y:
        problem += entry >= 1  # Set lower bound constraint for each entry

# Solve the problem
problem.solve()

# Print the solution status
print("Solution status:", pulp.LpStatus[problem.status])

# Print the optimal solution
print("Optimal solution:")
x=[]
for i in range(len(vector_tx)):
    x.append(pulp.value(vector_tx[i]))
    print(f"x{i} =", pulp.value(vector_tx[i]))

print("Objective value =", pulp.value(problem.objective))
vector_y_result = [np.dot(x, column) for column in matrix.T]

print("vector y = ", vector_y_result)
print("Tot cells transmitted = ", np.sum(vector_y_result))
print("Efficency = ", rows/np.sum(vector_y_result))

#print("Optimal solution:")
#for i, variable in enumerate(problem.variables()):
#    print(variable.name, "=", variable.varValue)