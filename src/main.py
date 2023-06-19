from classes.matrics import *

# ***********************************************************
#                                                           *
# PART 1: input value number of rows and number of columns  *
#                                                           *
# ***********************************************************

def check_value(x):
    while x<=0 or x>6:
        x = int(input("Wrong value! Enter again: "))
    return x

print("\n>> Setting dimensions...")
rows = check_value(int(input("Enter rows: ")))
cols = check_value(int(input("Enter cols: ")))




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
# PART 3: ask number of car on the crossroads               *
#                                                           *
# ***********************************************************
num_cars = int(input("\n>> How many cars do you want to insert? Answer: "))
while num_cars<2 or num_cars>(np.count_nonzero(occupation_matrix == 0))/3: # 3 messo a caso
    num_cars = int(input("Wrong value! Insert again: "))

complete_occupation_matrix = create_occ.insert_cars(occupation_matrix, num_cars)
print(complete_occupation_matrix,"\n")

#m_vis_1 = Visibility(rows, cols)
#print(m_occup.return_dims_occupation())
#print(m_occup.create_occupation_matrix())
#print(m_vis_1.return_dims_occupation())